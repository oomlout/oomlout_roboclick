# roboclick_action_convert_svg_to_png

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_convert_svg_to_png`
- Name long: `RoboClick Action: Convert Svg To Png`
- Category: `Conversion`
- Description: Self-contained action migrated from `convert_svg_to_png` (old/oomlout_ai_roboclick.py:929). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `convert_svg_to_png`
- `svg_to_png`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `file_destination` (string, default ``): Legacy parameter: file_destination

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
