# roboclick_action_ai_new_chat Tests

- Selected: all
- Total: 6
- Passed: 6
- Failed: 0

| Test | Description | Status | Duration (s) | Details |
|---|---|---|---:|---|
| test_1 | Test 1: working.py exposes callable define() and action(). | passed | 0.000 | define=True, action=True |
| test_2 | Test 2: define() returns a dict with basic metadata keys. | passed | 0.000 | missing_keys=[] |
| test_3 | Test 3: optional working.py test() callable is present. | passed | 0.000 | working.test callable=True |
| test_4 | Test 4: define() exposes base_ai_provider with open_ai default. | passed | 0.000 | base_ai_provider={'name': 'base_ai_provider', 'description': 'AI provider to use for this action. Options: open_ai, claude, gemini, open_web_ui.', 'type': 'string', 'default': 'open_ai'} |
| test_5 | Test 5: provider normalization supports kwargs, action config, and aliases. | passed | 0.000 | results=['open_ai', 'claude', 'gemini', 'open_web_ui', 'open_ai'], expected=['open_ai', 'claude', 'gemini', 'open_web_ui', 'open_ai'] |
| test_6 | Test 6: action() routes through new() and dispatches to provider handlers. | passed | 0.000 | captured=[('roboclick_action_ai_new_chat', 'new'), ('roboclick_action_ai_new_chat', 'new'), ('roboclick_action_ai_new_chat', 'new'), ('roboclick_action_ai_new_chat', 'new')], results=['open_ai', 'claude', 'gemini', 'open_web_ui', 'open_ai'] |
