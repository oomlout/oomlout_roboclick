# roboclick_action_corel_page_goto

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_page_goto`
- Name long: `RoboClick Action: Corel Page Goto`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_page_goto` (old/oomlout_ai_roboclick.py:1134). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_page_goto`
- `page_goto`

## Variables

- `page_number` (string, default ``): Legacy parameter: page_number

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
