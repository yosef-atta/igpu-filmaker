"""QML-facing media management and diagnostics, isolated from the video renderer."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from PySide6.QtCore import Property, QObject, QUrl, Signal, Slot

from filmaker.hardware.detection import available_ffmpeg_accelerators
from filmaker.media.probe import ProbeError, probe_media

logger = logging.getLogger(__name__)


def _resolve_path(file_url: str) -> Path:
    """Resolve a file URL or path string to a Path object."""
    if file_url.startswith("file://"):
        return Path(QUrl(file_url).toLocalFile())
    path = Path(file_url)
    if path.is_file():
        return path
    url_path = QUrl.fromUserInput(file_url).toLocalFile()
    if url_path:
        return Path(url_path)
    return path


class MediaController(QObject):
    """Small native bridge. Qt Multimedia owns preview decoding and playback."""

    mediaChanged = Signal()
    statusChanged = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._items: list[dict] = []
        self._status = "Import MP4/video/audio to begin"
        self._hardware = available_ffmpeg_accelerators()
        logger.info("FFmpeg accelerator capability report: %s", self._hardware)

    @Property("QVariantList", notify=mediaChanged)
    def items(self) -> list[dict]:
        return self._items

    @Property(str, notify=statusChanged)
    def status(self) -> str:
        return self._status

    @Property(str, constant=True)
    def hardwareReport(self) -> str:
        return json.dumps(self._hardware, ensure_ascii=False)

    def _set_status(self, message: str) -> None:
        self._status = message
        self.statusChanged.emit()
        logger.info("%s", message)

    @Slot(str, result=bool)
    def importFile(self, file_url: str) -> bool:
        path = _resolve_path(file_url)
        if not path.is_file():
            self._set_status(f"Missing file: {path.name or file_url}")
            return False
        if any(item["path"] == str(path.resolve()) for item in self._items):
            self._set_status(f"Already imported: {path.name}")
            return True
        try:
            metadata = probe_media(path)
            tracks = metadata["streams"]
            details = ", ".join(
                str(stream.get("codec_type", "?")) + ":" + str(stream.get("codec_name", "?"))
                for stream in tracks
            )
            self._set_status(f"Imported {path.name} — {details or 'no streams'}")
        except ProbeError as exc:
            # Qt Multimedia can still play supported files without the FFmpeg CLI.
            details = "Metadata unavailable (ffprobe required)"
            self._set_status(f"Imported {path.name}; {exc}")
        item = {
            "path": str(path.resolve()),
            "url": QUrl.fromLocalFile(str(path.resolve())).toString(),
            "name": path.name,
            "details": details,
        }
        self._items.append(item)
        self.mediaChanged.emit()
        return True

    @Slot(str)
    def reportPlaybackError(self, message: str) -> None:
        self._set_status(f"Playback error: {message}")

    @Slot(str)
    def reportPlaybackBackend(self, description: str) -> None:
        self._set_status(description)
