import marimo

__generated_with = "0.23.6"
app = marimo.App(width="full", layout_file="layouts/presentation.slides.json", app_title="LeWorldModel")


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
    return


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
            ],
            justify="center",
            align="start",
            gap="0",
        )

    _()
    return


if __name__ == "__main__":
    app.run()
