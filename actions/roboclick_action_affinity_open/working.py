import copy

import robo_roboclick

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'affinity'
    d["name_long_4"] = 'open'
    d["name_long_5"] = 'affinity_open'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_affinity_open'
    d["name_long"] = 'roboclick_action_affinity_open'
    d["name_short"] = ['affinity_open', 'open']
    d["name_short_options"] = ['affinity_open', 'open']
    d["description"] = 'Affinity open.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Affinity'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
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
    """Open file in Affinity."""
    action = kwargs.get("action", {})
    # Use file_source when available
    file_name = action.get("file_source", None)
    if not file_name:
        file_name = action.get("file_name", "")
    kwargs2 = copy.deepcopy(kwargs)
    kwargs2["file_name"] = file_name
    robo_roboclick.robo_affinity_open(**kwargs2)

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
