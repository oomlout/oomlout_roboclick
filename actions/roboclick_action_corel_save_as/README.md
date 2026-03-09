# roboclick_action_corel_save_as

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_save_as`
- Name long: `RoboClick Action: Corel Save As`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_save_as` (old/oomlout_ai_roboclick.py:1177). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_save_as`
- `save_as`

## Variables

- `file_name` (string, default ``): Legacy parameter: file_name

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
