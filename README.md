# LeWorldModel — TUM Seminar Presentation

A 20-minute seminar presentation for the *World Models* seminar at TU Munich, covering:

> **LeWorldModel: Learning a World Model with Latent Imagination for Model-Based Reinforcement Learning** (arXiv 2603.19312)

The talk is structured into four parts: motivation & related work, architecture (ViT encoder, AdaLN predictor, SIGReg), experimental results, and critical discussion.

## Tooling

- **Slides** — [Marimo](https://marimo.io/) reactive notebooks (`presentation.py`)
- **Animations** — [Manim Community](https://www.manim.community/) (`animations/`)

## Running the slides

```bash
uv sync
uv run marimo edit presentation.py
```
