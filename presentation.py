# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.23.6",
#   "bibtexparser>=1.4.0,<2.0",
# ]
# ///

import marimo

__generated_with = "0.23.8"
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
            f'<div style="position:fixed;top:1rem;left:1.5rem;z-index:100;">'
            f'<span style="font-size:0.7rem;font-weight:700;color:{c["text"]};letter-spacing:0.1em;text-transform:uppercase;">'
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
    # position here, and inline markers use the same numbers via cite() — so
    # the two never drift. To cite a new work: add its key here (and to
    # references.bib) and drop a cite("key") in the slide.
    CITED = [
        "maes_leworldmodel_2026",   # LeWM — the paper
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
        # Returns an HTML string — one bibliography entry in IEEE style.
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
        import sys

        _quality_to_dir = {
            "low_quality": "480p15",
            "medium_quality": "720p30",
            "high_quality": "1080p60",
            "fourk_quality": "2160p60",
        }
        _root = pathlib.Path(__file__).parent
        _res_dir = _quality_to_dir[quality]
        _scene_name = scene_cls.__name__
        _source = pathlib.Path(inspect.getfile(scene_cls))
        _source_stem = _source.stem
        _out = _root / "media" / "videos" / _source_stem / _res_dir / f"{_scene_name}.mp4"

        if sys.platform != "emscripten":
            # Re-render if missing or source file is newer than the cached render
            _stale = _out.exists() and _source.stat().st_mtime > _out.stat().st_mtime
            if not _out.exists() or _stale:
                from manim import config as manim_config
                manim_config.media_dir = str(_root / "media")
                manim_config.input_file = str(_source)
                manim_config.quality = quality
                manim_config.preview = False
                scene_cls().render()

            if not _out.exists():
                raise FileNotFoundError(
                    f"Render succeeded but output not found at expected path:\n{_out}\n"
                    f"Check that the scene class name matches the file stem."
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
            mo.md("World Models Seminar · Technical University of Munich "),
            mo.md("*Chair of Computer Aided Medical Procedures*"),
            mo.md("&nbsp;"),
            mo.md("# LeWorldModel"),    
            mo.md("###Stable End-to-End Joint-Embedding Predictive Architecture from Pixels"),
            mo.md("&nbsp;"),
            mo.md("Lucas Maes · Quentin Le Lidec · Damien Scieur  Yann LeCun · Randall Balestriero"),
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
                    "Representation collapse — the central challenge",
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
        _sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
        from animations.jepa_training import JEPATraining
        _video = render_scene(JEPATraining)
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
    - Loss looks fine — but representations are impoverished.
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
def sota_target_task_slide():
    def _():
        import marimo as mo
        return mo.vstack([
            section_strip(1),
            page_number(4),
            mo.md("## State of the Art — by *Target Task*"),
            mo.md("*WHAT PROBLEM IS THE WORLD MODEL ASKED TO SOLVE?*"),
            mo.md("&nbsp;"),
            sota_table(
                ["Family", "What it does", "Representative work"],
                [
                    ["Self-supervised representation learning",
                     "Predict masked latent patches — no actions, no planning",
                     f"I-JEPA [{cite('assran_i-jepa_2023')}], V-JEPA [{cite('bardes_v-jepa_2024')}] / "
                     f"V-JEPA 2 [{cite('assran_v-jepa_2025')}], Echo-JEPA [{cite('munim_echojepa_2026')}] / "
                     f"Brain-JEPA [{cite('dong_brain-jepa_2024')}]"],
                    ["Generative world models",
                     "Action-conditioned pixel-space simulators, often reward-based, for RL &amp; games",
                     f"IRIS [{cite('micheli_iris_2023')}], DIAMOND [{cite('alonso_diamond_2024')}], "
                     f"OASIS [{cite('decart_oasis_2024')}], DreamerV4 [{cite('hafner_dreamer4_2025')}], "
                     f"Genie [{cite('bruce_genie_2024')}]"],
                    ["Latent action-conditioned world models",
                     "Predict dynamics in latent space, plan by imagination",
                     f"DINO-WM [{cite('zhou_dino-wm_2024')}], PLDM [{cite('sobal_pldm_2025')}]"],
                ],
            ),
        ], align="start")
    _()
    return


@app.cell
def sota_anticollapse_slide():
    def _():
        import marimo as mo
        return mo.vstack([
            section_strip(1),
            page_number(5),
            mo.md("## State of the Art — by *Anti-Collapse Strategy*"),
            mo.md("*HOW DOES EACH METHOD AVOID REPRESENTATION COLLAPSE?*"),
            mo.md("&nbsp;"),
            sota_table(
                ["Strategy", "Mechanism", "Limitation"],
                [
                    ["Generative reconstruction",
                     "Pixel target is fixed — collapse impossible by construction",
                     "Wastes capacity modelling irrelevant pixel detail"],
                    ["EMA + stop-gradient",
                     "Asymmetric self-distillation from a moving-average teacher",
                     "No well-defined objective — purely heuristic"],
                    ["Frozen pretrained encoder",
                     "Encoder is fixed, so it cannot collapse",
                     "Bounded by pretraining knowledge; not end-to-end"],
                    [f"Explicit regularization (VICReg [{cite('bardes_vicreg_2022')}])",
                     "Variance / covariance penalty terms",
                     "Training instabilities; up to 6 loss hyperparameters"],
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
            mo.md("## State of the Art — Where LeWM Fits"),
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
    # Recap of the outline shown at the 01 → 02 boundary. Section 01 is grayed
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
                    "Representation collapse — the central challenge",
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
def bibliography_slide_1(mo):
    def _():
        import bibtexparser

        ENTRIES_PER_PAGE = 7

        import sys, io
        if sys.platform == "emscripten":
            from pyodide.http import open_url
            _bib_text = open_url("references.bib").read()
        else:
            with open("references.bib") as f:
                _bib_text = f.read()
        db = bibtexparser.load(io.StringIO(_bib_text))

        # Only the works cited in the slides, numbered by their position in CITED.
        by_key = {e.get("ID"): e for e in db.entries}
        cited_entries = [(i, by_key[k]) for i, k in enumerate(CITED, 1) if k in by_key]

        items = "".join(format_ref_ieee(i, e) for i, e in cited_entries[:ENTRIES_PER_PAGE])
        return mo.vstack([
            page_number(7),
            mo.Html(f'<h2 style="margin-bottom:0.5rem;">References</h2>{items}'),
        ], align="start")

    _()
    return


@app.cell
def bibliography_slide_2(mo):
    def _():
        import bibtexparser

        ENTRIES_PER_PAGE = 7

        import sys, io
        if sys.platform == "emscripten":
            from pyodide.http import open_url
            _bib_text = open_url("references.bib").read()
        else:
            with open("references.bib") as f:
                _bib_text = f.read()
        db = bibtexparser.load(io.StringIO(_bib_text))

        # Only the works cited in the slides, numbered by their position in CITED.
        by_key = {e.get("ID"): e for e in db.entries}
        cited_entries = [(i, by_key[k]) for i, k in enumerate(CITED, 1) if k in by_key]
        page_entries = cited_entries[ENTRIES_PER_PAGE : ENTRIES_PER_PAGE * 2]
        mo.stop(not page_entries)

        items = "".join(format_ref_ieee(i, e) for i, e in page_entries)
        return mo.vstack([
            page_number(8),
            mo.Html(f'<h2 style="margin-bottom:0.5rem;">References (cont.)</h2>{items}'),
        ], align="start")

    _()
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
