"""Flask web server that renders pages from the web_pages directory."""

from importlib import import_module, reload
from pathlib import Path
from typing import Any, Dict

import yaml
from flask import Flask, abort, render_template, request
from jinja2 import TemplateNotFound


TEMPLATE_DIR = Path(__file__).parent / "web_pages"
STATIC_DIR = TEMPLATE_DIR / "static"
SITE_TITLE = Path(__file__).parent.name
app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR),
)
app.config["SITE_TITLE"] = SITE_TITLE


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
    """Render a template and run optional hooks around the render."""
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
    """Serve the index page."""
    return render_page("index.html", page_title="Flask Index")


@app.route("/<path:page_name>")
def serve_page(page_name: str):
    """Serve any template from the web_pages directory."""
    template_name = page_name if page_name.endswith(".html") else f"{page_name}.html"
    return render_page(template_name)


if __name__ == "__main__":
    # Load port from web_port.yaml file
    port = 5000  # Default port
    port_file = Path(__file__).parent / "web_port.yaml"
    if port_file.exists():
        with open(port_file, 'r') as f:
            port_config = yaml.safe_load(f)
            if port_config and 'port' in port_config:
                port = port_config['port']
    
    app.run(host="0.0.0.0", port=port, debug=True)
