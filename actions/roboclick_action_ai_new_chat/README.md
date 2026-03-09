# roboclick_action_ai_new_chat

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_ai_new_chat`
- Name long: `RoboClick Action: AI New Chat`
- Category: `AI`
- Description: Self-contained action migrated from `ai_new_chat` (old/oomlout_ai_roboclick.py:564). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `ai_new_chat`
- `new_chat`

## Variables

- `log_url` (string, default ``): Legacy parameter: log_url
- `description` (string, default ``): Legacy parameter: description

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
