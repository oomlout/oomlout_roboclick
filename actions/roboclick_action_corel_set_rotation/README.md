# roboclick_action_corel_set_rotation

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_set_rotation`
- Name long: `RoboClick Action: Corel Set Rotation`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_set_rotation` (old/oomlout_ai_roboclick.py:1207). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_set_rotation`
- `set_rotation`

## Variables

- `angle` (string, default ``): Legacy parameter: angle

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
