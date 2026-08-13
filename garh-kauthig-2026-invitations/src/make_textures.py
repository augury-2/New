"""
Procedural texture generator for the Garh Kauthig 2026 invitation suite.

Produces seamless, tileable grayscale textures used as low-opacity overlays:
  paper-fiber.png   handmade / cotton-rag paper with visible fibres + inclusions
  paper-grain.png   fine tooth for letterpress feel
  gold-foil.png     brushed metal micro-striation for foil-stamp simulation

All tiles are seamless so they can repeat across the full A3 bleed at 300 DPI
without visible joins.  Run:  python3 src/make_textures.py
"""

import os
import numpy as np
from PIL import Image, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "textures")
os.makedirs(OUT, exist_ok=True)

SIZE = 1024


def _resize(arr, size):
    """Bicubic upscale of a float array to (size, size)."""
    a = np.clip(arr, 0.0, 1.0)
    img = Image.fromarray((a * 255.0).astype(np.uint8), mode="L")
    return np.asarray(img.resize((size, size), Image.BICUBIC), dtype=np.float32) / 255.0


def value_noise(size, gx, gy, seed, pad=2):
    """Seamless value noise. gx/gy = control-grid resolution (gx != gy -> streaks)."""
    rng = np.random.default_rng(seed)
    g = rng.random((gy, gx)).astype(np.float32)
    # wrap-pad so the interpolation is periodic, then crop the centre back out
    gp = np.pad(g, ((pad, pad), (pad, pad)), mode="wrap")
    cell_y, cell_x = size / gy, size / gx
    big_h = int(round(size + 2 * pad * cell_y))
    big_w = int(round(size + 2 * pad * cell_x))
    img = Image.fromarray((gp * 255.0).astype(np.uint8), mode="L")
    big = np.asarray(img.resize((big_w, big_h), Image.BICUBIC), dtype=np.float32) / 255.0
    oy = int(round(pad * cell_y))
    ox = int(round(pad * cell_x))
    return big[oy:oy + size, ox:ox + size]


def fbm(size, base, seed, octaves=5, lacunarity=2, gain=0.5, aspect=1.0):
    """Fractal sum of seamless value noise. aspect > 1 stretches features on x."""
    total = np.zeros((size, size), dtype=np.float32)
    amp, norm = 1.0, 0.0
    for o in range(octaves):
        gy = max(2, int(round(base * (lacunarity ** o))))
        gx = max(2, int(round(gy / aspect)))
        total += amp * value_noise(size, gx, gy, seed + o * 977)
        norm += amp
        amp *= gain
    return total / norm


def normalize(a, lo=0.0, hi=1.0):
    mn, mx = float(a.min()), float(a.max())
    if mx - mn < 1e-6:
        return np.full_like(a, (lo + hi) / 2)
    return lo + (a - mn) * (hi - lo) / (mx - mn)


def speckles(size, count, seed, rmin=1, rmax=3, dark=True):
    """Seamless pulp inclusions / flecks, drawn with wrap-around."""
    rng = np.random.default_rng(seed)
    layer = np.zeros((size, size), dtype=np.float32)
    yy, xx = np.mgrid[0:size, 0:size]
    for _ in range(count):
        cx, cy = rng.integers(0, size, 2)
        r = rng.uniform(rmin, rmax)
        dx = np.minimum(np.abs(xx - cx), size - np.abs(xx - cx))
        dy = np.minimum(np.abs(yy - cy), size - np.abs(yy - cy))
        d = np.sqrt(dx * dx + dy * dy)
        layer = np.maximum(layer, np.clip(1.0 - d / r, 0.0, 1.0) * rng.uniform(0.35, 1.0))
    return -layer if dark else layer


def save(arr, name, blur=0.0):
    a = np.clip(arr, 0.0, 1.0)
    img = Image.fromarray((a * 255.0).astype(np.uint8), mode="L")
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    img.save(os.path.join(OUT, name), optimize=True)
    print("wrote", name, img.size)


# ----------------------------------------------------------------- paper fibre
# Cotton-rag look: cloudy body dominates; short fibres are cross-hatched in
# both directions at equal weight so no single direction reads as banding.
clouds = fbm(SIZE, 4, 11, octaves=6, gain=0.58)
mottle = fbm(SIZE, 12, 154, octaves=4, gain=0.5)
fib_h = fbm(SIZE, 10, 502, octaves=4, gain=0.55, aspect=7.0)      # fibres lying across
fib_v = fbm(SIZE, 10, 913, octaves=4, gain=0.55, aspect=1 / 7.0)  # fibres lying down
tooth = fbm(SIZE, 110, 77, octaves=3, gain=0.5)

paper = (0.50
         + 0.34 * (normalize(clouds) - 0.5)
         + 0.22 * (normalize(mottle) - 0.5)
         + 0.15 * (normalize(fib_h) - 0.5)
         + 0.15 * (normalize(fib_v) - 0.5)
         + 0.14 * (normalize(tooth) - 0.5))
paper = normalize(paper, 0.74, 1.0)
paper = paper + speckles(SIZE, 150, 4242, 1.2, 3.2) * 0.16
paper = paper + speckles(SIZE, 26, 8181, 2.5, 6.0) * 0.08
save(np.clip(paper, 0, 1), "paper-fiber.png", blur=0.5)

# ------------------------------------------------------------------ fine grain
grain = fbm(SIZE, 140, 303, octaves=3, gain=0.45)
grain = normalize(grain, 0.82, 1.0)
save(grain, "paper-grain.png", blur=0.2)

# ------------------------------------------------------------ brushed gold foil
stripe = fbm(SIZE, 6, 2026, octaves=5, gain=0.62, aspect=40.0)
sheen = fbm(SIZE, 2, 606, octaves=3, gain=0.6, aspect=6.0)
foil = normalize(0.65 * normalize(stripe) + 0.35 * normalize(sheen), 0.24, 1.0)
save(foil, "gold-foil.png", blur=0.25)
