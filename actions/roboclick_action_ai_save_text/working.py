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
        v.append({'name': 'base_ai_provider', 'description': 'AI provider to use for this action. Options: open_ai, claude, gemini, open_web_ui.', 'type': 'string', 'default': 'open_ai'})
        v.append({'name': 'file_name', 'description': 'File name to save captured or extracted content.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name_full', 'description': 'Full file path to save captured content.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name_clip', 'description': 'File path used to store clipboard text.', 'type': 'string', 'default': ''})
        v.append({'name': 'tag_open', 'description': 'Opening tag used to extract copied text before falling back to clip.', 'type': 'string', 'default': ''})
        v.append({'name': 'tag_close', 'description': 'Closing tag used to extract copied text before falling back to clip.', 'type': 'string', 'default': ''})
        v.append({'name': 'clip', 'description': 'Clipboard text payload to save. default:&&&tag for copy&&&', 'type': 'string', 'default': '&&&tag for copy&&&'})
        v.append({'name': 'sanitize_text', 'description': 'Whether saved text should replace common Unicode punctuation with ASCII-friendly text and remove emoji.', 'type': 'boolean', 'default': True})
        v.append({'name': 'sanitize_double_linebreaks', 'description': 'Whether repeated line breaks should be reduced by half so accidental doubles become singles and four line breaks become two.', 'type': 'boolean', 'default': True})
        v.append({'name': 'position_click', 'description': 'Screen position to click before executing text copy.', 'type': 'string', 'default': ''})
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
    return robo_roboclick.robo_action_run("roboclick_action_ai_save_text", new, **kwargs)

def _get_action(kwargs):
    action = kwargs.get("action", {})
    if not isinstance(action, dict):
        action = {}
    return action

def _get_base_ai_provider(kwargs):
    action = _get_action(kwargs)
    workings = kwargs.get("workings", {})
    if not isinstance(workings, dict):
        workings = {}
    provider = kwargs.get("base_ai_provider", workings.get("base_ai_provider", action.get("base_ai_provider", "open_ai")))
    if provider in (None, ""):
        provider = "open_ai"
    provider = str(provider).strip().lower().replace("-", "_")
    aliases = {
        "openai": "open_ai",
        "chatgpt": "open_ai",
        "open_webui": "open_web_ui",
        "openwebui": "open_web_ui",
    }
    return aliases.get(provider, provider)

def _position_click(kwargs, default):
    action = _get_action(kwargs)
    position = action.get("position_click", "")
    if isinstance(position, (list, tuple)) and len(position) >= 2:
        return list(position[:2])
    if isinstance(position, str) and position.strip():
        cleaned = position.replace("[", "").replace("]", "").replace("(", "").replace(")", "")
        parts = [part.strip() for part in cleaned.split(",")]
        if len(parts) >= 2:
            try:
                return [int(float(parts[0])), int(float(parts[1]))]
            except Exception:
                pass
    return default

def _extract_between_tags(text, tag_open, tag_close):
    if not tag_open or not tag_close:
        return None
    if tag_open == tag_close:
        parts = text.split(tag_open)
        if len(parts) >= 3:
            return parts[-2]
        return None
    search_end = len(text)
    while True:
        start = text.rfind(tag_open, 0, search_end)
        if start == -1:
            return None
        content_start = start + len(tag_open)
        end = text.find(tag_close, content_start)
        if end != -1:
            return text[content_start:end]
        search_end = start

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
    return _strip_emoji(text).strip()

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

def new(**kwargs):
    provider = _get_base_ai_provider(kwargs)
    if provider == "open_ai":
        return action_open_ai(**kwargs)
    if provider == "claude":
        return action_claude(**kwargs)
    if provider == "gemini":
        return action_gemini(**kwargs)
    if provider == "open_web_ui":
        return action_open_web_ui(**kwargs)
    print(f"save_text -- unknown base_ai_provider '{provider}', defaulting to open_ai")
    return action_open_ai(**kwargs)

def old(**kwargs):
    return action_open_ai(**kwargs)

def _save_text_impl(kwargs, focus_position=None):
    action = _get_action(kwargs)
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

    click_pos = _position_click(kwargs, focus_position or [300, 300])
    robo_roboclick.robo_mouse_click(position=click_pos, delay=2, button="left")
    text = robo_roboclick.robo_keyboard_copy(delay=2)

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
            clipping = _extract_text(text, action, clip)
            clipping = _apply_sanitizers(clipping, sanitize_text, sanitize_double_linebreaks)
            f.write(clipping)
            print(f"Clip text saved to {file_name_clip_full}")

def action_open_ai(**kwargs):
    """Save text content from OpenAI chat session."""
    print("save_text -- saving text from open_ai")
    return _save_text_impl(kwargs, focus_position=[300, 300])

def action_claude(**kwargs):
    """Save text content from Claude chat session."""
    print("save_text -- saving text from claude")
    return _save_text_impl(kwargs, focus_position=[650, 400])

def action_gemini(**kwargs):
    """Save text content from Google Gemini chat session."""
    print("save_text -- saving text from gemini")
    return _save_text_impl(kwargs, focus_position=[650, 400])

def action_open_web_ui(**kwargs):
    """Save text content from Open WebUI chat session."""
    print("save_text -- saving text from open_web_ui")
    return _save_text_impl(kwargs, focus_position=[650, 400])

def test(**kwargs):
    test_file = os.path.join(os.path.dirname(__file__), "oomlout_test.py")
    if os.path.exists(test_file):
        import importlib.util
        import sys
        dir_path = os.path.dirname(__file__)
        added_to_path = False
        if dir_path not in sys.path:
            sys.path.insert(0, dir_path)
            added_to_path = True
        try:
            spec = importlib.util.spec_from_file_location(f"test_module_{abs(hash(test_file))}", test_file)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                test_fn = getattr(mod, "test", None)
                if callable(test_fn):
                    return test_fn(**kwargs)
        finally:
            if added_to_path and dir_path in sys.path:
                sys.path.remove(dir_path)
    return callable(old) and callable(new)
