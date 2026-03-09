# roboclick_action_corel_convert_to_curves

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_convert_to_curves`
- Name long: `RoboClick Action: Corel Convert To Curves`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_convert_to_curves` (old/oomlout_ai_roboclick.py:1023). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_convert_to_curves`
- `convert_to_curves`

## Variables

- `ungroup` (string, default ``): Legacy parameter: ungroup
- `delay` (string, default ``): Legacy parameter: delay

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
