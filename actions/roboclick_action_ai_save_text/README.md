# roboclick_action_ai_save_text

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_ai_save_text`
- Name long: `RoboClick Action: AI Save Text`
- Category: `AI`
- Description: Self-contained action migrated from `ai_save_text` (old/oomlout_ai_roboclick.py:680). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `ai_save_text`
- `save_text`

## Variables

- `file_name_full` (string, default ``): Legacy parameter: file_name_full
- `file_name_clip` (string, default ``): Legacy parameter: file_name_clip
- `clip` (string, default ``): Legacy parameter: clip

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
