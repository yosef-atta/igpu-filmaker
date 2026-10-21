"""Media metadata and hardware diagnostics with isolated subprocess dependencies."""

import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from filmaker.hardware.detection import available_ffmpeg_accelerators
from filmaker.media.probe import ProbeError, probe_media


def test_missing_file_fails_before_probe(tmp_path: Path) -> None:
    with pytest.raises(ProbeError, match="not found"):
        probe_media(tmp_path / "missing.mp4", executable="ffprobe")


def test_probe_parses_metadata(tmp_path: Path) -> None:
    media = tmp_path / "sample.mp4"
    media.write_bytes(b"fixture")
    with patch("filmaker.media.probe.subprocess.run") as run:
        run.return_value.returncode = 0
        run.return_value.stdout = (
            '{"format":{"duration":"1.0"},"streams":[{"codec_type":"video","codec_name":"h264"}]}'
        )
        result = probe_media(media, executable="ffprobe")
    assert result["streams"][0]["codec_name"] == "h264"
    assert result["name"] == "sample.mp4"


def test_probe_invalid_json(tmp_path: Path) -> None:
    media = tmp_path / "broken.mp4"
    media.touch()
    with patch("filmaker.media.probe.subprocess.run") as run:
        run.return_value.returncode = 0
        run.return_value.stdout = "invalid"
        with pytest.raises(ProbeError, match="invalid JSON"):
            probe_media(media, executable="ffprobe")


def test_hardware_report_does_not_claim_active_decoder() -> None:
    with patch("filmaker.hardware.detection.subprocess.run") as run:
        run.return_value.returncode = 0
        run.return_value.stdout = "Hardware acceleration methods:\nd3d11va\nvaapi\n"
        report = available_ffmpeg_accelerators(executable="ffmpeg")
    assert report["interfaces"] == ["d3d11va", "vaapi"]
    assert "not verified" in report["note"]


def test_probe_uses_utf8_and_recovers_from_missing_stdout(tmp_path: Path) -> None:
    media = tmp_path / "unicode.mp4"
    media.touch()
    with patch("filmaker.media.probe.subprocess.run") as run:
        run.return_value.returncode = 0
        run.return_value.stdout = None
        with pytest.raises(ProbeError, match="invalid JSON"):
            probe_media(media, executable="ffprobe")
    assert run.call_args.kwargs["encoding"] == "utf-8"
    assert run.call_args.kwargs["errors"] == "replace"


@pytest.mark.skipif(shutil.which("ffprobe") is None, reason="ffprobe not installed on PATH")
def test_probe_real_fixtures() -> None:
    fixtures_dir = Path(__file__).resolve().parent / "fixtures" / "media"
    video1 = fixtures_dir / "video1.mp4"
    video2 = fixtures_dir / "video2.mp4"
    audio1 = fixtures_dir / "audio1.m4a"

    if not video1.is_file():
        pytest.skip("Fixtures not generated")

    v1_meta = probe_media(video1)
    assert any(s["codec_type"] == "video" for s in v1_meta["streams"])
    assert any(s["codec_type"] == "audio" for s in v1_meta["streams"])

    v2_meta = probe_media(video2)
    assert any(s["codec_type"] == "video" for s in v2_meta["streams"])

    a1_meta = probe_media(audio1)
    assert any(s["codec_type"] == "audio" for s in a1_meta["streams"])
