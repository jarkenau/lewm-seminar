# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.23.6",
#   "bibtexparser>=1.4.0",
# ]
# ///
import marimo

__generated_with = "0.23.6"
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
            mo.vstack(
                [
                    mo.md(
                        r"""
                        <div style="text-align:center; font-size:0.85rem; letter-spacing:0.12em; color:#666; margin-bottom:2.5rem;">
                        World Models Seminar &nbsp;·&nbsp; Technical University of Munich<br>
                        <span style="font-size:0.78rem; color:#999;">Chair of Computer Aided Medical Procedures</span>
                        </div>
                        """
                    ),
                    mo.md(
                        r"""
                        <div style="text-align:center;">
                          <div style="font-size:2.0rem; font-weight:700; line-height:1.25; color:#111; max-width:820px; margin:0 auto;">
                            LeWorldModel: Stable End-to-End<br>Joint-Embedding Predictive Architecture<br>from Pixels
                          </div>
                        </div>
                        """
                    ),
                    mo.md(
                        r"""
                        <div style="text-align:center; margin-top:1.8rem; color:#444; font-size:0.95rem; line-height:2.0;">
                        Lucas Maes &nbsp;·&nbsp; Quentin Le Lidec &nbsp;·&nbsp; Damien Scieur<br>
                        Yann LeCun &nbsp;·&nbsp; Randall Balestriero
                        </div>
                        <div style="text-align:center; margin-top:0.4rem; color:#888; font-size:0.8rem; letter-spacing:0.04em;">
                        Mila / Université de Montréal &nbsp;·&nbsp; NYU &nbsp;·&nbsp; Samsung SAIL &nbsp;·&nbsp; Brown University
                        </div>
                        """
                    ),
                    mo.md(
                        r"""
                        <div style="text-align:center; margin-top:1.5rem;">
                          <a href="https://arxiv.org/abs/2603.19312" target="_blank" style="display:inline-block; background:#f0f0f0; border-radius:4px; padding:0.25rem 0.75rem; font-size:0.78rem; color:#555; font-family:monospace; letter-spacing:0.03em; text-decoration:none;">
                            arXiv&nbsp;2603.19312
                          </a>
                        </div>
                        """
                    ),
                    mo.md(
                        r"""
                        <hr style="border:none; border-top:1px solid #ddd; margin:2.5rem auto; width:480px;">
                        <div style="text-align:center; color:#555; font-size:0.88rem; line-height:1.8;">
                          Presented by <strong>Julian Arkenau</strong><br>
                          <span style="color:#888; font-size:0.82rem;">19 June 2026</span>
                        </div>
                        """
                    ),
                ],
                gap="0",
            )
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
                mo.md(
                    r"""
                    <div style="font-size:1.7rem; font-weight:700; color:#111; padding-top:2.5rem; margin-bottom:2rem;">Outline</div>
                    """
                ),
                mo.md(
                    r"""
                    <div style="font-size:1rem; color:#333;">
                      <div style="margin-bottom:1.2rem;">
                        <span style="color:#aaa; font-size:0.8rem; margin-right:1rem;">01</span><strong>Background &amp; State of the Art</strong>
                        <div style="margin-left:2.8rem; margin-top:0.3rem; font-size:0.82rem; color:#666; line-height:1.8;">
                          JEPA: predict in latent space, not pixel space<br>
                          Representation collapse — the central challenge<br>
                          How existing methods solve it and where they fall short
                        </div>
                      </div>
                      <div style="margin-bottom:1.2rem;">
                        <span style="color:#aaa; font-size:0.8rem; margin-right:1rem;">02</span><strong>LeWorldModel</strong>
                        <div style="margin-left:2.8rem; margin-top:0.3rem; font-size:0.82rem; color:#666; line-height:1.8;">
                          ViT-Tiny encoder + action-conditioned transformer predictor<br>
                          SIGReg: one hyperparameter to prevent collapse<br>
                          Latent planning via MPC + CEM
                        </div>
                      </div>
                      <div style="margin-bottom:1.2rem;">
                        <span style="color:#aaa; font-size:0.8rem; margin-right:1rem;">03</span><strong>Experiments</strong>
                        <div style="margin-left:2.8rem; margin-top:0.3rem; font-size:0.82rem; color:#666; line-height:1.8;">
                          Task performance and planning speed across multiple benchmarks<br>
                          Physics emerges in latent space
                        </div>
                      </div>
                      <div>
                        <span style="color:#aaa; font-size:0.8rem; margin-right:1rem;">04</span><strong>Discussion</strong>
                        <div style="margin-left:2.8rem; margin-top:0.3rem; font-size:0.82rem; color:#666; line-height:1.8;">
                          Authors' claims, personal assessment, open questions
                        </div>
                      </div>
                    </div>
                    """
                ),
                mo.Html(
                    '<div style="position:fixed; bottom:1.2rem; right:1.5rem; font-size:0.72rem; color:#bbb; letter-spacing:0.05em;">1</div>'
                ),
            ],
            align="start",
            gap="0",
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
            import base64
            import pathlib
            img_b64 = base64.b64encode(
                (pathlib.Path(__file__).parent / "media/images/jepa_final_frame.png").read_bytes()
            ).decode()
            img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width:100%; border-radius:4px;" />'
        else:
            img_tag = '<img src="media/images/jepa_final_frame.png" style="width:100%; border-radius:4px;" />'

        def right_col():
            return mo.vstack(
                [
                    mo.md(
                        r"""
                        <div style="font-size:0.72rem; letter-spacing:0.08em;
                                    color:#bbb; margin-bottom:0.5rem; text-align:center;">
                          JEPA ARCHITECTURE
                        </div>
                        """
                    ),
                    mo.Html(img_tag),
                ],
                align="center",
                gap="0",
            )

        return mo.hstack(
            [
                mo.vstack(
                    [
                        mo.md(
                            r"""
                            <div style="font-size:1.7rem; font-weight:700; color:#111; padding-top:2.5rem; margin-bottom:0.4rem;">
                              Representation Collapse
                            </div>
                            <div style="font-size:0.78rem; letter-spacing:0.1em; color:#aaa; margin-bottom:2rem;">
                              THE CORE PROBLEM OF JEPA-BASED ARCHITECTURES
                            </div>
                            <div style="font-size:1.35rem; color:#111; line-height:1.6; margin-top:1rem;">
                              What is the easiest way a model could achieve
                              <br><strong>(near-)perfect prediction loss?</strong>
                            </div>
                            """
                        ),
                    ],
                    align="start",
                    gap="0",
                ),
                right_col(),
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
            import base64
            import pathlib
            img_b64 = base64.b64encode(
                (pathlib.Path(__file__).parent / "media/images/jepa_final_frame.png").read_bytes()
            ).decode()
            img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width:100%; border-radius:4px;" />'
        else:
            img_tag = '<img src="media/images/jepa_final_frame.png" style="width:100%; border-radius:4px;" />'

        def right_col():
            return mo.vstack(
                [
                    mo.md(
                        r"""
                        <div style="font-size:0.72rem; letter-spacing:0.08em;
                                    color:#bbb; margin-bottom:0.5rem; text-align:center;">
                          JEPA ARCHITECTURE
                        </div>
                        """
                    ),
                    mo.Html(img_tag),
                ],
                align="center",
                gap="0",
            )

        return mo.hstack(
            [
                mo.vstack(
                    [
                        mo.md(
                            r"""
                            <div style="font-size:1.7rem; font-weight:700; color:#111; padding-top:2.5rem; margin-bottom:0.4rem;">
                              Representation Collapse
                            </div>
                            <div style="font-size:0.78rem; letter-spacing:0.1em; color:#aaa; margin-bottom:2rem;">
                              THE CORE PROBLEM OF JEPA-BASED ARCHITECTURES
                            </div>
                            <div style="font-size:1rem; color:#333;">
                              <div style="margin-bottom:1.6rem;">
                                <span style="color:#aaa; font-size:0.9rem; margin-right:1rem;">01</span>
                                <strong style="font-size:1.2rem;">Complete Collapse</strong>
                                <div style="margin-left:2.8rem; margin-top:0.5rem; font-size:1.05rem; color:#444; line-height:1.8;">
                                  The encoder maps all inputs to the same point in embedding space.<br>
                                  The predictor trivially satisfies the loss without learning anything.
                                </div>
                              </div>
                              <div>
                                <span style="color:#aaa; font-size:0.9rem; margin-right:1rem;">02</span>
                                <strong style="font-size:1.2rem;">Dimensional Collapse</strong>
                                <div style="margin-left:2.8rem; margin-top:0.5rem; font-size:1.05rem; color:#444; line-height:1.8;">
                                  Inputs map into a low-dimensional subspace of the full embedding space.<br>
                                  Loss looks fine — but representations carry far less information than intended.
                                </div>
                              </div>
                            </div>
                            """
                        ),
                    ],
                    align="start",
                    gap="0",
                ),
                right_col(),
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

        SLIDE_NO = 2
        ENTRIES_PER_PAGE = 7

        def clean(s):
            return s.replace("{", "").replace("}", "").replace("\n", " ")

        def render_page(entries):
            rows = []
            for i, entry in entries:
                authors = clean(entry.get("author", ""))
                year    = clean(entry.get("year", ""))
                title   = clean(entry.get("title", ""))
                venue   = clean(entry.get("journal") or entry.get("booktitle") or "")
                rows.append(
                    f'<div style="margin-bottom:0.9rem;">'
                    f'<span style="color:#aaa; font-size:0.78rem; margin-right:0.75rem;">[{i}]</span>'
                    f'<span style="font-size:0.82rem; color:#333; line-height:1.7;">'
                    f'{authors} ({year}). <em>{title}</em>. {venue}.'
                    f'</span></div>'
                )
            slide_no_html = (
                f'<div style="position:fixed; bottom:1.2rem; right:1.5rem; font-size:0.72rem; color:#bbb; letter-spacing:0.05em;">{SLIDE_NO}</div>'
                if SLIDE_NO is not None else ""
            )
            return mo.vstack(
                [
                    mo.md('<div style="font-size:1.7rem; font-weight:700; color:#111; padding-top:2.5rem; margin-bottom:1.8rem;">References</div>'),
                    mo.Html("".join(rows) + slide_no_html),
                ],
                align="start",
                gap="0",
            )

        import sys, io
        if sys.platform == "emscripten":
            from pyodide.http import open_url
            _bib_text = open_url("references.bib").read()
        else:
            with open("references.bib") as f:
                _bib_text = f.read()
        db = bibtexparser.load(io.StringIO(_bib_text))

        all_entries = list(enumerate(db.entries, 1))
        return render_page(all_entries[:ENTRIES_PER_PAGE])

    _()
    return


@app.cell
def bibliography_slide_2(mo):
    def _():
        import bibtexparser

        SLIDE_NO = 3  # update once all content slides are in place
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

        rows = []
        for i, entry in page_entries:
            authors = clean(entry.get("author", ""))
            year = clean(entry.get("year", ""))
            title = clean(entry.get("title", ""))
            venue = clean(entry.get("journal") or entry.get("booktitle") or "")
            rows.append(
                f'<div style="margin-bottom:0.9rem;">'
                f'<span style="color:#aaa; font-size:0.78rem; margin-right:0.75rem;">[{i}]</span>'
                f'<span style="font-size:0.82rem; color:#333; line-height:1.7;">'
                f'{authors} ({year}). <em>{title}</em>. {venue}.'
                f'</span></div>'
            )
        slide_no_html = (
            f'<div style="position:fixed; bottom:1.2rem; right:1.5rem; font-size:0.72rem; color:#bbb; letter-spacing:0.05em;">{SLIDE_NO}</div>'
            if SLIDE_NO is not None else ""
        )
        return mo.vstack(
            [
                mo.md('<div style="font-size:1.7rem; font-weight:700; color:#111; padding-top:2.5rem; margin-bottom:1.8rem;">References</div>'),
                mo.Html("".join(rows) + slide_no_html),
            ],
            align="start",
            justify="start",
            gap="0",
        )

    _()
    return


if __name__ == "__main__":
    app.run()
