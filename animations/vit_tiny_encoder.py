from manim import *
import numpy as np

# ── PushT geometry (shared with lewm_architecture.py) ─────────────────────────
GREEN_FILL, GREEN_STROKE = "#9FE6A0", "#5FB070"
GRAY_FILL,  GRAY_STROKE  = "#8194B4", "#5E6E8C"
EEF_BLUE = "#3B6FD6"

GOAL_POS  = np.array([ 0.16,  0.11, 0.0])
GOAL_ANG  = -16 * DEGREES
START_POS = np.array([-0.20, -0.17, 0.0])
START_ANG =  26 * DEGREES


def make_T(fill, stroke, opacity):
    pts = [[-0.6, 0.6, 0], [0.6, 0.6, 0], [0.6, 0.3, 0],
           [0.15, 0.3, 0], [0.15, -0.6, 0], [-0.15, -0.6, 0],
           [-0.15, 0.3, 0], [-0.6, 0.3, 0]]
    T = Polygon(*pts, stroke_color=stroke, stroke_width=2,
                fill_color=fill, fill_opacity=opacity)
    T.scale(0.30)
    return T


def make_pusht(progress):
    """PushT state centred near origin (no final shift)."""
    green = make_T(GREEN_FILL, GREEN_STROKE, 0.5)
    green.rotate(GOAL_ANG).shift(GOAL_POS)

    block_p = np.clip((progress - 0.3) / 0.7, 0.0, 1.0)
    pos = START_POS + (GOAL_POS - START_POS) * block_p
    ang = START_ANG + (GOAL_ANG - START_ANG) * block_p
    gray = make_T(GRAY_FILL, GRAY_STROKE, 1.0)
    gray.rotate(ang).shift(pos)

    push_dir = GOAL_POS - START_POS
    theta = np.arctan2(push_dir[1], push_dir[0])
    a = theta + np.clip(progress / 0.4, 0.0, 1.0) * np.pi
    eef = Dot(radius=0.05, color=EEF_BLUE, fill_opacity=1)
    eef.move_to(pos + 0.17 * np.array([np.cos(a), np.sin(a), 0.0]))

    return VGroup(green, gray, eef)


def pusht_scaled(img_center, img_size, progress=0.3):
    """PushT scene scaled to fit img_size and centred at img_center."""
    grp = make_pusht(progress)
    span = max(grp.get_width(), grp.get_height())
    if span > 0:
        grp.scale(img_size * 0.78 / span)
    grp.move_to(img_center)
    return grp


def make_cropped_patch_cell(scene_elems, grid_cell_center, grid_cell_size,
                            flat_center, flat_size, stroke_color="#2d2d2d"):
    """
    Crop scene_elems (positioned at image scale) to one grid cell, then
    translate + scale the result to flat_center / flat_size.
    """
    gc = np.array(grid_cell_center)
    hs = grid_cell_size / 2

    clip_rect = Rectangle(width=grid_cell_size, height=grid_cell_size,
                          fill_opacity=0, stroke_width=0).move_to(gc)

    cropped = VGroup()
    for elem in scene_elems:
        if isinstance(elem, Dot):
            dc = np.array(elem.get_center())
            if (gc[0] - hs <= dc[0] <= gc[0] + hs and
                    gc[1] - hs <= dc[1] <= gc[1] + hs):
                cropped.add(elem.copy())
        else:
            try:
                inter = Intersection(elem.copy(), clip_rect.copy())
                inter.set_fill(elem.get_fill_color(),
                               opacity=elem.get_fill_opacity())
                inter.set_stroke(elem.get_stroke_color(),
                                 width=elem.get_stroke_width(),
                                 opacity=elem.get_stroke_opacity())
                if inter.get_num_points() > 0:
                    cropped.add(inter)
            except Exception:
                pass

    # Move from grid-cell position to flat-patch position, then scale
    cropped.shift(np.array(flat_center) - gc)
    scale = flat_size / grid_cell_size
    cropped.scale(scale, about_point=np.array(flat_center))

    bg = Square(side_length=flat_size, fill_color=WHITE, fill_opacity=1,
                stroke_color=stroke_color, stroke_width=1.5).move_to(flat_center)
    return VGroup(bg, cropped)


class ViTTinyEncoder(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        Text.set_default(font="DejaVu Sans")

        TEXT_COLOR      = "#1a1a1a"
        BOX_STROKE      = "#2d2d2d"
        ARROW_COLOR     = "#444444"
        EMBED_COLOR     = "#E8704A"
        PE_COLOR        = "#5BA85A"
        CLS_COLOR       = "#7D3C98"
        TRANSFORMER_COLOR = "#2E4057"

        # ── Title ─────────────────────────────────────────────────────────────
        title = Text(
            "ViT-Tiny Encoder: Patch-based Image Encoding",
            font_size=26, color=TEXT_COLOR,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=0.8)
        self.wait(0.2)

        # ── Stage 1: Input PushT image ────────────────────────────────────────
        IMG_SIZE   = 2.0
        img_center = np.array([-5.0, -0.4, 0.0])

        img_border = Square(side_length=IMG_SIZE,
                            fill_color=WHITE, fill_opacity=1,
                            stroke_color=BOX_STROKE, stroke_width=2).move_to(img_center)
        img_state  = pusht_scaled(img_center, IMG_SIZE, progress=0.3)

        self.play(FadeIn(img_border), run_time=0.3)
        self.play(FadeIn(img_state), run_time=0.6)
        self.wait(0.4)

        # ── Stage 2: 3×3 grid overlay ─────────────────────────────────────────
        cell = IMG_SIZE / 3
        grid_lines = VGroup()
        lx, rx = img_center[0] - IMG_SIZE/2, img_center[0] + IMG_SIZE/2
        by, ty = img_center[1] - IMG_SIZE/2, img_center[1] + IMG_SIZE/2
        for i in [1, 2]:
            x = lx + i * cell
            grid_lines.add(Line([x, by, 0], [x, ty, 0],
                                stroke_color=BOX_STROKE, stroke_width=1.0))
            y = by + i * cell
            grid_lines.add(Line([lx, y, 0], [rx, y, 0],
                                stroke_color=BOX_STROKE, stroke_width=1.0))

        n_patches_label = MathTex(r"14 \times 14 \text{ patches}", font_size=15, color=TEXT_COLOR)
        n_patches_label.next_to(img_border, UP, buff=0.12)

        self.play(Create(grid_lines), FadeIn(n_patches_label), run_time=0.7)
        self.wait(0.4)

        # ── Stage 3: Flatten patches into a row ───────────────────────────────
        PATCH_SIZE = 0.54
        GAP        = 0.08
        flat_y     = -2.4
        N          = 9

        # Grid cell centres (row-major)
        grid_cell_centers = [
            np.array([lx + (col + 0.5) * cell, ty - (row + 0.5) * cell, 0.0])
            for row in range(3) for col in range(3)
        ]
        FLAT_X_OFFSET = 1.5
        flat_centers = [
            np.array([(i - 4) * (PATCH_SIZE + GAP) + FLAT_X_OFFSET, flat_y, 0.0])
            for i in range(N)
        ]

        # Build properly cropped flat patches using Intersection
        scene_elems = list(img_state)   # [green_T, gray_T, eef]
        flat_cells = VGroup(*[
            make_cropped_patch_cell(
                scene_elems=scene_elems,
                grid_cell_center=grid_cell_centers[i],
                grid_cell_size=cell,
                flat_center=flat_centers[i],
                flat_size=PATCH_SIZE,
            )
            for i in range(N)
        ])

        # Ghost outlines at grid positions (source for the fly-out animation)
        src_copies = VGroup(*[
            Square(side_length=cell, fill_color=WHITE, fill_opacity=0.4,
                   stroke_color="#888888", stroke_width=1.0).move_to(grid_cell_centers[i])
            for i in range(N)
        ])

        # Animate each patch flying from its grid position to the flat row
        self.play(
            LaggedStart(
                *[TransformFromCopy(src_copies[i], flat_cells[i]) for i in range(N)],
                lag_ratio=0.08,
            ),
            run_time=1.4,
        )
        self.wait(0.3)

        # ── Stage 4: E sweeps over flat patches → patch embeddings ───────────
        EMB_H = 0.42
        emb_y = -0.95

        embed_boxes = VGroup(*[
            Rectangle(width=PATCH_SIZE, height=EMB_H,
                      fill_color=EMBED_COLOR, fill_opacity=0.25,
                      stroke_color=EMBED_COLOR, stroke_width=2).move_to(
                np.array([(i - 4) * (PATCH_SIZE + GAP) + FLAT_X_OFFSET, emb_y, 0.0]))
            for i in range(N)
        ])

        # Pre-build per-token vector visuals (lines + ⋮) so they appear immediately
        N_VEC_LINES = 3
        token_visuals = []          # one VGroup per token: (lines, vdots)
        for box in embed_boxes:
            bc = box.get_center()
            bw = box.get_width() - 0.08
            bh = box.get_height()
            lines = VGroup(*[
                Line([bc[0] - bw/2, bc[1] - bh/2 + k*bh/(N_VEC_LINES+1), 0],
                     [bc[0] + bw/2, bc[1] - bh/2 + k*bh/(N_VEC_LINES+1), 0],
                     stroke_color=EMBED_COLOR, stroke_width=0.5, stroke_opacity=0.55)
                for k in range(1, N_VEC_LINES + 1)
            ])
            vdots = MathTex(r"\vdots", color=EMBED_COLOR, font_size=13)
            vdots.next_to(box, DOWN, buff=0.04)
            token_visuals.append(VGroup(lines, vdots))

        # Matrix E visual — a small kernel that slides over every flat patch
        E_W, E_H = PATCH_SIZE + 0.16, 0.68
        e_rect = RoundedRectangle(width=E_W, height=E_H, corner_radius=0.08,
                                  fill_color=EMBED_COLOR, fill_opacity=0.42,
                                  stroke_color=EMBED_COLOR, stroke_width=2.5)
        e_lbl = MathTex(r"E", font_size=22, color=BLACK)
        e_group = VGroup(e_rect, e_lbl)
        e_group.move_to(flat_centers[0])

        # Formula + D=192 stacked on the right
        formula = MathTex(
            r"z_i", r"=", r"E", r"\cdot", r"\mathrm{vec}(p_i)",
            font_size=22, color=TEXT_COLOR,
        )
        formula[0].set_color(EMBED_COLOR)
        formula[2].set_color(EMBED_COLOR)
        d_label = MathTex(r"D = 192", font_size=20, color=EMBED_COLOR)
        right_panel = VGroup(formula, d_label).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        right_panel.next_to(embed_boxes, RIGHT, buff=0.45)

        # Pre-build arrows so they can grow patch-by-patch during the E sweep
        proj_arrows = [
            Arrow(
                np.array([flat_centers[i][0], flat_y + PATCH_SIZE / 2 + 0.04, 0.0]),
                embed_boxes[i].get_bottom() + DOWN * 0.04,
                buff=0.0, stroke_color=BLACK, stroke_width=1.5,
                tip_length=0.12, color=BLACK,
            )
            for i in range(N)
        ]

        self.play(FadeIn(e_group), Write(formula), run_time=0.5)
        self.wait(0.15)

        # E slides patch-by-patch; arrow + embed box + vector lines appear together
        for i in range(N):
            if i > 0:
                self.play(e_group.animate.move_to(flat_centers[i]), run_time=0.20)
            self.play(
                GrowArrow(proj_arrows[i]),
                GrowFromCenter(embed_boxes[i]),
                FadeIn(token_visuals[i]),
                run_time=0.26,
            )

        self.play(FadeOut(e_group), run_time=0.35)
        self.play(Write(d_label), run_time=0.35)
        self.wait(0.3)

        # ── Stage 5: [CLS] token ──────────────────────────────────────────────
        cls_x   = embed_boxes[0].get_center()[0] - (PATCH_SIZE + GAP)
        cls_pos = np.array([cls_x, emb_y, 0.0])

        cls_box = Rectangle(width=PATCH_SIZE, height=EMB_H,
                            fill_color=CLS_COLOR, fill_opacity=0.25,
                            stroke_color=CLS_COLOR, stroke_width=2.5).move_to(cls_pos)
        cls_text  = Text("[CLS]", font_size=13, color=CLS_COLOR, weight=BOLD, font="DejaVu Sans").move_to(cls_pos)
        cls_label = Text("class token", font_size=14, color=CLS_COLOR)
        cls_label.next_to(cls_box, LEFT, buff=0.2)

        self.play(FadeIn(cls_box), Write(cls_text), run_time=0.7)
        self.play(FadeIn(cls_label), run_time=0.4)
        self.wait(0.3)

        # ── Stage 6: Positional encoding ──────────────────────────────────────
        all_token_boxes = [cls_box] + list(embed_boxes)
        N_tok = len(all_token_boxes)

        # Row of PE vectors sits above the embed row, with a 0.20-unit gap for "+"
        PE_BOX_H = EMB_H
        pe_y = emb_y + EMB_H / 2 + 0.20 + PE_BOX_H / 2   # ≈ −0.33

        pe_centers = [np.array([tok.get_center()[0], pe_y, 0.0]) for tok in all_token_boxes]

        pe_boxes = VGroup(*[
            Rectangle(width=PATCH_SIZE, height=PE_BOX_H,
                      fill_color=PE_COLOR, fill_opacity=0.20,
                      stroke_color=PE_COLOR, stroke_width=2).move_to(c)
            for c in pe_centers
        ])
        pe_labels = VGroup(*[
            MathTex(r"e_{" + str(i) + r"}", font_size=13, color=PE_COLOR).move_to(pe_centers[i])
            for i in range(N_tok)
        ])

        plus_y = (emb_y + EMB_H / 2 + pe_y - PE_BOX_H / 2) / 2
        plus_signs = VGroup(*[
            MathTex(r"+", font_size=16, color=PE_COLOR).move_to(
                np.array([tok.get_center()[0], plus_y, 0.0])
            )
            for tok in all_token_boxes
        ])

        pe_title = Text("Positional Encoding", font_size=15, color=PE_COLOR, weight=BOLD, font="DejaVu Sans")
        pe_title.next_to(pe_boxes, UP, buff=0.18)

        # Reuse the Stage-4 right-panel position for the PE formula
        pe_formula = MathTex(
            r"\mathbf{z}_i \leftarrow \mathbf{z}_i + e_i^{\mathrm{pos}}",
            font_size=18, color=PE_COLOR,
        )
        pe_dim = MathTex(
            r"E_{\mathrm{pos}} \in \mathbb{R}^{(N{+}1)\times 192}",
            font_size=14, color=PE_COLOR,
        )
        pe_right_panel = VGroup(pe_formula, pe_dim).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        pe_right_panel.move_to(right_panel.get_center())

        # Step 1: swap Stage-4 formula panel → PE boxes appear
        self.play(
            FadeOut(right_panel),
            FadeIn(pe_title),
            LaggedStart(*[FadeIn(pe_boxes[i]) for i in range(N_tok)], lag_ratio=0.05),
            LaggedStart(*[FadeIn(pe_labels[i]) for i in range(N_tok)], lag_ratio=0.05),
            run_time=0.8,
        )
        self.wait(0.2)

        # Step 2: "+" connectors and formula
        self.play(
            LaggedStart(*[FadeIn(plus_signs[i]) for i in range(N_tok)], lag_ratio=0.04),
            Write(pe_formula),
            run_time=0.7,
        )
        self.play(Write(pe_dim), run_time=0.4)
        self.wait(0.2)

        # Step 3: PE boxes collapse into tokens; tokens light up green
        self.play(
            *[pe_boxes[i].animate.move_to(all_token_boxes[i].get_center())
              for i in range(N_tok)],
            *[pe_labels[i].animate.move_to(all_token_boxes[i].get_center())
              for i in range(N_tok)],
            *[FadeOut(plus_signs[i]) for i in range(N_tok)],
            run_time=0.55,
        )
        self.play(
            *[FadeOut(pe_boxes[i]) for i in range(N_tok)],
            *[FadeOut(pe_labels[i]) for i in range(N_tok)],
            *[all_token_boxes[i].animate.set_stroke(color=PE_COLOR, width=3.5)
              for i in range(N_tok)],
            FadeOut(pe_title),
            FadeOut(pe_right_panel),
            run_time=0.4,
        )
        self.wait(0.3)

        # ── Stage 7: Transformer Encoder ──────────────────────────────────────
        # Width: from left edge of CLS to right edge of last patch token
        left_edge  = embed_boxes[0].get_left()[0] - (PATCH_SIZE + GAP)
        right_edge = embed_boxes[-1].get_right()[0]
        tok_width  = right_edge - left_edge
        tok_cx     = (left_edge + right_edge) / 2

        transformer_label    = Text("Transformer Encoder",                  font_size=16, color=TRANSFORMER_COLOR)
        transformer_sublabel = Text("ViT-Tiny: 12 layers, d=192, heads=3", font_size=13, color=TRANSFORMER_COLOR)
        label_group = VGroup(transformer_label, transformer_sublabel).arrange(DOWN, buff=0.12)

        box_height = label_group.get_height() + 0.3
        transformer_box = RoundedRectangle(
            width=tok_width, height=box_height, corner_radius=0.2,
            fill_color=TRANSFORMER_COLOR, fill_opacity=0.12,
            stroke_color=TRANSFORMER_COLOR, stroke_width=2.5,
        ).move_to(np.array([tok_cx, 0.0, 0.0]))

        label_group.move_to(transformer_box.get_center())

        up_arrows = VGroup(*[
            Arrow(
                tok.get_top() + UP * 0.05,
                transformer_box.get_bottom()
                + RIGHT * (tok.get_center()[0] - transformer_box.get_center()[0]),
                buff=0.05, stroke_color=ARROW_COLOR, stroke_width=1.2,
                tip_length=0.10, color=ARROW_COLOR,
                max_stroke_width_to_length_ratio=999,
            )
            for tok in all_token_boxes
        ])

        self.play(LaggedStart(*[GrowArrow(a) for a in up_arrows], lag_ratio=0.04), run_time=0.8)
        self.play(FadeIn(transformer_box), Write(transformer_label), run_time=0.9)
        self.play(FadeIn(transformer_sublabel), run_time=0.5)
        self.wait(0.3)

        # ── Stage 8: Extract [CLS] token ──────────────────────────────────────
        top_c = transformer_box.get_top()

        cls_extract_arrow = Arrow(
            top_c + UP * 0.05, top_c + UP * 0.30,
            buff=0.0, stroke_color=ARROW_COLOR, stroke_width=2.0,
            tip_length=0.14, color=ARROW_COLOR,
        )
        cls_out_box = Rectangle(
            width=PATCH_SIZE * 1.8, height=EMB_H,
            fill_color=CLS_COLOR, fill_opacity=0.25,
            stroke_color=CLS_COLOR, stroke_width=2.5,
        ).move_to(top_c + UP * (0.30 + 0.05 + EMB_H / 2))
        cls_out_text = Text("[CLS]", font_size=13, color=CLS_COLOR, weight=BOLD, font="DejaVu Sans").move_to(cls_out_box)
        cls_extract_label = Text("extract [CLS] token", font_size=13, color=CLS_COLOR)
        cls_extract_label.next_to(cls_out_box, RIGHT, buff=0.2)

        self.play(GrowArrow(cls_extract_arrow), run_time=0.4)
        self.play(FadeIn(cls_out_box), Write(cls_out_text), run_time=0.6)
        self.play(FadeIn(cls_extract_label), run_time=0.4)
        self.wait(0.3)

        # ── Stage 9: 1-layer MLP + BatchNorm → z_t ────────────────────────────
        MLP_COLOR = "#C0392B"
        cls_top = cls_out_box.get_top()

        mlp_arrow = Arrow(
            cls_top + UP * 0.05, cls_top + UP * 0.25,
            buff=0.0, stroke_color=ARROW_COLOR, stroke_width=2.0,
            tip_length=0.14, color=ARROW_COLOR,
        )
        mlp_box = RoundedRectangle(
            width=3.0, height=0.62, corner_radius=0.15,
            fill_color=MLP_COLOR, fill_opacity=0.12,
            stroke_color=MLP_COLOR, stroke_width=2.5,
        ).move_to(cls_top + UP * (0.25 + 0.05 + 0.31))
        mlp_label = Text("1-layer MLP + BatchNorm", font_size=13, color=MLP_COLOR).move_to(mlp_box)
        mlp_side_label = Text("(LeWM-specific projection)", font_size=11, color=MLP_COLOR)
        mlp_side_label.next_to(mlp_box, RIGHT, buff=0.2)

        mlp_top = mlp_box.get_top()
        mlp_out_arrow = Arrow(
            mlp_top + UP * 0.05, mlp_top + UP * 0.25,
            buff=0.0, stroke_color=ARROW_COLOR, stroke_width=2.0,
            tip_length=0.14, color=ARROW_COLOR,
        )
        latent_box = RoundedRectangle(
            width=3.0, height=0.62, corner_radius=0.15,
            fill_color=EMBED_COLOR, fill_opacity=0.20,
            stroke_color=EMBED_COLOR, stroke_width=2.5,
        ).move_to(mlp_top + UP * (0.25 + 0.05 + 0.31))
        latent_label = MathTex(r"z_t \in \mathbb{R}^{D}", color=EMBED_COLOR, font_size=24)
        latent_label.move_to(latent_box)
        latent_desc = Text("final latent", font_size=13, color=EMBED_COLOR)
        latent_desc.next_to(latent_box, RIGHT, buff=0.2)

        self.play(GrowArrow(mlp_arrow), run_time=0.4)
        self.play(FadeIn(mlp_box), Write(mlp_label), run_time=0.7)
        self.play(FadeIn(mlp_side_label), run_time=0.4)
        self.play(GrowArrow(mlp_out_arrow), run_time=0.4)
        self.play(FadeIn(latent_box), Write(latent_label), FadeIn(latent_desc), run_time=0.8)
        self.wait(1.5)
