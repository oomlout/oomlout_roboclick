# Google Gemini Roboclick Tests

Live browser automation tests for all Gemini AI roboclick actions.

## Prerequisites

1. **Google Gemini open** in Chrome/Edge at `gemini.google.com`, logged in
2. **Browser in the foreground** - roboclick drives your mouse and keyboard
3. Python environment with roboclick dependencies installed
4. No screen savers / sleep timers that would interrupt the session

---

## Running Tests

Double-click `run_google_tests.bat` (or run from repo root):

    run all 8 tests:         test\google\run_google_tests.bat
    run only test 03:        test\google\run_google_tests.bat 03
    run all except 05 and 07: test\google\run_google_tests.bat skip 05 07

DO NOT touch your mouse or keyboard while a test is running.
The batch pauses 5 seconds before starting so you can get ready.

---

## Test Catalogue

| # | Folder | What it tests | Output file |
|---|--------|--------------|-------------|
| 01 | 01_new_chat | Opens a fresh Gemini chat (new_chat) | - |
| 02 | 02_query | Sends a text query (ai_query) | - |
| 03 | 03_save_text | Sends a query and copies response to a txt file (save_text) | response.txt |
| 04 | 04_set_mode_thinking | Switches Gemini to Thinking mode then queries (set_mode) | thinking_response.txt |
| 05 | 05_add_file | Uploads a PNG then describes it (add_file + ai_query) | image_description.txt |
| 06 | 06_continue_chat | Two-block stream: stores codeword then returns to same chat (continue_chat) | recall_response.txt |
| 07 | 07_save_image_generated | Asks Gemini to draw an image and saves it (save_image_generated) | generated_circle.png |
| 08 | 08_full_stream | Full workflow: thinking mode, two queries, two saves, continue_chat | haiku.txt + haiku_ocean.txt |

---

## Notes

- Test 05 (add_file) needs a test_image.png in its folder - put any PNG there before running.
- file_test entries in each working.yaml tell roboclick what files to check for after the run.
- All YAMLs have enabled: false so they are excluded from the unit test suite and only run via this batch file.
- Each folder is a self-contained stream you can also run individually:

    python -c "import oomlout_roboclick; oomlout_roboclick.run_folder(r'test/google/parts/03_save_text')"

