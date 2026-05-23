from manim import *


class JEPATraining(Scene):
    def construct(self):
        # White background
        self.camera.background_color = WHITE

        # Colors
        TEXT_COLOR = "#1a1a1a"
        BOX_COLOR = "#2d2d2d"
        ARROW_COLOR = "#444444"
        EMBED_COLOR = "#4A90D9"
        PRED_COLOR = "#E8704A"
        LOSS_COLOR = "#5BA85A"
        NODE_FILL = "#f0f0f0"
        NODE_STROKE = "#2d2d2d"

        # ── Title ──────────────────────────────────────────────────────────────
        title = Text(
            "Joint Embedding Predictive Architecture (JEPA)",
            font_size=28,
            color=TEXT_COLOR,
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)

        # ── Helper: draw a small neural-net icon ───────────────────────────────
        def make_nn(layers=(3, 4, 3), node_r=0.13, h_gap=0.55, v_gap=0.32,
                    fill=NODE_FILL, stroke=NODE_STROKE):
            """Returns a VGroup of nodes + edges for a small NN diagram."""
            grp = VGroup()
            node_cols = []
            for col_i, n in enumerate(layers):
                col = VGroup()
                for row_i in range(n):
                    c = Circle(radius=node_r, fill_color=fill,
                               fill_opacity=1, stroke_color=stroke,
                               stroke_width=1.5)
                    c.move_to(
                        RIGHT * col_i * h_gap +
                        UP * (row_i - (n - 1) / 2) * v_gap
                    )
                    col.add(c)
                node_cols.append(col)
                grp.add(col)
            # edges
            edges = VGroup()
            for i in range(len(node_cols) - 1):
                for a in node_cols[i]:
                    for b in node_cols[i + 1]:
                        e = Line(a.get_center(), b.get_center(),
                                 stroke_color=stroke, stroke_width=0.8,
                                 stroke_opacity=0.5)
                        edges.add(e)
            grp.add(edges)
            return grp

        # ── Encoder left (context) ─────────────────────────────────────────────
        enc_left = make_nn()
        enc_left.move_to(LEFT * 3.5 + DOWN * 0.8)

        obs_left = MathTex(r"x(t)", color=TEXT_COLOR, font_size=36)
        obs_left.next_to(enc_left, DOWN, buff=0.3)
        obs_label_left = Tex(r"\textbf{\textsc{Observation}}", color=TEXT_COLOR, font_size=22)
        obs_label_left.next_to(obs_left, DOWN, buff=0.1)
        enc_label_left = Tex(r"\textbf{\textsc{Encoder}}", color=TEXT_COLOR, font_size=22)
        enc_label_left.next_to(enc_left, LEFT, buff=0.2)

        # ── Encoder right (target) ─────────────────────────────────────────────
        enc_right = make_nn()
        enc_right.move_to(RIGHT * 3.5 + DOWN * 0.8)

        obs_right = MathTex(r"x(t+1)", color=TEXT_COLOR, font_size=36)
        obs_right.next_to(enc_right, DOWN, buff=0.3)
        obs_label_right = Tex(r"\textbf{\textsc{Observation}}", color=TEXT_COLOR, font_size=22)
        obs_label_right.next_to(obs_right, DOWN, buff=0.1)
        enc_label_right = Tex(r"\textbf{\textsc{Encoder}}", color=TEXT_COLOR, font_size=22)
        enc_label_right.next_to(enc_right, RIGHT, buff=0.2)

        # ── Predictor (centre-top) ─────────────────────────────────────────────
        pred_nn = make_nn(layers=(3, 4, 3))
        pred_nn.move_to(UP * 1.3)
        pred_label = Tex(r"\textbf{\textsc{Predictor}}", color=TEXT_COLOR, font_size=22)
        pred_label.next_to(pred_nn, UP, buff=0.2)

        # ── Loss box ──────────────────────────────────────────────────────────
        loss_box = RoundedRectangle(
            width=2.6, height=0.9,
            corner_radius=0.15,
            fill_color="#f8f8f8",
            fill_opacity=1,
            stroke_color=BOX_COLOR,
            stroke_width=2,
        ).move_to(RIGHT * 3.5 + UP * 1.3)
        loss_text = MathTex(
            r"\min\,d\!\left(z(t{+}1),\, \hat{z}(t{+}1)\right)",
            color=TEXT_COLOR, font_size=20,
        )
        loss_text.move_to(loss_box.get_center())

        # ── Latent embedding dots ──────────────────────────────────────────────
        def latent_dot(color):
            return Dot(radius=0.12, color=color, fill_opacity=1)

        # z_ctx sits directly above enc_left; z_tgt directly above enc_right
        z_ctx = latent_dot(EMBED_COLOR).move_to(LEFT * 3.5 + UP * 0.5)
        z_tgt = latent_dot(EMBED_COLOR).move_to(RIGHT * 3.5 + UP * 0.5)
        z_pred = latent_dot(PRED_COLOR).move_to(RIGHT * 1.6 + UP * 1.3)

        z_ctx_label = MathTex(r"z(t)", color=EMBED_COLOR, font_size=26)
        z_ctx_label.next_to(z_ctx, LEFT, buff=0.15)
        z_tgt_label = MathTex(r"z(t+1)", color=EMBED_COLOR, font_size=26)
        z_tgt_label.next_to(z_tgt, RIGHT, buff=0.15)
        z_pred_label = MathTex(r"\hat{z}(t+1)", color=PRED_COLOR, font_size=26)
        z_pred_label.next_to(z_pred, DOWN, buff=0.12)

        # ── Arrows ────────────────────────────────────────────────────────────
        def make_arrow(start, end, color=ARROW_COLOR):
            return Arrow(
                start, end, buff=0.15,
                stroke_color=color, stroke_width=2.5,
                tip_length=0.18, max_stroke_width_to_length_ratio=999,
                color=color,
            )

        arr_obs_left = make_arrow(obs_left.get_top(), enc_left.get_bottom())
        arr_obs_right = make_arrow(obs_right.get_top(), enc_right.get_bottom())

        # Encoders → latent dots: straight up
        arr_enc_left_z = make_arrow(enc_left.get_top(), z_ctx.get_bottom())
        arr_enc_right_z = make_arrow(enc_right.get_top(), z_tgt.get_bottom())

        arr_z_pred_input = make_arrow(z_ctx.get_right(), pred_nn.get_left())
        arr_pred_z_out = make_arrow(pred_nn.get_right(), z_pred.get_left())

        # ── Stage 1: Observations & Encoders ─────────────────────────────────
        self.play(
            LaggedStart(
                AnimationGroup(FadeIn(obs_left), FadeIn(obs_label_left)),
                AnimationGroup(FadeIn(obs_right), FadeIn(obs_label_right)),
                lag_ratio=0.3,
            ),
            run_time=0.8,
        )
        self.wait(0.2)

        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(arr_obs_left), Create(enc_left),
                               FadeIn(enc_label_left)),
                AnimationGroup(GrowArrow(arr_obs_right), Create(enc_right),
                               FadeIn(enc_label_right)),
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )
        self.wait(0.3)

        # ── Stage 2: Latent embeddings flow out ──────────────────────────────
        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(arr_enc_left_z),
                               FadeIn(z_ctx), Write(z_ctx_label)),
                AnimationGroup(GrowArrow(arr_enc_right_z),
                               FadeIn(z_tgt), Write(z_tgt_label)),
                lag_ratio=0.4,
            ),
            run_time=1.0,
        )
        self.wait(0.3)

        # ── Stage 3: Predictor ───────────────────────────────────────────────
        self.play(
            GrowArrow(arr_z_pred_input),
            Create(pred_nn),
            FadeIn(pred_label),
            run_time=1.0,
        )
        self.play(
            GrowArrow(arr_pred_z_out),
            FadeIn(z_pred),
            Write(z_pred_label),
            run_time=0.8,
        )
        self.wait(0.3)

        # ── Stage 4: Loss ────────────────────────────────────────────────────
        self.play(
            FadeIn(loss_box), FadeIn(loss_text),
            run_time=0.8,
        )
        self.wait(0.4)

        self.wait(1.0)
