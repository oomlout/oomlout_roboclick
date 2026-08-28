import html
import math
from pathlib import Path

import robo_roboclick


d = {}


def describe():
    global d
    d = {
        "name": "roboclick_action_image_trace_vector",
        "name_long": "roboclick_action_image_trace_vector",
        "name_short": ["image_trace_vector", "trace_vector", "png_to_bezier_svg"],
        "name_short_options": ["image_trace_vector", "trace_vector", "png_to_bezier_svg"],
        "description": (
            "Trace a black-and-white raster image into closed cubic Bezier SVG paths. "
            "The SVG contains one clean compound path on one layer, with nested "
            "contours retained as holes."
        ),
        "returns": "Creates a structured vector SVG suitable for display, fabrication, and laser cutting.",
        "category": "Image",
        "variables": [
            {"name": "file_source", "description": "Black-and-white PNG/JPG source image.", "type": "string", "default": ""},
            {"name": "file_destination", "description": "Destination SVG path.", "type": "string", "default": "trace.svg"},
            {"name": "threshold", "description": "0-255 black/white threshold.", "type": "number", "default": 128},
            {"name": "invert", "description": "true, false, or auto based on border colour.", "type": "string", "default": "auto"},
            {"name": "simplify_tolerance_px", "description": "Contour simplification tolerance in source pixels.", "type": "number", "default": 1.5},
            {"name": "curve_smoothing", "description": "Catmull-Rom to cubic Bezier smoothing strength, 0-1.", "type": "number", "default": 0.75},
            {"name": "minimum_area_px", "description": "Discard contours smaller than this pixel area.", "type": "number", "default": 16},
            {"name": "output_width_mm", "description": "Physical SVG width in millimetres.", "type": "number", "default": 50},
        ],
    }
    return d


def define():
    global d
    if not d:
        describe()
    return dict(d)


def action(**kwargs):
    return robo_roboclick.robo_action_run("roboclick_action_image_trace_vector", old, **kwargs)


def _absolute_path(directory, value):
    path = Path(str(value))
    if path.is_absolute():
        return path
    return Path(directory) / path


def _clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def _format_number(value):
    value = 0.0 if abs(float(value)) < 0.0005 else float(value)
    return f"{value:.3f}".rstrip("0").rstrip(".")


def _limit_control(origin, control, maximum_distance):
    dx = control[0] - origin[0]
    dy = control[1] - origin[1]
    distance = math.hypot(dx, dy)
    if distance <= maximum_distance or distance == 0:
        return control
    scale = maximum_distance / distance
    return origin[0] + dx * scale, origin[1] + dy * scale


def _closed_bezier_path(points, smoothing):
    """Convert a closed point loop to cubic Beziers using bounded Catmull-Rom tangents."""
    count = len(points)
    if count < 3:
        return ""

    commands = [f"M {_format_number(points[0][0])} {_format_number(points[0][1])}"]
    for index in range(count):
        previous_point = points[(index - 1) % count]
        start_point = points[index]
        end_point = points[(index + 1) % count]
        next_point = points[(index + 2) % count]

        control_1 = (
            start_point[0] + (end_point[0] - previous_point[0]) * smoothing / 6.0,
            start_point[1] + (end_point[1] - previous_point[1]) * smoothing / 6.0,
        )
        control_2 = (
            end_point[0] - (next_point[0] - start_point[0]) * smoothing / 6.0,
            end_point[1] - (next_point[1] - start_point[1]) * smoothing / 6.0,
        )

        # Bounding tangent reach prevents a distant neighbouring vertex from
        # creating loops or spikes in tight laser-cut geometry.
        segment_length = max(0.001, math.dist(start_point, end_point))
        maximum_control_reach = segment_length * 0.55
        control_1 = _limit_control(start_point, control_1, maximum_control_reach)
        control_2 = _limit_control(end_point, control_2, maximum_control_reach)

        commands.append(
            "C "
            f"{_format_number(control_1[0])} {_format_number(control_1[1])} "
            f"{_format_number(control_2[0])} {_format_number(control_2[1])} "
            f"{_format_number(end_point[0])} {_format_number(end_point[1])}"
        )
    commands.append("Z")
    return " ".join(commands)


def _load_foreground_mask(file_source, threshold, invert):
    try:
        import cv2
        import numpy as np
        from PIL import Image
    except ImportError as error:
        raise RuntimeError(
            "image_trace_vector requires Pillow, numpy, and opencv-python-headless"
        ) from error

    with Image.open(file_source) as source_image:
        rgba = source_image.convert("RGBA")
        white = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        white.alpha_composite(rgba)
        grayscale = np.asarray(white.convert("L"), dtype=np.uint8)

    border = np.concatenate(
        (grayscale[0, :], grayscale[-1, :], grayscale[:, 0], grayscale[:, -1])
    )
    border_is_dark = float(np.median(border)) < threshold
    invert_text = str(invert).strip().lower()
    if invert_text in ("true", "1", "yes", "on"):
        foreground_is_light = True
    elif invert_text in ("false", "0", "no", "off"):
        foreground_is_light = False
    else:
        foreground_is_light = border_is_dark

    if foreground_is_light:
        mask = grayscale > threshold
    else:
        mask = grayscale < threshold
    return (mask.astype(np.uint8) * 255), cv2, np


def _extract_contours(mask, cv2, simplify_tolerance_px, minimum_area_px):
    import numpy as np

    # Padding guarantees a closed contour when artwork reaches an image edge.
    padded = np.pad(mask, 1, mode="constant", constant_values=0)
    contours, hierarchy = cv2.findContours(
        padded, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )
    if hierarchy is None:
        return []
    hierarchy = hierarchy[0]

    records = []
    for index, contour in enumerate(contours):
        area = abs(float(cv2.contourArea(contour)))
        if area < minimum_area_px:
            continue
        simplified = cv2.approxPolyDP(
            contour, epsilon=simplify_tolerance_px, closed=True
        ).reshape(-1, 2)
        if len(simplified) < 3:
            continue
        points = [
            (float(point[0] - 1), float(point[1] - 1))
            for point in simplified
        ]

        depth = 0
        parent = int(hierarchy[index][3])
        while parent != -1:
            depth += 1
            parent = int(hierarchy[parent][3])
        records.append({"area": area, "depth": depth, "points": points})

    # Largest outside contours first makes the SVG deterministic and easy to inspect.
    records.sort(key=lambda record: (-record["area"], record["depth"]))
    return records


def _build_svg(
    file_source,
    width_px,
    height_px,
    contours,
    curve_smoothing,
    output_width_mm,
    threshold,
    invert,
    simplify_tolerance_px,
    minimum_area_px,
):
    output_height_mm = output_width_mm * height_px / width_px
    paths = [
        _closed_bezier_path(record["points"], curve_smoothing)
        for record in contours
    ]
    paths = [path for path in paths if path]
    combined_path = " ".join(paths)
    source_name = html.escape(Path(file_source).name, quote=True)

    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     width="{_format_number(output_width_mm)}mm"
     height="{_format_number(output_height_mm)}mm"
     viewBox="0 0 {width_px} {height_px}" version="1.1">
  <title>Bezier trace of {source_name}</title>
  <desc>Closed fabrication contours traced from a black-and-white raster image.</desc>
  <metadata id="trace-settings">source={source_name}; threshold={threshold};
    invert={html.escape(str(invert), quote=True)};
    simplify-tolerance-px={_format_number(simplify_tolerance_px)};
    curve-smoothing={_format_number(curve_smoothing)};
    minimum-area-px={_format_number(minimum_area_px)};
    contour-count={len(paths)}</metadata>
  <g id="trace" inkscape:groupmode="layer" inkscape:label="Trace">
    <path id="trace-path" d="{combined_path}"
          fill="#000000" stroke="none" fill-rule="evenodd" clip-rule="evenodd"/>
  </g>
</svg>
'''


def trace_image_to_svg(
    file_source,
    file_destination,
    threshold=128,
    invert="auto",
    simplify_tolerance_px=1.5,
    curve_smoothing=0.75,
    minimum_area_px=16,
    output_width_mm=50,
):
    threshold = int(_clamp(float(threshold), 0, 255))
    simplify_tolerance_px = max(0.0, float(simplify_tolerance_px))
    curve_smoothing = _clamp(float(curve_smoothing), 0.0, 1.0)
    minimum_area_px = max(0.0, float(minimum_area_px))
    output_width_mm = max(0.001, float(output_width_mm))

    mask, cv2, _ = _load_foreground_mask(file_source, threshold, invert)
    height_px, width_px = mask.shape
    contours = _extract_contours(
        mask, cv2, simplify_tolerance_px, minimum_area_px
    )
    if not contours:
        raise ValueError("No traceable contours found in the source image")

    svg = _build_svg(
        file_source,
        width_px,
        height_px,
        contours,
        curve_smoothing,
        output_width_mm,
        threshold,
        invert,
        simplify_tolerance_px,
        minimum_area_px,
    )
    file_destination.parent.mkdir(parents=True, exist_ok=True)
    file_destination.write_text(svg, encoding="utf-8", newline="\n")
    return {"contours": len(contours), "width_px": width_px, "height_px": height_px}


def old(**kwargs):
    action_details = kwargs.get("action", {}) or {}
    directory = kwargs.get("directory", "")
    file_source_value = action_details.get(
        "file_source", action_details.get("file_input", "")
    )
    if not file_source_value:
        print("image_trace_vector requires file_source")
        return
    file_destination_value = action_details.get(
        "file_destination", action_details.get("file_output", "trace.svg")
    )
    file_source = _absolute_path(directory, file_source_value).resolve()
    file_destination = _absolute_path(directory, file_destination_value).resolve()
    if not file_source.is_file():
        print(f"file_source {file_source} does not exist, skipping vector trace")
        return

    try:
        result = trace_image_to_svg(
            file_source=file_source,
            file_destination=file_destination,
            threshold=action_details.get("threshold", 128),
            invert=action_details.get("invert", "auto"),
            simplify_tolerance_px=action_details.get("simplify_tolerance_px", 1.5),
            curve_smoothing=action_details.get("curve_smoothing", 0.75),
            minimum_area_px=action_details.get("minimum_area_px", 16),
            output_width_mm=action_details.get("output_width_mm", 50),
        )
    except Exception as error:
        print(f"Error tracing image {file_source}: {error}")
        return
    print(
        f"Vector trace saved to {file_destination} "
        f"({result['contours']} contours, {result['width_px']}x{result['height_px']} source)"
    )


def test(**kwargs):
    return callable(trace_image_to_svg) and callable(old)
