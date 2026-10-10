import os
import robo_roboclick

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'set'
    d["name_long_5"] = 'set_mode'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_set_mode'
    d["name_long"] = 'roboclick_action_ai_set_mode'
    d["name_short"] = ['set_mode', 'mode', 'ai_set_mode']
    d["name_short_options"] = ['set_mode', 'mode', 'ai_set_mode']
    d["description"] = 'Set mode.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
        v.append({'name': 'base_ai_provider', 'description': 'AI provider to use for this action. Options: open_ai, claude, gemini, open_web_ui.', 'type': 'string', 'default': 'open_ai'})
        v.append({'name': 'mode', 'description': 'Mode selector controlling action behavior.', 'type': 'string', 'default': ''})
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
    return robo_roboclick.robo_action_run("roboclick_action_ai_set_mode", new, **kwargs)

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
    print(f"set_mode -- unknown base_ai_provider '{provider}', defaulting to open_ai")
    return action_open_ai(**kwargs)

def old(**kwargs):
    return action_open_ai(**kwargs)

def action_open_ai(**kwargs):
    """Set OpenAI mode (e.g., deep_research)"""
    action = _get_action(kwargs)
    print("ai_set_mode -- setting OpenAI mode")
    mode = action.get("mode", "")
    if mode in ("deep_research", "deep_research_off"):
        robo_roboclick.robo_keyboard_press_tab(delay=2, repeat=1)
        robo_roboclick.robo_keyboard_press_enter(delay=2)
        robo_roboclick.robo_keyboard_press_down(delay=2, repeat=1)
        robo_roboclick.robo_keyboard_press_enter(delay=2)
        print("     OpenAI mode updated")

def action_claude(**kwargs):
    """Set Claude mode"""
    action = _get_action(kwargs)
    print("ai_set_mode -- setting Claude mode")
    mode = action.get("mode", "")
    print(f"     Claude mode requested: {mode}")

def action_gemini(**kwargs):
    """Set Gemini mode (e.g., thinking, deep_research)"""
    action = _get_action(kwargs)
    print("ai_set_mode -- setting Gemini mode")
    mode = action.get("mode", "")
    if mode in ("deep_research", "thinking", "gemini_pro"):
        robo_roboclick.robo_mouse_click(position=[200, 150], delay=2)
        robo_roboclick.robo_keyboard_press_down(delay=2, repeat=1)
        robo_roboclick.robo_keyboard_press_enter(delay=2)
        print(f"     Gemini mode updated to {mode}")

def action_open_web_ui(**kwargs):
    """Set Open WebUI mode"""
    action = _get_action(kwargs)
    print("ai_set_mode -- setting Open WebUI mode")
    mode = action.get("mode", "")
    print(f"     Open WebUI mode requested: {mode}")

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

