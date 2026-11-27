import json, numpy as np, soundfile as sf
SR = 48000
TLj = json.load(open('timeline.json')); TOT = TLj['total']; N = int(TOT * SR) + SR // 10
t = np.arange(N) / SR
voice = np.zeros(N)
for c in TLj['caps']:
    s, sr = sf.read(c['file']); i = int(round(c['start'] * SR)); voice[i:i + len(s)] += s[: max(0, min(len(s), N - i))]

# ---------- music: slow documentary pad, A minor ----------
def note(f): return 440.0 * 2 ** ((f - 69) / 12)
chords = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 55, 60, 64], [55, 59, 62, 67]]   # Am F C G
CH = 4.2
music = np.zeros(N)
k = 0; start = 0.0
while start < TOT:
    seg_len = CH + 1.6; n0 = int(start * SR); n1 = min(N, int((start + seg_len) * SR)); tt = np.arange(n1 - n0) / SR
    env = np.minimum(1, tt / 1.2) * np.minimum(1, (seg_len - tt) / 1.4)
    for m in chords[k % 4]:
        f = note(m)
        for det in (1.0, 1.003):
            ph = 2 * np.pi * f * det * tt
            music[n0:n1] += env * (np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)) * 0.045
    # soft felt-piano note on each change
    f = note(chords[k % 4][0] + 12); dec = np.exp(-tt * 1.6); ph = 2 * np.pi * f * tt
    music[n0:n1] += (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.1 * np.sin(3 * ph)) * dec * np.minimum(1, tt / 0.01) * 0.09
    # low bass note
    fb = note(chords[k % 4][0] - 12)
    music[n0:n1] += np.sin(2 * np.pi * fb * tt) * env * 0.07
    k += 1; start += CH
# gentle low-pass smoothing (3-tap moving average twice)
for _ in range(2): music = np.convolve(music, np.ones(5) / 5, 'same')
music *= np.minimum(1, t / 2.0) * np.clip((TOT - t) / 3.5, 0, 1)

# ---------- ducking with smooth attack/release ----------
act = (np.abs(voice) > 0.01).astype(float)
act = np.convolve(act, np.ones(int(0.03 * SR)) / int(0.03 * SR), 'same')
env = np.zeros(N); a_att, a_rel = np.exp(-1 / (0.08 * SR)), np.exp(-1 / (0.45 * SR)); e = 0.0
for i in range(0, N, 48):           # 1 ms steps
    x = 1.0 if act[i] > 0.05 else 0.0
    coef = a_att ** 48 if x > e else a_rel ** 48
    e = x + (e - x) * coef; env[i:i + 48] = e
music *= (1 - 0.6 * env)            # about -8 dB under speech

# ---------- sound design: soft transitions ----------
fx = np.zeros(N); rng = np.random.default_rng(11)
def add(at, sig):
    i = int(at * SR); j = min(N, i + len(sig)); fx[i:j] += sig[: j - i]
def swell(d=0.9):
    n = int(d * SR); tt = np.arange(n) / SR; nz = rng.standard_normal(n)
    y = np.zeros(n); acc = 0.0; cut = 0.01 + 0.06 * (tt / d)
    for i in range(n): acc += cut[i] * (nz[i] - acc); y[i] = acc
    shape = np.sin(np.pi * tt / d) ** 2
    sub = np.sin(2 * np.pi * 52 * tt) * np.exp(-((tt - d * 0.75) ** 2) / 0.02)
    return (y * 1.6 + sub * 0.35) * shape * 0.35
def chime():
    n = int(2.5 * SR); tt = np.arange(n) / SR; out = np.zeros(n)
    for f, a in ((note(69), 1), (note(76), .6), (note(81), .35)):
        out += np.sin(2 * np.pi * f * tt) * a * np.exp(-tt * 1.8)
    return out * np.minimum(1, tt / 0.005) * 0.07
for sc in TLj['scenes'][1:7]: add(sc['start'] - 0.55, swell())
add(TLj['scenes'][7]['start'] + 0.2, chime())

mix = voice * 1.0 + music * 0.42 + fx * 0.5
pk = np.max(np.abs(mix)); mix = mix / max(1.0, pk / 0.89)
sf.write('mix.wav', mix.astype(np.float32), SR, subtype='PCM_24')
def db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
sp = act > 0.5
print('peak', round(float(pk), 3), 'voice rms(speech) dB', round(db(voice[sp]), 1), 'music under speech dB', round(db(0.42*music[sp]), 1), 'music in gaps dB', round(db(0.42*music[~sp & (t > 2) & (t < TOT - 4)]), 1), 'fx peak', round(float(np.max(np.abs(0.5*fx))),3))
