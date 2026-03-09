# roboclick_action_wait_for_file

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_wait_for_file`
- Name long: `RoboClick Action: Wait For File`
- Category: `Utility`
- Description: Self-contained action migrated from `wait_for_file` (old/oomlout_ai_roboclick.py:1853). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `wait_for_file`

## Variables

- `file_name` (string, default ``): Legacy parameter: file_name
- `file_name_1` (string, default ``): Legacy parameter: file_name_1
- `file_name_2` (string, default ``): Legacy parameter: file_name_2
- `file_name_3` (string, default ``): Legacy parameter: file_name_3
- `file_name_4` (string, default ``): Legacy parameter: file_name_4
- `file_name_5` (string, default ``): Legacy parameter: file_name_5
- `file_name_6` (string, default ``): Legacy parameter: file_name_6

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
