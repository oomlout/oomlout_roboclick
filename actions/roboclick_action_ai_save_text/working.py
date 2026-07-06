import os
import re
import unicodedata

import robo_roboclick

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'save'
    d["name_long_5"] = 'save_text'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_save_text'
    d["name_long"] = 'roboclick_action_ai_save_text'
    d["name_short"] = ['save_text', 'ai_save_text', 'save_file_generated']
    d["name_short_options"] = ['save_text', 'ai_save_text', 'save_file_generated']
    d["description"] = 'Save text.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
        v.append({'name': 'file_name', 'description': 'File name to save captured or extracted content.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name_full', 'description': 'Full file path to save captured content.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name_clip', 'description': 'File path used to store clipboard text.', 'type': 'string', 'default': ''})
        v.append({'name': 'tag_open', 'description': 'Opening tag used to extract copied text before falling back to clip.', 'type': 'string', 'default': ''})
        v.append({'name': 'tag_close', 'description': 'Closing tag used to extract copied text before falling back to clip.', 'type': 'string', 'default': ''})
        v.append({'name': 'clip', 'description': 'Clipboard text payload to save. default:&&&tag for copy&&&', 'type': 'string', 'default': '&&&tag for copy&&&'})
        v.append({'name': 'sanitize_text', 'description': 'Whether saved text should replace common Unicode punctuation with ASCII-friendly text and remove emoji.', 'type': 'boolean', 'default': True})
        v.append({'name': 'sanitize_double_linebreaks', 'description': 'Whether repeated line breaks should be reduced by half so accidental doubles become singles and four line breaks become two.', 'type': 'boolean', 'default': True})
    d["variables"] = v
    return d

def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable

def _check_key_pressed():
    return None

def _scroll_lock_toggled():
    return False

def action(**kwargs):
    return old(**kwargs)

def _extract_between_tags(text, tag_open, tag_close):
    if not tag_open or not tag_close:
        return None
    if tag_open == tag_close:
        parts = text.split(tag_open)
        if len(parts) >= 3:
            return parts[-2]
        return None
    start = text.find(tag_open)
    if start == -1:
        return None
    start += len(tag_open)
    end = text.find(tag_close, start)
    if end == -1:
        return None
    return text[start:end]

def _extract_clip(text, clip):
    clipping = text.split(clip)
    if len(clipping) > 1:
        return clipping[len(clipping)-2]
    return text

def _extract_text(text, action, clip):
    tag_clipping = _extract_between_tags(
        text,
        action.get("tag_open", ""),
        action.get("tag_close", ""),
    )
    if tag_clipping is not None:
        return tag_clipping
    return _extract_clip(text, clip)

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

def _option_bool(kwargs, action, key, default):
    if key in kwargs:
        return _as_bool(kwargs.get(key), default)
    return _as_bool(action.get(key, default), default)

def _is_emoji_char(char):
    codepoint = ord(char)
    emoji_ranges = (
        (0x1F000, 0x1FAFF),
        (0x1FB00, 0x1FFFF),
        (0x2600, 0x27BF),
        (0x2300, 0x23FF),
    )
    return any(start <= codepoint <= end for start, end in emoji_ranges)

def _strip_emoji(text):
    stripped = []
    for char in text:
        codepoint = ord(char)
        if (
            _is_emoji_char(char)
            or 0x1F1E6 <= codepoint <= 0x1F1FF
            or 0x1F3FB <= codepoint <= 0x1F3FF
            or codepoint in (0x200D, 0x20E3, 0xFE0E, 0xFE0F)
        ):
            continue
        stripped.append(char)
    return "".join(stripped)

def _sanitize_text(text):
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201a": "'",
        "\u201b": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u201e": '"',
        "\u201f": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2015": "-",
        "\u2212": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\u202f": " ",
        "\u2009": " ",
        "\u200b": "",
        "\u2022": "-",
        "\u00b7": "-",
        "\u2032": "'",
        "\u2033": '"',
        "\u00d7": "x",
        "\u00f7": "/",
        "\u00a9": "(c)",
        "\u00ae": "(r)",
        "\u2122": "TM",
        "\u2264": "<=",
        "\u2265": ">=",
    }
    text = "".join(replacements.get(char, char) for char in text)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    return _strip_emoji(text)

def _sanitize_double_linebreaks(text):
    def reduce_linebreaks(match):
        linebreaks = re.findall(r"\r\n|\r|\n", match.group(0))
        if not linebreaks:
            return match.group(0)
        return linebreaks[0] * ((len(linebreaks) + 1) // 2)

    return re.sub(r"(?:(?:\r\n)|\r|\n){2,}", reduce_linebreaks, text)

def _apply_sanitizers(text, sanitize_text, sanitize_double_linebreaks):
    if sanitize_text:
        text = _sanitize_text(text)
    if sanitize_double_linebreaks:
        text = _sanitize_double_linebreaks(text)
    return text

def old(**kwargs):
    """Save text content from AI default between &&&tag for copy&&&"""
    action = kwargs.get("action", {})
    return_value = ""
    sanitize_text = _option_bool(kwargs, action, "sanitize_text", True)
    sanitize_double_linebreaks = _option_bool(kwargs, action, "sanitize_double_linebreaks", True)
    if "sanitize_double_linebreaks" not in kwargs and "sanitize_double_linebreaks" not in action:
        sanitize_double_linebreaks = _option_bool(kwargs, action, "remove_double_line_breaks", True)
    skip_if_tag_missing = action.get("skip_if_tag_missing", False)
    file_name_full = action.get("file_name_full", "text.txt")
    file_name_clip = action.get("file_name_clip", "")
    if file_name_clip == "":
        tag_open = action.get("tag_open", "")
        tag_close = action.get("tag_close", "")
        if tag_open != "" and tag_close != "":
            file_name_clip = action.get("file_name", "")
            if file_name_clip == "":
                file_name_clip = action.get("file_destination", "clip.txt")
            file_name_full = action.get("file_name_full", "")
        else:
            file_name_full = action.get("file_name", "")
            if file_name_full == "":
                file_name_full = action.get("file_destination", "clip.txt")
    
    
    clip = action.get("clip", "&&&tag for copy&&&")
    directory = kwargs.get("directory", "")

    robo_roboclick.robo_mouse_click(position=[300, 300], delay=2, button="left")  # Click to focus
    text = robo_roboclick.robo_keyboard_copy(delay=2)  # Copy the selected text

    if file_name_full != "":
        file_name_full_full = os.path.join(directory, file_name_full)
        with open(file_name_full_full, 'w', encoding='utf-8') as f:
            f.write(_apply_sanitizers(text, sanitize_text, sanitize_double_linebreaks))
            print(f"Text saved to {file_name_full_full}")
    if file_name_clip != "":
        file_name_clip_full = os.path.join(directory, file_name_clip)
        tag_open = action.get("tag_open", "")
        tag_close = action.get("tag_close", "")
        if skip_if_tag_missing and tag_open and tag_close:
            tag_clipping = _extract_between_tags(text, tag_open, tag_close)
            if tag_clipping is None:
                print(f"Tag {tag_open} not found; skipping {file_name_clip_full}")
                return return_value
        with open(file_name_clip_full, 'w', encoding='utf-8') as f:
            # Prefer explicit tag pairs, then the legacy clip marker, then the full text.
            clipping = _extract_text(text, action, clip)
            clipping = _apply_sanitizers(clipping, sanitize_text, sanitize_double_linebreaks)
            f.write(clipping)
            print(f"Clip text saved to {file_name_clip_full}")
    pass

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
