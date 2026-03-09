# roboclick_action_ai_query

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_ai_query`
- Name long: `RoboClick Action: AI Query`
- Category: `AI`
- Description: Self-contained action migrated from `ai_query` (old/oomlout_ai_roboclick.py:621). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `ai_query`
- `query`

## Variables

- `text` (string, default ``): Legacy parameter: text
- `delay` (string, default ``): Legacy parameter: delay
- `mode_ai_wait` (string, default ``): Legacy parameter: mode_ai_wait
- `method` (string, default ``): Legacy parameter: method

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
