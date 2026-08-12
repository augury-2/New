# Drop official logo artwork here

No institutional emblem is drawn anywhere in this project. Until real artwork is
supplied, the header and footer set the marks **as type, using the poster's exact
wording**.

To swap in the real logos, save files with these exact stems — any of `.svg`,
`.png` or `.jpg` — and rebuild. Nothing else needs editing; `src/build.mjs`
detects them and replaces the type lockup with an `<img>`.

| File stem | Replaces | Position | Rendered height |
|---|---|---|---|
| `geu` | Graphic Era, deemed to be University, Dehradun | header, left | 19 mm |
| `emerge` | EMERGE / Discover. Connect. Excel. / Induction Program 2026 | header, right | 19 mm |
| `gesm` | Graphic Era School of Management | footer, left | 13 mm |
| `swaragini` | Swaragini, The Cultural Society of Graphic Era University | footer, right | 13 mm |

For example: `geu.svg`, `emerge.png`.

```bash
./build.sh --quick
```

**Prefer SVG.** These print at A3, so vector art stays crisp at any size. If only
raster is available, supply at least 300 dpi at the rendered height — roughly
2250 px wide for a header mark. Artwork cropped out of the poster JPEG will look
soft in print.

Transparent backgrounds (SVG or PNG with alpha) sit correctly on the ivory paper.
A logo on a solid white or cream rectangle will show as a visible patch.
