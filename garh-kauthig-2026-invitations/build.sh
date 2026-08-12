#!/usr/bin/env bash
#
# Full build for the Garh Kauthig 2026 A3 invitation suite.
#
#   ./build.sh            rebuild everything from source
#   ./build.sh --quick    skip regenerating textures / ornaments / background
#
# Produces, in output/:
#   html/                      the editable source pages
#   pdf/                       vector PDFs, 303 x 426 mm (A3 + 3 mm bleed)
#   png/                       300 dpi rasters
#   print-ready/rgb/           RGB masters with TrimBox + BleedBox set
#   print-ready/cmyk/          DeviceCMYK conversions
#   print-ready/with-crop-marks/  CMYK plus crop marks and a tint strip
#
set -euo pipefail
cd "$(dirname "$0")"

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
# shellcheck disable=SC1091
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && nvm use 22 >/dev/null 2>&1 || true

QUICK=${1:-}

if [ "$QUICK" != "--quick" ]; then
  echo "==> paper + foil textures"
  python3 src/make_textures.py
  echo "==> ornament library"
  python3 src/make_ornaments.py
fi

echo "==> compose pages"
node src/build.mjs

if [ "$QUICK" != "--quick" ]; then
  echo "==> bake background plate (300 dpi)"
  node src/render.mjs --bake
  python3 src/plate_to_jpeg.py
  # the pages must be recomposed only if the plate filename changed; it does not,
  # so no rebuild is needed here.
fi

echo "==> render PDF + PNG"
node src/render.mjs

echo "==> prepress (trim/bleed boxes, CMYK, crop marks)"
python3 src/prepress.py

echo "==> audit: no fragile soft-mask constructs"
python3 src/check_softmask.py

echo "==> colour-managed CMYK rasters"
python3 src/make_cmyk_tiff.py

echo "==> web previews"
python3 src/make_previews.py

echo
echo "Done. Deliverables are in output/print-ready/"
