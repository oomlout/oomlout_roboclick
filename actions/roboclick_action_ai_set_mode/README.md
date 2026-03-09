# roboclick_action_ai_set_mode

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_ai_set_mode`
- Name long: `RoboClick Action: AI Set Mode`
- Category: `AI`
- Description: Self-contained action migrated from `ai_set_mode` (old/oomlout_ai_roboclick.py:720). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `ai_set_mode`
- `set_mode`

## Variables

- `mode` (string, default ``): Legacy parameter: mode

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
