# iGPU FilMaker — Product Requirements Document

**Status:** Planning / POC  
**Platforms:** Windows and Linux  
**Target hardware:** Diverse Intel and AMD integrated GPUs  
**Current stage:** Proof of Concept; not an MVP

## 1. Overview

iGPU FilMaker is a native, non-destructive video editor with a familiar, Premiere-inspired workflow. Its purpose is to make practical, capable editing accessible on computers using integrated graphics, while remaining extensible for future features beyond those in existing editors.

The product should prioritize responsive interaction, predictable resource use, and dependable exports over maximizing feature count. A dedicated GPU must not be required.

## 2. Users and problem

**Primary users:** Video creators and editors on Windows or Linux laptops/desktops with Intel or AMD iGPUs, including systems with limited shared memory.

**Problem:** Full-featured editors can feel resource-heavy on iGPU systems; lightweight editors may compromise editing workflows or extensibility.

**Proposed value:** A familiar multi-track editing experience optimized around the resources a machine actually has, with adaptable preview quality, caching, proxy workflows, and hardware acceleration where available.

## 3. Product principles

- **iGPU-first:** Treat shared memory, memory bandwidth, thermal limits, and GPU driver differences as first-class constraints.
- **Native and cross-platform:** Windows and Linux are supported from the start; test both continuously.
- **Non-destructive editing:** Original media remains unchanged; edits are expressed as project data.
- **Extensible by design:** Keep UI, timeline model, media processing, rendering, and export logically separate.
- **Performance is measurable:** Profile frame drops, UI responsiveness, RAM/CPU usage, seeking, and export correctness.
- **No feature parity requirement:** Premiere is a workflow reference, not a feature checklist or visual asset source.

## 4. Proposed technology and constraints

- Application logic and editing model: **Python**.
- Desktop interface: **PySide6 / Qt Quick (QML + JavaScript)**.
- Media probing, decoding, encoding, and export: **FFmpeg**, accessed through supported Python APIs and/or separate processes; test Qt Multimedia and PyAV where appropriate.
- Rendering: initially evaluate Qt-supported rendering paths. Choose the compositing architecture only after real measurements; Qt Multimedia playback is not assumed to provide a complete multi-track editor.
- Tooling: **uv** for Python; **pnpm** only if standalone JS/TS tooling is introduced. QML JavaScript itself does not require pnpm.
- Use existing native dependencies as libraries/tools; application code will be authored in Python and JS/TS, not in C/C++/Rust.
- Examine Qt/FFmpeg licensing and codec distribution obligations before distributing releases.

Architecture selections are **provisional** until validated by the POC. Future phases may revise them.

## 5. Intended product capabilities (post-POC)

- Media import, organization, metadata, and project relinking.
- Multi-track video/audio timeline: trim, split, move, ripple operations, snapping, undo/redo.
- Reliable synchronized playback, frame seeking, thumbnails, waveforms, and adjustable preview resolution.
- Essential transitions, transforms, basic color, titles/subtitles, volume adjustments, and keyframes.
- Configurable exports; hardware acceleration when available; software fallback.
- Autosave, project recovery, customizable workspaces and keyboard shortcuts.
- Future advanced features and custom editing workflows without restricting the architecture to Premiere's design.

This list represents product direction, **not POC scope**.

## 6. POC objective and boundaries

**Proof statement:** On both Windows and Linux, a user can import at least two media clips, apply timeline edits, preview the edited result, include an additional audio track, and export a valid playable MP4 that reflects those edits.

**In POC scope:**
- Simple native UI, media probing/import, a basic editable single-video-track timeline with an additional audio track.
- Trim, split, rearrange, play/pause, seeking, preview, MP4 export (H.264 + AAC).
- Save/load a minimal versioned project format.
- GPU/backend capability reporting; transparent hardware-accelerated or software fallback.
- Reproducible performance and correctness tests on Windows and Linux.

**Out of POC scope:** Premiere-quality UI polish, broad codec support, full multi-track effects compositing, plugins, advanced keyframes, cloud collaboration, final performance optimizations, installer/release packaging, and any claim of production readiness.

## 7. POC acceptance criteria

1. The same test project opens on Windows and Linux and references source media without modifying originals.
2. Two clips can be imported, trimmed/split, arranged and played through a simple timeline; separate audio can be added.
3. Preview and exported output honor the same documented edit timings, including clip boundaries and audio synchronization, within an explicitly measured frame/sample tolerance.
4. MP4 H.264/AAC export finishes and the result is validated by probing and playback (including expected duration, video and audio streams).
5. The UI stays responsive during preview, seeking, and export.
6. Logs identify decode/encode backends actually used, fallback behavior, and CPU/RAM/frame-drop/seek/export metrics when available.
7. Validation runs on at least one Intel iGPU and one AMD iGPU across Windows and Linux collectively, with operating-system coverage on both platforms. Record hardware, drivers, media fixtures, and known limitations.

**Reference benchmark:** 1080p30 H.264 single-stream playback, plus seek tests, on representative iGPU devices. Performance thresholds will be set from baseline measurements rather than promised in advance.

## 8. Risks and open decisions

- Python and QML cannot perform high-throughput per-pixel processing efficiently on their own; delegate heavy work to optimized native dependencies.
- Decode-to-preview interop, GPU memory copies, and video/audio synchronization require measurement.
- Driver and codec availability differs by OS and device; implement accurate detection and graceful fallback.
- Export correctness and live preview performance are separate engineering gates.
- Project schema, rendering/compositing approach, and distribution/license model remain open until evidence is collected.

## 9. Delivery approach and Git workflow

First complete the POC and document results; decide the next phase (potentially an MVP) only after reviewing evidence.

- Long-lived branches: `main` (stable milestones) and `develop` (integration).
- Work branches: `feature/<topic>`, `fix/<topic>`, `docs/<topic>`, created from `develop`; PRs merge back into `develop`.
- Release preparation: `release/<version>` from `develop`, merged through reviewed PRs to `main`, then synchronized back to `develop`.
- Emergency fixes: `hotfix/<topic>` from `main`, merged to both `main` and `develop`.
- Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `perf:`, `chore:`, etc.
- Protect `main` and `develop` with PRs, review requirements, and CI checks once workflows exist. Do not configure required checks before the corresponding checks run successfully.
- Keep tasks for each stage separate. `docs/TASKS.md` tracks the current POC; archive it as `docs/tasks/POC.md` before replacing it for a later stage (e.g., `docs/tasks/MVP.md`).
