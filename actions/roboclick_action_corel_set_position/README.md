# roboclick_action_corel_set_position

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_set_position`
- Name long: `RoboClick Action: Corel Set Position`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_set_position` (old/oomlout_ai_roboclick.py:1192). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_set_position`
- `set_position`

## Variables

- `x` (string, default ``): Legacy parameter: x
- `y` (string, default ``): Legacy parameter: y

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
