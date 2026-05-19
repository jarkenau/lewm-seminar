import marimo

__generated_with = "0.23.6"
app = marimo.App(
    width="full",
    app_title="LeWorldModel",
    layout_file="layouts/presentation.slides.json",
)

with app.setup:
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

    def render_scene(scene_cls, quality="high_quality"):
        import base64
        import pathlib
        import subprocess
        from manim import config as manim_config

        _quality_to_dir = {
            "low_quality": "480p15",
            "medium_quality": "720p30",
            "high_quality": "1080p60",
            "fourk_quality": "2160p60",
        }
        _assets = pathlib.Path(__file__).parent / "assets"
        _res_dir = _quality_to_dir[quality]
        _out = _assets / "videos" / _res_dir / f"{scene_cls.__name__}.mp4"
        _out.parent.mkdir(parents=True, exist_ok=True)

        if not _out.exists():
            manim_config.media_dir = str(_assets)
            manim_config.quality = quality
            manim_config.preview = False
            try:
                scene_cls().render()
            except Exception:
                _list = _assets / "videos" / _res_dir / "partial_movie_files" / scene_cls.__name__ / "partial_movie_file_list.txt"
                subprocess.run(
                    ["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(_list), "-c", "copy", str(_out)],
                    check=True,
                )

        _b64 = base64.b64encode(_out.read_bytes()).decode()
        import marimo as mo
        return mo.Html(
            f'<video autoplay loop controls style="width:100%;">'
            f'<source src="data:video/mp4;base64,{_b64}" type="video/mp4">'
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
                    <div style="font-size:1.7rem; font-weight:700; color:#111; margin-bottom:2rem;">Outline</div>
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
            justify="center",
            align="start",
            gap="0",
        )


    _()
    return


@app.cell
def jepa_principle_animation_slide():
    def _():
        import random

        class JEPAPrincipleAnimation(Scene):
            def construct(self):
                self.camera.background_color = WHITE

                BLUE   = ManimColor("#1565C0")
                GREEN  = ManimColor("#2E7D32")
                PURPLE = ManimColor("#7B3F9E")
                DARK   = ManimColor("#222222")
                RED_C  = ManimColor("#C62828")

                # ── helpers ────────────────────────────────────────────

                def pixel_frame(seed, label_text):
                    random.seed(seed)
                    grays = ["#cccccc","#aaaaaa","#888888","#666666",
                             "#eeeeee","#bbbbbb","#999999","#dddddd"]
                    cs = 0.3
                    cells = VGroup(*[
                        Rectangle(
                            width=cs, height=cs,
                            fill_color=ManimColor(random.choice(grays)),
                            fill_opacity=1.0,
                            stroke_width=0.4,
                            stroke_color=ManimColor("#999999"),
                        ).move_to(RIGHT * c * cs + DOWN * r * cs)
                        for r in range(4) for c in range(4)
                    ])
                    cells.move_to([0, 0, 0])
                    border = Rectangle(width=4*cs, height=4*cs, color=DARK, stroke_width=2.0)
                    lbl = Text(label_text, color=DARK, font_size=18).next_to(border, DOWN, buff=0.1)
                    return VGroup(cells, border, lbl)

                def encoder_box():
                    box = RoundedRectangle(
                        width=1.5, height=0.52, corner_radius=0.08,
                        fill_color=ManimColor("#EDE7F6"), fill_opacity=1.0,
                        color=PURPLE, stroke_width=2.0,
                    )
                    lbl = Text("Encoder", color=PURPLE, font_size=16).move_to(box)
                    return VGroup(box, lbl)

                def latent_vec(label_text, color):
                    bars = VGroup(*[
                        Rectangle(
                            width=0.32, height=0.16,
                            fill_color=color,
                            fill_opacity=0.35 + 0.06 * (k % 5),
                            stroke_width=0.5,
                            stroke_color=color,
                        )
                        for k in range(8)
                    ]).arrange(DOWN, buff=0.035)
                    lbl = Text(label_text, color=color, font_size=22).next_to(bars, DOWN, buff=0.08)
                    return VGroup(bars, lbl)

                def pred_box():
                    box = RoundedRectangle(
                        width=1.7, height=0.52, corner_radius=0.08,
                        fill_color=ManimColor("#E8F5E9"), fill_opacity=1.0,
                        color=GREEN, stroke_width=2.0,
                    )
                    lbl = Text("Predictor", color=GREEN, font_size=16).move_to(box)
                    return VGroup(box, lbl)

                # ── objects ────────────────────────────────────────────

                fi    = pixel_frame(42, "frame i")
                fi1   = pixel_frame(99, "frame i+1")
                enci  = encoder_box()
                enci1 = encoder_box()
                lati  = latent_vec(r"z_i",             BLUE)
                lati1 = latent_vec(r"z_{i+1}",         BLUE)
                lhat  = latent_vec(r"\hat{z}_{i+1}",   GREEN)
                pred  = pred_box()

                # ── layout ─────────────────────────────────────────────

                LX, RX         = -4.5, 5.0
                TOP_Y, ENC_Y   =  2.5,  0.7
                LAT_Y          = -1.5
                PRED_X, HAT_X  = -1.0,  2.2
                LOSS_Y         = -3.3

                fi.move_to([LX, TOP_Y, 0])
                enci.move_to([LX, ENC_Y, 0])
                lati.move_to([LX, LAT_Y, 0])

                fi1.move_to([RX, TOP_Y, 0])
                enci1.move_to([RX, ENC_Y, 0])
                lati1.move_to([RX, LAT_Y, 0])

                pred.move_to([PRED_X, LAT_Y, 0])
                lhat.move_to([HAT_X,  LAT_Y, 0])

                # ── arrows ─────────────────────────────────────────────

                a_fi_enc    = Arrow(fi[1].get_bottom(),    enci[0].get_top(),    color=PURPLE, stroke_width=2.5, buff=0.07)
                a_enc_lati  = Arrow(enci[0].get_bottom(),  lati[0].get_top(),    color=BLUE,   stroke_width=2.5, buff=0.07)
                a_fi1_enc   = Arrow(fi1[1].get_bottom(),   enci1[0].get_top(),   color=PURPLE, stroke_width=2.5, buff=0.07)
                a_enc_lati1 = Arrow(enci1[0].get_bottom(), lati1[0].get_top(),   color=BLUE,   stroke_width=2.5, buff=0.07)
                a_lati_pred = Arrow(lati[0].get_right(),   pred[0].get_left(),   color=GREEN,  stroke_width=2.5, buff=0.07)
                a_pred_hat  = Arrow(pred[0].get_right(),   lhat[0].get_left(),   color=GREEN,  stroke_width=2.5, buff=0.07)

                loss = Text(
                    "L = ||z(i+1) - z_hat(i+1)||",
                    color=RED_C, font_size=26,
                )
                loss.move_to([(HAT_X + RX) / 2, LOSS_Y, 0])

                a_lati1_loss = Arrow(lati1[0].get_bottom(), loss.get_top() + LEFT  * 0.6, color=RED_C, stroke_width=2.0, buff=0.07)
                a_lhat_loss  = Arrow(lhat[0].get_bottom(),  loss.get_top() + RIGHT * 0.6, color=RED_C, stroke_width=2.0, buff=0.07)

                # ── animate ────────────────────────────────────────────

                self.play(FadeIn(fi), FadeIn(fi1))
                self.wait(0.3)

                self.play(FadeIn(enci), FadeIn(enci1))
                self.play(GrowArrow(a_fi_enc), GrowArrow(a_fi1_enc))
                self.wait(0.2)

                self.play(GrowArrow(a_enc_lati), GrowArrow(a_enc_lati1))
                self.play(FadeIn(lati), FadeIn(lati1))
                self.wait(0.4)

                self.play(FadeIn(pred))
                self.play(GrowArrow(a_lati_pred))
                self.play(GrowArrow(a_pred_hat))
                self.play(FadeIn(lhat))
                self.wait(0.4)

                self.play(GrowArrow(a_lati1_loss), GrowArrow(a_lhat_loss))
                self.play(Write(loss))
                self.wait(1.0)

        return render_scene(JEPAPrincipleAnimation)

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
                    mo.md('<div style="font-size:1.7rem; font-weight:700; color:#111; margin-bottom:1.8rem;">References</div>'),
                    mo.Html("".join(rows) + slide_no_html),
                ],
                align="start",
                gap="0",
            )

        with open("references.bib") as f:
            db = bibtexparser.load(f)

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

        with open("references.bib") as f:
            db = bibtexparser.load(f)

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
                mo.md('<div style="font-size:1.7rem; font-weight:700; color:#111; margin-bottom:1.8rem;">References</div>'),
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
