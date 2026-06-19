# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.23.6",
# ]
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(
    width="full",
    app_title="World Models Seminar",
    layout_file="layouts/presentation.slides.json",
)


@app.cell
def _():
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

    # Structured metadata for each cited key: (short name, authors, year, venue).
    # Venue is empty string for arXiv-only preprints.
    REFS = {
        "maes_leworldmodel_2026":       ("LeWM",        "Maes et al.",          2026, ""),
        "assran_i-jepa_2023":           ("I-JEPA",      "Assran et al.",        2023, "CVPR"),
        "bardes_v-jepa_2024":           ("V-JEPA",      "Bardes et al.",        2024, ""),
        "assran_v-jepa_2025":           ("V-JEPA 2",    "Assran et al.",        2025, ""),
        "munim_echojepa_2026":          ("Echo-JEPA",   "Munim et al.",         2026, ""),
        "dong_brain-jepa_2024":         ("Brain-JEPA",  "Dong et al.",          2024, "NeurIPS"),
        "micheli_iris_2023":            ("IRIS",        "Micheli et al.",       2023, "ICLR"),
        "alonso_diamond_2024":          ("DIAMOND",     "Alonso et al.",        2024, "NeurIPS"),
        "decart_oasis_2024":            ("OASIS",       "Decart & Etched",      2024, ""),
        "hafner_dreamer4_2025":         ("DreamerV4",   "Hafner et al.",        2025, ""),
        "bruce_genie_2024":             ("Genie",       "Bruce et al.",         2024, "ICML"),
        "zhou_dino-wm_2024":            ("DINO-WM",     "Zhou et al.",          2024, ""),
        "sobal_pldm_2025":              ("PLDM",        "Sobal et al.",         2025, ""),
        "bardes_vicreg_2022":           ("VICReg",      "Bardes et al.",        2022, "ICLR"),
        "dosovitskiy_vit_2021":         ("ViT",         "Dosovitskiy et al.",   2021, "ICLR"),
        "ba_layer_normalization_2016":  ("LayerNorm",   "Ba et al.",            2016, ""),
        "peebles_dit_2022":             ("DiT",         "Peebles & Xie",        2023, "ICCV"),
        "balestriero_lejepa_2025":      ("LeJEPA",      "Balestriero & LeCun",  2025, ""),
        "grill_byol_2020":              ("BYOL",        "Grill et al.",         2020, "NeurIPS"),
    }

    def cite_compact(key):
        # Space-constrained inline citation: Name — Authors (Venue Year)
        if key not in REFS:
            return ""
        short, authors, year, venue = REFS[key]
        year_str = f"{venue} {year}" if venue else str(year)
        return f"{short} — {authors} ({year_str})"

    def cite_full(key):
        # Full inline citation: "Name" — Authors, Venue Year
        if key not in REFS:
            return ""
        short, authors, year, venue = REFS[key]
        year_str = f"{venue} {year}" if venue else str(year)
        return f'"{short}"" — {authors}, {year_str}'

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
                f'<video autoplay muted controls style="{VIDEO_STYLE}">'
                f'<source src="data:video/mp4;base64,{_b64}" type="video/mp4">'
                f'</video>'
            )
        else:
            # WASM: video served as a static file copied alongside the HTML in CI
            _rel = f"media/videos/{_source_stem}/{_res_dir}/{_scene_name}.mp4"
            import marimo as mo
            return mo.Html(
                f'<video autoplay muted controls style="{VIDEO_STYLE}">'
                f'<source src="{_rel}" type="video/mp4">'
                f'</video>'
            )

    return (
        SECTION,
        VIDEO_STYLE,
        cite_compact,
        page_number,
        render_scene,
        sota_table,
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
                "video::-webkit-media-controls-panel { background: transparent !important; -webkit-backdrop-filter: none !important; backdrop-filter: none !important; }"
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
def outline_slide(SECTION):
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
                    "Representation collapse: The central challenge",
                    "How existing methods solve it and where they fall short",
                    "Taxonomy of world models",
                ]),
                _entry(2, "02 · LeWorldModel", [
                    "ViT-Tiny encoder + action-conditioned transformer predictor",
                    "SIGReg: One hyperparameter to prevent collapse",
                    "Latent planning via MPC + CEM",
                ]),
                _entry(3, "03 · Experiments", [
                    "Task performance and planning speed across multiple benchmarks",
                    "Violation of Expectation: Physics structure in latent space",
                ]),
                _entry(4, "04 · Discussion", [
                    "Key findings and authors' claims",
                    "Limitations & future directions",
                ]),
            ],
            align="start",
            gap="0.5rem",
        )
    _()
    return


@app.cell
def jepa_principle_animation_slide(VIDEO_STYLE, page_number, render_scene):
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
            f'<video autoplay muted controls style="{VIDEO_STYLE}">'
            '<source src="media/videos/jepa_training/1080p60/JEPATraining.mp4" type="video/mp4">'
            '</video>'
        )
    _credit = _mo.Html(
        '<p style="font-size:0.7rem;color:#888;text-align:right;margin-top:0.25rem;">'
        'Adapted from: <a href="https://youtu.be/kYkIdXwW2AE" '
        'target="_blank" style="color:#888;">Yann LeCun\'s $1B Bet Against LLMs [Part 1]</a>'
        '</p>'
    )
    _mo.vstack([page_number(1), _video, _credit])
    return


@app.cell
def representation_collapse_question(page_number):
    def _():
        import sys
        import marimo as mo

        if sys.platform != "emscripten":
            import pathlib
            img_src = (pathlib.Path(__file__).parent / "media/images/jepa_final_frame.png").read_bytes()
        else:
            img_src = "media/images/jepa_final_frame.png"

        return mo.vstack([

            page_number(2),
            mo.hstack(
                [
                    mo.vstack(
                        [
                            mo.md("## Representation Collapse"),
                            mo.md("*The Core Problem of JEPA-Based Architectures*"),
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
def representation_collapse_answer(page_number):
    def _():
        import sys
        import marimo as mo

        if sys.platform != "emscripten":
            import pathlib
            img_src = (pathlib.Path(__file__).parent / "media/images/jepa_final_frame.png").read_bytes()
        else:
            img_src = "media/images/jepa_final_frame.png"

        return mo.vstack([

            page_number(3),
            mo.hstack(
                [
                    mo.vstack(
                        [
                            mo.md("## Representation Collapse"),
                            mo.md("*The Core Problem of JEPA-Based Architectures*"),
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
def sota_anticollapse_slide(cite_compact, page_number, sota_table):
    def _():
        import marimo as mo
        return mo.vstack([

            page_number(4),
            mo.md("## State of the Art by *Anti-Collapse Strategy*"),
            mo.md("&nbsp;"),
            sota_table(
                ["Strategy", "Mechanism", "Limitation"],
                [
                    [f'EMA + stop-gradient<br><small style="color:#64748B;">{cite_compact("grill_byol_2020")}</small>',
                     "Asymmetric self-distillation from a moving-average teacher",
                     "No well-defined objective, purely heuristic"],
                    [f'Frozen pretrained encoder<br><small style="color:#64748B;">{cite_compact("zhou_dino-wm_2024")}</small>',
                     "Encoder is fixed, so it cannot collapse",
                     "Bounded by pretraining knowledge; not end-to-end"],
                    [f'Explicit regularization<br><small style="color:#64748B;">{cite_compact("bardes_vicreg_2022")} &ensp; {cite_compact("sobal_pldm_2025")}</small>',
                     "Variance / covariance penalty terms",
                     "Training instabilities; up to 6 loss hyperparameters"],
                ],
            ),
        ], align="start")
    _()
    return


@app.cell
def sota_target_task_slide(VIDEO_STYLE, page_number, render_scene):
    import sys as _sys
    import marimo as _mo
    if _sys.platform != "emscripten":
        _sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
        from animations.world_model_taxonomy import WorldModelTaxonomy
        _video = render_scene(WorldModelTaxonomy)
    else:
        _video = _mo.Html(
            f'<video autoplay muted controls style="{VIDEO_STYLE}">'
            '<source src="media/videos/world_model_taxonomy/1080p60/WorldModelTaxonomy.mp4" type="video/mp4">'
            '</video>'
        )
    _credit = _mo.Html(
        '<p style="font-size:0.7rem;color:#888;text-align:right;margin-top:0.25rem;">'
        'Adapted from: <a href="https://drfeifei.substack.com/p/a-functional-taxonomy-of-world-models" '
        'target="_blank" style="color:#888;">A Functional Taxonomy of World Models — Fei-Fei Li</a>'
        '</p>'
    )
    _mo.vstack([page_number(5), _video, _credit])
    return


@app.cell
def outline_recap_after_sota(SECTION):
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
                    "Representation collapse: The central challenge",
                    "How existing methods solve it and where they fall short",
                    "Taxonomy of world models",
                ], done=True),
                _entry(2, "02 · LeWorldModel", [
                    "ViT-Tiny encoder + action-conditioned transformer predictor",
                    "SIGReg: One hyperparameter to prevent collapse",
                    "Latent planning via MPC + CEM",
                ]),
                _entry(3, "03 · Experiments", [
                    "Task performance and planning speed across multiple benchmarks",
                    "Violation of Expectation: Physics structure in latent space",
                ]),
                _entry(4, "04 · Discussion", [
                    "Key findings and authors' claims",
                    "Limitations & future directions",
                ]),
            ],
            align="start",
            gap="0.5rem",
        )
    _()
    return


@app.cell
def lewm_architecture_animation_slide(VIDEO_STYLE, page_number, render_scene):
    import sys as _sys
    import marimo as _mo
    if _sys.platform != "emscripten":
        _sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
        from animations.lewm_architecture import LeWMArchitecture
        _video = render_scene(LeWMArchitecture)
    else:
        _video = _mo.Html(
            f'<video autoplay muted controls style="{VIDEO_STYLE}">'
            '<source src="media/videos/lewm_architecture/1080p60/LeWMArchitecture.mp4" type="video/mp4">'
            '</video>'
        )
    _mo.vstack([page_number(7), _video])
    return


@app.cell
def vit_encoder_slide(VIDEO_STYLE, mo, page_number):
    import sys as _sys
    import base64 as _base64
    import pathlib as _pathlib
    _mp4 = _pathlib.Path(__file__).parent / "media/videos/vit_tiny_encoder/1080p60/ViTTinyEncoder.mp4"
    if _sys.platform != "emscripten" and _mp4.exists():
        _b64 = _base64.b64encode(_mp4.read_bytes()).decode()
        _video = mo.Html(
            f'<video autoplay muted controls style="{VIDEO_STYLE}">'
            f'<source src="data:video/mp4;base64,{_b64}" type="video/mp4">'
            f'</video>'
        )
    else:
        _video = mo.Html(
            f'<video autoplay muted controls style="{VIDEO_STYLE}">'
            '<source src="media/videos/vit_tiny_encoder/1080p60/ViTTinyEncoder.mp4" type="video/mp4">'
            '</video>'
        )

    mo.vstack([

        page_number(8),
        _video,
        mo.Html(
            '<p style="font-size:0.7rem;color:#888;text-align:right;margin-top:0.25rem;">'
            '"An Image is Worth 16×16 Words: Transformers for Image Recognition at Scale"'
            ' — Dosovitskiy et al., ICLR 2021'
            '</p>'
        ),
    ])
    return


@app.cell
def adaln_formulas_slide(mo, page_number):
    import sys as _sys
    import pathlib as _pathlib

    _ACTION = "#8E6FBF"

    _heading = mo.Html(
        f'<div style="display:flex;align-items:center;gap:0.6rem;">'
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:1.7rem;height:1.7rem;border-radius:50%;background:{_ACTION};'
        f'color:white;font-weight:700;font-size:1.1rem;flex-shrink:0;">2</span>'
        f'<h2 style="margin:0;line-height:1.2;">Injecting Actions via Layer Normalization</h2>'
        f'</div>'
    )

    _adaptive_ln = mo.vstack([
        mo.Html(f'<h3 style="margin:0 0 0.3rem 0;color:#334155;">AdaLN-Zero &nbsp;<span style="font-size:0.8rem;font-weight:400;color:#64748B;">Peebles &amp; Xie, &ldquo;Scalable Diffusion Models with Transformers&rdquo;, ICCV 2023</span></h3>'),
        mo.md(r"$$y = \underbrace{(1+\Sigma(a))}_{\text{scale}} \cdot \frac{x-\mu}{\sigma} + \underbrace{\Delta(a)}_{\text{shift}}$$"),
        mo.md(r"$$x \leftarrow x + \underbrace{G(a)}_{\text{gate}} \cdot \text{sublayer}(y)$$"),
        mo.md(
            "- Scale & shift **depend** on the action **a**\n"
            "- Why per layer? Signal from concat/add fades\n"
            "- Zero-init: $G{=}0$ at start → predictor is identity; gates open as training progresses"
        ),
    ], align="start")

    if _sys.platform != "emscripten":
        _img_src = (_pathlib.Path(__file__).parent / "media/images/AdaLNTransformerBlock_ManimCE_v0.20.1.png").read_bytes()
    else:
        _img_src = "media/images/AdaLNTransformerBlock_ManimCE_v0.20.1.png"

    mo.vstack([
        page_number(9),
        _heading,
        mo.md("&nbsp;"),
        mo.hstack([
            _adaptive_ln,
            mo.image(_img_src),
        ], widths=[1, 1], gap="2rem", align="start"),
    ], align="start")
    return


@app.cell
def sigreg_optimal_distribution_slide(mo, page_number):
    import sys as _sys
    import pathlib as _pathlib

    _SIG = "#10B981"

    _heading = mo.Html(
        f'<div style="display:flex;align-items:center;gap:0.6rem;">'
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:1.7rem;height:1.7rem;border-radius:50%;background:{_SIG};'
        f'color:white;font-weight:700;font-size:1.1rem;flex-shrink:0;">3</span>'
        f'<h2 style="margin:0;line-height:1.2;">Regularization: Constraining the latent space</h2>'
        f'</div>'
    )

    _left = mo.vstack([
        mo.Html(
            f'<p style="margin:0;font-size:1rem;color:#64748B;">'
            f'Balestriero &amp; LeCun, arXiv 2025 &mdash; <em>LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics</em>'
            f'</p>'
        ),
        mo.md("&nbsp;"),
        mo.md("&nbsp;"),
        mo.Html(
            '<div style="font-size:2.5rem;">'
            '<p style="margin:0 0 1.2rem 0;">&#8226; Downstream tasks are solved by probes on frozen embeddings</p>'
            '<p style="margin:0 0 1.2rem 0;">&#8226; Low-spread dimensions are invisible to any probe &#8594; bias or noise</p>'
            '<p style="margin:0 0 1.2rem 0;">&nbsp;</p>'
            '<p style="margin:0 0 1.2rem 0;">&#8594; <strong>Isotropy</strong> makes every dimension equally usable</p>'
            '<p style="margin:0;">&#8594; <strong>Conclusion:</strong> Isotropic Gaussian is uniquely optimal</p>'
            '</div>'
        ),
    ], align="start")

    if _sys.platform != "emscripten":
        _arch_img = (_pathlib.Path(__file__).parent / "media/images/lewm_architecture_last_frame.png").read_bytes()
    else:
        _arch_img = "media/images/lewm_architecture_last_frame.png"

    _right = mo.vstack([
        mo.md("&nbsp;"),
        mo.md("&nbsp;"),
        mo.Html('<p style="margin:0 0 0.4rem 0;font-size:0.8rem;color:#94A3B8;text-align:center;">LeWM Architecture</p>'),
        mo.image(_arch_img),
    ], align="center")

    mo.vstack([
        page_number(10),
        _heading,
        mo.md("&nbsp;"),
        mo.hstack([_left, _right], widths=[2, 1], gap="2rem", align="start"),
    ], align="start")
    return


@app.cell
def sigreg_algorithm_slide(mo, page_number):
    _SIG = "#10B981"

    _heading = mo.Html(
        f'<div style="display:flex;align-items:center;gap:0.6rem;">'
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:1.7rem;height:1.7rem;border-radius:50%;background:{_SIG};'
        f'color:white;font-weight:700;font-size:1.1rem;flex-shrink:0;">3</span>'
        f'<h2 style="margin:0;line-height:1.2;">SIGReg Algorithm</h2>'
        f'</div>'
    )

    _spacer = mo.Html('<div style="min-width:2rem;flex-shrink:0;"></div>')

    _left = mo.vstack([
        mo.md("**Step 1**: Sample $M$ random unit-norm directions:"),
        mo.hstack([_spacer, mo.md(r"$$\boldsymbol{u}^{(m)} \sim \mathcal{U}(S^{d-1}), \quad m = 1, \ldots, M$$")], gap="0"),
        mo.md("**Step 2**: Project embeddings $Z \\in \\mathbb{R}^{N \\times d}$ onto each direction:"),
        mo.hstack([_spacer, mo.md(r"$$\boldsymbol{h}^{(m)} = Z\,\boldsymbol{u}^{(m)} \in \mathbb{R}^N$$")], gap="0"),
        mo.md("**Step 3**: Apply a normality test $T$ to each projection and average:"),
        mo.hstack([_spacer, mo.md(r"$$\text{SIGReg}(Z) \triangleq \frac{1}{M}\sum_{m=1}^{M} T\!\left(\boldsymbol{h}^{(m)}\right)$$")], gap="0"),
        mo.md(
            "By the **Cramér–Wold theorem**: matching all 1-D marginals "
            "$\\Leftrightarrow$ Matching the full $d$-dimensional joint distribution."
        ),
    ], align="start")

    mo.vstack([

        page_number(11),
        _heading,
        mo.md("&nbsp;"),
        _left,
    ], align="start")
    return


@app.cell
def sigreg_mechanism_slide(VIDEO_STYLE, mo, page_number, render_scene):
    import sys as _sys
    if _sys.platform != "emscripten":
        _sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
        from animations.sigreg_collapse import SIGRegVisualization
        _video = render_scene(SIGRegVisualization)
    else:
        _video = mo.Html(
            f'<video autoplay muted loop controls style="{VIDEO_STYLE}">'
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

        page_number(12),
        _heading,
        _video,
    ], align="start")
    return


@app.cell
def latent_planning_concept_slide(mo, page_number):
    import sys as _sys
    import pathlib as _pathlib

    _PLAN = "#0EA5E9"

    _heading = mo.Html(
        f'<h2 style="margin:0;line-height:1.2;">Latent Planning</h2>'
    )

    if _sys.platform != "emscripten":
        _fig_src = (_pathlib.Path(__file__).parent / "media/images/lewm_latent_planning_fig4.png").read_bytes()
    else:
        _fig_src = "media/images/lewm_latent_planning_fig4.png"

    _fig = mo.image(
        src=_fig_src,
        width="100%",
    )

    _fig_credit = mo.Html(
        '<p style="font-size:0.7rem;color:#888;text-align:right;margin-top:0.25rem;">'
        'From "LeWorldModel: Learning a World Model with Latent Imagination for Model-Based Reinforcement Learning"'
        ' — Maes et al. (arXiv 2026)'
        '</p>'
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

        page_number(13),
        _heading,
        mo.md("*Finding the optimal action sequence entirely in imagination*"),
        mo.md("&nbsp;"),
        _fig,
        _fig_credit,
        mo.md("&nbsp;"),
        _bullets,
    ], align="start")
    return


@app.cell
def outline_recap_after_lewm(SECTION):
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
                    "Representation collapse: The central challenge",
                    "How existing methods solve it and where they fall short",
                    "Taxonomy of world models",
                ], done=True),
                _entry(2, "02 · LeWorldModel", [
                    "ViT-Tiny encoder + action-conditioned transformer predictor",
                    "SIGReg: One hyperparameter to prevent collapse",
                    "Latent planning via MPC + CEM",
                ], done=True),
                _entry(3, "03 · Experiments", [
                    "Task performance and planning speed across multiple benchmarks",
                    "Violation of Expectation: Physics structure in latent space",
                ]),
                _entry(4, "04 · Discussion", [
                    "Key findings and authors' claims",
                    "Limitations & future directions",
                ]),
            ],
            align="start",
            gap="0.5rem",
        )
    _()
    return


@app.cell
def experiments_environments_slide(mo, page_number):
    import sys as _esys
    import pathlib as _epathlib

    _EXP_BG  = "#FEF3C7"
    _EXP_BDR = "#F59E0B"

    _heading = mo.Html(
        '<h2 style="margin:0;">Evaluation Environments</h2>'
    )
    _subtitle = mo.Html(
        '<p style="margin:0;color:#64748B;font-size:1.1rem;">'
        'Four tasks spanning 2D/3D manipulation and navigation'
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
            _src = (_epathlib.Path(__file__).parent / f"media/images/{_name}.png").read_bytes()
        else:
            _src = f"media/images/{_name}.png"
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

    _fig_credit = mo.Html(
        '<p style="font-size:0.7rem;color:#888;text-align:right;margin-top:0.25rem;">'
        'From "LeWorldModel: Learning a World Model with Latent Imagination for Model-Based Reinforcement Learning"'
        ' — Maes et al. (arXiv 2026)'
        '</p>'
    )

    mo.vstack([

        page_number(14),
        _heading,
        _subtitle,
        mo.md("&nbsp;"),
        _env_panels,
        _fig_credit,
        mo.md("&nbsp;"),
        _results,
    ], align="start")
    return


@app.cell
def experiments_physics_slide(mo, page_number):
    import pathlib as _pathlib
    import sys as _sys

    _heading = mo.Html(
        '<h2 style="margin:0;">Violation of Expectation</h2>'
    )

    if _sys.platform != "emscripten":
        _voe_src = (_pathlib.Path(__file__).parent / "media/images/fig10_voe_clean.png").read_bytes()
    else:
        _voe_src = "media/images/fig10_voe_clean.png"

    _fig = mo.image(
        src=_voe_src,
        width="80%",
    )

    _content = mo.Html(
        '<div style="font-size:1.05rem;line-height:1.9;">'

        '<ul style="list-style:disc;padding-left:1.4rem;margin:0;">'
        '<li>Surprise = discrepancy between predicted and actual future observations</li>'
        '</ul>'
        '<p style="font-weight:700;margin:0.8rem 0 0.3rem 0;">Two perturbation types</p>'
        '<ul style="list-style:disc;padding-left:1.4rem;margin:0;">'
        '<li>Visual: object color changes abruptly mid-trajectory</li>'
        '<li>Physical: object teleports to a random location</li>'
         '</div>'
    )

    _fig_credit = mo.Html(
        '<p style="font-size:0.7rem;color:#888;text-align:right;margin-top:0.25rem;">'
        'From "LeWorldModel: Learning a World Model with Latent Imagination for Model-Based Reinforcement Learning"'
        ' — Maes et al. (arXiv 2026)'
        '</p>'
    )

    mo.vstack([
        page_number(15),
        _heading,
        mo.Html('<div style="height:0.8rem;"></div>'),
        _content,
        mo.Html('<div style="height:2.5rem;"></div>'),
        _fig,
        _fig_credit,
    ], align="start", gap="1rem")
    return


@app.cell
def outline_recap_after_experiments(SECTION):
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
                    "Representation collapse: The central challenge",
                    "How existing methods solve it and where they fall short",
                    "Taxonomy of world models",
                ], done=True),
                _entry(2, "02 · LeWorldModel", [
                    "ViT-Tiny encoder + action-conditioned transformer predictor",
                    "SIGReg: One hyperparameter to prevent collapse",
                    "Latent planning via MPC + CEM",
                ], done=True),
                _entry(3, "03 · Experiments", [
                    "Task performance and planning speed across multiple benchmarks",
                    "Violation of Expectation: Physics structure in latent space",
                ], done=True),
                _entry(4, "04 · Discussion", [
                    "Key findings and authors' claims",
                    "Limitations & future directions",
                ]),
            ],
            align="start",
            gap="0.5rem",
        )
    _()
    return


@app.cell
def findings_limitations_slide(mo, page_number):
    _DISC = "#8B5CF6"

    def _bullet(head):
        return (
            f'<div style="display:flex;gap:0.7rem;margin:1.2rem 0;line-height:1.5;">'
            f'<span style="color:{_DISC};font-weight:700;flex-shrink:0;margin-top:0.1rem;font-size:1.5rem;">▸</span>'
            f'<span style="font-size:1.5rem;"><strong>{head}</strong></span>'
            f'</div>'
        )

    _findings_html = "".join([
        _bullet("Stable end-to-end training from raw pixels, competitive across diverse tasks"),
        _bullet("SIGReg (LeJEPA) is sufficient to stabilize end-to-end world model training"),
        _bullet("48× faster planning than DINO-WM"),
        _bullet("Latent space captures physical structure"),
    ])

    mo.vstack([
        page_number(16),
        mo.md("## Key Findings"),
        mo.md("&nbsp;"),
        mo.Html(_findings_html),
    ], align="start")
    return


@app.cell
def discussion_slide(mo, page_number):
    f_DISC = "#8B5CF6"

    def _bullet(head):
        return (
            '<div style="display:flex;gap:0.7rem;margin:1.2rem 0;line-height:1.5;">'
            f'<span style="color:{f_DISC};font-weight:700;flex-shrink:0;margin-top:0.1rem;font-size:1.5rem;">&#9658;</span>'
            f'<span style="font-size:1.5rem;"><strong>{head}</strong></span>'
            '</div>'
        )

    _limitations_html = "".join([
        _bullet("Short horizon &#8594 Hierarchichal JEPAs" ),
        _bullet("Deterministic predictor: Multimodal dynamics (contacts, collisions) unrepresentable"),
        _bullet("Not a foundation model: Action conditioning &#8594 Must retrain per environment"),
        _bullet("Latent planning with CEM does not scale to high-DoF"),
    ])

    mo.vstack([
        page_number(17),
        mo.md("## Limitations & Future Work"),
        mo.md("&nbsp;"),
        mo.Html(_limitations_html),
    ], align="start")
    return


if __name__ == "__main__":
    app.run()
