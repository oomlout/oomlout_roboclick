# roboclick_action_alias_add_image

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_alias_add_image`
- Name long: `RoboClick Action: Add Image`
- Category: `Legacy Alias`
- Description: Self-contained action migrated from `add_image` (old/oomlout_ai_roboclick.py:1748). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `add_image`
- `legacy_alias`

## Variables

- `file_name` (string, default ``): Legacy parameter: file_name
- `position_click` (string, default ``): Legacy parameter: position_click

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
