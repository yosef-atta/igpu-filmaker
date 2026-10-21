"""Configure Qt's FFmpeg decoding backend before the media player is created."""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

# Qt documents "," as an empty device list, disabling HW decoding attempts.
QT_DECODING_TYPES = "QT_FFMPEG_DECODING_HW_DEVICE_TYPES"
DECODING_MODE = "FILMAKER_DECODING_MODE"


def configure_decoding() -> str:
    """Use safe software decoding for the POC unless explicitly opted into hardware."""
    mode = os.environ.get(DECODING_MODE, "software").strip().lower()
    if mode not in {"software", "hardware"}:
        logger.warning("Unknown %s=%r; defaulting to software", DECODING_MODE, mode)
        mode = "software"
    if mode == "software":
        os.environ[QT_DECODING_TYPES] = ","
        logger.info("Preview decode: software (safe compatibility mode)")
    else:
        os.environ.pop(QT_DECODING_TYPES, None)
        logger.info("Preview decode: Qt automatic hardware selection (experimental)")
    return mode
