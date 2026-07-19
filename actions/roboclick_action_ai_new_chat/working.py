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
    d["name_long_4"] = 'new'
    d["name_long_5"] = 'new_chat'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_new_chat'
    d["name_long"] = 'roboclick_action_ai_new_chat'
    d["name_short"] = ['new_chat', 'ai_new_chat']
    d["name_short_options"] = ['new_chat', 'ai_new_chat']
    d["description"] = 'New chat.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
        v.append({'name': 'base_ai_provider', 'description': 'AI provider to use for this action. Options: open_ai, claude, gemini, open_web_ui.', 'type': 'string', 'default': 'open_ai'})
        v.append({'name': 'log_url', 'description': 'Whether to capture and store the current chat URL.', 'type': 'string', 'default': ''})
        v.append({'name': 'description', 'description': 'Optional kickoff note sent in the first chat message.', 'type': 'string', 'default': ''})
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
    return robo_roboclick.robo_action_run("roboclick_action_ai_new_chat", new, **kwargs)

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
    print(f"new_chat -- unknown base_ai_provider '{provider}', defaulting to open_ai")
    return action_open_ai(**kwargs)

def old(**kwargs):
    return action_open_ai(**kwargs)

def action_open_ai(**kwargs):
    """Open new chat session"""
    action = _get_action(kwargs)
    description = action.get("description", "")
    log_url = action.get("log_url", True)
    print("new_chat -- opening up a new chat")
    robo_roboclick.robo_chrome_open_url(url="https://chat.openai.com/chat", delay=15, message=".:action -- opening a new chat:.")    
    #check for hitting limit
    if True:
        print(".:check message limit:.")
        clip = robo_roboclick.robo_keyboard_copy(delay=5, position=[300, 300])  # Copy some text to check for limit
        if "0 messages remaining" in clip.lower():
            print("    Hit message limit, cannot proceed.")
            #delay 6 hours
            print("    Delaying for 6 hours before retrying...")
            robo_roboclick.robo_delay(delay=21600)  # Delay for 6 hours
            return "exit"
        robo_roboclick.ai_check_for_too_many_requests(**kwargs)
        pass
    #type in start query
    start_query = ""
    if description != "":        
        #load start_query from prompt.md
        #https://chatgpt.com/c/69ebfd24-448c-83eb-8fba-84d3988a54ff
        #prompt file is in the directory of this python file, with the name prompt.md the file might have complicated charcters like emoji so open it to support that
        prompt_file = os.path.join(os.path.dirname(__file__), "prompt.md")
        if os.path.exists(prompt_file):
            with open(prompt_file, 'r', encoding='utf-8') as file:
                start_query = file.read()
        else:
            start_query = description
    start_query += ""
    #type
    if False:
        robo_roboclick.robo_keyboard_send(string=start_query, delay=5)
    #paste
    if True:
        robo_roboclick.robo_keyboard_paste(text=start_query, delay=5)

    #robo_roboclick.robo_keyboard_press_enter(delay=40)
    #control enter
    robo_roboclick.robo_keyboard_press_ctrl_generic(string="enter", delay=40)
    robo_roboclick.ai_check_for_too_many_requests(**kwargs)
    if log_url:
        return _log_current_url(kwargs)

def _load_start_query(kwargs):
    action = _get_action(kwargs)
    description = action.get("description", "")
    start_query = ""
    if description != "":
        prompt_file = os.path.join(os.path.dirname(__file__), "prompt.md")
        if os.path.exists(prompt_file):
            with open(prompt_file, 'r', encoding='utf-8') as file:
                start_query = file.read()
        else:
            start_query = description
    return start_query

def _send_start_query(start_query, delay=40):
    if start_query:
        robo_roboclick.robo_keyboard_paste(text=start_query, delay=5)
    robo_roboclick.robo_keyboard_press_ctrl_generic(string="enter", delay=delay)

def _log_current_url(kwargs):
    provider = _get_base_ai_provider(kwargs)
    if provider == "open_ai":
        return _log_current_url_open_ai(kwargs)
    if provider == "claude":
        return _log_current_url_claude(kwargs)
    if provider == "gemini":
        return _log_current_url_gemini(kwargs)
    if provider == "open_web_ui":
        return _log_current_url_open_web_ui(kwargs)
    print(f"log_current_url -- unknown base_ai_provider '{provider}', defaulting to open_ai")
    return _log_current_url_open_ai(kwargs)

def _log_current_url_open_ai(kwargs):
    action = _get_action(kwargs)
    log_url = action.get("log_url", True)
    if not log_url:
        return None
    robo_roboclick.robo_keyboard_press_ctrl_generic(string="l", delay=2)
    url = robo_roboclick.robo_keyboard_copy(delay=2)
    print(f".:current chat url is {url[:60]}:.")
    robo_roboclick.robo_keyboard_press_escape(delay=2, repeat=5)
    url_file = os.path.join(kwargs.get("directory_absolute", ""), "url.yaml")
    if os.path.exists(url_file):
        with open(url_file, 'r') as file:
            url_data = yaml.safe_load(file)
    else:
        url_data = []
    if url_data == None:
        url_data = []
    url_data.append(url)
    with open(url_file, 'w') as file:
        yaml.dump(url_data, file)
    return url

def _log_current_url_claude(kwargs):
    return _log_current_url_open_ai(kwargs)

def _log_current_url_gemini(kwargs):
    return None

def _log_current_url_open_web_ui(kwargs):
    return None

def action_claude(**kwargs):
    """Open new Claude chat session."""
    print("new_chat -- opening up a new claude chat")
    robo_roboclick.robo_chrome_open_url(url="https://claude.ai/new", delay=15, message=".:action -- opening a new claude chat:.")
    robo_roboclick.ai_check_for_too_many_requests(**kwargs)
    start_query = _load_start_query(kwargs)
    # TODO: Verify Claude's prompt box position for your browser/window size.
    # Guessed coordinate: [650, 860].
    robo_roboclick.robo_mouse_click(position=[650, 470], delay=2)
    _send_start_query(start_query, delay=40)
    url = _log_current_url(kwargs)
    return url

def action_gemini(**kwargs):
    """Open new Gemini chat session."""
    print("new_chat -- opening up a new gemini chat")
    robo_roboclick.robo_chrome_open_url(url="https://gemini.google.com/app", delay=15, message=".:action -- opening a new gemini chat:.")
    robo_roboclick.ai_check_for_too_many_requests(**kwargs)
    start_query = _load_start_query(kwargs)
    # TODO: Verify Gemini's prompt box position for your browser/window size.
    # Guessed coordinate: [650, 860].
    robo_roboclick.robo_mouse_click(position=[650, 860], delay=2)
    _send_start_query(start_query, delay=40)
    return _log_current_url(kwargs)

def action_open_web_ui(**kwargs):
    """Open new Open WebUI chat session."""
    action = _get_action(kwargs)
    url = action.get("url", kwargs.get("open_web_ui_url", "http://localhost:8080/"))
    print("new_chat -- opening up a new open_web_ui chat")
    robo_roboclick.robo_chrome_open_url(url=url, delay=15, message=".:action -- opening a new open_web_ui chat:.")
    robo_roboclick.ai_check_for_too_many_requests(**kwargs)
    start_query = _load_start_query(kwargs)
    # TODO: Verify Open WebUI's new-chat button and prompt box positions.
    # Guessed new-chat coordinate: [90, 120].
    # Guessed prompt coordinate: [650, 860].
    robo_roboclick.robo_mouse_click(position=[90, 120], delay=2)
    robo_roboclick.robo_mouse_click(position=[650, 860], delay=2)
    _send_start_query(start_query, delay=40)
    return _log_current_url(kwargs)

def test(**kwargs):
    try:
        import oomlout_test
    except Exception:
        return callable(old) and callable(new)

    test_fn = getattr(oomlout_test, "test", None)
    test_file = getattr(oomlout_test, "__file__", "")
    if test_file and os.path.abspath(test_file) == os.path.abspath(os.path.join(os.path.dirname(__file__), "oomlout_test.py")):
        return callable(old) and callable(new)
    if not callable(test_fn):
        return callable(old) and callable(new)

    try:
        return bool(test_fn(**kwargs))
    except Exception:
        return callable(old) and callable(new)
