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
    """Test 4: define() documents retry_if_failed with a default of 1."""
    working = _load_working_module()
    metadata = working.define()
    variables = metadata.get("variables", [])
    retry_vars = [item for item in variables if isinstance(item, dict) and item.get("name") == "retry_if_failed"]
    passed = len(retry_vars) == 1 and retry_vars[0].get("default") == 1
    return {
        "passed": passed,
        "details": f"retry_vars={retry_vars!r}",
    }


def test_5(**kwargs):
    """Test 5: successful first save does not send a retry prompt."""
    working = _load_working_module()
    calls = _stub_robo(working, create_on_calls={1})
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = "image.png"
        working.action(
            directory_absolute=temp_dir,
            action={
                "file_name": file_name,
                "mode_ai_wait": "fast_clipboard_state",
            },
        )
        output_exists = (Path(temp_dir) / file_name).exists()
    passed = output_exists and calls["save_count"] == 1 and calls["pasted"] == []
    return {
        "passed": passed,
        "details": f"save_count={calls['save_count']}, pasted={calls['pasted']!r}, output_exists={output_exists}",
    }


def test_6(**kwargs):
    """Test 6: default retry_if_failed sends the retry prompt once and saves on the second attempt."""
    working = _load_working_module()
    calls = _stub_robo(working, create_on_calls={2})
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = "retry.png"
        working.action(
            directory_absolute=temp_dir,
            action={
                "file_name": file_name,
                "mode_ai_wait": "fast_clipboard_state",
            },
        )
        output_exists = (Path(temp_dir) / file_name).exists()
    retry_prompt = "oops the image seems to have not generated please try again"
    passed = output_exists and calls["save_count"] == 2 and calls["pasted"] == [retry_prompt]
    return {
        "passed": passed,
        "details": f"save_count={calls['save_count']}, pasted={calls['pasted']!r}, output_exists={output_exists}",
    }


def test_7(**kwargs):
    """Test 7: retry_if_failed false disables retry prompts and extra save attempts."""
    working = _load_working_module()
    calls = _stub_robo(working, create_on_calls=set())
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = "missing.png"
        working.action(
            directory_absolute=temp_dir,
            action={
                "file_name": file_name,
                "mode_ai_wait": "fast_clipboard_state",
                "retry_if_failed": False,
            },
        )
        output_exists = (Path(temp_dir) / file_name).exists()
    passed = not output_exists and calls["save_count"] == 1 and calls["pasted"] == []
    return {
        "passed": passed,
        "details": f"save_count={calls['save_count']}, pasted={calls['pasted']!r}, output_exists={output_exists}",
    }


def test_8(**kwargs):
    """Test 8: retry_if_failed controls the number of retry prompts after the first failure."""
    working = _load_working_module()
    calls = _stub_robo(working, create_on_calls={3})
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = "third_try.png"
        working.action(
            directory_absolute=temp_dir,
            action={
                "file_name": file_name,
                "mode_ai_wait": "fast_clipboard_state",
                "retry_if_failed": 2,
            },
        )
        output_exists = (Path(temp_dir) / file_name).exists()
    retry_prompt = "oops the image seems to have not generated please try again"
    passed = output_exists and calls["save_count"] == 3 and calls["pasted"] == [retry_prompt, retry_prompt]
    return {
        "passed": passed,
        "details": f"save_count={calls['save_count']}, pasted={calls['pasted']!r}, output_exists={output_exists}",
    }


def test_9(**kwargs):
    """Test 9: top-level retry_if_failed overrides the action value."""
    working = _load_working_module()
    calls = _stub_robo(working, create_on_calls=set())
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = "top_level_override.png"
        working.action(
            directory_absolute=temp_dir,
            retry_if_failed=False,
            action={
                "file_name": file_name,
                "mode_ai_wait": "fast_clipboard_state",
                "retry_if_failed": 2,
            },
        )
        output_exists = (Path(temp_dir) / file_name).exists()
    passed = not output_exists and calls["save_count"] == 1 and calls["pasted"] == []
    return {
        "passed": passed,
        "details": f"save_count={calls['save_count']}, pasted={calls['pasted']!r}, output_exists={output_exists}",
    }


def test_10(**kwargs):
    """Test 10: an invalid png is deleted and retried as a failed save."""
    working = _load_working_module()
    calls = _stub_robo(working, create_on_calls={2}, invalid_on_calls={1})
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = "bad_then_good.png"
        working.action(
            directory_absolute=temp_dir,
            action={
                "file_name": file_name,
                "mode_ai_wait": "fast_clipboard_state",
            },
        )
        output_path = Path(temp_dir) / file_name
        output_exists = output_path.exists()
        output_is_png = _path_is_png(output_path) if output_exists else False
    retry_prompt = "oops the image seems to have not generated please try again"
    passed = output_exists and output_is_png and calls["save_count"] == 2 and calls["pasted"] == [retry_prompt]
    return {
        "passed": passed,
        "details": f"save_count={calls['save_count']}, pasted={calls['pasted']!r}, output_exists={output_exists}, output_is_png={output_is_png}",
    }


def test_11(**kwargs):
    """Test 11: an invalid png is deleted even when retries are disabled."""
    working = _load_working_module()
    calls = _stub_robo(working, invalid_on_calls={1})
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = "bad_no_retry.png"
        working.action(
            directory_absolute=temp_dir,
            action={
                "file_name": file_name,
                "mode_ai_wait": "fast_clipboard_state",
                "retry_if_failed": False,
            },
        )
        output_exists = (Path(temp_dir) / file_name).exists()
    passed = not output_exists and calls["save_count"] == 1 and calls["pasted"] == []
    return {
        "passed": passed,
        "details": f"save_count={calls['save_count']}, pasted={calls['pasted']!r}, output_exists={output_exists}",
    }


def test(test_to_run="all", **kwargs):
    selected = _resolve_selected_tests(test_to_run)
    if not selected:
        _write_text(
            SUMMARY_FILE,
            "# roboclick_action_save_image_generated Tests\n\n"
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
        "# roboclick_action_save_image_generated Tests",
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

def _write_valid_png(path):
    from PIL import Image

    with Image.new("RGB", (1, 1), (255, 255, 255)) as img:
        img.save(path, format="PNG")

def _path_is_png(path):
    from PIL import Image

    try:
        with Image.open(path) as img:
            if img.format != "PNG":
                return False
            img.verify()
        return True
    except Exception:
        return False

def _stub_robo(working, create_on_calls=None, invalid_on_calls=None):
    if create_on_calls is None:
        create_on_calls = set()
    if invalid_on_calls is None:
        invalid_on_calls = set()
    calls = {
        "save_count": 0,
        "pasted": [],
        "ctrl": [],
    }

    def no_op(*args, **kwargs):
        return None

    def ctrl_generic(**kwargs):
        calls["ctrl"].append(kwargs.get("string", ""))

    def paste(**kwargs):
        calls["pasted"].append(kwargs.get("text", ""))

    def save_image(**kwargs):
        calls["save_count"] += 1
        if calls["save_count"] in create_on_calls or calls["save_count"] in invalid_on_calls:
            action = kwargs.get("action", {})
            file_name = action.get("file_name", "working.png")
            directory_absolute = kwargs.get("directory_absolute", "")
            output_path = Path(directory_absolute) / file_name
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if calls["save_count"] in invalid_on_calls:
                output_path.write_text("<html>not an image</html>", encoding="utf-8")
            else:
                _write_valid_png(output_path)

    working.robo_roboclick.robo_delay = no_op
    working.robo_roboclick.ai_wait_mode_fast_check = no_op
    working.robo_roboclick.ai_check_for_too_many_requests = no_op
    working.robo_roboclick.robo_mouse_click = no_op
    working.robo_roboclick.robo_keyboard_press_down = no_op
    working.robo_roboclick.robo_keyboard_press_backspace = no_op
    working.robo_roboclick.robo_keyboard_press_ctrl_generic = ctrl_generic
    working.robo_roboclick.robo_keyboard_paste = paste
    working.robo_roboclick.ai_save_image = save_image
    working.clean_png = no_op
    return calls


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
    print(f"roboclick_action_save_image_generated tests complete. selected={test_to_run} passed={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
