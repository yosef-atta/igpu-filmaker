"""Optional ffprobe-based metadata inspection without loading video frames in Python."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


class ProbeError(RuntimeError):
    """A media file could not be inspected."""


def probe_media(path: str | Path, *, executable: str | None = None) -> dict:
    """Inspect a local media file; require ffprobe available on PATH or explicitly provided."""
    media = Path(path).expanduser().resolve()
    if not media.is_file():
        raise ProbeError(f"Media file not found: {media}")
    command = executable or shutil.which("ffprobe")
    if not command:
        raise ProbeError("ffprobe not found on PATH; install FFmpeg for stream metadata")
    try:
        process = subprocess.run(
            [command, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(media)],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ProbeError(f"Could not run ffprobe: {exc}") from exc
    if process.returncode:
        raise ProbeError((process.stderr or "").strip() or "ffprobe failed")
    try:
        result = json.loads(process.stdout)
    except (json.JSONDecodeError, TypeError, UnicodeError) as exc:
        raise ProbeError("ffprobe returned invalid JSON") from exc
    if not isinstance(result, dict) or not isinstance(result.get("streams"), list):
        raise ProbeError("ffprobe returned no usable stream metadata")
    return {
        "path": str(media),
        "name": media.name,
        "format": result.get("format", {}),
        "streams": result["streams"],
    }
