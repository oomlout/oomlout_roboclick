# roboclick_action_corel_paste

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_paste`
- Name long: `RoboClick Action: Corel Paste`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_paste` (old/oomlout_ai_roboclick.py:1145). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_paste`
- `paste`

## Variables

- `x` (string, default ``): Legacy parameter: x
- `y` (string, default ``): Legacy parameter: y
- `width` (string, default ``): Legacy parameter: width
- `height` (string, default ``): Legacy parameter: height

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
