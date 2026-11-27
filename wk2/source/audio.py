"""Synthesized, royalty-free music bed: soft kick, light hats, low pad."""
import sys, wave
import numpy as np

SR = 44100


def bed(length, bpm=100, hats=True, seed=1):
    rng = np.random.default_rng(seed)
    n = int(length * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    beat = 60 / bpm
    # pad: A minor add9, slow swell, two detuned voices
    for f in (110.0, 164.81, 261.63, 246.94):
        out += 0.05 * (np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * 1.004 * t))
    out *= 0.6 + 0.4 * np.sin(2 * np.pi * t / (beat * 8)) ** 2
    # kick on every beat
    kl = int(0.35 * SR)
    kt = np.arange(kl) / SR
    freq = 50 + 90 * np.exp(-kt * 25)
    kick = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-kt * 9) * 0.55
    # hat on the off beat
    hl = int(0.05 * SR)
    hat = rng.standard_normal(hl) * np.exp(-np.arange(hl) / SR * 80) * 0.06
    hat = np.diff(np.concatenate([[0], hat]))  # crude high pass
    k = 0.0
    while k < length:
        i = int(k * SR)
        out[i:i + kl] += kick[: max(0, min(kl, n - i))]
        if hats:
            j = int((k + beat / 2) * SR)
            if j < n:
                out[j:j + hl] += hat[: max(0, min(hl, n - j))]
        k += beat
    # fades
    fi, fo = int(0.4 * SR), int(1.2 * SR)
    out[:fi] *= np.linspace(0, 1, fi)
    out[-fo:] *= np.linspace(1, 0, fo)
    out /= np.max(np.abs(out)) + 1e-9
    return (out * 0.5 * 32767).astype(np.int16)


if __name__ == "__main__":
    path, length, bpm, hats = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4] == "1"
    data = bed(length, bpm, hats)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(data.tobytes())
