"""Test MediaController logic and error handling."""

from pathlib import Path
from unittest.mock import patch

from PySide6.QtCore import QCoreApplication

from filmaker.media.controller import MediaController


def test_controller_import_missing_file(tmp_path: Path) -> None:
    app = QCoreApplication.instance() or QCoreApplication([])
    controller = MediaController()
    success = controller.importFile(str(tmp_path / "nonexistent.mp4"))
    assert not success
    assert "Missing file" in controller.status
    del app


def test_controller_import_valid_file_and_duplicate(tmp_path: Path) -> None:
    app = QCoreApplication.instance() or QCoreApplication([])
    sample = tmp_path / "test.mp4"
    sample.write_bytes(b"dummy content")

    controller = MediaController()

    with patch("filmaker.media.controller.probe_media") as mock_probe:
        mock_probe.return_value = {
            "path": str(sample),
            "name": sample.name,
            "format": {"duration": "2.0"},
            "streams": [{"codec_type": "video", "codec_name": "h264"}],
        }
        success = controller.importFile(str(sample))
        assert success
        assert len(controller.items) == 1
        assert controller.items[0]["name"] == "test.mp4"
        assert "Imported test.mp4" in controller.status

        # Try duplicate import
        second = controller.importFile(str(sample))
        assert second
        assert len(controller.items) == 1
        assert "Already imported" in controller.status

    del app


def test_controller_playback_error_and_backend_reporting() -> None:
    app = QCoreApplication.instance() or QCoreApplication([])
    controller = MediaController()

    controller.reportPlaybackError("Decoder failure")
    assert "Playback error: Decoder failure" in controller.status

    controller.reportPlaybackBackend("Using software backend")
    assert controller.status == "Using software backend"

    del app
