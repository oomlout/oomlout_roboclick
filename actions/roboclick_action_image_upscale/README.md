# roboclick_action_image_upscale

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_image_upscale`
- Name long: `RoboClick Action: Image Upscale`
- Category: `Image`
- Description: Self-contained action migrated from `image_upscale` (old/oomlout_ai_roboclick.py:1698). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `image_upscale`
- `upscale`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `file_destination` (string, default ``): Legacy parameter: file_destination
- `scale` (string, default ``): Legacy parameter: scale
- `crop` (string, default ``): Legacy parameter: crop

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
