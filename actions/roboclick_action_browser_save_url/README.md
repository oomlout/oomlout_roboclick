# roboclick_action_browser_save_url

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_browser_save_url`
- Name long: `RoboClick Action: Browser Save Url`
- Category: `Browser`
- Description: Self-contained action migrated from `browser_save_url` (old/oomlout_ai_roboclick.py:891). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `browser_save_url`
- `save_url`

## Variables

- `url` (string, default ``): Legacy parameter: url
- `url_directory` (string, default ``): Legacy parameter: url_directory

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
