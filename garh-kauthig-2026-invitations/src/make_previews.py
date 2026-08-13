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
    '04-faculty-members': 'Faculty Members',
    '05-research-scholars': 'Research Scholars',
    '06-mba-seniors-2025-27': 'MBA 2025-27 Seniors',
    '07-mba-freshers-2026-28': 'MBA 2026-28 Freshers',
}
PER_ROW = 4


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

    # contact sheet, wrapped so seven panels stay legible
    pad, cap = 26, 34
    pw = panels[0][0].width
    ph = max(p.height for p, _ in panels)
    rows = (len(panels) + PER_ROW - 1) // PER_ROW
    cols = min(len(panels), PER_ROW)
    w = pad + cols * (pw + pad)
    h = pad + rows * (ph + cap + pad)
    sheet = Image.new('RGB', (w, h), '#efe7d6')
    draw = ImageDraw.Draw(sheet)
    for i, (p, label) in enumerate(panels):
        r, c = divmod(i, PER_ROW)
        x = pad + c * (pw + pad)
        y = pad + r * (ph + cap + pad)
        sheet.paste(p, (x, y))
        draw.rectangle([x - 1, y - 1, x + p.width, y + p.height], outline='#b9a475')
        tw = draw.textlength(label)
        draw.text((x + (p.width - tw) / 2, y + p.height + 12), label, fill='#5c3a18')
    dst = os.path.join(OUT, 'contact-sheet.jpg')
    sheet.save(dst, 'JPEG', quality=90, optimize=True)
    print(f'  contact-sheet.jpg  {sheet.width}x{sheet.height}  '
          f'{os.path.getsize(dst) / 1024:.0f} KB')


if __name__ == '__main__':
    main()
