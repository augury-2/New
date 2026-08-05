"""
KAUTHIK — Design System
=======================
Palette, typography, layout grid and geometry constants for the
"Kauthik" cinematic presentation.

Everything downstream (art generation, slide layout, animation) reads
its constants from here so the deck stays visually consistent.
"""

from __future__ import annotations

# ---------------------------------------------------------------- geometry ---
# 16:9 widescreen, PowerPoint default widescreen size.
SLIDE_W_IN = 13.3333333
SLIDE_H_IN = 7.5
EMU_PER_IN = 914400
SLIDE_W_EMU = int(round(SLIDE_W_IN * EMU_PER_IN))   # 12192000
SLIDE_H_EMU = int(round(SLIDE_H_IN * EMU_PER_IN))   # 6858000

# Master margins (inches). Generous cinematic margins, safe for auditoriums.
MARGIN_X = 1.05
MARGIN_Y = 0.72
CONTENT_W = SLIDE_W_IN - 2 * MARGIN_X          # 11.233
BASELINE = 0.18                                # vertical rhythm unit

# Oversized bleed geometry used by every drifting background layer, so that
# parallax motion never exposes a hard edge. (inches)
BLEED = dict(x=-1.35, y=-0.80, w=16.05, h=9.10)
# A tighter bleed for layers that only breathe (scale) rather than drift.
BLEED_SOFT = dict(x=-0.62, y=-0.36, w=14.57, h=8.22)

# Render resolutions for generated artwork (px).
RES_BASE = (2560, 1440)        # full-bleed base plates (16:9)
RES_BLEED = (2848, 1616)       # ~16.05in x 9.10in at 177 dpi-equivalent
RES_HALF = (1440, 1440)


# ----------------------------------------------------------------- palette ---
# Uttarakhand-inspired. Hex without '#'.
class C:
    # Cores — deep, cinematic darks
    FOREST_DEEP = "07211A"      # deepest forest green (near-black)
    FOREST = "0E2A22"           # deep forest green
    FOREST_MID = "16463A"       # mid forest
    PINE = "1E5C48"

    NIGHT = "060D1A"            # near-black royal-blue night
    ROYAL_DEEP = "0A1E3C"       # deep royal blue
    ROYAL = "12386C"            # royal blue
    ROYAL_LIT = "1F5490"        # lit royal blue
    HAZE_BLUE = "35618F"        # atmospheric ridge haze

    # Lights
    SNOW = "F8F6F1"             # snow white (never pure white)
    SNOW_DIM = "E4E0D6"
    BEIGE = "E8DCC8"            # warm beige
    BEIGE_DEEP = "D3C3A6"

    SLATE = "4A5560"            # slate grey
    SLATE_LIGHT = "8A939C"
    SLATE_DARK = "2A323A"

    # Accents — the festival
    GOLD = "E3B34A"             # golden yellow (primary accent)
    GOLD_LIGHT = "F2CE7B"
    GOLD_DEEP = "C08F2A"
    SAFFRON = "E0762A"          # saffron
    SAFFRON_LIGHT = "F0912F"
    MAROON = "6E1B27"           # maroon
    MAROON_LIGHT = "8E2833"
    COPPER = "B87333"           # copper
    COPPER_LIGHT = "D08F4E"
    EARTH = "4A3428"            # earth brown
    EARTH_LIGHT = "6B4E3B"

    # Utility
    INK = "0B1014"


def rgb(hexstr: str) -> tuple[int, int, int]:
    hexstr = hexstr.lstrip("#")
    return (int(hexstr[0:2], 16), int(hexstr[2:4], 16), int(hexstr[4:6], 16))


def rgba(hexstr: str, a: float | int) -> tuple[int, int, int, int]:
    """a as 0..1 float or 0..255 int."""
    alpha = int(round(a * 255)) if isinstance(a, float) and a <= 1.0 else int(a)
    return rgb(hexstr) + (max(0, min(255, alpha)),)


def mix(a: str, b: str, t: float) -> tuple[int, int, int]:
    ra, ga, ba = rgb(a)
    rb, gb, bb = rgb(b)
    return (
        int(round(ra + (rb - ra) * t)),
        int(round(ga + (gb - ga) * t)),
        int(round(ba + (bb - ba) * t)),
    )


def mix_hex(a: str, b: str, t: float) -> str:
    r, g, bl = mix(a, b, t)
    return f"{r:02X}{g:02X}{bl:02X}"


# -------------------------------------------------------------- typography ---
# Display / title faces (serif, engraved, editorial).
F_DISPLAY = "Cinzel"                 # engraved Roman caps — chapter numerals, hero
F_SERIF = "Cormorant Garamond"       # literary serif — quotes, long display lines
F_EDITORIAL = "Playfair Display"     # high-contrast editorial serif — statements
# Body / UI faces (geometric humanist sans).
F_BODY = "Poppins"                   # body copy, labels
F_UI = "Montserrat"                  # eyebrows, kickers, data labels, captions

# Type scale (pt) — large, auditorium-readable.
T_HERO = 104          # cover title
T_H1 = 62             # section divider titles
T_H2 = 44             # slide titles
T_H3 = 30             # sub-heads / card titles
T_QUOTE = 40          # pull quotes
T_LEAD = 22           # lead paragraph
T_BODY = 17           # body copy
T_SMALL = 13.5        # captions
T_MICRO = 10.5        # micro labels / sources
T_EYEBROW = 12.5      # tracked-out kickers
T_STAT = 66           # big numbers
T_STAT_SM = 40
T_NUMERAL = 190       # ghosted chapter numerals

TRACK_EYEBROW = 340    # character spacing (1/100 pt) for kickers
TRACK_DISPLAY = 90
TRACK_TIGHT = -20


# ------------------------------------------------------------------ motion ---
# Durations in ms. Everything slow, eased, cinematic.
D_TRANSITION = 1500          # slide transition
D_TRANSITION_SLOW = 2200     # divider transition
D_FADE = 1100                # standard element fade-in
D_FADE_SLOW = 1700
D_RISE = 1300                # fade + drift up
STAGGER = 260                # ms between sequenced siblings

# Looping background layer periods (ms). Deliberately non-harmonic so the
# composite never visibly repeats.
LOOP_SKY = 46000
LOOP_CLOUD_FAR = 38000
LOOP_CLOUD_NEAR = 27000
LOOP_MIST = 31000
LOOP_DUST = 23000
LOOP_EMBER = 17000
LOOP_GLOW = 13000
LOOP_RIDGE = 53000
LOOP_KENBURNS = 41000

EASE = 45000                 # accel/decel (1/1000 %) → 45% ease in, 45% out
