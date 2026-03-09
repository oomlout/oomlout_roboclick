# roboclick_action_corel_trace_full

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_corel_trace_full`
- Name long: `RoboClick Action: Corel Trace Full`
- Category: `CorelDRAW`
- Description: Self-contained action migrated from `corel_trace_full` (old/oomlout_ai_roboclick.py:1273). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `corel_trace_full`
- `trace_full`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `file_source_trace` (string, default ``): Legacy parameter: file_source_trace
- `file_destination` (string, default ``): Legacy parameter: file_destination
- `delay_trace` (string, default ``): Legacy parameter: delay_trace
- `delay_png` (string, default ``): Legacy parameter: delay_png
- `max_dimension` (string, default ``): Legacy parameter: max_dimension
- `detail_minus` (string, default ``): Legacy parameter: detail_minus
- `x` (string, default ``): Legacy parameter: x
- `y` (string, default ``): Legacy parameter: y
- `number_of_colors` (string, default ``): Legacy parameter: number_of_colors
- `remove_background_color_from_entire_image` (string, default ``): Legacy parameter: remove_background_color_from_entire_image
- `smoothing` (string, default ``): Legacy parameter: smoothing
- `corner_smoothness` (string, default ``): Legacy parameter: corner_smoothness

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
