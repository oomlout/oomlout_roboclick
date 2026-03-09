# roboclick_action_google_doc_new

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_google_doc_new`
- Name long: `RoboClick Action: Google Doc New`
- Category: `Google Doc`
- Description: Self-contained action migrated from `google_doc_new` (old/oomlout_ai_roboclick.py:1447). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `google_doc_new`
- `new`

## Variables

- `template` (string, default ``): Legacy parameter: template
- `title` (string, default ``): Legacy parameter: title
- `folder` (string, default ``): Legacy parameter: folder

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
