# LeWorldModel: TUM Seminar Presentation

A 20-minute seminar presentation for the *World Models* seminar at TU Munich, covering
**LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels** ([arXiv 2603.19312](https://arxiv.org/abs/2603.19312)).

![LeWM architecture](media/images/lewm_architecture_last_frame.png)

> **Built with code, not slides.** This presentation is an experiment in replacing PowerPoint with
> a fully programmatic toolchain: [Marimo](https://marimo.io/) for the slide layout and
> [Manim](https://www.manim.community/) for animations. See the [Tooling reflection](#tooling-reflection)
> section below for an recap of the tooling.

## Talk structure

**Title and Outline** (not numbered)

**01 · Background and State of the Art** (slides 1 to 5)

| Slide | Topic |
| ----- | ----- |
| 1 | JEPA principle: predict in latent space (Manim animation) |
| 2 | Representation collapse: what is it? |
| 3 | Representation collapse: complete vs. dimensional |
| 4 | State of the Art by anti-collapse strategy (EMA/stop-grad, frozen encoders, VICReg-style) |
| 5 | World model taxonomy by target task (Manim animation) |

**02 · LeWorldModel** (slides 7 to 13)

| Slide | Topic |
| ----- | ----- |
| 7 | Architecture overview: ViT-Tiny encoder + AR predictor (Manim animation) |
| 8 | ViT-Tiny encoder: patch tokenisation to CLS token embedding (Manim animation) |
| 9 | Action conditioning via AdaLN-Zero: scale / shift / gate from action embedding |
| 10 | SIGReg: why isotropic Gaussian is uniquely optimal |
| 11 | SIGReg algorithm: Cramér-Wold sketching + normality test |
| 12 | SIGReg: enforcing the Gaussian target (Manim animation) |
| 13 | Latent planning via MPC + CEM |

*Note: slide 6 is unused — it is an outline recap transition with no page number.*

**03 · Experiments** (slides 14 to 15)

| Slide | Topic |
| ----- | ----- |
| 14 | Evaluation environments: Push-T, OGBench-Cube, Two-Room, Reacher |
| 15 | Violation of Expectation: physics structure in latent space and surprise detection |

**04 · Discussion** (slides 16 to 17)

| Slide | Topic |
| ----- | ----- |
| 16 | Key findings: stable training, SIGReg sufficiency, planning speed, latent structure |
| 17 | Limitations & future work: short horizon, determinism, generalization, CEM scaling |

## Dependencies

Install [uv](https://docs.astral.sh/uv/) if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

In addition to the Python packages managed by `uv`, you need **ffmpeg** installed system-wide:

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg
```

## Running the slides

```bash
uv sync
uv run marimo edit presentation.py
```

Once the notebook is open, switch to slideshow mode via the menu (or press `S`). Key shortcuts during the presentation:

| Key | Action |
| --- | ------ |
| `S` | Toggle presentation / speaker view |
| `F` | Toggle fullscreen |
| `Space` or `Right` | Next slide |
| `Left` | Previous slide |

## Tooling reflection

This project was a deliberate experiment: Build a university seminar presentation **without
PowerPoint or Keynote**, using only code.

### What worked well

**Manim animations** are the clearest win. Coding an animation, especially with a coding agent,
produces results that would be impractical to create manually in a GUI tool. The ViT-Tiny Encoder
and the SigReg regulaizer are explained more precisely and engagingly through motion than
any static diagram could achieve. The agent writes the animation code, you tweak it, the output is
a pixel-perfect, reproducible `.mp4`. For technically rich ML content this is a genuine advantage
over slide tools.

**Version control** is a first-class citizen. Every slide change is a diff, conflicts are
mergeable, and the full history is transparent. No more "final_v3_REAL.pptx".

**Reactive notebook model** (Marimo) means that changing a shared variable like a colour scheme, a
citation list, or a helper function propagates to all slides automatically.

### What took longer than expected

**Programmatic layout is slow.** Placing two elements side by side in PowerPoint is a two-second
drag. In Marimo it requires understanding `mo.hstack` / `mo.vstack`, writing explicit CSS, and
iterating through re-renders. Tables, alignment, font sizing, and spacing all require manual HTML
or CSS. The total time spent on layout and styling was noticeably higher than it would have been in a GUI tool,
and the result is not obviously better-looking.

**Summary:** Use this stack when animations or programmatic content are central to the talk. For
standard lecture slides where layout speed matters more than animation quality, a GUI tool is still
faster.

### Alternative: fully generated website

As an alternative to the Marimo GUI, the presentation could be compiled to a **static website**
— a single self-contained HTML file (or a small bundle) with all slides as pages, the Manim
`.mp4`s embedded, and a minimal JavaScript slide player for keyboard navigation.
