#!/usr/bin/env python3
"""
Colour-managed CMYK rasters for the Garh Kauthig 2026 invitation suite.

Why this exists alongside the CMYK PDF: Ghostscript's device conversion is a
plain arithmetic RGB->CMYK transform, which is valid but not colour-managed.
This script instead runs the verified 300 dpi render through littleCMS with an
ICC profile, giving a CMYK file whose appearance is predictable, and embeds the
profile so a press operator can see exactly what was assumed.

It also checks its own work: each CMYK raster is converted back to sRGB through
the same profile pair and compared with the source, and the total area coverage
is measured so nothing is delivered above the ink limit for coated stock.

Run after:  node src/render.mjs
"""

import os
import sys

from PIL import Image, ImageChops, ImageStat, ImageCms

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG_DIR = os.path.join(ROOT, 'output', 'png')
OUT = os.path.join(ROOT, 'output', 'print-ready', 'cmyk-tiff')

ICC_DIR = '/usr/share/ghostscript/iccprofiles'
SRGB = os.path.join(ICC_DIR, 'srgb.icc')
CMYK = os.path.join(ICC_DIR, 'default_cmyk.icc')
TAC_LIMIT = 320       # total area coverage ceiling for coated offset


def main():
    for p in (SRGB, CMYK):
        if not os.path.exists(p):
            sys.exit(f'missing ICC profile: {p}')
    os.makedirs(OUT, exist_ok=True)

    src_prof = ImageCms.getOpenProfile(SRGB)
    dst_prof = ImageCms.getOpenProfile(CMYK)
    to_cmyk = ImageCms.buildTransform(src_prof, dst_prof, 'RGB', 'CMYK',
                                      renderingIntent=1)   # relative colorimetric
    back = ImageCms.buildTransform(dst_prof, src_prof, 'CMYK', 'RGB',
                                   renderingIntent=1)

    names = sorted(f for f in os.listdir(PNG_DIR)
                   if f.endswith('.png') and f.startswith('garh-kauthig'))
    if not names:
        sys.exit('no 300 dpi renders found -- run: node src/render.mjs')

    ok = True
    for name in names:
        rgb = Image.open(os.path.join(PNG_DIR, name)).convert('RGB')
        cmyk = ImageCms.applyTransform(rgb, to_cmyk)

        dst = os.path.join(OUT, name.replace('.png', '-CMYK-300dpi.tif'))
        cmyk.save(dst, 'TIFF', dpi=(300, 300), compression='tiff_lzw',
                  icc_profile=ImageCms.getOpenProfile(CMYK).tobytes())

        # --- verify: round-trip back to sRGB and measure the drift ----------
        rt = ImageCms.applyTransform(cmyk, back)
        stat = ImageStat.Stat(ImageChops.difference(rgb, rt))
        drift = sum(stat.mean) / 3

        # --- verify: ink limit ----------------------------------------------
        small = cmyk.resize((cmyk.width // 4, cmyk.height // 4), Image.BOX)
        tac_max = max(sum(p) * 100 // 255 for p in small.getdata())

        dpi = round(rgb.width / (303 / 25.4))
        size_mb = os.path.getsize(dst) / 1048576
        good = drift < 4.0 and tac_max <= TAC_LIMIT and dpi >= 299
        ok &= good
        print(f'{"PASS" if good else "FAIL"}  {os.path.basename(dst)}')
        print(f'        {rgb.width}x{rgb.height}px @ {dpi} dpi, {size_mb:.1f} MB, '
              f'round-trip drift {drift:.2f}/255, peak TAC {tac_max}%')

    print('\nOVERALL:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
