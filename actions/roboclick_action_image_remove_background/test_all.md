# roboclick_action_image_remove_background Tests

- Selected: all
- Total: 6
- Passed: 6
- Failed: 0

| Test | Description | Status | Duration (s) | Details |
|---|---|---|---:|---|
| test_1 | Test 1: working.py exposes callable define() and action(). | passed | 0.265 | define=True, action=True |
| test_2 | Test 2: define() returns a dict with basic metadata keys. | passed | 0.000 | missing_keys=[] |
| test_3 | Test 3: optional working.py test() callable executes successfully. | passed | 0.000 | working_test_result=True |
| test_4 | Test 4: background_remove_all is exposed and defaults to true. | passed | 0.000 | setting={'name': 'background_remove_all', 'description': 'Remove matching key-coloured pixels everywhere in the image. Set false to remove only the border-connected screen.', 'type': 'boolean', 'default': True} |
| test_5 | Test 5: default mode removes key colour inside an enclosed subject gap. | passed | 0.000 | enclosed_alpha=0, subject_alpha=255 |
| test_6 | Test 6: background_remove_all=false preserves enclosed key-coloured details. | passed | 0.000 | enclosed_alpha=255, border_alpha=0 |
