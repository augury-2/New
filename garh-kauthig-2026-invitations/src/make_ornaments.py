"""
Ornament library generator for the Garh Kauthig 2026 invitation suite.

Emits assets/ornaments.svg -- a <defs> sheet of <symbol> and <pattern> nodes
that the page template inlines once and references with <use>.  Geometric
ornament (mandalas, scallop rings, aipan lattices, weaves, mountain ranges) is
computed in polar/parametric maths so it is exact and truly symmetrical;
pictorial ornament (dhol-damau, hudka, ransingha, temple bell, hill house,
dancers, jewellery) is hand-authored path data.

No institutional emblem is drawn here.  The two university marks belong to the
institutions and are set as type lockups (or dropped in as supplied artwork) by
src/build.mjs instead.

Everything is stroked/filled with `currentColor` so a single CSS colour drives
the whole sheet -- which is how the antique-gold line art stays consistent.

Run:  python3 src/make_ornaments.py
"""

import math
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

F = 3  # coordinate rounding


def n(v):
    return f"{round(v, F):g}"


def pol(r, deg):
    """Polar -> cartesian, 0deg = +x, angles increase clockwise on screen."""
    a = math.radians(deg)
    return r * math.cos(a), r * math.sin(a)


def arc(r, a0, a1, sweep=1):
    x0, y0 = pol(r, a0)
    x1, y1 = pol(r, a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    return f"M{n(x0)},{n(y0)} A{n(r)},{n(r)} 0 {large} {sweep} {n(x1)},{n(y1)}"


def petal(r0, r1, amid, half, bulge=1.0):
    """Pointed-oval petal from radius r0 to r1, centred on angle amid."""
    ax, ay = pol(r0, amid)
    bx, by = pol(r1, amid)
    rm = (r0 + r1) / 2
    c1x, c1y = pol(rm * bulge, amid - half)
    c2x, c2y = pol(rm * bulge, amid + half)
    return (f"M{n(ax)},{n(ay)} Q{n(c1x)},{n(c1y)} {n(bx)},{n(by)} "
            f"Q{n(c2x)},{n(c2y)} {n(ax)},{n(ay)} Z")


def dots(r, a0, a1, step, rd):
    out = []
    a = a0
    while a <= a1 + 1e-6:
        x, y = pol(r, a)
        out.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(rd)}"/>')
        a += step
    return "".join(out)


def tri_ring(r, a0, a1, step, h, w):
    """Aipan-style triangles pointing outward along an arc."""
    out = []
    a = a0
    while a <= a1 + 1e-6:
        tx, ty = pol(r + h, a)
        lx, ly = pol(r, a - w)
        rx, ry = pol(r, a + w)
        out.append(f'<path d="M{n(lx)},{n(ly)} L{n(tx)},{n(ty)} L{n(rx)},{n(ry)} Z"/>')
        a += step
    return "".join(out)


# ===========================================================================
#  Corner mandala -- a quarter mandala anchored at the corner (aipan derived)
# ===========================================================================
def scallops(r, a0, a1, count, out=True):
    """Semicircular scallops riding an arc -- a temple-cornice edge."""
    seg = (a1 - a0) / count
    chord = 2 * r * math.sin(math.radians(seg) / 2)
    rr = chord / 2
    parts = []
    for i in range(count):
        s0, e0 = a0 + i * seg, a0 + (i + 1) * seg
        x0, y0 = pol(r, s0)
        x1, y1 = pol(r, e0)
        parts.append(f'M{n(x0)},{n(y0)} A{n(rr)},{n(rr)} 0 0 {1 if out else 0} {n(x1)},{n(y1)}')
    return '<path d="' + " ".join(parts) + '"/>'


def corner_mandala():
    """Quarter mandala anchored in the corner: compact aipan rosette, scalloped
    cornice, then a vine that runs out along both frame rules.  Radii are kept
    tight so there is no dead zone between the rosette and the vine."""
    g = []
    a0, a1 = 0.0, 90.0
    # rosette in the corner itself
    for i in range(4):
        amid = a0 + (a1 - a0) * (i + 0.5) / 4
        g.append(f'<path d="{petal(9, 30, amid, 10, 1.06)}" fill="currentColor" fill-opacity=".16"/>')
        g.append(f'<path d="{petal(9, 30, amid, 10, 1.06)}"/>')
    g.append(f'<path d="{arc(6, a0, a1)}" stroke-width="1.3"/>')
    g.append(f'<path d="{arc(35, a0, a1)}"/>')
    g.append(f'<path d="{arc(38.5, a0, a1)}" stroke-width="0.9"/>')
    # scalloped cornice
    g.append(scallops(40, a0, a1, 6))
    g.append(f'<path d="{arc(54, a0, a1)}" stroke-width="1.1"/>')
    g.append(f'<g fill="currentColor" stroke="none">{dots(60, 7.5, 82.5, 12.5, 1.7)}</g>')
    g.append(f'<path d="{arc(66, a0, a1)}" stroke-width="0.85"/>')
    # aipan triangles facing outward
    g.append(f'<g fill="currentColor" fill-opacity=".5">{tri_ring(68, 6, 84, 13, 6, 3.4)}</g>')
    # vine: doubled stem sweeping corner-to-corner, leaves alternating outward
    g.append('<path d="M0,126 C 34,125 62,112 82,92 C 102,72 114,44 116,18 '
             'C 117,10 118,4 118,0" stroke-width="1.4"/>')
    g.append('<path d="M0,118 C 32,117 58,105 76,86 C 94,67 106,42 108,18 '
             'C 109,10 110,4 110,0" stroke-width="0.85" stroke-opacity=".7"/>')
    for i, amid in enumerate((9, 22.5, 36, 49.5, 63, 76.5)):
        rr = 112 if i % 2 == 0 else 110
        g.append(f'<path d="{petal(rr, rr + 20, amid, 5.0, 1.02)}" stroke-width="1.15"/>')
        px, py = pol(rr - 7, amid)
        g.append(f'<circle cx="{n(px)}" cy="{n(py)}" r="1.4" fill="currentColor" stroke="none"/>')
    # buds where the vine runs into the frame rules
    for x, y, rot in ((0, 126, 0), (118, 0, 90)):
        g.append(f'<g transform="translate({x},{y}) rotate({rot})">'
                 f'<path d="M0,0 L-13,0" stroke-width="1.1"/>'
                 f'<circle cx="-17" cy="0" r="2.3" fill="currentColor" stroke="none"/></g>')
    body = "".join(g)
    return (f'<symbol id="orn-corner" viewBox="0 0 134 134">'
            f'<g fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</g></symbol>')


# ===========================================================================
#  Lotus / kalash divider  (horizontal, symmetrical)
# ===========================================================================
def lotus_divider():
    g = []
    # central lotus: petals fanning upward, drawn about origin then translated
    petals = []
    for i in range(7):
        amid = 180 + 22.5 * i        # 180deg = pointing left, sweeping over the top
        petals.append(f'<path d="{petal(4, 26, amid, 12, 1.1)}"/>')
    inner = []
    for i in range(5):
        amid = 191 + 24.5 * i
        inner.append(f'<path d="{petal(3, 15, amid, 11, 1.12)}" fill="currentColor" fill-opacity=".22"/>')
    g.append(f'<g transform="translate(300,30)">{"".join(petals)}{"".join(inner)}'
             f'<path d="M-15,2 Q0,12 15,2" stroke-width="1.6"/>'
             f'<circle cx="0" cy="0" r="2.6" fill="currentColor" stroke="none"/></g>')
    # tapering rules + beads on both sides
    for s in (-1, 1):
        x0 = 300 + s * 34
        g.append(f'<path d="M{n(x0)},30 L{n(300 + s * 150)},30" stroke-width="1.6"/>')
        g.append(f'<path d="M{n(300 + s * 44)},24 Q{n(300 + s * 86)},30 {n(300 + s * 44)},36" stroke-width="1.2"/>')
        g.append(f'<circle cx="{n(300 + s * 158)}" cy="30" r="3.2" fill="currentColor" stroke="none"/>')
        g.append(f'<path d="M{n(300 + s * 166)},30 L{n(300 + s * 214)},30" stroke-width="1.1"/>')
        g.append(f'<path d="M{n(300 + s * 222)},24 L{n(300 + s * 232)},30 L{n(300 + s * 222)},36" stroke-width="1.2"/>')
        g.append(f'<path d="M{n(300 + s * 238)},30 L{n(300 + s * 296)},30" stroke-width="0.9"/>')
    body = "".join(g)
    return (f'<symbol id="orn-divider" viewBox="0 0 600 60">'
            f'<g fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</g></symbol>')


def small_flourish():
    g = ['<path d="M60,20 L20,20 Q8,20 8,13 Q8,6 16,8 Q24,10 24,20 Q24,30 12,32"/>',
         '<path d="M60,20 L100,20 Q112,20 112,13 Q112,6 104,8 Q96,10 96,20 Q96,30 108,32"/>',
         '<path d="M52,20 L68,20"/>',
         '<circle cx="60" cy="20" r="3.4" fill="currentColor" stroke="none"/>',
         f'<path d="{petal(6, 18, 270, 13, 1.1)}" transform="translate(60,20)"/>']
    return (f'<symbol id="orn-flourish" viewBox="0 0 120 40">'
            f'<g fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round">{"".join(g)}</g></symbol>')


def rosette():
    g = []
    for i in range(12):
        g.append(f'<path d="{petal(8, 30, i * 30, 13, 1.08)}"/>')
    for i in range(12):
        g.append(f'<path d="{petal(5, 17, i * 30 + 15, 12, 1.1)}" fill="currentColor" fill-opacity=".2"/>')
    g.append('<circle cx="0" cy="0" r="4" fill="currentColor" stroke="none"/>')
    g.append(f'<path d="{arc(34, 0, 180)}"/><path d="{arc(34, 180, 360)}"/>')
    return (f'<symbol id="orn-rosette" viewBox="0 0 76 76">'
            f'<g transform="translate(38,38)" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" '
            f'stroke-linejoin="round">{"".join(g)}</g></symbol>')


# ===========================================================================
#  Patterns: aipan lattice, ringaal weave, temple-carving band
# ===========================================================================
def pattern_aipan():
    """Delicate aipan lattice -- fine diamond grid, four-petal flowers, dots."""
    u = 64
    g = []
    g.append(f'<path d="M{u/2},0 L{u},{u/2} L{u/2},{u} L0,{u/2} Z" stroke-width="0.85"/>')
    for i in range(4):
        g.append(f'<path d="{petal(3.5, 13, i * 90 + 45, 17, 1.12)}" '
                 f'transform="translate({u/2},{u/2})" stroke-width="0.8"/>')
    g.append(f'<circle cx="{u/2}" cy="{u/2}" r="1.7" fill="currentColor" stroke="none"/>')
    for cx, cy in ((0, 0), (u, 0), (0, u), (u, u)):
        for i in range(4):
            g.append(f'<path d="{petal(2.5, 9, i * 90 + 45, 18, 1.1)}" '
                     f'transform="translate({cx},{cy})" stroke-width="0.7"/>')
    for x, y in ((u/2, 9), (u/2, u - 9), (9, u/2), (u - 9, u/2)):
        g.append(f'<circle cx="{x}" cy="{y}" r="1.25" fill="currentColor" stroke="none"/>')
    return (f'<pattern id="pat-aipan" width="{u}" height="{u}" patternUnits="userSpaceOnUse">'
            f'<g fill="none" stroke="currentColor" stroke-linejoin="round">'
            f'{"".join(g)}</g></pattern>')


def pattern_ringaal():
    """Ringaal (hill bamboo) plait: strips genuinely pass over and under."""
    u = 32
    a0, a1 = 3, 13     # first strip band
    b0, b1 = 19, 29    # second strip band
    seg = []

    def hline(y, gaps):
        """Horizontal edge across the tile, broken over the given x ranges."""
        xs = [0.0]
        for g0, g1 in gaps:
            xs += [g0, g1]
        xs += [float(u)]
        out = []
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > 0.2:
                out.append(f'M{n(xs[i])},{n(y)} L{n(xs[i + 1])},{n(y)}')
        return out

    def vline(x, gaps):
        ys = [0.0]
        for g0, g1 in gaps:
            ys += [g0, g1]
        ys += [float(u)]
        out = []
        for i in range(0, len(ys) - 1, 2):
            if ys[i + 1] - ys[i] > 0.2:
                out.append(f'M{n(x)},{n(ys[i])} L{n(x)},{n(ys[i + 1])}')
        return out

    # horizontal strip A rides OVER vertical A, UNDER vertical B
    seg += hline(a0, [(b0, b1)]) + hline(a1, [(b0, b1)])
    # horizontal strip B rides UNDER vertical A, OVER vertical B
    seg += hline(b0, [(a0, a1)]) + hline(b1, [(a0, a1)])
    # vertical strip A rides UNDER horizontal A, OVER horizontal B
    seg += vline(a0, [(a0, a1)]) + vline(a1, [(a0, a1)])
    # vertical strip B rides OVER horizontal A, UNDER horizontal B
    seg += vline(b0, [(b0, b1)]) + vline(b1, [(b0, b1)])
    d = " ".join(seg)
    return (f'<pattern id="pat-ringaal" width="{u}" height="{u}" patternUnits="userSpaceOnUse"'
            f' patternTransform="scale(0.709)">'
            f'<g fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round">'
            f'<path d="{d}"/></g></pattern>')


def pattern_carving():
    """Repeating temple / wooden-door carving band (unit 72 x 28)."""
    g = [
        '<path d="M0,26 L72,26" stroke-width="1.1"/>',
        '<path d="M0,3 L72,3" stroke-width="1.1"/>',
        # trefoil arch
        '<path d="M8,26 L8,15 Q8,6 18,6 Q28,6 28,15 L28,26"/>',
        '<path d="M13,26 L13,16 Q13,11 18,11 Q23,11 23,16 L23,26" stroke-width="0.9"/>',
        # lotus bud between arches
        '<path d="M36,26 L36,20 Q30,17 33,11 Q36,6 36,4 Q36,6 39,11 Q42,17 36,20" stroke-width="1"/>',
        '<path d="M44,26 L44,15 Q44,6 54,6 Q64,6 64,15 L64,26"/>',
        '<path d="M49,26 L49,16 Q49,11 54,11 Q59,11 59,16 L59,26" stroke-width="0.9"/>',
        '<circle cx="18" cy="15" r="1.6" fill="currentColor" stroke="none"/>',
        '<circle cx="54" cy="15" r="1.6" fill="currentColor" stroke="none"/>',
        '<circle cx="72" cy="14.5" r="1.4" fill="currentColor" stroke="none"/>',
        '<circle cx="0" cy="14.5" r="1.4" fill="currentColor" stroke="none"/>',
    ]
    # scaled so that 28 user units land on exactly 6 mm (22.68 CSS px)
    return (f'<pattern id="pat-carving" width="72" height="28" patternUnits="userSpaceOnUse"'
            f' patternTransform="scale(0.81)">'
            f'<g fill="none" stroke="currentColor" stroke-width="1.2" '
            f'stroke-linecap="round" stroke-linejoin="round">{"".join(g)}</g></pattern>')


def pattern_textile():
    """Folk textile band -- chevrons and stripes as on a Garhwali pankhi."""
    u = 24
    g = ['<path d="M0,16 L6,8 L12,16 L18,8 L24,16" stroke-width="1.2"/>',
         '<path d="M0,22 L24,22" stroke-width="1"/>',
         '<path d="M0,2 L24,2" stroke-width="1"/>',
         '<circle cx="6" cy="19" r="1.1" fill="currentColor" stroke="none"/>',
         '<circle cx="18" cy="19" r="1.1" fill="currentColor" stroke="none"/>']
    return (f'<pattern id="pat-textile" width="{u}" height="{u}" patternUnits="userSpaceOnUse">'
            f'<g fill="none" stroke="currentColor">{"".join(g)}</g></pattern>')


# ===========================================================================
#  Himalayan ranges  (procedural, fixed seed -> stable output)
# ===========================================================================
def ridge(width, base, peaks, seed, jitter=0.5):
    """Return a closed silhouette path across `width` from a list of
    (x_fraction, height) peak anchors, with fractal sub-detail."""
    rnd = random.Random(seed)
    pts = [(0.0, base)]
    prev_x, prev_y = 0.0, base
    for fx, h in peaks:
        px, py = fx * width, base - h
        # rising flank with a couple of shoulders
        steps = 3
        for s in range(1, steps):
            t = s / steps
            x = prev_x + (px - prev_x) * t
            y = prev_y + (py - prev_y) * t
            y += rnd.uniform(-1, 1) * h * 0.10 * jitter
            pts.append((x, y))
        pts.append((px, py))
        prev_x, prev_y = px, py
    pts.append((width, base))
    d = "M" + " L".join(f"{n(x)},{n(y)}" for x, y in pts) + " Z"
    return d, pts


def mountains():
    W, H = 1200, 420
    out = []
    layers = [
        # (opacity-class, base, peaks, seed)
        ("far", 330, [(0.10, 150), (0.22, 205), (0.34, 168), (0.46, 250),
                      (0.58, 196), (0.70, 262), (0.82, 190), (0.94, 226)], 7),
        ("mid", 372, [(0.14, 150), (0.28, 214), (0.41, 172), (0.55, 232),
                      (0.68, 178), (0.80, 210), (0.92, 158)], 21),
        ("near", 410, [(0.08, 96), (0.24, 138), (0.38, 104), (0.52, 150),
                       (0.66, 112), (0.80, 142), (0.95, 100)], 33),
    ]
    for cls, base, peaks, seed in layers:
        d, pts = ridge(W, base, peaks, seed)
        out.append(f'<path class="mtn-{cls}" d="{d}"/>')
        # snow caps on the taller summits of the far/mid ranges
        if cls != "near":
            rnd = random.Random(seed + 500)
            for fx, h in peaks:
                if h < 190:
                    continue
                px, py = fx * W, base - h
                sw = h * 0.30
                zig = []
                k = 5
                for i in range(k + 1):
                    t = i / k
                    zig.append((px - sw + 2 * sw * t,
                                py + h * 0.30 + rnd.uniform(-1, 1) * h * 0.045))
                dd = (f"M{n(px)},{n(py)} L{n(px + sw)},{n(py + h * 0.34)} "
                      + " L".join(f"{n(x)},{n(y)}" for x, y in reversed(zig))
                      + f" L{n(px - sw)},{n(py + h * 0.34)} Z")
                out.append(f'<path class="mtn-snow" d="{dd}"/>')
    return (f'<symbol id="orn-mountains" viewBox="0 0 {W} {H}" '
            f'preserveAspectRatio="none">{"".join(out)}</symbol>')


def peak_line():
    """Sharp outlined Himalayan range for the footer rule."""
    W, H = 600, 96
    base = 88
    peaks = [(0.06, 34), (0.15, 58), (0.25, 40), (0.36, 78), (0.47, 52),
             (0.58, 86), (0.68, 46), (0.78, 66), (0.88, 38), (0.96, 52)]
    d, _ = ridge(W, base, peaks, 91, jitter=0.25)
    snow = []
    for fx, h in peaks:
        if h < 70:
            continue
        px, py = fx * W, base - h
        sw = h * 0.26
        snow.append(f'<path d="M{n(px - sw)},{n(py + h * 0.30)} L{n(px - sw * 0.45)},'
                    f'{n(py + h * 0.16)} L{n(px)},{n(py + h * 0.28)} '
                    f'L{n(px + sw * 0.5)},{n(py + h * 0.14)} L{n(px + sw)},{n(py + h * 0.30)}" '
                    f'stroke-width="1"/>')
    return (f'<symbol id="orn-peakline" viewBox="0 0 {W} {H}">'
            f'<g fill="none" stroke="currentColor" stroke-width="1.4" '
            f'stroke-linejoin="round"><path d="{d}"/>{"".join(snow)}</g></symbol>')


def pines():
    """Three deodar/pine conifers, line-drawn, trunks stopping at the apex."""
    def tree(cx, base, h, w, layers, sw):
        p = []
        apex = base - h
        p.append(f'<path d="M{n(cx)},{n(base)} L{n(cx)},{n(apex + h * 0.10)}" stroke-width="{sw}"/>')
        p.append(f'<path d="M{n(cx - w * 0.10)},{n(apex + h * 0.16)} L{n(cx)},{n(apex)} '
                 f'L{n(cx + w * 0.10)},{n(apex + h * 0.16)}" stroke-width="{sw}"/>')
        for i in range(layers):
            t = i / (layers - 1)
            y = base - h * (0.14 + 0.72 * t)
            hw = w * 0.5 * (1 - t) + w * 0.05
            drop = h * 0.075
            p.append(f'<path d="M{n(cx - hw)},{n(y + drop)} Q{n(cx)},{n(y - drop * 0.7)} '
                     f'{n(cx + hw)},{n(y + drop)}" stroke-width="{sw}"/>')
        p.append(f'<path d="M{n(cx - w * 0.12)},{n(base)} L{n(cx + w * 0.12)},{n(base)}" stroke-width="{sw}"/>')
        return "".join(p)
    g = (tree(56, 150, 134, 58, 6, 1.5) + tree(112, 150, 96, 42, 5, 1.3)
         + tree(18, 150, 80, 34, 4, 1.2)
         + '<path d="M2,150 L138,150" stroke-width="1.1" stroke-opacity=".7"/>')
    return (f'<symbol id="orn-pines" viewBox="0 0 140 158">'
            f'<g fill="none" stroke="currentColor" stroke-linecap="round" '
            f'stroke-linejoin="round">{g}</g></symbol>')


def prayer_flags():
    """Bunting on a slack line, flags hanging square off the string."""
    W = 244
    x0, x1 = 10, 234
    sag = 30

    def line_y(t):
        return 10 + sag * math.sin(math.pi * t) ** 0.85

    pts = [(x0 + (x1 - x0) * (i / 24), line_y(i / 24)) for i in range(25)]
    d = "M" + " L".join(f"{n(x)},{n(y)}" for x, y in pts)
    g = [f'<path d="{d}" stroke-width="1.4"/>']
    for s, x in ((1, x0), (-1, x1)):
        g.append(f'<path d="M{n(x)},{n(line_y(0) )} L{n(x)},{n(line_y(0) + 52)}" stroke-width="1.5"/>')
        g.append(f'<circle cx="{n(x)}" cy="{n(line_y(0) - 5)}" r="3" fill="currentColor" stroke="none"/>')
    fw, fh = 17, 26
    for i in range(9):
        t = (i + 0.5) / 9
        cx = x0 + (x1 - x0) * t
        cy = line_y(t)
        g.append(f'<path d="M{n(cx - fw / 2)},{n(cy)} L{n(cx + fw / 2)},{n(cy)} '
                 f'L{n(cx + fw / 2)},{n(cy + fh)} Q{n(cx)},{n(cy + fh + 5)} '
                 f'{n(cx - fw / 2)},{n(cy + fh)} Z" stroke-width="1.2"/>')
        if i % 2 == 0:
            g.append(f'<path d="M{n(cx - 5)},{n(cy + 9)} L{n(cx + 5)},{n(cy + 9)} '
                     f'M{n(cx - 5)},{n(cy + 16)} L{n(cx + 5)},{n(cy + 16)}" stroke-width="0.8"/>')
    return (f'<symbol id="orn-flags" viewBox="0 0 {W} 96">'
            f'<g fill="none" stroke="currentColor" stroke-linecap="round" '
            f'stroke-linejoin="round">{"".join(g)}</g></symbol>')


# ===========================================================================
#  Hand-authored pictograms
# ===========================================================================
PICTO = {
    # ---- Dhol (barrel drum) + Damau (kettle drum), the Garhwali drum pair ----
    "dhol": ("0 0 220 150", 2.1, """
      <path d="M52,40 C86,31 134,31 168,40 C176,58 176,92 168,110 C134,119 86,119 52,110
               C44,92 44,58 52,40 Z"/>
      <ellipse cx="52" cy="75" rx="11" ry="35"/>
      <ellipse cx="168" cy="75" rx="11" ry="35"/>
      <path d="M63,45 L86,75 L63,105 M86,43 L109,75 L86,107 M109,42 L132,75 L109,108
               M132,43 L155,75 L132,107" stroke-width="1.2"/>
      <path d="M63,45 L63,105 M86,43 L86,107 M109,42 L109,108 M132,43 L132,107
               M155,45 L155,105" stroke-width="0.7" stroke-opacity=".55"/>
      <path d="M66,36 C84,10 138,10 156,36" stroke-width="1.5"/>
      <path d="M176,112 L212,132" stroke-width="2.4"/>
      <path d="M44,112 C34,124 26,132 18,136" stroke-width="2.4"/>
      <circle cx="212" cy="132" r="3" fill="currentColor" stroke="none"/>
    """),
    "damau": ("0 0 180 130", 2.1, """
      <path d="M26,86 A64,52 0 0 1 154,86"/>
      <ellipse cx="90" cy="86" rx="64" ry="13"/>
      <path d="M26,86 C26,100 54,110 90,110 C126,110 154,100 154,86" stroke-width="1.3"/>
      <path d="M40,74 L140,74" stroke-width="0.9" stroke-opacity=".5"/>
      <path d="M52,58 Q90,50 128,58" stroke-width="1.1"/>
      <path d="M64,20 C74,34 78,44 78,58 M116,20 C106,34 102,44 102,58" stroke-width="2.3"/>
      <circle cx="64" cy="18" r="3.4" fill="currentColor" stroke="none"/>
      <circle cx="116" cy="18" r="3.4" fill="currentColor" stroke="none"/>
    """),
    # ---- Hudka (hourglass / waisted hand drum) ----
    "hudka": ("0 0 120 170", 2.1, """
      <ellipse cx="60" cy="26" rx="30" ry="10"/>
      <ellipse cx="60" cy="144" rx="30" ry="10"/>
      <path d="M30,26 C30,58 44,70 44,85 C44,100 30,112 30,144"/>
      <path d="M90,26 C90,58 76,70 76,85 C76,100 90,112 90,144"/>
      <path d="M36,36 L84,58 M84,36 L36,58 M40,112 L80,134 M80,112 L40,134" stroke-width="1"/>
      <path d="M44,74 L76,74 M44,96 L76,96" stroke-width="1"/>
      <path d="M30,40 C10,52 6,90 22,118" stroke-width="1.4"/>
    """),
    # ---- Ransingha (curved copper horn) ----
    "ransingha": ("0 0 220 140", 2.1, """
      <path d="M22,104 C40,104 52,96 58,84 C66,66 62,44 74,30 C88,14 118,12 140,24
               C160,35 168,52 176,66"/>
      <path d="M30,112 C50,112 64,102 70,88 C78,68 74,48 84,36 C96,24 116,22 132,32
               C150,43 158,60 166,74"/>
      <path d="M176,66 L206,44 L212,54 L184,76 Z"/>
      <path d="M166,74 L184,76" stroke-width="1.2"/>
      <ellipse cx="209" cy="49" rx="4" ry="8" transform="rotate(-38 209 49)"/>
      <path d="M14,100 L14,116 C14,120 18,122 22,120 L30,116 L22,104 Z"/>
      <path d="M88,28 L94,38 M104,22 L108,33 M122,24 L124,35" stroke-width="1.1"/>
    """),
    # ---- Temple bell ----
    "bell": ("0 0 120 170", 2.1, """
      <path d="M34,112 C34,78 42,58 46,44 C48,36 52,32 60,32 C68,32 72,36 74,44
               C78,58 86,78 86,112"/>
      <path d="M26,112 L94,112 C98,112 100,116 100,119 C100,122 98,125 94,125
               L26,125 C22,125 20,122 20,119 C20,116 22,112 26,112 Z"/>
      <path d="M52,125 C52,136 54,142 60,146 C66,142 68,136 68,125" stroke-width="1.4"/>
      <circle cx="60" cy="150" r="6"/>
      <path d="M60,32 L60,22" stroke-width="1.6"/>
      <circle cx="60" cy="16" r="7"/>
      <path d="M60,9 L60,2" stroke-width="1.4"/>
      <path d="M40,96 L80,96" stroke-width="1" stroke-opacity=".6"/>
      <path d="M44,76 L76,76" stroke-width="0.9" stroke-opacity=".5"/>
    """),
    # ---- Traditional Garhwali hill house: slate roof, carved wooden balcony ----
    "house": ("0 0 220 160", 1.9, """
      <path d="M14,66 L110,20 L206,66 Z"/>
      <path d="M28,66 L110,27 L192,66" stroke-width="1"/>
      <path d="M46,44 L60,52 M74,36 L88,44 M132,44 L146,36 M160,52 L174,44" stroke-width="0.8"/>
      <path d="M26,66 L26,140 L194,140 L194,66"/>
      <path d="M26,92 L194,92" stroke-width="1.2"/>
      <path d="M26,116 L194,116" stroke-width="1.2"/>
      <path d="M40,92 L40,116 M62,92 L62,116 M84,92 L84,116 M106,92 L106,116
               M128,92 L128,116 M150,92 L150,116 M172,92 L172,116" stroke-width="0.9"/>
      <path d="M52,74 L52,86 M68,74 L68,86 M84,74 L84,86" stroke-width="0.9"/>
      <path d="M44,70 L92,70 L92,88 L44,88 Z" stroke-width="1.1"/>
      <path d="M128,70 L176,70 L176,88 L128,88 Z" stroke-width="1.1"/>
      <path d="M140,74 L140,86 M152,74 L152,86 M164,74 L164,86" stroke-width="0.9"/>
      <path d="M96,140 L96,120 L124,120 L124,140" stroke-width="1.3"/>
      <path d="M110,120 L110,140" stroke-width="0.9"/>
      <path d="M96,120 Q110,108 124,120" stroke-width="1.1"/>
      <path d="M14,140 L206,140" stroke-width="1.6"/>
      <path d="M110,20 L110,8" stroke-width="1.4"/>
      <circle cx="110" cy="5" r="3.4" fill="currentColor" stroke="none"/>
    """),
    # ---- Traditional jewellery: nath + galobandh necklace ----
    "jewellery": ("0 0 180 140", 1.9, """
      <path d="M34,34 C34,18 62,10 90,10 C118,10 146,18 146,34" stroke-width="1.3"/>
      <path d="M28,40 C40,86 62,112 90,112 C118,112 140,86 152,40"/>
      <path d="M36,52 C48,88 66,104 90,104 C114,104 132,88 144,52" stroke-width="1.2"/>
      <circle cx="90" cy="112" r="7"/>
      <path d="M90,119 L90,128" stroke-width="1.2"/>
      <circle cx="90" cy="132" r="4.5"/>
      <g stroke-width="1.1">
        <circle cx="54" cy="72" r="4"/><circle cx="72" cy="90" r="4"/>
        <circle cx="108" cy="90" r="4"/><circle cx="126" cy="72" r="4"/>
      </g>
      <path d="M20,26 A20,20 0 1 1 20,66" stroke-width="1.5"/>
      <circle cx="16" cy="70" r="3.2" fill="currentColor" stroke="none"/>
      <path d="M160,26 A20,20 0 1 0 160,66" stroke-width="1.5"/>
      <circle cx="164" cy="70" r="3.2" fill="currentColor" stroke="none"/>
    """),
    # ---- Kalash (auspicious pot) ----
    "kalash": ("0 0 110 150", 2.0, """
      <path d="M22,72 C22,52 34,44 55,44 C76,44 88,52 88,72 C88,100 74,124 55,124
               C36,124 22,100 22,72 Z"/>
      <path d="M34,44 L34,34 L76,34 L76,44" stroke-width="1.4"/>
      <path d="M28,34 L82,34" stroke-width="1.6"/>
      <path d="M55,34 L55,22" stroke-width="1.2"/>
      <path d="M55,22 C42,20 34,12 34,4 C44,8 50,14 55,22 C60,14 66,8 76,4 C76,12 68,20 55,22 Z"/>
      <path d="M28,90 Q55,102 82,90" stroke-width="1.1"/>
      <path d="M24,124 L86,124 C90,124 92,128 90,132 L20,132 C18,128 20,124 24,124 Z"/>
      <circle cx="55" cy="72" r="7" stroke-width="1.2"/>
    """),
}


def dancers():
    """A jhora-style chain of three dancers with joined hands -- filled gold
    silhouettes, which stay legible at small print sizes where outline figures
    turn to mush."""
    STEP = 104

    def figure(idx, flip, outer_arm, inner_arm, veil):
        s = -1 if flip else 1
        x = idx * STEP
        tx = x + (100 if flip else 0)
        g = [f'<g transform="translate({n(tx)},0) scale({s},1)">']
        # ghagra (flared skirt)
        g.append('<path d="M40,68 C29,96 20,124 12,152 C34,164 68,164 90,152 '
                 'C81,124 71,96 60,68 Z" fill="currentColor" stroke="none"/>')
        # hem bands knocked out of the silhouette
        g.append('<path d="M15,143 C37,153 67,153 87,143" fill="none" stroke="#ffffff" '
                 'stroke-opacity=".55" stroke-width="3.2"/>')
        g.append('<path d="M18,132 C39,142 65,142 84,132" fill="none" stroke="#ffffff" '
                 'stroke-opacity=".3" stroke-width="1.8"/>')
        # choli / torso
        g.append('<path d="M40,68 C37,56 37,45 41,37 L59,37 C63,45 63,56 60,68 Z" '
                 'fill="currentColor" stroke="none"/>')
        # head, bun, nose-ring hint
        g.append('<circle cx="50" cy="25" r="9.5" fill="currentColor" stroke="none"/>')
        g.append('<path d="M41,24 C41,11 59,11 59,24 C59,15 55,9 50,9 C45,9 41,15 41,24 Z" '
                 'fill="currentColor" stroke="none"/>')
        # odhni trailing behind the head
        g.append(f'<path d="{veil}" fill="none" stroke="currentColor" stroke-width="3" '
                 'stroke-linecap="round" stroke-opacity=".9"/>')
        for arm in (outer_arm, inner_arm):
            if arm:
                g.append(f'<path d="{arm}" fill="none" stroke="currentColor" '
                         'stroke-width="3.6" stroke-linecap="round"/>')
        g.append('</g>')
        return "".join(g)

    RAISED = "M58,42 C74,36 84,22 82,6"
    ACROSS = "M58,42 C72,44 86,47 98,49"
    DOWNIN = "M42,42 C30,45 20,47 8,49"
    VEIL_R = "M58,20 C76,26 88,44 90,70"
    VEIL_L = "M58,20 C74,28 84,46 86,72"

    figs = (figure(0, False, RAISED, ACROSS, VEIL_R)
            + figure(1, True, RAISED, ACROSS, VEIL_L)
            + figure(2, False, RAISED, DOWNIN, VEIL_R))
    # clasped hands between neighbours
    joins = ('<g fill="currentColor" stroke="none">'
             '<circle cx="105" cy="49" r="3.4"/><circle cx="209" cy="49" r="3.4"/></g>')
    return (f'<symbol id="orn-dancers" viewBox="0 0 324 172">'
            f'<g transform="translate(4,0)">{figs}{joins}</g></symbol>')


def picto_symbols():
    out = []
    for key, (vb, sw, body) in PICTO.items():
        out.append(f'<symbol id="orn-{key}" viewBox="{vb}">'
                   f'<g fill="none" stroke="currentColor" stroke-width="{sw}" '
                   f'stroke-linecap="round" stroke-linejoin="round">{body}</g></symbol>')
    return "".join(out)


# ===========================================================================
def build():
    parts = [
        corner_mandala(), lotus_divider(), small_flourish(), rosette(),
        pattern_aipan(), pattern_ringaal(), pattern_carving(), pattern_textile(),
        mountains(), peak_line(), pines(), prayer_flags(),
        picto_symbols(), dancers(),
    ]
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" '
           'xmlns:xlink="http://www.w3.org/1999/xlink" width="0" height="0" '
           'style="position:absolute" aria-hidden="true"><defs>'
           + "".join(parts) + "</defs></svg>")
    path = os.path.join(OUT, "ornaments.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("wrote", path, len(svg), "bytes")


if __name__ == "__main__":
    build()
