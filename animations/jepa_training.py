from manim import *
import numpy as np


class JEPATraining(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        TEXT_COLOR    = "#1a1a1a"
        ARROW_COLOR   = "#444444"
        EMBED_COLOR   = "#4A90D9"
        PRED_COLOR    = "#E8704A"
        LATENT_COLOR  = "#7B1FA2"
        NODE_FILL     = "#f0f0f0"
        NODE_STROKE   = "#2d2d2d"

        # Layout constants
        ENC_Y   = -0.50
        Z_Y     =  0.78
        PRED_Y  =  1.90
        FRAME_Y = -2.70

        # ── Title ──────────────────────────────────────────────────────────────
        title = Text(
            "Joint Embedding Predictive Architecture (JEPA)",
            font_size=28, color=TEXT_COLOR,
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)

        # ── Helper: neural-net icon ────────────────────────────────────────────
        def make_nn(layers=(3, 4, 3), node_r=0.13, h_gap=0.55, v_gap=0.32):
            grp = VGroup()
            node_cols = []
            for col_i, n in enumerate(layers):
                col = VGroup()
                for row_i in range(n):
                    c = Circle(radius=node_r, fill_color=NODE_FILL,
                               fill_opacity=1, stroke_color=NODE_STROKE,
                               stroke_width=1.5)
                    c.move_to(RIGHT * col_i * h_gap +
                              UP * (row_i - (n - 1) / 2) * v_gap)
                    col.add(c)
                node_cols.append(col)
                grp.add(col)
            edges = VGroup()
            for i in range(len(node_cols) - 1):
                for a in node_cols[i]:
                    for b in node_cols[i + 1]:
                        edges.add(Line(a.get_center(), b.get_center(),
                                       stroke_color=NODE_STROKE,
                                       stroke_width=0.8, stroke_opacity=0.5))
            grp.add(edges)
            return grp

        # ── Helper: stacked video frames with real images ──────────────────────
        ASSETS = "/Users/julian/Documents/tum/lewm-seminar/assets"

        def make_image_frame(path, anchor, fw=1.5):
            img = ImageMobject(path)
            img.set_width(fw)
            img.move_to(anchor)
            return Group(img)

        def make_frame_stack(anchor, img_paths, n_behind=2, fw=1.5):
            """Front image at anchor; ghost frames behind-right use earlier imgs."""
            stack = Group()
            for i in range(n_behind, 0, -1):
                offset = RIGHT * 0.11 * i + DOWN * 0.08 * i
                ghost = make_image_frame(img_paths[-(i + 1)],
                                         anchor + offset, fw)
                ghost.set_opacity(0.45 + 0.20 * (n_behind - i))
                stack.add(ghost)
            stack.add(make_image_frame(img_paths[-1], anchor, fw))
            return stack

        # ── Encoders ───────────────────────────────────────────────────────────
        enc_left = make_nn().move_to(LEFT * 3.5 + UP * ENC_Y)
        enc_label_left = Tex(r"\textbf{\textsc{Encoder}}",
                             color=TEXT_COLOR, font_size=22)
        enc_label_left.next_to(enc_left, LEFT, buff=0.2)

        enc_right = make_nn().move_to(RIGHT * 3.5 + UP * ENC_Y)
        enc_label_right = Tex(r"\textbf{\textsc{Encoder}}",
                              color=TEXT_COLOR, font_size=22)
        enc_label_right.next_to(enc_right, RIGHT, buff=0.2)

        # ── Video / goal frames ────────────────────────────────────────────────
        context_imgs = [f"{ASSETS}/ur_frame_0.png",
                        f"{ASSETS}/ur_frame_1.png"]
        frame_left  = make_frame_stack(LEFT  * 3.5 + UP * FRAME_Y,
                                       img_paths=context_imgs, n_behind=1)
        frame_right = make_frame_stack(RIGHT * 3.5 + UP * FRAME_Y,
                                       img_paths=[f"{ASSETS}/ur_goal.png"], n_behind=0)

        video_label = Tex(r"\textbf{Video}", color=TEXT_COLOR, font_size=20)
        video_label.next_to(frame_left, DOWN, buff=0.18)

        goal_label = Tex(r"\textbf{Goal State}", color=TEXT_COLOR, font_size=20)
        goal_label.next_to(frame_right, DOWN, buff=0.18)

        # ── Predictor ──────────────────────────────────────────────────────────
        pred_nn = make_nn(layers=(3, 4, 3)).move_to(UP * PRED_Y)
        pred_label = Tex(r"\textbf{\textsc{Predictor}}",
                         color=TEXT_COLOR, font_size=22)
        pred_label.next_to(pred_nn, UP, buff=0.2)

        # ── Vector comparison ──────────────────────────────────────────────────
        vcenter = RIGHT * 3.5 + UP * PRED_Y

        pred_vec = MathTex(r"\mathtt{[0.05,\ -0.02,\ ...,\ 0.50]}",
                           color=PRED_COLOR, font_size=22
                           ).move_to(vcenter + UP * 0.32)
        pred_vec_label = Tex(r"\textbf{Predicted Embedding}",
                             color=PRED_COLOR, font_size=18
                             ).next_to(pred_vec, RIGHT, buff=0.15)

        goal_vec = MathTex(r"\mathtt{[0.12,\ \ 0.08,\ ...,\ 0.37]}",
                           color=EMBED_COLOR, font_size=22
                           ).move_to(vcenter + DOWN * 0.32)
        goal_vec_label = Tex(r"\textbf{Goal Embedding}",
                             color=EMBED_COLOR, font_size=18
                             ).next_to(goal_vec, RIGHT, buff=0.15)

        # ── Arrows ─────────────────────────────────────────────────────────────
        def make_arrow(start, end, color=ARROW_COLOR):
            return Arrow(start, end, buff=0.15,
                         stroke_color=color, stroke_width=2.5,
                         tip_length=0.22,
                         max_tip_length_to_length_ratio=1.0,
                         color=color)

        # Force vertical alignment using encoder x-center
        lx = enc_left.get_center()[0]
        rx = enc_right.get_center()[0]
        arr_frame_left  = make_arrow(
            np.array([lx, frame_left.get_top()[1],  0]),
            np.array([lx, enc_left.get_bottom()[1], 0]),
        )
        arr_frame_right = make_arrow(
            np.array([rx, frame_right.get_top()[1],  0]),
            np.array([rx, enc_right.get_bottom()[1], 0]),
        )
        arr_enc_left_pred     = make_arrow(enc_left.get_top(),      pred_nn.get_left())
        arr_pred_to_compare   = make_arrow(pred_nn.get_right(),     pred_vec.get_left())
        arr_enc_right_compare = make_arrow(enc_right.get_top(),     goal_vec.get_bottom())

        # Latent variable: dot + label below predictor
        latent_dot = Dot(radius=0.14, color=LATENT_COLOR, fill_opacity=1)
        latent_dot.move_to(DOWN * 0.10)
        latent_var = Tex(r"\textbf{Latent Variable}", color=LATENT_COLOR, font_size=20)
        latent_var.next_to(latent_dot, DOWN, buff=0.15)
        arr_latent_pred = make_arrow(latent_dot.get_top(), pred_nn.get_bottom())

        # ── Stage 1: frames appear ────────────────────────────────────────────
        self.play(
            LaggedStart(
                AnimationGroup(FadeIn(frame_left),  FadeIn(video_label)),
                AnimationGroup(FadeIn(frame_right), FadeIn(goal_label)),
                lag_ratio=0.3,
            ),
            run_time=1.0,
        )
        self.wait(0.2)

        # ── Stage 2: encoders ────────────────────────────────────────────────
        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(arr_frame_left),
                               Create(enc_left), FadeIn(enc_label_left)),
                AnimationGroup(GrowArrow(arr_frame_right),
                               Create(enc_right), FadeIn(enc_label_right)),
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )
        self.wait(0.3)

        # ── Stage 3: predictor ───────────────────────────────────────────────
        self.play(
            GrowArrow(arr_enc_left_pred),
            Create(pred_nn),
            FadeIn(pred_label),
            run_time=1.0,
        )
        self.play(
            FadeIn(latent_dot),
            FadeIn(latent_var),
            GrowArrow(arr_latent_pred),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                GrowArrow(arr_pred_to_compare),
                GrowArrow(arr_enc_right_compare),
                lag_ratio=0.4,
            ),
            run_time=0.9,
        )
        self.wait(0.3)

        # ── Stage 4: vector comparison ───────────────────────────────────────
        self.play(
            LaggedStart(
                AnimationGroup(FadeIn(pred_vec), FadeIn(pred_vec_label)),
                AnimationGroup(FadeIn(goal_vec), FadeIn(goal_vec_label)),
                lag_ratio=0.5,
            ),
            run_time=0.9,
        )
        self.wait(0.4)
        self.wait(1.0)
