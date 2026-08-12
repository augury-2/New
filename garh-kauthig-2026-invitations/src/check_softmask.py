#!/usr/bin/env python3
"""
Guards against the soft-mask failure that turned the display title into a solid
maroon rectangle and the year into a gold bar in the client's PDF viewer.

Background
----------
Several CSS constructs are exported by Chromium as PDF *soft-mask groups* in an
ExtGState -- a gradient clipped to text with `background-clip: text`, a gradient
fading to transparent, a blurred box-shadow, element `opacity`.  A viewer with
incomplete soft-mask support paints the masked content unmasked, so a gradient
clipped to the glyphs of "Garh Kauthig" arrives as a filled rectangle the size of
the heading.  It renders correctly in Ghostscript and Poppler, which is why the
fault reached the client rather than being caught locally.

The design now uses solid ink and pre-blended flat tints, so no such group should
exist.  This asserts that, per file:

  * no /Luminosity soft mask   (the failure mode above)
  * no /S /Alpha soft-mask group

Image alpha channels -- an /SMask on an /Subtype /Image -- are deliberately
allowed: that is how ordinary PNG transparency is stored, and support for it is
universal.

Run:  python3 src/check_softmask.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGETS = [
    os.path.join(ROOT, 'output', 'pdf'),
    os.path.join(ROOT, 'output', 'print-ready', 'rgb'),
    os.path.join(ROOT, 'output', 'print-ready', 'cmyk'),
    os.path.join(ROOT, 'output', 'print-ready', 'with-crop-marks'),
]


def audit(path):
    raw = open(path, 'rb').read()
    luminosity = raw.count(b'/Luminosity')
    alpha_group = raw.count(b'/S /Alpha') + raw.count(b'/S/Alpha')
    # /SMask entries that sit on an image dictionary are fine
    image_alpha = raw.count(b'/SMask') - raw.count(b'/SMask /None')
    return luminosity, alpha_group, image_alpha


def main():
    files = []
    for d in TARGETS:
        if os.path.isdir(d):
            files += [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith('.pdf')]
    if not files:
        sys.exit('no PDFs to audit -- run ./build.sh first')

    ok = True
    for f in files:
        lum, alp, img = audit(f)
        good = lum == 0 and alp == 0
        ok &= good
        print(f'{"PASS" if good else "FAIL"}  {os.path.basename(f)}')
        print(f'        luminosity masks {lum} | alpha groups {alp} | image alpha {img} (allowed)')
        if not good:
            print('        ^ a gradient-on-text, fading gradient or blurred shadow has '
                  'crept back in; it will render as a solid block in some viewers')

    print('\nOVERALL:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
