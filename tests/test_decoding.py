"""Decoder configuration must avoid unsupported hardware acceleration by default."""

from filmaker.hardware.decoding import configure_decoding


def test_default_uses_software_decoder(monkeypatch) -> None:
    monkeypatch.delenv("FILMAKER_DECODING_MODE", raising=False)
    assert configure_decoding() == "software"
    assert __import__("os").environ["QT_FFMPEG_DECODING_HW_DEVICE_TYPES"] == ","


def test_hardware_mode_is_explicit_opt_in(monkeypatch) -> None:
    monkeypatch.setenv("FILMAKER_DECODING_MODE", "hardware")
    monkeypatch.setenv("QT_FFMPEG_DECODING_HW_DEVICE_TYPES", ",")
    assert configure_decoding() == "hardware"
    assert "QT_FFMPEG_DECODING_HW_DEVICE_TYPES" not in __import__("os").environ


def test_unknown_mode_falls_back_to_software(monkeypatch) -> None:
    monkeypatch.setenv("FILMAKER_DECODING_MODE", "invalid")
    assert configure_decoding() == "software"
