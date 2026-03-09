# roboclick_action_corel_open

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_open`
- Name long: `RoboClick Action: Corel Open`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_open` (old/oomlout_ai_roboclick.py:1121). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_open`
- `open`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
