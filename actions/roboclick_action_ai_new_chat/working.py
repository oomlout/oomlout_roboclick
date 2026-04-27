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
    d["name_short"] = ['new_chat', 'chat', 'ai_new_chat']
    d["name_short_options"] = ['new_chat', 'chat', 'ai_new_chat']
    d["description"] = 'New chat.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
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
    return old(**kwargs)

def old(**kwargs):
    """Open new chat session"""
    action = kwargs.get("action", {})
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
        robo_roboclick.ai_check_for_too_many_requests()
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
    robo_roboclick.ai_check_for_too_many_requests()
    #if log_url is True:
    if log_url:
        #press ctrl l
        robo_roboclick.robo_keyboard_press_ctrl_generic(string="l", delay=2)
        #copy the url
        url = robo_roboclick.robo_keyboard_copy(delay=2)
        #print the url
        print(f".:current chat url is {url[:60]}:.")
        #press esc
        robo_roboclick.robo_keyboard_press_escape(delay=2, repeat=5)
        #save to url.yaml
        if True:            
            url_file = os.path.join(kwargs.get("directory_absolute", ""), "url.yaml")
            #if url exists load it to add to the list
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
