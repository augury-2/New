"""
KAUTHIK — Animation Engine
==========================
python-pptx cannot author animations, so this module writes the OOXML
`<p:timing>` tree and slide transitions by hand.

Two ideas carry the whole deck:

1. LIVING BACKGROUNDS. Every background plate is oversized beyond the slide
   edge and given an infinitely repeating, auto-reversing, eased motion or
   scale behaviour. Different layers get different periods and directions, so
   the composite never visibly repeats and the parallax reads as real depth.
   Because the motion is a ping-pong with `accel`/`decel` easing, velocity
   goes to zero at each turn — there is no snap, no seam, no jolt.

2. CHOREOGRAPHED FOREGROUND. Titles, rules, cards, charts and icons are all
   placed in one auto-starting group with computed delays, so each slide
   plays itself the moment it appears. Nothing depends on the presenter
   clicking at the right moment.

Everything is emitted as one auto-start click-group, which keeps the id space
small and the XML close to what PowerPoint itself writes.
"""

from __future__ import annotations

from lxml import etree

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "p14": "http://schemas.microsoft.com/office/powerpoint/2010/main",
    "p159": "http://schemas.microsoft.com/office/powerpoint/2015/09/main",
}
P = NS["p"]


def _q(tag: str) -> str:
    pre, local = tag.split(":")
    return "{%s}%s" % (NS[pre], local)


def _parse(xml: str) -> etree._Element:
    return etree.fromstring(xml.encode("utf-8"))


# ============================================================== transitions ===
_XMLNS = (
    'xmlns:p="%(p)s" xmlns:a="%(a)s" xmlns:r="%(r)s" '
    'xmlns:mc="%(mc)s" xmlns:p14="%(p14)s"' % NS
)


def set_transition(slide, kind: str = "morph", dur: int = 1500,
                   morph_by: str = "byObject") -> None:
    """
    Attach a slide transition.

    kind: 'morph'  — Morph (PowerPoint 2016+), degrading to a smooth fade in
                     older builds via mc:Fallback
          'fade'   — cross fade through black-free blend
          'smooth' — long, slow fade used for chapter dividers
          'none'   — remove any transition
    """
    sld = slide._element
    for old in sld.findall(_q("p:transition")):
        sld.remove(old)
    for old in sld.findall(_q("mc:AlternateContent")):
        sld.remove(old)
    if kind == "none":
        return

    if kind == "morph":
        xml = (
            '<mc:AlternateContent %(ns)s>'
            '<mc:Choice xmlns:p159="%(p159)s" Requires="p159">'
            '<p:transition spd="slow" p14:dur="%(dur)d">'
            '<p159:morph option="%(opt)s"/>'
            '</p:transition></mc:Choice>'
            '<mc:Fallback>'
            '<p:transition spd="slow" p14:dur="%(dur)d"><p:fade/></p:transition>'
            '</mc:Fallback></mc:AlternateContent>'
            % dict(ns=_XMLNS, p159=NS["p159"], dur=dur, opt=morph_by)
        )
    else:
        spd = "slow" if kind == "smooth" else "med"
        xml = ('<p:transition %s spd="%s" p14:dur="%d"><p:fade/></p:transition>'
               % (_XMLNS, spd, dur))

    node = _parse(xml)
    anchor = sld.find(_q("p:clrMapOvr"))
    if anchor is not None:
        anchor.addnext(node)
    else:
        cs = sld.find(_q("p:cSld"))
        cs.addnext(node)


# ================================================================= timeline ===
class Timeline:
    """
    Collects animation effects for one slide, then writes the `<p:timing>`
    tree. All effects land in a single auto-starting group; ordering and
    rhythm come from per-effect `delay` values.
    """

    def __init__(self, slide):
        self.slide = slide
        self._fx: list[str] = []
        self._n = 0

    # ---------------------------------------------------------------- utils --
    def _id(self) -> int:
        self._n += 1
        return 100 + self._n * 3          # generous spacing, ids stay unique

    @staticmethod
    def _sid(shape) -> int:
        return int(shape._element.nvSpPr.cNvPr.get("id")) if hasattr(shape._element, "nvSpPr") \
            else int(shape._element.find(".//" + _q("p:cNvPr")).get("id"))

    def _tgt(self, shape) -> str:
        return '<p:tgtEl><p:spTgt spid="%d"/></p:tgtEl>' % self._sid(shape)

    def _effect(self, body: str, delay: int, preset_id: int, preset_class: str,
                subtype: int = 0, accel: int = 0, decel: int = 0,
                extra: str = "") -> None:
        self._fx.append(
            '<p:par><p:cTn id="%d" presetID="%d" presetClass="%s" '
            'presetSubtype="%d" fill="hold" grpId="0" nodeType="withEffect"%s%s%s>'
            '<p:stCondLst><p:cond delay="%d"/></p:stCondLst>'
            '<p:childTnLst>%s</p:childTnLst></p:cTn></p:par>'
            % (self._id(), preset_id, preset_class, subtype,
               (' accel="%d"' % accel) if accel else "",
               (' decel="%d"' % decel) if decel else "",
               extra, max(0, int(delay)), body)
        )

    # ------------------------------------------------- living background fx --
    def loop_drift(self, shape, dx: float, dy: float, dur: int,
                   delay: int = 0, ease: int = 45000) -> "Timeline":
        """
        Infinite, seamless parallax drift.

        dx/dy are fractions of the SLIDE size (0.04 ≈ half an inch on a 16:9
        deck). The path runs out to (dx, dy) and auto-reverses forever with
        symmetric easing, so the layer breathes rather than loops.
        """
        body = (
            '<p:animMotion origin="layout" path="M 0 0 L %.5f %.5f " '
            'pathEditMode="relative" ptsTypes="AA">'
            '<p:cBhvr additive="base">'
            '<p:cTn id="%d" dur="%d" autoRev="1" repeatCount="indefinite" '
            'accel="%d" decel="%d" fill="hold"/>'
            '%s'
            '<p:attrNameLst><p:attrName>ppt_x</p:attrName>'
            '<p:attrName>ppt_y</p:attrName></p:attrNameLst>'
            '</p:cBhvr></p:animMotion>'
            % (dx, dy, self._id(), dur, ease, ease, self._tgt(shape))
        )
        self._effect(body, delay, 0, "path", accel=ease, decel=ease)
        return self

    def loop_zoom(self, shape, pct: float, dur: int, delay: int = 0,
                  ease: int = 45000) -> "Timeline":
        """
        Infinite Ken-Burns breathing. `pct` is the target scale (1.06 = 106%).
        Only ever scales UP from rest, so an oversized plate can never expose
        a slide edge.
        """
        v = int(round(pct * 100000))
        body = (
            '<p:animScale>'
            '<p:cBhvr>'
            '<p:cTn id="%d" dur="%d" autoRev="1" repeatCount="indefinite" '
            'accel="%d" decel="%d" fill="hold"/>'
            '%s</p:cBhvr>'
            '<p:by x="%d" y="%d"/>'
            '</p:animScale>'
            % (self._id(), dur, ease, ease, self._tgt(shape), v, v)
        )
        self._effect(body, delay, 6, "emph", accel=ease, decel=ease)
        return self

    def loop_breathe(self, shape, dx: float, dy: float, pct: float,
                     dur_drift: int, dur_zoom: int, delay: int = 0) -> "Timeline":
        """Drift and breathe together — used for the hero sky plates."""
        self.loop_drift(shape, dx, dy, dur_drift, delay)
        self.loop_zoom(shape, pct, dur_zoom, delay)
        return self

    # ------------------------------------------------------ entrance effects --
    def _set_visible(self, shape, delay: int = 0) -> str:
        return (
            '<p:set><p:cBhvr>'
            '<p:cTn id="%d" dur="1" fill="hold">'
            '<p:stCondLst><p:cond delay="%d"/></p:stCondLst></p:cTn>'
            '%s'
            '<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
            '</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
            % (self._id(), delay, self._tgt(shape))
        )

    def fade_in(self, shape, delay: int = 0, dur: int = 1100) -> "Timeline":
        """The workhorse: a slow, clean fade up from nothing."""
        body = self._set_visible(shape) + (
            '<p:animEffect transition="in" filter="fade">'
            '<p:cBhvr><p:cTn id="%d" dur="%d"/>%s</p:cBhvr>'
            '</p:animEffect>' % (self._id(), dur, self._tgt(shape))
        )
        self._effect(body, delay, 10, "entr")
        return self

    def rise_in(self, shape, delay: int = 0, dur: int = 1300,
                rise: float = 0.035) -> "Timeline":
        """Fade while drifting gently upward — how every title enters."""
        body = self._set_visible(shape) + (
            '<p:animEffect transition="in" filter="fade">'
            '<p:cBhvr><p:cTn id="%d" dur="%d"/>%s</p:cBhvr></p:animEffect>'
            '<p:animMotion origin="layout" path="M 0 %.5f L 0 0 " '
            'pathEditMode="relative" ptsTypes="AA">'
            '<p:cBhvr additive="base">'
            '<p:cTn id="%d" dur="%d" decel="70000" fill="hold"/>%s'
            '<p:attrNameLst><p:attrName>ppt_x</p:attrName>'
            '<p:attrName>ppt_y</p:attrName></p:attrNameLst>'
            '</p:cBhvr></p:animMotion>'
            % (self._id(), dur, self._tgt(shape),
               rise, self._id(), dur, self._tgt(shape))
        )
        self._effect(body, delay, 42, "entr", subtype=4)
        return self

    def drift_in(self, shape, delay: int = 0, dur: int = 1400,
                 dx: float = -0.030, dy: float = 0.0) -> "Timeline":
        """Fade in while sliding from a direction — for side-entering cards."""
        body = self._set_visible(shape) + (
            '<p:animEffect transition="in" filter="fade">'
            '<p:cBhvr><p:cTn id="%d" dur="%d"/>%s</p:cBhvr></p:animEffect>'
            '<p:animMotion origin="layout" path="M %.5f %.5f L 0 0 " '
            'pathEditMode="relative" ptsTypes="AA">'
            '<p:cBhvr additive="base">'
            '<p:cTn id="%d" dur="%d" decel="70000" fill="hold"/>%s'
            '<p:attrNameLst><p:attrName>ppt_x</p:attrName>'
            '<p:attrName>ppt_y</p:attrName></p:attrNameLst>'
            '</p:cBhvr></p:animMotion>'
            % (self._id(), dur, self._tgt(shape),
               dx, dy, self._id(), dur, self._tgt(shape))
        )
        self._effect(body, delay, 42, "entr", subtype=4)
        return self

    def zoom_in(self, shape, delay: int = 0, dur: int = 1500,
                start: float = 0.94) -> "Timeline":
        """Fade in while easing up from slightly small — for hero imagery."""
        v = int(round(start * 100000))
        body = self._set_visible(shape) + (
            '<p:animEffect transition="in" filter="fade">'
            '<p:cBhvr><p:cTn id="%d" dur="%d"/>%s</p:cBhvr></p:animEffect>'
            '<p:animScale><p:cBhvr>'
            '<p:cTn id="%d" dur="%d" decel="65000" fill="hold"/>%s</p:cBhvr>'
            '<p:from x="%d" y="%d"/><p:to x="100000" y="100000"/>'
            '</p:animScale>'
            % (self._id(), dur, self._tgt(shape),
               self._id(), dur, self._tgt(shape), v, v)
        )
        self._effect(body, delay, 23, "entr", subtype=16)
        return self

    def wipe_in(self, shape, delay: int = 0, dur: int = 1400,
                direction: str = "left") -> "Timeline":
        """
        Progressive reveal — a timeline rule drawing itself, a bar growing,
        a map region filling in. `direction` is where the reveal starts from.
        """
        body = self._set_visible(shape) + (
            '<p:animEffect transition="in" filter="wipe(%s)">'
            '<p:cBhvr><p:cTn id="%d" dur="%d"/>%s</p:cBhvr>'
            '</p:animEffect>' % (direction, self._id(), dur, self._tgt(shape))
        )
        sub = {"left": 10, "right": 2, "up": 4, "down": 1}.get(direction, 10)
        self._effect(body, delay, 22, "entr", subtype=sub)
        return self

    def appear(self, shape, delay: int = 0) -> "Timeline":
        """Instant appear — the building block of the counting statistics."""
        self._effect(self._set_visible(shape), delay, 1, "entr")
        return self

    def disappear(self, shape, delay: int = 0) -> "Timeline":
        body = (
            '<p:set><p:cBhvr>'
            '<p:cTn id="%d" dur="1" fill="hold">'
            '<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
            '%s'
            '<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
            '</p:cBhvr><p:to><p:strVal val="hidden"/></p:to></p:set>'
            % (self._id(), self._tgt(shape))
        )
        self._effect(body, delay, 1, "exit")
        return self

    def count_up(self, shapes: list, delay: int = 0, step: int = 105) -> "Timeline":
        """
        Animate a statistic counting upward.

        `shapes` is a stack of identically positioned text boxes holding the
        intermediate values, ending with the true figure. Each appears, then
        vanishes as the next arrives; the final one stays. PowerPoint has no
        numeric text animation, so this is the honest way to do it — and it
        reads exactly like a counter on screen.
        """
        for i, sh in enumerate(shapes):
            self.appear(sh, delay + i * step)
            if i < len(shapes) - 1:
                self.disappear(sh, delay + (i + 1) * step)
        return self

    # ------------------------------------------------------ sequence helpers --
    def stagger(self, shapes, start: int = 0, gap: int = 260,
                mode: str = "rise", **kw) -> "Timeline":
        """Sequence a group of shapes — icon grids, cards, list items."""
        fn = {"rise": self.rise_in, "fade": self.fade_in,
              "drift": self.drift_in, "zoom": self.zoom_in,
              "wipe": self.wipe_in}[mode]
        for i, sh in enumerate(shapes):
            fn(sh, delay=start + i * gap, **kw)
        return self

    # ------------------------------------------------------------- emission --
    def apply(self) -> None:
        """Write the collected effects into the slide's <p:timing> element."""
        sld = self.slide._element
        for old in sld.findall(_q("p:timing")):
            sld.remove(old)
        if not self._fx:
            return

        xml = (
            '<p:timing %(ns)s><p:tnLst><p:par>'
            '<p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
            '<p:childTnLst><p:seq concurrent="1" nextAc="seek">'
            '<p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
            '<p:par><p:cTn id="3" fill="hold">'
            '<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
            '<p:childTnLst><p:par><p:cTn id="4" fill="hold">'
            '<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
            '<p:childTnLst>%(fx)s</p:childTnLst>'
            '</p:cTn></p:par></p:childTnLst>'
            '</p:cTn></p:par>'
            '</p:childTnLst></p:cTn>'
            '<p:prevCondLst><p:cond evt="onPrev" delay="0">'
            '<p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0">'
            '<p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
            '</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'
            % dict(ns=_XMLNS, fx="".join(self._fx))
        )
        node = _parse(xml)
        # <p:timing> must follow cSld / clrMapOvr / transition
        for tag in ("mc:AlternateContent", "p:transition", "p:clrMapOvr", "p:cSld"):
            prev = sld.find(_q(tag))
            if prev is not None:
                prev.addnext(node)
                return
        sld.append(node)
