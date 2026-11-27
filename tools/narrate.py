"""Narration (Kokoro, voice af_heart) + synthesized SFX + soft music bed, timed to video cues."""
import json, sys, wave
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'wk2', 'source'))
from audio import bed
from kokoro_onnx import Kokoro

SR = 44100
K = Kokoro(os.path.expanduser('~/kokoro/kokoro-v1.0.onnx'), os.path.expanduser('~/kokoro/voices-v1.0.bin'))
VOICE = 'af_heart'

def tts(text, speed):
    s, sr = K.create(text, voice=VOICE, speed=speed, lang='en-us')
    s = resample_poly(s, SR, sr)
    # trim leading/trailing silence
    idx = np.where(np.abs(s) > 0.01)[0]
    return s[max(0, idx[0] - 200): idx[-1] + 800] if len(idx) else s

def whoosh(d=0.45):
    n = int(d * SR); t = np.arange(n) / SR
    noise = np.random.default_rng(3).standard_normal(n)
    # sweep a simple one-pole low pass upward then down
    cut = 0.02 + 0.25 * np.sin(np.pi * t / d) ** 2
    y = np.zeros(n); acc = 0
    for i in range(n):
        acc += cut[i] * (noise[i] - acc); y[i] = acc
    return y * np.sin(np.pi * t / d) ** 2 * 0.5

def pop(f=880, d=0.12):
    n = int(d * SR); t = np.arange(n) / SR
    fr = f * (1 + 0.6 * np.exp(-t * 40))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 30) * 0.35

def click(d=0.05):
    n = int(d * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2200 * t) * 0.5 + np.random.default_rng(5).standard_normal(n) * 0.2) * np.exp(-t * 120) * 0.5

def tick():
    return pop(1320, 0.07) * 0.6

SFX = {'whoosh': whoosh, 'pop': pop, 'click': click, 'tick': tick,
       'chime': lambda: pop(1046, 0.35) + pop(1568, 0.35) * 0.6}

def build(cfg, out):
    dur = cfg['dur']; n = int(dur * SR)
    voice = np.zeros(n); fx = np.zeros(n)
    report = []
    for start, end, text in cfg['cues']:
        win = end - start
        s = tts(text, 1.0)
        if len(s) / SR > win:
            sp = min(1.3, (len(s) / SR) / win * 1.03)
            s = tts(text, sp)
        else:
            sp = 1.0
        i = int(start * SR); j = min(n, i + len(s))
        voice[i:j] += s[: j - i]
        report.append((start, round(len(s) / SR, 2), round(win, 2), sp, text))
    for at, kind in cfg['sfx']:
        s = SFX[kind](); i = int(at * SR); j = min(n, i + len(s)); fx[i:j] += s[: j - i]
    music = bed(dur, bpm=96, hats=False).astype(float) / 32767
    # duck music under voice
    env = np.convolve((np.abs(voice) > 0.02).astype(float), np.ones(int(0.25 * SR)) / int(0.25 * SR), 'same')
    music *= 0.16 * (1 - 0.6 * np.clip(env * 3, 0, 1))
    voice = voice / (np.max(np.abs(voice)) + 1e-9) * 0.85
    mix = voice + fx * 0.6 + music
    mix /= max(1.0, np.max(np.abs(mix)) / 0.95)
    sf.write(out, mix.astype(np.float32), SR)
    for r in report: print(r)

if __name__ == '__main__':
    build(json.load(open(sys.argv[1])), sys.argv[2])
