from manim import *
import numpy as np


class WorldModelTaxonomy(Scene):
    """
    Three functional types of world models (after World Labs taxonomy):
      1. Renderer  — outputs observations (image frames)
      2. Simulator — outputs state (latent trajectory)
      3. Planner   — outputs actions (token sequence)
    """

    # ── Palette (matches jepa_training / lewm_architecture) ─────────────────────
    TEXT_C     = "#1a1a1a"
    MUTED_C    = "#888888"
    BOX_FILL   = "#f4f4f4"
    BOX_STROKE = "#2d2d2d"
    CURVE_C    = "#4A90D9"   # EMBED_COLOR blue
    MTN_DARK   = "#2d4a3c"
    MTN_MID    = "#4a6c56"
    SUN_C      = "#e05530"
    BG         = WHITE

    # ── Layout constants ─────────────────────────────────────────────────────────
    LBL_X  = -5.4
    LBL_W  = 1.95
    LBL_H  = 1.80
    ROW_Y  = [2.1, 0.0, -2.1]
    CSTART = -4.05
    CEND   =  6.55

    def construct(self):
        self.camera.background_color = self.BG

        title = self._title()
        lb1, lb2, lb3 = [self._lbl_box(*args) for args in [
            ("renders",   self.ROW_Y[0], "actions",    "pixels",
             ("Cosmos-Predict2.5", "Ali et al., 2025")),
            ("simulates", self.ROW_Y[1], "actions",    "world state",
             ("Motus", "Bi et al., 2025")),
            ("plans",     self.ROW_Y[2], "obs + goal", "actions",
             ("LeWorldModel", "Maes et al., 2026")),
        ]]
        c1 = self._renderer_row(self.ROW_Y[0])
        c2 = self._simulator_row(self.ROW_Y[1])
        c3 = self._planner_row(self.ROW_Y[2])

        # ── Animation ────────────────────────────────────────────────────────────
        self.play(Write(title), run_time=0.8)
        self.wait(0.2)

        # Row 1 — Renderer
        self.play(FadeIn(lb1), run_time=0.5)
        self.play(
            AnimationGroup(*[FadeIn(f, shift=RIGHT * 0.1) for f in c1],
                           lag_ratio=0.18),
            run_time=1.5,
        )
        self.wait(1.8)

        # Row 2 — Simulator
        self.play(FadeIn(lb2), run_time=0.5)
        self.play(
            FadeIn(c2.static),
            Create(c2.curve),
            run_time=1.5,
        )
        self.play(FadeIn(c2.dots), run_time=0.4)
        self.wait(1.8)

        # Row 3 — Planner
        self.play(FadeIn(lb3), run_time=0.5)
        self.play(
            AnimationGroup(*[FadeIn(t, shift=RIGHT * 0.1) for t in c3],
                           lag_ratio=0.18),
            run_time=1.5,
        )
        self.wait(2.5)

    # ── Helpers ──────────────────────────────────────────────────────────────────

    def _title(self):
        return Text(
            "Functional Taxonomy of World Models",
            font_size=28, color=self.TEXT_C,
        ).to_edge(UP, buff=0.4)

    def _lbl_box(self, italic_word, y, in_val, out_val, example=None):
        box = RoundedRectangle(
            corner_radius=0.1,
            width=self.LBL_W, height=self.LBL_H,
            fill_color=self.BOX_FILL, fill_opacity=1,
            stroke_color=self.BOX_STROKE, stroke_width=2,
        ).move_to([self.LBL_X, y, 0])
        w1 = Tex(r"\textit{" + italic_word + r"}", font_size=28, color=self.TEXT_C,
                 ).move_to([self.LBL_X, y + 0.57, 0])
        divider = Line(
            [self.LBL_X - self.LBL_W * 0.42, y + 0.27, 0],
            [self.LBL_X + self.LBL_W * 0.42, y + 0.27, 0],
            stroke_color=self.BOX_STROKE, stroke_width=0.8,
        )
        w3 = Tex(r"\textrm{IN} $\to$ \textrm{" + in_val + r"}",
                 font_size=16, color=self.TEXT_C,
                 ).move_to([self.LBL_X, y + 0.04, 0])
        w4 = Tex(r"\textrm{OUT} $\to$ \textrm{" + out_val + r"}",
                 font_size=16, color=self.TEXT_C,
                 ).move_to([self.LBL_X, y - 0.24, 0])
        elements = [box, w1, divider, w3, w4]
        if example:
            paper_name, authors = example
            sep = Line(
                [self.LBL_X - self.LBL_W * 0.42, y - 0.48, 0],
                [self.LBL_X + self.LBL_W * 0.42, y - 0.48, 0],
                stroke_color=self.BOX_STROKE, stroke_width=0.5,
            )
            cite_title = Tex(r"\textit{" + paper_name + r"}", font_size=13,
                             color=self.TEXT_C).move_to([self.LBL_X, y - 0.62, 0])
            cite_auth = Tex(r"\textrm{" + authors + r"}", font_size=12,
                            color=self.TEXT_C).move_to([self.LBL_X, y - 0.76, 0])
            elements += [sep, cite_title, cite_auth]
        return VGroup(*elements)

    def _mountain_icon(self, cx, cy, w=1.85, h=0.95):
        bg = Rectangle(
            width=w, height=h,
            fill_color=self.BOX_FILL, fill_opacity=1,
            stroke_color=self.BOX_STROKE, stroke_width=2,
        ).move_to([cx, cy, 0])
        back_mtn = Polygon(
            [cx - w * 0.40, cy - h * 0.44, 0],
            [cx - w * 0.02, cy + h * 0.37, 0],
            [cx + w * 0.28, cy - h * 0.44, 0],
            fill_color=self.MTN_DARK, fill_opacity=1, stroke_width=0,
        )
        front_mtn = Polygon(
            [cx + w * 0.06, cy - h * 0.44, 0],
            [cx + w * 0.30, cy + h * 0.08, 0],
            [cx + w * 0.46, cy - h * 0.44, 0],
            fill_color=self.MTN_MID, fill_opacity=1, stroke_width=0,
        )
        sun = Circle(
            radius=h * 0.10,
            fill_color=self.SUN_C, fill_opacity=1, stroke_width=0,
        ).move_to([cx - w * 0.18, cy + h * 0.20, 0])
        return VGroup(bg, back_mtn, front_mtn, sun)

    def _renderer_row(self, y):
        n = 5
        cw = (self.CEND - self.CSTART) / n
        fw, fh = cw * 0.88, self.LBL_H
        frames = VGroup()
        for i in range(n):
            cx = self.CSTART + cw * (i + 0.5)
            frames.add(self._mountain_icon(cx, y, fw, fh))
        return frames

    def _simulator_row(self, y):
        xl = self.CSTART + 0.3
        xr = self.CEND   - 0.2
        xspan = xr - xl

        def curve_pt(t):
            x = xl + t * xspan
            v = (0.48 * np.sin(2.8 * np.pi * t)
                 + 0.15 * np.sin(6.2 * np.pi * t + 0.4))
            return np.array([x, y + v * self.LBL_H * 0.52, 0])

        curve = ParametricFunction(
            curve_pt, t_range=[0, 1, 0.005],
            color=self.CURVE_C, stroke_width=2.8,
        )

        guide = DashedLine(
            [xl, y, 0], [xr, y, 0],
            stroke_color=self.MUTED_C, stroke_width=0.8,
            stroke_opacity=0.5, dash_length=0.14,
        )

        t_arrow = Arrow(
            [xl, y - self.LBL_H * 0.53, 0],
            [xr + 0.12, y - self.LBL_H * 0.53, 0],
            buff=0, stroke_color=self.TEXT_C, stroke_width=2,
            tip_length=0.17, color=self.TEXT_C,
            max_tip_length_to_length_ratio=0.1,
        )
        t_lbl = MathTex(r"t", font_size=18, color=self.TEXT_C).next_to(
            t_arrow, RIGHT, buff=0.08)

        def state_box(pt, tex_label):
            box = RoundedRectangle(
                corner_radius=0.07, width=0.55, height=0.32,
                fill_color=self.BOX_FILL, fill_opacity=1,
                stroke_color=self.BOX_STROKE, stroke_width=1.5,
            ).move_to(pt + UP * 0.40)
            txt = MathTex(tex_label, font_size=16, color=self.CURVE_C).move_to(box)
            return VGroup(box, txt)

        s0_box = state_box(curve_pt(0), r"z_0")
        sT_box = state_box(curve_pt(1), r"z_T")

        start_dot = Dot(curve_pt(0), radius=0.09, color=self.CURVE_C)
        end_dot   = Dot(curve_pt(1), radius=0.09, color=self.CURVE_C)

        static = VGroup(guide, t_arrow, t_lbl, s0_box, sT_box)
        dots   = VGroup(start_dot, end_dot)
        result = VGroup(static, curve, dots)
        result.static = static
        result.curve  = curve
        result.dots   = dots
        return result

    def _planner_row(self, y):
        actions = ["reach", "grasp", "lift", "push", "place"]
        n  = len(actions)
        cw = (self.CEND - self.CSTART) / n
        tw = cw * 0.82
        th = self.LBL_H * 0.82
        tokens = VGroup()
        for i, act in enumerate(actions):
            cx = self.CSTART + cw * (i + 0.5)
            box = RoundedRectangle(
                corner_radius=0.1, width=tw, height=th,
                fill_color=self.BOX_FILL, fill_opacity=1,
                stroke_color=self.BOX_STROKE, stroke_width=2,
            ).move_to([cx, y, 0])
            txt = Tex(r"\textrm{" + act + r"}", font_size=18, color=self.TEXT_C).move_to(box)
            tokens.add(VGroup(box, txt))
        return tokens
