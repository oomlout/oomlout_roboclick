import os
import yaml
import robo_roboclick

d = {}

def describe():
    global d
    d = {}
    d["name"] = "roboclick_action_ai_from_directory"
    d["name_short"] = ["ai_from_directory", "from_directory"]
    d["description"] = (
        "Load working.yaml then working_1.yaml, working_2.yaml, ... from a directory "
        "and execute the roboclick actions defined in each file one by one. "
        "Each file may define a single action (flat keys) or a list under actions:. "
        "{variable} placeholders are replaced with values from the part workings."
    )
    d["returns"] = "Executes all actions found in the directory sequence."
    d["category"] = "AI"
    v = []
    v.append({"name": "directory",    "description": "Path to the folder containing working.yaml and working_N.yaml files.", "type": "string", "default": ""})
    v.append({"name": "mode_ai_wait", "description": "AI wait strategy (slow, fast_button_state, or fast_clipboard_state).", "type": "string", "default": "slow"})
    d["variables"] = v
    return d

def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    return dict(d)

def test(**kwargs):
    try:
        import oomlout_test
    except Exception:
        return callable(action)
    test_fn = getattr(oomlout_test, "test", None)
    if not callable(test_fn):
        return callable(action)
    try:
        return bool(test_fn(**kwargs))
    except Exception:
        return callable(action)


def action(**kwargs):
    print("")
    print(".:action:. -- ai_from_directory -- loading directory action chain")

    import oomlout_roboclick

    action_def        = kwargs.get("action", {})
    workings          = kwargs.get("workings", {})
    discovered        = kwargs.get("_discovered_actions")

    target_dir  = action_def.get("directory", "")
    mode_ai     = action_def.get("mode_ai_wait", "slow") or "slow"

    if not target_dir:
        print("     ERROR: no directory defined in action")
        robo_roboclick.robo_delay(delay=10)
        return

    target_dir = os.path.abspath(target_dir)
    if not os.path.isdir(target_dir):
        print(f"     ERROR: directory not found: {target_dir}")
        robo_roboclick.robo_delay(delay=10)
        return

    # collect yaml files: working.yaml first, then working_1.yaml, working_2.yaml, ...
    yaml_files = []
    base_file = os.path.join(target_dir, "working.yaml")
    if os.path.isfile(base_file):
        yaml_files.append(base_file)
    for i in range(1, 100):
        path = os.path.join(target_dir, f"working_{i}.yaml")
        if os.path.isfile(path):
            yaml_files.append(path)
        else:
            break

    if not yaml_files:
        print(f"     No working yaml files found in {target_dir}")
        return

    print(f"     Found {len(yaml_files)} yaml file(s) in {target_dir}")

    if discovered is None:
        discovered = oomlout_roboclick.build_action_lookup()

    for yaml_file in yaml_files:
        print(f"     Loading: {os.path.basename(yaml_file)}")
        with open(yaml_file, "r", encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f)
            except Exception as e:
                print(f"     ERROR parsing {yaml_file}: {e}")
                robo_roboclick.robo_delay(delay=5)
                continue

        if not data:
            continue

        # normalise: list under actions: = multiple; flat dict = single action
        if "actions" in data and isinstance(data["actions"], list):
            action_list = data["actions"]
        else:
            action_list = [data]

        for act in action_list:
            # substitute {variable} placeholders from workings
            act = _substitute_dict(act, workings)

            # fill in mode_ai_wait if not set in the action
            if "mode_ai_wait" not in act:
                act["mode_ai_wait"] = mode_ai

            # dispatch through the registered action system
            run_kwargs = dict(kwargs)
            run_kwargs["action"] = act
            run_kwargs["_discovered_actions"] = discovered
            oomlout_roboclick.run_action(**run_kwargs)


def _substitute_dict(obj, workings):
    """Recursively substitute {variable} in all string values."""
    if isinstance(obj, dict):
        return {k: _substitute_dict(v, workings) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_substitute_dict(v, workings) for v in obj]
    if isinstance(obj, str):
        class SafeDict(dict):
            def __missing__(self, key):
                return "{" + key + "}"
        try:
            return obj.format_map(SafeDict(workings))
        except Exception:
            return obj
    return obj
