# LeWorldModel — TUM Seminar Presentation

A 20-minute seminar presentation for the *World Models* seminar at TU Munich, covering:

> **LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels** (arXiv 2603.19312)

The talk is structured into four parts: motivation & related work, architecture (ViT encoder, AdaLN predictor, SIGReg), experimental results, and critical discussion.

## Tooling

- **Slides** — [Marimo](https://marimo.io/) reactive notebooks
- **Animations** — [Manim Community](https://www.manim.community/)

## Dependencies

In addition to the Python packages managed by `uv`, you need **ffmpeg** installed system-wide:

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg
```

Manim uses ffmpeg to stitch animation frames into video. The slide deck renders animations on first load and caches them under `assets/` — no pre-rendered videos need to be committed.

## Running the slides

```bash
uv sync
uv run marimo edit presentation.py
```
