from manim import *
import numpy as np

config.background_color = WHITE
config.frame_width  = 13
config.frame_height = 9


class AdaLNTransformerBlock(Scene):
    """
    Static landscape figure — AdaLN-Zero block matching the reference ViT diagram.
    Conditioning arrows use a vertical bus so nothing crosses.

    Render:
        uv run manim -s -r 1300,900 animations/adaln_block.py AdaLNTransformerBlock
    """

    # ── Palette ────────────────────────────────────────────────────────────
    ADALN_F, ADALN_S = "#FEF08A", "#A16207"
    MHA_F,   MHA_S   = "#DCFCE7", "#166534"
    MLP_F,   MLP_S   = "#DBEAFE", "#1E40AF"
    PAT_F,   PAT_S   = "#FFE4E6", "#9F1239"
    BG_F,    BG_S    = "#E5E7EB", "#6B7280"
    ACT_F,   ACT_S   = "#EDE9FE", "#5B21B6"
    MOD_C            = "#5B21B6"
    GATE_C           = "#B91C1C"
    TEXT_C           = "#111827"

    # ── Transformer column ─────────────────────────────────────────────────
    TX = 3.5      # center x
    BW = 2.7      # block width
    BH = 0.60     # standard block height

    YP  = -4.00   # Embedded Patches (outside block, moved down)
    YN1 = -2.80   # AdaLN 1
    YM  = -1.56   # Multi-Head Attention
    YA1 = -0.34   # add circle 1
    YN2 =  0.74   # AdaLN 2
    YL  =  1.84   # MLP
    YA2 =  2.92   # add circle 2

    # ── Conditioning column ────────────────────────────────────────────────
    # Bus line: single vertical at x=BX; horizontal branches for each target.
    AX  = -3.2    # Mod.MLP + action box center x
    BX  =  0.4    # bus line x (gap between action side and block)

    # ── Helpers ────────────────────────────────────────────────────────────
    def _box(self, label, fill, stroke, w=None, h=None, fsize=22):
        w = w or self.BW
        h = h or self.BH
        r = RoundedRectangle(width=w, height=h, corner_radius=0.18,
                             fill_color=fill, fill_opacity=0.95,
                             stroke_color=stroke, stroke_width=2.5)
        lines = label.split("\n")
        t = VGroup(*[Text(l, font_size=fsize, color=self.TEXT_C) for l in lines]
                   ).arrange(DOWN, aligned_edge=ORIGIN, buff=0.06).move_to(r)
        return VGroup(r, t)

    def _add_circle(self, pos):
        c = Circle(radius=0.28, fill_color=WHITE, fill_opacity=1,
                   stroke_color=self.TEXT_C, stroke_width=2.5).move_to(pos)
        p = Text("+", font_size=28, weight=BOLD, color=self.TEXT_C).move_to(c)
        return VGroup(c, p)

    # Shared arrow style — applied everywhere for visual consistency
    TIP = 0.18
    RATIO = 0.99   # prevent Manim from auto-shrinking tips on short arrows

    def _va(self, from_mob, to_mob):
        return Arrow(from_mob.get_top(), to_mob.get_bottom(),
                     buff=0.09, stroke_width=2.5, color=self.TEXT_C,
                     tip_length=self.TIP, max_tip_length_to_length_ratio=self.RATIO)

    def _skip(self, from_right, to_right):
        rx = self.TX + self.BW / 2 + 0.22
        a = np.array([from_right[0], from_right[1], 0])
        b = np.array([to_right[0],   to_right[1],   0])
        return VGroup(
            Line(a,            [rx, a[1], 0], stroke_width=2.5, color=self.TEXT_C),
            Line([rx, a[1], 0],[rx, b[1], 0], stroke_width=2.5, color=self.TEXT_C),
            Arrow([rx, b[1], 0], b, buff=0.0, stroke_width=2.5, color=self.TEXT_C,
                  tip_length=self.TIP, max_tip_length_to_length_ratio=self.RATIO),
        )

    def _branch(self, target_y, target_x, color):
        """Horizontal arrow from bus (BX, target_y) → (target_x, target_y)."""
        return Arrow(
            [self.BX, target_y, 0], [target_x, target_y, 0],
            buff=0.09, stroke_width=2.5, color=color,
            tip_length=self.TIP, max_tip_length_to_length_ratio=self.RATIO,
        )

    # ── construct ──────────────────────────────────────────────────────────
    def construct(self):
        Text.set_default(font="DejaVu Sans")
        TX, BX, AX = self.TX, self.BX, self.AX

        # ── Block background ───────────────────────────────────────────────
        blk_top = self.YA2 + 0.88
        blk_bot = self.YN1 - 0.42
        blk_cy  = (blk_top + blk_bot) / 2
        blk_h   = blk_top - blk_bot

        bg = RoundedRectangle(
            width=self.BW + 1.05, height=blk_h, corner_radius=0.38,
            fill_color=self.BG_F, fill_opacity=0.90,
            stroke_color=self.BG_S, stroke_width=2.5,
        ).move_to([TX, blk_cy, 0])
        lx = Text("L ×", font_size=19, color="#6B7280").move_to(
            bg.get_corner(UL) + [0.35, -0.22, 0])

        # ── Transformer elements ───────────────────────────────────────────
        patches = self._box("Embedded\nPatches", self.PAT_F, self.PAT_S,
                            w=self.BW - 0.2, h=0.80, fsize=20
                            ).move_to([TX, self.YP, 0])
        adaln1  = self._box("AdaLN", self.ADALN_F, self.ADALN_S, fsize=23
                            ).move_to([TX, self.YN1, 0])
        mha     = self._box("Multi-Head\nAttention", self.MHA_F, self.MHA_S,
                            h=0.88, fsize=21).move_to([TX, self.YM, 0])
        add1    = self._add_circle([TX, self.YA1, 0])
        adaln2  = self._box("AdaLN", self.ADALN_F, self.ADALN_S, fsize=23
                            ).move_to([TX, self.YN2, 0])
        mlp     = self._box("MLP", self.MLP_F, self.MLP_S, fsize=23
                            ).move_to([TX, self.YL, 0])
        add2    = self._add_circle([TX, self.YA2, 0])

        # Vertical arrows (main flow)
        in_arr  = self._va(patches, adaln1)
        dx = 0.40
        qkv = VGroup(*[
            Arrow(adaln1.get_top() + [d, 0, 0], mha.get_bottom() + [d, 0, 0],
                  buff=0.09, stroke_width=2.5, color=self.TEXT_C,
                  tip_length=self.TIP, max_tip_length_to_length_ratio=self.RATIO)
            for d in [-dx, 0, dx]
        ])
        va_m2a1 = self._va(mha,    add1)
        va_a2n  = self._va(add1,   adaln2)
        va_n2l  = self._va(adaln2, mlp)
        va_l2a  = self._va(mlp,    add2)
        out_arr = Arrow(add2.get_top(), [TX, blk_top + 0.25, 0],
                        buff=0.0, stroke_width=2.5, color=self.TEXT_C,
                        tip_length=self.TIP, max_tip_length_to_length_ratio=self.RATIO)

        skip1 = self._skip(patches[0].get_right(), add1[0].get_right())
        skip2 = self._skip(add1[0].get_right(),    add2[0].get_right())

        # ── Conditioning (left side) ───────────────────────────────────────
        # ── Left column: a_t → Embedder → c → Mod. MLP ───────────────────
        # Positions chosen so everything sits in the upper-left with room to breathe

        # Mod. MLP box (simple, formula lives above it)
        mod_box = self._box("Mod. MLP\n(SiLU + Linear)", self.ACT_F, self.ACT_S,
                            w=2.3, h=0.82, fsize=19).move_to([AX, 0.05, 0])

        # Embedder box
        act_box = self._box("Embedder\n(Conv1d + SiLU)", self.ACT_F, self.ACT_S,
                            w=2.3, h=0.85, fsize=19).move_to([AX, -1.55, 0])

        # Arrow Embedder → Mod. MLP, labelled "c"
        arr_a2m = Arrow(act_box.get_top(), mod_box.get_bottom(),
                        buff=0.09, stroke_width=2.5, color=self.TEXT_C,
                        tip_length=self.TIP, max_tip_length_to_length_ratio=self.RATIO)
        c_label = MathTex(r"c", font_size=22, color=self.TEXT_C).move_to(
            arr_a2m.get_center() + np.array([0.28, 0, 0]))

        # a_t label + arrow into Embedder
        at_label = MathTex(r"a_t", font_size=28, color=self.TEXT_C
                           ).next_to(act_box, DOWN, buff=0.55)
        at_arrow = Arrow(at_label.get_top() + UP * 0.05, act_box.get_bottom(),
                         buff=0.08, stroke_width=2.5, color=self.TEXT_C,
                         tip_length=self.TIP, max_tip_length_to_length_ratio=self.RATIO)

        zero_ann = VGroup()   # now inside formula

        # Arrow from Mod.MLP right edge → bus, at mod_box center y
        mod_r_pt = mod_box.get_right()
        arr_m2bus = Line(
            [mod_r_pt[0], mod_r_pt[1], 0], [BX, mod_r_pt[1], 0],
            stroke_width=2.5, color=self.MOD_C,
        )

        # ── Vertical bus line ──────────────────────────────────────────────
        # Spans from just below adaln1 to just above add2.
        bus_bot = self.YN1 - 0.05
        bus_top = self.YA2 + 0.05
        bus_line = Line([BX, bus_bot, 0], [BX, bus_top, 0],
                        stroke_width=2.5, color=self.MOD_C)

        # Junction dot where Mod.MLP connects to bus
        junction = Dot([BX, mod_r_pt[1], 0], radius=0.08, color=self.MOD_C)

        # ── 4 horizontal branch arrows from bus to targets ─────────────────
        # Order (bottom → top): Δ₁Σ₁→adaln1, G₁→add1, Δ₂Σ₂→adaln2, G₂→add2
        adaln1_lx = TX - self.BW / 2   # left edge of adaln boxes
        adaln2_lx = adaln1_lx
        add1_lx   = TX - 0.28          # left edge of add circles
        add2_lx   = TX - 0.28

        br_ds1 = self._branch(self.YN1, adaln1_lx, self.MOD_C)
        br_g1  = self._branch(self.YA1, add1_lx,   self.GATE_C)
        br_ds2 = self._branch(self.YN2, adaln2_lx, self.MOD_C)
        br_g2  = self._branch(self.YA2, add2_lx,   self.GATE_C)

        # Coloured junction dots on bus where each branch leaves
        dots = VGroup(*[
            Dot([BX, y, 0], radius=0.07, color=col)
            for y, col in [
                (self.YN1, self.MOD_C),
                (self.YA1, self.GATE_C),
                (self.YN2, self.MOD_C),
                (self.YA2, self.GATE_C),
            ]
        ])

        # Branch labels (above each horizontal arrow, between bus and target)
        def _lbl(tex, color, y, x_mid, below=False):
            offset = -0.30 if below else 0.30
            return MathTex(tex, font_size=21, color=color).move_to([x_mid, y + offset, 0])

        gray_lx = TX - (self.BW + 1.05) / 2   # left edge of gray background box
        mid_ada = (BX + gray_lx) / 2
        mid_add = (BX + gray_lx) / 2

        lbl_ds1 = _lbl(r"\Delta_{\rm attn},\Sigma_{\rm attn}", self.MOD_C,  self.YN1, mid_ada)
        lbl_g1  = _lbl(r"G_{\rm attn}",                       self.GATE_C, self.YA1, mid_add)
        lbl_ds2 = _lbl(r"\Delta_{\rm mlp},\Sigma_{\rm mlp}",  self.MOD_C,  self.YN2, mid_ada)
        lbl_g2  = _lbl(r"G_{\rm mlp}",                        self.GATE_C, self.YA2, mid_add, below=True)

        # ── Title ──────────────────────────────────────────────────────────
        title = Text("AdaLN-Zero Transformer Block",
                     font_size=26, weight=BOLD, color=self.TEXT_C
                     ).move_to([TX, blk_top + 0.50, 0])

        # ── Legend ─────────────────────────────────────────────────────────
        def _leg(line_col, txt):
            return VGroup(
                Line(ORIGIN, RIGHT*0.45, stroke_width=3, color=line_col),
                Text(txt, font_size=16, color=line_col),
            ).arrange(RIGHT, buff=0.12)

        legend = VGroup(
            _leg(self.MOD_C,  "  Δ, Σ  (shift + scale)  →  AdaLN"),
            _leg(self.GATE_C, "  G  (gate)  →  residual ×G"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.45)

        # ── Compose ────────────────────────────────────────────────────────
        self.add(
            # transformer
            bg, lx,
            patches, in_arr,
            adaln1, qkv, mha, va_m2a1,
            add1, skip1,
            va_a2n, adaln2, va_n2l, mlp, va_l2a,
            add2, skip2, out_arr,
            # conditioning
            mod_box, arr_a2m, c_label, act_box, at_arrow, at_label,
            arr_m2bus, bus_line, junction,
            br_ds1, br_g1, br_ds2, br_g2,
            dots,
            lbl_ds1, lbl_g1, lbl_ds2, lbl_g2,
            # title + legend
            title, legend,
        )
