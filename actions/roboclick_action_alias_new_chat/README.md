# roboclick_action_alias_new_chat

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_alias_new_chat`
- Name long: `RoboClick Action: New Chat`
- Category: `Legacy Alias`
- Description: Self-contained action migrated from `new_chat` (old/oomlout_ai_roboclick.py:1763). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `new_chat`
- `legacy_alias`

## Variables

- `description` (string, default ``): Legacy parameter: description
- `log_url` (string, default ``): Legacy parameter: log_url

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
