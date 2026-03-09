# roboclick_action_image_quad_swap_for_tile

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_image_quad_swap_for_tile`
- Name long: `RoboClick Action: Image Quad Swap For Tile`
- Category: `Image`
- Description: Self-contained action migrated from `image_quad_swap_for_tile` (old/oomlout_ai_roboclick.py:1649). Action logic is implemented directly in old().
- Returns: Pass-through action result.

## Name Short Options

- `image_quad_swap_for_tile`
- `quad_swap_for_tile`

## Variables

- `file_source` (string, default ``): Legacy parameter: file_source
- `file_destination` (string, default ``): Legacy parameter: file_destination

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
