# roboclick_action_file_copy

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_file_copy`
- Name long: `RoboClick Action: File Copy`
- Category: `File`
- Description: Self-contained action migrated from `file_copy` (old/oomlout_ai_roboclick.py:1402). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `file_copy`
- `copy`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `file_destination` (string, default ``): Legacy parameter: file_destination

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
