import os
import re
import pyautogui
import robo_roboclick

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'query'
    d["name_long_5"] = 'ai_query'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_query'
    d["name_long"] = 'roboclick_action_ai_query'
    d["name_short"] = ['ai_query', 'query']
    d["description"] = 'Ai query.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
        v.append({'name': 'base_ai_provider', 'description': 'AI provider to use for this action. Options: open_ai, claude, gemini, open_web_ui.', 'type': 'string', 'default': 'open_ai'})
        v.append({'name': 'text', 'description': 'Text content used by this action.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_name', 'description': 'File name to read or write for this action. if folder name starts with source_files it will pull from project source_files rather than folder', 'type': 'string', 'default': ''})
        v.append({'name': 'delay', 'description': 'Delay duration in seconds.', 'type': 'string', 'default': ''})
        v.append({'name': 'mode_ai_wait', 'description': 'AI wait strategy (slow, fast_button_state, or fast_clipboard_state).', 'type': 'string', 'default': ''})
        v.append({'name': 'method', 'description': 'Query input method (typing or paste).', 'type': 'string', 'default': ''})
        v.append({'name': 'position_click', 'description': 'Screen position to click before executing the step.', 'type': 'string', 'default': ''})
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
    return robo_roboclick.robo_action_run("roboclick_action_ai_query", new, **kwargs)

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
    print(f"ai_query -- unknown base_ai_provider '{provider}', defaulting to open_ai")
    return action_open_ai(**kwargs)

def old(**kwargs):
    return action_open_ai(**kwargs)

def _load_query_texts(kwargs):
    directory = kwargs.get("directory", "")
    action = _get_action(kwargs)
    query_text = action.get("text", "")
    file_name = action.get("file_name", "")
    folder_name = action.get("folder_name", "")
    f_string_replace = action.get("f_string_replace", True)
    
    query_texts = []
    if query_text != "":
        query_texts.append(query_text)
    else:
        if file_name != "" and query_text != "":
            print(f"     ERROR both query text and file are defined query text will be used")
            robo_roboclick.robo_delay(delay=10)
        
        file_names = file_name
        if not isinstance(file_names, list):
            file_names = [file_names]
        if folder_name != "":
            file_names = []
            for i in range(1, 50):
                file_name_check = f"{folder_name}\\working_{i}.md"
                file_names.append(file_name_check)
        for file_name_seed in file_names:
            file_name = file_name_seed
            if file_name.startswith("prompt\\") or file_name.startswith("prompt/") or file_name.startswith("roboclick\\") or file_name.startswith("roboclick/"):
                filename_absolute = os.path.abspath(file_name)
            else:
                file_name = f"{directory}\\{file_name}"
                filename_absolute = os.path.abspath(file_name)
            if filename_absolute != "":
                if os.path.exists(filename_absolute):
                    with open(filename_absolute, 'r', encoding='utf-8') as f:
                        query_text = f.read()
                        if f_string_replace:
                            workings = kwargs.get("workings", {})
                            query_text = re.sub(
                                r"\{([A-Za-z_][A-Za-z0-9_]*)\}",
                                lambda m: str(workings[m.group(1)]) if m.group(1) in workings else m.group(0),
                                query_text,
                            )
                    query_texts.append(query_text)
                    print(f"     Loaded query text from {filename_absolute}")
                else:
                    if folder_name == "":
                        print(f"     File Missing")
                        robo_roboclick.robo_delay(delay=10)
                    folder_name_check = os.path.dirname(filename_absolute)
                    if not os.path.exists(folder_name_check):
                        print(f"     Folder {folder_name_check} does not exist for file {filename_absolute}")
                        robo_roboclick.robo_delay(delay=10)
            else:
                print(f"     No valid file name provided for query text.")
                robo_roboclick.robo_delay(delay=10)
                query_text = ""
    return query_texts

def _send_query_texts_impl(query_texts, kwargs, default_focus_pos=None):
    action = _get_action(kwargs)
    delay = action.get("delay", 60)
    mode_ai = action.get("mode_ai_wait", "slow") or "slow"
    method = action.get("method", "typing")

    if default_focus_pos:
        pos = _position_click(kwargs, default_focus_pos)
        robo_roboclick.robo_mouse_click(position=pos, delay=2)

    for query_text in query_texts:
        robo_roboclick.ai_check_for_too_many_requests(**kwargs)
        print(".:clearing:.")
        robo_roboclick.robo_keyboard_press_ctrl_generic(string="a", delay=2)
        robo_roboclick.robo_keyboard_press_backspace(delay=2, repeat=1)

        if len(query_text) > 1000:
            method = "paste"
            print(".:paste_method:.")

        if method == "typing":
            query_text_clean = query_text.replace("\r\n", "\n").replace("\r", "\n")
            query_text_lines = query_text_clean.split("\n")
            for line in query_text_lines:
                robo_roboclick.robo_keyboard_send(string=line, delay=0.1)
                robo_roboclick.robo_keyboard_press_shift_enter(delay=0.1)
        elif method == "paste":
            robo_roboclick.robo_keyboard_send(string="  ")
            robo_roboclick.robo_keyboard_paste(text=query_text)
            robo_roboclick.robo_delay(delay=10)

        query_text_print = query_text.replace("\n", "\\n").replace("\t", "\\t")
        print(f"\n.: text: {query_text_print[:60]}:.")

        if mode_ai == "slow":
            robo_roboclick.robo_keyboard_press_ctrl_generic(string="enter", delay=delay)
            robo_roboclick.ai_check_for_too_many_requests(**kwargs)
        elif "fast" in mode_ai:
            robo_roboclick.robo_keyboard_press_ctrl_generic(string="enter", delay=1)
            robo_roboclick.ai_wait_mode_fast_check(mode_ai_wait=mode_ai, **kwargs)

def action_open_ai(**kwargs):
    """Send query to OpenAI"""
    print("\n.:action:. -- ai_query (open_ai) -- sending a query")
    query_texts = _load_query_texts(kwargs)
    _send_query_texts_impl(query_texts, kwargs)

def action_claude(**kwargs):
    """Send query to Claude"""
    print("\n.:action:. -- ai_query (claude) -- sending a query")
    query_texts = _load_query_texts(kwargs)
    _send_query_texts_impl(query_texts, kwargs, default_focus_pos=[650, 470])

def action_gemini(**kwargs):
    """Send query to Google Gemini"""
    print("\n.:action:. -- ai_query (gemini) -- sending a query")
    query_texts = _load_query_texts(kwargs)
    _send_query_texts_impl(query_texts, kwargs, default_focus_pos=[650, 860])

def action_open_web_ui(**kwargs):
    """Send query to Open WebUI"""
    print("\n.:action:. -- ai_query (open_web_ui) -- sending a query")
    query_texts = _load_query_texts(kwargs)
    _send_query_texts_impl(query_texts, kwargs, default_focus_pos=[650, 860])

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
