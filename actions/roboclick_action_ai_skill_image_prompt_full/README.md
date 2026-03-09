# roboclick_action_ai_skill_image_prompt_full

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_ai_skill_image_prompt_full`
- Name long: `RoboClick Action: AI Skill Image Prompt Full`
- Category: `AI Skill`
- Description: Self-contained action migrated from `ai_skill_image_prompt_full` (old/oomlout_ai_roboclick.py:742). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `ai_skill_image_prompt_full`
- `image_prompt_full`

## Variables

- `image_detail` (string, default ``): Legacy parameter: image_detail
- `file_destination` (string, default ``): Legacy parameter: file_destination

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
