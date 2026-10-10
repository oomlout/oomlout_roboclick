# test_10

- Description: Test 10: disabling sanitize_text preserves whitespace at the beginning and end.
- Status: passed
- Duration (s): 0.0
- Details: output=' \n\t Alpha\n\t '

## Captured Output

```text
[roboclick] [action] roboclick_action_ai_save_text file_name=not_trimmed.txt sanitize_text=false sanitize_double_linebreaks=false
Text saved to C:\Users\aaron\AppData\Local\Temp\tmpbxbuuz_d\not_trimmed.txt
[roboclick] [action_finished] roboclick_action_ai_save_text ok
```
