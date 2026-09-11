import threading
import time
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import yaml

import oomlout_roboclick


class ThreadedRecursiveRunnerTests(unittest.TestCase):
    def test_roboclick_metadata_name_does_not_make_file_action_look_like_ui(self):
        discovered = {
            "run_python": mock.Mock(
                metadata={
                    "name": "roboclick_action_run_python",
                    "name_long": "roboclick_action_run_python",
                    "category": "File",
                }
            )
        }

        self.assertTrue(
            oomlout_roboclick._action_is_thread_safe(
                {"command": "run_python"},
                discovered,
                allow_subprocess=True,
            )
        )
        self.assertFalse(
            oomlout_roboclick._action_is_thread_safe(
                {"command": "run_python"},
                discovered,
            )
        )
        self.assertFalse(
            oomlout_roboclick._action_is_thread_safe(
                {"command": "corel_open"},
                discovered,
                allow_subprocess=True,
            )
        )

    def test_requested_mode_only_returns_real_action_blocks(self):
        workings = {
            "oomlout_ai_roboclick_1": {"actions": [{"command": "run_python"}]},
            "oomlout_ai_roboclick_3": {"actions": [{"command": "image_resize"}]},
            "oomlout_corel_roboclick_1": {"actions": [{"command": "corel_open"}]},
        }

        self.assertEqual(
            oomlout_roboclick._resolve_mode_names(workings, "ai"),
            ["oomlout_ai_roboclick_1", "oomlout_ai_roboclick_3"],
        )

    def test_recursive_runner_remains_linear_by_default(self):
        with (
            mock.patch.object(oomlout_roboclick, "run_folder_recursive_linear") as linear,
            mock.patch.object(oomlout_roboclick, "run_folder_recursive_threaded") as threaded,
        ):
            oomlout_roboclick.run_folder_recursive(directory="unused")

        linear.assert_called_once()
        threaded.assert_not_called()

    def test_folder_modes_keep_order_across_two_workers(self):
        calls = []
        active = 0
        maximum_active = 0
        lock = threading.Lock()

        def fake_run_single(**kwargs):
            nonlocal active, maximum_active
            with lock:
                active += 1
                maximum_active = max(maximum_active, active)
            time.sleep(0.03)
            with lock:
                calls.append((Path(kwargs["folder"]).name, kwargs["mode"]))
                active -= 1
            return ""

        workings = {
            "oomlout_ai_roboclick_1": {"actions": [{"command": "run_python"}]},
            "oomlout_ai_roboclick_2": {"actions": [{"command": "image_resize"}]},
        }

        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for folder_name in ("alpha", "beta"):
                folder = root / folder_name
                folder.mkdir()
                (folder / "working.yaml").write_text(
                    yaml.safe_dump(workings),
                    encoding="utf-8",
                )

            with (
                mock.patch.object(oomlout_roboclick, "build_action_lookup", return_value={}),
                mock.patch.object(oomlout_roboclick, "run_single", side_effect=fake_run_single),
            ):
                oomlout_roboclick.run_folder_recursive_threaded(
                    directory=str(root),
                    mode="ai",
                    threaded_workers=2,
                    threaded_subprocess_actions=True,
                )

        self.assertEqual(maximum_active, 2)
        for folder_name in ("alpha", "beta"):
            folder_modes = [mode for folder, mode in calls if folder == folder_name]
            self.assertEqual(
                folder_modes,
                ["oomlout_ai_roboclick_1", "oomlout_ai_roboclick_2"],
            )


if __name__ == "__main__":
    unittest.main()
