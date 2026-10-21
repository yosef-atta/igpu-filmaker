"""Foundation tests that do not need a graphics display."""

from pathlib import Path

from filmaker import __version__
from filmaker.main import qml_entrypoint


def test_version() -> None:
    assert __version__ == "0.0.0"


def test_qml_entrypoint_exists() -> None:
    entrypoint = qml_entrypoint()
    assert entrypoint.is_file()
    assert entrypoint.name == "Main.qml"


def test_module_boundaries_are_importable() -> None:
    import filmaker.core
    import filmaker.export
    import filmaker.hardware
    import filmaker.media
    import filmaker.preview
    import filmaker.project
    import filmaker.timeline

    assert Path(filmaker.timeline.__file__).is_file()
