import os
import robo_roboclick

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'image'
    d["name_long_4"] = 'remove'
    d["name_long_5"] = 'background'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_image_remove_background'
    d["name_long"] = 'roboclick_action_image_remove_background'
    d["name_short"] = ['image_remove_background', 'image_remove_background_keyed', 'remove_background']
    d["name_short_options"] = ['image_remove_background', 'image_remove_background_keyed', 'remove_background']
    d["description"] = 'Key a flat chroma screen background (green or magenta) out of an image, replacing it with real transparency, in place.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Image'
    v = []
    if True:
        v.append({'name': 'file_name', 'description': 'Image to process, relative to the part directory. Overwritten as an RGBA png.', 'type': 'string', 'default': ''})
        v.append({'name': 'color_key', 'description': 'Which screen colour to remove: green or magenta.', 'type': 'string', 'default': 'green'})
        v.append({'name': 'threshold_low', 'description': 'Keyness where edge feathering starts.', 'type': 'string', 'default': '20'})
        v.append({'name': 'threshold_high', 'description': 'Keyness treated as pure background.', 'type': 'string', 'default': '90'})
        v.append({'name': 'background_remove_all', 'description': 'Remove matching key-coloured pixels everywhere in the image. Set false to remove only the border-connected screen.', 'type': 'boolean', 'default': True})
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
    return robo_roboclick.robo_action_run("roboclick_action_image_remove_background", old, **kwargs)

def old(**kwargs):
    """Remove a chroma key screen from an image, leaving real transparency.

    By default all key-coloured pixels are removed, including screen visible
    through enclosed gaps inside the subject. Set ``background_remove_all``
    false to retain the older border-connected flood-fill behaviour when the
    subject itself intentionally contains the key colour. Edge pixels feather
    and get despilled so they don't fringe key-coloured.
    """
    try:
        import numpy as np
        from PIL import Image
    except Exception as error:
        print(f"image_remove_background needs numpy and pillow: {error}")
        return "exit_no_tab"

    action = kwargs.get("action", {})
    directory = kwargs.get("directory", "")
    file_name = action.get("file_name", "")
    color_key = action.get("color_key", "green")
    background_remove_all = action.get(
        "background_remove_all",
        kwargs.get("background_remove_all", True),
    )
    if isinstance(background_remove_all, str):
        background_remove_all = background_remove_all.strip().lower() not in {
            "0", "false", "no", "off", "",
        }
    else:
        background_remove_all = bool(background_remove_all)
    try:
        threshold_low = int(action.get("threshold_low", "20"))
        threshold_high = int(action.get("threshold_high", "90"))
    except (TypeError, ValueError):
        threshold_low, threshold_high = 20, 90

    if file_name == "":
        print("file_name not set, skipping image_remove_background")
        return ""

    file_path = file_name if os.path.isabs(file_name) else os.path.join(directory, file_name)
    if not os.path.isfile(file_path):
        print(f"image file {file_path} does not exist")
        return "exit_no_tab"

    pixels = np.array(Image.open(file_path).convert("RGBA"))

    # keyness: how strongly each pixel matches the screen colour
    # green: g - max(r, b)    magenta: min(r, b) - g
    r = pixels[..., 0].astype(np.int16)
    g = pixels[..., 1].astype(np.int16)
    b = pixels[..., 2].astype(np.int16)
    if color_key == "magenta":
        key = np.minimum(r, b) - g
    else:
        key = g - np.maximum(r, b)

    # By default remove every matching pixel. This also clears screen visible
    # through enclosed gaps (handles, arches, wheels, letter counters, etc.).
    # The opt-out retains the original border-connected flood fill for images
    # whose subject intentionally uses the chroma-key colour.
    from collections import deque
    candidate = key > threshold_low
    height, width = candidate.shape
    if background_remove_all:
        background = candidate.copy()
    else:
        background = np.zeros((height, width), dtype=bool)
        queue = deque()
        for col in range(width):
            for row in (0, height - 1):
                if candidate[row, col] and not background[row, col]:
                    background[row, col] = True
                    queue.append((row, col))
        for row in range(height):
            for col in (0, width - 1):
                if candidate[row, col] and not background[row, col]:
                    background[row, col] = True
                    queue.append((row, col))
        while queue:
            row, col = queue.popleft()
            for next_row, next_col in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
                if 0 <= next_row < height and 0 <= next_col < width:
                    if candidate[next_row, next_col] and not background[next_row, next_col]:
                        background[next_row, next_col] = True
                        queue.append((next_row, next_col))

    if not background.any():
        print(f"no {color_key} screen found touching the border of {file_path}, leaving image unchanged")
        return ""

    # alpha ramps from opaque at threshold_low down to clear at threshold_high,
    # so anti-aliased edge pixels feather instead of fringing
    fade = (key.astype(np.float32) - threshold_low) / float(threshold_high - threshold_low)
    fade = np.clip(fade, 0.0, 1.0)
    alpha = pixels[..., 3].astype(np.float32)
    alpha[background] *= 1.0 - fade[background]
    pixels[..., 3] = alpha.astype(np.uint8)

    # despill the surviving semi-transparent edge so it doesn't glow key-coloured
    edge = background & (pixels[..., 3] > 0)
    if edge.any():
        if color_key == "magenta":
            ceiling = g + threshold_low
            pixels[..., 0][edge] = np.minimum(r, ceiling)[edge].astype(np.uint8)
            pixels[..., 2][edge] = np.minimum(b, ceiling)[edge].astype(np.uint8)
        else:
            ceiling = np.maximum(r, b) + threshold_low
            pixels[..., 1][edge] = np.minimum(g, ceiling)[edge].astype(np.uint8)

    removed = int(background.sum())
    total = int(background.size)
    Image.fromarray(pixels, "RGBA").save(file_path)
    print(f"keyed {color_key} screen to transparency: {removed} of {total} pixels "
          f"({100 * removed / total:.1f}%), saved to {file_path}")
    return ""

def test(**kwargs):
    # Functional coverage lives in this action's oomlout_test.py. Importing it
    # here and calling test() recursively re-enters test_3 indefinitely.
    return callable(old)
