"""
GARH KAUTHIG — Student Curtain-Raiser Deck
===========================================
A vibrant, celebratory event-introduction presentation for the Swaragini
Cultural Club's "Garh Kauthig" — built to excite students, NOT a documentary.

Content follows the club's own script (no history section).  Vibrant festival
palette.  Real event photos drop into the labelled PHOTO frames (see photos/).

    python3 event.py           # -> GarhKauthig.pptx
"""
from __future__ import annotations
import os
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

import design as D
from design import rgb
import pptx_helpers as PX
from pptx_helpers import (text, picture, rect, hairline, vline, dot, ring,
                          notes, blank_slide, set_slide_bg, IN)
from anim import Timeline, set_transition
import icons
import media

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
PHOTOS = os.path.join(HERE, "photos")
ICONDIR = os.path.join(ASSETS, "icons")

W, H = D.SLIDE_W_IN, D.SLIDE_H_IN
MX = 0.92


# ---------------------------------------------------------- vibrant palette --
class V:
    GREEN_DEEP = "0A3B2C"     # rich festival green (primary bg)
    GREEN = "12583F"
    GREEN_BRIGHT = "1C7A54"
    CREAM = "FBF1DC"          # warm cream (alt bg)
    CREAM_DEEP = "F3E4C6"
    WHITE = "FFFDF7"
    INK = "12241C"

    MARIGOLD = "F5A81C"       # marigold yellow
    SAFFRON = "EE7B1E"        # saffron orange
    RED = "E23A2E"            # festive red
    MAGENTA = "D81E6A"        # pink-magenta (pichhora)
    TURQUOISE = "17A6A0"      # turquoise
    BLUE = "1E63B4"           # royal blue
    GOLD = "F2CE7B"
    GOLD_DEEP = "D9A43A"


ACCENTS = [V.MARIGOLD, V.RED, V.TURQUOISE, V.SAFFRON, V.MAGENTA, V.BLUE]

FD, FS, FE = D.F_DISPLAY, D.F_SERIF, D.F_EDITORIAL
FB, FU = D.F_BODY, D.F_UI


# ------------------------------------------------------------------ helpers --
def para(txt, **kw):
    kw["text"] = txt
    kw.setdefault("size", 17)
    kw.setdefault("color", V.WHITE)
    kw.setdefault("font", FB)
    return kw


_prs = None
IDX = 0


def new_slide(bg=V.GREEN_DEEP, transition="morph", dur=D.D_TRANSITION):
    slide = blank_slide(_prs)
    set_slide_bg(slide, bg)
    set_transition(slide, transition, dur)
    return slide, Timeline(slide)


def _idx():
    global IDX
    IDX += 1
    return IDX


def eyebrow(slide, x, y, txt, color=V.GOLD, w=10.0):
    dot(slide, x + 0.05, y + 0.13, 0.12, fill=V.MARIGOLD)
    return [text(slide, x + 0.26, y, w, 0.34,
                 [para(txt, font=FU, size=12.5, color=color, caps=True,
                       track=300)], name="eyebrow")]


def icon_chip(slide, cx, cy, d, name, ring_color, glyph_color=None, lw=3.0):
    """A round color chip with a line icon — the deck's vibrant motif."""
    dot(slide, cx, cy, d, fill=ring_color)
    p = os.path.join(ICONDIR, _icon_file(name, glyph_color or "12241C"))
    if p and os.path.exists(p):
        picture(slide, p, cx - d * 0.28, cy - d * 0.28, d * 0.56, d * 0.56)
    return


_ICON_CACHE = {}


def _icon_file(name, color):
    """Render an icon PNG in a given colour on demand, cached to assets/icons."""
    key = (name, color)
    if key in _ICON_CACHE:
        return _ICON_CACHE[key]
    fn = f"ev_{name}_{color}.png"
    path = os.path.join(ICONDIR, fn)
    if not os.path.exists(path):
        try:
            img = icons.render(name, 220, color=color, lw=7.0)
            img.save(path)
        except Exception:
            _ICON_CACHE[key] = None
            return None
    _ICON_CACHE[key] = fn
    return fn


def photo_frame(slide, x, y, w, h, label="YOUR PHOTO", accent=V.MARIGOLD,
                icon="mountain", tint=V.GREEN_BRIGHT, name=None):
    """
    A vibrant placeholder that becomes a real photo once files are supplied.
    Rounded, accent-bordered, with a soft tint, an icon and a caption so the
    layout already reads well before the photos are dropped in.
    """
    card = rect(slide, x, y, w, h, fill=tint, alpha=0.30, line=accent,
                line_w=2.4, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.045,
                name=name or "photo")
    ic = _icon_file(icon, accent.lstrip("#"))
    if ic:
        s = min(w, h) * 0.30
        picture(slide, os.path.join(ICONDIR, ic), x + w / 2 - s / 2,
                y + h / 2 - s * 0.75, s, s)
    text(slide, x, y + h / 2 + min(w, h) * 0.12, w, 0.4,
         [para(label, font=FU, size=11, color=accent, caps=True, track=240,
               align="c")])
    return card


def real_or_frame(slide, x, y, w, h, filename, **frame_kw):
    """Use a real photo if present in photos/, else a labelled frame."""
    p = os.path.join(PHOTOS, filename)
    if os.path.exists(p):
        # cover-crop into the box via a rounded picture
        pic = picture(slide, p, x, y, w, h)
        return pic
    return photo_frame(slide, x, y, w, h, **frame_kw)


def footer(slide, label):
    text(slide, MX, H - 0.44, 7.0, 0.3,
         [para("GARH  KAUTHIG", font=FU, size=9.5, color=V.GOLD, caps=True,
               track=260)], name="fL")
    text(slide, W - MX - 5.0, H - 0.44, 5.0, 0.3,
         [para(label, font=FU, size=9.5, color=V.GOLD_DEEP, caps=True,
               track=200, align="r")], name="fR")


def band(slide, y, h, color, alpha=1.0):
    return rect(slide, -0.1, y, W + 0.2, h, fill=color, alpha=alpha)


def living_bg(slide, tl, accent=V.MARIGOLD, cool=False, petals=True):
    """Subtle vibrant motion: a drifting glow + floating particles."""
    glow = os.path.join(ASSETS, "glow_cool.png" if cool else "glow_gold.png")
    if os.path.exists(glow):
        g = picture(slide, glow, W * 0.5 - 4.5, -1.2, 9.0, 9.0)
        PX.set_picture_transparency(g, 0.35)
        tl.loop_zoom(g, 1.07, D.LOOP_GLOW)
    if petals:
        fx = os.path.join(ASSETS, "fx_petals.png")
        if os.path.exists(fx):
            p = picture(slide, fx, D.BLEED["x"], D.BLEED["y"], D.BLEED["w"],
                        D.BLEED["h"])
            PX.set_picture_transparency(p, 0.2)
            tl.loop_drift(p, 0.02, 0.012, D.LOOP_DUST)


def ornament_border(slide, top=True):
    p = os.path.join(ASSETS, "orn_aipan_gold.png")
    if os.path.exists(p):
        if top:
            picture(slide, p, -0.1, -0.15, W + 0.2, 0.9)
        else:
            picture(slide, p, -0.1, H - 0.75, W + 0.2, 0.9)


# ============================================================= SLIDES ========
def s_cover():
    slide, tl = new_slide(bg=V.GREEN_DEEP, transition="none")
    living_bg(slide, tl, accent=V.MARIGOLD)
    ornament_border(slide, top=True)

    eb = eyebrow(slide, MX, 1.02, "Swaragini Cultural Club  ·  Presents",
                 color=V.GOLD, w=11)
    # Devanagari hero title
    hi = text(slide, MX, 1.5, W - 2 * MX, 2.2,
              [para("गढ़ कौथिग", font=FD, size=118, color=V.MARIGOLD, bold=True,
                    cs=True, shadow=dict(blur=26, dist=5, alpha=55))],
              name="hindi")
    sub = text(slide, MX, 3.9, W - 2 * MX, 1.0,
               [para("A Celebration of Uttarakhand\u2019s Culture", font=FE,
                     size=40, color=V.WHITE,
                     shadow=dict(blur=18, dist=3, alpha=50))], name="sub")
    r = hairline(slide, MX, 4.98, 3.0, color=V.MARIGOLD, weight=2.4)
    tag = text(slide, MX, 5.16, W - 2 * MX, 0.5,
               [para("Music  ·  Dance  ·  Food  ·  Craft  ·  Community",
                     font=FU, size=15, color=V.GOLD, caps=True, track=240)],
               name="tag")

    # a bright photo strip across the bottom (their event collage goes here)
    files = ["cover1.jpg", "cover2.jpg", "cover3.jpg", "cover4.jpg", "cover5.jpg"]
    fw = (W - 2 * MX - 4 * 0.18) / 5
    frames = []
    for i, fn in enumerate(files):
        fx = MX + i * (fw + 0.18)
        fr = real_or_frame(slide, fx, 5.95, fw, 1.05, fn,
                           label="PHOTO", accent=ACCENTS[i % len(ACCENTS)],
                           icon=["dancer", "temple", "dhol", "mountain",
                                 "hands"][i], tint=V.GREEN_BRIGHT)
        frames.append(fr)

    aud = media.add_audio(slide, os.path.join(ASSETS, "score.m4a"),
                          x=W - 0.56, y=0.28, size=0.40)
    for s in eb:
        tl.fade_in(s, delay=300)
    tl.rise_in(hi, delay=600, dur=1500, rise=0.05)
    tl.rise_in(sub, delay=1300, dur=1400)
    tl.wipe_in(r, delay=1900, dur=800)
    tl.fade_in(tag, delay=2150, dur=1200)
    tl.stagger(frames, start=2400, gap=180, mode="rise")
    tl.play_media(aud, loop=True, vol=60000, kind="audio")
    footer(slide, "Curtain Raiser")
    tl.apply()
    notes(slide, "Open on the title. Let the dhol-damau track set the mood. "
                 "This is a surprise curtain-raiser \u2014 keep the energy high.")


def s_represents():
    slide, tl = new_slide(bg=V.GREEN_DEEP)
    living_bg(slide, tl, accent=V.SAFFRON)
    eb = eyebrow(slide, MX, 0.8, "What It Means")
    ttl = text(slide, MX, 1.22, 8.2, 1.0,
               [para("Garh Kauthig represents", font=FE, size=44, color=V.WHITE),
                para("a celebration of belonging", font=FE, size=44,
                     color=V.MARIGOLD)], name="title")
    r = hairline(slide, MX, 2.9, 2.4, color=V.MARIGOLD, weight=2.2)
    body = text(slide, MX, 3.15, 6.0, 2.6,
                [para("\u201cGarh Kauthik\u201d is a traditional Uttarakhandi "
                      "word meaning a fair, festival or community celebration.",
                      font=FS, size=24, color=V.WHITE, italic=True, line=1.28),
                 para("It brings people together to celebrate the region\u2019s "
                      "culture, music, dance, food, clothing and traditions.",
                      font=FB, size=17, color=V.GOLD, line=1.4, before=14)],
                name="body")
    fr = real_or_frame(slide, 7.5, 1.5, 4.9, 4.6, "represents.jpg",
                       label="FESTIVAL PHOTO", accent=V.MARIGOLD, icon="dhol",
                       tint=V.GREEN_BRIGHT)
    for s in eb:
        tl.fade_in(s, delay=250)
    tl.rise_in(ttl, delay=500, dur=1300)
    tl.wipe_in(r, delay=1100, dur=700)
    tl.rise_in(body, delay=1300, dur=1300)
    tl.zoom_in(fr, delay=900, dur=1500)
    footer(slide, "01 · Meaning")
    tl.apply()
    notes(slide, "Define the word simply. Kauthig = a fair / celebration that "
                 "brings the whole community together.")


def s_where():
    slide, tl = new_slide(bg=V.CREAM)
    band(slide, 0, 2.35, V.GREEN_DEEP)
    living_bg(slide, tl, accent=V.SAFFRON, petals=False)
    eb = eyebrow(slide, MX, 0.7, "Across The Hills", color=V.GOLD)
    ttl = text(slide, MX, 1.12, W - 2 * MX, 0.8,
               [para("Where is Garh Kauthig celebrated?", font=FE, size=34,
                     color=V.WHITE)], name="title")
    lead = text(slide, MX, 1.78, W - 2 * MX, 0.5,
                [para("In villages, towns and cities across Uttarakhand \u2014 "
                      "especially the Garhwal region. It comes alive during:",
                      font=FB, size=14.5, color=V.GOLD, align="c")], name="lead")

    items = [
        ("seedling", "HARVEST FESTIVALS",
         "Gratitude for bountiful crops and agricultural prosperity."),
        ("temple", "SACRED DAYS",
         "Rituals and spiritual observances across mountain hamlets."),
        ("cart", "COMMUNITY MELAS",
         "Seasonal harvest gatherings and regional marketplaces."),
        ("flag", "TEMPLE PROCESSIONS",
         "Annual deity processions and community thanksgiving melas."),
        ("youth", "MODERN PLATFORMS",
         "Bringing youth together to celebrate folk arts and identity."),
    ]
    cw = (W - 2 * MX - 4 * 0.3) / 5
    cards = []
    for i, (ic, hd, bd) in enumerate(items):
        x = MX + i * (cw + 0.3)
        acc = ACCENTS[i % len(ACCENTS)]
        fr = real_or_frame(slide, x, 2.62, cw, 1.85, f"where{i+1}.jpg",
                           label="PHOTO", accent=acc, icon=ic, tint=V.GREEN)
        icon_chip(slide, x + cw / 2, 4.68, 0.62, ic, acc)
        hh = text(slide, x - 0.1, 5.08, cw + 0.2, 0.5,
                  [para(hd, font=FU, size=11.5, color=V.GREEN_DEEP, bold=True,
                        caps=True, track=60, align="c")], name="wh")
        bb = text(slide, x - 0.1, 5.5, cw + 0.2, 1.4,
                  [para(bd, font=FB, size=10.5, color="2A4034", align="c",
                        line=1.24)], name="wb")
        cards += [fr, hh, bb]
    for s in eb:
        tl.fade_in(s, delay=200)
    tl.fade_in(ttl, delay=450)
    tl.fade_in(lead, delay=700)
    tl.stagger(cards, start=1000, gap=140, mode="rise")
    footer(slide, "02 · Where")
    tl.apply()
    notes(slide, "Five occasions when Kauthigs happen. Emphasise: it's woven "
                 "into the farming calendar, faith, and now student life.")


def s_happens():
    slide, tl = new_slide(bg=V.GREEN_DEEP)
    living_bg(slide, tl, accent=V.MAGENTA)
    eb = eyebrow(slide, MX, 0.8, "The Experience")
    ttl = text(slide, MX, 1.2, 6.4, 1.6,
               [para("What happens at a", font=FE, size=40, color=V.WHITE),
                para("Garh Kauthig", font=FE, size=40, color=V.MARIGOLD)],
               name="title")
    acts = [
        ("dancer", "Garhwali & Kumaoni folk dance and music"),
        ("flag", "Cultural competitions and regional games"),
        ("sweet", "Local, authentic food stalls and handicrafts"),
        ("jewel", "Traditional clothing and mountain jewellery"),
    ]
    rows = []
    for i, (ic, tx) in enumerate(acts):
        y = 2.9 + i * 0.82
        acc = ACCENTS[i % len(ACCENTS)]
        icon_chip(slide, MX + 0.32, y + 0.24, 0.6, ic, acc)
        rr = text(slide, MX + 0.85, y, 5.6, 0.7,
                  [para(tx, font=FB, size=16.5, color=V.WHITE, line=1.12)],
                  name="act")
        rows.append(rr)

    # folk performances panel
    panel = rect(slide, 7.2, 1.5, 5.2, 4.6, fill=V.MARIGOLD, alpha=0.95,
                 shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05, name="panel")
    ph = text(slide, 7.55, 1.85, 4.6, 0.6,
              [para("POPULAR FOLK PERFORMANCES", font=FU, size=13,
                    color=V.GREEN_DEEP, bold=True, caps=True, track=120)],
              name="ph")
    pv = text(slide, 7.55, 2.55, 4.55, 1.3,
              [para("Jhora  ·  Chanchari  ·  Chholiya", font=FE, size=20,
                    color=V.INK, line=1.22),
               para("Pandav Nritya  ·  Langvir Nritya", font=FE, size=20,
                    color=V.INK, line=1.22, before=6)], name="pv")
    pb = text(slide, 7.55, 3.95, 4.55, 1.9,
              [para("Mesmerising performances that showcase the martial spirit "
                    "and living culture of the mountains \u2014 danced in a "
                    "circle, together.", font=FB, size=13, color=V.GREEN_DEEP,
                    line=1.34)], name="pb")
    for s in eb:
        tl.fade_in(s, delay=200)
    tl.rise_in(ttl, delay=450, dur=1300)
    tl.stagger(rows, start=1000, gap=200, mode="rise")
    tl.zoom_in(panel, delay=900, dur=1200)
    tl.fade_in(ph, delay=1400)
    tl.rise_in(pv, delay=1650, dur=1200)
    tl.fade_in(pb, delay=2050)
    footer(slide, "03 · What Happens")
    tl.apply()
    notes(slide, "Dance, music, competitions, food, crafts, costume. Name the "
                 "folk forms \u2014 students may get to learn some of these.")


def s_offer():
    slide, tl = new_slide(bg=V.CREAM)
    living_bg(slide, tl, accent=V.TURQUOISE, cool=True, petals=False)
    eb = eyebrow(slide, MX, 0.8, "For Every Participant", color=V.SAFFRON)
    ttl = text(slide, MX, 1.22, W - 2 * MX, 0.9,
               [para("What will this event offer you?", font=FE, size=40,
                     color=V.GREEN_DEEP)], name="title")
    lead = text(slide, MX, 2.15, 9.5, 0.5,
                [para("A chance to grow \u2014 culturally, creatively and "
                      "personally:", font=FB, size=15, color=V.SAFFRON)],
                name="lead")
    offers = [
        ("book", "Learn about Uttarakhand\u2019s rich culture"),
        ("hands", "Develop creative and performance skills"),
        ("dhol", "Experience traditional music and dance"),
        ("sunrise", "An exclusive opportunity to showcase your talent"),
        ("youth", "Build confidence, teamwork and cultural roots"),
    ]
    cw = (W - 2 * MX - 0.4) / 2
    cards = []
    for i, (ic, tx) in enumerate(offers):
        col, row = i % 2, i // 2
        x = MX + col * (cw + 0.4)
        y = 2.9 + row * 1.22
        if i == 4:
            x = MX + (W - 2 * MX) / 2 - cw / 2      # center the last one
        acc = ACCENTS[i % len(ACCENTS)]
        c = rect(slide, x, y, cw, 1.02, fill=V.WHITE, alpha=1.0, line=acc,
                 line_w=1.6, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08,
                 name="ocard")
        icon_chip(slide, x + 0.55, y + 0.51, 0.62, ic, acc)
        tt = text(slide, x + 1.0, y, cw - 1.2, 1.02,
                  [para(tx, font=FB, size=15, color=V.GREEN_DEEP, line=1.14)],
                  name="ot", anchor=MSO_ANCHOR.MIDDLE)
        cards += [c, tt]
    for s in eb:
        tl.fade_in(s, delay=200)
    tl.rise_in(ttl, delay=450, dur=1200)
    tl.fade_in(lead, delay=800)
    tl.stagger(cards, start=1100, gap=130, mode="rise")
    footer(slide, "04 · What You Gain")
    tl.apply()
    notes(slide, "Sell the value to students: culture, skills, stage time, "
                 "confidence, friendships.")


def s_guide():
    slide, tl = new_slide(bg=V.GREEN_DEEP)
    living_bg(slide, tl, accent=V.MAGENTA)
    eb = eyebrow(slide, MX, 0.8, "Your Mentors")
    ttl = text(slide, MX, 1.22, 6.2, 1.0,
               [para("Who will guide you?", font=FE, size=42, color=V.WHITE)],
               name="title")
    body = text(slide, MX, 2.5, 5.6, 2.6,
                [para("Our teams", font=FB, size=17, color=V.GOLD, line=1.4),
                 para("DevBhoomi & Uttarayani", font=FE, size=34,
                      color=V.MARIGOLD, line=1.12, before=4),
                 para("will guide participants and teach them about "
                      "Uttarakhand\u2019s traditional culture, folk "
                      "performances, and authentic artistic presentation.",
                      font=FB, size=16, color=V.WHITE, line=1.4, before=12)],
                name="body")
    # two mentor team frames
    f1 = real_or_frame(slide, 6.9, 1.5, 2.6, 2.9, "team1.jpg",
                       label="TEAM DEVBHOOMI", accent=V.RED, icon="dancer",
                       tint=V.GREEN_BRIGHT)
    f2 = real_or_frame(slide, 9.75, 1.5, 2.65, 2.9, "team2.jpg",
                       label="TEAM UTTARAYANI", accent=V.TURQUOISE,
                       icon="hands", tint=V.GREEN_BRIGHT)
    f3 = real_or_frame(slide, 6.9, 4.6, 5.5, 2.1, "team3.jpg",
                       label="PERFORMANCE PHOTO", accent=V.MARIGOLD,
                       icon="flag", tint=V.GREEN_BRIGHT)
    for s in eb:
        tl.fade_in(s, delay=250)
    tl.rise_in(ttl, delay=500, dur=1300)
    tl.rise_in(body, delay=900, dur=1300)
    tl.stagger([f1, f2, f3], start=1000, gap=220, mode="zoom")
    footer(slide, "05 · Your Guides")
    tl.apply()
    notes(slide, "Introduce the mentor teams DevBhoomi and Uttarayani \u2014 "
                 "the seniors who will train the participants.")


def s_win():
    slide, tl = new_slide(bg=V.GREEN_DEEP)
    living_bg(slide, tl, accent=V.MARIGOLD)
    ornament_border(slide, top=False)
    eb = eyebrow(slide, MX, 1.0, "Your Moment On Stage", color=V.GOLD, w=11)
    ttl = text(slide, MX, 1.5, W - 2 * MX, 1.6,
               [para("Showcase your talent \u2014 and win!", font=FE, size=48,
                     color=V.WHITE, shadow=dict(blur=18, dist=3, alpha=45))],
               name="title")
    body = text(slide, MX, 3.0, W - 2 * MX, 0.9,
                [para("Present the true beauty of Uttarakhand\u2019s culture "
                      "through your own creativity and performance.", font=FB,
                      size=18, color=V.GOLD, align="c", line=1.35)],
                name="body")
    # prize block
    pill = rect(slide, W / 2 - 2.6, 4.15, 5.2, 2.1, fill=V.MARIGOLD, alpha=1.0,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.10, name="pill")
    plabel = text(slide, W / 2 - 2.6, 4.42, 5.2, 0.5,
                  [para("CASH PRIZE", font=FU, size=17, color=V.GREEN_DEEP,
                        bold=True, caps=True, track=280, align="c")],
                  name="plabel")
    prize = text(slide, W / 2 - 2.6, 4.9, 5.2, 1.2,
                 [para("\u20B9 11,000", font=FD, size=72, color=V.RED,
                       bold=True, align="c")], name="prize")
    for s in eb:
        tl.fade_in(s, delay=300)
    tl.rise_in(ttl, delay=650, dur=1400)
    tl.fade_in(body, delay=1300)
    tl.zoom_in(pill, delay=1600, dur=1100)
    tl.fade_in(plabel, delay=2000)
    tl.rise_in(prize, delay=2200, dur=1200)
    footer(slide, "06 · Compete")
    tl.apply()
    notes(slide, "The hook: participate and win. Announce the cash prize of "
                 "\u20B911,000 with energy \u2014 this is the call to action.")


def s_closing():
    slide, tl = new_slide(bg=V.CREAM, transition="smooth",
                          dur=D.D_TRANSITION_SLOW)
    living_bg(slide, tl, accent=V.SAFFRON, petals=True)
    ornament_border(slide, top=True)
    ornament_border(slide, top=False)
    ln = text(slide, 0.6, 2.55, W - 1.2, 2.6,
              [para("Celebrate our traditions,", font=FE, size=42,
                    color=V.GREEN_DEEP, align="c", line=1.2),
               para("showcase your talent, and keep the", font=FE, size=42,
                    color=V.GREEN_DEEP, align="c", line=1.2),
               para("culture of Uttarakhand alive.", font=FE, size=42,
                    color=V.RED, align="c", line=1.2, before=6)], name="line")
    tl.rise_in(ln, delay=500, dur=1800, rise=0.03)
    footer(slide, "The Invitation")
    tl.apply()
    notes(slide, "Land the emotional line, then invite them in. Pause before "
                 "Thank You.")


def s_thanks():
    slide, tl = new_slide(bg=V.GREEN_DEEP, transition="smooth",
                          dur=D.D_TRANSITION_SLOW)
    living_bg(slide, tl, accent=V.MARIGOLD)
    ornament_border(slide, top=True)
    ornament_border(slide, top=False)
    ty = text(slide, MX, 2.4, W - 2 * MX, 1.6,
              [para("THANK YOU!", font=FD, size=88, color=V.MARIGOLD, bold=True,
                    align="c", shadow=dict(blur=24, dist=4, alpha=55))],
              name="ty")
    sub = text(slide, MX, 4.5, W - 2 * MX, 0.7,
               [para("Presented by the Swaragini Cultural Club", font=FU,
                     size=16, color=V.GOLD, caps=True, track=200, align="c")],
               name="sub")
    tl.rise_in(ty, delay=500, dur=1500, rise=0.04)
    tl.fade_in(sub, delay=1300, dur=1300)
    tl.apply()
    notes(slide, "Close with warmth and a smile. Invite questions / sign-ups.")


# ================================================================= build =====
def build():
    global _prs, IDX
    IDX = 0
    _prs = Presentation()
    _prs.slide_width = D.SLIDE_W_EMU
    _prs.slide_height = D.SLIDE_H_EMU

    s_cover()
    s_represents()
    s_where()
    s_happens()
    s_offer()
    s_guide()
    s_win()
    s_closing()
    s_thanks()

    out = os.path.join(HERE, "GarhKauthig.pptx")
    _prs.save(out)
    n = len(_prs.slides._sldIdLst)
    print(f"saved {out}  ({n} slides, {os.path.getsize(out)/1e6:.1f} MB)")


if __name__ == "__main__":
    os.makedirs(PHOTOS, exist_ok=True)
    build()
