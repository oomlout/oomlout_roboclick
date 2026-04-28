# oomlout_roboclick

`oomlout_roboclick` is a modular action runner for desktop-style automation workflows. It loads actions from the [`actions/`](actions) folder, reads a `working.yaml` or `working.oomp` file, and executes numbered workflow modes such as AI, CorelDRAW, browser, file, image, conversion, Google Docs, and OpenSCAD steps.

The current codebase is a newer modular runner around older GUI automation patterns. In practice, many workflows are Windows-focused and depend on visible desktop applications, mouse/keyboard control, and file-based handoff between steps.

## What It Does

- Discovers action modules from [`actions/`](actions)
- Runs workflows from `working.yaml` or `working.oomp`
- Supports multi-stage mode blocks like `oomlout_ai_roboclick_1` and `oomlout_corel_roboclick_1`
- Generates action documentation as JSON and HTML
- Includes an action-audit test runner plus example/integration tests

## Repo Layout

- [`oomlout_roboclick.py`](oomlout_roboclick.py): main modular runner, action discovery, CLI, docs export
- [`robo_roboclick.py`](robo_roboclick.py): lower-level GUI/file helpers used by some actions
- [`actions/`](actions): one folder per action, usually with `working.py` and `oomlout_test.py`
- [`tests/`](tests): test definitions used by [`run_tests.py`](run_tests.py)
- [`test_data/`](test_data): example workflow inputs
- [`templates/documentation_template.html`](templates/documentation_template.html): HTML template for generated docs
- [`documentation_data.json`](documentation_data.json): generated action documentation data
- [`documentation.html`](documentation.html): generated action documentation site
- [`actions.md`](actions.md): migration/reference inventory for the action set
- [`old/`](old): older monolithic scripts kept for reference/migration history

## Setup

Python 3 is required. A lightweight [`requirements.txt`](requirements.txt) is included for the Python packages used by the current code.

External tools/apps referenced by the code:

- Google Chrome
- CorelDRAW
- Inkscape
- OpenSCAD
- SingleFile browser extension

Suggested install:

```bash
pip install -r requirements.txt
```

Notes:

- Many actions automate live desktop applications, so headless or CI-only environments will be limited.
- Several action modules still import `robo`, while this repo currently ships [`robo_roboclick.py`](robo_roboclick.py) at the top level and [`old/robo_roboclick.py`](old/robo_roboclick.py) in `old/`. If you hit import errors, that compatibility path likely needs cleanup.
- Some action folders still show migration mismatches between folder names and metadata names; the runner tolerates at least some of these cases.

## Docs Generation

Regenerate action documentation:

```bat
action_documentation_regenerate.bat
```

Or call the CLI directly with the same flags shown above.

Generated outputs:

- [`documentation_data.json`](documentation_data.json)
- [`documentation.html`](documentation.html)
