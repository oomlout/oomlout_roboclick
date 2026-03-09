# roboclick_action_save_image_search_result

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_save_image_search_result`
- Name long: `RoboClick Action: Save Image Search Result`
- Category: `AI Image`
- Description: Self-contained action migrated from `save_image_search_result` (old/oomlout_ai_roboclick.py:1796). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `save_image_search_result`

## Variables

- `index` (string, default ``): Legacy parameter: index
- `file_name` (string, default ``): Legacy parameter: file_name
- `overwrite` (string, default ``): Legacy parameter: overwrite
- `position_click` (string, default ``): Legacy parameter: position_click

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
