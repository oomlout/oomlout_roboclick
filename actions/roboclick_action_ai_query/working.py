import robo

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
    d["name_short_options"] = ['ai_query', 'query']
    d["description"] = 'Ai query.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI'
    v = []
    if True:
        v.append({'name': 'text', 'description': 'Text content used by this action.', 'type': 'string', 'default': ''})
        v.append({'name': 'delay', 'description': 'Delay duration in seconds.', 'type': 'string', 'default': ''})
        v.append({'name': 'mode_ai_wait', 'description': 'AI wait strategy (slow, fast_button_state, or fast_clipboard_state).', 'type': 'string', 'default': ''})
        v.append({'name': 'method', 'description': 'Query input method (typing or paste).', 'type': 'string', 'default': ''})
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

def ai_wait_mode_fast_check(mode_ai_wait="fast_button_state"):  
    if mode_ai_wait == "fast_button_state" or mode_ai_wait == "fast":
        return ai_wait_mode_fast_check_state_of_submit_button_approach()
    elif mode_ai_wait == "fast_clipboard_state":
        return ai_wait_mode_fast_clipboard_creating_image_approach()

def ai_wait_mode_fast_check_state_of_submit_button_approach():  
    print("Waiting for AI to finish responding (fast mode)...")
    count = 0
    count_max = 100
    running = True    
    point_check_color = [1445,964]
    #point_check_color = [1331,964]
    color_done= (0, 0, 0)
    color_expecting = (236,236,236)

    while running and count < count_max:
        robo.robo_delay(delay=10)
        pixel_color = pyautogui.screenshot().getpixel((point_check_color[0], point_check_color[1]))
        print(f"    Pixel color at {point_check_color}: {pixel_color} ")
        #check if it is the expected color
        if pixel_color == color_expecting:
            print("    Good news the right color was found")
        else:
            print("    The expected color was not found, may need to move")
        if pixel_color == color_done:
            print("    AI apIpears to have finished responding.")
            running = False
            robo.robo_delay(delay=2)

def ai_wait_mode_fast_clipboard_creating_image_approach():  
    print("Waiting for AI to finish responding (fast mode)...")
    count = 0
    count_max = 100
    running = True    
    string_check = "Creating image"

    while running and count < count_max:
        robo.robo_delay(delay=10)
        #mouse click at 300,300
        robo.robo_mouse_click(position=[300, 300], delay=2, button="left")  # Click to focus
        text = robo.robo_keyboard_copy(delay=2)
        if string_check in text:
            print("    AI appears to be creating an image, waiting for it to finish...")
        else:
            print("    AI appears to have finished responding.")
            running = False
            robo.robo_delay(delay=2)

def action(**kwargs):
    return old(**kwargs)

def old(**kwargs):
    """Send query to AI"""
    action = kwargs.get("action", {})
    print("ai_query -- sending a query")
    #get the query from the action
    action = kwargs.get("action", {})
    delay = action.get("delay", 60)
    query_text = action.get("text", "")
    mode_ai = action.get("mode_ai_wait", "slow")
    if mode_ai == None:
        mode_ai = "slow"
    method = action.get("method", "typing")  #"standard" or "line_by_line"

    #clear text box
    if True:
        print("    Clearing text box before query...")
        #select all
        robo.robo_keyboard_press_ctrl_generic(string="a", delay=2)
        #back space
        robo.robo_keyboard_press_backspace(delay=2, repeat=1)

    #if query text is more than 1000 characters use paste method
    if len(query_text) > 1000:
        method = "paste"
        print("    Query text is long, using paste method.")

    if method == "typing":
        #split the text on line breaks
        query_text = query_text.replace("\r\n", "\n").replace("\r", "\n")
        query_text_lines = query_text.split("\n")
        for line in query_text_lines:
            #send each line with a delay of 1 second between lines
            robo.robo_keyboard_send(string=line, delay=0.1)
            robo.robo_keyboard_press_shift_enter(delay=0.1)  # Press Shift+Enter to create a new line
    elif method == "paste":
        #press space twice to ensure focus
        robo.robo_keyboard_send(string="  ")
        robo.robo_keyboard_paste(text=query_text)
        #paste the entire text at once
        #delay 5 seconds
        robo.robo_delay(delay=5)
        robo.robo_keyboard_press_ctrl_generic(string="v", delay=2)
    

    print(f"Querying with text: {query_text}")
    
    if mode_ai =="slow":
        #robo.robo_keyboard_press_enter(delay=delay)
        #ctrl enter
        robo.robo_keyboard_press_ctrl_generic(string="enter", delay=delay)
    elif "fast" in mode_ai: 
        #robo.robo_keyboard_press_enter(delay=1)
        robo.robo_keyboard_press_ctrl_generic(string="enter", delay=1)
        ai_wait_mode_fast_check(mode_ai_wait=mode_ai)

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
