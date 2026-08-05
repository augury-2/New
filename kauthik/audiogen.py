"""
KAUTHIK — Original dhol-damau folk score
========================================
A lively, festive instrumental bed in the Garhwali *dhol-damau* idiom:

  - DHOL      big double-headed drum — deep bass stroke ("dhaa") + sharp
              rim/treble stroke ("na")
  - DAMAU     small copper kettledrum — tight, bright, fast subdivisions
  - MASAKBEEN reed bagpipe — a continuous tonic drone + a simple, catchy
              Garhwali-style pentatonic melody
  - RANSINGHA long curved horn — low brass swells at phrase turns

Everything is synthesised from scratch (no samples, no copyrighted song), so it
is royalty-free and safe to present.  It is an *original instrumental in the
folk style*, not a reproduction of any particular recording.

    python3 audiogen.py        # -> assets/score.m4a
"""
from __future__ import annotations
import math, os, subprocess, wave
import numpy as np

FFMPEG = "/projects/ffmpeg/bin/ffmpeg"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
SR = 44100

BPM = 116
BEAT = 60.0 / BPM
BARS = 8                      # seamless loop length
STEPS = 16                    # 16th-note grid per bar
STEP = BEAT / 4
N_STEPS = BARS * STEPS
DUR = N_STEPS * STEP
TAU = 2 * math.pi
TONIC = 146.83                # D3 tonic for the whole piece


# ----------------------------------------------------------------- helpers ---
def _env(n, attack, decay, sr=SR, exp=True):
    t = np.arange(n) / sr
    a = int(attack * sr)
    e = np.ones(n)
    if a > 0:
        e[:a] = np.linspace(0, 1, a)
    if exp:
        e *= np.exp(-t / max(decay, 1e-4))
    return e


def _place(buf, sig, at_sec, gain=1.0):
    i0 = int(at_sec * SR)
    if i0 < 0:                      # clip a leading transient landing before t=0
        sig = sig[-i0:]
        i0 = 0
    if i0 >= len(buf) or len(sig) == 0:
        return
    i1 = min(len(buf), i0 + len(sig))
    buf[i0:i1] += sig[:i1 - i0] * gain


# --------------------------------------------------------------- percussion --
def dhol_bass(amp=1.0):
    n = int(0.42 * SR)
    t = np.arange(n) / SR
    pitch = 58 + (150 - 58) * np.exp(-t * 34)          # fast downward chirp
    body = np.sin(TAU * np.cumsum(pitch) / SR)
    sub = np.sin(TAU * 46 * t) * np.exp(-t * 7)
    slap = np.random.randn(n) * np.exp(-t * 120) * 0.6  # stick transient
    sig = (body * np.exp(-t * 6.5) + sub * 0.7 + slap * 0.5)
    return sig * amp


def dhol_treble(amp=1.0):
    n = int(0.16 * SR)
    t = np.arange(n) / SR
    pitch = 150 + (300 - 150) * np.exp(-t * 40)
    body = np.sin(TAU * np.cumsum(pitch) / SR) * np.exp(-t * 26)
    click = np.random.randn(n) * np.exp(-t * 90) * 0.9
    return (body * 0.7 + click * 0.7) * amp


def damau(hi=False, amp=1.0):
    n = int(0.11 * SR)
    t = np.arange(n) / SR
    f = 430 if hi else 330
    pitch = f + f * 0.6 * np.exp(-t * 60)
    body = np.sin(TAU * np.cumsum(pitch) / SR) * np.exp(-t * 40)
    click = np.random.randn(n) * np.exp(-t * 160) * 0.8
    return (body * 0.6 + click * 0.6) * amp


def build_percussion():
    n = int(DUR * SR) + SR
    dh = np.zeros(n)
    dm = np.zeros(n)
    rng = np.random.RandomState(21)

    # dhol pattern over one bar, as 16th-step indices
    bass_steps  = [0, 3, 6, 10, 11]
    treble_steps = [4, 7, 8, 12, 14]
    # damau: steady bright 8ths with extra fills on the 2nd half
    damau_steps = [0, 2, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15]
    accents = {0, 8}

    for bar in range(BARS):
        base = bar * STEPS * STEP
        swing = 0.012
        for s in bass_steps:
            jit = rng.uniform(-0.006, 0.006)
            a = 1.0 if s in accents else 0.82
            _place(dh, dhol_bass(a), base + s * STEP + jit)
        for s in treble_steps:
            jit = rng.uniform(-0.006, 0.006)
            sw = swing if s % 2 else 0
            _place(dh, dhol_treble(0.8), base + s * STEP + sw + jit)
        for s in damau_steps:
            jit = rng.uniform(-0.004, 0.004)
            a = 0.9 if s in accents else 0.5
            _place(dm, damau(hi=(s % 4 == 2), amp=a),
                   base + s * STEP + jit)
        # bar-turn flourish
        if bar % 2 == 1:
            for k in range(4):
                _place(dm, damau(hi=True, amp=0.55),
                       base + (15) * STEP + k * (STEP / 4))
    return dh[:int(DUR * SR)] * 0.5, dm[:int(DUR * SR)] * 0.42


# ---------------------------------------------------- masakbeen (bagpipe) ----
def _reed(freq, dur, amp=1.0, vib=5.5, vibdepth=0.006):
    n = int(dur * SR)
    t = np.arange(n) / SR
    vibrato = 1 + vibdepth * np.sin(TAU * vib * t)
    ph = TAU * np.cumsum(freq * vibrato) / SR
    # nasal reed: strong odd + some even harmonics
    tone = (np.sin(ph) + 0.55 * np.sin(2 * ph) + 0.42 * np.sin(3 * ph)
            + 0.22 * np.sin(4 * ph) + 0.16 * np.sin(5 * ph))
    env = np.minimum(1.0, t * 18) * np.minimum(1.0, (dur - t) * 10)
    env = np.clip(env, 0, 1)
    return tone * env * amp


def semis(deg):
    return TONIC * 2 ** (deg / 12.0)


def build_masakbeen():
    n = int(DUR * SR)
    out = np.zeros(n)
    # continuous drone (tonic + fifth), the hallmark of the bagpipe
    t = np.arange(n) / SR
    drone = (np.sin(TAU * TONIC * t) + 0.6 * np.sin(TAU * semis(7) * t)
             + 0.3 * np.sin(TAU * TONIC * 0.5 * t))
    drone += 0.4 * np.sin(TAU * (2 * TONIC) * t)
    out += drone * 0.10

    # melody — major pentatonic, a lilting repeating phrase (beats, degree, len)
    penta = [0, 2, 4, 7, 9, 12]
    phrase = [
        (0.0, 7, 1.0), (1.0, 9, 0.5), (1.5, 7, 0.5), (2.0, 4, 1.0),
        (3.0, 2, 1.0),
        (4.0, 4, 0.5), (4.5, 7, 0.5), (5.0, 9, 1.0), (6.0, 7, 1.0),
        (7.0, 4, 1.0),
    ]
    for rep in range(BARS // 2):
        boff = rep * 4 * BEAT
        # vary the phrase slightly on the repeat
        var = 0 if rep % 2 == 0 else 0
        for (bt, deg, ln) in phrase:
            f = semis(penta[deg] if deg < len(penta) else deg)
            _place(out, _reed(f, ln * BEAT, amp=0.16),
                   boff + bt * BEAT)
    return out


# ------------------------------------------------------------- ransingha -----
def build_ransingha():
    n = int(DUR * SR)
    out = np.zeros(n)
    for phrase in range(BARS // 2):
        at = phrase * 4 * BEAT
        dur = 1.6
        m = int(dur * SR)
        t = np.arange(m) / SR
        f = semis(-12)                         # an octave below tonic
        tone = (np.sin(TAU * f * t) + 0.5 * np.sin(TAU * 2 * f * t)
                + 0.3 * np.sin(TAU * 3 * f * t))
        env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
        _place(out, tone * env, at, gain=0.14)
    return out


# ------------------------------------------------------------------ master ---
def crossfade_seam(x, ms=140):
    k = int(SR * ms / 1000)
    head = x[:k].copy()
    x[:k] = x[:k] * np.linspace(0, 1, k) + x[-k:] * np.linspace(1, 0, k)
    x[-k:] = x[-k:] * np.linspace(1, 0, k) + head * np.linspace(0, 1, k)
    return x


def render():
    np.random.seed(21)
    dh, dm = build_percussion()
    mel = build_masakbeen()
    horn = build_ransingha()
    L = min(len(dh), len(dm), len(mel), len(horn))
    mix = dh[:L] + dm[:L] + mel[:L] + horn[:L]
    mix = crossfade_seam(mix)

    # gentle bus compression via soft clip, then normalise
    mix = np.tanh(mix * 1.25)
    mix /= (np.max(np.abs(mix)) + 1e-9)
    mix *= 0.94

    # light stereo spread (Haas)
    d = 90
    left = mix.copy()
    right = np.concatenate([np.zeros(d), mix[:-d]]) * 0.97
    stereo = np.stack([left, right], axis=1)
    pcm = (stereo * 32767).astype(np.int16)

    wav = os.path.join(HERE, "_score.wav")
    with wave.open(wav, "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    out = os.path.join(ASSETS, "score.m4a")
    subprocess.run([FFMPEG, "-y", "-i", wav, "-c:a", "aac", "-b:a", "160k", out],
                   check=True, capture_output=True)
    os.remove(wav)
    return out


if __name__ == "__main__":
    out = render()
    print(f"saved {out}  ({os.path.getsize(out)/1e6:.2f} MB, "
          f"{DUR:.1f}s seamless loop @ {BPM} BPM, dhol-damau + masakbeen)")
