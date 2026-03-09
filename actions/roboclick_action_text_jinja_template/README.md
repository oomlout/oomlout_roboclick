# roboclick_action_text_jinja_template

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_text_jinja_template`
- Name long: `RoboClick Action: Text Jinja Template`
- Category: `Text`
- Description: Self-contained action migrated from `text_jinja_template` (old/oomlout_ai_roboclick.py:1825). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `text_jinja_template`
- `jinja_template`

## Variables

- `file_template` (string, default ``): Legacy parameter: file_template
- `file_source` (string, default ``): Legacy parameter: file_source
- `file_output` (string, default ``): Legacy parameter: file_output
- `search_and_replace` (string, default ``): Legacy parameter: search_and_replace
- `convert_to_pdf` (string, default ``): Legacy parameter: convert_to_pdf
- `convert_to_png` (string, default ``): Legacy parameter: convert_to_png
- `dict_data` (string, default ``): Legacy parameter: dict_data

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
