# roboclick_action_alias_close_tab

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_alias_close_tab`
- Name long: `RoboClick Action: Close Tab`
- Category: `Legacy Alias`
- Description: Self-contained action migrated from `close_tab` (old/oomlout_ai_roboclick.py:1758). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `close_tab`
- `legacy_alias`

## Variables

- _none_

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
