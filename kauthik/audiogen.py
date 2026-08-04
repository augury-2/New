"""
KAUTHIK — Original ambient score
================================
Synthesises a seamless-looping instrumental bed evoking a hill fair:
a dhol/damau-style hand-drum pattern over a soft tanpura-like drone with
a distant flute motif.  Fully synthetic — royalty-free, no sampled music.

    python3 audiogen.py       # -> assets/score.m4a

NOT a reproduction of any specific folk song; an original atmospheric bed.
"""
from __future__ import annotations
import math, os, subprocess, struct, wave
import numpy as np

FFMPEG = "/projects/ffmpeg/bin/ffmpeg"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
SR = 44100
BPM = 92
BEAT = 60.0 / BPM
BARS = 8                       # loop length
BEATS = BARS * 4
DUR = BEATS * BEAT             # seconds, seamless loop


def _t(n):
    return np.arange(n) / SR


def drone(dur):
    """Low tanpura-like drone on the tonic + fifth, slow shimmer."""
    n = int(dur * SR); t = _t(n)
    base = 110.0                      # A2
    out = np.zeros(n)
    for f, a in ((base, 0.5), (base * 1.5, 0.32), (base * 2, 0.18),
                 (base * 3, 0.08)):
        det = 1 + 0.004 * math.sin(2 * math.pi * 0.07 * 1)
        out += a * np.sin(2 * math.pi * f * t)
        out += a * 0.5 * np.sin(2 * math.pi * f * det * t + 0.6)
    lfo = 0.75 + 0.25 * np.sin(2 * math.pi * (BARS and 1 / dur) * t)   # 1 cycle/loop
    return out * lfo * 0.16


def _drum(n_total, hits, kind):
    """Place membrane-drum hits (bass=dhol, tight=damau) at hit times."""
    out = np.zeros(n_total)
    for (tsec, amp) in hits:
        i0 = int(tsec * SR)
        if kind == "bass":
            dl = 0.34; f0, f1 = 150, 62
        else:                                    # tight kettle drum
            dl = 0.14; f0, f1 = 300, 150
        m = int(dl * SR)
        tt = _t(m)
        env = np.exp(-tt * (9 if kind == "bass" else 20))
        pitch = f1 + (f0 - f1) * np.exp(-tt * 26)
        body = np.sin(2 * math.pi * np.cumsum(pitch) / SR)
        noise = (np.random.RandomState(i0 % 9999).randn(m)
                 * np.exp(-tt * (30 if kind == "bass" else 55)))
        seg = (body * 0.8 + noise * 0.4) * env * amp
        i1 = min(n_total, i0 + m)
        out[i0:i1] += seg[:i1 - i0]
    return out


def percussion(dur):
    n = int(dur * SR)
    bass, tight = [], []
    # a rolling 4/4 fair groove; slight swing, accents on 1 and 3
    for b in range(BEATS):
        tb = b * BEAT
        acc = 1.0 if b % 4 in (0, 2) else 0.7
        bass.append((tb, 0.9 * acc))
        tight.append((tb + BEAT * 0.5, 0.5))           # off-beat damau
        if b % 4 == 3:
            tight.append((tb + BEAT * 0.75, 0.42))      # pickup fill
            bass.append((tb + BEAT * 0.5, 0.5))
    b = _drum(n, bass, "bass")
    d = _drum(n, tight, "tight")
    return b * 0.5 + d * 0.4


def flute(dur):
    """Sparse, breathy pentatonic motif far back in the mix."""
    n = int(dur * SR); out = np.zeros(n)
    scale = [0, 2, 4, 7, 9]           # major pentatonic
    root = 440.0
    rs = np.random.RandomState(3)
    notes = [(0, 7, 2.0), (2.5, 9, 1.2), (4.0, 4, 1.6), (6.5, 2, 1.4),
             (9.0, 7, 2.2), (12.0, 9, 1.0), (14.0, 4, 3.0)]
    for (tsec, semi, ln) in notes:
        if tsec >= dur:
            continue
        f = root * 2 ** (semi / 12.0)
        m = int(min(ln, dur - tsec) * SR); tt = _t(m)
        env = np.minimum(1, tt * 6) * np.exp(-tt * 1.1)
        vib = 1 + 0.006 * np.sin(2 * math.pi * 5 * tt)
        tone = (np.sin(2 * math.pi * f * tt * vib)
                + 0.15 * np.sin(2 * math.pi * 2 * f * tt))
        i0 = int(tsec * SR)
        out[i0:i0 + m] += tone * env * 0.10
    return out


def crossfade_seam(x, ms=120):
    """Wrap the tail into the head so the loop point is inaudible."""
    k = int(SR * ms / 1000)
    head = x[:k].copy()
    x[:k] = x[:k] * np.linspace(0, 1, k) + x[-k:] * np.linspace(1, 0, k)
    x[-k:] = x[-k:] * np.linspace(1, 0, k) + head * np.linspace(0, 1, k)
    return x


def render():
    np.random.seed(11)
    mix = drone(DUR) + percussion(DUR) + flute(DUR)
    mix = crossfade_seam(mix)
    peak = np.max(np.abs(mix)) + 1e-9
    mix = (mix / peak) * 0.89
    # gentle stereo width
    left = mix.copy(); right = mix.copy()
    right[100:] = mix[:-100] * 0.96
    stereo = np.stack([left, right], axis=1)
    pcm = (stereo * 32767).astype(np.int16)

    wav_path = os.path.join(HERE, "_score.wav")
    with wave.open(wav_path, "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())

    out = os.path.join(ASSETS, "score.m4a")
    subprocess.run([FFMPEG, "-y", "-i", wav_path, "-c:a", "aac", "-b:a",
                    "128k", out], check=True, capture_output=True)
    os.remove(wav_path)
    return out


if __name__ == "__main__":
    out = render()
    sz = os.path.getsize(out) / 1e6
    print(f"saved {out}  ({sz:.2f} MB, {DUR:.1f}s seamless loop @ {BPM} BPM)")
