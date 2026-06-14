# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.23.6",
#   "bibtexparser>=1.4.0,<2.0",
# ]
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(
    width="full",
    app_title="World Models Seminar",
    layout_file="layouts/presentation.slides.json",
)

with app.setup:
    import sys as _sys

    _WASM = _sys.platform == "emscripten"

    if not _WASM:
        from manim import (
            BOLD,
            BLACK,
            ITALIC,
            WHITE,
            GRAY,
            UP,
            DOWN,
            LEFT,
            RIGHT,
            TAU,
            ManimColor,
            Scene,
            Text,
            VGroup,
            Circle,
            Rectangle,
            RoundedRectangle,
            Arrow,
            CurvedArrow,
            GrowArrow,
            FadeIn,
            FadeOut,
            Create,
            Write,
        )

    VIDEO_STYLE = "width:100%;height:auto;display:block;"

    SECTION = {
        1: {"bg": "#DBEAFE", "border": "#3B82F6", "text": "#1E40AF", "label": "01 · Background & State of the Art"},
        2: {"bg": "#D1FAE5", "border": "#10B981", "text": "#065F46", "label": "02 · LeWorldModel"},
        3: {"bg": "#FEF3C7", "border": "#F59E0B", "text": "#78350F", "label": "03 · Experiments"},
        4: {"bg": "#EDE9FE", "border": "#8B5CF6", "text": "#4C1D95", "label": "04 · Discussion"},
    }

    def section_strip(num):
        import marimo as mo
        c = SECTION[num]
        return mo.Html(
            f'<div style="position:fixed;top:0.6rem;right:1.75rem;z-index:100;">'
            f'<span style="font-size:0.6rem;font-weight:700;color:{c["text"]};letter-spacing:0.1em;'
            f'text-transform:uppercase;background:{c["bg"]};padding:0.2rem 0.5rem;'
            f'border-radius:0.25rem;">'
            f'{c["label"]}</span></div>'
        )

    def page_number(num):
        # Slide number in the bottom-right corner. Numbering starts at 1 on the
        # first content slide (after the title and outline slides) so viewers
        # can reference slides during Q&A.
        import marimo as mo
        return mo.Html(
            f'<div style="position:fixed;bottom:1rem;right:1.75rem;z-index:100;">'
            f'<span style="font-size:1.25rem;font-weight:600;color:#64748B;">'
            f'{num}</span></div>'
        )

    # Single source of truth for citations: the works cited in the slides, in
    # reference order. Each entry is a BibTeX key from references.bib. The
    # bibliography renders *exactly* these (and only these), numbered by their
    # position here, and inline markers use the same numbers via cite() —so
    # the two never drift. To cite a new work: add its key here (and to
    # references.bib) and drop a cite("key") in the slide.
    CITED = [
        "maes_leworldmodel_2026",   # LeWM —the paper
        "assran_i-jepa_2023",       # I-JEPA
        "bardes_v-jepa_2024",       # V-JEPA
        "assran_v-jepa_2025",       # V-JEPA 2
        "munim_echojepa_2026",      # Echo-JEPA
        "dong_brain-jepa_2024",     # Brain-JEPA
        "micheli_iris_2023",        # IRIS
        "alonso_diamond_2024",      # DIAMOND
        "decart_oasis_2024",        # OASIS
        "hafner_dreamer4_2025",     # Dreamer 4
        "bruce_genie_2024",         # Genie
        "zhou_dino-wm_2024",        # DINO-WM
        "sobal_pldm_2025",          # PLDM
        "bardes_vicreg_2022",       # VICReg
        "dosovitskiy_vit_2021",     # ViT
        "ba_layer_normalization_2016",  # Layer Normalization
        "peebles_dit_2022",             # DiT —AdaLN origin
        "balestriero_lejepa_2025",      # LeJEPA —SIGReg origin
    ]

    def cite(key):
        # Citation number for a BibTeX key, from its position in CITED.
        return CITED.index(key) + 1 if key in CITED else "?"

    def _abbrev_authors(raw):
        import re
        authors = [a.strip() for a in re.split(r"\s+and\s+", raw)]
        out = []
        for a in authors:
            if "," in a:
                last, first = a.split(",", 1)
                last, first = last.strip(), first.strip()
            else:
                parts = a.split()
                last, first = parts[-1], " ".join(parts[:-1])
            initials = ". ".join(p[0] for p in first.split() if p)
            initials = initials + "." if initials else ""
            out.append(f"{initials} {last}".strip())
        if len(out) > 6:
            return ", ".join(out[:6]) + " et al."
        return (", ".join(out[:-1]) + ", and " + out[-1]) if len(out) > 1 else (out[0] if out else "")

    def format_ref_ieee(i, entry):
        # Returns an HTML string —one bibliography entry in IEEE style.
        def clean(s): return s.replace("{","").replace("}","").replace("\n"," ").strip()
        import re
        authors  = _abbrev_authors(clean(entry.get("author", "")))
        title    = clean(entry.get("title", ""))
        year     = clean(entry.get("year", ""))
        venue    = clean(entry.get("journal") or entry.get("booktitle") or "")
        url      = entry.get("url", "").strip()
        note     = clean(entry.get("note", ""))
        arxiv_m  = re.search(r"arXiv:([\d.]+)", note)
        arxiv_id = arxiv_m.group(1) if arxiv_m else ""

        venue_str  = f"<em>{venue}</em>" if venue else (f"arXiv:{arxiv_id}" if arxiv_id else "")
        venue_part = f"{venue_str}, " if venue_str else ""
        link_html  = (f' <a href="{url}" style="color:#3B82F6;">arXiv:{arxiv_id}</a>'
                      if arxiv_id and url else
                      f' <a href="{url}" style="color:#3B82F6;">link</a>' if url else "")
        return (
            f'<p style="margin:0.35rem 0;font-size:0.95rem;line-height:1.45;color:#1E293B;">'
            f'<strong>[{i}]</strong> {authors}, &ldquo;{title},&rdquo; {venue_part}{year}.{link_html}'
            f'</p>'
        )

    def sota_table(headers, rows, aligns=None, section=1):
        # Styled HTML table rendered as raw HTML so it escapes Marimo's green
        # zebra-striping / yellow hover on markdown tables. Rows have no
        # background by default and tint to the section colour on hover.
        import marimo as mo
        c = SECTION[section]
        aligns = aligns or ["left"] * len(headers)

        head = "".join(
            f'<th style="text-align:{a};padding:0.6rem 1rem;'
            f'border-bottom:2px solid #CBD5E1;font-weight:700;color:#374151;'
            f'font-size:1.15rem;">{h}</th>'
            for h, a in zip(headers, aligns)
        )
        body = ""
        for row in rows:
            cells = "".join(
                f'<td style="text-align:{a};padding:0.6rem 1rem;'
                f'border-bottom:1px solid #E5E7EB;">{cell}</td>'
                for cell, a in zip(row, aligns)
            )
            body += f"<tr>{cells}</tr>"

        # Hover highlight in the section colour (background tint + text shade).
        style = (
            "<style>"
            ".sota-table tbody tr{transition:background-color .12s ease;}"
            f".sota-table tbody tr:hover{{background:{c['bg']} !important;}}"
            f".sota-table tbody tr:hover td{{color:{c['text']};font-weight:600;}}"
            "</style>"
        )
        return mo.Html(
            style
            + '<table class="sota-table" style="border-collapse:collapse;'
            'width:100%;font-size:1.3rem;line-height:1.5;color:#374151;">'
            f'<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'
        )

    def render_scene(scene_cls, quality="high_quality"):
        import base64
        import inspect
        import pathlib
        import subprocess
        import sys

        _quality_to_dir = {
            "low_quality": "480p15",
            "medium_quality": "720p30",
            "high_quality": "1080p60",
            "fourk_quality": "2160p60",
        }
        _quality_to_flag = {
            "low_quality": "-ql",
            "medium_quality": "-qm",
            "high_quality": "-qh",
            "fourk_quality": "-qk",
        }
        _root = pathlib.Path(__file__).parent
        _res_dir = _quality_to_dir[quality]
        _scene_name = scene_cls.__name__
        _source = pathlib.Path(inspect.getfile(scene_cls))
        _source_stem = _source.stem
        _out = _root / "media" / "videos" / _source_stem / _res_dir / f"{_scene_name}.mp4"

        if sys.platform != "emscripten":
            # Re-render via CLI subprocess if missing or stale —the CLI is the
            # only reliable way to get output at the expected path.
            _stale = _out.exists() and _source.stat().st_mtime > _out.stat().st_mtime
            if not _out.exists() or _stale:
                subprocess.run(
                    [sys.executable, "-m", "manim",
                     _quality_to_flag[quality], str(_source), _scene_name],
                    cwd=str(_root),
                    check=True,
                    capture_output=True,
                )

            if not _out.exists():
                import marimo as mo
                return mo.callout(
                    mo.md(f"Video not found: `{_out.name}` —"
                          f"run `manim -qh {_source.name} {_scene_name}` to render it."),
                    kind="warn",
                )

            _b64 = base64.b64encode(_out.read_bytes()).decode()
            import marimo as mo
            return mo.Html(
                f'<video autoplay muted style="{VIDEO_STYLE}">'
                f'<source src="data:video/mp4;base64,{_b64}" type="video/mp4">'
                f'</video>'
            )
        else:
            # WASM: video served as a static file copied alongside the HTML in CI
            _rel = f"media/videos/{_source_stem}/{_res_dir}/{_scene_name}.mp4"
            import marimo as mo
            return mo.Html(
                f'<video autoplay muted style="{VIDEO_STYLE}">'
                f'<source src="{_rel}" type="video/mp4">'
                f'</video>'
            )


@app.cell
def title_slide():
    import marimo as mo
    mo.vstack(
        [
            mo.Html(
                "<style>"
                ":root { font-size: 12px; }"
                "mjx-container { font-size: 85% !important; }"
                ".marimo-markdown p, .marimo-markdown li { font-size: 0.9rem; }"
                "</style>"
            ),
            mo.md("World Models Seminar · Technical University of Munich "),
            mo.md("*Chair of Computer Aided Medical Procedures*"),
            mo.md("&nbsp;"),
            mo.md("# LeWorldModel"),    
            mo.md("###Stable End-to-End Joint-Embedding Predictive Architecture from Pixels"),
            mo.md("&nbsp;"),
            mo.md("Lucas Maes · Quentin Le Lidec · Damien Scieur · Yann LeCun · Randall Balestriero"),
            mo.md("*Mila / Université de Montréal · NYU · Samsung SAIL · Brown University*"),
            mo.md("[arXiv 2603.19312](https://arxiv.org/abs/2603.19312)"),
            mo.md("---"),
            mo.md("Presented by **Julian Arkenau** · 19 June 2026"),
        ],
        justify="center",
        align="center",
    )
    return (mo,)


@app.cell
def outline_slide():
    def _():
        import marimo as mo

        def _entry(num, title, bullets):
            c = SECTION[num]
            items = "".join(
                f'<li style="margin:0.25rem 0;font-size:1.2rem;color:#374151;">{b}</li>'
                for b in bullets
            )
            return mo.Html(
                f'<div style="padding:0.25rem 0;">'
                f'<div style="font-weight:700;color:{c["text"]};font-size:1.6rem;margin-bottom:0.3rem;">{title}</div>'
                f'<ul style="margin:0;padding-left:1.1rem;">{items}</ul>'
                f'</div>'
            )

        return mo.vstack(
            [
                mo.md("# Outline"),
                _entry(1, "01 · Background & State of the Art", [
                    "JEPA: predict in latent space, not pixel space",
                    "Representation collapse —the central challenge",
                    "How existing methods solve it and where they fall short",
                ]),
                _entry(2, "02 · LeWorldModel", [
                    "ViT-Tiny encoder + action-conditioned transformer predictor",
                    "SIGReg: one hyperparameter to prevent collapse",
                    "Latent planning via MPC + CEM",
                ]),
                _entry(3, "03 · Experiments", [
                    "Task performance and planning speed across multiple benchmarks",
                    "Physics emerges in latent space",
                ]),
                _entry(4, "04 · Discussion", [
                    "Authors' claims, personal assessment, open questions",
                ]),
            ],
            align="start",
            gap="0.5rem",
        )
    _()
    return


@app.cell
def jepa_principle_animation_slide():
    import sys as _sys
    import marimo as _mo
    if _sys.platform != "emscripten":
        import pathlib as _pathlib, subprocess as _sp
        _sys.path.insert(0, str(_pathlib.Path(__file__).parent))
        from animations.jepa_training import JEPATraining
        _video = render_scene(JEPATraining)
        # Keep the last frame in sync for the following static slides
        _mp4  = _pathlib.Path(__file__).parent / "media/videos/jepa_training/1080p60/JEPATraining.mp4"
        _frame = _pathlib.Path(__file__).parent / "media/images/jepa_final_frame.png"
        _frame.parent.mkdir(parents=True, exist_ok=True)
        if _mp4.exists() and (not _frame.exists() or _mp4.stat().st_mtime > _frame.stat().st_mtime):
            _sp.run(
                ["ffmpeg", "-sseof", "-0.1", "-i", str(_mp4),
                 "-frames:v", "1", str(_frame), "-y"],
                capture_output=True,
            )
    else:
        _video = _mo.Html(
            f'<video autoplay muted style="{VIDEO_STYLE}">'
            '<source src="media/videos/jepa_training/1080p60/JEPATraining.mp4" type="video/mp4">'
            '</video>'
        )
    _mo.vstack([section_strip(1), page_number(1), _video])
    return


@app.cell
def representation_collapse_question():
    def _():
        import sys
        import marimo as mo

        if sys.platform != "emscripten":
            import pathlib
            img_src = (pathlib.Path(__file__).parent / "media/images/jepa_final_frame.png").read_bytes()
        else:
            img_src = "media/images/jepa_final_frame.png"

        return mo.vstack([
            section_strip(1),
            page_number(2),
            mo.hstack(
                [
                    mo.vstack(
                        [
                            mo.md("## Representation Collapse"),
                            mo.md("*THE CORE PROBLEM OF JEPA-BASED ARCHITECTURES*"),
                            mo.md("&nbsp;"),
                            mo.md("&nbsp;"),
                            mo.md("What is the easiest way a model could achieve **(near-)perfect prediction loss?**"),
                        ],
                        align="start",
                    ),
                    mo.vstack(
                        [
                            mo.md("*JEPA ARCHITECTURE*"),
                            mo.image(img_src),
                        ],
                        align="center",
                    ),
                ],
                widths=[1, 1],
                gap="3rem",
                align="start",
            ),
        ])
    _()
    return


@app.cell
def representation_collapse_answer():
    def _():
        import sys
        import marimo as mo

        if sys.platform != "emscripten":
            import pathlib
            img_src = (pathlib.Path(__file__).parent / "media/images/jepa_final_frame.png").read_bytes()
        else:
            img_src = "media/images/jepa_final_frame.png"

        return mo.vstack([
            section_strip(1),
            page_number(3),
            mo.hstack(
                [
                    mo.vstack(
                        [
                            mo.md("## Representation Collapse"),
                            mo.md("*THE CORE PROBLEM OF JEPA-BASED ARCHITECTURES*"),
                            mo.md("&nbsp;"),
                            mo.md("""
    **01 Complete Collapse**

    - All inputs collapse to a single point in embedding space.
    - Predictor achieves zero loss without learning anything.

    **02 Dimensional Collapse**

    - Embeddings span only a low-dimensional subspace.
    - Loss looks fine, but representations are impoverished.
                            """),
                        ],
                        align="start",
                    ),
                    mo.vstack(
                        [
                            mo.md("*JEPA ARCHITECTURE*"),
                            mo.image(img_src),
                        ],
                        align="center",
                    ),
                ],
                widths=[1, 1],
                gap="3rem",
                align="start",
            ),
        ])
    _()
    return


@app.cell
def sota_anticollapse_slide():
    def _():
        import marimo as mo
        return mo.vstack([
            section_strip(1),
            page_number(4),
            mo.md("## State of the Art —by *Anti-Collapse Strategy*"),
            mo.md("*HOW DOES EACH METHOD AVOID REPRESENTATION COLLAPSE?*"),
            mo.md("&nbsp;"),
            sota_table(
                ["Strategy", "Mechanism", "Limitation"],
                [
                    [f"Generative reconstruction (DreamerV4 [{cite('hafner_dreamer4_2025')}])",
                     "Pixel target is fixed, collapse impossible by construction",
                     "Wastes capacity modelling irrelevant pixel detail"],
                    [f"EMA + stop-gradient (V-JEPA 2 [{cite('assran_v-jepa_2025')}])",
                     "Asymmetric self-distillation from a moving-average teacher",
                     "No well-defined objective, purely heuristic"],
                    [f"Frozen pretrained encoder (DINO-WM [{cite('zhou_dino-wm_2024')}])",
                     "Encoder is fixed, so it cannot collapse",
                     "Bounded by pretraining knowledge; not end-to-end"],
                    [f"Explicit regularization (VICReg [{cite('bardes_vicreg_2022')}], PLDM [{cite('sobal_pldm_2025')}])",
                     "Variance / covariance penalty terms",
                     "Training instabilities; up to 6 loss hyperparameters"],
                ],
            ),
        ], align="start")
    _()
    return


@app.cell
def sota_target_task_slide():
    def _():
        import marimo as mo
        return mo.vstack([
            section_strip(1),
            page_number(5),
            mo.md("## State of the Art —by *Target Task*"),
            mo.md("*WHAT PROBLEM IS THE WORLD MODEL ASKED TO SOLVE?*"),
            mo.md("&nbsp;"),
            sota_table(
                ["Family", "What it does", "Representative work"],
                [
                    ["Self-supervised representation learning",
                     "Predict masked latent patches no actions, no planning",
                     f"I-JEPA [{cite('assran_i-jepa_2023')}], V-JEPA 2 [{cite('assran_v-jepa_2025')}]"],
                    ["Generative world models",
                     "Action-conditioned pixel-space simulators, often reward-based, for RL &amp; games",
                     f"DreamerV4 [{cite('hafner_dreamer4_2025')}], Genie [{cite('bruce_genie_2024')}]"],
                    ["Latent action-conditioned world models",
                     "Predict dynamics in latent space, plan by imagination",
                     f"DINO-WM [{cite('zhou_dino-wm_2024')}], PLDM [{cite('sobal_pldm_2025')}]"],
                ],
            ),
        ], align="start")
    _()
    return


@app.cell
def sota_summary_slide():
    def _():
        import marimo as mo
        return mo.vstack([
            section_strip(1),
            page_number(6),
            mo.md("## State of the Art —Where LeWM Fits"),
            mo.md("*TWO AXES, ONE GAP*"),
            mo.md("&nbsp;"),
            sota_table(
                ["Method", "Target task", "Anti-collapse",
                 "End-to-end", "Reward-free", "Loss hyperparams"],
                [
                    [f"V-JEPA 2 [{cite('assran_v-jepa_2025')}]", "Representation learning", "EMA + stop-grad", "✓", "—", "—"],
                    [f"DreamerV4 [{cite('hafner_dreamer4_2025')}]", "Generative control", "Reconstruction", "✓", "✗", "—"],
                    [f"DINO-WM [{cite('zhou_dino-wm_2024')}]", "Latent control", "Frozen encoder", "✗", "✓", "—"],
                    [f"PLDM [{cite('sobal_pldm_2025')}]", "Latent control", f"VICReg [{cite('bardes_vicreg_2022')}]", "✓", "✓", "6"],
                    [f"LeWM [{cite('maes_leworldmodel_2026')}]", "Latent control", "SIGReg", "✓", "✓", "1"],
                ],
                aligns=["left", "left", "left", "center", "center", "center"],
            ),
            mo.md("&nbsp;"),
            mo.md(
                "**LeWM** is the only method that is *task-agnostic, reward-free, "
                "end-to-end from pixels,* **and** trained with a single, provably "
                "collapse-free regularizer."
            ),
        ], align="start")
    _()
    return


@app.cell
def outline_recap_after_sota():
    # Recap of the outline shown at the 01 — 02 boundary. Section 01 is grayed
    # out (done) and 02 is flagged "up next", giving anyone who has drifted a
    # beat to re-orient before the main contributions begin.
    def _():
        import marimo as mo

        def _entry(num, title, bullets, *, done=False):
            c = SECTION[num]
            if done:
                title_color, bullet_color, opacity = "#9CA3AF", "#9CA3AF", "0.5"
                mark = '<span style="color:#9CA3AF;">&#10003;</span> '
            else:
                title_color, bullet_color, opacity = c["text"], "#374151", "1"
                mark = ""
            items = "".join(
                f'<li style="margin:0.25rem 0;font-size:1.2rem;color:{bullet_color};">{b}</li>'
                for b in bullets
            )
            return mo.Html(
                f'<div style="padding:0.25rem 0;opacity:{opacity};">'
                f'<div style="font-weight:700;color:{title_color};font-size:1.6rem;margin-bottom:0.3rem;">'
                f'{mark}{title}</div>'
                f'<ul style="margin:0;padding-left:1.1rem;">{items}</ul>'
                f'</div>'
            )

        return mo.vstack(
            [
                mo.md("# Outline"),
                _entry(1, "01 · Background & State of the Art", [
                    "JEPA: predict in latent space, not pixel space",
                    "Representation collapse —the central challenge",
                    "How existing methods solve it and where they fall short",
                ], done=True),
                _entry(2, "02 · LeWorldModel", [
                    "ViT-Tiny encoder + action-conditioned transformer predictor",
                    "SIGReg: one hyperparameter to prevent collapse",
                    "Latent planning via MPC + CEM",
                ]),
                _entry(3, "03 · Experiments", [
                    "Task performance and planning speed across multiple benchmarks",
                    "Physics emerges in latent space",
                ]),
                _entry(4, "04 · Discussion", [
                    "Authors' claims, personal assessment, open questions",
                ]),
            ],
            align="start",
            gap="0.5rem",
        )
    _()
    return


@app.cell
def lewm_architecture_animation_slide():
    import sys as _sys
    import marimo as _mo
    if _sys.platform != "emscripten":
        _sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
        from animations.lewm_architecture import LeWMArchitecture
        _video = render_scene(LeWMArchitecture)
    else:
        _video = _mo.Html(
            f'<video autoplay muted style="{VIDEO_STYLE}">'
            '<source src="media/videos/lewm_architecture/1080p60/LeWMArchitecture.mp4" type="video/mp4">'
            '</video>'
        )
    _mo.vstack([section_strip(2), page_number(7), _video])
    return


@app.cell
def vit_encoder_slide(mo):
    import sys as _sys
    if _sys.platform != "emscripten":
        _sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
        from animations.vit_tiny_encoder import ViTTinyEncoder
        _video = render_scene(ViTTinyEncoder)
    else:
        _video = mo.Html(
            f'<video autoplay muted loop style="{VIDEO_STYLE}">'
            '<source src="media/videos/vit_tiny_encoder/1080p60/ViTTinyEncoder.mp4" type="video/mp4">'
            '</video>'
        )

    mo.vstack([
        section_strip(2),
        page_number(8),
        _video,
        mo.Html(
            f'<div style="text-align:right;font-size:0.9rem;color:#000000;margin-top:0.25rem;">'
            f'ViT architecture: Dosovitskiy et al. [{cite("dosovitskiy_vit_2021")}]'
            f'</div>'
        ),
    ])
    return


@app.cell
def adaln_formulas_slide(mo):
    import sys as _sys
    import pathlib as _pathlib

    _ACTION = "#8E6FBF"

    _heading = mo.Html(
        f'<div style="display:flex;align-items:center;gap:0.6rem;">'
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:1.7rem;height:1.7rem;border-radius:50%;background:{_ACTION};'
        f'color:white;font-weight:700;font-size:1.1rem;flex-shrink:0;">2</span>'
        f'<h2 style="margin:0;line-height:1.2;">Action Conditioning via AdaLN-Zero</h2>'
        f'</div>'
    )

    _standard_ln = mo.vstack([
        mo.Html(f'<h3 style="margin:0 0 0.3rem 0;color:#334155;">Standard LN &nbsp;<span style="font-size:0.8rem;font-weight:400;color:#64748B;">Ba et al. [{cite("ba_layer_normalization_2016")}]</span></h3>'),
        mo.md(r"$$y = \gamma \cdot \frac{x - \mu}{\sigma} + \beta$$"),
        mo.md(
            "- $\\gamma, \\beta$ are **fixed** learned parameters\n"
            "- Same for every input, no external conditioning"
        ),
    ], align="start")

    _adaptive_ln = mo.vstack([
        mo.Html(f'<h3 style="margin:0 0 0.3rem 0;color:#334155;">AdaLN-Zero &nbsp;<span style="font-size:0.8rem;font-weight:400;color:#64748B;">Peebles & Xie [{cite("peebles_dit_2022")}]</span></h3>'),
        mo.md(r"$$y = \underbrace{(1+\Sigma(c))}_{\text{scale}} \cdot \frac{x-\mu}{\sigma} + \underbrace{\Delta(c)}_{\text{shift}}, \quad x \leftarrow x + \underbrace{G(c)}_{\text{gate}} \cdot \text{sublayer}(y)$$"),
        mo.md(r"$$[\Delta,\Sigma,G]_{\text{attn}},[\Delta,\Sigma,G]_{\text{mlp}} = \text{SiLU}(c)\,W + b$$"),
        mo.md(
            "- $\\Delta, \\Sigma, G$ **from conditioning signal** $c$ (the action)\n"
            "- **6 outputs**: shift / scale / gate for attn & MLP\n"
            "- **Zero-init**: $W=0, b=0$ — identity at init"
        ),
    ], align="start")

    _silu_img_url = "https://pytorch.org/docs/2.12/_images/SiLU.png"
    _silu_panel = mo.Html(
        f'<div style="margin-left:auto;width:fit-content;text-align:center;transform:scale(0.65);transform-origin:top right;">'
        f'<img src="{_silu_img_url}" style="max-width:100%;height:auto;display:block;" />'
        f'<p style="margin:0.3rem 0 0.1rem 0;font-size:1.1rem;font-weight:600;color:#334155;">SiLU(x) = x · σ(x)</p>'
        f'<a href="https://docs.pytorch.org/docs/2.12/generated/torch.nn.SiLU.html" '
        f'style="font-size:1rem;color:#3B82F6;">torch.nn.SiLU</a>'
        f'</div>'
    )

    mo.vstack([
        section_strip(2),
        page_number(9),
        _heading,
        mo.md("*HOW THE ACTION EMBEDDING MODULATES EVERY PREDICTOR LAYER*"),
        mo.hstack([
            mo.vstack([_standard_ln, mo.md("&nbsp;"), _adaptive_ln], align="start"),
            _silu_panel,
        ], widths=[1, 1], gap="2rem", align="start"),
    ])
    return


@app.cell
def adaln_why_lewm_slide(mo):
    import sys as _sys
    import pathlib as _pathlib

    _ACTION = "#8E6FBF"

    _heading = mo.Html(
        f'<div style="display:flex;align-items:center;gap:0.6rem;">'
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:1.7rem;height:1.7rem;border-radius:50%;background:{_ACTION};'
        f'color:white;font-weight:700;font-size:1.1rem;flex-shrink:0;">2</span>'
        f'<h2 style="margin:0;line-height:1.2;">Why AdaLN-Zero in LeWM?</h2>'
        f'</div>'
    )

    _text = mo.vstack([
        mo.md(
            "**01 Why scale + shift? Not concatenation or addition?**\n\n"
            "- *Concat / addition*: action signal is drowned out or shifts features uniformly\n"
            "- *AdaLN*: action conditions both the **scale and shift of every feature**\n\n"
            "**02 Why zero-init?**\n\n"
            "- $G{=}0$ gates out the sublayer's contribution **pure skip connection**:  \n"
            "  $x \\leftarrow x + 0{\\cdot}\\text{sublayer}(y) = x$\n"
            "- **Two-phase**: SIGReg first anchors the latent geometry; "
            "gates then open progressively as representations mature — stable end-to-end training"
        ),
    ], align="start")

    if _sys.platform != "emscripten":
        _img_src = (_pathlib.Path(__file__).parent / "media/images/AdaLNTransformerBlock_ManimCE_v0.20.1.png").read_bytes()
    else:
        _img_src = "media/images/AdaLNTransformerBlock_ManimCE_v0.20.1.png"

    mo.vstack([
        section_strip(2),
        page_number(10),
        _heading,
        mo.md("&nbsp;"),
        mo.hstack([
            _text,
            mo.image(_img_src),
        ], widths=[1, 1], gap="2rem", align="start"),
    ], align="start")
    return


@app.cell
def sigreg_optimal_distribution_slide(mo):
    _SIG = "#10B981"

    _heading = mo.Html(
        f'<div style="display:flex;align-items:center;gap:0.6rem;">'
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:1.7rem;height:1.7rem;border-radius:50%;background:{_SIG};'
        f'color:white;font-weight:700;font-size:1.1rem;flex-shrink:0;">3</span>'
        f'<h2 style="margin:0;line-height:1.2;">Why Isotropic Gaussian?</h2>'
        f'</div>'
    )

    mo.vstack([
        section_strip(2),
        page_number(11),
        _heading,
        mo.md("*THE THEORETICALLY OPTIMAL TARGET FOR ANY DOWNSTREAM TASK*"),
        mo.md("&nbsp;"),
        mo.Html('<h3 style="margin:0 0 0.5rem 0;color:#334155;">Two lemmas against anisotropy</h3>'),
        mo.md(
            "- **Lemma 1**: anisotropic covariance ($\\lambda_K > \\lambda_1$) "
            "always hurts bias on some downstream task\n"
            "- **Lemma 2**: OLS estimation variance is minimised **if and only if** "
            "$\\text{Cov}(Z) \\propto I$"
        ),
        mo.md("&nbsp;"),
        mo.Html(
            f'<h3 style="margin:0 0 0.5rem 0;color:#334155;">Theorem 1'
            f'&nbsp;<span style="font-size:0.8rem;font-weight:400;color:#64748B;">'
            f'LeJEPA [{cite("balestriero_lejepa_2025")}]</span></h3>'
        ),
        mo.md(
            "Among all distributions with fixed total variance, "
            "$\\mathcal{N}(0, I)$ **uniquely minimises** integrated squared bias "
            "across all downstream tasks (linear & nonlinear)."
        ),
    ], align="start")
    return


@app.cell
def sigreg_algorithm_slide(mo):
    _SIG = "#10B981"

    _heading = mo.Html(
        f'<div style="display:flex;align-items:center;gap:0.6rem;">'
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:1.7rem;height:1.7rem;border-radius:50%;background:{_SIG};'
        f'color:white;font-weight:700;font-size:1.1rem;flex-shrink:0;">3</span>'
        f'<h2 style="margin:0;line-height:1.2;">SIGReg: The Sketching Algorithm</h2>'
        f'</div>'
    )

    _left = mo.vstack([
        mo.Html('<h3 style="margin:0 0 0.3rem 0;color:#334155;">The sketching algorithm</h3>'),
        mo.md(
            "**Step 1**: Sample $M$ random unit-norm directions:\n\n"
            "$$\\boldsymbol{u}^{(m)} \\sim \\mathcal{U}(S^{d-1}), \\quad m = 1, \\ldots, M$$\n\n"
            "**Step 2**: Project embeddings $Z \\in \\mathbb{R}^{N \\times d}$ onto each direction:\n\n"
            "$$\\boldsymbol{h}^{(m)} = Z\\,\\boldsymbol{u}^{(m)} \\in \\mathbb{R}^N$$\n\n"
            "**Step 3**: Apply a normality test $T$ to each projection and average:\n\n"
            "$$\\text{SIGReg}(Z) \\triangleq \\frac{1}{M}\\sum_{m=1}^{M} T\\!\\left(\\boldsymbol{h}^{(m)}\\right)$$\n\n"
            "By the **Cramér–Wold theorem**: matching all 1-D marginals "
            "$\\Leftrightarrow$ matching the full $d$-dimensional joint distribution."
        ),
    ], align="start")

    _right = mo.vstack([
        mo.Html(
            '<p style="margin:0 0 0.3rem 0;font-size:0.72rem;font-weight:700;'
            'color:#94A3B8;text-transform:uppercase;letter-spacing:0.08em;">'
            'Normality test: Epps–Pulley</p>'
        ),
        mo.md(r"$$T = N\!\int_{-\infty}^{\infty} \!\left|\hat{\varphi}_X(t) - e^{-t^2/2}\right|^2 e^{-t^2/2}\,\mathrm{d}t$$"),
        mo.md(
            "<span style='font-size:0.78rem;color:#94A3B8;'>"
            "Compares empirical CF against the Gaussian CF. "
            "Bounded gradients $|\\partial T/\\partial z_i| \\leq 4\\sigma^2/N$, "
            "$\\mathcal{O}(N)$, differentiable."
            "</span>"
        ),
    ], align="start")

    mo.vstack([
        section_strip(2),
        page_number(12),
        _heading,
        mo.md("&nbsp;"),
        mo.hstack([_left, _right], widths=[1, 1], gap="2.5rem", align="start"),
    ], align="start")
    return


@app.cell
def sigreg_mechanism_slide(mo):
    import sys as _sys
    if _sys.platform != "emscripten":
        _sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
        from animations.sigreg_collapse import SIGRegVisualization
        _video = render_scene(SIGRegVisualization)
    else:
        _video = mo.Html(
            f'<video autoplay muted loop style="{VIDEO_STYLE}">'
            '<source src="media/videos/sigreg_collapse/1080p60/SIGRegVisualization.mp4"'
            ' type="video/mp4"></video>'
        )

    _SIG = "#10B981"

    _heading = mo.Html(
        f'<div style="display:flex;align-items:center;gap:0.6rem;">'
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:1.7rem;height:1.7rem;border-radius:50%;background:{_SIG};'
        f'color:white;font-weight:700;font-size:1.1rem;flex-shrink:0;">3</span>'
        f'<h2 style="margin:0;line-height:1.2;">SIGReg: Enforcing the Gaussian Target</h2>'
        f'</div>'
    )

    mo.vstack([
        section_strip(2),
        page_number(13),
        _heading,
        _video,
    ], align="start")
    return


@app.cell
def latent_planning_concept_slide(mo):
    import sys as _sys
    import pathlib as _pathlib

    _PLAN = "#0EA5E9"

    _heading = mo.Html(
        f'<h2 style="margin:0;line-height:1.2;">Latent Planning —Planning in Imagination</h2>'
    )

    if _sys.platform != "emscripten":
        _fig_src = (_pathlib.Path(__file__).parent / "media/images/lewm_latent_planning_fig4.png").read_bytes()
    else:
        _fig_src = "media/images/lewm_latent_planning_fig4.png"

    _fig = mo.image(
        src=_fig_src,
        caption=f"Figure 4. LeWorldModel Latent Planning. Source: [{cite('maes_leworldmodel_2026')}]",
        width="100%",
    )

    def _item(n, title, body):
        return mo.md(f'<span style="font-weight:700;">{n}. {title}</span> {body}')

    _bullets = mo.hstack([
        mo.vstack([
            _item(1, "Encode", r"map $o_1 \to z_1$ and $o_g \to z_g$ via frozen encoder"),
            _item(2, "Imagine", r"unroll predictor $H$ steps with candidate actions $a_1, \ldots, a_H$"),
        ], align="start"),
        mo.vstack([
            _item(3, "Score", r"compute cost $\|\hat{z}_H - z_g\|$ in latent space"),
            _item(4, "Iterate", "solver updates actions and repeats until cost is minimised"),
        ], align="start"),
    ], gap="2rem", align="start")

    mo.vstack([
        section_strip(2),
        page_number(14),
        _heading,
        mo.md("*FINDING THE OPTIMAL ACTION SEQUENCE ENTIRELY IN IMAGINATION*"),
        mo.md("&nbsp;"),
        _fig,
        mo.md("&nbsp;"),
        _bullets,
    ], align="start")
    return


@app.cell
def latent_planning_cem_slide(mo):
    _heading = mo.Html(
        f'<h2 style="margin:0;line-height:1.2;">CEM + MPC: Search, Execute, Replan</h2>'
    )

    _callout = mo.Html(
        '<div style="background:#F0F9FF;border:1.5px solid #0EA5E9;border-radius:0.5rem;'
        'padding:0.5rem 1rem;margin-bottom:0.8rem;">'
        '<span style="font-size:0.72rem;font-weight:700;color:#0C4A6E;'
        'text-transform:uppercase;letter-spacing:0.08em;">Zero-order optimizer&ensp;</span>'
        '<span style="font-size:0.9rem;color:#374151;">'
        'Does not require differentiability through the world model rollout.'
        '</span></div>'
    )

    _algo = mo.Html(
        '<div style="background:#F8FAFC;border:1px solid #CBD5E1;border-radius:0.5rem;'
        'padding:0.6rem 1rem;font-family:monospace;font-size:0.83rem;line-height:1.55;">'
        '<div style="font-weight:700;font-size:0.75rem;letter-spacing:0.06em;color:#475569;'
        'text-transform:uppercase;border-bottom:1px solid #CBD5E1;margin-bottom:0.4rem;'
        'padding-bottom:0.25rem;">Algorithm —Cross-Entropy Method (CEM) for Action Sequence Optimization</div>'
        '<div><b>Initialize:</b> μ<sub>0</sub> = <b>0</b>, Σ<sub>0</sub> = I</div>'
        '<div><b>for</b> t = 1 <b>to</b> T <b>do</b></div>'
        '<div style="padding-left:1.4rem;">Sample N candidates '
        '{a<sub>1:H</sub><sup>(i)</sup>} ~ 𝒩(μ<sub>t−1</sub>, Σ<sub>t−1</sub>)</div>'
        '<div style="padding-left:1.4rem;"><b>for</b> i = 1 <b>to</b> N <b>do</b></div>'
        '<div style="padding-left:2.8rem;">Roll out a<sub>1:H</sub><sup>(i)</sup> in world model f</div>'
        '<div style="padding-left:2.8rem;">Compute cost '
        'J<sup>(i)</sup> = ‖ẑ<sub>H</sub><sup>(i)</sup> − z<sub>g</sub>‖²</div>'
        '<div style="padding-left:1.4rem;"><b>end for</b></div>'
        '<div style="padding-left:1.4rem;">Select top-K elites ℰ (lowest cost)</div>'
        '<div style="padding-left:1.4rem;">'
        'μ<sub>t</sub> ← (1/K) ∑<sub>i∈ℰ</sub> a<sub>1:H</sub><sup>(i)</sup></div>'
        '<div style="padding-left:1.4rem;">'
        'Σ<sub>t</sub> ← Var<sub>i∈ℰ</sub>(a<sub>1:H</sub><sup>(i)</sup>)</div>'
        '<div><b>end for</b></div>'
        '<div><b>return</b> μ<sub>T</sub></div>'
        '<div style="border-top:1px solid #CBD5E1;margin-top:0.35rem;padding-top:0.25rem;'
        'font-size:0.72rem;color:#64748B;font-family:sans-serif;">'
        'LeWM: N=300 &ensp; K=30 &ensp; T=30 (PushT) / 10 (others) &ensp; H=5'
        '</div></div>'
    )

    _mpc = mo.vstack([
        mo.Html('<h3 style="margin:0.6rem 0 0.3rem 0;color:#334155;">Model Predictive Control (MPC)</h3>'),
        mo.md(
            "- **Execute** the entire optimized $H{=}5$ step sequence in the real environment\n"
            "- **Observe** the resulting new state\n"
            "- **Replan** by running CEM again from the new real observation\n\n"
            "*Short horizon keeps prediction error low enough that the full plan can be trusted.*"
        ),
    ], align="start")

    mo.vstack([
        section_strip(2),
        page_number(15),
        _heading,
        mo.md("&nbsp;"),
        _callout,
        _algo,
        _mpc,
    ], align="start")
    return


@app.cell
def outline_recap_after_lewm():
    ''# Recap shown at the 02 — 03 boundary. Sections 01 and 02 are grayed out
    # (done); 03 is up next.
    def _():
        import marimo as mo

        def _entry(num, title, bullets, *, done=False):
            c = SECTION[num]
            if done:
                title_color, bullet_color, opacity = "#9CA3AF", "#9CA3AF", "0.5"
                mark = '<span style="color:#9CA3AF;">&#10003;</span> '
            else:
                title_color, bullet_color, opacity = c["text"], "#374151", "1"
                mark = ""
            items = "".join(
                f'<li style="margin:0.25rem 0;font-size:1.2rem;color:{bullet_color};">{b}</li>'
                for b in bullets
            )
            return mo.Html(
                f'<div style="padding:0.25rem 0;opacity:{opacity};">'
                f'<div style="font-weight:700;color:{title_color};font-size:1.6rem;margin-bottom:0.3rem;">'
                f'{mark}{title}</div>'
                f'<ul style="margin:0;padding-left:1.1rem;">{items}</ul>'
                f'</div>'
            )

        return mo.vstack(
            [
                mo.md("# Outline"),
                _entry(1, "01 · Background & State of the Art", [
                    "JEPA: predict in latent space, not pixel space",
                    "Representation collapse —the central challenge",
                    "How existing methods solve it and where they fall short",
                ], done=True),
                _entry(2, "02 · LeWorldModel", [
                    "ViT-Tiny encoder + action-conditioned transformer predictor",
                    "SIGReg: one hyperparameter to prevent collapse",
                    "Latent planning via MPC + CEM",
                ], done=True),
                _entry(3, "03 · Experiments", [
                    "Task performance and planning speed across multiple benchmarks",
                    "Physics emerges in latent space",
                ]),
                _entry(4, "04 · Discussion", [
                    "Authors' claims, personal assessment, open questions",
                ]),
            ],
            align="start",
            gap="0.5rem",
        )
    _()
    return


@app.cell
def experiments_environments_slide(mo):
    import sys as _esys
    import pathlib as _epathlib

    _EXP_BG  = "#FEF3C7"
    _EXP_BDR = "#F59E0B"

    _heading = mo.Html(
        '<h2 style="margin:0;">Evaluation Environments</h2>'
    )
    _subtitle = mo.Html(
        '<p style="margin:0;color:#64748B;font-size:1.1rem;">'
        'Four tasks spanning 2D/3D manipulation, navigation, and motion planning'
        '</p>'
    )

    _env_imgs = {}
    for _name, _label in [
        ("env_pusht",   "Push-T (2D)"),
        ("env_ogbench", "OGBench-Cube (3D)"),
        ("env_tworoom", "Two-Room (nav.)"),
        ("env_reacher", "Reacher (2D)"),
    ]:
        if _esys.platform != "emscripten":
            _src = (_epathlib.Path(__file__).parent / f"assets/{_name}.png").read_bytes()
        else:
            _src = f"assets/{_name}.png"
        _env_imgs[_label] = _src

    _env_panels = mo.hstack(
        [
            mo.vstack(
                [
                    mo.image(src, width=201),
                    mo.Html(f'<p style="margin:4px 0 0;font-size:0.85rem;color:#64748B;text-align:center;">{lbl}</p>'),
                ],
                align="center",
            )
            for lbl, src in _env_imgs.items()
        ],
        gap=1,
    )

    _results = mo.md(
        "- **Push-T** (2D manipulation): LeWM **96%** vs PLDM 78% vs DINO-WM 92% → best overall \n"
        "- **OGBench-Cube** (3D manipulation): LeWM 74% vs DINO-WM 86% → DINO-WM leads; 3D visual complexity challenges encoder\n"
        "- **Two-Room** (navigation): LeWM 87% vs PLDM/DINO-WM ~100% → worst case; Gaussian prior ill-suited to low-dimensional task\n"
        "- **Reacher** (continuous control): LeWM **86%** vs PLDM 78% vs DINO-WM 79% → best overall\n"
        "- **Speed**: LeWM plans in **<1 s** → **48× faster** than DINO-WM at equal compute budget"
    )

    mo.vstack([
        section_strip(3),
        page_number(16),
        _heading,
        _subtitle,
        mo.md("&nbsp;"),
        _env_panels,
        mo.md("&nbsp;"),
        _results,
    ], align="start")
    return


@app.cell
def experiments_physics_slide(mo):
    _heading = mo.Html(
        '<h2 style="margin:0;">Physics Without Supervision</h2>'
    )

    _content = mo.Html(
        '<div style="font-size:1.05rem;line-height:1.9;">'

        '<p style="font-weight:700;margin:0 0 0.3rem 0;">Linear Probing (PushT)</p>'
        '<ul style="list-style:disc;padding-left:1.4rem;margin:0 0 1.2rem 0;">'
        '<li>Can physical quantities be read out from the latent space without any physics supervision?</li>'
        '<li>Frozen encoder + linear layer achieves R² &gt; 0.90 for position and angle, outperforming PLDM</li>'
        '<li>Linear (not non-linear) decoder recovering a quantity means it is stored as an explicit direction in latent space</li>'
        '<li style="list-style:none;padding-left:1rem;font-size:0.88em;color:#444;line-height:2.2;">'
        'R<sup>2</sup> = 1 &minus; '
        '<span style="display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;margin:0 3px;">'
        '<span style="border-bottom:1px solid currentColor;padding:0 4px;">&sum;<sub>i</sub>(y<sub>i</sub> &minus; &#375;<sub>i</sub>)<sup>2</sup></span>'
        '<span style="padding:0 4px;">&sum;<sub>i</sub>(y<sub>i</sub> &minus; &#563;)<sup>2</sup></span>'
        '</span>'
        '</li>'
        '<li style="list-style:none;padding-left:1rem;font-size:0.88em;color:#444;">'
        '&#375;<sub>i</sub> = predicted value &nbsp;&nbsp; &#563; = mean of y &nbsp;&nbsp; R<sup>2</sup> = 1 means perfect prediction'
        '</li>'
        '<li>Physical structure emerges implicitly from the JEPA training objective alone</li>'
        '</ul>'

        '<p style="font-weight:700;margin:0 0 0.3rem 0;">Violation-of-Expectation</p>'
        '<ul style="list-style:disc;padding-left:1.4rem;margin:0;">'
        '<li>Does the model assign higher surprise to physically impossible events than to mere visual changes?</li>'
        '<li>Teleportation (physical violation) causes sharp MSE spikes; color changes (visual-only) do not</li>'
        '<li>LeWM has learned an implicit notion of physical plausibility, not just visual pattern matching</li>'
        '</ul>'

        '</div>'
    )

    mo.vstack([
        section_strip(3),
        page_number(17),
        _heading,
        mo.Html('<div style="height:0.8rem;"></div>'),
        _content,
    ], align="start", gap="1rem")
    return


@app.cell
def outline_recap_after_experiments():
    # Recap shown at the 03 — 04 boundary. Sections 01, 02, and 03 are grayed
    # out (done); 04 is up next.
    def _():
        import marimo as mo

        def _entry(num, title, bullets, *, done=False):
            c = SECTION[num]
            if done:
                title_color, bullet_color, opacity = "#9CA3AF", "#9CA3AF", "0.5"
                mark = '<span style="color:#9CA3AF;">&#10003;</span> '
            else:
                title_color, bullet_color, opacity = c["text"], "#374151", "1"
                mark = ""
            items = "".join(
                f'<li style="margin:0.25rem 0;font-size:1.2rem;color:{bullet_color};">{b}</li>'
                for b in bullets
            )
            return mo.Html(
                f'<div style="padding:0.25rem 0;opacity:{opacity};">'
                f'<div style="font-weight:700;color:{title_color};font-size:1.6rem;margin-bottom:0.3rem;">'
                f'{mark}{title}</div>'
                f'<ul style="margin:0;padding-left:1.1rem;">{items}</ul>'
                f'</div>'
            )

        return mo.vstack(
            [
                mo.md("# Outline"),
                _entry(1, "01 · Background & State of the Art", [
                    "JEPA: predict in latent space, not pixel space",
                    "Representation collapse —the central challenge",
                    "How existing methods solve it and where they fall short",
                ], done=True),
                _entry(2, "02 · LeWorldModel", [
                    "ViT-Tiny encoder + action-conditioned transformer predictor",
                    "SIGReg: one hyperparameter to prevent collapse",
                    "Latent planning via MPC + CEM",
                ], done=True),
                _entry(3, "03 · Experiments", [
                    "Task performance and planning speed across multiple benchmarks",
                    "Physics emerges in latent space",
                ], done=True),
                _entry(4, "04 · Discussion", [
                    "Authors' claims, personal assessment, open questions",
                ]),
            ],
            align="start",
            gap="0.5rem",
        )
    _()
    return


@app.cell
def discussion_slide(mo):
    _DISC = "#8B5CF6"
    _DISC_TEXT = "#4C1D95"

    def _col_header(label, icon):
        return (
            f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1rem;">'
            f'<span style="font-size:2rem;">{icon}</span>'
            f'<span style="font-weight:700;font-size:2rem;color:{_DISC_TEXT};">{label}</span>'
            f'</div>'
        )

    def _bullet(head, body):
        return (
            f'<div style="display:flex;gap:0.7rem;margin:1.2rem 0;line-height:1.5;">'
            f'<span style="color:{_DISC};font-weight:700;flex-shrink:0;margin-top:0.1rem;font-size:1.5rem;">▸</span>'
            f'<span style="font-size:1.5rem;"><strong>{head}</strong>'
            f'<br><span style="font-size:1.3rem;color:#374151;">{body}</span></span>'
            f'</div>'
        )

    _findings_html = (
        _col_header("Key Findings", "◆")
        + _bullet("2 loss terms —no EMA, no frozen encoder",
                  "Stable end-to-end JEPA from pixels; 6 hyperparameters — 1 vs the only existing alternative")
        + _bullet("Zero-shot planning across all task types",
                  "Same model, same hyperparameters: manipulation, navigation, motion planning. All reward-free.")
        + _bullet("Fixed-compute dominance",
                  "Equal FLOP budget: LeWM 90% vs DINO-WM 13% on PushT. Token efficiency becomes planning quality.")
        + _bullet("Regularizer shapes planning geometry",
                  "Gaussian prior produces straight latent trajectories, making CEM search more effective as a side effect")
    )

    _limitations_html = (
        _col_header("Limitations & Future Work", "?")
        + _bullet("CEM doesn't scale to high-DoF",
                  "Zero-order optimizer breaks for robot arms or locomotion")
        + _bullet("Not a foundation model",
                  "Must retrain per environment; no cross-environment or cross-action-space transfer")
        + _bullet("Future: hierarchical world models",
                  "Multi-scale temporal abstraction to move beyond H=5")
        + _bullet("Future: online / interactive learning",
                  "Closing the loop between world model and environment")
    )

    _grid = mo.Html(
        f'<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:10rem;width:100%;align-items:start;">'
        f'<div>{_findings_html}</div>'
        f'<div>{_limitations_html}</div>'
        f'</div>'
    )

    mo.vstack([
        section_strip(4),
        page_number(18),
        mo.md("## Discussion"),
        mo.md("&nbsp;"),
        _grid,
    ], align="start")
    return


@app.cell
def _bib_text_cell():
    BIB_TEXT = """
    @misc{maes_leworldmodel_2026,
    	title = {{LeWorldModel}: {Stable} {End}-to-{End} {Joint}-{Embedding} {Predictive} {Architecture} from {Pixels}},
    	shorttitle = {{LeWorldModel}},
    	url = {http://arxiv.org/abs/2603.19312},
    	doi = {10.48550/arXiv.2603.19312},
    	abstract = {Joint Embedding Predictive Architectures (JEPAs) offer a compelling framework for learning world models in compact latent spaces, yet existing methods remain fragile, relying on complex multi-term losses, exponential moving averages, pre-trained encoders, or auxiliary supervision to avoid representation collapse. In this work, we introduce LeWorldModel (LeWM), the first JEPA that trains stably end-to-end from raw pixels using only two loss terms: a next-embedding prediction loss and a regularizer enforcing Gaussian-distributed latent embeddings. This reduces tunable loss hyperparameters from six to one compared to the only existing end-to-end alternative. With {\\textasciitilde}15M parameters trainable on a single GPU in a few hours, LeWM plans up to 48x faster than foundation-model-based world models while remaining competitive across diverse 2D and 3D control tasks. Beyond control, we show that LeWM's latent space encodes meaningful physical structure through probing of physical quantities. Surprise evaluation confirms that the model reliably detects physically implausible events.},
    	urldate = {2026-04-29},
    	publisher = {arXiv},
    	author = {Maes, Lucas and Lidec, Quentin Le and Scieur, Damien and LeCun, Yann and Balestriero, Randall},
    	month = mar,
    	year = {2026},
    	note = {arXiv:2603.19312 [cs]},
    	keywords = {Computer Science - Artificial Intelligence, Computer Science - Machine Learning},
    	file = {Full Text PDF:/Users/julian/Zotero/storage/JXWAAKII/Maes et al. - 2026 - LeWorldModel Stable End-to-End Joint-Embedding Predictive Architecture from Pixels.pdf:application/pdf;Snapshot:/Users/julian/Zotero/storage/RCDFNTWS/2603.html:text/html},
    }

    @article{lecun_path_nodate,
    	title = {A {Path} {Towards} {Autonomous} {Machine} {Intelligence} {Version} 0.9.2, 2022-06-27},
    	abstract = {How could machines learn as eﬃciently as humans and animals? How could machines learn to reason and plan? How could machines learn representations of percepts and action plans at multiple levels of abstraction, enabling them to reason, predict, and plan at multiple time horizons? This position paper proposes an architecture and training paradigms with which to construct autonomous intelligent agents. It combines concepts such as conﬁgurable predictive world model, behavior driven through intrinsic motivation, and hierarchical joint embedding architectures trained with self-supervised learning.},
    	language = {en},
    	author = {LeCun, Yann},
    	file = {PDF:/Users/julian/Zotero/storage/3GY34T4M/LeCun - A Path Towards Autonomous Machine Intelligence Version 0.9.2, 2022-06-27.pdf:application/pdf},
    }

    @misc{chen_vl-jepa_2026,
    	title = {{VL}-{JEPA}: {Joint} {Embedding} {Predictive} {Architecture} for {Vision}-language},
    	shorttitle = {{VL}-{JEPA}},
    	url = {http://arxiv.org/abs/2512.10942},
    	doi = {10.48550/arXiv.2512.10942},
    	abstract = {We introduce VL-JEPA, a vision-language model built on a Joint Embedding Predictive Architecture (JEPA). Instead of autoregressively generating tokens as in classical VLMs, VL-JEPA predicts continuous embeddings of the target texts. By learning in an abstract representation space, the model focuses on task-relevant semantics while abstracting away surface-level linguistic variability. In a strictly controlled comparison against standard token-space VLM training with the same vision encoder and training data, VL-JEPA achieves stronger performance while having 50\\% fewer trainable parameters. At inference time, a lightweight text decoder is invoked only when needed to translate VL-JEPA predicted embeddings into text. We show that VL-JEPA natively supports selective decoding that reduces the number of decoding operations by 2.85x while maintaining similar performance compared to non-adaptive uniform decoding. Beyond generation, the VL-JEPA's embedding space naturally supports open-vocabulary classification, text-to-video retrieval, and discriminative VQA without any architecture modification. On eight video classification and eight video retrieval datasets, the average performance VL-JEPA surpasses that of CLIP, SigLIP2, and Perception Encoder. At the same time, the model achieves comparable performance as classical VLMs (InstructBLIP, QwenVL) on four VQA datasets: GQA, TallyQA, POPE and POPEv2, despite only having 1.6B parameters.},
    	urldate = {2026-05-04},
    	publisher = {arXiv},
    	author = {Chen, Delong and Shukor, Mustafa and Moutakanni, Theo and Chung, Willy and Yu, Jade and Kasarla, Tejaswi and Bang, Yejin and Bolourchi, Allen and LeCun, Yann and Fung, Pascale},
    	month = feb,
    	year = {2026},
    	note = {arXiv:2512.10942 [cs]},
    	keywords = {Computer Science - Computer Vision and Pattern Recognition},
    	file = {Full Text PDF:/Users/julian/Zotero/storage/ZI44Y5XT/Chen et al. - 2026 - VL-JEPA Joint Embedding Predictive Architecture for Vision-language.pdf:application/pdf;Snapshot:/Users/julian/Zotero/storage/7PYUYUH7/2512.html:text/html},
    }

    @misc{balestriero_lejepa_2025,
    	title = {{LeJEPA}: {Provable} and {Scalable} {Self}-{Supervised} {Learning} {Without} the {Heuristics}},
    	shorttitle = {{LeJEPA}},
    	url = {http://arxiv.org/abs/2511.08544},
    	doi = {10.48550/arXiv.2511.08544},
    	abstract = {Learning manipulable representations of the world and its dynamics is central to AI. Joint-Embedding Predictive Architectures (JEPAs) offer a promising blueprint, but lack of practical guidance and theory has led to ad-hoc R\\&D. We present a comprehensive theory of JEPAs and instantiate it in \\{{\\textbackslash}bf LeJEPA\\}, a lean, scalable, and theoretically grounded training objective. First, we identify the isotropic Gaussian as the optimal distribution that JEPAs' embeddings should follow to minimize downstream prediction risk. Second, we introduce a novel objective--\\{{\\textbackslash}bf Sketched Isotropic Gaussian Regularization\\} (SIGReg)--to constrain embeddings to reach that ideal distribution. Combining the JEPA predictive loss with SIGReg yields LeJEPA with numerous theoretical and practical benefits: (i) single trade-off hyperparameter, (ii) linear time and memory complexity, (iii) stability across hyper-parameters, architectures (ResNets, ViTs, ConvNets) and domains, (iv) heuristics-free, e.g., no stop-gradient, no teacher-student, no hyper-parameter schedulers, and (v) distributed training-friendly implementation requiring only \\${\\textbackslash}approx\\$50 lines of code. Our empirical validation covers 10+ datasets, 60+ architectures, all with varying scales and domains. As an example, using imagenet-1k for pretraining and linear evaluation with frozen backbone, LeJEPA reaches 79{\\textbackslash}\\% with a ViT-H/14. We hope that the simplicity and theory-friendly ecosystem offered by LeJEPA will reestablish self-supervised pre-training as a core pillar of AI research ({\\textbackslash}href\\{https://github.com/rbalestr-lab/lejepa\\}\\{GitHub repo\\}).},
    	urldate = {2026-05-04},
    	publisher = {arXiv},
    	author = {Balestriero, Randall and LeCun, Yann},
    	month = nov,
    	year = {2025},
    	note = {arXiv:2511.08544 [cs]},
    	keywords = {Computer Science - Artificial Intelligence, Computer Science - Computer Vision and Pattern Recognition, Computer Science - Machine Learning, Statistics - Machine Learning},
    	file = {Full Text PDF:/Users/julian/Zotero/storage/9DKKPNNA/Balestriero and LeCun - 2025 - LeJEPA Provable and Scalable Self-Supervised Learning Without the Heuristics.pdf:application/pdf;Snapshot:/Users/julian/Zotero/storage/RUB3Z3RV/2511.html:text/html},
    }

    @article{matsuo_deep_2022,
    	title = {Deep learning, reinforcement learning, and world models},
    	volume = {152},
    	issn = {08936080},
    	url = {https://linkinghub.elsevier.com/retrieve/pii/S0893608022001150},
    	doi = {10.1016/j.neunet.2022.03.037},
    	abstract = {Deep learning (DL) and reinforcement learning (RL) methods seem to be a part of indispensable factors to achieve human-level or super-human AI systems. On the other hand, both DL and RL have strong connections with our brain functions and with neuroscientific findings. In this review, we summarize talks and discussions in the ‘‘Deep Learning and Reinforcement Learning’’ session of the symposium, International Symposium on Artificial Intelligence and Brain Science. In this session, we discussed whether we can achieve comprehensive understanding of human intelligence based on the recent advances of deep learning and reinforcement learning algorithms. Speakers contributed to provide talks about their recent studies that can be key technologies to achieve human-level intelligence.},
    	language = {en},
    	urldate = {2026-05-04},
    	journal = {Neural Networks},
    	author = {Matsuo, Yutaka and LeCun, Yann and Sahani, Maneesh and Precup, Doina and Silver, David and Sugiyama, Masashi and Uchibe, Eiji and Morimoto, Jun},
    	month = aug,
    	year = {2022},
    	pages = {267--275},
    	file = {PDF:/Users/julian/Zotero/storage/J245CKJR/Matsuo et al. - 2022 - Deep learning, reinforcement learning, and world models.pdf:application/pdf},
    }

    @misc{nam_causal-jepa_2026,
    	title = {Causal-{JEPA}: {Learning} {World} {Models} through {Object}-{Level} {Latent} {Interventions}},
    	shorttitle = {Causal-{JEPA}},
    	url = {http://arxiv.org/abs/2602.11389},
    	doi = {10.48550/arXiv.2602.11389},
    	abstract = {World models require robust relational understanding to support prediction, reasoning, and control. While object-centric representations provide a useful abstraction, they are not sufficient to capture interaction-dependent dynamics. We therefore propose C-JEPA, a simple and flexible object-centric world model that extends masked joint embedding prediction from image patches to object-centric representations. By applying object-level masking that requires an object's state to be inferred from other objects, C-JEPA induces latent interventions with counterfactual-like effects and prevents shortcut solutions, making interaction reasoning essential. Empirically, C-JEPA leads to consistent gains in visual question answering, with an absolute improvement of about 20{\\textbackslash}\\% in counterfactual reasoning compared to the same architecture without object-level masking. On agent control tasks, C-JEPA enables substantially more efficient planning by using only 1{\\textbackslash}\\% of the total latent input features required by patch-based world models, while achieving comparable performance. Finally, we provide a formal analysis demonstrating that object-level masking induces a causal inductive bias via latent interventions. Our code is available at https://github.com/galilai-group/cjepa.},
    	urldate = {2026-05-04},
    	publisher = {arXiv},
    	author = {Nam, Heejeong and Lidec, Quentin Le and Maes, Lucas and LeCun, Yann and Balestriero, Randall},
    	month = feb,
    	year = {2026},
    	note = {arXiv:2602.11389 [cs]},
    	keywords = {Computer Science - Artificial Intelligence},
    	file = {Full Text PDF:/Users/julian/Zotero/storage/YAFY2CD9/Nam et al. - 2026 - Causal-JEPA Learning World Models through Object-Level Latent Interventions.pdf:application/pdf;Snapshot:/Users/julian/Zotero/storage/F9MMYMUE/2602.html:text/html},
    }

    @article{ha_world_2018,
    	title = {World {Models}},
    	url = {http://arxiv.org/abs/1803.10122},
    	doi = {10.5281/zenodo.1207631},
    	abstract = {We explore building generative neural network models of popular reinforcement learning environments. Our world model can be trained quickly in an unsupervised manner to learn a compressed spatial and temporal representation of the environment. By using features extracted from the world model as inputs to an agent, we can train a very compact and simple policy that can solve the required task. We can even train our agent entirely inside of its own hallucinated dream generated by its world model, and transfer this policy back into the actual environment. An interactive version of this paper is available at https://worldmodels.github.io/},
    	urldate = {2026-05-04},
    	author = {Ha, David and Schmidhuber, Jürgen},
    	month = mar,
    	year = {2018},
    	note = {arXiv:1803.10122 [cs]},
    	keywords = {Computer Science - Machine Learning, Statistics - Machine Learning},
    	file = {Full Text PDF:/Users/julian/Zotero/storage/B844DNWA/Ha and Schmidhuber - 2018 - World Models.pdf:application/pdf;Snapshot:/Users/julian/Zotero/storage/ST4PC9YM/1803.html:text/html},
    }

    @inproceedings{bromley_signature_1993,
    	title = {Signature {Verification} using a "{Siamese}" {Time} {Delay} {Neural} {Network}},
    	volume = {6},
    	url = {https://proceedings.neurips.cc/paper_files/paper/1993/hash/288cc0ff022877bd3df94bc9360b9c5d-Abstract.html},
    	urldate = {2026-05-05},
    	booktitle = {Advances in {Neural} {Information} {Processing} {Systems}},
    	publisher = {Morgan-Kaufmann},
    	author = {Bromley, Jane and Guyon, Isabelle and LeCun, Yann and Säckinger, Eduard and Shah, Roopak},
    	year = {1993},
    	file = {Full Text PDF:/Users/julian/Zotero/storage/PKF36WS9/Bromley et al. - 1993 - Signature Verification using a Siamese Time Delay Neural Network.pdf:application/pdf},
    }

    @misc{assran_v-jepa_2025,
    	title = {V-{JEPA} 2: {Self}-{Supervised} {Video} {Models} {Enable} {Understanding}, {Prediction} and {Planning}},
    	shorttitle = {V-{JEPA} 2},
    	url = {http://arxiv.org/abs/2506.09985},
    	doi = {10.48550/arXiv.2506.09985},
    	abstract = {A major challenge for modern AI is to learn to understand the world and learn to act largely by observation. This paper explores a self-supervised approach that combines internet-scale video data with a small amount of interaction data (robot trajectories), to develop models capable of understanding, predicting, and planning in the physical world. We first pre-train an action-free joint-embedding-predictive architecture, V-JEPA 2, on a video and image dataset comprising over 1 million hours of internet video. V-JEPA 2 achieves strong performance on motion understanding (77.3 top-1 accuracy on Something-Something v2) and state-of-the-art performance on human action anticipation (39.7 recall-at-5 on Epic-Kitchens-100) surpassing previous task-specific models. Additionally, after aligning V-JEPA 2 with a large language model, we demonstrate state-of-the-art performance on multiple video question-answering tasks at the 8 billion parameter scale (e.g., 84.0 on PerceptionTest, 76.9 on TempCompass). Finally, we show how self-supervised learning can be applied to robotic planning tasks by post-training a latent action-conditioned world model, V-JEPA 2-AC, using less than 62 hours of unlabeled robot videos from the Droid dataset. We deploy V-JEPA 2-AC zero-shot on Franka arms in two different labs and enable picking and placing of objects using planning with image goals. Notably, this is achieved without collecting any data from the robots in these environments, and without any task-specific training or reward. This work demonstrates how self-supervised learning from web-scale data and a small amount of robot interaction data can yield a world model capable of planning in the physical world.},
    	urldate = {2026-05-06},
    	publisher = {arXiv},
    	author = {Assran, Mido and Bardes, Adrien and Fan, David and Garrido, Quentin and Howes, Russell and Komeili, Mojtaba and Muckley, Matthew and Rizvi, Ammar and Roberts, Claire and Sinha, Koustuv and Zholus, Artem and Arnaud, Sergio and Gejji, Abha and Martin, Ada and Hogan, Francois Robert and Dugas, Daniel and Bojanowski, Piotr and Khalidov, Vasil and Labatut, Patrick and Massa, Francisco and Szafraniec, Marc and Krishnakumar, Kapil and Li, Yong and Ma, Xiaodong and Chandar, Sarath and Meier, Franziska and LeCun, Yann and Rabbat, Michael and Ballas, Nicolas},
    	month = jun,
    	year = {2025},
    	note = {arXiv:2506.09985 [cs]},
    	keywords = {Computer Science - Artificial Intelligence, Computer Science - Robotics, Computer Science - Computer Vision and Pattern Recognition, Computer Science - Machine Learning},
    	file = {Full Text PDF:/Users/julian/Zotero/storage/JI95FUI6/Assran et al. - 2025 - V-JEPA 2 Self-Supervised Video Models Enable Understanding, Prediction and Planning.pdf:application/pdf;Snapshot:/Users/julian/Zotero/storage/GQTKDXV9/2506.html:text/html},
    }

    @misc{assran_i-jepa_2023,
    	title = {Self-{Supervised} {Learning} from {Images} with a {Joint}-{Embedding} {Predictive} {Architecture}},
    	shorttitle = {I-{JEPA}},
    	url = {http://arxiv.org/abs/2301.08243},
    	doi = {10.48550/arXiv.2301.08243},
    	publisher = {arXiv},
    	author = {Assran, Mahmoud and Duval, Quentin and Misra, Ishan and Bojanowski, Piotr and Vincent, Pascal and Rabbat, Michael and LeCun, Yann and Ballas, Nicolas},
    	year = {2023},
    	note = {arXiv:2301.08243 [cs]. CVPR 2023},
    }

    @misc{bardes_v-jepa_2024,
    	title = {Revisiting {Feature} {Prediction} for {Learning} {Visual} {Representations} from {Video}},
    	shorttitle = {V-{JEPA}},
    	url = {http://arxiv.org/abs/2404.08471},
    	doi = {10.48550/arXiv.2404.08471},
    	publisher = {arXiv},
    	author = {Bardes, Adrien and Garrido, Quentin and Ponce, Jean and Chen, Xinlei and Rabbat, Michael and LeCun, Yann and Assran, Mahmoud and Ballas, Nicolas},
    	year = {2024},
    	note = {arXiv:2404.08471 [cs]},
    }

    @misc{munim_echojepa_2026,
    	title = {{EchoJEPA}: {A} {Latent} {Predictive} {Foundation} {Model} for {Echocardiography}},
    	shorttitle = {{EchoJEPA}},
    	url = {http://arxiv.org/abs/2602.02603},
    	doi = {10.48550/arXiv.2602.02603},
    	publisher = {arXiv},
    	author = {Munim, Alif and Fallahpour, Adibvafa and Szasz, Teodora and Attarpour, Ahmadreza and Jiang, River and Sooriyakanthan, Brana and Sooriyakanthan, Maala and Whitney, Heather and Slivnick, Jeremy and Rubin, Barry and Tsang, Wendy and Wang, Bo},
    	year = {2026},
    	note = {arXiv:2602.02603 [cs]},
    }

    @misc{dong_brain-jepa_2024,
    	title = {Brain-{JEPA}: {Brain} {Dynamics} {Foundation} {Model} with {Gradient} {Positioning} and {Spatiotemporal} {Masking}},
    	shorttitle = {Brain-{JEPA}},
    	url = {http://arxiv.org/abs/2409.19407},
    	doi = {10.48550/arXiv.2409.19407},
    	publisher = {arXiv},
    	author = {Dong, Zijian and Li, Ruilin and Wu, Yilei and Nguyen, Thuan Tinh and Chong, Joanna Su Xian and Ji, Fang and Tong, Nathanael Ren Jie and Chen, Christopher Li Hsian and Zhou, Juan Helen},
    	year = {2024},
    	note = {arXiv:2409.19407 [cs]. NeurIPS 2024},
    }

    @misc{micheli_iris_2023,
    	title = {Transformers are {Sample}-{Efficient} {World} {Models}},
    	shorttitle = {{IRIS}},
    	url = {http://arxiv.org/abs/2209.00588},
    	doi = {10.48550/arXiv.2209.00588},
    	publisher = {arXiv},
    	author = {Micheli, Vincent and Alonso, Eloi and Fleuret, François},
    	year = {2023},
    	note = {arXiv:2209.00588 [cs]. ICLR 2023},
    }

    @misc{alonso_diamond_2024,
    	title = {Diffusion for {World} {Modeling}: {Visual} {Details} {Matter} in {Atari}},
    	shorttitle = {{DIAMOND}},
    	url = {http://arxiv.org/abs/2405.12399},
    	doi = {10.48550/arXiv.2405.12399},
    	publisher = {arXiv},
    	author = {Alonso, Eloi and Jelley, Adam and Micheli, Vincent and Kanervisto, Anssi and Storkey, Amos and Pearce, Tim and Fleuret, François},
    	year = {2024},
    	note = {arXiv:2405.12399 [cs]. NeurIPS 2024},
    }

    @misc{decart_oasis_2024,
    	title = {Oasis: {A} {Universe} in a {Transformer}},
    	shorttitle = {Oasis},
    	url = {https://oasis-model.github.io/},
    	author = {{Decart} and {Etched}},
    	year = {2024},
    	note = {Interactive diffusion-transformer world model},
    }

    @misc{hafner_dreamer4_2025,
    	title = {Training {Agents} {Inside} of {Scalable} {World} {Models}},
    	shorttitle = {Dreamer 4},
    	url = {http://arxiv.org/abs/2509.24527},
    	doi = {10.48550/arXiv.2509.24527},
    	publisher = {arXiv},
    	author = {Hafner, Danijar and Yan, Wilson and Lillicrap, Timothy},
    	year = {2025},
    	note = {arXiv:2509.24527 [cs]},
    }

    @misc{bruce_genie_2024,
    	title = {Genie: {Generative} {Interactive} {Environments}},
    	shorttitle = {Genie},
    	url = {http://arxiv.org/abs/2402.15391},
    	doi = {10.48550/arXiv.2402.15391},
    	publisher = {arXiv},
    	author = {Bruce, Jake and Dennis, Michael and Edwards, Ashley and Parker-Holder, Jack and Shi, Yuge and others},
    	year = {2024},
    	note = {arXiv:2402.15391 [cs]. ICML 2024},
    }

    @misc{zhou_dino-wm_2024,
    	title = {{DINO}-{WM}: {World} {Models} on {Pre}-trained {Visual} {Features} enable {Zero}-shot {Planning}},
    	shorttitle = {{DINO}-{WM}},
    	url = {http://arxiv.org/abs/2411.04983},
    	doi = {10.48550/arXiv.2411.04983},
    	publisher = {arXiv},
    	author = {Zhou, Gaoyue and Pan, Hengkai and LeCun, Yann and Pinto, Lerrel},
    	year = {2024},
    	note = {arXiv:2411.04983 [cs]},
    }

    @misc{sobal_pldm_2025,
    	title = {Learning from {Reward}-{Free} {Offline} {Data}: {A} {Case} for {Planning} with {Latent} {Dynamics} {Models}},
    	shorttitle = {{PLDM}},
    	url = {http://arxiv.org/abs/2502.14819},
    	doi = {10.48550/arXiv.2502.14819},
    	publisher = {arXiv},
    	author = {Sobal, Vlad and Zhang, Wancong and Cho, Kyunghyun and Balestriero, Randall and Rudner, Tim G. J. and LeCun, Yann},
    	year = {2025},
    	note = {arXiv:2502.14819 [cs]},
    }

    @misc{ba_layer_normalization_2016,
    	title = {Layer {Normalization}},
    	url = {http://arxiv.org/abs/1607.06450},
    	publisher = {arXiv},
    	author = {Ba, Jimmy Lei and Kiros, Jamie Ryan and Hinton, Geoffrey E.},
    	year = {2016},
    	note = {arXiv:1607.06450 [cs]},
    }

    @misc{peebles_dit_2022,
    	title = {Scalable {Diffusion} {Models} with {Transformers}},
    	url = {http://arxiv.org/abs/2212.09748},
    	publisher = {arXiv},
    	author = {Peebles, William and Xie, Saining},
    	year = {2022},
    	note = {arXiv:2212.09748 [cs]},
    }

    @inproceedings{dosovitskiy_vit_2021,
    	title = {An {Image} is {Worth} 16x16 {Words}: {Transformers} for {Image} {Recognition} at {Scale}},
    	url = {http://arxiv.org/abs/2010.11929},
    	booktitle = {International {Conference} on {Learning} {Representations} ({ICLR})},
    	author = {Dosovitskiy, Alexey and Beyer, Lucas and Kolesnikov, Alexander and Weissenborn, Dirk and Zhai, Xiaohua and Unterthiner, Thomas and Dehghani, Mostafa and Minderer, Matthias and Heigold, Georg and Gelly, Sylvain and Uszkoreit, Jakob and Houlsby, Neil},
    	year = {2021},
    	note = {arXiv:2010.11929},
    }

    @misc{bardes_vicreg_2022,
    	title = {{VICReg}: {Variance}-{Invariance}-{Covariance} {Regularization} for {Self}-{Supervised} {Learning}},
    	shorttitle = {{VICReg}},
    	url = {http://arxiv.org/abs/2105.04906},
    	doi = {10.48550/arXiv.2105.04906},
    	publisher = {arXiv},
    	author = {Bardes, Adrien and Ponce, Jean and LeCun, Yann},
    	year = {2022},
    	note = {arXiv:2105.04906 [cs]. ICLR 2022},
    }
    """
    return (BIB_TEXT,)


@app.cell
def bibliography_slide_1(BIB_TEXT, mo):
    def _():
        import bibtexparser

        ENTRIES_PER_PAGE = 8

        import io
        parser = bibtexparser.bparser.BibTexParser(common_strings=True)
        db = bibtexparser.load(io.StringIO(BIB_TEXT), parser=parser)

        # Only the works cited in the slides, numbered by their position in CITED.
        by_key = {e.get("ID"): e for e in db.entries}
        cited_entries = [(i, by_key[k]) for i, k in enumerate(CITED, 1) if k in by_key]

        items = "".join(format_ref_ieee(i, e) for i, e in cited_entries[:ENTRIES_PER_PAGE])
        return mo.vstack([
            page_number(19),
            mo.Html(f'<h2 style="margin-bottom:0.5rem;">References</h2>{items}'),
        ], align="start")

    _()
    return


@app.cell
def bibliography_slide_2(BIB_TEXT, mo):
    def _():
        import bibtexparser

        ENTRIES_PER_PAGE = 8

        import io
        parser = bibtexparser.bparser.BibTexParser(common_strings=True)
        db = bibtexparser.load(io.StringIO(BIB_TEXT), parser=parser)

        # Only the works cited in the slides, numbered by their position in CITED.
        by_key = {e.get("ID"): e for e in db.entries}
        cited_entries = [(i, by_key[k]) for i, k in enumerate(CITED, 1) if k in by_key]
        page_entries = cited_entries[ENTRIES_PER_PAGE:]
        mo.stop(not page_entries)

        items = "".join(format_ref_ieee(i, e) for i, e in page_entries)
        return mo.vstack([
            page_number(20),
            mo.Html(f'<h2 style="margin-bottom:0.5rem;">References (cont.)</h2>{items}'),
        ], align="start")

    _()
    return


if __name__ == "__main__":
    app.run()
