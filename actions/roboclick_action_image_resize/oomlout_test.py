import tempfile
from pathlib import Path

from PIL import Image


def _load_working_module():
    import importlib.util

    working_path = Path(__file__).resolve().parent / "working.py"
    specification = importlib.util.spec_from_file_location("roboclick_image_resize_test", working_path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def test(**kwargs):
    working = _load_working_module()
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_path = Path(temporary_directory)
        source_path = temporary_path / "source.png"
        destination_path = temporary_path / "resized.png"
        Image.new("RGB", (800, 400), "white").save(source_path)

        working.old(
            directory=str(temporary_path),
            action={
                "file_source": source_path.name,
                "file_destination": destination_path.name,
                "maximum_dimension": 300,
            },
        )
        if not destination_path.is_file():
            return False
        with Image.open(destination_path) as resized_image:
            return resized_image.size == (300, 150)


if __name__ == "__main__":
    raise SystemExit(0 if test() else 1)
