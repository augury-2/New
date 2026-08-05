"""
KAUTHIK — Procedural Cinematic Art Engine
=========================================
Every visual in the deck is generated here: skies, fractal Himalayan
ridgelines with true atmospheric perspective, drifting mist, particle
fields, volumetric light rays, temple and forest silhouettes, prayer
flags, Aipan-inspired motifs and a stroked icon library.

Design intent: layers are rendered SEPARATELY and oversized, so that the
deck builder can stack them and animate each one independently to create
genuine parallax depth.
"""

from __future__ import annotations

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from design import C, RES_BASE, RES_BLEED, mix, rgb

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS, exist_ok=True)


# =========================================================== noise helpers ===
def _rand_grid(gw: int, gh: int, seed: int, tile_x: bool = False) -> np.ndarray:
    rng = np.random.default_rng(seed)
    g = rng.random((gh + 1, gw + 1)).astype(np.float32)
    if tile_x:
        g[:, -1] = g[:, 0]
    return g


def _upsample(g: np.ndarray, w: int, h: int) -> np.ndarray:
    im = Image.fromarray(g, mode="F").resize((w, h), Image.BICUBIC)
    return np.asarray(im, dtype=np.float32)


def fbm(w: int, h: int, base_gw: int, base_gh: int, octaves: int = 5,
        gain: float = 0.5, lac: int = 2, seed: int = 0,
        tile_x: bool = False) -> np.ndarray:
    """Fractal value noise in [0,1]. Optionally seamless on X."""
    total = np.zeros((h, w), dtype=np.float32)
    amp, norm = 1.0, 0.0
    gw, gh = base_gw, base_gh
    for o in range(octaves):
        total += amp * _upsample(_rand_grid(gw, gh, seed * 977 + o * 131, tile_x), w, h)
        norm += amp
        amp *= gain
        gw *= lac
        gh *= lac
    out = total / max(norm, 1e-6)
    lo, hi = float(out.min()), float(out.max())
    return (out - lo) / max(hi - lo, 1e-6)


def ridged(w: int, h: int, gw: int, gh: int, octaves: int, seed: int,
           tile_x: bool = False) -> np.ndarray:
    n = fbm(w, h, gw, gh, octaves=octaves, seed=seed, tile_x=tile_x)
    return 1.0 - np.abs(n * 2.0 - 1.0)


def blur_f(a: np.ndarray, radius: float, passes: int = 3) -> np.ndarray:
    """Fast approximate Gaussian blur for float arrays (PIL can't blur mode 'F').

    Three successive box blurs approximate a Gaussian closely enough for
    atmospheric work, and it is O(n) via summed-area tables.
    """
    if radius <= 0:
        return a
    out = a.astype(np.float32)
    r = max(1, int(round(radius)))
    for _ in range(passes):
        for axis in (0, 1):
            pad = [(0, 0), (0, 0)]
            pad[axis] = (r, r)
            p = np.pad(out, pad, mode="edge")
            cs = np.cumsum(p, axis=axis, dtype=np.float32)
            zero = np.zeros_like(np.take(cs, [0], axis=axis))
            cs = np.concatenate([zero, cs], axis=axis)
            n = out.shape[axis]
            hi = np.take(cs, np.arange(2 * r + 1, 2 * r + 1 + n), axis=axis)
            lo = np.take(cs, np.arange(0, n), axis=axis)
            out = (hi - lo) / float(2 * r + 1)
    return out


def smoothstep(a: float, b: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - a) / max(b - a, 1e-6), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


# ============================================================ compositing ===
def _to_img(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def _rgba(w: int, h: int) -> np.ndarray:
    return np.zeros((h, w, 4), dtype=np.float32)


def save(img: Image.Image, name: str, optimize: bool = True) -> str:
    path = os.path.join(ASSETS, name)
    img.save(path, optimize=optimize)
    return path


def add_grain(arr: np.ndarray, amount: float = 3.2, seed: int = 7) -> np.ndarray:
    """Film grain. Subtle — this is what stops gradients looking 'digital'."""
    h, w = arr.shape[:2]
    rng = np.random.default_rng(seed)
    g = rng.normal(0.0, amount, (h, w)).astype(np.float32)
    g = blur_f(g, 1.0, passes=1)
    out = arr.copy()
    out[..., :3] += g[..., None]
    return out


def vignette(arr: np.ndarray, strength: float = 0.38, power: float = 1.7) -> np.ndarray:
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx = (xx / (w - 1) - 0.5) * 2.0
    ny = (yy / (h - 1) - 0.5) * 2.0
    r = np.sqrt(nx * nx * 0.86 + ny * ny)
    v = 1.0 - strength * np.clip(r, 0, 1.6) ** power
    out = arr.copy()
    out[..., :3] *= v[..., None]
    return out


# ============================================================ sky / plates ===
# All moods place their light band around y≈0.30–0.50, because that is where
# the ridge stack puts the horizon. Below the horizon the sky darkens again
# into valley haze, which is what makes the ranges read as distant.
SKY_MOODS: dict[str, dict] = {
    # stops: list of (position 0..1 from top, hex)
    "dawn": dict(
        stops=[(0.00, "04101F"), (0.13, "0A1C39"), (0.23, "1D3660"),
               (0.31, "6A4F73"), (0.37, "BE6836"), (0.43, "E7A24B"),
               (0.51, "F3D093"), (0.64, "C3A37C"), (0.82, "8A7259"),
               (1.00, "5E4C3C")],
        sun=(0.50, 0.44, 0.33, "FFE9BC", 1.00),
    ),
    "dusk": dict(
        stops=[(0.00, "070E1C"), (0.14, "111A38"), (0.24, "31264C"),
               (0.31, "6B2A44"), (0.37, "A83A33"), (0.43, "DC7130"),
               (0.50, "EFA945"), (0.62, "B07A4E"), (0.80, "6E4E3A"),
               (1.00, "42302A")],
        sun=(0.58, 0.45, 0.31, "FFD08A", 0.98),
    ),
    "ember": dict(
        stops=[(0.00, "070505"), (0.16, "16090A"), (0.30, "3C1218"),
               (0.40, "6E1B27"), (0.50, "A83E22"), (0.60, "D9722C"),
               (0.74, "8C4A28"), (1.00, "351914")],
        sun=(0.50, 0.56, 0.34, "FFC98A", 0.85),
    ),
    "night": dict(
        stops=[(0.00, "020509"), (0.20, "050C18"), (0.36, "0A1730"),
               (0.46, "13294D"), (0.56, "1B3A64"), (0.72, "12253F"),
               (1.00, "070E1A")],
        sun=(0.30, 0.24, 0.30, "AECBEC", 0.42),
    ),
    "forest": dict(
        stops=[(0.00, "03110C"), (0.18, "072018"), (0.34, "0E2A22"),
               (0.45, "1A473A"), (0.55, "2A6B52"), (0.70, "16382C"),
               (1.00, "071811")],
        sun=(0.68, 0.30, 0.36, "D6EFC2", 0.46),
    ),
    "royal": dict(
        stops=[(0.00, "030B18"), (0.18, "07152C"), (0.34, "0E2748"),
               (0.46, "184070"), (0.58, "22568F"), (0.74, "133155"),
               (1.00, "061225")],
        sun=(0.50, 0.46, 0.38, "B8D8F5", 0.40),
    ),
    "monsoon": dict(
        stops=[(0.00, "080D10"), (0.20, "111A1F"), (0.36, "1C2C33"),
               (0.46, "2C444D"), (0.56, "425F69"), (0.72, "24373E"),
               (1.00, "0D1417")],
        sun=(0.42, 0.46, 0.36, "CFE3EA", 0.36),
    ),
    "snow": dict(
        stops=[(0.00, "0C1826"), (0.18, "1A2E44"), (0.34, "2E4A62"),
               (0.45, "537892"), (0.56, "8AAAC0"), (0.70, "5E7C93"),
               (1.00, "22333F")],
        sun=(0.50, 0.42, 0.40, "F2F8FC", 0.52),
    ),
    "parchment": dict(
        stops=[(0.00, "14130F"), (0.22, "1E1C16"), (0.42, "2C281F"),
               (0.58, "3A3327"), (0.76, "2A251C"), (1.00, "161410")],
        sun=(0.50, 0.46, 0.46, "A08C68", 0.30),
    ),
}


def sky_plate(mood: str, size=RES_BASE, seed: int = 3,
              grain: float = 3.0, vig: float = 0.34) -> Image.Image:
    """Multi-stop vertical gradient + radial light source + cloud modulation."""
    w, h = size
    spec = SKY_MOODS[mood]
    stops = spec["stops"]
    ys = np.linspace(0.0, 1.0, h, dtype=np.float32)

    ramp = np.zeros((h, 3), dtype=np.float32)
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        m = (ys >= p0) & (ys <= p1)
        if not m.any():
            continue
        t = (ys[m] - p0) / max(p1 - p0, 1e-6)
        t = t * t * (3 - 2 * t)                      # smoothstep between stops
        a, b = np.array(rgb(c0), np.float32), np.array(rgb(c1), np.float32)
        ramp[m] = a[None, :] + (b - a)[None, :] * t[:, None]
    ramp[ys < stops[0][0]] = np.array(rgb(stops[0][1]), np.float32)
    ramp[ys > stops[-1][0]] = np.array(rgb(stops[-1][1]), np.float32)

    arr = np.repeat(ramp[:, None, :], w, axis=1)

    # radial light source (sun / moon bloom)
    sx, sy, srad, scol, sint = spec["sun"]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx / w - sx) * (w / h)) ** 2 + (yy / h - sy) ** 2)
    glow = np.exp(-(d / max(srad, 1e-3)) ** 1.55) * sint
    arr += np.array(rgb(scol), np.float32)[None, None, :] * glow[..., None] * 0.72

    # broad atmospheric cloud modulation (baked, very soft)
    cl = fbm(w // 4, h // 4, 5, 3, octaves=5, seed=seed + 41)
    cl = np.asarray(Image.fromarray(cl, "F").resize((w, h), Image.BICUBIC), np.float32)
    band = smoothstep(0.05, 0.55, ys)[:, None] * (1.0 - smoothstep(0.72, 1.0, ys)[:, None])
    arr += (cl - 0.5)[..., None] * 26.0 * band[..., None]

    arr = vignette(arr, strength=vig)
    arr = add_grain(arr, grain, seed=seed)
    out = np.dstack([np.clip(arr, 0, 255), np.full((h, w), 255.0, np.float32)])
    return _to_img(out).convert("RGB")


# ============================================================== ridgelines ===
def _ridge_profile(w: int, seed: int, roughness: float = 0.52,
                   peaks: int = 4, sharp: float = 1.0) -> np.ndarray:
    """
    1-D Himalayan skyline in [0,1].

    Built as the upper envelope of asymmetric triangular massifs — this is
    what gives real ranges their angular summits and long straight flanks —
    then roughened with fractal detail whose amplitude scales with local
    altitude so the ridgelines stay crisp instead of turning to mush.
    """
    rng = np.random.default_rng(seed)
    xs = np.linspace(0.0, 1.0, w, dtype=np.float32)
    hgt = np.zeros(w, dtype=np.float32)

    npk = max(2, peaks) + 2
    for i in range(npk):
        cx = float((i + rng.uniform(0.10, 0.90)) / npk)
        pk = float(rng.uniform(0.42, 1.0))
        sl = float(rng.uniform(1.5, 3.4)) * sharp     # left flank steepness
        sr = float(rng.uniform(1.5, 3.4)) * sharp     # right flank steepness
        tri = np.where(xs < cx,
                       1.0 - (cx - xs) * sl,
                       1.0 - (xs - cx) * sr)
        hgt = np.maximum(hgt, np.clip(tri, 0.0, None) * pk)

    # secondary shoulders / foothills
    for i in range(npk):
        cx = float(rng.uniform(0.0, 1.0))
        pk = float(rng.uniform(0.16, 0.42))
        s = float(rng.uniform(3.0, 7.0)) * sharp
        tri = 1.0 - np.abs(xs - cx) * s
        hgt = np.maximum(hgt, np.clip(tri, 0.0, None) * pk)

    det = fbm(w, 1, 16, 1, octaves=6, gain=roughness, seed=seed + 7)[0]
    fine = fbm(w, 1, 90, 1, octaves=3, gain=0.45, seed=seed + 71)[0]
    hgt = hgt * (1.0 + (det - 0.5) * 0.34) + (det - 0.5) * 0.055 \
        + (fine - 0.5) * 0.022 * hgt

    hgt = np.clip(hgt, 0.0, None)
    hgt -= hgt.min()
    return hgt / max(hgt.max(), 1e-6)


def ridge_layer(size, seed: int, top: float, height: float,
                color_hi: str, color_lo: str, alpha: float = 1.0,
                roughness: float = 0.52, peaks: int = 4,
                snow: float = 0.0, snow_color: str = "EAF2F8",
                haze: float = 0.0, haze_color: str = "8FB4D6",
                sharp: float = 1.0, blur: float = 0.0) -> Image.Image:
    """
    One mountain range as its own RGBA plate.

    top     — where the highest summit sits (0..1 of image height)
    height  — vertical extent of the range body (0..1)
    snow    — 0..1 fraction of peak height that carries snow
    haze    — strength of atmospheric haze rising from the range base
    """
    w, h = size
    prof = _ridge_profile(w, seed, roughness=roughness, peaks=peaks, sharp=sharp)
    skyline = (top + (1.0 - prof) * height) * h            # y of the ridge crest

    yy = np.arange(h, dtype=np.float32)[:, None]
    below = yy >= skyline[None, :]

    # vertical shading inside the range (lighter at crest, darker at base)
    depth = np.clip((yy - skyline[None, :]) / (h * max(height, 0.05) * 1.5), 0, 1)
    hi = np.array(rgb(color_hi), np.float32)
    lo = np.array(rgb(color_lo), np.float32)
    body = hi[None, None, :] + (lo - hi)[None, None, :] * depth[..., None]

    a = np.where(below, 255.0 * alpha, 0.0).astype(np.float32)

    # soft crest so ridges read as atmosphere, not cut paper
    feather = np.clip(1.0 - (skyline[None, :] - yy) / 2.2, 0, 1) * (yy < skyline[None, :])
    a = np.maximum(a, feather * 255.0 * alpha)

    # snow caps — ALTITUDE based, exactly as a real snowline behaves: snow
    # exists above a roughly constant elevation, so only the high summits
    # carry it and the lower shoulders stay bare rock.
    if snow > 0:
        snow_y = (top + height * snow) * h
        jag = fbm(w, 1, 34, 1, octaves=5, seed=seed + 500)[0]
        fine = fbm(w, 1, 150, 1, octaves=3, seed=seed + 501)[0]
        sy = snow_y + (jag - 0.5) * h * height * 0.55 + (fine - 0.5) * h * height * 0.12
        sm = below & (yy < sy[None, :])
        sc = np.array(rgb(snow_color), np.float32)
        t = np.clip((sy[None, :] - yy) / max(h * height * 0.55, 1.0), 0, 1) ** 0.55
        body = np.where(sm[..., None],
                        body + (sc[None, None, :] - body) * (0.30 + 0.58 * t)[..., None],
                        body)

    # rock striation / gully shading for the nearer ranges
    if height > 0.10:
        st = fbm(w, h, 26, 10, octaves=5, seed=seed + 909)
        gully = ridged(w, h, 34, 6, 4, seed + 910)
        body += (st - 0.5)[..., None] * 14.0 * below[..., None]
        body -= (gully ** 3)[..., None] * 13.0 * below[..., None]

    out = np.dstack([body, a])
    img = _to_img(out)
    if blur > 0:
        img = img.filter(ImageFilter.GaussianBlur(blur))

    # haze pooling at the foot of the range (atmospheric perspective)
    if haze > 0:
        hz = _rgba(w, h)
        base = skyline + h * height * 0.30
        g = np.clip(1.0 - np.abs(yy - base[None, :]) / (h * 0.13), 0, 1) ** 1.6
        n = fbm(w, h, 8, 3, octaves=4, seed=seed + 313)
        g = g * (0.45 + 0.85 * n)
        hz[..., :3] = np.array(rgb(haze_color), np.float32)[None, None, :]
        hz[..., 3] = g * 255.0 * haze
        hzi = _to_img(hz).filter(ImageFilter.GaussianBlur(w / 260))
        img = Image.alpha_composite(img, hzi)
    return img


def himalaya_stack(size=RES_BLEED, seed: int = 11, mood: str = "dawn",
                   layers: int = 5, top0: float = 0.30, dtop: float = 0.115,
                   h0: float = 0.16, dh: float = 0.10) -> list[Image.Image]:
    """
    A full mountain system as independent parallax plates, farthest first.
    Atmospheric perspective is real: distant ranges are lighter, bluer,
    lower-contrast and hazier.
    """
    if mood in ("dusk", "ember"):
        far, near = "6B5A72", C.EARTH
        haze_c = "D89A6A"
    elif mood in ("night", "royal"):
        far, near = "2A4A72", "081726"
        haze_c = "6E9AC6"
    elif mood == "forest":
        far, near = "4E7A6A", C.FOREST_DEEP
        haze_c = "A8C8B4"
    elif mood == "snow":
        far, near = "8AA7BC", "34495C"
        haze_c = "DCE9F1"
    else:                                   # dawn
        far, near = "6E86A8", "132A2A"
        haze_c = "E8C79A"

    out = []
    for i in range(layers):
        t = i / max(layers - 1, 1)
        hi = "%02X%02X%02X" % mix(far, near, t ** 0.85)
        lo = "%02X%02X%02X" % mix(far, near, min(1.0, t ** 0.85 + 0.16))
        out.append(ridge_layer(
            size, seed=seed + i * 37,
            top=top0 + dtop * i,
            height=h0 + dh * i,
            color_hi=hi, color_lo=lo,
            alpha=0.78 + 0.22 * t,
            roughness=0.50 + 0.05 * i,
            peaks=3 + i,
            snow=(0.50 - 0.10 * i) if i <= 2 else 0.0,
            haze=(0.34 - 0.075 * i) if i < 4 else 0.0,
            haze_color=haze_c,
            sharp=0.85 + 0.30 * i,
            blur=max(0.0, 1.30 - 0.42 * i),
        ))
    return out


# ================================================================== clouds ===
def cloud_layer(size=RES_BLEED, seed: int = 5, color: str = "FFFFFF",
                alpha: float = 0.20, band=(0.16, 0.56), scale: int = 5,
                octaves: int = 6, wisp: float = 7.0, thresh: float = 0.50,
                soft: float = 0.42, blur: float = 4.0) -> Image.Image:
    """
    Horizontally stretched cloud / mist bank. Seamless on X so it can drift
    forever, soft-banded in Y so it never fights the typography.

    `wisp` stretches the noise horizontally (higher = longer, thinner streaks).
    """
    w, h = size
    n = fbm(max(24, int(w / wisp)), h, scale, max(2, scale // 2),
            octaves=octaves, seed=seed, tile_x=True)
    n = np.asarray(Image.fromarray(n, "F").resize((w, h), Image.BICUBIC), np.float32)
    n = np.clip((n - thresh) / max(soft, 1e-3), 0, 1) ** 1.45

    ys = np.linspace(0, 1, h, dtype=np.float32)
    b = smoothstep(band[0] - 0.12, band[0] + 0.10, ys) * \
        (1.0 - smoothstep(band[1] - 0.10, band[1] + 0.18, ys))
    a = n * b[:, None] * 255.0 * alpha

    arr = _rgba(w, h)
    arr[..., :3] = np.array(rgb(color), np.float32)[None, None, :]
    arr[..., 3] = a
    return _to_img(arr).filter(ImageFilter.GaussianBlur(blur))


def mist_layer(size=RES_BLEED, seed: int = 9, color: str = "CFE0EC",
               alpha: float = 0.34, y0: float = 0.55, y1: float = 1.0,
               blur: float = 9.0) -> Image.Image:
    """Low-lying valley fog. Denser, softer and lower than cloud_layer."""
    w, h = size
    n = fbm(int(w / 5), h, 4, 2, octaves=5, seed=seed, tile_x=True)
    n = np.asarray(Image.fromarray(n, "F").resize((w, h), Image.BICUBIC), np.float32)
    ys = np.linspace(0, 1, h, dtype=np.float32)
    b = smoothstep(y0 - 0.14, y0 + 0.12, ys) * (1.0 - smoothstep(y1 - 0.06, y1 + 0.2, ys))
    a = (0.30 + 0.85 * n) * b[:, None] * 255.0 * alpha
    arr = _rgba(w, h)
    arr[..., :3] = np.array(rgb(color), np.float32)[None, None, :]
    arr[..., 3] = a
    return _to_img(arr).filter(ImageFilter.GaussianBlur(blur))


# =============================================================== particles ===
def particle_layer(size=RES_BLEED, seed: int = 13, count: int = 420,
                   color: str = "FFE7B8", rmin: float = 1.4, rmax: float = 5.2,
                   amin: float = 0.16, amax: float = 0.78, glow: float = 2.4,
                   band=(0.0, 1.0), streak: float = 1.0,
                   bloom: bool = True) -> Image.Image:
    """
    Floating dust / snow / embers / fireflies. Radial-falloff sprites so they
    read as light rather than dots. `streak` >1 elongates them (drifting snow).
    """
    w, h = size
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), dtype=np.float32)

    for _ in range(count):
        r = float(rng.uniform(rmin, rmax))
        a = float(rng.uniform(amin, amax))
        cx = float(rng.uniform(0, w))
        cy = float(rng.uniform(band[0], band[1]) * h)
        rr = int(math.ceil(r * glow * max(1.0, streak))) + 2
        x0, x1 = max(0, int(cx) - rr), min(w, int(cx) + rr + 1)
        y0, y1 = max(0, int(cy) - rr), min(h, int(cy) + rr + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        dx = (xx - cx) / max(r * streak, 1e-3)
        dy = (yy - cy) / max(r, 1e-3)
        d = np.sqrt(dx * dx + dy * dy)
        core = np.exp(-(d ** 2) * 1.35) * a
        if bloom:
            core += np.exp(-(d / glow) ** 1.7) * a * 0.30
        acc[y0:y1, x0:x1] += core

    arr = _rgba(w, h)
    arr[..., :3] = np.array(rgb(color), np.float32)[None, None, :]
    arr[..., 3] = np.clip(acc, 0, 1) * 255.0
    return _to_img(arr)


def petal_layer(size=RES_BLEED, seed: int = 21, count: int = 90,
                colors=(C.SAFFRON_LIGHT, C.GOLD_LIGHT, "F0C9D2", C.MAROON_LIGHT),
                smin: int = 9, smax: int = 26, alpha: float = 0.55) -> Image.Image:
    """Marigold / rhododendron petals — the flowers of a Himalayan shrine."""
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rng = np.random.default_rng(seed)
    for _ in range(count):
        s = int(rng.integers(smin, smax))
        col = rgb(colors[int(rng.integers(0, len(colors)))])
        a = int(255 * alpha * rng.uniform(0.45, 1.0))
        p = Image.new("RGBA", (s * 3, s * 3), (0, 0, 0, 0))
        d = ImageDraw.Draw(p)
        # a petal = asymmetric lens shape
        d.pieslice([s * 0.4, s * 0.9, s * 2.6, s * 2.1], 200, 340, fill=col + (a,))
        d.pieslice([s * 0.4, s * 0.6, s * 2.6, s * 1.8], 20, 160, fill=col + (int(a * .82),))
        p = p.filter(ImageFilter.GaussianBlur(0.7))
        p = p.rotate(float(rng.uniform(0, 360)), resample=Image.BICUBIC, expand=True)
        img.alpha_composite(p, (int(rng.uniform(-s, w - s)), int(rng.uniform(-s, h - s))))
    return img


def star_layer(size=RES_BLEED, seed: int = 31, count: int = 700) -> Image.Image:
    return particle_layer(size, seed=seed, count=count, color="EAF2FF",
                          rmin=0.8, rmax=2.4, amin=0.22, amax=0.95, glow=3.2,
                          band=(0.0, 0.62))


# ============================================================== light rays ===
def light_rays(size=RES_BLEED, seed: int = 17, sx: float = 0.5, sy: float = 0.12,
               color: str = "FFE6B0", alpha: float = 0.34, rays: int = 13,
               spread: float = 1.05, length: float = 1.15,
               blur: float = 7.0) -> Image.Image:
    """Volumetric god-rays computed analytically in polar space."""
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    px, py = sx * w, sy * h
    dx, dy = xx - px, yy - py
    ang = np.arctan2(dy, dx)
    dist = np.sqrt(dx * dx + dy * dy) / (math.hypot(w, h))

    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), dtype=np.float32)
    for _ in range(rays):
        a0 = float(rng.uniform(-math.pi * 0.02, math.pi * 1.02))
        wd = float(rng.uniform(0.012, 0.070)) * spread
        st = float(rng.uniform(0.35, 1.0))
        da = np.abs(((ang - a0 + math.pi) % (2 * math.pi)) - math.pi)
        acc += np.exp(-(da / wd) ** 2) * st

    falloff = np.exp(-(dist / max(length, 1e-3)) ** 1.35)
    near = smoothstep(0.0, 0.10, dist)
    a = np.clip(acc, 0, 2.2) * falloff * near * alpha
    arr = _rgba(w, h)
    arr[..., :3] = np.array(rgb(color), np.float32)[None, None, :]
    arr[..., 3] = np.clip(a, 0, 1) * 255.0
    return _to_img(arr).filter(ImageFilter.GaussianBlur(blur))


def glow_orb(size=(1200, 1200), color: str = "FFD98A", alpha: float = 0.55,
             power: float = 1.6) -> Image.Image:
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx / w) - 0.5) ** 2 + ((yy / h) - 0.5) ** 2) * 2.0
    a = np.exp(-(d ** power) * 3.1) * alpha
    arr = _rgba(w, h)
    arr[..., :3] = np.array(rgb(color), np.float32)[None, None, :]
    arr[..., 3] = np.clip(a, 0, 1) * 255.0
    return _to_img(arr)


# =============================================== silhouettes: architecture ===
def _shikhara(d: ImageDraw.ImageDraw, cx: float, base_y: float, w: float,
              h: float, col, bands: int = 8, lw: float = 2.0):
    """
    A latina (single-spire) Nagara shikhara — the curvilinear stone tower of
    the Katyuri- and Chand-era temples that anchor most Uttarakhand fairs.
    Near-vertical at the base, curving inward to a fine neck.
    """
    left, right = [], []
    steps = 120
    for i in range(steps + 1):
        t = i / steps
        y = base_y - h * t
        half = (w / 2) * (1.0 - t ** 1.42) ** 0.80
        half = max(half, w * 0.070)
        left.append((cx - half, y))
        right.append((cx + half, y))
    d.polygon(left + right[::-1], fill=col)

    # bhumi mouldings — the horizontal storey markers of the tower
    for i in range(1, bands):
        t = (i / bands) ** 0.92
        y = base_y - h * t
        half = (w / 2) * (1.0 - t ** 1.42) ** 0.80
        d.rectangle([cx - half * 1.13, y - lw * 0.9, cx + half * 1.13, y + lw * 0.9],
                    fill=col)

    top = base_y - h
    r = w * 0.17
    d.ellipse([cx - r, top - r * 0.62, cx + r, top + r * 0.50], fill=col)       # amalaka
    d.rectangle([cx - w * 0.042, top - r * 1.30, cx + w * 0.042, top - r * 0.35], fill=col)
    d.ellipse([cx - w * 0.085, top - r * 2.00, cx + w * 0.085, top - r * 1.15], fill=col)  # kalasha
    d.line([(cx, top - r * 1.95), (cx, top - r * 3.10)], fill=col, width=max(2, int(lw * 1.4)))
    d.polygon([(cx, top - r * 3.06), (cx + w * 0.34, top - r * 2.72),
               (cx, top - r * 2.38)], fill=col)                                # dhwaja


def temple_silhouette(size=(1800, 1500), color: str = "0A1A16",
                      alpha: float = 1.0, flags: bool = True,
                      bells: bool = True) -> Image.Image:
    """
    A Himalayan stone temple in silhouette — sanctum with curvilinear spire,
    flanking pillared mandapas with tiered slate roofs, prayer-flag lines and
    a row of hanging bells. Drawn to FILL its frame, bottom-anchored, so the
    deck can place it at any size.
    """
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    col = rgb(color) + (int(255 * alpha),)
    lw = max(2.0, w * 0.0035)
    gy = h * 0.985
    cx = w * 0.5

    # jagati (plinth), stepped
    for k, (fw, fh) in enumerate([(0.86, 0.030), (0.74, 0.030), (0.62, 0.028)]):
        d.rectangle([cx - w * fw / 2, gy - h * (0.088 - k * 0.029),
                     cx + w * fw / 2, gy - h * (0.058 - k * 0.029)], fill=col)

    # sanctum cube + spire
    sw = w * 0.255
    d.rectangle([cx - sw / 2, gy - h * 0.325, cx + sw / 2, gy - h * 0.085], fill=col)
    d.rectangle([cx - sw * 0.60, gy - h * 0.345, cx + sw * 0.60, gy - h * 0.310], fill=col)
    _shikhara(d, cx, gy - h * 0.330, sw * 1.05, h * 0.545, col, lw=lw)

    # flanking mandapas with tiered slate roofs
    for s in (-1, 1):
        mx = cx + s * w * 0.285
        mw = w * 0.215
        d.rectangle([mx - mw / 2, gy - h * 0.205, mx + mw / 2, gy - h * 0.085], fill=col)
        for k, (sc, hh) in enumerate([(0.80, 0.300), (0.55, 0.360)]):
            d.polygon([(mx - mw * sc, gy - h * (0.200 - k * 0.006)),
                       (mx, gy - h * hh),
                       (mx + mw * sc, gy - h * (0.200 - k * 0.006))], fill=col)
        d.line([(mx, gy - h * 0.357), (mx, gy - h * 0.400)], fill=col, width=int(lw * 1.4))
        d.ellipse([mx - lw * 2.2, gy - h * 0.412, mx + lw * 2.2, gy - h * 0.396], fill=col)
        for k in (-1, 0, 1):                                  # pillars
            px = mx + k * mw * 0.32
            d.rectangle([px - mw * 0.050, gy - h * 0.190, px + mw * 0.050, gy - h * 0.085],
                        fill=col)

    # kholi (carved doorway) as negative space
    d.rectangle([cx - sw * 0.19, gy - h * 0.235, cx + sw * 0.19, gy - h * 0.085],
                fill=(0, 0, 0, 0))
    d.pieslice([cx - sw * 0.19, gy - h * 0.275, cx + sw * 0.19, gy - h * 0.195],
               180, 360, fill=(0, 0, 0, 0))

    if bells:
        by = gy - h * 0.352
        for k in range(-3, 4):
            if k == 0:
                continue
            bx = cx + k * sw * 0.26
            br = w * 0.014
            d.line([(bx, by), (bx, by + h * 0.028)], fill=col, width=max(1, int(lw * .8)))
            d.pieslice([bx - br, by + h * 0.024, bx + br, by + h * 0.024 + br * 2],
                       180, 360, fill=col)
            d.rectangle([bx - br, by + h * 0.024 + br * 0.85,
                         bx + br, by + h * 0.024 + br * 1.05], fill=col)

    if flags:
        _prayer_line(d, (w * 0.045, gy - h * 0.560), (cx - sw * 0.52, gy - h * 0.760),
                     col, n=6, sag=h * 0.048, lw=lw)
        _prayer_line(d, (cx + sw * 0.52, gy - h * 0.760), (w * 0.955, gy - h * 0.560),
                     col, n=6, sag=h * 0.048, lw=lw)
    return img


def _prayer_line(d, p0, p1, col, n=8, sag=30.0, lw=2.0,
                 fw=None, fh=None, colors=None):
    (x0, y0), (x1, y1) = p0, p1
    span = math.hypot(x1 - x0, y1 - y0)
    fw = fw if fw is not None else span / max(n, 1) * 0.42
    fh = fh if fh is not None else fw * 1.35
    pts = []
    for i in range(49):
        t = i / 48
        pts.append((x0 + (x1 - x0) * t,
                    y0 + (y1 - y0) * t + math.sin(math.pi * t) * sag))
    d.line(pts, fill=col, width=max(1, int(lw * 0.8)))
    for i in range(n):
        t = (i + 0.5) / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t + math.sin(math.pi * t) * sag
        c = col if colors is None else rgb(colors[i % len(colors)]) + (col[3],)
        d.polygon([(x - fw / 2, y), (x + fw / 2, y + fw * 0.06),
                   (x + fw * 0.44, y + fh), (x - fw * 0.46, y + fh * 0.94)], fill=c)


def prayer_flag_layer(size=(2848, 620), colors=(C.GOLD, C.SNOW, C.MAROON,
                                                C.PINE, C.SAFFRON),
                      lines: int = 2, alpha: float = 0.88,
                      per_line: int = 40) -> Image.Image:
    """Strings of coloured prayer flags — a signature of Himalayan shrines."""
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for L in range(lines):
        y0 = h * (0.05 + 0.17 * L)
        y1 = h * (0.20 + 0.14 * L)
        sag = h * (0.20 + 0.09 * L)
        fw = w / per_line * 0.46
        _prayer_line(d, (0, y0), (w, y1),
                     rgb(C.SLATE_DARK) + (int(190 * alpha),),
                     n=per_line, sag=sag, lw=max(2.0, w * 0.0010),
                     fw=fw, fh=fw * 1.30,
                     colors=[colors[(i + L * 2) % len(colors)] for i in range(per_line)])
    # recolour: _prayer_line uses col[3] for alpha, so re-apply global alpha
    if alpha < 1.0:
        a = np.asarray(img, dtype=np.float32)
        a[..., 3] *= alpha
        img = _to_img(a)
    return img


def pine_layer(size=(2848, 900), color: str = "05130F", alpha: float = 1.0,
               count: int = 52, seed: int = 8, hmin: float = 0.34,
               hmax: float = 0.90, ground: float = 0.10) -> Image.Image:
    """Deodar / chir-pine treeline — the middle parallax layer of a hill slope."""
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    col = rgb(color) + (int(255 * alpha),)
    rng = np.random.default_rng(seed)

    base = h * (1.0 - ground * 0.5)
    trees = []
    for i in range(count):
        trees.append((
            w * (i + float(rng.uniform(-0.45, 0.45))) / count,
            h * float(rng.uniform(hmin, hmax)),
            float(rng.uniform(0.19, 0.30)),
            int(rng.integers(6, 10)),
        ))
    trees.sort(key=lambda t: t[1])          # short trees behind, tall in front

    for x, th, ratio, tiers in trees:
        tw = th * ratio
        d.rectangle([x - tw * 0.048, base - th * 0.30, x + tw * 0.048, base + 2], fill=col)
        for k in range(tiers):
            t = k / tiers
            ty = base - th * (0.06 + 0.90 * t)
            tW = tw * (1.0 - t * 0.86) ** 0.85
            tH = th * 0.26 * (1.0 - t * 0.30)
            d.polygon([(x - tW / 2, ty), (x + tW / 2, ty), (x, ty - tH)], fill=col)

    if ground > 0:                          # solid slope the trees stand on
        d.rectangle([0, h * (1.0 - ground), w, h], fill=col)
    return img


def stall_layer(size=(2848, 700), color: str = "10201C", alpha: float = 1.0,
                count: int = 9, seed: int = 14,
                bunting=(C.GOLD, C.SAFFRON, C.MAROON, C.SNOW)) -> Image.Image:
    """The fair itself: a row of canopied market stalls with bunting."""
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    col = rgb(color) + (int(255 * alpha),)
    rng = np.random.default_rng(seed)
    base = h * 0.99
    for i in range(count):
        cx = w * (i + 0.5) / count + float(rng.uniform(-w * 0.012, w * 0.012))
        sw = w / count * float(rng.uniform(0.62, 0.86))
        sh = h * float(rng.uniform(0.44, 0.66))
        d.rectangle([cx - sw * 0.035, base - sh * 0.72, cx - sw * 0.035 + sw * 0.07, base], fill=col)
        d.rectangle([cx + sw * 0.44, base - sh * 0.72, cx + sw * 0.50, base], fill=col)
        d.rectangle([cx - sw * 0.50, base - sh * 0.72, cx - sw * 0.44, base], fill=col)
        # scalloped canopy
        pts = [(cx - sw * 0.56, base - sh * 0.70), (cx, base - sh * 1.02),
               (cx + sw * 0.56, base - sh * 0.70)]
        d.polygon(pts, fill=col)
        scal = 7
        for k in range(scal):
            t0 = k / scal
            x0 = cx - sw * 0.56 + sw * 1.12 * t0
            rw = sw * 1.12 / scal
            d.pieslice([x0, base - sh * 0.74, x0 + rw, base - sh * 0.62], 0, 180, fill=col)
        # counter + goods
        d.rectangle([cx - sw * 0.44, base - sh * 0.30, cx + sw * 0.44, base - sh * 0.22], fill=col)
        for k in range(int(rng.integers(3, 6))):
            gx = cx - sw * 0.36 + sw * 0.72 * (k + .5) / 5
            gr = sw * float(rng.uniform(0.035, 0.062))
            d.ellipse([gx - gr, base - sh * 0.30 - gr * 1.8, gx + gr, base - sh * 0.30], fill=col)
    # bunting across the whole row
    for L in range(2):
        y = h * (0.10 + 0.11 * L)
        n = 34
        for i in range(n):
            t = (i + .5) / n
            x = w * t
            yy = y + math.sin(math.pi * t * 3.0) * h * 0.05
            c = rgb(bunting[i % len(bunting)]) + (int(255 * alpha * 0.9),)
            fw = w / n * 0.5
            d.polygon([(x - fw / 2, yy), (x + fw / 2, yy), (x, yy + h * 0.085)], fill=c)
    return img


# ================================================ motifs: Aipan / mandala ===
def aipan_border(size=(2848, 150), color: str = C.SNOW, alpha: float = 0.42,
                 motifs: int = 9) -> Image.Image:
    """
    A repeating band inspired by Aipan — the ritual threshold art of Kumaon,
    drawn by women in white rice paste over red ochre. Its grammar is a
    lattice of dots joined by lines, with lotus and diamond units between
    two rules. Kept sparse so it reads as refinement, not decoration.
    """
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    col = rgb(color) + (int(255 * alpha),)
    lw = max(1, int(round(h * 0.016)))
    cy = h * 0.5

    d.line([(0, h * 0.10), (w, h * 0.10)], fill=col, width=lw)
    d.line([(0, h * 0.90), (w, h * 0.90)], fill=col, width=lw)

    step = w / motifs
    r = min(step * 0.115, h * 0.30)
    for i in range(motifs):
        cx = step * (i + 0.5)
        # eight-petal lotus: petals as thin lenses, not circles
        for k in range(8):
            a = math.pi * 2 * k / 8
            p0 = (cx + math.cos(a) * r * 0.30, cy + math.sin(a) * r * 0.30)
            p1 = (cx + math.cos(a) * r, cy + math.sin(a) * r)
            pa = (cx + math.cos(a + 0.36) * r * 0.66, cy + math.sin(a + 0.36) * r * 0.66)
            pb = (cx + math.cos(a - 0.36) * r * 0.66, cy + math.sin(a - 0.36) * r * 0.66)
            d.line([p0, pa, p1, pb, p0], fill=col, width=lw, joint="curve")
        d.ellipse([cx - r * 0.14, cy - r * 0.14, cx + r * 0.14, cy + r * 0.14], fill=col)

        # diamond + dot chain linking the rosettes
        mx = cx + step * 0.5
        dr = r * 0.34
        d.line([(mx - dr, cy), (mx, cy - dr), (mx + dr, cy), (mx, cy + dr), (mx - dr, cy)],
               fill=col, width=lw)
        for s in (-1, 1):
            for k in (1, 2):
                px = cx + s * (r + step * 0.5 - dr) * k / 2.6
                d.ellipse([px - lw, cy - lw, px + lw, cy + lw], fill=col)
        # dotted rows above and below
        for yy_ in (h * 0.26, h * 0.74):
            for k in range(4):
                px = cx - step * 0.30 + step * 0.60 * k / 3
                d.ellipse([px - lw * .9, yy_ - lw * .9, px + lw * .9, yy_ + lw * .9], fill=col)
    return img


def mandala(size=(1600, 1600), color: str = C.GOLD, alpha: float = 0.20,
            rings: int = 4, petals: int = 16) -> Image.Image:
    """
    A ghosted rosette in the Aipan / Himalayan-shrine idiom: a clean lotus
    mandala used at very low opacity as a compositional anchor.
    """
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    col = rgb(color) + (int(255 * alpha),)
    cx, cy = w / 2, h / 2
    R = min(w, h) * 0.47
    lw = max(1, int(R * 0.0055))

    for t in (0.30, 0.62, 0.86, 1.00):
        r = R * t
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=lw)

    # outer lotus ring — pointed petals between r=0.62 and r=0.86
    for k in range(petals):
        a = math.pi * 2 * k / petals
        a0, a1 = a - math.pi / petals, a + math.pi / petals
        pts = [(cx + math.cos(a0) * R * 0.62, cy + math.sin(a0) * R * 0.62),
               (cx + math.cos(a - 0.5 / petals) * R * 0.79,
                cy + math.sin(a - 0.5 / petals) * R * 0.79),
               (cx + math.cos(a) * R * 0.86, cy + math.sin(a) * R * 0.86),
               (cx + math.cos(a + 0.5 / petals) * R * 0.79,
                cy + math.sin(a + 0.5 / petals) * R * 0.79),
               (cx + math.cos(a1) * R * 0.62, cy + math.sin(a1) * R * 0.62)]
        d.line(pts, fill=col, width=lw, joint="curve")

    # inner lotus
    for k in range(petals // 2):
        a = math.pi * 2 * k / (petals // 2) + math.pi / petals
        p0 = (cx + math.cos(a) * R * 0.30, cy + math.sin(a) * R * 0.30)
        p1 = (cx + math.cos(a) * R * 0.60, cy + math.sin(a) * R * 0.60)
        pa = (cx + math.cos(a + 0.20) * R * 0.46, cy + math.sin(a + 0.20) * R * 0.46)
        pb = (cx + math.cos(a - 0.20) * R * 0.46, cy + math.sin(a - 0.20) * R * 0.46)
        d.line([p0, pa, p1, pb, p0], fill=col, width=lw, joint="curve")

    # dotted outermost ring
    for k in range(petals * 3):
        a = math.pi * 2 * k / (petals * 3)
        px, py = cx + math.cos(a) * R, cy + math.sin(a) * R
        d.ellipse([px - lw * 1.6, py - lw * 1.6, px + lw * 1.6, py + lw * 1.6], fill=col)

    dr = R * 0.055
    d.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], outline=col, width=lw)
    return img


def texture_overlay(size=RES_BASE, kind: str = "paper", alpha: float = 0.10,
                    seed: int = 6) -> Image.Image:
    """Handmade-paper / woven-wool / stone grain, for tactile depth."""
    w, h = size
    if kind == "wool":
        n = fbm(w, h, 120, 6, octaves=4, seed=seed)
        n = n * 0.5 + 0.5 * fbm(w, h, 6, 120, octaves=4, seed=seed + 1)
    elif kind == "stone":
        n = ridged(w, h, 30, 18, 6, seed)
    else:
        n = fbm(w, h, 70, 40, octaves=6, seed=seed)
    arr = _rgba(w, h)
    arr[..., :3] = 255.0
    arr[..., 3] = np.clip((n - 0.5) * 2.0, 0, 1) * 255.0 * alpha
    return _to_img(arr)


def scrim(size=RES_BASE, color: str = "05100C", a_top: float = 0.10,
          a_bot: float = 0.86, power: float = 1.35) -> Image.Image:
    """Readability scrim: a vertical alpha ramp that protects typography."""
    w, h = size
    ys = np.linspace(0, 1, h, dtype=np.float32) ** power
    a = (a_top + (a_bot - a_top) * ys) * 255.0
    arr = _rgba(w, h)
    arr[..., :3] = np.array(rgb(color), np.float32)[None, None, :]
    arr[..., 3] = np.repeat(a[:, None], w, axis=1)
    return _to_img(arr)


def side_scrim(size=RES_BASE, color: str = "05100C", a_in: float = 0.88,
               a_out: float = 0.0, frac: float = 0.62,
               side: str = "left") -> Image.Image:
    w, h = size
    xs = np.linspace(0, 1, w, dtype=np.float32)
    if side == "right":
        xs = 1.0 - xs
    t = smoothstep(0.0, frac, xs)
    a = (a_in + (a_out - a_in) * t) * 255.0
    arr = _rgba(w, h)
    arr[..., :3] = np.array(rgb(color), np.float32)[None, None, :]
    arr[..., 3] = np.repeat(a[None, :], h, axis=0)
    return _to_img(arr)
