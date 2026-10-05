"""Make the dark-mode variant of assets/img/research/sweepx_ecosystem.png.

Neutral (grey) pixels have their lightness inverted onto the site's dark palette
(white -> #1c1c1d page background, light-grey card fill -> darker card, dark text -> light text),
keeping any faint tint; coloured pixels (teal, orange, logos, ribbon) are kept as they are.
The teal engine block (with its white text) is left untouched, and the sweep-agent box,
whose fill is pure white like the page, gets the same card shade as the other boxes.

Soft drop shadows around the cards would invert into a glow, so light grey pixels outside the
cards and the engine halo are flattened to the page background.

Run from the repo root:  uv run --python 3.12 --with numpy --with scipy --with pillow python _tools/make_sweepx_dark.py
"""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SRC = "assets/img/research/sweepx_ecosystem.png"
DST = "assets/img/research/sweepx_ecosystem_dark.png"
BG = 28 / 255          # site dark background #1c1c1d
TEXT = 0.88            # where near-black text ends up
GAMMA = 0.55           # <1 stretches the near-white range so cards stay distinct from the page
ENGINE_BOX = (584, 341, 1016, 561)   # x0, y0, x1, y1 of the teal engine block
AGENT_BOX = (609, 150, 990, 272)     # sweep-agent box (orange border)
HALO_RGB = (234, 245, 243)           # light-teal rounded rectangle around the engine block

def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


im = np.asarray(Image.open(SRC).convert("RGB")).astype(float) / 255.0
H, W, _ = im.shape
mean = im.mean(axis=2, keepdims=True)
chroma = im.max(axis=2) - im.min(axis=2)

V = mean[..., 0].copy()
ax0, ay0, ax1, ay1 = AGENT_BOX
inner = np.zeros((H, W), bool); inner[ay0 + 5:ay1 - 4, ax0 + 5:ax1 - 4] = True
V[inner] = np.minimum(V[inner], 251 / 255)          # give the agent box the card fill shade

k = (TEXT - BG) / (0.9 ** GAMMA)
Vd = BG + k * np.clip(1.0 - V, 0, 1) ** GAMMA
neutral = Vd[..., None] + (im - mean)               # keep faint tints (e.g. the engine halo)

w = np.clip((40 / 255 - chroma) / (28 / 255), 0, 1)[..., None]   # 1 = grey, 0 = coloured
out = w * neutral + (1 - w) * im

ex0, ey0, ex1, ey1 = ENGINE_BOX
teal = np.linalg.norm(im - np.array([14, 138, 120]) / 255.0, axis=2) < 60 / 255
region = np.zeros((H, W), bool); region[ey0:ey1 + 1, ex0:ex1 + 1] = True
lab, n = ndi.label(teal & region)
block = lab == (np.argmax(np.bincount(lab.ravel())[1:]) + 1)
block = ndi.binary_fill_holes(block)                # include the white text inside the block
out[block] = im[block]

# flatten the cards' soft shadows: light neutral pixels outside the card shapes and the halo
# become page background. Card shape = its fill grown by 3 px (fill ends ~1 px inside the
# 2-3 px dashed border; the shadow starts right outside it).
fillc = np.all((im >= 247 / 255) & (im <= 253 / 255), axis=2)
fillc = ndi.binary_opening(fillc, structure=disk(5))   # cuts thin leaks through dash gaps at the corners
lab, n = ndi.label(fillc)
sizes = np.bincount(lab.ravel())
cards = np.isin(lab, [i for i in range(1, n + 1) if sizes[i] > 20000])
keep = ndi.binary_dilation(cards, structure=disk(3))   # round, like the cards
orange = (im[..., 0] > 200 / 255) & (im[..., 1] > 100 / 255) & (im[..., 1] < 170 / 255) & (im[..., 2] < 90 / 255)
ring = np.zeros((H, W), bool); ring[ay0 - 2:ay1 + 3, ax0 - 2:ax1 + 3] = True
keep |= ndi.binary_fill_holes(orange & ring)          # sweep-agent: everything inside its orange border
halo = np.linalg.norm(im - np.array(HALO_RGB) / 255.0, axis=2) < 12 / 255
lab, n = ndi.label(halo)
halo = ndi.binary_dilation(ndi.binary_fill_holes(lab == (np.argmax(np.bincount(lab.ravel())[1:]) + 1)), iterations=1)
keep |= halo
shadow = (~keep) & (mean[..., 0] > 0.80) & (chroma < 0.06)
out[shadow] = BG

Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(DST, optimize=True)
print("wrote", DST, (W, H))
