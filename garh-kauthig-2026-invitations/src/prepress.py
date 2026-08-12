#!/usr/bin/env python3
"""
Prepress finishing for the Garh Kauthig 2026 invitation suite.

Takes the vector PDFs that Chromium produced (output/pdf/*.pdf) and, for each:

  1. writes an RGB print master with correct /TrimBox and /BleedBox, so a
     printer's RIP knows where A3 ends and the 3 mm bleed begins;
  2. writes a DeviceCMYK conversion via Ghostscript for offset/digital presses
     that require CMYK on delivery;
  3. writes a proofing copy carrying crop marks and a colour/registration
     strip in an added 8 mm slug.

Everything is verified afterwards and the findings printed, because "the
command exited 0" is not evidence that a print file is correct.

Usage:  python3 src/prepress.py
"""

import os
import shutil
import subprocess
import sys

import pikepdf
from pikepdf import Array, Dictionary, Name

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'output', 'pdf')
OUT_RGB = os.path.join(ROOT, 'output', 'print-ready', 'rgb')
OUT_CMYK = os.path.join(ROOT, 'output', 'print-ready', 'cmyk')
OUT_MARKS = os.path.join(ROOT, 'output', 'print-ready', 'with-crop-marks')

MM = 72.0 / 25.4          # points per millimetre
BLEED_MM = 3.0
TRIM_W_MM, TRIM_H_MM = 297.0, 420.0
SLUG_MM = 8.0             # extra paper for crop marks on the proofing copy


def trim_box_for(page):
    """Compute the exact A3 trim rectangle inside a bleed-sized MediaBox.

    The layout places the trim area 3 mm from the top-left of the sheet (CSS
    lays out downward from the top), so the box is derived from that corner
    rather than by assuming the trim is perfectly centred -- Chromium rounds
    the media height up by a fraction of a point.
    """
    mb = [float(v) for v in page.MediaBox]
    media_w = mb[2] - mb[0]
    media_h = mb[3] - mb[1]
    tw, th = TRIM_W_MM * MM, TRIM_H_MM * MM
    left = mb[0] + BLEED_MM * MM
    top = mb[1] + media_h - BLEED_MM * MM     # PDF y grows upward
    return [left, top - th, left + tw, top], media_w, media_h


def finish_rgb(src, dst):
    with pikepdf.open(src) as pdf:
        page = pdf.pages[0]
        tb, mw, mh = trim_box_for(page)
        page.TrimBox = Array(tb)
        page.BleedBox = Array([float(v) for v in page.MediaBox])
        page.ArtBox = Array(tb)
        pdf.save(dst, linearize=True)
    return tb, mw, mh


def finish_cmyk(src, dst):
    """DeviceCMYK conversion. Ghostscript flattens the transparency groups used
    by the paper-texture layers, which is exactly what a prepress RIP does."""
    cmd = [
        'gs', '-dBATCH', '-dNOPAUSE', '-dQUIET', '-dSAFER',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.6',
        '-sColorConversionStrategy=CMYK',
        '-dProcessColorModel=/DeviceCMYK',
        '-dOverrideICC=true',
        '-dAutoRotatePages=/None',
        '-dEmbedAllFonts=true', '-dSubsetFonts=true',
        # keep every raster at full 300 dpi -- no downsampling of the paper
        # plate -- but re-encode it as high-quality DCT rather than Flate, which
        # would triple the delivered file size for no visible gain on a
        # continuous-tone texture
        '-dDownsampleColorImages=false', '-dDownsampleGrayImages=false',
        '-dDownsampleMonoImages=false',
        '-dAutoFilterColorImages=false', '-dAutoFilterGrayImages=false',
        '-dColorImageFilter=/DCTEncode', '-dGrayImageFilter=/DCTEncode',
        '-dJPEGQ=95',
        '-dColorImageResolution=300', '-dGrayImageResolution=300',
        '-dColorConversionStrategyForImages=/DeviceCMYK',
        '-dPreserveOverprintSettings=true',
        f'-sOutputFile={dst}', src,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f'ghostscript failed on {src}:\n{r.stderr[:2000]}')
    # re-stamp the boxes: pdfwrite does not carry TrimBox/BleedBox across
    with pikepdf.open(dst, allow_overwriting_input=True) as pdf:
        page = pdf.pages[0]
        tb, _, _ = trim_box_for(page)
        page.TrimBox = Array(tb)
        page.BleedBox = Array([float(v) for v in page.MediaBox])
        page.ArtBox = Array(tb)
        pdf.save(dst + '.tmp', linearize=True)
    shutil.move(dst + '.tmp', dst)


def add_crop_marks(src, dst):
    """Place the bleed-size page onto a slightly larger sheet and draw crop
    marks, a registration target and a tint strip in the slug."""
    with pikepdf.open(src) as pdf:
        page = pdf.pages[0]
        mb = [float(v) for v in page.MediaBox]
        media_w, media_h = mb[2] - mb[0], mb[3] - mb[1]
        slug = SLUG_MM * MM
        new_w, new_h = media_w + 2 * slug, media_h + 2 * slug

        # 1. re-home the existing content inside the enlarged sheet
        page.add_underlay(page, rect=pikepdf.Rectangle(
            slug, slug, slug + media_w, slug + media_h))
        page.MediaBox = Array([0, 0, new_w, new_h])

        tb, _, _ = trim_box_for_shifted(mb, media_w, media_h, slug)
        page.TrimBox = Array(tb)
        page.BleedBox = Array([slug, slug, slug + media_w, slug + media_h])

        # 2. marks, drawn in registration black (all four plates)
        x0, y0, x1, y1 = tb
        gap, length = 3.0 * MM, 5.0 * MM
        ops = ['q', '0.4 w', '0 0 0 1 K', '0 0 0 RG']
        for (px, py, dx, dy) in (
            (x0, y0, -1, 0), (x0, y0, 0, -1), (x1, y0, 1, 0), (x1, y0, 0, -1),
            (x0, y1, -1, 0), (x0, y1, 0, 1), (x1, y1, 1, 0), (x1, y1, 0, 1),
        ):
            sx, sy = px + dx * gap, py + dy * gap
            ops.append(f'{sx:.3f} {sy:.3f} m {sx + dx * length:.3f} {sy + dy * length:.3f} l S')

        # registration target, centred in the head slug
        cx, cy, r = new_w / 2, new_h - slug / 2, 2.2 * MM
        ops += [f'{cx - r:.3f} {cy:.3f} m {cx + r:.3f} {cy:.3f} l S',
                f'{cx:.3f} {cy - r:.3f} m {cx:.3f} {cy + r:.3f} l S',
                f'{cx:.3f} {cy:.3f} m {cx + r * 0.62:.3f} {cy:.3f} l '
                f'{cx + r * 0.62:.3f} {cy:.3f} {r * 0.62:.3f} 0 360 re S']

        # process tint strip along the foot slug
        patches = [(0, 0, 0, 1), (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0),
                   (0, 0, 0, 0.5), (0.4, 0.3, 0.3, 0), (0, 0, 0, 0.25)]
        pw, ph = 8.0 * MM, 3.2 * MM
        bx = new_w / 2 - (len(patches) * pw) / 2
        for i, (c, m, y, k) in enumerate(patches):
            ops.append(f'{c} {m} {y} {k} k '
                       f'{bx + i * pw:.3f} {slug / 2 - ph / 2:.3f} {pw:.3f} {ph:.3f} re f')
        ops.append('Q')

        page.contents_add(pikepdf.Stream(pdf, '\n'.join(ops).encode()), prepend=False)
        pdf.save(dst, linearize=True)


def trim_box_for_shifted(mb, media_w, media_h, slug):
    tw, th = TRIM_W_MM * MM, TRIM_H_MM * MM
    left = slug + BLEED_MM * MM
    top = slug + media_h - BLEED_MM * MM
    return [left, top - th, left + tw, top], media_w, media_h


def verify(path, expect_cmyk):
    """Report what is actually in the file rather than trusting the exit code."""
    with pikepdf.open(path) as pdf:
        page = pdf.pages[0]
        def box(n):
            if n not in page:
                return None
            b = [float(v) for v in page[n]]
            return (round((b[2] - b[0]) / MM, 2), round((b[3] - b[1]) / MM, 2))
        info = {
            'pages': len(pdf.pages),
            'media_mm': box('/MediaBox'),
            'trim_mm': box('/TrimBox'),
            'bleed_mm': box('/BleedBox'),
        }
    raw = open(path, 'rb').read()
    info['DeviceRGB'] = raw.count(b'/DeviceRGB')
    info['DeviceCMYK'] = raw.count(b'/DeviceCMYK')
    info['fonts'] = len(set(__import__('re').findall(rb'/FontName\s*/([A-Za-z0-9+\-]+)', raw)))
    info['size_mb'] = round(len(raw) / 1048576, 2)
    ok = (info['pages'] == 1
          and info['media_mm'] and abs(info['media_mm'][0] - 303) < 0.3
          and abs(info['media_mm'][1] - 426) < 0.3
          and info['trim_mm'] and abs(info['trim_mm'][0] - 297) < 0.1
          and abs(info['trim_mm'][1] - 420) < 0.1)
    if expect_cmyk:
        ok = ok and info['DeviceCMYK'] > 0
    info['PASS'] = ok
    return info


def main():
    for d in (OUT_RGB, OUT_CMYK, OUT_MARKS):
        os.makedirs(d, exist_ok=True)
    names = sorted(f for f in os.listdir(SRC) if f.endswith('.pdf'))
    if not names:
        sys.exit('no source PDFs -- run `node src/render.mjs` first')

    all_ok = True
    for name in names:
        src = os.path.join(SRC, name)
        print(f'\n=== {name}')
        rgb = os.path.join(OUT_RGB, name.replace('.pdf', '-RGB-A3-bleed.pdf'))
        finish_rgb(src, rgb)
        v = verify(rgb, expect_cmyk=False)
        print('  RGB       ', v)
        all_ok &= v['PASS']

        cmyk = os.path.join(OUT_CMYK, name.replace('.pdf', '-CMYK-A3-bleed.pdf'))
        finish_cmyk(rgb, cmyk)
        v = verify(cmyk, expect_cmyk=True)
        print('  CMYK      ', v)
        all_ok &= v['PASS']

        marks = os.path.join(OUT_MARKS, name.replace('.pdf', '-CMYK-cropmarks.pdf'))
        add_crop_marks(cmyk, marks)
        with pikepdf.open(marks) as pdf:
            mb = [float(x) for x in pdf.pages[0].MediaBox]
            tb = [float(x) for x in pdf.pages[0].TrimBox]
        print('  CROP MARKS media %.1f x %.1f mm | trim %.1f x %.1f mm'
              % ((mb[2] - mb[0]) / MM, (mb[3] - mb[1]) / MM,
                 (tb[2] - tb[0]) / MM, (tb[3] - tb[1]) / MM))

    print('\nOVERALL:', 'PASS' if all_ok else 'FAIL')
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
