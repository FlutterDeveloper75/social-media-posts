import json, numpy as np, soundfile as sf
from scipy.signal import resample_poly
from kokoro_onnx import Kokoro
SR = 48000
K = Kokoro('/home/claude/kokoro/kokoro-v1.0.onnx', '/home/claude/kokoro/voices-v1.0.bin')
script = json.load(open('script.json'))
out = []
for sc in script:
    for i, line in enumerate(sc['lines']):
        s, sr = K.create(line, voice='af_heart', speed=0.96, lang='en-us')
        s = resample_poly(s.astype(np.float64), SR // 1000, sr // 1000)   # 24k -> 48k
        idx = np.where(np.abs(s) > 0.008)[0]
        s = s[max(0, idx[0] - int(0.02 * SR)): idx[-1] + int(0.08 * SR)]
        # level-match each line by RMS of voiced part, then 15 ms fades to avoid clicks
        rms = np.sqrt(np.mean(s[np.abs(s) > 0.02] ** 2)); s = s * (0.12 / rms)
        f = int(0.015 * SR); s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f)
        fn = f"v_{sc['id']}_{i}.wav"; sf.write(fn, s.astype(np.float32), SR, subtype='PCM_24')
        out.append({'scene': sc['id'], 'i': i, 'file': fn, 'text': line, 'dur': round(len(s) / SR, 3), 'peak': round(float(np.max(np.abs(s))), 3)})
json.dump(out, open('voice.json', 'w'), indent=1)
tot = sum(o['dur'] for o in out)
for o in out: print(o['scene'], o['dur'], o['peak'], o['text'][:50])
print('speech total', round(tot, 1))
