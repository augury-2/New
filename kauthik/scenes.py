"""
KAUTHIK — Scene Compositor
==========================
Generates (and caches on disk) the deck's background artwork, then lays it
into a slide as a stack of independently animated parallax layers.

The layer order is always the same, back to front:

    base       sky + distant ranges, baked          slowest drift + breathe
    rays        volumetric light                     slow breathe
    mid        near ranges, transparent above       medium drift
    ground     pines / stalls / temple / flags      medium-fast drift
    mist       low valley fog                       counter-drift
    particles  dust, embers, snow, fireflies        fastest drift + breathe
    scrim      readability gradient                 static
    ornament   aipan band, mandala                  static or slow breathe

Because each layer moves at its own rate and in its own direction, the frame
reads with genuine depth, and because every layer is oversized well past the
slide edge, no motion can ever reveal a border.
"""

from __future__ import annotations

import os

from PIL import Image

import artgen as A
from design import BLEED, C, LOOP_CLOUD_FAR, LOOP_CLOUD_NEAR, LOOP_DUST, \
    LOOP_EMBER, LOOP_GLOW, LOOP_KENBURNS, LOOP_MIST, LOOP_RIDGE
from pptx_helpers import picture, send_to_back

ASSETS = A.ASSETS
os.makedirs(ASSETS, exist_ok=True)

# Canvas geometry for every full-bleed layer. All layers share this aspect so
# that stacking them keeps perfect registration.
BASE_PX = (2200, 1250)
MID_PX = (1800, 1024)
FX_PX = (1800, 1024)

MOODS = ["dawn", "dusk", "ember", "night", "royal", "forest", "snow", "parchment"]

# Per-mood seeds so no two skies share a ridgeline.
SEED = {m: 11 + i * 23 for i, m in enumerate(MOODS)}


def _p(name: str) -> str:
    return os.path.join(ASSETS, name)


def _exists(name: str) -> bool:
    return os.path.exists(_p(name)) and os.path.getsize(_p(name)) > 0


# ============================================================ asset builders ===
def build_base(mood: str, force: bool = False) -> str:
    """Sky, atmospheric cloud band and the three most distant ranges, baked."""
    name = f"base_{mood}.jpg"
    if _exists(name) and not force:
        return _p(name)
    s = SEED[mood]
    img = A.sky_plate(mood, size=BASE_PX, seed=s).convert("RGBA")
    stack = A.himalaya_stack(size=BASE_PX, mood=mood, seed=s,
                            layers=5, top0=0.31, dtop=0.112, h0=0.16, dh=0.10)
    for i, layer in enumerate(stack[:3]):
        img.alpha_composite(layer)
        if i == 1:
            img.alpha_composite(A.cloud_layer(
                size=BASE_PX, seed=s + 5, alpha=0.19, band=(0.24, 0.52),
                wisp=8.0, blur=3.4))
    img.alpha_composite(A.cloud_layer(size=BASE_PX, seed=s + 8, alpha=0.13,
                                      band=(0.12, 0.38), wisp=11.0, blur=5.0))
    img.convert("RGB").save(_p(name), quality=87, optimize=True,
                            progressive=True)
    return _p(name)


def build_mid(mood: str, force: bool = False) -> str:
    """The two nearest ranges, transparent above the ridgeline."""
    name = f"mid_{mood}.png"
    if _exists(name) and not force:
        return _p(name)
    s = SEED[mood]
    stack = A.himalaya_stack(size=MID_PX, mood=mood, seed=s,
                            layers=5, top0=0.31, dtop=0.112, h0=0.16, dh=0.10)
    img = Image.new("RGBA", MID_PX, (0, 0, 0, 0))
    for layer in stack[3:]:
        img.alpha_composite(layer)
    img.save(_p(name), optimize=True)
    return _p(name)


_FX_SPECS = {
    # particle fields
    "dust":      dict(kind="particle", count=260, color="FFE7B8", rmin=1.2,
                      rmax=4.4, amin=0.10, amax=0.52, glow=2.6, band=(0.0, 1.0)),
    "embers":    dict(kind="particle", count=210, color="FFB463", rmin=1.4,
                      rmax=5.2, amin=0.14, amax=0.72, glow=3.0, band=(0.18, 1.0)),
    "snowfall":  dict(kind="particle", count=380, color="F2F8FF", rmin=1.4,
                      rmax=4.0, amin=0.14, amax=0.62, glow=2.0, streak=0.75,
                      band=(0.0, 1.0)),
    "stars":     dict(kind="particle", count=620, color="EAF2FF", rmin=0.7,
                      rmax=2.2, amin=0.16, amax=0.92, glow=3.4, band=(0.0, 0.56)),
    "fireflies": dict(kind="particle", count=150, color="FFE08A", rmin=1.8,
                      rmax=5.6, amin=0.18, amax=0.80, glow=3.6, band=(0.30, 1.0)),
    "pollen":    dict(kind="particle", count=190, color="D9EFC0", rmin=1.2,
                      rmax=3.8, amin=0.10, amax=0.46, glow=2.8, band=(0.10, 1.0)),
    # fog banks
    "mist_low":  dict(kind="mist", color="CFE0EC", alpha=0.30, y0=0.58, y1=1.0,
                      seed=9),
    "mist_mid":  dict(kind="mist", color="E4D6C0", alpha=0.24, y0=0.42, y1=0.92,
                      seed=17),
    "mist_warm": dict(kind="mist", color="F0CDA0", alpha=0.26, y0=0.46, y1=1.0,
                      seed=23),
    "mist_cold": dict(kind="mist", color="D8E8F4", alpha=0.28, y0=0.50, y1=1.0,
                      seed=29),
    # light
    "rays_top":   dict(kind="rays", sx=0.50, sy=0.06, color="FFE6B0",
                       alpha=0.22, rays=15, spread=0.9, length=1.20),
    "rays_left":  dict(kind="rays", sx=0.14, sy=0.10, color="FFDFA6",
                       alpha=0.20, rays=12, spread=1.0, length=1.15),
    "rays_right": dict(kind="rays", sx=0.86, sy=0.12, color="FFE2AE",
                       alpha=0.20, rays=12, spread=1.0, length=1.15),
    "rays_cool":  dict(kind="rays", sx=0.50, sy=0.08, color="D8E9F8",
                       alpha=0.16, rays=13, spread=0.95, length=1.15),
    # petals
    "petals":    dict(kind="petals", count=64, smin=7, smax=19, alpha=0.46),
}


def build_fx(key: str, force: bool = False) -> str:
    name = f"fx_{key}.png"
    if _exists(name) and not force:
        return _p(name)
    spec = dict(_FX_SPECS[key])
    kind = spec.pop("kind")
    if kind == "particle":
        img = A.particle_layer(size=FX_PX, seed=hash(key) % 9973, **spec)
    elif kind == "mist":
        img = A.mist_layer(size=FX_PX, **spec)
    elif kind == "rays":
        img = A.light_rays(size=FX_PX, seed=hash(key) % 7919, **spec)
    else:
        img = A.petal_layer(size=FX_PX, seed=hash(key) % 6151, **spec)
    img.save(_p(name), optimize=True)
    return _p(name)


_SCRIMS = {
    "bottom":   dict(color="04100C", a_top=0.02, a_bot=0.90, power=1.5),
    "bottom_r": dict(color="050A14", a_top=0.00, a_bot=0.86, power=1.9),
    "top":      dict(color="04100C", a_top=0.86, a_bot=0.02, power=0.6),
    "full":     dict(color="050C10", a_top=0.62, a_bot=0.80, power=1.0),
    "deep":     dict(color="04080B", a_top=0.78, a_bot=0.92, power=1.0),
    "veil":     dict(color="060F14", a_top=0.40, a_bot=0.58, power=1.0),
}


def build_scrim(key: str, force: bool = False) -> str:
    name = f"scrim_{key}.png"
    if _exists(name) and not force:
        return _p(name)
    A.scrim(size=(1400, 800), **_SCRIMS[key]).save(_p(name), optimize=True)
    return _p(name)


def build_side_scrim(side: str, force: bool = False) -> str:
    name = f"sidescrim_{side}.png"
    if _exists(name) and not force:
        return _p(name)
    A.side_scrim(size=(1400, 800), color="050D10", a_in=0.90, a_out=0.0,
                 frac=0.66, side=side).save(_p(name), optimize=True)
    return _p(name)


def build_ornaments(force: bool = False) -> None:
    jobs = {
        "orn_aipan_gold.png": lambda: A.aipan_border(
            size=(2400, 128), color=C.GOLD, alpha=0.50, motifs=9),
        "orn_aipan_snow.png": lambda: A.aipan_border(
            size=(2400, 128), color=C.SNOW, alpha=0.34, motifs=9),
        "orn_mandala.png": lambda: A.mandala(
            size=(1500, 1500), color=C.GOLD, alpha=0.14),
        "orn_mandala_soft.png": lambda: A.mandala(
            size=(1500, 1500), color=C.BEIGE, alpha=0.10),
        "orn_temple_dark.png": lambda: A.temple_silhouette(
            size=(1500, 1250), color="050F0B", alpha=0.97),
        "orn_temple_ink.png": lambda: A.temple_silhouette(
            size=(1500, 1250), color="0A0C10", alpha=0.94),
        "orn_pines.png": lambda: A.pine_layer(
            size=(2200, 700), color="04120D", alpha=0.98, count=58, ground=0.12),
        "orn_pines_soft.png": lambda: A.pine_layer(
            size=(2200, 620), color="0A1A22", alpha=0.85, count=46,
            hmin=0.28, hmax=0.70, ground=0.10, seed=21),
        "orn_stalls.png": lambda: A.stall_layer(
            size=(2200, 620), color="0A1712", alpha=0.97, count=10),
        "orn_flags.png": lambda: A.prayer_flag_layer(
            size=(2400, 520), lines=2, alpha=0.85, per_line=42),
        "tex_paper.png": lambda: A.texture_overlay(
            size=(1600, 900), kind="paper", alpha=0.085),
        "tex_wool.png": lambda: A.texture_overlay(
            size=(1600, 900), kind="wool", alpha=0.075),
        "glow_gold.png": lambda: A.glow_orb(
            size=(900, 900), color="FFD98A", alpha=0.42),
        "glow_cool.png": lambda: A.glow_orb(
            size=(900, 900), color="9FC8F0", alpha=0.30),
    }
    for name, fn in jobs.items():
        if _exists(name) and not force:
            continue
        fn().save(_p(name), optimize=True)


def build_all(force: bool = False, verbose: bool = True) -> None:
    for m in MOODS:
        if verbose:
            print(f"  · sky/ranges  {m}")
        build_base(m, force)
        build_mid(m, force)
    for k in _FX_SPECS:
        build_fx(k, force)
    for k in _SCRIMS:
        build_scrim(k, force)
    for s in ("left", "right"):
        build_side_scrim(s, force)
    build_ornaments(force)
    if verbose:
        tot = sum(os.path.getsize(os.path.join(ASSETS, f))
                  for f in os.listdir(ASSETS) if os.path.isfile(os.path.join(ASSETS, f)))
        print(f"  · assets ready ({tot / 1e6:.1f} MB)")


# =============================================================== composition ===
B = BLEED


def scene(slide, tl, mood: str = "dawn", *,
          rays: str | None = "rays_top",
          mid: bool = True,
          ground: str | None = None,      # 'pines' | 'pines_soft' | 'stalls' | 'temple'
          ground_h: float = 2.10,
          mist: str | None = "mist_low",
          particles: str | None = "dust",
          scrim: str | None = "bottom",
          side: str | None = None,        # 'left' | 'right'
          aipan: str | None = None,       # 'gold' | 'snow'
          mandala: tuple | None = None,   # (cx, cy, diameter)
          texture: str | None = None,     # 'paper' | 'wool'
          glow: tuple | None = None,      # (cx, cy, d, 'gold'|'cool')
          flags: bool = False,
          live: bool = True) -> dict:
    """
    Build one slide's living background and register its looping animations.

    Returns the created shapes by role so callers can adjust or reorder them.
    """
    out: dict = {}

    base = picture(slide, build_base(mood), B["x"], B["y"], B["w"], B["h"],
                   name="bgBase")
    out["base"] = base
    if live:
        tl.loop_drift(base, 0.016, 0.007, LOOP_RIDGE)
        tl.loop_zoom(base, 1.035, LOOP_KENBURNS)

    if rays:
        r = picture(slide, build_fx(rays), B["x"], B["y"], B["w"], B["h"],
                    name="bgRays")
        out["rays"] = r
        if live:
            tl.loop_zoom(r, 1.070, LOOP_GLOW)
            tl.loop_drift(r, -0.020, 0.004, LOOP_CLOUD_FAR)

    if mid:
        m = picture(slide, build_mid(mood), B["x"], B["y"], B["w"], B["h"],
                    name="bgMid")
        out["mid"] = m
        if live:
            tl.loop_drift(m, 0.034, 0.011, LOOP_CLOUD_FAR)
            tl.loop_zoom(m, 1.025, LOOP_KENBURNS + 6000)

    if ground:
        if ground == "temple":
            g = picture(slide, _p("orn_temple_dark.png"),
                        6.05, 7.5 - ground_h, 2.55, ground_h, name="bgGround")
        else:
            asset = {"pines": "orn_pines.png", "pines_soft": "orn_pines_soft.png",
                     "stalls": "orn_stalls.png"}[ground]
            g = picture(slide, _p(asset), -1.10, 7.5 - ground_h + 0.02,
                        15.55, ground_h, name="bgGround")
        out["ground"] = g
        if live:
            tl.loop_drift(g, 0.024 if ground != "temple" else 0.008,
                          0.005, LOOP_CLOUD_NEAR)

    if flags:
        f = picture(slide, _p("orn_flags.png"), -0.85, 0.10, 15.05, 1.55,
                    name="bgFlags")
        out["flags"] = f
        if live:
            tl.loop_drift(f, 0.030, 0.012, LOOP_CLOUD_NEAR - 3000)

    if mist:
        mi = picture(slide, build_fx(mist), B["x"], B["y"], B["w"], B["h"],
                     name="bgMist")
        out["mist"] = mi
        if live:
            tl.loop_drift(mi, -0.058, -0.013, LOOP_MIST)
            tl.loop_zoom(mi, 1.055, LOOP_MIST + 5000)

    if particles:
        pa = picture(slide, build_fx(particles), B["x"], B["y"], B["w"], B["h"],
                     name="bgParticles")
        out["particles"] = pa
        if live:
            dur = LOOP_EMBER if particles in ("embers", "fireflies") else LOOP_DUST
            tl.loop_drift(pa, 0.072, -0.034, dur)
            tl.loop_zoom(pa, 1.090, dur + 4000)

    if glow:
        cx, cy, d, tone = glow
        gl = picture(slide, _p("glow_%s.png" % tone), cx - d / 2, cy - d / 2, d, d,
                     name="bgGlow")
        out["glow"] = gl
        if live:
            tl.loop_zoom(gl, 1.10, LOOP_GLOW + 3000)

    if texture:
        tx = picture(slide, _p("tex_%s.png" % texture), 0, 0, 13.3333, 7.5,
                     name="bgTexture")
        out["texture"] = tx

    if scrim:
        sc = picture(slide, build_scrim(scrim), 0, 0, 13.3333, 7.5, name="bgScrim")
        out["scrim"] = sc

    if side:
        ss = picture(slide, build_side_scrim(side), 0, 0, 13.3333, 7.5,
                     name="bgSideScrim")
        out["sidescrim"] = ss

    if mandala:
        cx, cy, d = mandala
        md = picture(slide, _p("orn_mandala.png"), cx - d / 2, cy - d / 2, d, d,
                     name="bgMandala")
        out["mandala"] = md
        if live:
            tl.loop_zoom(md, 1.045, LOOP_CLOUD_NEAR + 7000)

    if aipan:
        ai = picture(slide, _p("orn_aipan_%s.png" % aipan), -0.30, 7.5 - 0.42,
                     13.93, 0.34, name="bgAipan")
        out["aipan"] = ai

    return out
