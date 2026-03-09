# roboclick_action_google_doc_add_text

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_google_doc_add_text`
- Name long: `RoboClick Action: Google Doc Add Text`
- Category: `Google Doc`
- Description: Self-contained action migrated from `google_doc_add_text` (old/oomlout_ai_roboclick.py:1482). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `google_doc_add_text`
- `add_text`

## Variables

- `url` (string, default ``): Legacy parameter: url
- `text` (string, default ``): Legacy parameter: text
- `position` (string, default ``): Legacy parameter: position

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
