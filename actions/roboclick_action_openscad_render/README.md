# roboclick_action_openscad_render

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_openscad_render`
- Name long: `RoboClick Action: OpenSCAD Render`
- Category: `OpenSCAD`
- Description: Self-contained action migrated from `openscad_render` (old/oomlout_ai_roboclick.py:1877). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `openscad_render`
- `render`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `file_destination` (string, default ``): Legacy parameter: file_destination
- `render_type` (string, default ``): Legacy parameter: render_type
- `delay` (string, default ``): Legacy parameter: delay

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
