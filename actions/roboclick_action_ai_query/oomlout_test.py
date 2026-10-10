from __future__ import annotations

from typing import Any
import working


def test(**kwargs) -> dict[str, Any]:
    failures = []
    
    # Test 1: describe contains base_ai_provider variable
    desc = working.describe()
    vars_list = desc.get("variables", [])
    has_provider_var = any(v.get("name") == "base_ai_provider" for v in vars_list)
    if not has_provider_var:
        failures.append("describe() missing base_ai_provider variable")
        
    # Test 2: provider resolution
    cases = [
        ({"action": {"base_ai_provider": "gemini"}}, "gemini"),
        ({"base_ai_provider": "claude"}, "claude"),
        ({"workings": {"base_ai_provider": "open_web_ui"}}, "open_web_ui"),
        ({}, "open_ai"),
    ]
    for case_kwargs, expected in cases:
        got = working._get_base_ai_provider(case_kwargs)
        if got != expected:
            failures.append(f"_get_base_ai_provider({case_kwargs}) returned '{got}', expected '{expected}'")

    # Test 3: new() dispatches to action_gemini
    called = []
    orig_gemini = working.action_gemini
    working.action_gemini = lambda **k: called.append("gemini") or "ok_gemini"
    try:
        res = working.new(base_ai_provider="gemini")
        if res != "ok_gemini" or "gemini" not in called:
            failures.append("new(base_ai_provider='gemini') did not dispatch to action_gemini")
    finally:
        working.action_gemini = orig_gemini

    return {
        "all_passed": len(failures) == 0,
        "passed": 3 - len(failures),
        "failed": len(failures),
        "details": failures,
    }
