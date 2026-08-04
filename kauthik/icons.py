"""
KAUTHIK — Icon Library
======================
A single, coherent set of stroked line icons drawn on a 100x100 grid and
rendered at 4x supersampling. Deliberately geometric and minimal — the
visual register of a keynote, not clipart — and every glyph is specific to
Kauthik's subject matter (hurka drums, ransingha horns, ringal baskets,
Aipan rosettes, pichhora cloth) rather than generic stock symbols.
"""

from __future__ import annotations

import math
import os

from PIL import Image, ImageDraw

from design import C, rgb

ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icons")
os.makedirs(ICON_DIR, exist_ok=True)

SS = 4                      # supersample
G = 100.0                   # design grid


class Pen:
    """Thin wrapper so icon routines read like drawing instructions."""

    def __init__(self, d: ImageDraw.ImageDraw, col, lw: float):
        self.d, self.col, self.lw = d, col, lw

    def _s(self, pts):
        return [(x * SS, y * SS) for x, y in pts]

    def line(self, pts, w=1.0, joint="curve"):
        self.d.line(self._s(pts), fill=self.col,
                    width=max(1, int(round(self.lw * w * SS))), joint=joint)

    def poly(self, pts, w=1.0):
        self.line(list(pts) + [pts[0]], w=w)

    def fillpoly(self, pts):
        self.d.polygon(self._s(pts), fill=self.col)

    def circle(self, cx, cy, r, w=1.0, fill=False):
        box = [(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS]
        if fill:
            self.d.ellipse(box, fill=self.col)
        else:
            self.d.ellipse(box, outline=self.col,
                           width=max(1, int(round(self.lw * w * SS))))

    def dot(self, cx, cy, r=2.0):
        self.circle(cx, cy, r, fill=True)

    def arc(self, cx, cy, r, a0, a1, w=1.0):
        box = [(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS]
        self.d.arc(box, a0, a1, fill=self.col,
                   width=max(1, int(round(self.lw * w * SS))))

    def rect(self, x0, y0, x1, y1, w=1.0, r=0.0):
        if r > 0:
            self.d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS],
                                     radius=r * SS, outline=self.col,
                                     width=max(1, int(round(self.lw * w * SS))))
        else:
            self.d.rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], outline=self.col,
                             width=max(1, int(round(self.lw * w * SS))))

    def fillrect(self, x0, y0, x1, y1, r=0.0):
        if r > 0:
            self.d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS],
                                     radius=r * SS, fill=self.col)
        else:
            self.d.rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=self.col)


# ============================================================== music & dance ==
def i_dhol(p: Pen):
    """Dhol — the double-headed barrel drum that opens every Kauthik."""
    p.line([(22, 30), (18, 50), (22, 70)])
    p.line([(78, 30), (82, 50), (78, 70)])
    p.line([(22, 30), (78, 30)])
    p.line([(22, 70), (78, 70)])
    for i in range(5):
        x0 = 24 + i * 13
        p.line([(x0, 31), (x0 + 7, 69)], w=0.62)
        p.line([(x0 + 7, 31), (x0, 69)], w=0.62)
    p.line([(30, 22), (70, 22)], w=0.8)
    p.line([(50, 22), (50, 30)], w=0.8)


def i_damau(p: Pen):
    """Damau — the kettle drum, always paired with the dhol."""
    p.line([(18, 52), (82, 52)])
    p.arc(50, 52, 32, 0, 180)
    p.line([(24, 46), (76, 46)], w=0.65)
    for k in range(6):
        x = 27 + k * 9.2
        p.line([(x, 47), (x + 4, 51)], w=0.5)
    p.line([(30, 22), (42, 42)], w=1.0)          # sticks
    p.line([(28, 20), (34, 22)], w=0.9)
    p.line([(70, 22), (58, 42)], w=1.0)
    p.line([(66, 20), (72, 22)], w=0.9)
    p.line([(34, 84), (66, 84)], w=0.7)
    p.line([(40, 52), (40, 84)], w=0.0)


def i_hurka(p: Pen):
    """Hurka — the hourglass drum of the Jhora circle."""
    p.line([(30, 22), (44, 50), (30, 78)])
    p.line([(70, 22), (56, 50), (70, 78)])
    p.line([(30, 22), (70, 22)])
    p.line([(30, 78), (70, 78)])
    p.line([(44, 50), (56, 50)], w=0.7)
    for i in range(4):
        y = 28 + i * 12
        p.line([(32 + i * 3, y), (68 - i * 3, y + 8)], w=0.5)


def i_ransingha(p: Pen):
    """Ransingha — the crescent-curved copper horn of Garhwal."""
    inner, outer = [], []
    for i in range(37):
        t = i / 36
        a = math.pi * (1.06 - 0.72 * t)          # sweep the crescent
        rad = 34.0
        tube = 3.0 + 9.0 * (t ** 2.2)            # bore widens toward the bell
        cx, cy = 52, 74
        nx, ny = math.cos(a), -math.sin(a)
        inner.append((cx + nx * (rad - tube), cy + ny * (rad - tube)))
        outer.append((cx + nx * (rad + tube), cy + ny * (rad + tube)))
    p.line(inner, w=1.0)
    p.line(outer, w=1.0)
    p.line([inner[0], outer[0]], w=1.0)          # mouthpiece
    # flared bell
    bx, by = outer[-1], inner[-1]
    p.line([by, (by[0] + 9, by[1] - 12)], w=1.0)
    p.line([bx, (bx[0] + 15, bx[1] - 3)], w=1.0)
    p.line([(by[0] + 9, by[1] - 12), (bx[0] + 15, bx[1] - 3)], w=1.0)
    p.dot(inner[0][0] - 2, inner[0][1] + 2, 3.0)


def i_masakbeen(p: Pen):
    """Masakbeen — the Himalayan bagpipe."""
    p.line([(30, 44), (22, 66), (38, 82), (62, 78), (66, 56), (52, 42), (30, 44)], w=1.0)
    p.line([(52, 44), (74, 26)], w=1.0)          # blowpipe
    p.line([(70, 22), (80, 30)], w=0.9)
    p.line([(36, 44), (30, 22)], w=0.95)         # drone
    p.line([(25, 20), (35, 22)], w=0.85)
    p.line([(44, 43), (44, 24)], w=0.8)          # chanter
    p.line([(40, 22), (48, 22)], w=0.75)
    p.dot(44, 20, 2.2)
    p.dot(30, 20, 2.2)


def i_bhankora(p: Pen):
    """Bhankora — the long straight temple trumpet."""
    p.line([(12, 62), (72, 44)], w=1.05)
    p.line([(14, 70), (72, 58)], w=1.05)
    p.line([(12, 62), (14, 70)], w=1.0)
    p.line([(72, 44), (92, 30)], w=1.05)         # bell flare
    p.line([(72, 58), (92, 62)], w=1.05)
    p.line([(92, 30), (92, 62)], w=1.05)
    for k in range(3):
        x = 28 + k * 16
        p.line([(x, 62 - k * 4.6), (x + 1, 68 - k * 3.2)], w=0.55)


def i_sword(p: Pen):
    """Chholiya — the sword-and-shield dance of Kumaon."""
    p.circle(38, 56, 26, w=0.85)                 # farra (shield)
    p.circle(38, 56, 16, w=0.55)
    p.dot(38, 56, 3.0)
    p.line([(58, 82), (58, 40)], w=1.15)         # blade
    p.line([(64, 82), (64, 40)], w=1.15)
    p.line([(58, 40), (61, 26), (64, 40)], w=1.1)
    p.line([(48, 82), (74, 82)], w=1.1)          # crossguard
    p.line([(61, 82), (61, 92)], w=1.0)          # grip
    p.dot(61, 94, 3.0)


def i_jhora(p: Pen):
    """Jhora — dancers with linked arms moving in a slow circle."""
    p.circle(50, 52, 30, w=0.7)
    for k in range(6):
        a = math.pi * 2 * k / 6 - math.pi / 2
        x, y = 50 + math.cos(a) * 30, 52 + math.sin(a) * 30
        p.dot(x, y, 5.2)
    p.arc(50, 52, 16, 0, 300, w=0.8)


def i_dancer(p: Pen):
    p.circle(50, 20, 9)
    p.line([(50, 29), (50, 56)])
    p.line([(50, 36), (26, 24)])
    p.line([(50, 36), (74, 26)])
    p.line([(50, 56), (34, 84)])
    p.line([(50, 56), (68, 82)])
    p.line([(34, 84), (24, 84)], w=0.8)


# ==================================================================== spirit ==
def i_temple(p: Pen):
    p.line([(18, 84), (82, 84)])
    p.line([(24, 84), (24, 58)])
    p.line([(76, 84), (76, 58)])
    p.line([(20, 58), (80, 58)])
    pts = []
    for i in range(25):
        t = i / 24
        half = 26 * (1 - t ** 1.5) ** 0.8
        pts.append((50 - half, 58 - 34 * t))
    p.line(pts)
    p.line([(x + 2 * (50 - x), y) for x, y in pts])
    p.line([(50, 24), (50, 14)], w=0.9)
    p.dot(50, 12, 3.4)
    p.line([(42, 84), (42, 68), (58, 68), (58, 84)], w=0.8)


def i_bell(p: Pen):
    p.line([(50, 14), (50, 24)], w=0.9)
    p.circle(50, 12, 4, w=0.9)
    pts = [(30, 70)]
    for i in range(21):
        t = i / 20
        a = math.pi * (1.0 - t)
        pts.append((50 - math.cos(a) * 20, 70 - math.sin(a) * 44))
    p.line(pts)
    p.line([(28, 70), (72, 70)])
    p.dot(50, 78, 4.0)
    p.line([(50, 70), (50, 76)], w=0.7)


def i_diya(p: Pen):
    p.arc(50, 62, 26, 0, 180)
    p.line([(24, 62), (76, 62)])
    p.line([(50, 58), (50, 44)], w=0.8)
    p.line([(44, 36), (50, 22), (56, 36)], w=1.0)
    p.arc(50, 38, 8, 200, 340, w=0.8)


def i_trident(p: Pen):
    p.line([(50, 22), (50, 86)], w=1.1)
    p.line([(30, 22), (30, 46)], w=1.0)
    p.line([(70, 22), (70, 46)], w=1.0)
    p.line([(30, 46), (50, 56), (70, 46)], w=1.0)
    p.line([(26, 22), (34, 22)], w=0.9)
    p.line([(66, 22), (74, 22)], w=0.9)
    p.line([(46, 18), (54, 18)], w=0.9)
    p.line([(36, 68), (64, 68)], w=0.8)


def i_mountain(p: Pen):
    p.line([(8, 78), (34, 34), (48, 54), (62, 26), (92, 78)])
    p.line([(8, 78), (92, 78)], w=0.8)
    p.line([(27, 44), (34, 34), (41, 44), (36, 41), (31, 47)], w=0.7)
    p.line([(55, 37), (62, 26), (69, 38)], w=0.7)


def i_river(p: Pen):
    for k, y in enumerate((36, 54, 72)):
        pts = [(10 + i * 4, y + math.sin(i * 0.55 + k) * 6) for i in range(21)]
        p.line(pts, w=1.0 - k * 0.12)


def i_sunrise(p: Pen):
    p.arc(50, 66, 24, 180, 360)
    p.line([(14, 66), (86, 66)])
    for k in range(7):
        a = math.pi * (0.10 + 0.80 * k / 6)
        p.line([(50 - math.cos(a) * 32, 66 - math.sin(a) * 32),
                (50 - math.cos(a) * 40, 66 - math.sin(a) * 40)], w=0.8)


def i_flag(p: Pen):
    p.line([(28, 16), (28, 88)], w=1.1)
    p.line([(28, 20), (76, 30), (28, 42)], w=1.0)
    p.line([(28, 48), (66, 56), (28, 66)], w=0.85)
    p.line([(18, 88), (38, 88)], w=0.9)


# ====================================================================== food ==
def i_pot(p: Pen):
    p.arc(50, 52, 30, 20, 160, w=1.0)
    p.line([(21, 62), (26, 82), (74, 82), (79, 62)])
    p.line([(18, 60), (82, 60)])
    p.line([(30, 52), (34, 34)], w=0.7)
    p.line([(50, 50), (50, 30)], w=0.7)
    p.line([(70, 52), (66, 34)], w=0.7)


def i_thali(p: Pen):
    p.circle(50, 54, 34)
    p.circle(50, 54, 26, w=0.7)
    for k in range(3):
        a = math.pi * 2 * k / 3 - math.pi / 2
        p.circle(50 + math.cos(a) * 15, 54 + math.sin(a) * 15, 7, w=0.8)
    p.line([(16, 54), (84, 54)], w=0.0)


def i_millet(p: Pen):
    p.line([(50, 88), (50, 40)], w=1.0)
    for k in range(6):
        y = 42 + k * 8
        s = 1.0 - k * 0.09
        p.line([(50, y), (50 - 16 * s, y - 8 * s)], w=0.8)
        p.line([(50, y), (50 + 16 * s, y - 8 * s)], w=0.8)
    p.line([(50, 40), (50, 26)], w=0.8)
    p.dot(50, 24, 3.0)


def i_sweet(p: Pen):
    p.circle(50, 56, 26)
    for k in range(10):
        a = math.pi * 2 * k / 10
        p.dot(50 + math.cos(a) * 17, 56 + math.sin(a) * 17, 2.4)
    p.arc(50, 56, 10, 0, 360, w=0.7)
    p.line([(34, 26), (50, 34), (66, 26)], w=0.8)


def i_leaf(p: Pen):
    p.line([(24, 80), (50, 24), (76, 80)], w=0.0)
    pts = [(50, 20)]
    for i in range(1, 21):
        t = i / 20
        pts.append((50 + math.sin(math.pi * t) * 24, 20 + 60 * t))
    p.line(pts)
    p.line([(50, 20)] + [(50 - (x - 50), y) for x, y in pts[1:]])
    p.line([(50, 22), (50, 86)], w=0.7)
    for k in range(4):
        y = 34 + k * 13
        p.line([(50, y), (50 + 13 - k * 2, y + 8)], w=0.5)
        p.line([(50, y), (50 - 13 + k * 2, y + 8)], w=0.5)


def i_chilli(p: Pen):
    """Lakhori mirch — the small fierce chilli of Almora."""
    left, right = [], []
    for i in range(29):
        t = i / 28
        cx = 46 + 14 * math.sin(t * 1.35)
        cy = 32 + 52 * t
        half = 13.0 * math.sin(math.pi * (0.12 + 0.80 * t)) * (1.0 - 0.55 * t)
        left.append((cx - half, cy))
        right.append((cx + half, cy))
    p.line(left + right[::-1] + [left[0]], w=1.05)
    p.line([(46, 32), (40, 18)], w=1.0)          # stalk
    p.line([(40, 18), (30, 14)], w=0.9)
    p.line([(40, 18), (50, 12)], w=0.9)


# ===================================================================== crafts ==
def i_aipan(p: Pen):
    """Aipan rosette — white rice paste on ochre, drawn at the threshold."""
    for k in range(8):
        a = math.pi * 2 * k / 8
        p.line([(50 + math.cos(a) * 10, 54 + math.sin(a) * 10),
                (50 + math.cos(a + 0.34) * 22, 54 + math.sin(a + 0.34) * 22),
                (50 + math.cos(a) * 34, 54 + math.sin(a) * 34),
                (50 + math.cos(a - 0.34) * 22, 54 + math.sin(a - 0.34) * 22),
                (50 + math.cos(a) * 10, 54 + math.sin(a) * 10)], w=0.8)
    p.circle(50, 54, 8, w=0.9)
    p.dot(50, 54, 2.6)
    for k in range(8):
        a = math.pi * 2 * k / 8 + math.pi / 8
        p.dot(50 + math.cos(a) * 42, 54 + math.sin(a) * 42, 2.4)


def i_copper(p: Pen):
    """Tamta copperware of Almora."""
    p.arc(50, 58, 28, 0, 180, w=1.0)
    p.line([(22, 58), (22, 44)], w=1.0)
    p.line([(78, 58), (78, 44)], w=1.0)
    p.arc(50, 44, 28, 180, 360, w=0.9)
    p.line([(38, 34), (38, 22), (62, 22), (62, 34)], w=0.9)
    p.line([(32, 22), (68, 22)], w=0.8)
    p.arc(50, 66, 16, 0, 180, w=0.6)


def i_ringal(p: Pen):
    """Ringal — Himalayan dwarf-bamboo basketry."""
    p.line([(22, 34), (30, 82), (70, 82), (78, 34)])
    p.line([(20, 34), (80, 34)])
    for k in range(3):
        y = 46 + k * 13
        p.line([(24 + k * 2.2, y), (76 - k * 2.2, y)], w=0.6)
    for k in range(5):
        x = 28 + k * 11
        p.line([(x + 2, 36), (x - 1 + (k - 2) * 1.2, 80)], w=0.5)
    p.arc(50, 34, 26, 200, 340, w=0.9)


def i_loom(p: Pen):
    """Backstrap loom — the woollen weaving of the high valleys."""
    p.rect(18, 22, 82, 82, w=1.0)
    for k in range(5):
        x = 26 + k * 12
        p.line([(x, 24), (x, 80)], w=0.55)
    for k in range(3):
        y = 38 + k * 14
        p.line([(20, y), (80, y)], w=0.8)
    p.line([(14, 56), (86, 56)], w=1.0)
    p.dot(86, 56, 3.0)


def i_chisel(p: Pen):
    """Woodcarving — the carved kholi doorframes of hill houses."""
    # the carved doorframe
    p.line([(20, 88), (20, 30), (60, 30), (60, 88)], w=1.0)
    p.line([(14, 30), (66, 30)], w=1.0)
    p.line([(14, 24), (66, 24)], w=0.8)
    for k in range(4):
        y = 40 + k * 12
        p.line([(24, y), (30, y)], w=0.6)
        p.line([(50, y), (56, y)], w=0.6)
    p.circle(40, 46, 7, w=0.7)
    # the chisel and mallet
    p.line([(78, 20), (66, 44)], w=1.1)
    p.line([(66, 44), (60, 52)], w=1.0)
    p.line([(74, 16), (86, 24)], w=1.0)
    p.line([(80, 56), (94, 42)], w=1.0)
    p.line([(84, 60), (98, 46)], w=1.0)
    p.line([(80, 56), (84, 60)], w=1.0)
    p.line([(94, 42), (98, 46)], w=1.0)


def i_pichhora(p: Pen):
    """Rangwali Pichhora — the hand-painted odhni of Kumaoni women."""
    p.line([(22, 22), (78, 22)])
    p.line([(22, 22), (18, 82)])
    p.line([(78, 22), (82, 82)])
    pts = [(18, 82)]
    for i in range(1, 13):
        t = i / 12
        pts.append((18 + 64 * t, 82 + (6 if i % 2 else -4)))
    pts.append((82, 82))
    p.line(pts, w=0.9)
    for k in range(3):
        for j in range(2):
            cx, cy = 34 + k * 16, 40 + j * 20
            p.circle(cx, cy, 5, w=0.6)
            p.dot(cx, cy, 1.8)


def i_jewel(p: Pen):
    """Nath — the ceremonial nose ring of the hills."""
    p.circle(46, 52, 28, w=1.1)
    p.circle(46, 52, 20, w=0.6)
    p.dot(74, 52, 4.2)
    p.line([(74, 48), (88, 40)], w=0.8)
    for k in range(5):
        a = math.pi * (0.25 + 0.5 * k / 4)
        p.dot(46 + math.cos(a) * 28, 52 + math.sin(a) * 28, 2.2)


# =================================================================== economy ==
def i_coin(p: Pen):
    """The rupee — livelihood earned at the fair."""
    p.circle(50, 52, 32)
    p.circle(50, 52, 25, w=0.55)
    p.line([(38, 34), (64, 34)], w=1.05)         # ₹ upper bar
    p.line([(38, 43), (64, 43)], w=1.05)         # ₹ lower bar
    p.line([(38, 34), (38, 43)], w=0.0)
    p.line([(56, 34), (52, 55), (38, 55)], w=1.05)   # bowl of the glyph
    p.line([(44, 55), (62, 72)], w=1.05)         # descending stroke
    p.line([(38, 55), (44, 55)], w=0.0)


def i_scales(p: Pen):
    p.line([(50, 20), (50, 78)], w=1.0)
    p.line([(20, 32), (80, 32)], w=1.0)
    p.arc(32, 32, 12, 0, 180, w=0.9)
    p.arc(68, 32, 12, 0, 180, w=0.9)
    p.line([(34, 78), (66, 78)], w=1.0)
    p.dot(50, 18, 3.2)


def i_gi_seal(p: Pen):
    """Geographical Indication — the certified origin of a hill product."""
    p.circle(50, 46, 26)
    for k in range(16):
        a = math.pi * 2 * k / 16
        p.line([(50 + math.cos(a) * 26, 46 + math.sin(a) * 26),
                (50 + math.cos(a) * 31, 46 + math.sin(a) * 31)], w=0.7)
    p.arc(50, 46, 14, 40, 320, w=1.0)
    p.line([(50, 46), (62, 46)], w=1.0)
    p.line([(38, 72), (34, 92), (50, 84), (66, 92), (62, 72)], w=0.9)


def i_cart(p: Pen):
    p.line([(16, 30), (28, 30), (36, 64), (80, 64)], w=1.0)
    p.line([(30, 40), (84, 40), (80, 64)], w=1.0)
    p.circle(42, 76, 8, w=1.0)
    p.circle(74, 76, 8, w=1.0)
    p.line([(44, 44), (44, 60)], w=0.6)
    p.line([(58, 44), (58, 60)], w=0.6)
    p.line([(72, 44), (72, 60)], w=0.6)


def i_hands(p: Pen):
    """Community — the fair as a gathering, not a transaction."""
    p.circle(50, 50, 34, w=0.6)
    for k in range(5):
        a = math.pi * 2 * k / 5 - math.pi / 2
        cx, cy = 50 + math.cos(a) * 30, 50 + math.sin(a) * 30
        p.circle(cx, cy, 7.5, w=0.9)
        p.dot(cx, cy, 2.0)
    for k in range(5):
        a0 = math.pi * 2 * k / 5 - math.pi / 2
        a1 = math.pi * 2 * (k + 1) / 5 - math.pi / 2
        p.line([(50 + math.cos(a0) * 21, 50 + math.sin(a0) * 21),
                (50 + math.cos(a1) * 21, 50 + math.sin(a1) * 21)], w=0.7)


# =================================================================== tourism ==
def i_camera(p: Pen):
    p.rect(16, 34, 84, 80, w=1.0, r=6)
    p.circle(50, 57, 17, w=1.0)
    p.circle(50, 57, 9, w=0.6)
    p.line([(36, 34), (42, 24), (58, 24), (64, 34)], w=0.9)
    p.dot(74, 44, 3.0)


def i_trail(p: Pen):
    pts = [(18, 84)]
    for i in range(1, 25):
        t = i / 24
        pts.append((18 + 64 * t + math.sin(t * 5.5) * 10, 84 - 60 * t))
    p.line(pts)
    p.dot(18, 84, 4.0)
    p.dot(pts[-1][0], pts[-1][1], 4.0)
    p.circle(pts[-1][0], pts[-1][1], 9, w=0.7)


def i_homestay(p: Pen):
    p.line([(14, 50), (50, 20), (86, 50)], w=1.1)
    p.line([(24, 46), (24, 84), (76, 84), (76, 46)], w=1.0)
    p.rect(40, 60, 60, 84, w=0.9)
    p.line([(32, 54), (36, 54)], w=0.0)
    p.rect(30, 56, 38, 66, w=0.7)
    p.rect(62, 56, 70, 66, w=0.7)
    p.line([(50, 20), (50, 12)], w=0.8)


def i_tent(p: Pen):
    p.line([(12, 82), (50, 22), (88, 82)], w=1.1)
    p.line([(12, 82), (88, 82)], w=1.0)
    p.line([(50, 22), (50, 82)], w=0.7)
    p.line([(38, 82), (50, 56), (62, 82)], w=0.9)


# ==================================================== future & preservation ==
def i_seedling(p: Pen):
    p.line([(50, 88), (50, 46)], w=1.1)
    p.arc(34, 46, 16, 0, 180, w=1.0)
    p.arc(66, 42, 16, 0, 180, w=1.0)
    p.line([(36, 88), (64, 88)], w=0.9)
    p.line([(50, 60), (36, 52)], w=0.0)


def i_book(p: Pen):
    p.line([(50, 30), (50, 84)], w=1.0)
    p.line([(50, 30), (16, 38), (16, 80), (50, 84)], w=1.0)
    p.line([(50, 30), (84, 38), (84, 80), (50, 84)], w=1.0)
    for k in range(3):
        y = 48 + k * 11
        p.line([(24, y), (43, y + 1.5)], w=0.55)
        p.line([(57, y + 1.5), (76, y)], w=0.55)


def i_signal(p: Pen):
    p.dot(50, 76, 5.0)
    for k, r in enumerate((18, 30, 42)):
        p.arc(50, 76, r, 210, 330, w=1.0 - k * 0.15)


def i_archive(p: Pen):
    p.rect(18, 30, 82, 46, w=1.0)
    p.rect(24, 46, 76, 84, w=1.0)
    p.line([(40, 58), (60, 58)], w=1.0)
    p.line([(24, 66), (76, 66)], w=0.6)
    p.line([(24, 74), (76, 74)], w=0.6)


def i_youth(p: Pen):
    p.circle(34, 32, 11)
    p.circle(66, 38, 8, w=0.85)
    p.line([(34, 43), (34, 66)], w=1.0)
    p.line([(20, 54), (48, 54)], w=1.0)
    p.line([(34, 66), (24, 86)], w=1.0)
    p.line([(34, 66), (46, 86)], w=1.0)
    p.line([(66, 46), (66, 64)], w=0.85)
    p.line([(66, 64), (58, 84)], w=0.85)
    p.line([(66, 64), (76, 84)], w=0.85)


def i_globe(p: Pen):
    p.circle(50, 52, 32)
    p.line([(18, 52), (82, 52)], w=0.7)
    p.arc(50, 52, 32, 0, 360, w=0.0)
    for rx in (11, 22):
        p.d.arc([(50 - rx) * SS, 20 * SS, (50 + rx) * SS, 84 * SS], 0, 360,
                fill=p.col, width=max(1, int(round(p.lw * 0.6 * SS))))


# ================================================================ challenges ==
def i_empty_house(p: Pen):
    p.line([(14, 50), (50, 20), (86, 50)], w=1.1)
    p.line([(24, 46), (24, 84), (76, 84), (76, 46)], w=1.0)
    p.line([(34, 62), (48, 76)], w=0.8)
    p.line([(48, 62), (34, 76)], w=0.8)
    p.line([(56, 62), (68, 76)], w=0.8)
    p.line([(68, 62), (56, 76)], w=0.8)
    p.line([(30, 34), (44, 44)], w=0.6)


def i_decline(p: Pen):
    p.line([(16, 24), (16, 84), (86, 84)], w=1.0)
    p.line([(26, 36), (44, 52), (58, 44), (78, 72)], w=1.1)
    p.line([(78, 72), (78, 58)], w=0.9)
    p.line([(78, 72), (64, 72)], w=0.9)


def i_thermometer(p: Pen):
    p.line([(50, 20), (50, 62)], w=1.1)
    p.circle(50, 72, 11, w=1.1)
    p.arc(50, 20, 7, 180, 360, w=1.1)
    p.dot(50, 72, 4.5)
    for k in range(4):
        y = 30 + k * 8
        p.line([(58, y), (68, y)], w=0.6)


def i_clock(p: Pen):
    p.circle(50, 54, 32)
    p.line([(50, 54), (50, 32)], w=1.0)
    p.line([(50, 54), (66, 62)], w=1.0)
    for k in range(12):
        a = math.pi * 2 * k / 12
        p.dot(50 + math.cos(a) * 26, 54 + math.sin(a) * 26, 1.6)


def i_language(p: Pen):
    """Garhwali and Kumaoni — two mother tongues under pressure."""
    p.rect(10, 20, 60, 58, w=1.0, r=5)
    p.line([(22, 58), (22, 72), (36, 58)], w=1.0)
    p.line([(20, 32), (50, 32)], w=0.75)         # the shirorekha of Devanagari
    p.line([(26, 32), (26, 46)], w=0.75)
    p.line([(36, 32), (36, 46)], w=0.75)
    p.line([(26, 40), (36, 40)], w=0.6)
    p.line([(44, 32), (44, 46)], w=0.75)
    p.rect(44, 44, 92, 82, w=0.85, r=5)
    p.line([(80, 82), (80, 94), (68, 82)], w=0.85)
    p.line([(54, 56), (82, 56)], w=0.65)
    p.line([(54, 66), (74, 66)], w=0.65)


# ================================================================== registry ==
REGISTRY = {k[2:]: v for k, v in list(globals().items()) if k.startswith("i_")}


def render(name: str, px: int = 300, color: str = C.GOLD, lw: float = 3.0,
           alpha: float = 1.0) -> Image.Image:
    """Render one icon to a transparent PNG of `px` square."""
    if name not in REGISTRY:
        raise KeyError(f"unknown icon {name!r}; have {sorted(REGISTRY)}")
    img = Image.new("RGBA", (int(G * SS), int(G * SS)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pen = Pen(d, rgb(color) + (int(255 * alpha),), lw)
    REGISTRY[name](pen)
    return img.resize((px, px), Image.LANCZOS)


def emit_all(px: int = 300, color: str = C.GOLD, lw: float = 3.0,
             suffix: str = "") -> dict[str, str]:
    """Write every icon to assets/icons and return name -> path."""
    out = {}
    for name in REGISTRY:
        path = os.path.join(ICON_DIR, f"{name}{suffix}.png")
        render(name, px=px, color=color, lw=lw).save(path, optimize=True)
        out[name] = path
    return out
