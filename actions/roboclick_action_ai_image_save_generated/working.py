import os
import random
from pathlib import Path
import shutil

import robo_roboclick

try:
    from PIL import Image
except Exception:
    Image = None

try:
    import pyautogui  # type: ignore
except Exception:
    pyautogui = None  # type: ignore

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'save'
    d["name_long_4"] = 'image'
    d["name_long_5"] = 'save_image_generated'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_image_save_generated'
    d["name_long"] = 'roboclick_action_ai_image_save_generated'
    d["name_short"] = ['save_image_generated', 'generated']
    d["name_short_options"] = ['save_image_generated', 'generated']
    d["description"] = 'Save image generated.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI Image'
    v = []
    if True:
        v.append({'name': 'base_ai_provider', 'description': 'AI provider to use for this action. Options: open_ai, claude, gemini, open_web_ui.', 'type': 'string', 'default': 'open_ai'})
        v.append({'name': 'file_name', 'description': 'File name to read or write for this action.', 'type': 'string', 'default': ''})
        v.append({'name': 'position_click', 'description': 'Screen position used to open the generated image context menu.', 'type': 'string', 'default': ''})
        v.append({'name': 'mode_ai_wait', 'description': 'AI wait strategy (slow, fast_button_state, or fast_clipboard_state).', 'type': 'string', 'default': ''})
        v.append({'name': 'retry_if_failed', 'description': 'Number of times to ask the AI to retry and save again if the expected image file is missing. Use false or 0 to disable.', 'type': 'number', 'default': 1})
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
    return robo_roboclick.robo_action_run("roboclick_action_ai_image_save_generated", new, **kwargs)

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

def _retry_count(value, default=1):
    if value in (None, ""):
        return default
    if isinstance(value, bool):
        return 1 if value else 0
    if isinstance(value, (int, float)):
        return max(0, int(value))
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("false", "no", "n", "off"):
            return 0
        if normalized in ("true", "yes", "y", "on"):
            return 1
        try:
            return max(0, int(float(normalized)))
        except Exception:
            return default
    return default

def _wait_for_image(mode_ai_wait, kwargs=None):
    kwargs = kwargs or {}
    if mode_ai_wait is None:
        mode_ai_wait = "slow"
    if mode_ai_wait == "slow":
        delay = random.randint(110, 140)
        robo_roboclick.robo_delay(delay=delay)
    elif "fast" in mode_ai_wait:
        robo_roboclick.ai_wait_mode_fast_check(mode_ai_wait="fast_clipboard_state", **kwargs)

def _prepare_to_save_image(kwargs=None):
    kwargs = kwargs or {}
    robo_roboclick.robo_keyboard_press_ctrl_generic(string="r", delay=20)
    robo_roboclick.ai_check_for_too_many_requests(**kwargs)
    robo_roboclick.robo_mouse_click(position=[330,360], delay=2)
    robo_roboclick.robo_keyboard_press_end(delay=1)
    robo_roboclick.robo_keyboard_press_down(delay=1, repeat=40)
    robo_roboclick.ai_check_for_too_many_requests(**kwargs)

def _send_retry_prompt(kwargs=None):
    kwargs = kwargs or {}
    retry_prompt = "oops the image seems to have not generated please try again"
    robo_roboclick.ai_check_for_too_many_requests(**kwargs)
    robo_roboclick.robo_keyboard_press_ctrl_generic(string="a", delay=2)
    robo_roboclick.robo_keyboard_press_backspace(delay=2, repeat=1)
    robo_roboclick.robo_keyboard_paste(text=retry_prompt, delay=2)
    robo_roboclick.robo_keyboard_press_ctrl_generic(string="enter", delay=1)
    print(f".:retrying image generation:. {retry_prompt}")

def _delete_bad_image(file_name_absolute):
    try:
        os.remove(file_name_absolute)
        print(f".:deleted invalid image file {file_name_absolute[:60]}:.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f".:failed to delete invalid image file {file_name_absolute[:60]}:. {e}")

def _is_valid_png(file_name_absolute):
    if not os.path.exists(file_name_absolute):
        return False
    if Image is None:
        return os.path.getsize(file_name_absolute) > 0
    try:
        with Image.open(file_name_absolute) as img:
            if img.format != "PNG":
                return False
            img.verify()
        return True
    except Exception:
        return False

def clean_png(file_name):
    if Image is None:
        return
    path = Path(file_name)
    try:
        with Image.open(path) as img:
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            temp_path = path.with_suffix(".tmp.png")
            img.save(temp_path, format="PNG", optimize=False, compress_level=6)
            temp_path.replace(path)
            print(f"[OK] {path}")
    except Exception as e:
        print(f"[FAIL] {path} -> {e}")

def _save_image_once(kwargs, file_name_absolute):
    robo_roboclick.ai_check_for_too_many_requests(**kwargs)
    robo_roboclick.ai_save_image(**kwargs)
    if os.path.exists(file_name_absolute):
        if not _is_valid_png(file_name_absolute):
            print(f".:image file is not a valid png:.")
            _delete_bad_image(file_name_absolute)
            return False
        print("")
        print(f".:image saved to {file_name_absolute[:60]}:.")
        clean_png(file_name_absolute)
        return True
    print(f".:image not saved:.")
    return False

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
    print(f"save_image_generated -- unknown base_ai_provider '{provider}', defaulting to open_ai")
    return action_open_ai(**kwargs)

def old(**kwargs):
    return action_open_ai(**kwargs)

def _save_generated_loop(kwargs):
    action = _get_action(kwargs)
    mode_ai_wait = action.get("mode_ai_wait", "slow")
    retry_value = kwargs.get("retry_if_failed", action.get("retry_if_failed", 1))
    retry_if_failed = _retry_count(retry_value, 1)
    file_name = action.get("file_name", "working.png")
    file_name_absolute = os.path.abspath(os.path.join(kwargs.get("directory_absolute", ""), file_name))
    
    for attempt in range(retry_if_failed + 1):
        if attempt > 0:
            _send_retry_prompt(kwargs)
        _wait_for_image(mode_ai_wait, kwargs)
        _prepare_to_save_image(kwargs)
        if _save_image_once(kwargs, file_name_absolute):
            return ""
        if attempt < retry_if_failed:
            print(f".:image save retry {attempt + 1} of {retry_if_failed}:.")

    print(
        f"Image save failed after {retry_if_failed + 1} attempt(s): "
        f"{file_name_absolute}. Stopping this action sequence; "
        "no valid image was saved."
    )
    return "exit_no_tab"

def action_open_ai(**kwargs):
    """Save generated image from OpenAI"""
    print("save_image_generated -- saving generated image from open_ai")
    return _save_generated_loop(kwargs)

def action_claude(**kwargs):
    """Save generated image from Claude"""
    print("save_image_generated -- saving generated image from claude")
    return _save_generated_loop(kwargs)

def action_gemini(**kwargs):
    """Save generated image from Google Gemini"""
    print("save_image_generated -- saving generated image from gemini")
    return _save_generated_loop(kwargs)

def action_open_web_ui(**kwargs):
    """Save generated image from Open WebUI"""
    print("save_image_generated -- saving generated image from open_web_ui")
    return _save_generated_loop(kwargs)

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
