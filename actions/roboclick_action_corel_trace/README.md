# roboclick_action_corel_trace

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_trace`
- Name long: `RoboClick Action: Corel Trace`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_trace` (old/oomlout_ai_roboclick.py:1238). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_trace`
- `trace`

## Variables

- `file_name` (string, default ``): Legacy parameter: file_name
- `remove_background_color_from_entire_image` (string, default ``): Legacy parameter: remove_background_color_from_entire_image
- `delay_trace` (string, default ``): Legacy parameter: delay_trace
- `number_of_colors` (string, default ``): Legacy parameter: number_of_colors
- `detail_minus` (string, default ``): Legacy parameter: detail_minus
- `smoothing` (string, default ``): Legacy parameter: smoothing
- `corner_smoothness` (string, default ``): Legacy parameter: corner_smoothness

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
