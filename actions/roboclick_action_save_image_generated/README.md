# roboclick_action_save_image_generated

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_save_image_generated`
- Name long: `RoboClick Action: Save Image Generated`
- Category: `AI Image`
- Description: Self-contained action migrated from `save_image_generated` (old/oomlout_ai_roboclick.py:1790). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `save_image_generated`

## Variables

- `file_name` (string, default ``): Legacy parameter: file_name
- `position_click` (string, default ``): Legacy parameter: position_click
- `mode_ai_wait` (string, default ``): Legacy parameter: mode_ai_wait

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
