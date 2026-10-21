"""Report available FFmpeg acceleration APIs, not active playback acceleration."""

from __future__ import annotations

import shutil
import subprocess


def available_ffmpeg_accelerators(*, executable: str | None = None) -> dict:
    """Return advertised FFmpeg interfaces; device/codec support remains unverified."""
    command = executable or shutil.which("ffmpeg")
    if not command:
        return {"available": False, "interfaces": [], "note": "ffmpeg not found on PATH"}
    try:
        proc = subprocess.run(
            [command, "-hide_banner", "-hwaccels"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "interfaces": [], "note": str(exc)}
    if proc.returncode:
        return {"available": False, "interfaces": [], "note": proc.stderr.strip()}
    interfaces = [
        line.strip()
        for line in proc.stdout.splitlines()
        if line.strip() and not line.startswith("Hardware acceleration")
    ]
    return {
        "available": True,
        "interfaces": interfaces,
        "note": "Compiled FFmpeg interfaces only; active Qt playback backend is not verified.",
    }
