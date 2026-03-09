# roboclick_action_base_time_delay

- Runtime entrypoint: `working.py`
- Canonical interface: `define()` + `action()`
- Canonical test runner: `oomlout_test.py`
- Config schema: `config.yaml`

## Metadata

- Name: `roboclick_action_base_time_delay`
- Name long: `roboclick_action_base_time_delay`
- Category: `Other`
- Description: Pause execution for N seconds with optional skip mechanisms.
- Returns: empty string normally; may early-return on skip

## Name Short Options

- `delay`
- `wait`
- `robo_delay`
- `sleep`

## Variables

- `delay` (number, default `1`): Number of seconds to delay (default: 1)
- `rand` (number, default `0`): Additional random seconds to add to delay (default: 0)
- `message` (string, default ``): Optional message to print before delaying
- `mode_skip_key` (boolean, default `True`): Whether pressing 's' should skip the delay (default: true)
- `mode_scroll_lock_skip` (boolean, default `True`): Whether toggling Scroll Lock should skip the delay (default: true, Windows only)

## Return Semantics

- Continue: `""` or `None`
- Stop run: `exit` or `exit_no_tab`
- Manual merge update: return a `dict`
