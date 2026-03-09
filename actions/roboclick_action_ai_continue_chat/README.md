# roboclick_action_ai_continue_chat

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_ai_continue_chat`
- Name long: `RoboClick Action: AI Continue Chat`
- Category: `AI`
- Description: Self-contained action migrated from `ai_continue_chat` (old/oomlout_ai_roboclick.py:441). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `ai_continue_chat`
- `continue_chat`

## Variables

- `url_chat` (string, default ``): Legacy parameter: url_chat
- `log_url` (string, default ``): Legacy parameter: log_url

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
