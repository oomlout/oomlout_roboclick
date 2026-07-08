import contextlib
import io
import re
import sys
import time
import tempfile
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

try:
    from pypdf import PdfReader
except Exception:
    from PyPDF2 import PdfReader


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
    """Test 2: define() returns a dict with basic metadata keys and aliases."""
    working = _load_working_module()
    metadata = working.define()
    aliases = metadata.get("name_short", [])
    required = ["name", "description", "variables", "category"]
    missing = [key for key in required if key not in metadata]
    passed = len(missing) == 0 and "pdf_create" in aliases and "create_pdf" in aliases
    return {
        "passed": passed,
        "details": f"missing_keys={missing}, aliases={aliases!r}",
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
    """Test 4: merges the provided PDFs in order."""
    working = _load_working_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        _write_pdf(temp_path / "one.pdf", "First PDF")
        _write_pdf(temp_path / "two.pdf", "Second PDF")
        working.action(
            directory=temp_dir,
            action={
                "pdfs": ["one.pdf", "two.pdf"],
                "file_destination": "combined.pdf",
            },
        )
        output = PdfReader(str(temp_path / "combined.pdf"))
        texts = [_page_text(page) for page in output.pages]
    passed = len(texts) == 2 and "First PDF" in texts[0] and "Second PDF" in texts[1]
    return {
        "passed": passed,
        "details": f"texts={texts!r}",
    }


def test_5(**kwargs):
    """Test 5: missing input PDFs are replaced with a labeled A4 page by default."""
    working = _load_working_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        _write_pdf(temp_path / "one.pdf", "First PDF")
        _write_pdf(temp_path / "two.pdf", "Second PDF")
        working.action(
            directory=temp_dir,
            action={
                "pdfs": ["one.pdf", "missing.pdf", "two.pdf"],
                "file_destination": "with_missing.pdf",
            },
        )
        output = PdfReader(str(temp_path / "with_missing.pdf"))
        texts = [_page_text(page) for page in output.pages]
        missing_page_size = (
            round(float(output.pages[1].mediabox.width)),
            round(float(output.pages[1].mediabox.height)),
        )
    a4_size = (round(A4[0]), round(A4[1]))
    passed = (
        len(texts) == 3
        and "First PDF" in texts[0]
        and "missing.pdf" in texts[1]
        and "Second PDF" in texts[2]
        and missing_page_size == a4_size
    )
    return {
        "passed": passed,
        "details": f"texts={texts!r}, missing_page_size={missing_page_size}, a4_size={a4_size}",
    }


def test_6(**kwargs):
    """Test 6: fill_missing_files_with_blank_page false skips missing input PDFs."""
    working = _load_working_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        _write_pdf(temp_path / "one.pdf", "First PDF")
        _write_pdf(temp_path / "two.pdf", "Second PDF")
        working.action(
            directory=temp_dir,
            action={
                "pdfs": ["one.pdf", "missing.pdf", "two.pdf"],
                "file_destination": "skip_missing.pdf",
                "fill_missing_files_with_blank_page": False,
            },
        )
        output = PdfReader(str(temp_path / "skip_missing.pdf"))
        texts = [_page_text(page) for page in output.pages]
    passed = len(texts) == 2 and "First PDF" in texts[0] and "Second PDF" in texts[1]
    return {
        "passed": passed,
        "details": f"texts={texts!r}",
    }


def test_7(**kwargs):
    """Test 7: comma-separated PDF lists are accepted."""
    working = _load_working_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        _write_pdf(temp_path / "one.pdf", "First PDF")
        _write_pdf(temp_path / "two.pdf", "Second PDF")
        working.action(
            directory=temp_dir,
            action={
                "pdfs": "one.pdf, two.pdf",
                "file_destination": "comma.pdf",
            },
        )
        output = PdfReader(str(temp_path / "comma.pdf"))
        texts = [_page_text(page) for page in output.pages]
    passed = len(texts) == 2 and "First PDF" in texts[0] and "Second PDF" in texts[1]
    return {
        "passed": passed,
        "details": f"texts={texts!r}",
    }


def test(test_to_run="all", **kwargs):
    selected = _resolve_selected_tests(test_to_run)
    if not selected:
        _write_text(
            SUMMARY_FILE,
            "# roboclick_action_pdf_create Tests\n\n"
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
        "# roboclick_action_pdf_create Tests",
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


def _write_pdf(path, text):
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setFont("Helvetica", 12)
    c.drawString(72, A4[1] - 72, text)
    c.showPage()
    c.save()


def _page_text(page):
    try:
        return page.extract_text() or ""
    except Exception:
        return ""


def _write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


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
    print(f"roboclick_action_pdf_create tests complete. selected={test_to_run} passed={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
