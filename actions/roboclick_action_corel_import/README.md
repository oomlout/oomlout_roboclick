# roboclick_action_corel_import

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_import`
- Name long: `RoboClick Action: Corel Import`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_import` (old/oomlout_ai_roboclick.py:1075). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_import`
- `import`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `x` (string, default ``): Legacy parameter: x
- `y` (string, default ``): Legacy parameter: y
- `width` (string, default ``): Legacy parameter: width
- `height` (string, default ``): Legacy parameter: height
- `max_dimension` (string, default ``): Legacy parameter: max_dimension
- `angle` (string, default ``): Legacy parameter: angle
- `special, 'no double click' - to deal with non square objects` (string, default ``): Legacy parameter: special, 'no double click' - to deal with non square objects

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
