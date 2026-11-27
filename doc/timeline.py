import json
FPS = 30
v = json.load(open('voice.json'))
LEAD = {'s1': 0.9}; TAIL = {'s7': 1.3, 's8': 4.2}
GAP = 0.5
scenes, caps, t = [], [], 0.0
order = []
for o in v:
    if o['scene'] not in order: order.append(o['scene'])
for sid in order:
    lines = [o for o in v if o['scene'] == sid]
    start = t; c = t + LEAD.get(sid, 0.75)
    for k, o in enumerate(lines):
        caps.append({'scene': sid, 'file': o['file'], 'text': o['text'], 'start': round(c, 3), 'end': round(c + o['dur'], 3)})
        c += o['dur'] + (GAP if k < len(lines) - 1 else 0)
    end = c + TAIL.get(sid, 0.95)
    nfr = round((end - start) * FPS); end = start + nfr / FPS
    scenes.append({'id': sid, 'start': round(start, 4), 'dur': round(nfr / FPS, 4), 'frames': nfr})
    t = end
json.dump({'scenes': scenes, 'caps': caps, 'total': round(t, 3)}, open('timeline.json', 'w'), indent=1)
for s in scenes: print(s)
print('total', round(t, 2))
