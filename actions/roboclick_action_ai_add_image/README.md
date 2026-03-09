# roboclick_action_ai_add_image

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_ai_add_image`
- Name long: `RoboClick Action: AI Add Image`
- Category: `AI`
- Description: Self-contained action migrated from `ai_add_image` (old/oomlout_ai_roboclick.py:381). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `ai_add_image`
- `add_image`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `position_click` (string, default ``): Legacy parameter: position_click
- `mode -- source_files from source_files directory` (string, default ``): Legacy parameter: mode -- source_files from source_files directory

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
