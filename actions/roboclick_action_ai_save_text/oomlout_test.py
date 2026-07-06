import contextlib
import io
import re
import sys
import time
import tempfile
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RESULT_DIR = BASE_DIR / "test_result"
SUMMARY_FILE = BASE_DIR / "test.md"
SUMMARY_ALL_FILE = BASE_DIR / "test_all.md"


def test_1(**kwargs):
    """Test 1: working.py exposes callable define() and action()."""
    working = _load_working_module()
    has_define = callable(getattr(working, "define", None))
    has_action = callable(getattr(working, "action", None))
    passed = has_define and has_action
    return {
        "passed": passed,
        "details": f"define={has_define}, action={has_action}",
    }


def test_2(**kwargs):
    """Test 2: define() returns a dict with basic metadata keys."""
    working = _load_working_module()
    define_fn = getattr(working, "define", None)
    if not callable(define_fn):
        return {"passed": False, "details": "define() missing"}
    metadata = define_fn()
    if not isinstance(metadata, dict):
        return {"passed": False, "details": "define() did not return dict"}
    required = ["name", "description", "variables", "category"]
    missing = [key for key in required if key not in metadata]
    return {
        "passed": len(missing) == 0,
        "details": f"missing_keys={missing}",
    }


def test_3(**kwargs):
    """Test 3: optional working.py test() callable executes successfully."""
    working = _load_working_module()
    working_test = getattr(working, "test", None)
    if not callable(working_test):
        return {"passed": True, "details": "working.test() not defined; skipped"}
    result = working_test(test_to_run="1")
    passed = bool(result)
    return {
        "passed": passed,
        "details": f"working_test_result={result!r}",
    }

def test_4(**kwargs):
    """Test 4: tag_open/tag_close extracts to file_name before legacy clip parsing."""
    working = _load_working_module()
    copied_text = (
        "before\n"
        "&&&song_seeds_output&&&\n"
        "[{\"moment\": \"stale\"}]\n"
        "&&&song_seeds_output&&&\n"
        "middle\n"
        "&&&song_seeds_output&&&\n"
        "[{\"moment\": \"opening\"}]\n"
        "&&&song_seeds_output&&&\n"
        "after &&&tag for copy&&&legacy&&&tag for copy&&&"
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        _stub_copy(working, copied_text)
        working.action(
            directory=temp_dir,
            action={
                "file_name": "song_seeds.json",
                "tag_open": "&&&song_seeds_output&&&",
                "tag_close": "&&&song_seeds_output&&&",
            },
        )
        output = (Path(temp_dir) / "song_seeds.json").read_text(encoding="utf-8")
    return {
        "passed": output.strip() == '[{"moment": "opening"}]',
        "details": f"output={output!r}",
    }


def test_5(**kwargs):
    """Test 5: missing tag_open/tag_close markers fall back to the legacy clip marker."""
    working = _load_working_module()
    copied_text = "before &&&tag for copy&&&legacy value&&&tag for copy&&& after"
    with tempfile.TemporaryDirectory() as temp_dir:
        _stub_copy(working, copied_text)
        working.action(
            directory=temp_dir,
            action={
                "file_name": "fallback.txt",
                "tag_open": "&&&missing_open&&&",
                "tag_close": "&&&missing_close&&&",
                "clip": "&&&tag for copy&&&",
            },
        )
        output = (Path(temp_dir) / "fallback.txt").read_text(encoding="utf-8")
    return {
        "passed": output == "legacy value",
        "details": f"output={output!r}",
    }

def test_6(**kwargs):
    """Test 6: sanitize_text and sanitize_double_linebreaks default to enabled."""
    working = _load_working_module()
    copied_text = (
        "Alpha\u2014beta \u201cquoted\u201d and \u2018single\u2019 "
        "smile\U0001f642\n\nGamma\n\n\n\nDelta"
    )
    expected = "Alpha-beta \"quoted\" and 'single' smile\nGamma\n\nDelta"
    with tempfile.TemporaryDirectory() as temp_dir:
        _stub_copy(working, copied_text)
        working.action(
            directory=temp_dir,
            action={
                "file_name": "sanitized.txt",
            },
        )
        output = (Path(temp_dir) / "sanitized.txt").read_text(encoding="utf-8")
    return {
        "passed": output == expected,
        "details": f"output={output!r}",
    }


def test_7(**kwargs):
    """Test 7: sanitize_text and sanitize_double_linebreaks can be disabled."""
    working = _load_working_module()
    copied_text = "Alpha\u2014beta smile\U0001f642\n\nGamma"
    with tempfile.TemporaryDirectory() as temp_dir:
        _stub_copy(working, copied_text)
        working.action(
            directory=temp_dir,
            action={
                "file_name": "unsanitized.txt",
                "sanitize_text": False,
                "sanitize_double_linebreaks": False,
            },
        )
        output = (Path(temp_dir) / "unsanitized.txt").read_text(encoding="utf-8")
    return {
        "passed": output == copied_text,
        "details": f"output={output!r}",
    }


def test_8(**kwargs):
    """Test 8: top-level kwargs can override sanitize options."""
    working = _load_working_module()
    copied_text = "Alpha\u2014beta smile\U0001f642\n\nGamma"
    with tempfile.TemporaryDirectory() as temp_dir:
        _stub_copy(working, copied_text)
        working.action(
            directory=temp_dir,
            sanitize_text=False,
            sanitize_double_linebreaks=False,
            action={
                "file_name": "kwargs_unsanitized.txt",
            },
        )
        output = (Path(temp_dir) / "kwargs_unsanitized.txt").read_text(encoding="utf-8")
    return {
        "passed": output == copied_text,
        "details": f"output={output!r}",
    }


def test(test_to_run="all", **kwargs):
    selected = _resolve_selected_tests(test_to_run)
    if not selected:
        _write_text(
            SUMMARY_FILE,
            "# roboclick_action_ai_save_text Tests\n\n"
            f"- Status: failed\n"
            f"- Reason: unknown test_to_run `{test_to_run}`\n",
        )
        return False

    all_available = _resolve_selected_tests("all")
    selected_names = {name for name, _ in selected}
    all_names = {name for name, _ in all_available}
    running_all = selected_names == all_names

    results = []
    for case_name, case_fn in selected:
        results.append(_run_case(case_name, case_fn, _get_test_description(case_fn), kwargs))

    passed = sum(1 for item in results if item["status"] == "passed")
    failed = len(results) - passed
    lines = [
        "# roboclick_action_ai_save_text Tests",
        "",
        f"- Selected: {test_to_run}",
        f"- Total: {len(results)}",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        "",
        "| Test | Description | Status | Duration (s) | Details |",
        "|---|---|---|---:|---|",
    ]
    for item in results:
        lines.append(
            f"| {item['name']} | {item['description'].replace('|', '/')} | "
            f"{item['status']} | {item['duration']:.3f} | "
            f"{item['details'].replace('|', '/')} |"
        )
    summary_content = "\n".join(lines) + "\n"
    _write_text(SUMMARY_FILE, summary_content)
    if running_all:
        _write_text(SUMMARY_ALL_FILE, summary_content)
    return failed == 0


def _load_working_module():
    working_file = BASE_DIR / "working.py"
    module_name = f"{BASE_DIR.name}_working_{abs(hash(str(working_file)))}"
    spec = spec_from_file_location(module_name, str(working_file))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load working module from {working_file}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def _stub_copy(working, copied_text):
    working.robo_roboclick.robo_mouse_click = lambda **kwargs: None
    working.robo_roboclick.robo_keyboard_copy = lambda **kwargs: copied_text


def _get_test_description(test_fn):
    doc = getattr(test_fn, "__doc__", "") or ""
    return " ".join(doc.strip().split())


def _resolve_selected_tests(test_to_run):
    tests = {}
    for name, value in globals().items():
        if not callable(value):
            continue
        if not re.match(r"^test_\d+$", name):
            continue
        tests[name] = value
    tests = dict(sorted(tests.items(), key=lambda item: int(item[0].split("_", 1)[1])))

    if test_to_run in (None, "", "all"):
        return list(tests.items())

    token = str(test_to_run).strip().lower()
    if token.isdigit():
        token = f"test_{token}"
    if token in tests:
        return [(token, tests[token])]
    return []


def _run_case(case_name, case_fn, description, case_kwargs):
    started = time.monotonic()
    log_buffer = io.StringIO()
    status = "passed"
    details = ""
    error_text = ""
    try:
        with contextlib.redirect_stdout(log_buffer), contextlib.redirect_stderr(log_buffer):
            result = case_fn(**case_kwargs)
        if isinstance(result, dict):
            passed = bool(result.get("passed", False))
            details = str(result.get("details", ""))
        else:
            passed = bool(result)
            details = f"raw_result={result!r}"
        status = "passed" if passed else "failed"
    except Exception as exc:
        status = "failed"
        error_text = repr(exc)
        details = "exception raised"

    elapsed = round(time.monotonic() - started, 3)
    lines = [
        f"# {case_name}",
        "",
        f"- Description: {description}",
        f"- Status: {status}",
        f"- Duration (s): {elapsed}",
        f"- Details: {details}",
    ]
    if error_text:
        lines.append(f"- Error: `{error_text}`")
    logs = log_buffer.getvalue().strip()
    if logs:
        lines.extend(["", "## Captured Output", "", "```text", logs, "```"])
    _write_text(RESULT_DIR / f"{case_name}.md", "\n".join(lines) + "\n")
    return {
        "name": case_name,
        "description": description,
        "status": status,
        "duration": elapsed,
        "details": details,
        "error": error_text,
    }


def main():
    test_to_run = "all"
    if len(sys.argv) > 1:
        test_to_run = sys.argv[1]
    ok = test(test_to_run=test_to_run)
    print(f"roboclick_action_ai_save_text tests complete. selected={test_to_run} passed={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
