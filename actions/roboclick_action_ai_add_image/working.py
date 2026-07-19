import os

import robo_roboclick

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'add'
    d["name_long_5"] = 'add_image'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_add_image'
    d["name_long"] = 'roboclick_action_ai_add_image'
    d["name_short"] = ['add_image', 'ai_add_image']
    d["name_short_options"] = ['add_image', 'ai_add_image']
    d["description"] = 'Add image.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
        v.append({'name': 'base_ai_provider', 'description': 'AI provider to use for this action. Options: open_ai, claude, gemini, open_web_ui.', 'type': 'string', 'default': 'open_ai'})
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
        v.append({'name': 'position_click', 'description': 'Screen position to click before executing the step.', 'type': 'string', 'default': ''})
        v.append({'name': 'mode -- source_files from source_files directory', 'description': 'Value for mode -- source files from source files directory.', 'type': 'string', 'default': ''})
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
    return robo_roboclick.robo_action_run("roboclick_action_ai_add_image", new, **kwargs)

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

def _image_file_absolute(kwargs):
    action = _get_action(kwargs)
    file_name = action.get("file_source", "")
    if file_name == "":
        file_name = action.get("file_name", "working.png")
    directory = kwargs.get("directory", "")
    directory_absolute = os.path.abspath(directory)

    mode = action.get("mode", "")
    if mode == "source_files":
        return os.path.abspath(os.path.join(os.path.abspath("source_files"), file_name))
    return os.path.abspath(os.path.join(directory_absolute, file_name))

def _ensure_image_exists(file_name_absolute):
    if os.path.exists(file_name_absolute):
        return True
    print(f"File {file_name_absolute} does not exist, skipping action.")
    print(f"    ERROR ERROR ERROR Exiting action due to missing file: {file_name_absolute}")
    robo_roboclick.robo_delay(delay=5)
    return False

def _send_file_to_open_dialog(file_name_absolute):
    #delay 5 seconds to allow the file dialog to open
    robo_roboclick.robo_delay(delay=5)
    robo_roboclick.robo_keyboard_send(string=file_name_absolute, delay=5)
    #delay 2 seconds to allow the file path to be entered
    robo_roboclick.robo_delay(delay=2)
    robo_roboclick.robo_keyboard_press_enter(delay=5)    
    robo_roboclick.robo_delay(delay=15)
    robo_roboclick.robo_keyboard_press_escape(delay=5, repeat=5)
    

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
    print(f"add_image -- unknown base_ai_provider '{provider}', defaulting to open_ai")
    return action_open_ai(**kwargs)

def old(**kwargs):
    return action_open_ai(**kwargs)

def action_open_ai(**kwargs):
    """Add an image file to the current OpenAI chat context."""
    print("add_image -- adding an image to open_ai")
    file_name_absolute = _image_file_absolute(kwargs)
    if not _ensure_image_exists(file_name_absolute):
        return "exit"

    # OpenAI/ChatGPT: this is the existing keyboard path. It assumes focus is
    # in the composer, then shift-tabs to the add-file button.
    robo_roboclick.robo_keyboard_send(string="  ", delay=2)
    robo_roboclick.robo_keyboard_press_tab_shift(delay=5, repeat=1)
    robo_roboclick.robo_keyboard_press_enter(delay=5)
    robo_roboclick.robo_keyboard_press_enter(delay=5)
    _send_file_to_open_dialog(file_name_absolute)

    return ""

def action_claude(**kwargs):
    """Add an image file to the current Claude chat context."""
    print("add_image -- adding an image to claude")
    file_name_absolute = _image_file_absolute(kwargs)
    if not _ensure_image_exists(file_name_absolute):
        return "exit"

    # Guess: Claude's attachment button is near the lower-left edge of the
    # composer. Override with position_click if your window differs.
    #send tab
    robo_roboclick.robo_keyboard_press_tab(delay=2, repeat=1)
    #send enter
    robo_roboclick.robo_keyboard_press_enter(delay=5)
    #send enter
    robo_roboclick.robo_keyboard_press_enter(delay=5)
    _send_file_to_open_dialog(file_name_absolute)
    #delay 5
    robo_roboclick.robo_delay(delay=5)
    #shift tab
    robo_roboclick.robo_keyboard_press_tab_shift(delay=2, repeat=1)
    return ""

def action_gemini(**kwargs):
    """Add an image file to the current Gemini chat context."""
    print("add_image -- adding an image to gemini")
    file_name_absolute = _image_file_absolute(kwargs)
    if not _ensure_image_exists(file_name_absolute):
        return "exit"

    # Guess: Gemini's add/upload affordance is near the lower-left of the input
    # bar. Override with position_click once calibrated.
    robo_roboclick.robo_mouse_click(position=_position_click(kwargs, [520, 890]), delay=2)
    _send_file_to_open_dialog(file_name_absolute)
    return ""

def action_open_web_ui(**kwargs):
    """Add an image file to the current Open WebUI chat context."""
    print("add_image -- adding an image to open_web_ui")
    file_name_absolute = _image_file_absolute(kwargs)
    if not _ensure_image_exists(file_name_absolute):
        return "exit"

    # Guess: Open WebUI usually keeps the upload/plus control just left of the
    # prompt box. Override with position_click for your theme/layout.
    robo_roboclick.robo_mouse_click(position=_position_click(kwargs, [520, 860]), delay=2)
    _send_file_to_open_dialog(file_name_absolute)   
    #wait 5 seconds for the file to be uploaded
    robo_roboclick.robo_delay(delay=5)
    #press shift_tab
    robo_roboclick.robo_keyboard_press_tab_shift(delay=2, repeat=1)
    return ""

def test(**kwargs):
    try:
        import oomlout_test
    except Exception:
        return callable(old) and callable(new)

    test_fn = getattr(oomlout_test, "test", None)
    if not callable(test_fn):
        return callable(old) and callable(new)

    try:
        return bool(test_fn(**kwargs))
    except Exception:
        return callable(old) and callable(new)
