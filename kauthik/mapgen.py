"""
KAUTHIK — Cartography
=====================
Renders the deck's maps from real district geometry (Census-2011 district
boundaries, via the public `india-maps-data` GeoJSON set):

  * India, with Uttarakhand lit up in gold
  * Uttarakhand, split into its two historic divisions — Garhwal and Kumaon
  * Individual layers for districts, division fills, borders, rivers and the
    Kauthik location markers, so the deck can reveal them progressively.

Every layer is produced at the same projection and canvas size, so stacking
them in PowerPoint keeps perfect registration.
"""

from __future__ import annotations

import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from design import C, rgb
from artgen import blur_f, _to_img, _rgba

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# The two historic divisions of Uttarakhand.
GARHWAL = {"Uttarkashi", "Chamoli", "Rudraprayag", "Tehri Garhwal",
           "Pauri Garhwal", "Dehradun", "Haridwar"}
KUMAON = {"Pithoragarh", "Bageshwar", "Almora", "Champawat", "Nainital",
          "Udham Singh Nagar"}

# Kauthik / mela locations plotted on the state map.
# (name, lon, lat, division, tier)  tier 1 = headline fair, 2 = major, 3 = notable
KAUTHIK_SITES = [
    ("Bageshwar",   79.7714, 29.8378, "kumaon",  1),   # Uttarayani Kauthik
    ("Jauljibi",    80.4239, 29.7539, "kumaon",  1),   # Indo-Nepal trade mela
    ("Devidhura",   79.7167, 29.3500, "kumaon",  1),   # Bagwal
    ("Nauti",       79.2350, 30.2650, "garhwal", 1),   # Nanda Devi Raj Jat start
    ("Thal",        80.1167, 29.8167, "kumaon",  2),
    ("Dwarahat",    79.4333, 29.7833, "kumaon",  2),   # Syalde Bikhauti
    ("Almora",      79.6667, 29.5892, "kumaon",  2),   # Nanda Devi Mela
    ("Gauchar",     79.3120, 30.2880, "garhwal", 2),
    ("Bhimtal",     79.5651, 29.3452, "kumaon",  3),   # Harela Mela
    ("Dehradun",    78.0322, 30.3165, "garhwal", 1),   # Gad Kauthig
    ("Uttarkashi",  78.4500, 30.7300, "garhwal", 3),
    ("Srinagar",    78.7833, 30.2200, "garhwal", 3),
    ("Pithoragarh", 80.2167, 29.5833, "kumaon",  3),
    ("Champawat",   80.0958, 29.3358, "kumaon",  3),
    ("Purnagiri",   80.1500, 29.0500, "kumaon",  3),
]

# Approximate courses of the sacred rivers, as polylines (lon, lat).
RIVERS = {
    "Bhagirathi–Ganga": [(78.94, 30.99), (78.62, 30.73), (78.48, 30.55),
                         (78.60, 30.29), (78.40, 30.15), (78.28, 30.05),
                         (78.17, 29.95)],
    "Alaknanda":        [(79.49, 30.74), (79.32, 30.56), (79.16, 30.42),
                         (78.98, 30.28), (78.79, 30.22), (78.60, 30.29)],
    "Saryu":            [(80.02, 30.09), (79.90, 29.95), (79.77, 29.84),
                         (79.62, 29.75), (79.50, 29.62)],
    "Kali":             [(80.60, 30.20), (80.52, 29.95), (80.42, 29.75),
                         (80.28, 29.40), (80.14, 29.05)],
}


# ----------------------------------------------------------------- geometry ---
def _load(path: str) -> dict:
    with open(os.path.join(DATA, path), "r") as f:
        return json.load(f)


def _rings(geom: dict) -> list[list[tuple[float, float]]]:
    t, c = geom["type"], geom["coordinates"]
    if t == "Polygon":
        return [[(float(x), float(y)) for x, y in ring] for ring in c]
    if t == "MultiPolygon":
        out = []
        for poly in c:
            for ring in poly:
                out.append([(float(x), float(y)) for x, y in ring])
        return out
    return []


class Proj:
    """Equirectangular projection with latitude-corrected aspect."""

    def __init__(self, bounds, size, pad=0.06):
        (lon0, lat0, lon1, lat1) = bounds
        w, h = size
        self.w, self.h = w, h
        cx, cy = (lon0 + lon1) / 2, (lat0 + lat1) / 2
        k = math.cos(math.radians(cy))          # shrink longitude toward poles
        dw = (lon1 - lon0) * k
        dh = (lat1 - lat0)
        s = min(w * (1 - 2 * pad) / max(dw, 1e-9), h * (1 - 2 * pad) / max(dh, 1e-9))
        self.k, self.s = k, s
        self.ox = w / 2 - cx * k * s
        self.oy = h / 2 + cy * s

    def __call__(self, lon, lat):
        return (lon * self.k * self.s + self.ox, self.oy - lat * self.s)

    def many(self, pts):
        return [self(x, y) for x, y in pts]


def _bounds(features) -> tuple[float, float, float, float]:
    xs, ys = [], []
    for f in features:
        for ring in _rings(f["geometry"]):
            for x, y in ring:
                xs.append(x)
                ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys))


# ------------------------------------------------------------------- render ---
SS = 3          # supersampling factor for crisp anti-aliased edges


def _blank(size):
    return Image.new("RGBA", (size[0] * SS, size[1] * SS), (0, 0, 0, 0))


def _down(img, size):
    return img.resize(size, Image.LANCZOS)


def _fill_feature(d, proj, feat, fill=None, outline=None, width=1.0):
    for ring in _rings(feat["geometry"]):
        if len(ring) < 3:
            continue
        pts = [(x * SS, y * SS) for x, y in proj.many(ring)]
        if fill is not None:
            d.polygon(pts, fill=fill)
        if outline is not None:
            d.line(pts + [pts[0]], fill=outline, width=max(1, int(width * SS)))


def india_map(size=(1500, 1500), highlight: str = "Uttarakhand",
              base: str = "1B2A38", base_a: int = 150,
              line: str = "2E4456", hi: str = C.GOLD,
              glow: bool = True) -> Image.Image:
    """India in quiet slate, with one state lit in gold."""
    fc = _load("india.geojson")
    feats = fc["features"]
    proj = Proj(_bounds(feats), size, pad=0.045)

    img = _blank(size)
    d = ImageDraw.Draw(img)
    for f in feats:
        if f["properties"].get("st_nm") == highlight:
            continue
        _fill_feature(d, proj, f, fill=rgb(base) + (base_a,),
                      outline=rgb(line) + (110,), width=0.55)
    out = _down(img, size)

    hl = _blank(size)
    dh = ImageDraw.Draw(hl)
    for f in feats:
        if f["properties"].get("st_nm") == highlight:
            _fill_feature(dh, proj, f, fill=rgb(hi) + (235,),
                          outline=rgb(C.GOLD_LIGHT) + (255,), width=0.8)
    hl = _down(hl, size)

    if glow:
        a = np.asarray(hl, dtype=np.float32)
        g = blur_f(a[..., 3], max(3, size[0] * 0.012))
        halo = _rgba(size[0], size[1])
        halo[..., :3] = np.array(rgb(C.GOLD_LIGHT), np.float32)[None, None, :]
        halo[..., 3] = np.clip(g * 0.85, 0, 255)
        out = Image.alpha_composite(out, _to_img(halo))
    return Image.alpha_composite(out, hl)


def _uk_proj(size, pad=0.075):
    fc = _load("uttarakhand.geojson")
    return fc["features"], Proj(_bounds(fc["features"]), size, pad=pad)


def uttarakhand_layers(size=(2200, 1500)) -> dict[str, Image.Image]:
    """
    The state map, as a set of registered layers for progressive reveal.

    Keys: 'shadow', 'garhwal', 'kumaon', 'districts', 'rivers',
          'glow_garhwal', 'glow_kumaon'
    """
    feats, proj = _uk_proj(size)
    layers: dict[str, Image.Image] = {}

    # drop shadow — lifts the whole landmass off the background
    sh = _blank(size)
    ds = ImageDraw.Draw(sh)
    for f in feats:
        _fill_feature(ds, proj, f, fill=(0, 0, 0, 190))
    sh = _down(sh, size)
    a = np.asarray(sh, dtype=np.float32)
    sa = blur_f(a[..., 3], max(4, size[0] * 0.011))
    arr = _rgba(*size[::-1][::-1]) if False else _rgba(size[0], size[1])
    arr[..., :3] = 0.0
    arr[..., 3] = np.clip(sa * 0.9, 0, 255)
    layers["shadow"] = _to_img(arr).transform(
        size, Image.AFFINE, (1, 0, -size[0] * 0.006, 0, 1, -size[1] * 0.010),
        resample=Image.BICUBIC)

    for name, members, c_hi, c_lo in (
            ("garhwal", GARHWAL, C.PINE, C.FOREST_DEEP),
            ("kumaon", KUMAON, "1F4E7A", "0A1E38")):
        im = _blank(size)
        di = ImageDraw.Draw(im)
        for f in feats:
            if f["properties"]["district"] in members:
                _fill_feature(di, proj, f, fill=rgb(c_hi) + (232,))
        im = _down(im, size)
        # inner vertical shading so the fill isn't flat
        a = np.asarray(im, dtype=np.float32)
        ys = np.linspace(0, 1, size[1], dtype=np.float32)[:, None]
        lo = np.array(rgb(c_lo), np.float32)
        a[..., :3] = a[..., :3] * (1 - ys[..., None] * 0.55) + lo[None, None, :] * (ys[..., None] * 0.55)
        layers[name] = _to_img(a)

        gl = _rgba(size[0], size[1])
        gl[..., :3] = np.array(rgb(C.GOLD_LIGHT if name == "garhwal" else "7FB4E8"),
                               np.float32)[None, None, :]
        gl[..., 3] = np.clip(blur_f(np.asarray(im, np.float32)[..., 3],
                                    max(3, size[0] * 0.008)) * 0.55, 0, 255)
        layers["glow_" + name] = _to_img(gl)

    # district hairlines
    dl = _blank(size)
    dd = ImageDraw.Draw(dl)
    for f in feats:
        _fill_feature(dd, proj, f, outline=rgb(C.BEIGE) + (95,), width=0.7)
    layers["districts"] = _down(dl, size)

    # rivers
    rv = _blank(size)
    dr = ImageDraw.Draw(rv)
    for pts in RIVERS.values():
        p = [(x * SS, y * SS) for x, y in proj.many(pts)]
        dr.line(p, fill=rgb("7FC7E8") + (200,), width=max(2, int(2.2 * SS)),
                joint="curve")
    rv = _down(rv, size)
    layers["rivers"] = rv.filter(ImageFilter.GaussianBlur(0.6))
    return layers


def kauthik_markers(size=(2200, 1500), tiers=(1, 2, 3),
                    ring: bool = True) -> Image.Image:
    """Location pins for the fairs. Tier 1 fairs get an emphasis ring."""
    _, proj = _uk_proj(size)
    img = _blank(size)
    d = ImageDraw.Draw(img)
    for name, lon, lat, div, tier in KAUTHIK_SITES:
        if tier not in tiers:
            continue
        x, y = proj(lon, lat)
        x, y = x * SS, y * SS
        r = {1: 11.0, 2: 7.5, 3: 5.0}[tier] * SS
        col = rgb(C.GOLD_LIGHT) if tier == 1 else (
            rgb(C.GOLD) if tier == 2 else rgb(C.BEIGE))
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (255,))
        if tier == 1 and ring:
            for k, rr in enumerate((r * 2.1, r * 3.2)):
                d.ellipse([x - rr, y - rr, x + rr, y + rr],
                          outline=rgb(C.GOLD_LIGHT) + (150 - k * 60,),
                          width=max(1, int(1.6 * SS)))
    out = _down(img, size)
    a = np.asarray(out, dtype=np.float32)
    halo = _rgba(size[0], size[1])
    halo[..., :3] = np.array(rgb(C.GOLD_LIGHT), np.float32)[None, None, :]
    halo[..., 3] = np.clip(blur_f(a[..., 3], max(3, size[0] * 0.006)) * 0.8, 0, 255)
    return Image.alpha_composite(_to_img(halo), out)


def site_positions(size=(2200, 1500)) -> dict[str, tuple[float, float]]:
    """Fractional (x, y) of each site within the map frame — for text labels."""
    _, proj = _uk_proj(size)
    out = {}
    for name, lon, lat, div, tier in KAUTHIK_SITES:
        x, y = proj(lon, lat)
        out[name] = (x / size[0], y / size[1])
    return out


def route_layer(size=(2200, 1500), pts=None, color: str = C.SAFFRON_LIGHT,
                width: float = 3.2, dash: bool = True) -> Image.Image:
    """A pilgrimage route — e.g. the Nanda Devi Raj Jat, Nauti to Homkund."""
    _, proj = _uk_proj(size)
    pts = pts or [(79.32, 30.28), (79.42, 30.32), (79.55, 30.38),
                  (79.68, 30.42), (79.78, 30.47), (79.88, 30.52)]
    img = _blank(size)
    d = ImageDraw.Draw(img)
    p = [(x * SS, y * SS) for x, y in proj.many(pts)]
    if dash:
        for i in range(len(p) - 1):
            (x0, y0), (x1, y1) = p[i], p[i + 1]
            n = 9
            for k in range(n):
                if k % 2:
                    continue
                t0, t1 = k / n, (k + 0.85) / n
                d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                        (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
                       fill=rgb(color) + (235,), width=max(2, int(width * SS)))
    else:
        d.line(p, fill=rgb(color) + (235,), width=max(2, int(width * SS)),
               joint="curve")
    return _down(img, size)
