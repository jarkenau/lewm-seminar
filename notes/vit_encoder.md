# ViT-Tiny Encoder — Speaker Notes (Slide 8)

## Patch Tokenization

- Input image is split into fixed-size patches — in LeWM a $224\times224$ image with patch size $P=14$ yields $16\times16 = 256$ patches of $14\times14$ pixels each (config: `img_size=224`, `patch_size=14`)
- Each patch is flattened and linearly projected to $D=192$ dimensions via trainable matrix $\mathbf{E} \in \mathbb{R}^{P^2 \cdot C \times D}$; positional embeddings $\mathbf{E}_{pos} \in \mathbb{R}^{(N+1) \times D}$ are added to retain spatial order
- The full input sequence to the Transformer is (Dosovitskiy et al., Eq. 1):

$$\mathbf{z}_0 = [\mathbf{x}_\text{class};\ \mathbf{x}_p^1\mathbf{E};\ \mathbf{x}_p^2\mathbf{E};\ \cdots;\ \mathbf{x}_p^N\mathbf{E}] + \mathbf{E}_{pos}$$

- ViT has far less image-specific inductive bias than CNNs — spatial relations between patches must be learned from data, not baked in (Dosovitskiy et al., §3.1 "Inductive bias")

## [CLS] Token

- A learnable $\mathbf{x}_\text{class}$ token is prepended at position 0 — borrowed from BERT; its final state aggregates global image context via self-attention across all patches
- 1D positional embeddings are used; Dosovitskiy et al. found no significant gain from 2D-aware alternatives

## Transformer Encoder (ViT-Tiny)

Each of the $L=12$ layers applies LayerNorm → MSA → residual, then LayerNorm → MLP → residual (Dosovitskiy et al., Eq. 2–3):

$$\mathbf{z}'_\ell = \text{MSA}(\text{LN}(\mathbf{z}_{\ell-1})) + \mathbf{z}_{\ell-1}, \qquad \ell = 1 \ldots L$$

$$\mathbf{z}_\ell = \text{MLP}(\text{LN}(\mathbf{z}'_\ell)) + \mathbf{z}'_\ell, \qquad \ell = 1 \ldots L$$

- MLP has two layers with GELU nonlinearity
- ViT-Tiny: $d=192$, 3 attention heads, ${\sim}5\text{M}$ parameters

## Extracting the Image Representation

After $L=12$ layers the [CLS] token is read off and normalized (Dosovitskiy et al., Eq. 4):

$$\mathbf{y} = \text{LN}(\mathbf{z}_L^0)$$

## LeWM-Specific Projection (Maes et al., §3.1)

- $\mathbf{y}$ passes through a **1-layer MLP + BatchNorm** to produce the final latent $z_t \in \mathbb{R}^D$
- This projection is *necessary*: the final ViT LayerNorm normalizes embeddings and prevents the SIGReg anti-collapse regularizer from being optimized effectively — BatchNorm restores the free statistics SIGReg requires
