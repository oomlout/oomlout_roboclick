# roboclick_action_ai_save_text Tests

- Selected: all
- Total: 11
- Passed: 11
- Failed: 0

| Test | Description | Status | Duration (s) | Details |
|---|---|---|---:|---|
| test_1 | Test 1: working.py exposes callable define() and action(). | passed | 0.203 | define=True, action=True |
| test_2 | Test 2: define() returns a dict with basic metadata keys. | passed | 0.000 | missing_keys=[] |
| test_3 | Test 3: optional working.py test() callable executes successfully. | passed | 0.016 | working_test_result=True |
| test_4 | Test 4: tag_open/tag_close extracts to file_name before legacy clip parsing. | passed | 0.000 | output='[{"moment": "opening"}]' |
| test_5 | Test 5: missing tag_open/tag_close markers fall back to the legacy clip marker. | passed | 0.000 | output='legacy value' |
| test_6 | Test 6: sanitize_text and sanitize_double_linebreaks default to enabled. | passed | 0.000 | output='Alpha-beta "quoted" and \'single\' smile\nGamma\n\nDelta' |
| test_7 | Test 7: sanitize_text and sanitize_double_linebreaks can be disabled. | passed | 0.000 | output='Alpha—beta smile🙂\n\nGamma' |
| test_8 | Test 8: top-level kwargs can override sanitize options. | passed | 0.000 | output='Alpha—beta smile🙂\n\nGamma' |
| test_9 | Test 9: sanitize_text trims whitespace at the beginning and end by default. | passed | 0.016 | output='Alpha-beta' |
| test_10 | Test 10: disabling sanitize_text preserves whitespace at the beginning and end. | passed | 0.000 | output=' \n\t Alpha\n\t ' |
| test_11 | Test 11: distinct marker pairs extract the final complete pair. | passed | 0.000 | output='The final generated story belongs here.' |
