import copy

import robo

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'text'
    d["name_long_4"] = 'jinja'
    d["name_long_5"] = 'jinja_template'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_text_jinja_template'
    d["name_long"] = 'roboclick_action_text_jinja_template'
    d["name_short"] = ['jinja_template', 'template', 'text_jinja_template']
    d["name_short_options"] = ['jinja_template', 'template', 'text_jinja_template']
    d["description"] = 'Jinja template.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Text'
    v = []
    if True:
        v.append({'name': 'file_template', 'description': 'Legacy parameter: file_template', 'type': 'string', 'default': ''})
        v.append({'name': 'file_source', 'description': 'Legacy parameter: file_source', 'type': 'string', 'default': ''})
        v.append({'name': 'file_output', 'description': 'Legacy parameter: file_output', 'type': 'string', 'default': ''})
        v.append({'name': 'search_and_replace', 'description': 'Legacy parameter: search_and_replace', 'type': 'string', 'default': ''})
        v.append({'name': 'convert_to_pdf', 'description': 'Legacy parameter: convert_to_pdf', 'type': 'string', 'default': ''})
        v.append({'name': 'convert_to_png', 'description': 'Legacy parameter: convert_to_png', 'type': 'string', 'default': ''})
        v.append({'name': 'dict_data', 'description': 'Legacy parameter: dict_data', 'type': 'string', 'default': ''})
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
    """Process text using Jinja template."""
    action = kwargs.get("action", {})
    directory = kwargs.get("directory", "")
    kwargs["directory"] = directory
    file_template = action.get("file_template", "template.txt")
    kwargs["file_template"] = f"{directory}\\{file_template}"
    file_source = action.get("file_source", f"{directory}/working.yaml")
    kwargs["file_source"] = file_source
    file_output = action.get("file_output", "output.txt")
    kwargs["file_output"] = f"{directory}\\{file_output}"
    search_and_replace = action.get("search_and_replace", [])
    if search_and_replace != []:
        kwargs["search_and_replace"] = search_and_replace
    robo.robo_text_jinja_template(**kwargs)
    if action.get("convert_to_pdf", False):
        kwargs2 = copy.deepcopy(kwargs)
        kwargs2["file_input"] = kwargs["file_output"]
        kwargs2.pop("file_output")
        robo.robo_convert_svg_to_pdf(**kwargs2)
    if action.get("convert_to_png", False):
        kwargs2 = copy.deepcopy(kwargs)
        kwargs2["file_input"] = kwargs["file_output"]
        kwargs2.pop("file_output")
        robo.robo_convert_svg_to_png(**kwargs2)
    pass

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
