import os
from pathlib import Path

import robo_roboclick


d = {}


def describe():
    global d
    d = {}
    d["name"] = "roboclick_action_image_resize"
    d["name_long"] = "roboclick_action_image_resize"
    d["name_short"] = ["image_resize", "resize_image", "image_thumbnail"]
    d["name_short_options"] = ["image_resize", "resize_image", "image_thumbnail"]
    d["description"] = "Resize an image proportionally so its largest side is at most the requested pixel size."
    d["returns"] = "The destination image path, or an empty string when the source cannot be resized."
    d["category"] = "Image"
    d["variables"] = [
        {"name": "file_source", "description": "Path to the source image.", "type": "string", "default": ""},
        {"name": "file_destination", "description": "Path to the resized image.", "type": "string", "default": ""},
        {"name": "maximum_dimension", "description": "Maximum width or height in pixels.", "type": "integer", "default": 300},
        {"name": "allow_upscale", "description": "Whether images smaller than the limit may be enlarged.", "type": "boolean", "default": False},
        {"name": "resample", "description": "Pillow resampling mode: nearest, lanczos, bicubic, or bilinear.", "type": "string", "default": "lanczos"},
        {"name": "regenerate_pngs", "description": "Replace the destination when it already exists.", "type": "boolean", "default": False},
    ]
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    return dict(d)


def action(**kwargs):
    return robo_roboclick.robo_action_run("roboclick_action_image_resize", old, **kwargs)


def _absolute_path(directory, filename):
    path = Path(str(filename))
    if not path.is_absolute():
        path = Path(directory) / path
    return path.resolve()


def _as_boolean(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ["1", "true", "yes", "on"]


def old(**kwargs):
    """Resize one image without changing its aspect ratio."""
    action_details = kwargs.get("action", {})
    directory = kwargs.get("directory", "")

    file_source = action_details.get("file_source", action_details.get("file_input", ""))
    if file_source == "":
        print("file_source is not set, skipping image resize")
        return ""

    file_destination = action_details.get(
        "file_destination",
        action_details.get("file_output", ""),
    )
    if file_destination == "":
        source_path = Path(str(file_source))
        file_destination = f"{source_path.stem}_300{source_path.suffix}"

    source_path = _absolute_path(directory, file_source)
    destination_path = _absolute_path(directory, file_destination)
    maximum_dimension = int(action_details.get("maximum_dimension", 300))
    allow_upscale = _as_boolean(action_details.get("allow_upscale", False))
    regenerate_pngs = _as_boolean(
        action_details.get("regenerate_pngs", kwargs.get("regenerate_pngs", False))
    )

    if destination_path.is_file() and not regenerate_pngs:
        print(f"Keeping existing image {destination_path}")
        return str(destination_path)

    if maximum_dimension <= 0:
        print("maximum_dimension must be greater than zero, skipping image resize")
        return ""
    if not source_path.is_file():
        print(f"file_source {source_path} does not exist, skipping image resize")
        return ""

    from PIL import Image, ImageOps

    resampling = getattr(Image, "Resampling", Image)
    resample_modes = {
        "nearest": resampling.NEAREST,
        "lanczos": resampling.LANCZOS,
        "bicubic": resampling.BICUBIC,
        "bilinear": resampling.BILINEAR,
    }
    resample = resample_modes.get(
        str(action_details.get("resample", "lanczos")).lower(),
        resampling.LANCZOS,
    )

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source_path) as source_image:
        source_image = ImageOps.exif_transpose(source_image)
        source_width, source_height = source_image.size
        largest_side = max(source_width, source_height)
        scale = maximum_dimension / largest_side
        if not allow_upscale:
            scale = min(1.0, scale)

        destination_width = max(1, round(source_width * scale))
        destination_height = max(1, round(source_height * scale))
        resized_image = source_image.resize(
            (destination_width, destination_height),
            resample,
        )
        resized_image.save(destination_path)

    print(
        f"Image resized proportionally to {destination_width} x {destination_height} "
        f"and saved to {destination_path}"
    )
    return str(destination_path)


def test(**kwargs):
    return callable(old) and callable(action) and isinstance(define(), dict)
