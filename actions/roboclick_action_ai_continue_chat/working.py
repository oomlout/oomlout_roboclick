import os

import yaml

import robo_roboclick

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'continue'
    d["name_long_5"] = 'continue_chat'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_continue_chat'
    d["name_long"] = 'roboclick_action_ai_continue_chat'
    d["name_short"] = ['continue_chat', 'ai_continue_chat']
    d["name_short_options"] = ['continue_chat', 'ai_continue_chat']
    d["description"] = 'Continue chat.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
        v.append({'name': 'base_ai_provider', 'description': 'AI provider to use for this action. Options: open_ai, claude, gemini, open_web_ui.', 'type': 'string', 'default': 'open_ai'})
        v.append({'name': 'url_chat', 'description': 'Chat URL to continue an existing conversation.', 'type': 'string', 'default': ''})
        v.append({'name': 'log_url', 'description': 'Whether to capture and store the current chat URL.', 'type': 'string', 'default': ''})
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
    return robo_roboclick.robo_action_run("roboclick_action_ai_continue_chat", new, **kwargs)

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
    print(f"continue_chat -- unknown base_ai_provider '{provider}', defaulting to open_ai")
    return action_open_ai(**kwargs)

def old(**kwargs):
    return action_open_ai(**kwargs)

def _resolve_url_chat(kwargs):
    action = _get_action(kwargs)
    url_chat = action.get("url_chat", kwargs.get("url_chat", ""))
    if not url_chat:
        url_file = os.path.join(kwargs.get("directory_absolute", ""), "url.yaml")
        if os.path.exists(url_file):
            with open(url_file, 'r') as file:
                url_data = yaml.safe_load(file)
            if isinstance(url_data, list) and url_data:
                url_chat = url_data[-1]
            elif isinstance(url_data, str):
                url_chat = url_data
    return url_chat

def _log_current_url_if_requested(kwargs):
    action = _get_action(kwargs)
    log_url = action.get("log_url", kwargs.get("log_url", False))
    if not log_url:
        return None
    robo_roboclick.robo_keyboard_press_ctrl_generic(string="l", delay=2)
    url = robo_roboclick.robo_keyboard_copy(delay=2)
    print(f".:current chat url is {url[:60]}:.")
    robo_roboclick.robo_keyboard_press_escape(delay=2, repeat=5)
    url_file = os.path.join(kwargs.get("directory_absolute", ""), "url.yaml")
    url_data = []
    if os.path.exists(url_file):
        with open(url_file, 'r') as file:
            url_data = yaml.safe_load(file)
    if url_data is None:
        url_data = []
    url_data.append(url)
    with open(url_file, 'w') as file:
        yaml.dump(url_data, file)
    return url

def action_open_ai(**kwargs):
    """Continue existing OpenAI chat session"""
    url_chat = _resolve_url_chat(kwargs)
    if not url_chat:
        print("continue_chat -- no url_chat provided and url.yaml has no saved chat URL")
        return "exit_no_tab"
    print("continue_chat -- continuing an existing open_ai chat")
    robo_roboclick.robo_chrome_open_url(url=url_chat, delay=30, message="    opening existing open_ai chat")
    clip = robo_roboclick.robo_keyboard_copy(delay=5, position=[300, 300])
    if "0 messages remaining" in clip.lower():
        print("    Hit message limit, cannot proceed.")
        robo_roboclick.robo_delay(delay=21600)
        return "exit"
    return _log_current_url_if_requested(kwargs)

def action_claude(**kwargs):
    """Continue existing Claude chat session"""
    url_chat = _resolve_url_chat(kwargs)
    if not url_chat:
        url_chat = "https://claude.ai/chats"
    print("continue_chat -- continuing an existing claude chat")
    robo_roboclick.robo_chrome_open_url(url=url_chat, delay=30, message="    opening existing claude chat")
    robo_roboclick.ai_check_for_too_many_requests(**kwargs)
    return _log_current_url_if_requested(kwargs)

def action_gemini(**kwargs):
    """Continue existing Gemini chat session"""
    url_chat = _resolve_url_chat(kwargs)
    if not url_chat:
        url_chat = "https://gemini.google.com/app"
    print("continue_chat -- continuing an existing gemini chat")
    robo_roboclick.robo_chrome_open_url(url=url_chat, delay=30, message="    opening existing gemini chat")
    robo_roboclick.ai_check_for_too_many_requests(**kwargs)
    return _log_current_url_if_requested(kwargs)

def action_open_web_ui(**kwargs):
    """Continue existing Open WebUI chat session"""
    url_chat = _resolve_url_chat(kwargs)
    if not url_chat:
        url_chat = kwargs.get("open_web_ui_url", "http://localhost:8080/")
    print("continue_chat -- continuing an existing open_web_ui chat")
    robo_roboclick.robo_chrome_open_url(url=url_chat, delay=30, message="    opening existing open_web_ui chat")
    robo_roboclick.ai_check_for_too_many_requests(**kwargs)
    return _log_current_url_if_requested(kwargs)

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
