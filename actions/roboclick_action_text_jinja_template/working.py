import copy
import os

import robo_roboclick

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
    d["description"] = 'Jinja template. When `robo_roboclick.robo_text_jinja_template()` receives string values in `dict_data` or the source yaml, it automatically adds template helper strings for each key: `{key}_upper`, `{key}_lower`, `{key}_length_1` through `{key}_length_9`, plus `{key}_length_1_upper` through `{key}_length_9_upper` and `{key}_length_1_lower` through `{key}_length_9_lower`.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'Text'
    v = []
    if True:
        v.append({'name': 'file_template', 'description': 'Template file to render with Jinja variables.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_output', 'description': 'Output file path for rendered text or converted assets.', 'type': 'string', 'default': ''})
        v.append({'name': 'search_and_replace', 'description': 'Search/replace rules applied during templating.', 'type': 'string', 'default': ''})
        v.append({'name': 'convert_to_pdf', 'description': 'Whether to convert rendered output to PDF.', 'type': 'string', 'default': ''})
        v.append({'name': 'convert_to_png', 'description': 'Whether to convert rendered output to PNG.', 'type': 'string', 'default': ''})
        v.append({'name': 'dict_data', 'description': 'Dictionary data passed into template rendering. For each string value, the template also gets helper strings named `{key}_upper`, `{key}_lower`, `{key}_length_1` to `{key}_length_9`, `{key}_length_1_upper` to `{key}_length_9_upper`, and `{key}_length_1_lower` to `{key}_length_9_lower`.', 'type': 'string', 'default': ''})
        v.append({'name': 'dict_data_yaml_files', 'description': 'Map of template variable names to YAML files whose parsed contents are loaded fresh at render time.', 'type': 'dict', 'default': {}})
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
    return robo_roboclick.robo_action_run("roboclick_action_text_jinja_template", old, **kwargs)

def old(**kwargs):
    """Process text using Jinja template."""
    action = kwargs.get("action", {})
    directory = kwargs.get("directory", "")
    kwargs["directory"] = directory
    file_template = action.get("file_template", "template.txt")
    kwargs["file_template"] = f"{file_template}"
    file_source = action.get("file_source", f"{directory}/working.yaml")
    kwargs["file_source"] = file_source
    file_output = action.get("file_output", "output.txt")
    kwargs["file_output"] = f"{directory}\\{file_output}"
    search_and_replace = action.get("search_and_replace", [])
    if search_and_replace != []:
        kwargs["search_and_replace"] = search_and_replace
    # dict_data_files maps a template variable to a text file whose CONTENT is
    # read fresh at render time; dict_data_files_exists maps a variable to a
    # file name set as the variable's value only if that file EXISTS at render
    # time (else ""). Both let values produced by earlier actions in the same
    # run - a generated joke, a generated background image - reach the template
    # instead of the stale value baked into the source yaml at build time.
    dict_data_files = action.get("dict_data_files", {})
    dict_data_yaml_files = action.get("dict_data_yaml_files", {})
    dict_data_files_exists = action.get("dict_data_files_exists", {})
    has_content = isinstance(dict_data_files, dict) and dict_data_files != {}
    has_yaml = isinstance(dict_data_yaml_files, dict) and dict_data_yaml_files != {}
    has_exists = isinstance(dict_data_files_exists, dict) and dict_data_files_exists != {}
    if has_content or has_yaml or has_exists:
        dict_data = {}
        try:
            dict_data = robo_roboclick.load_yaml_unicode_test(file_source) or {}
        except Exception as error:
            print(f"could not load {file_source} for render-time data: {error}")
        if has_content:
            for key, file_name in dict_data_files.items():
                file_path = file_name if os.path.isabs(file_name) else os.path.join(directory, file_name)
                if os.path.isfile(file_path):
                    with open(file_path, "r", encoding="utf-8") as infile:
                        dict_data[key] = infile.read().strip()
        if has_yaml:
            for key, file_name in dict_data_yaml_files.items():
                file_path = file_name if os.path.isabs(file_name) else os.path.join(directory, file_name)
                if os.path.isfile(file_path):
                    try:
                        dict_data[key] = robo_roboclick.load_yaml_unicode_test(file_path) or {}
                    except Exception as error:
                        print(f"could not load YAML data file {file_path}: {error}")
        if has_exists:
            for key, file_name in dict_data_files_exists.items():
                file_path = file_name if os.path.isabs(file_name) else os.path.join(directory, file_name)
                dict_data[key] = file_name if os.path.isfile(file_path) else ""
        if dict_data != {}:
            kwargs["dict_data"] = dict_data
    robo_roboclick.robo_text_jinja_template(**kwargs)
    if action.get("convert_to_pdf", False):
        kwargs2 = copy.deepcopy(kwargs)
        kwargs2["file_input"] = kwargs["file_output"]
        kwargs2.pop("file_output")
        robo_roboclick.robo_convert_svg_to_pdf(**kwargs2)
    if action.get("convert_to_png", False):
        kwargs2 = copy.deepcopy(kwargs)
        kwargs2["file_input"] = kwargs["file_output"]
        kwargs2.pop("file_output")
        robo_roboclick.robo_convert_svg_to_png(**kwargs2)
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
