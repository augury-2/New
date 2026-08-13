#!/usr/bin/env python3
"""
Flat image versions of the Garh Kauthig 2026 invitations.

The PDFs remain the master files, but images are what actually get shared on
WhatsApp, dropped into a slide, or handed to a local press that would rather
have a JPEG than a PDF.  Three sets are written:

  output/images/jpg-300dpi/   print quality, trimmed A3, ~4 MB each
  output/images/jpg-share/    1400 px wide, under 600 KB, for messaging
  output/images/png-300dpi/   lossless, trimmed A3, ~12 MB each -- only with
                              --with-png, because these are slow to write and
                              far too large to keep in the repository

JPEG is written at quality 95 with chroma subsampling switched off, which on
this artwork is visually indistinguishable from the lossless PNG at a third of
the size.

The 3 mm bleed is cropped off: bleed only exists so a printer can trim through
it, and on a flat image it would show as a 3 mm band of background outside the
intended edge.  Physical resolution is written into the file metadata, so
Word, Canva and print software place the image at A3 rather than guessing.

Run after:  node src/render.mjs
"""

import os
import sys

from PIL import Image, ImageChops, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'output', 'png')
OUT = os.path.join(ROOT, 'output', 'images')

SHEET_W_MM = 303.0          # rendered sheet: A3 plus 3 mm bleed all round
BLEED_MM = 3.0
TRIM_W_MM, TRIM_H_MM = 297.0, 420.0
DPI = 300
SHARE_W = 1400
WITH_PNG = '--with-png' in sys.argv


def expected_px(mm, dpi=DPI):
    return round(mm / 25.4 * dpi)


def main():
    subs = ['jpg-300dpi', 'jpg-share'] + (['png-300dpi'] if WITH_PNG else [])
    for sub in subs:
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)

    names = sorted(f for f in os.listdir(SRC)
                   if f.endswith('.png') and f.startswith('garh-kauthig'))
    if not names:
        sys.exit('no renders found -- run: node src/render.mjs')

    ok = True
    for name in names:
        im = Image.open(os.path.join(SRC, name)).convert('RGB')
        px_per_mm = im.width / SHEET_W_MM
        b = round(BLEED_MM * px_per_mm)
        trimmed = im.crop((b, b, im.width - b, im.height - b))

        want_w, want_h = expected_px(TRIM_W_MM), expected_px(TRIM_H_MM)
        # allow a pixel of rounding either way
        good = abs(trimmed.width - want_w) <= 2 and abs(trimmed.height - want_h) <= 2
        ok &= good

        stem = name[:-4]
        jpg = os.path.join(OUT, 'jpg-300dpi', f'{stem}-A3-300dpi.jpg')
        png = os.path.join(OUT, 'png-300dpi', f'{stem}-A3-300dpi.png')
        trimmed.save(jpg, 'JPEG', quality=95, subsampling=0, optimize=True,
                     progressive=True, dpi=(DPI, DPI))
        if WITH_PNG:
            trimmed.save(png, 'PNG', compress_level=6, dpi=(DPI, DPI))

        share = trimmed.resize(
            (SHARE_W, round(SHARE_W * trimmed.height / trimmed.width)), Image.LANCZOS)
        shr = os.path.join(OUT, 'jpg-share', f'{stem}-share.jpg')
        share.save(shr, 'JPEG', quality=86, optimize=True, progressive=True)

        print(f'{"PASS" if good else "FAIL"}  {stem}')
        print(f'        trimmed {trimmed.width}x{trimmed.height} px '
              f'(A3 at {DPI} dpi = {want_w}x{want_h})')
        # how far the JPEG strays from the source, sampled on a grid
        with Image.open(jpg) as back:
            step = max(1, trimmed.width // 60)
            worst = 0
            for x in range(0, trimmed.width, step):
                for y in range(0, trimmed.height, step):
                    worst = max(worst, max(abs(a - b) for a, b in
                                zip(trimmed.getpixel((x, y)), back.getpixel((x, y)))))
        written = [jpg, shr] + ([png] if WITH_PNG else [])
        for f in written:
            print(f'        {os.path.basename(os.path.dirname(f)):11s} '
                  f'{os.path.getsize(f) / 1048576:6.2f} MB  {os.path.basename(f)}')
        print(f'        jpeg worst per-channel error vs source: {worst}/255')

    # confirm the DPI tag actually survived the write
    probe = os.path.join(OUT, 'jpg-300dpi', sorted(os.listdir(os.path.join(OUT, 'jpg-300dpi')))[0])
    with Image.open(probe) as p:
        tagged = p.info.get('dpi')
        mm_w = round(p.width / (tagged[0] / 25.4)) if tagged else None
    print(f'\nmetadata check: {os.path.basename(probe)} reports {tagged} dpi '
          f'-> places at {mm_w} mm wide')
    ok &= bool(tagged) and abs(mm_w - TRIM_W_MM) <= 1

    print('OVERALL:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
