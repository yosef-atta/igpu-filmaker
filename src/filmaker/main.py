"""Native desktop entry point for the foundation proof of concept."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from filmaker.hardware.decoding import configure_decoding
from filmaker.media.controller import MediaController


def qml_entrypoint() -> Path:
    """Return the shipped QML entry point."""
    return Path(__file__).resolve().parent / "ui" / "Main.qml"


def main() -> int:
    """Start Qt Quick; return a nonzero status when the UI cannot load."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    configure_decoding()
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    controller = MediaController(app)
    engine.rootContext().setContextProperty("mediaController", controller)
    engine.load(QUrl.fromLocalFile(str(qml_entrypoint())))
    if not engine.rootObjects():
        return 1
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
