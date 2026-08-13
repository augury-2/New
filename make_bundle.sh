#!/usr/bin/env bash
#
# Bundles the finished Garh Kauthig 2026 deliverables into one archive, so the
# whole set can be fetched with a single download instead of file by file.
#
#   ./make_bundle.sh
#
# Only finished output goes in -- no sources, fonts or intermediates. The
# archive is verified after writing.
#
set -euo pipefail
cd "$(dirname "$0")"

INV=garh-kauthig-2026-invitations
ITN=garh-kauthig-2026-itinerary
OUT=Garh-Kauthig-2026-Deliverables.zip
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT

ROOT="$STAGE/Garh-Kauthig-2026"
mkdir -p "$ROOT"/{"1 - Invitations (JPG, print quality)","2 - Invitations (PDF, send to printer)","3 - Invitations (JPG, for WhatsApp)","4 - Programme"}

cp "$INV"/output/images/jpg-300dpi/*.jpg        "$ROOT/1 - Invitations (JPG, print quality)/"
cp "$INV"/output/print-ready/cmyk/*.pdf         "$ROOT/2 - Invitations (PDF, send to printer)/"
cp "$INV"/output/images/jpg-share/*.jpg         "$ROOT/3 - Invitations (JPG, for WhatsApp)/"
cp "$ITN"/garh-kauthig-2026-itinerary.docx      "$ROOT/4 - Programme/"
cp "$ITN"/garh-kauthig-2026-itinerary.pdf       "$ROOT/4 - Programme/"
cp "$INV"/output/preview/contact-sheet.jpg      "$ROOT/All seven invitations at a glance.jpg"

cat > "$ROOT/READ ME.txt" <<'TXT'
GARH KAUTHIG 2026
Graphic Era School of Management  x  Swaragini, The Cultural Society
Thursday, 13 August 2026, 01:00 PM onwards
Silver Jubilee Convention Centre, Graphic Era (Deemed to be University), Dehradun
Held as part of the EMERGE Induction Program 2026

WHAT IS IN HERE
---------------
1 - Invitations (JPG, print quality)
    Seven invitations, exactly A3 at 300 dpi (3508 x 4961 pixels), bleed already
    trimmed off. 300 dpi is written into each file, so Word, Canva and print
    software place them at A3 rather than guessing. Use these for anything that
    wants an image rather than a PDF.

2 - Invitations (PDF, send to printer)
    The same seven as print files: DeviceCMYK, 303 x 426 mm (A3 plus a 3 mm
    bleed on every edge), with the trim and bleed boxes set so the press needs
    no instructions. This is what the printer should get.
    Recommended stock: 300-350 gsm uncoated or textured natural white. The
    design already simulates a handmade paper surface, so a gloss coat fights it.

3 - Invitations (JPG, for WhatsApp)
    1400 pixels wide, about 400 KB each. For messaging and social, not printing.

4 - Programme
    The running order, in Word (editable - retype the times, rename the
    performances, move rows) and as a designed A4 PDF for circulating.

THE SEVEN INVITATIONS
---------------------
  01  Vice Chancellor
  02  Pro Vice Chancellor
  03  Registrar
  04  Faculty Members
  05  Research Scholars
  06  MBA 2025-27 Batch, Seniors
  07  MBA 2026-28 Batch, Freshers

TWO THINGS STILL OUTSTANDING
----------------------------
1. THE LOGOS. The header and footer currently set the university and EMERGE
   wording as type, matching the poster. The real logo artwork was never
   supplied, and institutional marks should not be redrawn by eye. Send the
   files (SVG preferred) and they drop straight in.

2. THE PROGRAMME TIMINGS. The poster gives a 01:00 PM start and nothing else,
   so no running times have been invented. The Word file lists the seven points
   the organisers' notes did not settle.

Nothing in this bundle contains invented event information. Every date, time,
venue and name comes from the supplied poster and notes.
TXT

rm -f "$OUT"
( cd "$STAGE" && zip -qr -9 "$OLDPWD/$OUT" "Garh-Kauthig-2026" -x '.*' )

echo "wrote $OUT  ($(du -h "$OUT" | cut -f1))"
unzip -t "$OUT" >/dev/null && echo "archive integrity: OK"
echo "contents:"
unzip -l "$OUT" | awk 'NR>3 && NF>3 {printf "  %8s  %s\n", $1, substr($0, index($0,$4))}' | head -40
n=$(unzip -l "$OUT" | tail -1 | awk '{print $2}')
echo "$n files total"
