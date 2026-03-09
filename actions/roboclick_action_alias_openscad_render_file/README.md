# roboclick_action_alias_openscad_render_file

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_alias_openscad_render_file`
- Name long: `RoboClick Action: OpenSCAD Render File`
- Category: `Legacy Alias`
- Description: Self-contained action migrated from `openscad_render_file` (old/oomlout_ai_roboclick.py:1778). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `openscad_render_file`
- `render_file`
- `legacy_alias`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `file_destination` (string, default ``): Legacy parameter: file_destination
- `delay` (string, default ``): Legacy parameter: delay

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
