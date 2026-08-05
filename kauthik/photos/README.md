# Your event photos go here

The deck (`event.py` → `GarhKauthig.pptx`) automatically uses a real photo if a
file with the matching name exists in this `photos/` folder. If a file is
missing, a labelled vibrant placeholder frame is shown instead — so the deck
always builds and looks intentional.

**I cannot pull images you attach in chat into the build.** Please add the
image files here (commit/push them to this branch, or drop them into the
workspace), then I'll rebuild and they slot straight in — and I'll also build a
Ken-Burns montage video from them, set to the dhol-damau track.

## File names the deck looks for

| Filename          | Where it appears                         | Best orientation |
|-------------------|------------------------------------------|------------------|
| `cover1.jpg` … `cover5.jpg` | Cover collage strip (5 small tiles) | landscape/square |
| `represents.jpg`  | "Garh Kauthig represents" — big right image | portrait/tall  |
| `where1.jpg` … `where5.jpg` | "Where celebrated" — 5 occasion tiles | landscape      |
| `team1.jpg`       | "Who will guide you" — Team DevBhoomi    | portrait         |
| `team2.jpg`       | "Who will guide you" — Team Uttarayani   | portrait         |
| `team3.jpg`       | "Who will guide you" — wide performance shot | landscape    |

- `.jpg`, `.jpeg` or `.png` all work (rename to the exact base name above).
- Any resolution is fine; higher is better. Images are placed into fixed boxes.
- If you'd rather I map your specific photos to specific slots, just tell me
  which photo goes where and I'll wire them by name.

## Optional: your own audio / video
- Drop `score_custom.m4a` (or `.mp3`) here to use YOUR track instead of the
  synthesised dhol-damau score.
- Drop short clips as `clip1.mp4`, `clip2.mp4`, … and I'll assemble a real
  video montage.
