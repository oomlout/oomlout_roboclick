# roboclick_action_browser_close_tab

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_browser_close_tab`
- Name long: `RoboClick Action: Browser Close Tab`
- Category: `Browser`
- Description: Self-contained action migrated from `browser_close_tab` (old/oomlout_ai_roboclick.py:874). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `browser_close_tab`
- `close_tab`

## Variables

- _none_

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
