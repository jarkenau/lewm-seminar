# CLAUDE.md — LeWorldModel Seminar Project

## Intent

This project prepares a **20-minute university seminar presentation** (+ 10-minute Q&A) for the
*World Models* seminar at **TU Munich (TUM)**. The presentation covers the paper:

> **LeWorldModel: Learning a World Model with Latent Imagination for Model-Based Reinforcement
> Learning** (arXiv 2603.19312)

The seminar is self-contained and structured into four parts:
1. **Introduction & State of the Art** — motivation via LeCun 2022, the JEPA paradigm, and key
   related work (Ha & Schmidhuber, LeJEPA, V-JEPA 2, DINO-WM, PLDM, DreamerV3/V4)
2. **Main Contributions** — LeWM's architecture (ViT-Tiny encoder, action-conditioned transformer
   predictor with AdaLN, SIGReg anti-collapse regularizer, latent planning via MPC + CEM)
3. **Experimental Results** — benchmark comparisons and ablations
4. **Discussion** — author summary, personal critical assessment, and future work directions

---

## Tooling

### Slides — [Marimo](https://marimo.io/)

Slides are built as **reactive Marimo notebooks** (`.py` files). Marimo is a next-generation Python
notebook that is git-friendly (pure Python source), reactive (cells re-execute on state change),
and supports rich interactive widgets — making it well-suited for a technical ML presentation.

- Each slide is a Marimo cell or a group of cells.
- Use `mo.md(...)` for text/math, `mo.image(...)` for figures, and Marimo's layout primitives
  (`mo.hstack`, `mo.vstack`, `mo.tabs`, etc.) for slide composition.
- LaTeX math is rendered via `mo.md(r"$$...$$")`.
- Keep slides in a single file `presentation.py` unless complexity warrants splitting.

### Animations — [Manim Community](https://www.manim.community/)

Key architectural and conceptual aspects are visualized as **programmatic animations** rendered
with Manim (Community Edition). Animations are pre-rendered to video (`.mp4`) and embedded into
the Marimo slides.

- Animation source files live in `animations/` as individual Python scripts, one per concept.
- Render with: `.venv/bin/manim -pql animations/<scene>.py <SceneName>` (low quality for
  iteration, `-pqh` for final render). Manim is installed in the project venv, not global PATH.
- Output lands in `media/videos/` by default; copy final renders to `assets/` for embedding.
- Each animation file should contain exactly one `Scene` subclass with a descriptive name.

**Planned animation targets** (concepts that benefit from motion):
- JEPA training loop: encoder → predictor → latent target (vs. pixel reconstruction)
- AdaLN action conditioning: how action embeddings modulate transformer features
- SIGReg regularizer: intuition for preventing representational collapse
- MPC + CEM planning loop in latent space
- Comparison: generative (pixel-space) world model vs. JEPA (latent-space) world model

---

## Project Structure

```
.
├── CLAUDE.md                  # This file
├── presentation.py            # Marimo slide deck (main entry point)
├── animations/                # Manim scene source files
│   ├── jepa_training.py
│   ├── adaln_conditioning.py
│   ├── sigreg_collapse.py
│   ├── mpc_cem_planning.py
│   └── generative_vs_jepa.py
├── assets/                    # Pre-rendered videos + static figures
│   └── *.mp4
└── papers/                    # Key reference PDFs
    ├── 2603.19312v2.pdf        # LeWorldModel (main paper)
    ├── 2511.08544v3.pdf        # LeJEPA — SIGReg origin (Balestriero & LeCun, 2025)
    ├── 10356_a_path_towards_autonomous_mach.pdf  # LeCun 2022 — A Path Towards Autonomous Machine Intelligence
    ├── 1803.10122v4.pdf        # Ha & Schmidhuber — World Models (2018)
    ├── 2301.08243.pdf          # I-JEPA — Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture (Assran et al., CVPR 2023)
    ├── 2404.08471.pdf          # V-JEPA — Revisiting Feature Prediction for Learning Visual Representations from Video (Bardes et al., 2024)
    ├── 2506.09985v1.pdf        # V-JEPA 2 — Self-Supervised Video Models Enable Understanding, Prediction and Planning (Assran et al., 2025)
    ├── 2602.02603.pdf          # Echo-JEPA — A Latent Predictive Foundation Model for Echocardiography (Munim et al., 2026)
    ├── 2409.19407.pdf          # Brain-JEPA — Brain Dynamics Foundation Model with Gradient Positioning and Spatiotemporal Masking (Dong et al., NeurIPS 2024)
    ├── 2209.00588.pdf          # IRIS — Transformers are Sample-Efficient World Models (Micheli et al., ICLR 2023)
    ├── 2405.12399.pdf          # DIAMOND — Diffusion for World Modeling: Visual Details Matter in Atari (Alonso et al., NeurIPS 2024)
    ├── 2509.24527v1.pdf        # DreamerV4 — Training Agents Inside of Scalable World Models (Hafner et al., 2025)
    ├── 2402.15391.pdf          # Genie — Generative Interactive Environments (Bruce et al., ICML 2024)
    ├── 2411.04983v2.pdf        # DINO-WM — World Models on Pre-trained Visual Features enable Zero-shot Planning (Zhou et al., 2024)
    ├── 2502.14819.pdf          # PLDM — Learning from Reward-Free Offline Data: Planning with Latent Dynamics Models (Sobal et al., 2025)
    ├── 2105.04906.pdf          # VICReg — Variance-Invariance-Covariance Regularization for SSL (Bardes et al., ICLR 2022)
    ├── 2010.11929v2.pdf        # ViT — An Image is Worth 16x16 Words (Dosovitskiy et al., 2021)
    ├── 1607.06450.pdf          # Layer Normalization (Ba et al., 2016)
    ├── 2212.09748v2.pdf        # DiT — Scalable Diffusion Models with Transformers (Peebles & Xie) — AdaLN origin
    ├── 2508.10104v1.pdf        # (not cited in slides — extra reference)
    ├── 2604.03208v1.pdf        # (not cited in slides — extra reference)
    ├── 2605.26379v1.pdf        # (not cited in slides — extra reference)
    └── SWM_Introduction.pdf    # Example seminar format
```

---

## Key Concepts & Terminology

When working on this project, keep the following distinctions precise:

| Term | Meaning in this project |
|---|---|
| **JEPA** | Joint Embedding Predictive Architecture — predicts in *latent* space, not pixel space |
| **LeWM** | The main paper: a JEPA-based world model with action conditioning for MBRL |
| **SIGReg** | VICReg-inspired non-contrastive regularizer used to prevent collapse in LeWM |
| **AdaLN** | Adaptive Layer Norm used to inject action embeddings into the predictor transformer. Implemented as `ConditionalBlock` in `module.py` (repo: lucas-maes/le-wm): a single `SiLU → Linear(dim, 6*dim)` zero-initialized MLP outputs 6 vectors (shift/scale/gate for attention and MLP sublayers). LayerNorm uses `elementwise_affine=False`; modulation is `x*(1+scale)+shift`; gates zero the residual at init. |
| **MPC + CEM** | Model Predictive Control with Cross-Entropy Method — inference-time planning in latent space |
| **Anti-collapse** | Keeping latent representations from collapsing to a constant — JEPA's alternative to negative pairs |
| **Generative WM** | World models that reconstruct pixels (DreamerV3, IRIS, DIAMOND) — contrasted with LeWM |

---

## Official Implementation

The official LeWM source code is at **https://github.com/lucas-maes/le-wm**. Key files:

- `module.py` — `ConditionalBlock` (AdaLN-Zero), `ARPredictor`, `SIGReg`, `Embedder`, `MLP`
- `jepa.py` — top-level `JEPA` class wiring encoder, predictor, action encoder, projectors
- `train.py` — training loop
- `eval.py` — latent planning / MPC-CEM evaluation
- `config/` — Hydra configs for hyperparameters

---

## Working Instructions for Claude

- **Search project knowledge first** before answering any paper-specific question.
- Prefer **structured outputs** (tables, outlines, bullet lists) for slide-ready content.
- When writing Manim code, target **Manim Community Edition v0.18+** syntax.
- When writing Marimo code, use the `marimo` package API (`import marimo as mo`).
- Animation scenes should be **self-contained** (no shared state between files).
- Slide content should be **presentation-register** — concise, visual-first, technically precise.
- Flag any claim that contradicts the paper PDFs in the project library.