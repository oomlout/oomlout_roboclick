"""Per-request hooks for pages under web_pages/."""

from datetime import datetime
from typing import Any, Dict

from flask import request

BRANCH_MESSAGES = {
    "index.html": "Index branch active.",
    "example.html": "Example branch active.",
    "example_form.html": "Form branch active.",
}
DEFAULT_BRANCH = "Default branch."


def _handle_index(context: Dict[str, Any]) -> Dict[str, Any]:
    """Collect metadata specific to the index page."""
    context.setdefault("page_meta", {})["highlight"] = "index"
    return {
        "branch": BRANCH_MESSAGES["index.html"],
        "notes": ["Index page highlighted for visitors."],
    }


def _handle_example(context: Dict[str, Any]) -> Dict[str, Any]:
    """Collect metadata specific to the example page."""
    context.setdefault("page_meta", {})["highlight"] = "example"
    return {
        "branch": BRANCH_MESSAGES["example.html"],
        "notes": ["Example content prepared."],
    }


def _handle_example_form(context: Dict[str, Any]) -> Dict[str, Any]:
    """Collect metadata specific to the form page."""
    context.setdefault("page_meta", {})["highlight"] = "example_form"

    is_post = request.method == "POST"
    form_data = dict(request.form) if is_post else {}

    context["form_data"] = form_data
    context["form_submitted"] = is_post

    return {
        "branch": BRANCH_MESSAGES["example_form.html"],
        "notes": ["Form submitted." if is_post else "Awaiting form submission."],
        "extra_context": {"submitted_data": form_data} if is_post else {}
    }


def _handle_default(context: Dict[str, Any], template_name: str) -> Dict[str, Any]:
    """Fallback handler for pages without a dedicated routine."""
    context.setdefault("page_meta", {})["highlight"] = template_name
    return {
        "branch": DEFAULT_BRANCH,
        "notes": ["Generic handler executed."],
    }


def process_page(template_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch to the appropriate per-page routine using an if-tree."""
    if template_name == "index.html":
        handler = _handle_index
        handler_kwargs: Dict[str, Any] = {}
    elif template_name == "example.html":
        handler = _handle_example
        handler_kwargs = {}
    elif template_name == "example_form.html":
        handler = _handle_example_form
        handler_kwargs = {}
    else:
        handler = _handle_default
        handler_kwargs = {"template_name": template_name}

    result = handler(context, **handler_kwargs)
    result.setdefault("handler", handler.__name__)
    result.setdefault("notes", [])
    result.setdefault("extra_context", {})
    return result


def before_render(template_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Update the template context before rendering."""
    page_result = process_page(template_name, context)
    timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    branch = page_result["branch"]
    handler_name = page_result["handler"]
    notes = page_result.get("notes", [])
    extra_context = page_result.get("extra_context")

    if isinstance(extra_context, dict) and extra_context:
        context.update(extra_context)

    hook_debug = {
        "branch": branch,
        "handler": handler_name,
        "notes": notes,
        "template": template_name,
        "timestamp": timestamp,
        "form_payload": context.get("form_data") if template_name == "example_form.html" else None,
    }

    context["hook_branch"] = branch
    context["hook_debug"] = hook_debug
    context.setdefault("debug_info", {}).update(hook_debug)
    context.setdefault("page_meta", {})["handler"] = handler_name

    return {"hook_timestamp": timestamp}
