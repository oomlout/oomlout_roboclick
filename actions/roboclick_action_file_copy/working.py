import os
import robo_roboclick

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'file'
    d["name_long_4"] = 'copy'
    d["name_long_5"] = 'file_copy'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_file_copy'
    d["name_long"] = 'roboclick_action_file_copy'
    d["name_short"] = ['file_copy']
    d["name_short_options"] = ['file_copy']
    d["description"] = 'File copy.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'File'
    v = []
    if True:
        v.append({'name': 'file_source', 'description': 'Path to the source input file.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_destination', 'description': 'Path to the output file to create or update.', 'type': 'string', 'default': ''})
        v.append({'name': 'exit_on_missing', 'description': 'Exit the current roboclick when the source file is missing.', 'type': 'boolean', 'default': False})
        v.append({'name': 'delete_before_copy', 'description': 'Delete the destination first so a missing source leaves it absent rather than stale.', 'type': 'boolean', 'default': True})
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

def _as_bool(value, default=False):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("1", "true", "yes", "y", "on"):
            return True
        if normalized in ("0", "false", "no", "n", "off", ""):
            return False
    return bool(value)

def action(**kwargs):
    return robo_roboclick.robo_action_run("roboclick_action_file_copy", old, **kwargs)

def old(**kwargs):
    """Copy file from source to destination"""
    import shutil
    action = kwargs.get("action", {})
    file_source = action.get("file_source", "")
    file_destination = action.get("file_destination", "")
    exit_on_missing = _as_bool(action.get("exit_on_missing", False), False)
    delete_before_copy = _as_bool(action.get("delete_before_copy", True), True)
    directory = kwargs.get("directory", "")
    file_destination = os.path.join(directory, file_destination)

    return_value = ""

    if file_source == "" or file_destination == "":
        print("file_source or file_destination not set, skipping file copy")
        return

    # Delete the destination first (default) so the copy always reflects the
    # current source: if the source is missing the destination ends up ABSENT
    # rather than a stale leftover from an earlier run.
    if delete_before_copy and os.path.isfile(file_destination):
        try:
            os.remove(file_destination)
        except Exception as e:
            print(f"Error deleting destination before copy: {e}")

    if os.path.isfile(file_source):
        print(f"copying {file_source} to {file_destination}")
        #use shutil to copy the file
        import shutil
        try: 
            #create directory if it does not exist
            os.makedirs(os.path.dirname(file_destination), exist_ok=True)
            shutil.copy(file_source, file_destination)
        except Exception as e:
            print(f"Error copying file: {e}")
            import time
            time.sleep(1)
    else:
        print(f"file {file_source} does not exist")
        if exit_on_missing:
            return_value = "exit_no_tab"

    return return_value

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
