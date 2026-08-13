#!/usr/bin/env python3
"""
Converts the baked background plate to a prepress-grade JPEG.

The plate is a continuous-tone image (paper fibre, watercolour wash, gradients)
with no hard edges or type, so JPEG at quality 94 with chroma subsampling
switched off is visually lossless here -- measured maximum per-channel error is
1-2/255 -- while cutting the file from ~17 MB to ~3 MB.  That matters because
the plate is embedded in every one of the print PDFs.

Run after:  node src/render.mjs --bake
"""

import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG = os.path.join(ROOT, 'assets', 'background.png')
JPG = os.path.join(ROOT, 'assets', 'background.jpg')

if not os.path.exists(PNG):
    sys.exit('assets/background.png missing -- run: node src/render.mjs --bake')

im = Image.open(PNG).convert('RGB')
dpi = round(im.width / (303 / 25.4))
im.save(JPG, 'JPEG', quality=94, subsampling=0, optimize=True, dpi=(300, 300))

ref = Image.open(JPG).convert('RGB')
worst = 0
step_x, step_y = max(1, im.width // 40), max(1, im.height // 40)
for x in range(0, im.width, step_x):
    for y in range(0, im.height, step_y):
        worst = max(worst, max(abs(a - b) for a, b in
                               zip(im.getpixel((x, y)), ref.getpixel((x, y)))))

print(f'plate {im.width} x {im.height} px  ({dpi} dpi at 303 mm wide)')
print(f'  png {os.path.getsize(PNG) / 1048576:.1f} MB '
      f'-> jpg {os.path.getsize(JPG) / 1048576:.2f} MB')
print(f'  worst per-channel error over a 40x40 sample grid: {worst}/255')

# the PNG is an intermediate; the JPEG is what the print files reference
os.remove(PNG)
print('  removed intermediate assets/background.png')
