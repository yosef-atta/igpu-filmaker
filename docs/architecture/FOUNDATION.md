# Foundation Architecture (POC-01)

The initial architecture is a Python 3.12 package with Qt Quick (QML/JavaScript) for presentation. No custom C/C++/Rust source is required.

## Boundaries

- `ui/`: QML desktop presentation; no direct media decoding logic.
- `core/`: application orchestration and commands.
- `project/`: versioned project persistence and media reference model.
- `media/`: probe, import, decode and source lifecycle.
- `timeline/`: edit decisions and precise clip timing.
- `preview/`: interpreted timeline playback and viewer orchestration.
- `export/`: output planning and FFmpeg execution.
- `hardware/`: availability, capability reports, and safe fallback.

Dependencies should flow from application orchestration into independent domain modules. The timeline/project model must not depend on QML. Media decoding, compositing, hardware acceleration, and encoding are **not implemented in POC-01**.

## Local setup

Prerequisites: `uv` and a desktop environment (Windows or Linux with a graphical session).

```powershell
uv python install 3.12
uv sync --group dev
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run filmaker
```

The QML foundation shell opening successfully on both platforms is a manual acceptance check; CI smoke tests verify packaging and imports but do not establish GPU rendering or GUI compatibility. `uv.lock` should be generated and committed after dependency resolution for reproducible subsequent stages.
