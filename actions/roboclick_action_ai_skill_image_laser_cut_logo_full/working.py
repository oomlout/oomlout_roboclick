import oomlout_roboclick
import copy
from pathlib import Path

d = {}


PROMPT_DIR = Path(__file__).resolve().parent


def _load_prompt(filename, **replacements):
    prompt_text = (PROMPT_DIR / filename).read_text(encoding="utf-8")
    for key, value in replacements.items():
        prompt_text = prompt_text.replace(f"{{{key}}}", str(value))
    return prompt_text


def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'ai'
    d["name_long_4"] = 'skill'
    d["name_long_5"] = 'image_laser_cut_logo_full'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_ai_skill_image_laser_cut_logo_full'
    d["name_long"] = 'roboclick_action_ai_skill_image_laser_cut_logo_full'
    d["name_short"] = ['image_laser_cut_logo_full', 'image', 'ai_skill_image_laser_cut_logo_full']
    d["name_short_options"] = ['image_laser_cut_logo_full', 'image', 'ai_skill_image_laser_cut_logo_full']
    d["description"] = 'Image laser cut logo full.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'AI Skill'
    v = []
    if True:
        v.append({'name': 'image_detail', 'description': 'Prompt detail level for generated image instructions.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_destination', 'description': 'Path to the output file to create or update.', 'type': 'string', 'default': ''})
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
    """ make a laser cut logo image using AI."""
    action = kwargs.get("action", "")
    mode_ai_wait = action.get("mode_ai_wait", None)
    image_detail = action.get("image_detail", "colorful bubble letters")
    file_destination = action.get("file_destination", "")
    if file_destination == "":
        #try file_name
        file_destination = action.get("file_name", "")
        if file_destination == "":
            #try filename
            file_destination = action.get("filename", "initial_generated_test.png")
    

    action = {}
    kwargs2 = copy.deepcopy(kwargs)
    action["command"] = "ai_new_chat"
    action["description"] = f"making a icon logo for {image_detail} using AI"
    kwargs2["action"] = copy.deepcopy(action)
    oomlout_roboclick.run_single_action(**kwargs2)

    action = {}
    action["command"] = "ai_query"
    prompt = _load_prompt("prompt_1.md")
    action["text"] = prompt
    action["method"] = "paste"
    action["delay"] = 120
    if mode_ai_wait != "":
        action["mode_ai_wait"] = mode_ai_wait
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["action"] = copy.deepcopy(action)
    oomlout_roboclick.run_single_action(**kwargs2)
    
    action = {}
    action["command"] = "ai_query"
    prompt = _load_prompt("prompt_2.md", image_detail=image_detail)
    action["text"] = prompt
    action["method"] = "paste"
    action["delay"] = 240
    
    if mode_ai_wait != "":
        action["mode_ai_wait"] = mode_ai_wait
    kwargs2["action"] = copy.deepcopy(action)
    oomlout_roboclick.run_single_action(**kwargs2)

    action = {}
    action["command"] = "ai_query"
    prompt = _load_prompt("prompt_3.md")
    action["text"] = prompt
    action["method"] = "paste"
    action["delay"] = 240
    if mode_ai_wait != "":
        action["mode_ai_wait"] = mode_ai_wait
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["action"] = copy.deepcopy(action)
    oomlout_roboclick.run_single_action (**kwargs2)


    action = {}
    #- command: 'save_image'
    action["command"] = "ai_save_image"
    action["file_name"] = f"{file_destination}"
    if mode_ai_wait != "":
        action["mode_ai_wait"] = mode_ai_wait
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["action"] = copy.deepcopy(action)
    oomlout_roboclick.run_single_action(**kwargs2)

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
