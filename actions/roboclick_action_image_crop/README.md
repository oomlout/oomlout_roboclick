# roboclick_action_image_crop

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_image_crop`
- Name long: `RoboClick Action: Image Crop`
- Category: `Image`
- Description: Self-contained action migrated from `image_crop` (old/oomlout_ai_roboclick.py:1512). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `image_crop`
- `crop`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `file_destination` (string, default ``): Legacy parameter: file_destination
- `crop` (string, default ``): Legacy parameter: crop

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
