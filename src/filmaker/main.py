"""Native desktop entry point for the foundation proof of concept."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


def qml_entrypoint() -> Path:
    """Return the shipped QML entry point."""
    return Path(__file__).resolve().parent / "ui" / "Main.qml"


def main() -> int:
    """Start Qt Quick; return a nonzero status when the UI cannot load."""
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(QUrl.fromLocalFile(str(qml_entrypoint())))
    if not engine.rootObjects():
        return 1
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
