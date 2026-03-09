"""Auto-generated canonical mirror for tooling and static discovery."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
WORKING_FILE = BASE_DIR / "working.py"


def _load_working_module():
    module_name = f"{BASE_DIR.name}_working_{abs(hash(str(WORKING_FILE)))}"
    spec = spec_from_file_location(module_name, str(WORKING_FILE))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {WORKING_FILE}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_working = _load_working_module()
define = getattr(_working, "define")
action = getattr(_working, "action")


def test(**kwargs):
    test_fn = getattr(_working, "test", None)
    if callable(test_fn):
        return test_fn(**kwargs)

    fallback_file = BASE_DIR / "oomlout_test.py"
    spec = spec_from_file_location(f"{BASE_DIR.name}_oomlout_test", str(fallback_file))
    if spec is None or spec.loader is None:
        return False
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    fallback_test = getattr(module, "test", None)
    if not callable(fallback_test):
        return False
    return fallback_test(**kwargs)
