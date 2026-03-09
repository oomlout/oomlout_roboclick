# roboclick_action_corel_add_text

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_add_text`
- Name long: `RoboClick Action: Corel Add Text`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_add_text` (old/oomlout_ai_roboclick.py:951). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_add_text`
- `add_text`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `text` (string, default ``): Legacy parameter: text
- `x` (string, default ``): Legacy parameter: x
- `y` (string, default ``): Legacy parameter: y
- `font` (string, default ``): Legacy parameter: font
- `font_size` (string, default ``): Legacy parameter: font_size
- `bold` (string, default ``): Legacy parameter: bold
- `italic` (string, default ``): Legacy parameter: italic

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
