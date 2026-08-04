"""
KAUTHIK — Original animated dance background
============================================
Generates a seamless-looping silhouette dance loop (Jhora circle + Chholiya
sword dancers) over the deck's dusk Himalayan backdrop, then encodes it to
H.264 mp4 with ffmpeg.  Fully procedural — no stock footage.

    python3 dancevid.py            # -> assets/dance.mp4 + assets/dance_poster.jpg

All motion is periodic over the loop so frame N == frame 0 (seamless).
"""
from __future__ import annotations
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
import design as D
from design import rgb, rgba

FFMPEG = "/projects/ffmpeg/bin/ffmpeg"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1280, 720          # 16:9 video
FPS = 24
SECONDS = 6.0
N = int(FPS * SECONDS)    # frames in one seamless loop
GROUND_Y = int(H * 0.86)  # where the dancers stand

TAU = 2 * math.pi


# ----------------------------------------------------------------- backdrop --
def build_backdrop() -> Image.Image:
    """Dusk sky plate, darkened toward a warm stage floor."""
    base = Image.open(os.path.join(ASSETS, "base_dusk.jpg")).convert("RGB")
    # cover-crop to 16:9 of our size
    br = base.width / base.height
    tr = W / H
    if br > tr:
        nw = int(base.height * tr); x0 = (base.width - nw) // 2
        base = base.crop((x0, 0, x0 + nw, base.height))
    else:
        nh = int(base.width / tr); y0 = (base.height - nh) // 2
        base = base.crop((0, y0, base.width, y0 + nh))
    base = base.resize((W, H), Image.LANCZOS).convert("RGBA")

    # warm horizon glow behind the dancers
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gcx, gcy = int(W * 0.5), int(GROUND_Y - H * 0.16)
    for r, a in ((int(W * 0.55), 8), (int(W * 0.40), 14), (int(W * 0.26), 22)):
        gd.ellipse([gcx - r, gcy - int(r * 0.6), gcx + r, gcy + int(r * 0.6)],
                   fill=rgba(D.C.SAFFRON, a))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    base = Image.alpha_composite(base, glow)

    # dark ground / vignette
    vg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vg)
    for i in range(H - GROUND_Y + 60):
        y = GROUND_Y - 60 + i
        a = int(min(235, 40 + i * 2.6))
        vd.line([(0, y), (W, y)], fill=rgba(D.C.INK, a))
    # soft top & side darkening for cinema framing
    vd.rectangle([0, 0, W, int(H * 0.14)], fill=rgba(D.C.INK, 90))
    base = Image.alpha_composite(base, vg)
    return base.convert("RGB")


# ------------------------------------------------------------------ dancer ---
def _limb(dr, p0, p1, w, col):
    dr.line([p0, p1], fill=col, width=w)
    r = w // 2
    for (x, y) in (p0, p1):
        dr.ellipse([x - r, y - r, x + r, y + r], fill=col)


def draw_dancer(dr, cx, base_y, scale, phase, kind="jhora", lean_to=0.0):
    """Filled silhouette of a dancing figure, articulated by `phase` (0..1)."""
    col = rgb(D.C.INK)
    rim = rgba(D.C.SAFFRON, 70)
    s = scale
    lw = max(3, int(s * 0.11))
    t = phase * TAU

    # gentle full-body bob & sway
    bob = math.sin(t) * s * 0.05
    sway = math.sin(t + 0.4) * 0.16 + lean_to * 0.12
    hip = (cx, base_y - s * 0.92 + bob)
    sh_y = hip[1] - s * 0.52
    sh = (cx + math.sin(sway) * s * 0.10, sh_y)
    head_r = int(s * 0.15)
    head_c = (sh[0] + math.sin(sway) * s * 0.06, sh[1] - s * 0.30)

    # legs — alternating step
    step = math.sin(t)
    hipw = s * 0.16
    lk = 0.30 + 0.10 * max(0, step)
    rk = 0.30 + 0.10 * max(0, -step)
    lfoot = (cx - hipw - step * s * 0.18, base_y)
    rfoot = (cx + hipw + step * s * 0.18, base_y)
    lknee = ((hip[0] - hipw + lfoot[0]) / 2, base_y - s * lk)
    rknee = ((hip[0] + hipw + rfoot[0]) / 2, base_y - s * rk)

    # arms
    if kind == "chholiya":
        # one arm raises a sword in an arc, other holds a shield
        aa = -1.15 + math.sin(t) * 0.55                 # sword arm angle
        elbow_r = (sh[0] + math.cos(aa) * s * 0.34,
                   sh[1] + math.sin(aa) * s * 0.34)
        hand_r = (elbow_r[0] + math.cos(aa - 0.3) * s * 0.34,
                  elbow_r[1] + math.sin(aa - 0.3) * s * 0.34)
        # shield arm across body
        hand_l = (sh[0] - s * 0.30, sh[1] + s * 0.16)
        elbow_l = (sh[0] - s * 0.20, sh[1] + s * 0.20)
    else:
        # jhora — arms out to link with neighbours, bobbing
        ba = math.sin(t + 1.0) * 0.18
        hand_l = (sh[0] - s * 0.52, sh[1] + s * 0.10 + ba * s)
        elbow_l = (sh[0] - s * 0.28, sh[1] + s * 0.10)
        hand_r = (sh[0] + s * 0.52, sh[1] + s * 0.10 - ba * s)
        elbow_r = (sh[0] + s * 0.28, sh[1] + s * 0.10)

    # draw legs
    _limb(dr, hip, lknee, lw, col); _limb(dr, lknee, lfoot, lw, col)
    _limb(dr, hip, rknee, lw, col); _limb(dr, rknee, rfoot, lw, col)
    # torso (filled)
    tw = s * 0.20
    dr.polygon([(hip[0] - tw, hip[1]), (hip[0] + tw, hip[1]),
                (sh[0] + tw * 0.8, sh[1]), (sh[0] - tw * 0.8, sh[1])], fill=col)
    _limb(dr, hip, sh, int(tw * 2), col)
    # arms
    _limb(dr, sh, elbow_l, lw, col); _limb(dr, elbow_l, hand_l, lw, col)
    _limb(dr, sh, elbow_r, lw, col); _limb(dr, elbow_r, hand_r, lw, col)
    # head
    dr.ellipse([head_c[0] - head_r, head_c[1] - head_r,
                head_c[0] + head_r, head_c[1] + head_r], fill=col)

    if kind == "chholiya":
        # sword
        sa = aa - 0.3
        tip = (hand_r[0] + math.cos(sa) * s * 0.62,
               hand_r[1] + math.sin(sa) * s * 0.62)
        dr.line([hand_r, tip], fill=rgba(D.C.GOLD_LIGHT, 210),
                width=max(2, int(s * 0.03)))
        # shield
        shr = int(s * 0.16)
        dr.ellipse([hand_l[0] - shr, hand_l[1] - shr,
                    hand_l[0] + shr, hand_l[1] + shr], fill=rgb(D.C.MAROON))
        dr.ellipse([hand_l[0] - shr, hand_l[1] - shr,
                    hand_l[0] + shr, hand_l[1] + shr], outline=rgb(D.C.GOLD), width=2)
    return hand_l, hand_r


# ----------------------------------------------------------------- embers ----
def make_embers(n=46):
    import random
    random.seed(7)
    e = []
    for _ in range(n):
        e.append(dict(
            x=random.uniform(0, W),
            base=random.uniform(GROUND_Y - 30, GROUND_Y + 20),
            cyc=random.randint(1, 3),                 # integer cycles -> seamless
            ph=random.random(),
            rise=random.uniform(H * 0.35, H * 0.72),
            amp=random.uniform(10, 34),
            r=random.uniform(1.2, 3.0),
            col=random.choice([D.C.GOLD_LIGHT, D.C.SAFFRON, D.C.GOLD]),
        ))
    return e


def draw_embers(canvas, embers, phase):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    for e in embers:
        u = (phase * e["cyc"] + e["ph"]) % 1.0
        y = e["base"] - u * e["rise"]
        x = e["x"] + math.sin((u * e["cyc"] + e["ph"]) * TAU) * e["amp"]
        a = int(200 * math.sin(u * math.pi) * (0.5 + 0.5 * math.sin(phase * TAU * 3 + e["ph"] * 6)))
        a = max(0, min(210, a))
        r = e["r"]
        dr.ellipse([x - r, y - r, x + r, y + r], fill=rgba(e["col"], a))
    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    return Image.alpha_composite(canvas.convert("RGBA"), layer)


# ------------------------------------------------------------------- render --
def render():
    backdrop = build_backdrop()
    embers = make_embers()
    frames_dir = os.path.join(HERE, "_frames")
    os.makedirs(frames_dir, exist_ok=True)
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))

    # dancer line-up: a swaying Jhora row flanked by two Chholiya dancers
    line = [
        ("chholiya", 0.16, 150, -1.0),
        ("jhora",    0.31, 168, 0.0),
        ("jhora",    0.42, 182, 0.0),
        ("jhora",    0.52, 196, 0.0),
        ("jhora",    0.62, 182, 0.0),
        ("jhora",    0.73, 168, 0.0),
        ("chholiya", 0.87, 150, 1.0),
    ]
    for i in range(N):
        phase = i / N
        fig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dr = ImageDraw.Draw(fig)
        hands = []
        for j, (kind, fx, sc, lean) in enumerate(line):
            cx = fx * W
            by = GROUND_Y + (sc - 182) * 0.10
            dphase = phase + j * 0.13            # travelling wave along the line
            hl, hr = draw_dancer(dr, cx, by, sc, dphase % 1.0, kind, lean)
            hands.append((hl, hr, kind))
        # link Jhora hands with a soft rope-of-arms line
        for a in range(len(line) - 1):
            _, hr, ka = hands[a]
            hl, _, kb = hands[a + 1]
            if ka == "jhora" and kb == "jhora":
                dr.line([hr, hl], fill=rgb(D.C.INK), width=max(3, int(170 * 0.09)))
        frame = backdrop.copy().convert("RGBA")
        frame = Image.alpha_composite(frame, fig)
        frame = draw_embers(frame, embers, phase)
        # subtle breathing glow bottom-centre
        frame.convert("RGB").save(os.path.join(frames_dir, f"f{i:04d}.jpg"),
                                   quality=90)
        if i == N // 3:
            frame.convert("RGB").save(os.path.join(ASSETS, "dance_poster.jpg"),
                                      quality=92)
    return frames_dir


def encode(frames_dir):
    out = os.path.join(ASSETS, "dance.mp4")
    cmd = [FFMPEG, "-y", "-framerate", str(FPS),
           "-i", os.path.join(frames_dir, "f%04d.jpg"),
           "-vf", "format=yuv420p",
           "-c:v", "libx264", "-profile:v", "high", "-crf", "23",
           "-movflags", "+faststart", "-r", str(FPS), out]
    subprocess.run(cmd, check=True, capture_output=True)
    return out


if __name__ == "__main__":
    print("rendering dance frames…")
    fd = render()
    print("encoding mp4…")
    out = encode(fd)
    sz = os.path.getsize(out) / 1e6
    print(f"saved {out}  ({sz:.1f} MB, {SECONDS:.0f}s loop, {N} frames)")
