# roboclick_action_corel_object_order

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_object_order`
- Name long: `RoboClick Action: Corel Object Order`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_object_order` (old/oomlout_ai_roboclick.py:1110). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_object_order`
- `object_order`

## Variables

- `order` (string, default ``): Legacy parameter: order

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
