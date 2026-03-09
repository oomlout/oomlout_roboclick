# roboclick_action_browser_open_url

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_browser_open_url`
- Name long: `RoboClick Action: Browser Open Url`
- Category: `Browser`
- Description: Self-contained action migrated from `browser_open_url` (old/oomlout_ai_roboclick.py:883). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `browser_open_url`
- `open_url`

## Variables

- `url` (string, default ``): Legacy parameter: url

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
