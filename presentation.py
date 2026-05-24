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

    VIDEO_STYLE = "max-width:95%; max-height:45vh; width:auto; height:auto; display:block; margin:0 auto;"

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
                f'<video autoplay loop controls style="{VIDEO_STYLE}">'
                f'<source src="data:video/mp4;base64,{_b64}" type="video/mp4">'
                f'</video>'
            )
        else:
            # WASM: video served as a static file copied alongside the HTML in CI
            _rel = f"media/videos/{_source_stem}/{_res_dir}/{_scene_name}.mp4"
            import marimo as mo
            return mo.Html(
                f'<video autoplay loop controls style="{VIDEO_STYLE}">'
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
        return mo.vstack(
            [
                mo.md("# Outline"),
                mo.md("### 01 Background & State of the Art\n- JEPA: predict in latent space, not pixel space\n- Representation collapse — the central challenge\n- How existing methods solve it and where they fall short"),
                mo.md("### 02 LeWorldModel\n- ViT-Tiny encoder + action-conditioned transformer predictor\n- SIGReg: one hyperparameter to prevent collapse\n- Latent planning via MPC + CEM"),
                mo.md("### 03 Experiments\n- Task performance and planning speed across multiple benchmarks\n- Physics emerges in latent space"),
                mo.md("### 04 Discussion\n- Authors' claims, personal assessment, open questions"),
            ],
            align="start",
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
            f'<video autoplay loop controls style="{VIDEO_STYLE}">'
            '<source src="media/videos/jepa_training/1080p60/JEPATraining.mp4" type="video/mp4">'
            '</video>'
        )
    _video
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

        return mo.hstack(
            [
                mo.vstack(
                    [
                        mo.md("# Representation Collapse"),
                        mo.md("*THE CORE PROBLEM OF JEPA-BASED ARCHITECTURES*"),
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
        )
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

        return mo.hstack(
            [
                mo.vstack(
                    [
                        mo.md("# Representation Collapse"),
                        mo.md("*THE CORE PROBLEM OF JEPA-BASED ARCHITECTURES*"),
                        mo.md("""
    **01 Complete Collapse**

    The encoder maps all inputs to the same point in embedding space.
    The predictor trivially satisfies the loss without learning anything.

    **02 Dimensional Collapse**

    Inputs map into a low-dimensional subspace of the full embedding space.
    Loss looks fine — but representations carry far less information than intended.
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
        )
    _()
    return


@app.cell
def bibliography_slide_1(mo):
    def _():
        import bibtexparser

        ENTRIES_PER_PAGE = 7

        def clean(s):
            return s.replace("{", "").replace("}", "").replace("\n", " ")

        import sys, io
        if sys.platform == "emscripten":
            from pyodide.http import open_url
            _bib_text = open_url("references.bib").read()
        else:
            with open("references.bib") as f:
                _bib_text = f.read()
        db = bibtexparser.load(io.StringIO(_bib_text))

        all_entries = list(enumerate(db.entries, 1))
        lines = ["# References\n"]
        for i, entry in all_entries[:ENTRIES_PER_PAGE]:
            authors = clean(entry.get("author", ""))
            year = clean(entry.get("year", ""))
            title = clean(entry.get("title", ""))
            venue = clean(entry.get("journal") or entry.get("booktitle") or "")
            lines.append(f"**[{i}]** {authors} ({year}). *{title}*. {venue}.\n")

        return mo.vstack([mo.md("\n".join(lines))], align="start")

    _()
    return


@app.cell
def bibliography_slide_2(mo):
    def _():
        import bibtexparser

        ENTRIES_PER_PAGE = 7

        def clean(s):
            return s.replace("{", "").replace("}", "").replace("\n", " ")

        import sys, io
        if sys.platform == "emscripten":
            from pyodide.http import open_url
            _bib_text = open_url("references.bib").read()
        else:
            with open("references.bib") as f:
                _bib_text = f.read()
        db = bibtexparser.load(io.StringIO(_bib_text))

        all_entries = list(enumerate(db.entries, 1))
        page_entries = all_entries[ENTRIES_PER_PAGE : ENTRIES_PER_PAGE * 2]
        mo.stop(not page_entries)

        lines = ["# References (cont.)\n"]
        for i, entry in page_entries:
            authors = clean(entry.get("author", ""))
            year = clean(entry.get("year", ""))
            title = clean(entry.get("title", ""))
            venue = clean(entry.get("journal") or entry.get("booktitle") or "")
            lines.append(f"**[{i}]** {authors} ({year}). *{title}*. {venue}.\n")

        return mo.vstack([mo.md("\n".join(lines))], align="start")

    _()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
