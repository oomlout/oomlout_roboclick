# roboclick_action_corel_export

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_export`
- Name long: `RoboClick Action: Corel Export`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_export` (old/oomlout_ai_roboclick.py:1047). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_export`
- `export`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `file_destination` (string, default ``): Legacy parameter: file_destination
- `file_type` (string, default ``): Legacy parameter: file_type
- `delay` (string, default ``): Legacy parameter: delay

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
