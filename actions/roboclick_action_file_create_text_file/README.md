# roboclick_action_file_create_text_file

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_file_create_text_file`
- Name long: `RoboClick Action: File Create Text File`
- Category: `File`
- Description: Self-contained action migrated from `file_create_text_file` (old/oomlout_ai_roboclick.py:1429). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `file_create_text_file`
- `create_text_file`

## Variables

- `file_name` (string, default ``): Legacy parameter: file_name
- `content` (string, default ``): Legacy parameter: content

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
