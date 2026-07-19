from __future__ import annotations

import datetime as _dt
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

import robo_roboclick
import yaml


REPAIR_TAG = "&&&repaired_structured_file_output&&&"
STRUCTURED_SUFFIXES = {".json", ".yaml", ".yml"}
YAML_SUFFIXES = {".yaml", ".yml"}
TOP_LEVEL_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*:\s*(.*)$")


def describe():
    d = {}
    d["name"] = "roboclick_action_file_verify_structured"
    d["name_long"] = "roboclick_action_file_verify_structured"
    d["name_short"] = [
        "verify_structured",
        "verify_yaml_json",
        "repair_yaml_json",
        "verify_files",
    ]
    d["name_short_options"] = list(d["name_short"])
    d["description"] = (
        "Validate a YAML or JSON file. If malformed, write an error report, "
        "back up the original, ask AI to repair it, validate the repair, and retry."
    )
    d["returns"] = "None on valid or repaired files; keeps moving on failure."
    d["category"] = "File"
    d["variables"] = [
        {"name": "file_name", "description": "YAML/JSON file to validate or repair.", "type": "string", "default": ""},
        {"name": "file_source", "description": "Alias for file_name.", "type": "string", "default": ""},
        {"name": "retries", "description": "Number of AI repair attempts after the initial validation failure.", "type": "number", "default": 1},
        {"name": "mode_ai_wait", "description": "AI wait strategy for the repair prompt.", "type": "string", "default": "slow"},
        {"name": "repair", "description": "Whether to attempt AI repair when invalid.", "type": "boolean", "default": True},
        {"name": "dry_run", "description": "Validate and report to stdout only; do not write reports, backups, repairs, or open AI.", "type": "boolean", "default": False},
    ]
    return d


def define():
    return describe()


def _as_bool(value: Any, default: bool = False) -> bool:
    if value in (None, ""):
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("1", "true", "yes", "y", "on"):
            return True
        if normalized in ("0", "false", "no", "n", "off"):
            return False
    return bool(value)


def _as_int(value: Any, default: int = 1) -> int:
    try:
        return max(0, int(value))
    except Exception:
        return default


def _resolve_file(raw_path: str, directory: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate

    cwd_candidate = Path.cwd() / candidate
    if cwd_candidate.exists():
        return cwd_candidate

    if directory:
        return Path(directory) / candidate
    return cwd_candidate


def _validate(path: Path) -> tuple[bool, str]:
    suffix = path.suffix.lower()
    if suffix not in STRUCTURED_SUFFIXES:
        return True, ""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except Exception as exc:
        return False, f"Could not read file: {exc}"

    return _validate_text(text, suffix)


def _validate_text(text: str, suffix: str) -> tuple[bool, str]:
    try:
        if suffix == ".json":
            json.loads(text)
        else:
            yaml.safe_load(text)
    except Exception as exc:
        return False, str(exc)
    return True, ""


def _next_non_ws(text: str, start: int) -> str | None:
    for ch in text[start:]:
        if not ch.isspace():
            return ch
    return None


def _normalize_json_string_quotes(text: str) -> tuple[str, bool]:
    """
    Escape quote characters that appear inside JSON strings.

    AI repairs sometimes produce values such as ""quoted phrase"" or
    "text with "inner quotes" here". In strict JSON, a string-ending quote
    must be followed by structural punctuation after optional whitespace.
    Anything else is treated as an unescaped literal quote.
    """
    out: list[str] = []
    in_string = False
    escaped = False
    changed = False

    for index, ch in enumerate(text):
        if not in_string:
            out.append(ch)
            if ch == '"':
                in_string = True
                escaped = False
            continue

        if escaped:
            out.append(ch)
            escaped = False
            continue

        if ch == "\\":
            out.append(ch)
            escaped = True
            continue

        if ch == '"':
            next_ch = _next_non_ws(text, index + 1)
            if next_ch is None or next_ch in ",]}:":
                out.append(ch)
                in_string = False
            else:
                out.append('\\"')
                changed = True
            continue

        out.append(ch)

    return "".join(out), changed


def _looks_like_top_level_key(line: str) -> bool:
    return bool(TOP_LEVEL_KEY_RE.match(line))


def _looks_like_top_level_scalar(line: str) -> bool:
    stripped = line.strip()
    if not stripped or line != line.lstrip():
        return False
    if stripped in ("---", "...") or stripped.startswith("#"):
        return False
    if stripped.startswith(("- ", "? ", ": ")):
        return False
    return not _looks_like_top_level_key(line)


def _normalize_yaml_naked_sequence_items(text: str) -> tuple[str, bool]:
    """
    Convert an empty top-level key followed by naked scalar lines into a list.

    A common AI YAML failure is:
        themes:
        "Theme one"
        "Theme two"

    PyYAML reads those scalar lines as invalid top-level simple keys. The
    intended structure is usually:
        themes:
          - "Theme one"
          - "Theme two"
    """
    out: list[str] = []
    pending_empty_key = False
    pending_blank_lines: list[str] = []
    changed = False

    for line in text.splitlines():
        key_match = TOP_LEVEL_KEY_RE.match(line)
        if key_match:
            if pending_empty_key:
                out.extend(pending_blank_lines)
                pending_blank_lines = []
            out.append(line)
            pending_empty_key = key_match.group(1).strip() == ""
            continue

        if pending_empty_key:
            if not line.strip():
                pending_blank_lines.append(line)
                continue
            if _looks_like_top_level_scalar(line):
                out.append(f"  - {line.strip()}")
                pending_blank_lines = []
                changed = True
                continue
            out.extend(pending_blank_lines)
            pending_blank_lines = []
            pending_empty_key = False

        out.append(line)

    if pending_empty_key:
        out.extend(pending_blank_lines)

    trailing_newline = "\n" if text.endswith(("\n", "\r\n")) else ""
    return "\n".join(out) + trailing_newline, changed


def _repair_with_yamlfix(text: str) -> tuple[str, str]:
    try:
        from yamlfix import fix_code
    except Exception:
        return text, ""

    try:
        repaired = fix_code(text)
    except Exception:
        return text, ""

    if repaired != text:
        return repaired, "formatted YAML with yamlfix"
    return text, ""


def _repair_structured_text_candidates(text: str, suffix: str) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []
    if suffix == ".json":
        repaired, changed = _normalize_json_string_quotes(text)
        if changed:
            candidates.append((repaired, "normalized unescaped quote characters inside JSON strings"))
    elif suffix in YAML_SUFFIXES:
        repaired, changed = _normalize_yaml_naked_sequence_items(text)
        if changed:
            yamlfix_repaired, yamlfix_note = _repair_with_yamlfix(repaired)
            if yamlfix_note:
                candidates.append((yamlfix_repaired, f"converted naked top-level YAML scalar lines into sequence items, then {yamlfix_note}"))
            candidates.append((repaired, "converted naked top-level YAML scalar lines into sequence items"))

        yamlfix_repaired, yamlfix_note = _repair_with_yamlfix(text)
        if yamlfix_note:
            candidates.append((yamlfix_repaired, yamlfix_note))

    return candidates


def _try_deterministic_source_repair(source_path: Path, destination_path: Path, suffix: str) -> tuple[bool, str]:
    if suffix not in STRUCTURED_SUFFIXES:
        return False, ""

    try:
        text = source_path.read_text(encoding="utf-8-sig")
    except Exception as exc:
        return False, f"Could not read source for deterministic repair: {exc}"

    last_error = ""
    for repaired, note in _repair_structured_text_candidates(text, suffix):
        ok, error = _validate_text(repaired, suffix)
        if ok:
            destination_path.write_text(repaired, encoding="utf-8")
            return True, note
        last_error = error

    if last_error:
        return False, f"deterministic repair did not produce valid structured data: {last_error}"
    return False, ""


def _try_deterministic_candidate_repair(path: Path) -> tuple[bool, str]:
    return _try_deterministic_source_repair(path, path, path.suffix.lower())


def _error_report_path(path: Path) -> Path:
    return path.with_name(f"{path.name}_error_report.md")


def _candidate_path(path: Path, attempt: int) -> Path:
    return path.with_name(f"{path.name}_repair_candidate_{attempt}{path.suffix.lower()}")


def _malformed_suffix(path: Path) -> str:
    return ".jsonerror" if path.suffix.lower() == ".json" else ".yamlerror"


def _move_malformed_file(path: Path) -> Path:
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S%f")
    malformed = path.with_name(f"{path.stem}_error_{stamp}{_malformed_suffix(path)}")
    path.rename(malformed)
    return malformed


def _write_error_report(path: Path, error: str, attempt: int, retries: int, note: str = "") -> None:
    report = _error_report_path(path)
    lines = [
        f"# Structured File Error Report",
        "",
        f"- File: `{path}`",
        f"- Attempt: {attempt} of {retries}",
        f"- Timestamp: {_dt.datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Parser Error",
        "",
        "```text",
        str(error).strip(),
        "```",
    ]
    if note:
        lines.extend(["", "## Note", "", note])
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _remove_stale_report(path: Path) -> None:
    report = _error_report_path(path)
    if report.exists():
        try:
            report.unlink()
        except OSError:
            pass


def _child_action(command: str, kwargs: dict[str, Any], action_cfg: dict[str, Any]) -> Any:
    discovered = kwargs.get("_discovered_actions")
    if discovered is None:
        import oomlout_roboclick

        discovered = oomlout_roboclick.build_action_lookup(actions_root=kwargs.get("actions_root"))

    action_info = discovered.get(command)
    if action_info is None:
        print(f"[verify_structured] unknown child action: {command}")
        return ""

    run_kwargs = dict(kwargs)
    run_kwargs["_discovered_actions"] = discovered
    run_kwargs["action"] = dict(action_cfg, command=command)
    return action_info.action_fn(**run_kwargs)


def _repair_prompt(path: Path, malformed_path: Path, kind: str, error: str) -> str:
    return f"""You are repairing one malformed {kind} file that has been uploaded.

Return only a syntactically valid {kind} document between these exact tags:

{REPAIR_TAG}
[repaired file here]
{REPAIR_TAG}

Rules:
- Preserve the original data, keys, order, names, numbers, and strings as closely as possible.
- Fix syntax only: missing commas, quotes, colons, indentation, brackets, braces, or YAML block scalar formatting.
- Do not add commentary, markdown fences, explanations, or replacement prose.
- For JSON, output strict JSON that can be parsed by json.loads.
- For JSON, escape literal quote characters inside strings as \\". Never output doubled string delimiters like ""quoted text"" or raw inner quotes like "text with "quoted" words".
- For YAML, output plain YAML that can be parsed by yaml.safe_load.
- For YAML, list values under a key must be indented sequence items, for example themes: followed by lines beginning with two spaces and "- ".
- If a value is ambiguous, preserve the nearest literal text from the uploaded file.
- Before returning JSON, mentally re-parse the entire output and fix the first remaining syntax error until no errors remain.

Original file: {path.name}
Uploaded malformed file: {malformed_path.name}
Parser error:
{error}
"""


def _try_ai_repair(
    path: Path,
    malformed_path: Path,
    attempt: int,
    mode_ai_wait: str,
    kwargs: dict[str, Any],
    error: str,
) -> Path:
    kind = "JSON" if path.suffix.lower() == ".json" else "YAML"
    candidate = _candidate_path(path, attempt)
    tab_opened = False
    try:
        result = _child_action(
            "new_chat",
            kwargs,
            {"description": f"Repair malformed {path.suffix.lower().lstrip('.')}: {path.name}"},
        )
        if result == "exit":
            raise RuntimeError("new_chat exited before repair could run")
        tab_opened = True

        _child_action("add_file", kwargs, {"file_name": str(malformed_path)})
        _child_action(
            "ai_query",
            kwargs,
            {
                "text": _repair_prompt(path, malformed_path, kind, error),
                "delay": 300,
                "method": "paste",
                "mode_ai_wait": mode_ai_wait,
            },
        )
        _child_action(
            "save_text",
            kwargs,
            {
                "file_name": str(candidate),
                "tag_open": REPAIR_TAG,
                "tag_close": REPAIR_TAG,
                "sanitize_text": False,
                "sanitize_double_linebreaks": False,
            },
        )
        return candidate
    finally:
        if tab_opened:
            _child_action("close_tab", kwargs, {})


def action(**kwargs):
    return robo_roboclick.robo_action_run("roboclick_action_file_verify_structured", _action_impl, **kwargs)


def _action_impl(**kwargs):
    action_cfg = kwargs.get("action", {}) or {}
    raw_file = action_cfg.get("file_name") or action_cfg.get("file_source") or ""
    if not raw_file:
        print("[verify_structured] no file_name or file_source set")
        return "missing"

    path = _resolve_file(str(raw_file), kwargs.get("directory", ""))
    if path.suffix.lower() not in STRUCTURED_SUFFIXES:
        print(f"[verify_structured] not YAML/JSON, skipping: {path}")
        return "skipped"
    if not path.exists():
        print(f"[verify_structured] file not found, skipping: {path}")
        return "missing"

    dry_run = _as_bool(action_cfg.get("dry_run", False), False)
    ok, error = _validate(path)
    if ok:
        if not dry_run:
            _remove_stale_report(path)
        print(f"[verify_structured] valid: {path}")
        return "valid"

    retries = _as_int(action_cfg.get("retries", 1), 1)
    repair_enabled = _as_bool(action_cfg.get("repair", True), True)
    mode_ai_wait = action_cfg.get("mode_ai_wait", "slow") or "slow"

    if dry_run:
        print(f"[verify_structured] invalid: {path}")
        print(f"[verify_structured] dry run only: {error}")
        return "invalid"

    malformed_path = _move_malformed_file(path)
    _write_error_report(
        path,
        error,
        attempt=0,
        retries=retries,
        note=f"Malformed file moved to `{malformed_path}`.",
    )
    print(f"[verify_structured] invalid: {path}")
    print(f"[verify_structured] malformed file moved to: {malformed_path}")

    repaired_locally, local_note = _try_deterministic_source_repair(malformed_path, path, path.suffix.lower())
    if repaired_locally:
        _remove_stale_report(path)
        print(f"[verify_structured] deterministic repair applied: {local_note}")
        print(f"[verify_structured] repaired: {path}")
        return "repaired"

    if not repair_enabled or retries <= 0:
        return "invalid"

    current_error = error
    for attempt in range(1, retries + 1):
        try:
            candidate = _try_ai_repair(path, malformed_path, attempt, mode_ai_wait, kwargs, current_error)
        except Exception as exc:
            current_error = f"AI repair attempt failed: {exc}"
            _write_error_report(path, current_error, attempt=attempt, retries=retries)
            continue

        repaired_deterministically, deterministic_note = _try_deterministic_candidate_repair(candidate)
        if repaired_deterministically:
            print(f"[verify_structured] deterministic repair applied: {deterministic_note}")

        ok, candidate_error = _validate(candidate)
        if ok:
            shutil.copyfile(candidate, path)
            ok, installed_error = _validate(path)
            if ok:
                _remove_stale_report(path)
                print(f"[verify_structured] repaired: {path}")
                return "repaired"
            current_error = installed_error
        else:
            current_error = candidate_error

        _write_error_report(path, current_error, attempt=attempt, retries=retries)
        print(f"[verify_structured] repair attempt {attempt} failed: {current_error}")

    print(f"[verify_structured] leaving original in place after {retries} failed repair attempt(s): {path}")
    return "failed"


def test(**kwargs):
    return callable(action)
