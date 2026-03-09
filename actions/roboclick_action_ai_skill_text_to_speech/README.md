# roboclick_action_ai_skill_text_to_speech

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_ai_skill_text_to_speech`
- Name long: `RoboClick Action: AI Skill Text To Speech`
- Category: `AI Skill`
- Description: Self-contained action migrated from `ai_skill_text_to_speech` (old/oomlout_ai_roboclick.py:757). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `ai_skill_text_to_speech`
- `text_to_speech`

## Variables

- `text` (string, default ``): Legacy parameter: text
- `file_destination` (string, default ``): Legacy parameter: file_destination

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
