import tempfile
import xml.etree.ElementTree as ET
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from PIL import Image, ImageDraw


BASE_DIR = Path(__file__).resolve().parent


def _load_working():
    path = BASE_DIR / "working.py"
    spec = spec_from_file_location("roboclick_action_image_trace_vector_test", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _make_test_image(path, inverted=False):
    background = 0 if inverted else 255
    foreground = 255 if inverted else 0
    image = Image.new("L", (256, 256), background)
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 240, 240), fill=foreground)
    draw.ellipse((42, 42, 214, 214), fill=background)
    draw.rounded_rectangle((82, 74, 174, 190), radius=25, fill=foreground)
    draw.ellipse((108, 105, 148, 145), fill=background)
    image.save(path)


def _run_trace(inverted=False):
    working = _load_working()
    temporary = tempfile.TemporaryDirectory()
    folder = Path(temporary.name)
    source = folder / "source.png"
    destination = folder / "trace.svg"
    _make_test_image(source, inverted=inverted)
    result = working.trace_image_to_svg(source, destination, invert="auto")
    svg = destination.read_text(encoding="utf-8")
    return temporary, result, svg


def test(test_to_run="all", **kwargs):
    working = _load_working()
    metadata = working.define()
    aliases_ok = "image_trace_vector" in metadata.get("name_short", [])

    temporary, result, svg = _run_trace(inverted=False)
    try:
        ET.fromstring(svg)
        structure_ok = all(
            token in svg
            for token in (
                'inkscape:label="Trace"',
                'id="trace-path"',
                'fill-rule="evenodd"',
                " C ",
            )
        )
        structure_ok = structure_ok and svg.count('inkscape:groupmode="layer"') == 1
        normal_ok = result["contours"] >= 4
    finally:
        temporary.cleanup()

    inverted_temporary, inverted_result, inverted_svg = _run_trace(inverted=True)
    try:
        ET.fromstring(inverted_svg)
        inverted_ok = inverted_result["contours"] >= 4
    finally:
        inverted_temporary.cleanup()

    passed = aliases_ok and structure_ok and normal_ok and inverted_ok
    print(
        "image_trace_vector tests: "
        f"aliases={aliases_ok} structure={structure_ok} "
        f"normal={normal_ok} inverted={inverted_ok}"
    )
    return passed


if __name__ == "__main__":
    raise SystemExit(0 if test() else 1)
