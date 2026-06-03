from manim import *
import numpy as np


# ── Palette ────────────────────────────────────────────────────────────────────
C_EMBED   = "#3B82F6"   # blue   – embedding dots (anisotropic)
C_DIR     = "#B45309"   # dark amber – direction arrows (readable on white)
C_PROJ    = "#059669"   # dark green – projection markers / isotropic state
C_GAUSS   = "#DC2626"   # red    – target N(0,1) curve
C_HIST    = "#7C3AED"   # purple – empirical histogram bars
C_LABEL   = "#1E293B"   # dark slate – titles and text
C_MUTED   = "#94A3B8"   # light gray – secondary labels
BG        = "#FFFFFF"   # white background


class SIGRegVisualization(Scene):
    """
    Visualizes the SIGReg algorithm in seven phases:
      1. Anisotropic embedding cloud  (the 'before' state)
      2. Sample a random direction u^(m)
      3. Project embeddings onto the direction  → 1-D scalars
      4. Test normality: histogram vs N(0,1) target  → T(h^(m))
      5. Multiple directions fanned out (M directions)
      6. Training step: dots shift toward isotropic Gaussian
      7. End state: Z ~ N(0, I)

    Each phase shows its exact formula in the upper-right corner.
    """

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _make_dots(self, pts_2d, color=C_EMBED, radius=0.07):
        return VGroup(*[
            Dot(point=[x, y, 0], radius=radius, color=color)
            for x, y in pts_2d
        ])

    def _projection_line(self, start_2d, end_2d):
        return DashedLine(
            start=[start_2d[0], start_2d[1], 0],
            end=[end_2d[0], end_2d[1], 0],
            dash_length=0.07,
            color=GRAY,
            stroke_opacity=0.55,
            stroke_width=1.5,
        )

    def _section_title(self, text, color=C_LABEL):
        t = Text(text, font_size=26, color=color)
        t.to_edge(UP, buff=0.25)
        return t

    def _formula_panel(self, rows):
        """
        Build a formula panel for the upper-right corner.
        rows: list of (label_str, latex_str, font_size, color)
               label_str="" skips the small label above the formula.
        """
        elements = []
        for label_str, latex_str, fs, col in rows:
            if label_str:
                elements.append(Text(label_str, font_size=15, color=C_MUTED))
            elements.append(MathTex(latex_str, font_size=fs, color=BLACK))
        group = VGroup(*elements).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        group.to_edge(RIGHT, buff=0.6).shift(UP * 1.5)
        return group

    def _swap_formula(self, old, new, **kwargs):
        return AnimationGroup(FadeOut(old), FadeIn(new), **kwargs)

    # ── Main ───────────────────────────────────────────────────────────────────

    def construct(self):
        self.camera.background_color = BG
        np.random.seed(42)

        N = 28
        CLOUD_ORIGIN = np.array([-3.2, 0.0])

        # ── Generate point clouds ──────────────────────────────────────────────
        raw = np.random.randn(N, 2)
        raw[:, 0] *= 1.9
        raw[:, 1] *= 0.38
        angle = np.radians(22)
        rot = np.array([[np.cos(angle), -np.sin(angle)],
                        [np.sin(angle),  np.cos(angle)]])
        raw = (rot @ raw.T).T
        pts = raw + CLOUD_ORIGIN

        np.random.seed(99)
        iso_pts = np.random.randn(N, 2) * 0.95 + CLOUD_ORIGIN

        dir_angle = np.radians(40)
        u = np.array([np.cos(dir_angle), np.sin(dir_angle)])

        # ── Pre-build all formula panels ───────────────────────────────────────
        fp1 = self._formula_panel([
            ("embedding matrix",
             r"Z \in \mathbb{R}^{N \times d}", 24, C_LABEL),
            ("problem",
             r"\mathrm{Cov}(Z) \not\propto I_d", 22, "#D97706"),
        ])

        fp2 = self._formula_panel([
            ("step 1 — sample direction",
             r"\boldsymbol{u}^{(m)} \sim \mathcal{U}(S^{d-1})", 24, C_DIR),
        ])

        fp3 = self._formula_panel([
            ("step 2 — project onto direction",
             r"\boldsymbol{h}^{(m)} = Z\,\boldsymbol{u}^{(m)} \in \mathbb{R}^N", 22, C_PROJ),
        ])

        fp4 = self._formula_panel([
            ("step 3 — Epps–Pulley normality test",
             r"T = N\!\int_{-\infty}^{\infty}\!\left|\hat{\varphi}_X(t)"
             r"- e^{-t^2/2}\right|^2 e^{-t^2/2}\,\mathrm{d}t",
             16, C_HIST),
            ("",
             r"\hat{\varphi}_X(t) = \tfrac{1}{N}\textstyle\sum_j e^{it z_j}"
             r"\quad\text{(empirical CF)}",
             15, C_MUTED),
        ])

        fp5 = self._formula_panel([
            ("aggregate over M directions",
             r"\mathrm{SIGReg}(Z) \triangleq"
             r"\frac{1}{M}\sum_{m=1}^{M} T\!\left(Z\,\boldsymbol{u}^{(m)}\right)",
             20, C_LABEL),
            ("",
             r"M = 1024 \;\text{(insensitive to choice of }M\text{)}", 15, C_MUTED),
        ])

        # ══════════════════════════════════════════════════════════════════════
        # PHASE 1 — Anisotropic cloud
        # ══════════════════════════════════════════════════════════════════════
        title1 = self._section_title("Latent space  Z  (anisotropic)")
        ellipse = Ellipse(width=7.8, height=1.65, color=C_EMBED, stroke_width=1.2) \
                      .set_fill(C_EMBED, opacity=0.07) \
                      .rotate(angle) \
                      .move_to([CLOUD_ORIGIN[0], CLOUD_ORIGIN[1], 0])
        dots = self._make_dots(pts)
        bad_label = MathTex(r"\neq \mathcal{N}(0,I)", color="#D97706", font_size=28) \
                        .next_to(ellipse, DOWN, buff=0.25)

        self.play(FadeIn(title1), FadeIn(fp1))
        self.play(
            Create(ellipse),
            LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.06),
        )
        self.play(FadeIn(bad_label))
        self.wait(0.6)
        self.play(FadeOut(bad_label), FadeOut(title1))

        # ══════════════════════════════════════════════════════════════════════
        # PHASE 2 — Sample one direction u^(1)
        # ══════════════════════════════════════════════════════════════════════
        title2 = self._section_title("Step 1 — Sample a random direction", color=C_DIR)

        arrow_end = CLOUD_ORIGIN + u * 2.8
        dir_arrow = Arrow(
            start=[CLOUD_ORIGIN[0], CLOUD_ORIGIN[1], 0],
            end=[arrow_end[0], arrow_end[1], 0],
            color=C_DIR, buff=0, stroke_width=3,
            max_tip_length_to_length_ratio=0.12,
        )
        dir_label = MathTex(r"\boldsymbol{u}^{(1)}", color=C_DIR, font_size=30) \
                        .next_to(dir_arrow.get_end(), UP + RIGHT, buff=0.1)

        self.play(FadeIn(title2), self._swap_formula(fp1, fp2))
        self.play(GrowArrow(dir_arrow), run_time=0.8)
        self.play(FadeIn(dir_label))
        self.wait(0.7)
        self.play(FadeOut(title2))

        # ══════════════════════════════════════════════════════════════════════
        # PHASE 3 — Project embeddings onto u^(1)
        # ══════════════════════════════════════════════════════════════════════
        title3 = self._section_title("Step 2 — Project  →  1-D scalars", color=C_PROJ)

        scalars = raw @ u
        proj_2d = np.outer(scalars, u) + CLOUD_ORIGIN

        perp_lines = VGroup(*[
            self._projection_line(pts[i], proj_2d[i])
            for i in range(N)
        ])
        proj_dots = VGroup(*[
            Dot(point=[proj_2d[i, 0], proj_2d[i, 1], 0],
                radius=0.055, color=C_PROJ)
            for i in range(N)
        ])

        self.play(FadeIn(title3), self._swap_formula(fp2, fp3))
        self.play(Create(perp_lines), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(d) for d in proj_dots], lag_ratio=0.04))
        self.wait(0.8)
        self.play(FadeOut(title3))

        # ══════════════════════════════════════════════════════════════════════
        # PHASE 4 — Test normality: histogram vs N(0,1) target
        # ══════════════════════════════════════════════════════════════════════
        title4 = self._section_title("Step 3 — Test normality of projection", color=C_HIST)

        hist_ax = Axes(
            x_range=[-4.5, 4.5, 1],
            y_range=[0, 0.55, 0.1],
            x_length=5.0,
            y_length=2.6,
            axis_config={"color": "#94A3B8", "stroke_width": 1.5},
            tips=False,
        ).to_corner(DR, buff=0.55)

        bin_edges = np.linspace(-4.5, 4.5, 10)
        counts, _ = np.histogram(scalars, bins=bin_edges, density=True)
        bw = bin_edges[1] - bin_edges[0]
        bar_pixel_w = hist_ax.x_axis.unit_size * bw * 0.82

        bars = VGroup()
        for k, val in enumerate(counts):
            cx = (bin_edges[k] + bin_edges[k + 1]) / 2
            h = hist_ax.y_axis.unit_size * float(val)
            bar = Rectangle(
                width=bar_pixel_w,
                height=max(h, 0.02),
                fill_color=C_HIST,
                fill_opacity=0.75,
                stroke_width=0,
            ).move_to(hist_ax.c2p(cx, 0) + UP * h / 2)
            bars.add(bar)

        gauss_curve = hist_ax.plot(
            lambda x: np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi),
            x_range=[-4.5, 4.5],
            color=C_GAUSS, stroke_width=3,
        )
        gauss_lbl = MathTex(r"\mathcal{N}(0,1)\;\text{target}", color=C_GAUSS, font_size=20) \
                        .next_to(hist_ax, UP, buff=0.12).shift(RIGHT * 0.6)
        gap_lbl = MathTex(r"T\!\left(\boldsymbol{h}^{(1)}\right)", color="#D97706", font_size=22) \
                      .next_to(hist_ax, LEFT, buff=0.2)

        self.play(FadeIn(title4), self._swap_formula(fp3, fp4))
        self.play(Create(hist_ax))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04))
        self.play(Create(gauss_curve), FadeIn(gauss_lbl))
        self.play(FadeIn(gap_lbl))
        self.wait(1.2)
        self.play(
            FadeOut(title4),
            FadeOut(perp_lines), FadeOut(proj_dots),
            FadeOut(hist_ax), FadeOut(bars), FadeOut(gauss_curve),
            FadeOut(gauss_lbl), FadeOut(gap_lbl),
            FadeOut(dir_arrow), FadeOut(dir_label),
        )

        # ══════════════════════════════════════════════════════════════════════
        # PHASE 5 — M directions fanned out
        # ══════════════════════════════════════════════════════════════════════
        title5 = self._section_title("SIGReg averages over  M  directions", color=C_DIR)

        n_spokes = 6
        spoke_angles = np.linspace(0, np.pi, n_spokes, endpoint=False)
        spokes = VGroup()
        for a in spoke_angles:
            dv = np.array([np.cos(a), np.sin(a)])
            for sign in (+1, -1):
                end = CLOUD_ORIGIN + sign * dv * 2.2
                spokes.add(Arrow(
                    start=[CLOUD_ORIGIN[0], CLOUD_ORIGIN[1], 0],
                    end=[end[0], end[1], 0],
                    color=C_DIR, buff=0, stroke_width=2,
                    max_tip_length_to_length_ratio=0.10,
                ))

        self.play(FadeIn(title5), self._swap_formula(fp4, fp5))
        self.play(LaggedStart(*[GrowArrow(s) for s in spokes], lag_ratio=0.08))
        self.wait(2.0)
        self.play(FadeOut(title5), FadeOut(fp5), FadeOut(spokes),
                  FadeOut(ellipse), *[FadeOut(d) for d in dots])
