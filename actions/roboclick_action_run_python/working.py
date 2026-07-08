import json
import os
import subprocess
import sys
import robo_roboclick

d = {}

def describe():
    global d
    d = {}
    d["name_long_1"] = 'roboclick'
    d["name_long_2"] = 'action'
    d["name_long_3"] = 'run'
    d["name_long_4"] = 'python'
    d["name_long_5"] = 'run_python'
    d["name_long"] = ""
    for i in range(1, 50):
        adding = d.get(f"name_long_{i}", "")
        if adding != "":
            if d["name_long"]:
                d["name_long"] += "_"
            d["name_long"] += adding
    if d["name_long"].endswith("_"):
        d["name_long"] = d["name_long"][:-1]
    d["name"] = 'roboclick_action_run_python'
    d["name_long"] = 'roboclick_action_run_python'
    d["name_short"] = ['run_python', 'python_run']
    d["name_short_options"] = ['run_python', 'python_run']
    d["description"] = 'Run a local python script, passing the action details to it as a json kwargs argument.'
    d["returns"] = 'Pass-through action result.'
    d["category"] = 'File'
    v = []
    if True:
        v.append({'name': 'file_python', 'description': 'Path to the python script to run.', 'type': 'string', 'default': ''})
        v.append({'name': 'file_output', 'description': 'Path to the output file the script should create, relative to the part directory.', 'type': 'string', 'default': ''})
        v.append({'name': 'timeout', 'description': 'Maximum seconds to wait for the script to finish.', 'type': 'string', 'default': '600'})
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
    return robo_roboclick.robo_action_run("roboclick_action_run_python", old, **kwargs)

def old(**kwargs):
    """Run a python script with the action details passed as --kwargs json"""
    action = kwargs.get("action", {})
    file_python = action.get("file_python", "")
    directory = kwargs.get("directory", "")
    try:
        timeout = float(action.get("timeout", "600"))
    except (TypeError, ValueError):
        timeout = 600.0

    if file_python == "":
        print("file_python not set, skipping run_python")
        return ""

    if not os.path.isfile(file_python):
        print(f"python file {file_python} does not exist")
        return "exit_no_tab"

    # build the kwargs handed to the script: everything in the action dict
    # except the roboclick bookkeeping keys, with file_* paths (inputs and
    # outputs) resolved against the part directory so the script can use them
    script_kwargs = {}
    for key, value in action.items():
        if key in ("command", "description", "file_python", "timeout"):
            continue
        if key.startswith("file_") and isinstance(value, str) and value != "" and not os.path.isabs(value):
            value = os.path.join(directory, value)
        script_kwargs[key] = value
    script_kwargs["directory"] = directory

    file_output = script_kwargs.get("file_output", "")

    command = [sys.executable, file_python, "--kwargs", json.dumps(script_kwargs)]
    print(f"running python {file_python}")
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"python file {file_python} timed out after {timeout} seconds")
        return "exit_no_tab"

    if completed.stdout:
        print(completed.stdout.strip())
    if completed.returncode != 0:
        if completed.stderr:
            print(completed.stderr.strip())
        print(f"python file {file_python} failed with return code {completed.returncode}")
        return "exit_no_tab"

    if file_output != "" and not os.path.isfile(file_output):
        print(f"python file {file_python} did not create {file_output}")
        return "exit_no_tab"

    return ""

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
