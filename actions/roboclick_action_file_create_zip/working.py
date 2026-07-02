import os
import zipfile


def define():
    return {
        "name": "roboclick_action_file_create_zip",
        "name_short": ["create_zip", "file_create_zip"],
        "description": (
            "Create a zip from explicit files and/or directory trees. "
            "If any required source is missing, write a <zip>_error.txt listing the gaps and exit the chain. "
            "On success, delete any prior error file."
        ),
        "variables": [
            {
                "name": "zip_path",
                "description": "Absolute path where the zip file should be written.",
                "type": "string",
                "default": "",
            },
            {
                "name": "files",
                "description": (
                    "List of dicts with 'arcname' (name inside zip) and 'source' (absolute path). "
                    "Example: [{'arcname': 'story_guide.md', 'source': '/abs/path/story_guide.md'}]"
                ),
                "type": "list",
                "default": [],
            },
            {
                "name": "dirs",
                "description": (
                    "List of dicts with 'path' (absolute dir to walk recursively) and "
                    "'arcname_prefix' (prefix inside the zip for files in this dir). "
                    "Example: [{'path': '/abs/source/raw', 'arcname_prefix': 'source/raw'}]. "
                    "Dirs must exist; missing dirs are reported as errors."
                ),
                "type": "list",
                "default": [],
            },
        ],
        "category": "File",
    }


def _resolve(path, directory):
    """Resolve path against directory if relative, then normalise."""
    if not path:
        return ""
    if not os.path.isabs(path):
        path = os.path.join(directory, path)
    return os.path.normpath(path)


def action(**kwargs):
    action_cfg = kwargs.get("action", {})
    zip_path   = action_cfg.get("zip_path", "")
    files      = action_cfg.get("files", [])
    dirs       = action_cfg.get("dirs", [])
    directory  = kwargs.get("directory", "")

    if not zip_path:
        print("[create_zip] ERROR: zip_path not set")
        return "exit"

    zip_path   = _resolve(zip_path, directory)
    error_path = os.path.splitext(zip_path)[0] + "_error.txt"

    missing = []

    # Check explicit files (paths may be relative to part directory)
    for entry in files:
        src = _resolve(entry.get("source", ""), directory)
        if not src or not os.path.isfile(src):
            missing.append(src or "(no source specified)")
        else:
            entry["_resolved"] = src

    # Check dirs exist (paths may be relative to part directory)
    for entry in dirs:
        d = _resolve(entry.get("path", ""), directory)
        if not d or not os.path.isdir(d):
            missing.append(f"(dir) {d or '(no path specified)'}")
        else:
            entry["_resolved"] = d

    if missing:
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        with open(error_path, "w", encoding="utf-8") as f:
            f.write("create_zip: missing sources -- zip not created.\n\n")
            for m in missing:
                f.write(f"  MISSING: {m}\n")
        print(f"[create_zip] {len(missing)} source(s) missing -- wrote {error_path}")
        for m in missing:
            print(f"  MISSING: {m}")
        return "exit"

    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    total = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for entry in files:
            zf.write(entry["_resolved"], entry["arcname"])
            total += 1
        for entry in dirs:
            base    = entry["_resolved"]
            prefix  = entry.get("arcname_prefix", os.path.basename(base))
            for root, _, filenames in os.walk(base):
                for fname in sorted(filenames):
                    abs_path = os.path.join(root, fname)
                    rel      = os.path.relpath(abs_path, base).replace("\\", "/")
                    arcname  = f"{prefix}/{rel}" if prefix else rel
                    zf.write(abs_path, arcname)
                    total += 1

    if os.path.exists(error_path):
        os.remove(error_path)

    print(f"[create_zip] zip created: {zip_path} ({total} files)")
    return ""


def test(**kwargs):
    return callable(action)
