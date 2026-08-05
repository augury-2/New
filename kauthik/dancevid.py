"""
GARH KAUTHIG — Real-photo dance montage
=======================================
Builds a cinematic Ken-Burns montage (montage.mp4) from the club's own event
photographs, crossfaded and set to the original dhol-damau score. Embedded as
a looping background on the showcase slide.

Run:  python3 dancevid.py
Requires ffmpeg (found at /projects/ffmpeg/bin or on PATH).
"""
from __future__ import annotations
import os, shutil, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "photos")
ASSETS = os.path.join(HERE, "assets")

FFMPEG = next((p for p in ("/projects/ffmpeg/bin/ffmpeg",
                           shutil.which("ffmpeg")) if p and os.path.exists(p)),
              "ffmpeg")

FPS = 30
DUR = 4.7          # seconds per photo
XF = 0.8           # crossfade seconds
W, H = 1280, 720

# (file, ken-burns mode)  — dance first, official poster to close
SEQ = [
    ("cover2.jpg", "in"),    # colourful group dance (twirling scarves)
    ("cover1.jpg", "out"),   # Garhwali group dance under KAUTHIG banner
    ("cover3.jpg", "in"),    # colourful group dance
    ("cover4.jpg", "out"),   # official KAUTHIG cultural-competition poster
]
TRANS = ["fade", "smoothleft", "dissolve"]


def _run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("ffmpeg failed:\n" + " ".join(cmd) + "\n" +
                           r.stderr[-2500:])
    return r


def _kenburns_clip(src, mode, out):
    frames = int(round(DUR * FPS))
    if mode == "in":
        z = "1.0+0.24*on/%d" % frames
    else:
        z = "1.24-0.24*on/%d" % frames
    vf = (
        "scale=1920:1080:force_original_aspect_ratio=increase,"
        "crop=1920:1080,setsar=1,"
        "zoompan=z='%s':d=%d:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        "fps=%d:s=%dx%d,format=yuv420p" % (z, frames, FPS, W, H)
    )
    _run([FFMPEG, "-y", "-loop", "1", "-i", src, "-t", "%.3f" % DUR,
          "-filter_complex", vf, "-c:v", "libx264", "-preset", "medium",
          "-crf", "20", "-r", str(FPS), out])


def build():
    tmp = tempfile.mkdtemp(prefix="kb_")
    clips = []
    for i, (fn, mode) in enumerate(SEQ):
        src = os.path.join(PHOTOS, fn)
        if not os.path.exists(src):
            raise FileNotFoundError(src)
        c = os.path.join(tmp, "clip%d.mp4" % i)
        _kenburns_clip(src, mode, c)
        clips.append(c)

    n = len(clips)
    total = n * DUR - (n - 1) * XF
    # crossfade chain
    parts, prev = [], "0"
    for i in range(1, n):
        offset = i * DUR - i * XF
        tr = TRANS[(i - 1) % len(TRANS)]
        label = "v" if i == n - 1 else "x%d" % i
        parts.append("[%s][%d]xfade=transition=%s:duration=%.3f:offset=%.3f[%s]"
                     % (prev, i, tr, XF, offset, label))
        prev = label
    fc = ";".join(parts)

    out = os.path.join(ASSETS, "montage.mp4")
    cmd = [FFMPEG, "-y"]
    for c in clips:
        cmd += ["-i", c]
    cmd += ["-stream_loop", "-1", "-i", os.path.join(ASSETS, "score.m4a")]
    cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "%d:a" % n,
            "-t", "%.3f" % total, "-c:v", "libx264", "-preset", "medium",
            "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "160k", "-shortest",
            "-movflags", "+faststart", out]
    _run(cmd)

    # poster frame (first frame of the montage)
    poster = os.path.join(ASSETS, "montage_poster.jpg")
    _run([FFMPEG, "-y", "-i", out, "-frames:v", "1", "-q:v", "3", poster])

    shutil.rmtree(tmp, ignore_errors=True)
    print("saved %s  (%.1fs, %.1f MB)  + poster"
          % (out, total, os.path.getsize(out) / 1e6))


if __name__ == "__main__":
    build()
