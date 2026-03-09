# roboclick_action_alias_ai_save_image

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_alias_ai_save_image`
- Name long: `RoboClick Action: AI Save Image`
- Category: `Legacy Alias`
- Description: Self-contained action migrated from `ai_save_image` (old/oomlout_ai_roboclick.py:1773). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `ai_save_image`
- `save_image`
- `legacy_alias`

## Variables

- `file_name` (string, default ``): Legacy parameter: file_name
- `position_click` (string, default ``): Legacy parameter: position_click
- `mode_ai_wait` (string, default ``): Legacy parameter: mode_ai_wait

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
