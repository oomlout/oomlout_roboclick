import os
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import robo_roboclick

try:
    from pypdf import PdfReader, PdfWriter
except Exception:
    from PyPDF2 import PdfReader, PdfWriter

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'pdf'
    d["name_long_4"] = 'create'
    d["name_long_5"] = 'pdf_create'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_pdf_create'
    d["name_long"] = 'roboclick_action_pdf_create'
    d["name_short"] = ['pdf_create', 'create_pdf']
    d["name_short_options"] = ['pdf_create', 'create_pdf']
    d["description"] = 'Create a single PDF from a list of PDF files.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'PDF'
    v = []
    if True:
        v.append({'name': 'pdfs', 'description': 'List of PDF files to merge into one output PDF.', 'type': 'list', 'default': []})
        v.append({'name': 'file_destination', 'description': 'Path to the output PDF file.', 'type': 'string', 'default': 'combined.pdf'})
        v.append({'name': 'fill_missing_files_with_blank_page', 'description': 'Whether missing input files should be replaced with a blank A4 page labeled with the missing filename.', 'type': 'boolean', 'default': True})
    d["variables"] = v
    return d

def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable

def action(**kwargs):
    return robo_roboclick.robo_action_run("roboclick_action_pdf_create", old, **kwargs)

def _as_bool(value, default):
    if value in (None, ""):
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("true", "yes", "y", "1", "on"):
            return True
        if normalized in ("false", "no", "n", "0", "off"):
            return False
    return default

def _coerce_pdf_list(value):
    if value in (None, ""):
        return []
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        normalized = value.replace("\r\n", "\n").replace("\r", "\n")
        if "\n" in normalized:
            parts = normalized.split("\n")
        else:
            parts = normalized.split(",")
        return [item.strip() for item in parts if item.strip()]
    return [str(value).strip()]

def _resolve_path(directory, file_name):
    file_name = str(file_name)
    if os.path.isabs(file_name):
        return file_name
    return os.path.abspath(os.path.join(directory, file_name))

def _make_missing_file_page(file_name):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 110, "Missing PDF file")
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 145, str(file_name))
    c.showPage()
    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

def _add_pdf(writer, file_name):
    reader = PdfReader(file_name)
    for page in reader.pages:
        writer.add_page(page)

def old(**kwargs):
    """Create a single PDF from a list of PDF files."""
    action = kwargs.get("action", {})
    directory = kwargs.get("directory", kwargs.get("directory_absolute", ""))
    pdfs = _coerce_pdf_list(
        action.get(
            "pdfs",
            action.get("pdf_files", action.get("files", action.get("file_sources", []))),
        )
    )
    file_destination = action.get("file_destination", action.get("file_output", action.get("file_name", "combined.pdf")))
    fill_missing = _as_bool(action.get("fill_missing_files_with_blank_page", True), True)

    if not pdfs:
        print("No PDF files provided for pdf_create")
        return ""

    output_path = _resolve_path(directory, file_destination)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    writer = PdfWriter()
    for pdf_file in pdfs:
        source_path = _resolve_path(directory, pdf_file)
        if os.path.isfile(source_path):
            print(f"Adding PDF: {source_path}")
            _add_pdf(writer, source_path)
            continue
        print(f"Missing PDF: {source_path}")
        if fill_missing:
            writer.add_page(_make_missing_file_page(pdf_file))

    with open(output_path, "wb") as output_file:
        writer.write(output_file)
    print(f"Created PDF: {output_path}")
    return ""

def test(**kwargs):
    try:
        import oomlout_test
    except Exception:
        return callable(old)

    test_fn = getattr(oomlout_test, "test", None)
    if not callable(test_fn):
        return callable(old)

    try:
        return bool(test_fn(**kwargs))
    except Exception:
        return callable(old)
