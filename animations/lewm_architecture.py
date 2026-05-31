from pathlib import Path

from manim import *

ASSETS = Path(__file__).resolve().parent.parent / "assets"


class LeWMArchitecture(Scene):
    """Action-conditioned JEPA (LeWorldModel) forward step, white style.

    Encoders are ViT-Tiny boxes, the predictor is a Transformer with AdaLN
    action conditioning, and the full LeWM objective (MSE + SIGReg) is shown.
    """

    def construct(self):
        self.camera.background_color = WHITE

        # ── Colors (match jepa_training.py) ─────────────────────────────────
        TEXT_COLOR = "#1a1a1a"
        BOX_COLOR = "#2d2d2d"
        ARROW_COLOR = "#000000"
        EMBED_COLOR = "#4A90D9"   # latent z (blue)
        PRED_COLOR = "#E8704A"    # prediction ẑ (orange)
        LOSS_COLOR = "#5BA85A"    # loss (green)
        ACTION_COLOR = "#8E6FBF"  # action / AdaLN (purple)
        BOX_FILL = "#f4f4f4"

        # ── Helpers ─────────────────────────────────────────────────────────
        def make_arrow(start, end, color=ARROW_COLOR, sw=2.5):
            return Arrow(start, end, buff=0.12, stroke_color=color, stroke_width=sw,
                         tip_length=0.17, max_stroke_width_to_length_ratio=999,
                         max_tip_length_to_length_ratio=999, color=color)

        def labeled_box(lines, w, h, fill=BOX_FILL, stroke=BOX_COLOR):
            box = RoundedRectangle(width=w, height=h, corner_radius=0.1,
                                   fill_color=fill, fill_opacity=1,
                                   stroke_color=stroke, stroke_width=2)
            label = VGroup(*lines).arrange(DOWN, buff=0.06).move_to(box.get_center())
            return VGroup(box, label)

        def make_vit_box():
            """Rounded square — the outer shape of the NN icon, no nodes inside."""
            box = RoundedRectangle(width=1.55, height=0.75, corner_radius=0.1,
                                   fill_color=BOX_FILL, fill_opacity=1,
                                   stroke_color=BOX_COLOR, stroke_width=2)
            l1 = Text("ViT-Tiny", font_size=16, color=TEXT_COLOR, weight=BOLD)
            l2 = Tex(r"$\sim$5M params", font_size=18, color=TEXT_COLOR)
            labels = VGroup(l1, l2).arrange(DOWN, buff=0.07)
            labels.move_to(box.get_center())
            return VGroup(box, labels)

        EX = 4.6
        # ── Title ───────────────────────────────────────────────────────────
        title = Text("LeWorldModel — Action-Conditioned JEPA",
                     font_size=28, color=TEXT_COLOR).to_edge(UP, buff=0.4)

        # ── Encoders — rounded box ───────────────────────────────────────────
        IMG_H = 1.2
        GREEN_FILL, GREEN_STROKE = "#9FE6A0", "#5FB070"   # fixed target T
        GRAY_FILL, GRAY_STROKE = "#8194B4", "#5E6E8C"     # pushed object T
        EEF_BLUE = "#3B6FD6"                              # end-effector dot

        # PushT poses in the local box frame: the gray block is pushed from its
        # start pose onto the fixed green target; the EEF trails just behind it.
        START_POS = np.array([-0.20, -0.17, 0.0])
        GOAL_POS = np.array([0.16, 0.11, 0.0])
        START_ANG, GOAL_ANG = 26 * DEGREES, -16 * DEGREES

        def make_T(fill, stroke, opacity):
            pts = [[-0.6, 0.6, 0], [0.6, 0.6, 0], [0.6, 0.3, 0],
                   [0.15, 0.3, 0], [0.15, -0.6, 0], [-0.15, -0.6, 0],
                   [-0.15, 0.3, 0], [-0.6, 0.3, 0]]
            T = Polygon(*pts, stroke_color=stroke, stroke_width=2,
                        fill_color=fill, fill_opacity=opacity)
            T.scale(0.30)
            return T

        def make_state(progress, center):
            """One PushT observation: green target, gray block, blue EEF.

            The EEF starts on the wrong (goal-facing) side and must first swing
            around behind the block; only then does the push toward the target
            begin — so the rollout is not a perfectly direct trajectory.
            """
            green = make_T(GREEN_FILL, GREEN_STROKE, 0.5)
            green.rotate(GOAL_ANG).shift(GOAL_POS)

            block_p = np.clip((progress - 0.3) / 0.7, 0.0, 1.0)
            pos = START_POS + (GOAL_POS - START_POS) * block_p
            ang = START_ANG + (GOAL_ANG - START_ANG) * block_p
            gray = make_T(GRAY_FILL, GRAY_STROKE, 1.0)
            gray.rotate(ang).shift(pos)

            # EEF swings 180° from the goal-facing side (wrong) to behind the
            # block (correct) over the first part of the rollout.
            push_dir = GOAL_POS - START_POS
            theta = np.arctan2(push_dir[1], push_dir[0])
            swing = np.clip(progress / 0.4, 0.0, 1.0)
            a = theta + swing * np.pi
            eef = Dot(radius=0.05, color=EEF_BLUE, fill_opacity=1)
            eef.move_to(pos + 0.17 * np.array([np.cos(a), np.sin(a), 0.0]))

            return VGroup(green, gray, eef).shift(center)

        def build_encoder(x, progress, x_tex):
            enc = make_vit_box().move_to([x, -0.6, 0])
            center = np.array([x, -2.55, 0])
            border = Square(side_length=IMG_H, color=BOX_COLOR, stroke_width=1.5,
                            fill_color=WHITE, fill_opacity=1).move_to(center)
            state = make_state(progress, center)
            x_lab = MathTex(x_tex, color=TEXT_COLOR, font_size=28).next_to(border, DOWN, buff=0.18)
            obs_lab = Tex(r"\textbf{\textsc{Observation}}", color=TEXT_COLOR, font_size=16)
            obs_lab.next_to(x_lab, DOWN, buff=0.07)
            a_img = make_arrow(border.get_top(), enc.get_bottom())
            return dict(enc=enc, state=state, border=border, center=center,
                        x_lab=x_lab, obs_lab=obs_lab, a_img=a_img)

        STEP = 0.1
        encL = build_encoder(-EX, 0.0, r"x(t)")
        encR = build_encoder(EX, STEP, r"x(t{+}1)")

        # x(t) is really a short stack of past frames — show faded ghost copies
        # offset behind the current observation to convey the temporal context.
        ghostsL = []
        for off, op in [(np.array([-0.34, 0.30, 0]), 0.22),
                        (np.array([-0.17, 0.15, 0]), 0.42)]:
            gc = encL["center"] + off
            gb = Square(side_length=IMG_H, color=BOX_COLOR, stroke_width=1.5,
                        fill_color=WHITE, fill_opacity=1).move_to(gc)
            g = VGroup(gb, make_state(0.0, gc)).set_opacity(op)
            ghostsL.append(g)

        # ── Predictor box (Transformer + AdaLN) ─────────────────────────────
        pred = labeled_box(
            [Text("Transformer", font_size=20, color=TEXT_COLOR),
             Tex(r"$\sim$10M params", font_size=18, color=TEXT_COLOR),
             Text("AdaLN at every layer", font_size=13, color=ACTION_COLOR)],
            w=2.6, h=0.95,
        ).move_to([-0.7, 1.95, 0])

        z_to_pred = make_arrow(encL["enc"].get_top(), pred.get_left())

        # action conditioning (AdaLN) from below
        a_box = RoundedRectangle(width=1.5, height=0.7, corner_radius=0.08,
                                 fill_color="#f0ebf7", fill_opacity=1,
                                 stroke_color=ACTION_COLOR, stroke_width=2).move_to([-0.7, 0.5, 0])
        a_text = VGroup(
            MathTex(r"a(t)\in\mathbb{R}^2", color=ACTION_COLOR, font_size=18),
            Tex(r"goal $(x,\,y)$", color=ACTION_COLOR, font_size=14),
        ).arrange(DOWN, buff=0.08).move_to(a_box.get_center())
        a_to_pred = make_arrow(a_box.get_top(), pred.get_bottom(), sw=2.5)
        gb_lab = MathTex(r"\gamma,\ \beta", color=ACTION_COLOR, font_size=20).next_to(a_to_pred, RIGHT, buff=0.1)


        # ── Loss box ────────────────────────────────────────────────────────
        eq = MathTex(
            r"\mathcal{L}_{\mathrm{LeWM}}",
            r"=",
            r"\mathrm{MSE}",
            r"+",
            r"\lambda",
            r"\cdot",
            r"\mathrm{SIGReg}",
            font_size=30, color=TEXT_COLOR,
        )
        eq[2].set_color(PRED_COLOR)
        eq[4].set_color(LOSS_COLOR)
        eq[6].set_color(LOSS_COLOR)

        loss_rect = SurroundingRectangle(
            eq, color=BOX_COLOR, stroke_width=2,
            corner_radius=0.1, buff=0.2,
            fill_color=BOX_FILL, fill_opacity=1,
        )
        loss_box = VGroup(loss_rect, eq)
        loss_box.move_to([4.2, 1.95, 0])

        zpred_to_loss = make_arrow(pred.get_right(), loss_box.get_left())
        ztgt_to_loss = make_arrow(encR["enc"].get_top(), [EX, loss_box.get_bottom()[1], 0])

        # ── Numbered badges: the three components we zoom into next ───────────
        def badge(num, color):
            c = Circle(radius=0.17, fill_color=color, fill_opacity=1,
                       stroke_color=WHITE, stroke_width=2)
            t = Text(str(num), font_size=20, color=WHITE, weight=BOLD).move_to(c.get_center())
            return VGroup(c, t)

        badge1 = badge(1, EMBED_COLOR).move_to(encL["enc"].get_corner(UL))   # ViT-Tiny
        badge2 = badge(2, ACTION_COLOR).move_to(pred.get_corner(DL))          # AdaLN
        badge3 = badge(3, LOSS_COLOR).move_to(eq[6].get_corner(UR) + UP * 0.18)  # SIGReg

        # ════════════════════════════════════════════════════════════════════
        # Animation
        # ════════════════════════════════════════════════════════════════════
        # Whole diagram is static — every box, arrow and label is on screen from
        # the first frame. The only motion is the observation pair x(t) / x(t+1)
        # stepping through a realistic PushT sequence (x(t+1) one step ahead).
        state_L, state_R = encL["state"], encR["state"]
        self.add(
            title,
            encL["enc"], *ghostsL, encL["border"], state_L, encL["x_lab"], encL["obs_lab"], encL["a_img"],
            encR["enc"], encR["border"], state_R, encR["x_lab"], encR["obs_lab"], encR["a_img"],
            z_to_pred, pred,
            a_box, a_text, a_to_pred, gb_lab,
            loss_rect, eq, zpred_to_loss, ztgt_to_loss,
            badge1, badge2, badge3,
        )
        self.wait(1.0)

        # PushT rollout: the gray T is pushed onto the green target; x(t+1) is
        # always one control step ahead of x(t).
        for i in range(1, 10):
            new_L = make_state(i * STEP, encL["center"])
            new_R = make_state((i + 1) * STEP, encR["center"])
            self.play(
                FadeOut(state_L), FadeIn(new_L),
                FadeOut(state_R), FadeIn(new_R),
                run_time=0.7,
            )
            state_L, state_R = new_L, new_R
            self.wait(0.8)

        self.wait(1.5)
