# roboclick_action_ai_skill_validate_json

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_ai_skill_validate_json`
- Name long: `RoboClick Action: AI Skill Validate Json`
- Category: `AI Skill`
- Description: Self-contained action migrated from `ai_skill_validate_json` (old/oomlout_ai_roboclick.py:775). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `ai_skill_validate_json`
- `validate_json`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `file_destination` (string, default ``): Legacy parameter: file_destination

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
