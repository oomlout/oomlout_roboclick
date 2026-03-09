# roboclick_action_corel_set_size

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_set_size`
- Name long: `RoboClick Action: Corel Set Size`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_set_size` (old/oomlout_ai_roboclick.py:1219). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_set_size`
- `set_size`

## Variables

- `width` (string, default ``): Legacy parameter: width
- `height` (string, default ``): Legacy parameter: height
- `max_dimension` (string, default ``): Legacy parameter: max_dimension
- `select_all` (string, default ``): Legacy parameter: select_all

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
