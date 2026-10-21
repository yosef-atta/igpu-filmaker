# iGPU FilMaker — POC Tasks

**Stage:** POC only  
**Status:** Planned  
**Goal:** Demonstrate an end-to-end editing workflow with a valid final export on Windows and Linux.

## POC-01 — Foundation
- [ ] Set up Python project with `uv`, src layout, Python version policy, Ruff and pytest.
- [ ] Bootstrap PySide6/QML application; confirm launch on Windows and Linux.
- [ ] Define internal boundaries (project model, media, timeline, preview, export, hardware).
- [ ] Add basic CI for Python checks on Windows and Linux.

## POC-02 — Media and playback
- [ ] Probe/import at least two MP4 videos and an audio file; collect stream metadata.
- [ ] Implement play/pause and seeking for a single source in the preview.
- [ ] Detect video acceleration capabilities and log the backend actually used.
- [ ] Handle missing media, decode errors, and software fallback gracefully.

## POC-03 — Timeline and project
- [ ] Define rational/timebase-aware clip timings and non-destructive edit model.
- [ ] Implement video clip trim, split, rearrange, and basic timeline controls.
- [ ] Add an independent audio track with timing and basic level control.
- [ ] Save/load a minimally versioned JSON project.

## POC-04 — Edited preview
- [ ] Preview the timeline result across clip boundaries, not only a source player.
- [ ] Synchronize audio and video; handle seeking and playback state safely.
- [ ] Keep QML UI responsive during decoding and background work.
- [ ] Define shared timeline semantics for preview and export.

## POC-05 — Real export
- [ ] Generate MP4 using H.264 video and AAC audio from the edited timeline.
- [ ] Respect trims, clip order, audio timing, and project frame rate.
- [ ] Show export progress, cancellation, and readable error reporting.
- [ ] Validate resulting file with FFprobe and playback checks.

## POC-06 — Proof and measurements
- [ ] Prepare reproducible test media and documented benchmark scenarios.
- [ ] Test Windows and Linux with Intel/AMD iGPUs represented.
- [ ] Measure memory, CPU, frame drops, seek latency, and export speed.
- [ ] Compare preview against export for timing/audio consistency.
- [ ] Document limitations, risks, results, and the go/no-go decision for the next phase.

## Definition of done

The POC passes the acceptance criteria in [PRD.md](PRD.md), demonstrates an import → edit → preview → export workflow, and records reproducible evidence on both operating systems. No requirement to ship a polished MVP.

## Stage isolation

This file belongs to the **POC** only. At phase transition, preserve these tasks at `docs/tasks/POC.md`; create a separate `docs/tasks/MVP.md` (and later stage files) rather than merging old and new task scopes. `docs/TASKS.md` may then become a small index to the active stage.
