
# This route provides a form for creating a new part source entry.
# When submitted, it creates a directory in parts_source/ and writes all form values to working.yaml.
# The form fields are defined in part_form_fields, and any new fields added here will automatically be included in the YAML output.
from flask import redirect, url_for, flash

# List of fields for the create_part_source form.
# To add a default value, use a 3rd value in the tuple: (field, label, default)
# Example: ("classification", "Classification", "resistor")
part_form_fields = [
    ("classification", "Classification", ""),
    ("type", "Type", ""),
    ("size", "Size", ""),
    ("color", "Color", ""),
    ("description_main", "Description Main", ""),
    ("description_extra", "Description Extra", ""),
    ("manufacturer", "Manufacturer", ""),
    ("part_number", "Part Number", ""),
]

"""Flask web server that renders pages from the web_pages directory."""

import os
import subprocess
import sys
import threading
from importlib import import_module, reload
from pathlib import Path
from typing import Any, Dict

import yaml
from flask import Flask, abort, render_template, request
from jinja2 import TemplateNotFound



# BASE_DIR: Root directory of the project
BASE_DIR = Path(__file__).parent
# TEMPLATE_DIR: All HTML templates for the web server are stored in web_pages/
TEMPLATE_DIR = BASE_DIR / "web_pages"
# STATIC_DIR: Static files (CSS, JS, images) are stored in web_pages/static/
STATIC_DIR = TEMPLATE_DIR / "static"
# SITE_TITLE: Used for display in templates
SITE_TITLE = BASE_DIR.name
# LOCK_FILE: Used to prevent concurrent working_all runs
LOCK_FILE = Path("C:/gh/oomlout_base/lock/working_all.lock")

# Default values for OOMP form fields.
# Used to pre-populate OOMP creation forms in templates.
OOMP_DEFAULTS = {
    "oomp_classification": "",
    "oomp_type": "",
    "oomp_size": "",
    "oomp_color": "",
    "oomp_description_main": "",
    "oomp_description_extra": "",
    "oomp_manufacturer": "",
    "oomp_part_number": "",
    "extra": "",
}


def _load_port_config() -> int:
    """Load port configuration from web_port.yaml file."""
    port_file = BASE_DIR / "web_port.yaml"
    default_port = 5000
    
    if not port_file.exists():
        return default_port
    
    try:
        with port_file.open("r", encoding="utf-8") as handle:
            config = yaml.safe_load(handle)
        
        if isinstance(config, dict) and "port" in config:
            port = config["port"]
            if isinstance(port, int) and 1 <= port <= 65535:
                return port
            else:
                print(f"[config] Invalid port value in {port_file}: {port}; using default {default_port}")
                return default_port
        else:
            print(f"[config] No 'port' key found in {port_file}; using default {default_port}")
            return default_port
    except Exception as exc:
        print(f"[config] Failed to load {port_file}: {exc}; using default {default_port}")
        return default_port

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR),
)
app.config["SITE_TITLE"] = SITE_TITLE

# --- Navigation Auto-Generation ---
# This context processor scans web_pages/ for .html templates (excluding partials/layout) and provides nav_pages to all templates.
@app.context_processor
def inject_nav_pages():
    nav_pages = []
    for template_file in TEMPLATE_DIR.glob("*.html"):
        name = template_file.stem
        # Exclude partials (start with _) and layout.html
        if name.startswith("_") or name == "layout":
            continue
        # Human-friendly title
        title = name.replace("_", " ").title()
        nav_pages.append({
            "name": name,
            "title": title,
            "url": f"/{name}" if name != "index" else "/"
        })
    # Sort: index first, then alphabetical
    nav_pages.sort(key=lambda x: (x["name"] != "index", x["title"]))
    return {"nav_pages": nav_pages}

# --- Launch working_all Endpoint ---
# This endpoint launches action_run_working_all.bat when triggered from the parts source page.
@app.route("/launch_working_all", methods=["POST"])
def launch_working_all():
    """
    Launch action_run_working_all.bat in a new CMD window and redirect back to the create_part_source page.
    """
    try:
        cmd = 'start "Run Working All" cmd /c "action_run_working_all.bat"'
        subprocess.Popen(cmd, shell=True, cwd=Path(__file__).parent)
    except Exception as e:
        # Optionally, log or handle errors here
        pass
    # Always redirect back to the form
    return redirect(url_for("create_part_source"))
# --- Part Source Creation Route ---

# No background monitoring - keep it simple


@app.route("/create_part_source", methods=["GET", "POST"])
def create_part_source():
    """
    Render a form for creating a new part source entry and handle its submission.
    On POST, creates a directory in parts_source/ and writes all form values to working.yaml.
    The form fields are defined in part_form_fields above. To add new fields, simply add to that list.
    """
    if request.method == "POST":
        # Collect all form values into a dictionary (all fields optional, use default if blank)
        form_data = {}
        for field_tuple in part_form_fields:
            if len(field_tuple) == 3:
                field, _, default = field_tuple
            else:
                field, _ = field_tuple
                default = ""
            form_data[field] = request.form.get(field, default)
        # Directory name is a combination of all field values, joined by underscores ("none" for empty fields)
        dir_name = "_".join([form_data[field].replace(" ", "_") or "none" for field_tuple in part_form_fields for field in [field_tuple[0]]])
        part_dir = BASE_DIR / "parts_source" / dir_name
        part_dir.mkdir(parents=True, exist_ok=True)
        # Write all form data to working.yaml in the new directory
        with open(part_dir / "working.yaml", "w", encoding="utf-8") as f:
            yaml.dump(form_data, f, allow_unicode=True)
        # Redirect to the form with a success query parameter (no flash, no secret key needed)
        return redirect(url_for("create_part_source", created=dir_name))
    # On GET, render the form
    # Pass a list of (field, label, default) to the template for easy rendering
    form_fields_for_template = []
    for field_tuple in part_form_fields:
        if len(field_tuple) == 3:
            field, label, default = field_tuple
        else:
            field, label = field_tuple
            default = ""
        form_fields_for_template.append((field, label, default))
    return render_template(
        "create_part_source.html",
        page_title="Create Part Source",
        part_form_fields=form_fields_for_template,
    )

def run_working_all_with_file_lock():
    """
    Launch action_run_working_all.bat in a new CMD window and close the window after execution.
    Lock file checking is removed for simplicity.
    """
    try:
        # Command to run the batch file and close the window after execution
        cmd = 'start "Run Working All" cmd /c "action_run_working_all.bat"'
        app.logger.info("Launching action_run_working_all.bat in new CMD window...")
        subprocess.Popen(cmd, shell=True, cwd=Path(__file__).parent)
        app.logger.info("CMD window launched successfully")
        return True
    except Exception as e:
        app.logger.error(f"Error launching action_run_working_all.bat: {e}")
        return False
def get_working_all_status():
    """Get the current status of working_all execution."""
    is_running = LOCK_FILE.exists()
    
    status = {
        "is_running": is_running,
        "lock_file": str(LOCK_FILE)
    }
    
    if is_running:
        try:
            with open(LOCK_FILE, 'r') as f:
                status["pid"] = int(f.read().strip())
        except (ValueError, FileNotFoundError):
            status["pid"] = None
    
    return status


def _load_page_hooks():
    """Load (and hot-reload) the optional page hook module."""
    module_name = "web_pages.page_hooks"
    try:
        if module_name in globals().get("_hook_cache", {}):
            module = reload(globals()["_hook_cache"][module_name])
        else:
            module = import_module(module_name)
        globals().setdefault("_hook_cache", {})[module_name] = module
        return module
    except ModuleNotFoundError:
        return None


def _derive_page_title(template_name: str) -> str:
    """Return a fallback page title based on the template name."""
    base_name = template_name.rsplit(".", 1)[0]
    return base_name.replace("_", " ").title()


def render_page(template_name: str, **context: Any):
    """
    Render a template and run optional hooks around the render.
    This function is the main entry point for rendering HTML pages.
    It also injects navigation and debug context for templates.
    """
    hooks = _load_page_hooks()
    context_data: Dict[str, Any] = {
        "site_title": app.config.get("SITE_TITLE", SITE_TITLE),
        "request_method": request.method,
    }
    context_data.update(context)
    context_data.setdefault("page_title", _derive_page_title(template_name))

    hook_meta: Dict[str, Any] = {"template": template_name}
    if hooks and hasattr(hooks, "before_render"):
        extra = hooks.before_render(template_name, context_data)
        if isinstance(extra, dict):
            context_data.update(extra)
        hook_meta["hook_module"] = getattr(hooks, "__name__", "web_pages.page_hooks")
    else:
        hook_meta["hook_module"] = None

    context_keys = sorted(context_data.keys())
    context_data.setdefault("debug_info", {}).update({**hook_meta, "context_keys": context_keys})
    app.logger.debug("Rendering %s with context keys: %s", template_name, context_keys)

    try:
        return render_template(template_name, **context_data)
    except TemplateNotFound:
        abort(404)


@app.route("/")
def index():
    """
    Serve the main index page.
    This is the homepage for the web server. It renders index.html from web_pages/.
    """
    return render_page("index.html", page_title="Home")


## Route removed: /make_spelling_cards
# This route was removed because its template does not exist. If you wish to restore it, add make_spelling_cards.html to web_pages/ and re-add the route.

@app.route("/run_batch_only", methods=["POST"])
def run_batch_only():
    """
    Run the batch file without adding anything to working.yaml.
    Used for manual batch processing. Launches run_working_all.bat in a new window.
    """
    import os
    from pathlib import Path
    
    try:
        working_dir = str(Path(__file__).parent)
        os.system(f'start "Working All" /D "{working_dir}" cmd /c run_working_all.bat')
        return {"success": True, "message": "Batch file started successfully!"}
    except Exception as e:
        return {"success": False, "message": f"Failed to start batch file: {e}"}


@app.route("/working_all_status")
def working_all_status():
    """
    Return the status of working_all execution.
    Returns a JSON with lock file and PID if running.
    """
    status = get_working_all_status()
    return status


@app.route("/run_working_all", methods=["POST"])
def trigger_working_all():
    """
    Manually trigger working_all execution.
    Handles lock file logic and batch queuing for safe concurrent runs.
    """
    if LOCK_FILE.exists():
        print("[DEBUG] Lock file exists - entering queue mode")
        # Add run instruction to batch file for queuing
        batch_file = Path("C:/gh/oomlout_base/lock/working_all.bat")
        working_dir = str(BASE_DIR)
        
        # Create the command line
        command_line = f'cd /d "{working_dir}" && python working_all.py\n'
        print(f"[DEBUG] Command to queue: {command_line.strip()}")
        
        # Check if this command is already in the file
        if batch_file.exists():
            print(f"[DEBUG] Batch file exists at: {batch_file}")
            with open(batch_file, 'r') as f:
                existing_content = f.read()
            print(f"[DEBUG] Current batch file content:\n{existing_content}")
            if command_line.strip() in existing_content:
                print("[DEBUG] Command already in queue - skipping")
                return {"message": "working_all is already running - command already in queue"}
        else:
            print(f"[DEBUG] Batch file does not exist yet at: {batch_file}")
        
        # Append the command if not already there
        print("[DEBUG] Appending command to batch file")
        with open(batch_file, 'a') as f:
            f.write(command_line)
        print("[DEBUG] Command successfully added to queue")
        
        return {"message": "working_all is already running - added to queue in working_all.bat"}
    
    print("[DEBUG] No lock file - creating launcher batch file")
    
    # Create a temporary batch file with lock logic
    working_dir = str(BASE_DIR)
    lock_file_str = str(LOCK_FILE).replace('/', '\\')
    
    launcher_bat = BASE_DIR / "run_working_all_launcher.bat"
    
    batch_content = f'''@echo off
echo Starting working_all.py...
echo %TIME% > "{lock_file_str}"
cd /d "{working_dir}"
python working_all.py
python working_all.py
del "{lock_file_str}"
echo Done!
pause
'''
    
    print(f"[DEBUG] Creating launcher batch file at: {launcher_bat}")
    with open(launcher_bat, 'w') as f:
        f.write(batch_content)
    
    # Launch the batch file
    cmd = f'start "Working All" "{launcher_bat}"'
    print(f"[DEBUG] Executing command: {cmd}")
    os.system(cmd)
    os.system(cmd)
    
    return {"message": "Started working_all in new window"}


## Route removed: /oomp_create
# This route was removed as part of the cleanup. The page is now only accessible as a static template if present in web_pages/.

@app.route("/<path:page_name>")
def serve_page(page_name: str):
    """
    Serve any template from the web_pages directory.
    This dynamic route allows any .html file in web_pages/ to be accessed directly by its name.
    Example: /index or /oomp_create will serve index.html or oomp_create.html if present.
    SECURITY NOTE: Only .html files in web_pages/ are accessible. This prevents access to non-template files.
    If a template does not exist, a 404 is returned.
    """
    template_name = page_name if page_name.endswith(".html") else f"{page_name}.html"
    return render_page(template_name)


if __name__ == "__main__":
    port = _load_port_config()
    print(f"[config] Starting server on port {port}")
    # Print all registered routes for debugging and future maintainers.
    # Remove or comment out in production for security.
    print("[routes] Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule.rule} [{','.join(rule.methods)}]")
    # Start the Flask server
    app.run(host="0.0.0.0", port=port, debug=False)
