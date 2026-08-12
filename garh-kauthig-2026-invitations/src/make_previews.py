#!/usr/bin/env python3
"""
Web-viewable previews of the Garh Kauthig 2026 invitation suite.

The 300 dpi masters are 13 MB apiece, which is no use for reviewing on GitHub or
in a browser. This writes a trimmed (bleed removed) JPEG of each letter at a
sensible screen size, plus a side-by-side contact sheet of all three.

Run after:  node src/render.mjs
"""

import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG_DIR = os.path.join(ROOT, 'output', 'png')
OUT = os.path.join(ROOT, 'output', 'preview')

BLEED_MM = 3.0
SHEET_W_MM = 303.0
PREVIEW_W = 1400          # px on the long edge of a single preview
CONTACT_W = 480           # px per panel in the contact sheet

LABELS = {
    '01-vice-chancellor': 'Vice Chancellor',
    '02-pro-vice-chancellor': 'Pro Vice Chancellor',
    '03-registrar': 'Registrar',
}


def trimmed(path):
    """Crop the 3 mm bleed away so the preview shows the sheet as it will be
    delivered after trimming."""
    im = Image.open(path).convert('RGB')
    px_per_mm = im.width / SHEET_W_MM
    b = round(BLEED_MM * px_per_mm)
    return im.crop((b, b, im.width - b, im.height - b))


def main():
    os.makedirs(OUT, exist_ok=True)
    names = sorted(f for f in os.listdir(PNG_DIR)
                   if f.endswith('.png') and f.startswith('garh-kauthig'))
    if not names:
        sys.exit('no renders found -- run: node src/render.mjs')

    panels = []
    for name in names:
        im = trimmed(os.path.join(PNG_DIR, name))
        h = round(PREVIEW_W * im.height / im.width)
        small = im.resize((PREVIEW_W, h), Image.LANCZOS)
        dst = os.path.join(OUT, name.replace('.png', '-preview.jpg'))
        small.save(dst, 'JPEG', quality=88, optimize=True, progressive=True)
        print(f'  {os.path.basename(dst)}  {small.width}x{small.height}  '
              f'{os.path.getsize(dst) / 1024:.0f} KB')

        ch = round(CONTACT_W * im.height / im.width)
        panels.append((im.resize((CONTACT_W, ch), Image.LANCZOS),
                       next((v for k, v in LABELS.items() if k in name), name)))

    # contact sheet
    pad, cap = 26, 34
    w = pad + sum(p.width + pad for p, _ in panels)
    h = pad + max(p.height for p, _ in panels) + cap + pad
    sheet = Image.new('RGB', (w, h), '#efe7d6')
    draw = ImageDraw.Draw(sheet)
    x = pad
    for p, label in panels:
        sheet.paste(p, (x, pad))
        draw.rectangle([x - 1, pad - 1, x + p.width, pad + p.height], outline='#b9a475')
        tw = draw.textlength(label)
        draw.text((x + (p.width - tw) / 2, pad + p.height + 12), label, fill='#5c3a18')
        x += p.width + pad
    dst = os.path.join(OUT, 'contact-sheet.jpg')
    sheet.save(dst, 'JPEG', quality=90, optimize=True)
    print(f'  contact-sheet.jpg  {sheet.width}x{sheet.height}  '
          f'{os.path.getsize(dst) / 1024:.0f} KB')


if __name__ == '__main__':
    main()
