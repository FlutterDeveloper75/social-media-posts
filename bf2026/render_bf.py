import sys, json, os, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/claude/social-media-posts/wk2/source')
import lib
lib.BRAND = '/home/claude/v2/assets'
from lib import font, logo, draw_text, wrap, ease_out, ease_in_out, prog, clamp, mix, SceneWriter, AMBER, RED

W, H, FPS, M = 1080, 1920, 30, 90
TL = json.load(open('timeline.json'))
CFG = json.load(open('config.json'))
BG = (14, 14, 14); INK = (245, 243, 240); MUTE = (150, 145, 138); DIM = (70, 67, 63); LINE = (48, 46, 43)
AMB = AMBER

# precomputed vignette and grain
yy, xx = np.mgrid[0:H, 0:W]
r = np.sqrt(((xx - W / 2) / (W * .75)) ** 2 + ((yy - H * .45) / (H * .62)) ** 2)
VIG = np.clip(1 - 0.55 * np.clip(r - 0.35, 0, 1) ** 1.4, 0, 1)[..., None].astype(np.float32)
rng = np.random.default_rng(7)
GRAIN = [rng.normal(0, 5.5, (H // 2, W // 2, 1)).repeat(2, 0).repeat(2, 1).astype(np.float32) for _ in range(6)]

def finish(img, fno, fade):
    a = np.asarray(img.convert('RGB'), dtype=np.float32)
    a = a * VIG + GRAIN[fno % 6]
    a *= fade
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def T(d, xy, s, size, w=700, fill=INK, anchor='ls', a=1.0):
    draw_text(d, xy, s, font(size, w), mix(BG, fill, a), anchor=anchor)

def topbar(d, a=1):
    d.rectangle([M, 112, M + 56, 118], fill=mix(BG, RED, a))
    T(d, (M, 166), CFG['tag'], 26, 700, MUTE, a=a)

def chapter(d, t, label):
    a = ease_out(prog(t, 0.15, 0.6))
    T(d, (M, 392), label, 34, 800, AMB, a=a)

def bignum(d, t, value, suffix='%', y=720, size=300, start=0.35):
    p = ease_out(prog(t, start, 1.3)); n = int(round(value * p))
    a = ease_out(prog(t, start, 0.4))
    sz = int(size * (0.94 + 0.06 * ease_out(prog(t, start, 2.5))))
    T(d, (M - 8, y), f'{n}{suffix}', sz, 800, INK, a=a)

def label(d, t, text, y=800, size=50, start=0.8, width=W - 2 * M, color=INK):
    a = ease_out(prog(t, start, 0.5)); f = font(size, 600)
    for i, ln in enumerate(wrap(text, f, width)):
        T(d, (M, y + i * int(size * 1.28)), ln, size, 600, color, a=a)

def source(d, t, text, start=1.2):
    a = ease_out(prog(t, start, 0.5)) * 0.95
    f = font(24, 600); y = 1440
    for i, ln in enumerate(wrap(text, f, W - 2 * M)):
        T(d, (M, y + i * 34), ln, 24, 600, MUTE, a=a)

def caption(d, gt):
    for c in TL['caps']:
        if c['start'] - 0.05 <= gt <= c['end'] + 0.25:
            a = min(ease_out(prog(gt, c['start'] - 0.05, 0.2)), 1 - prog(gt, c['end'] + 0.05, 0.2))
            f = font(40, 600); lines = wrap(c['text'], f, W - 2 * M - 40)
            y0 = 1640 - (len(lines) - 1) * 26
            for i, ln in enumerate(lines):
                T(d, (W // 2, y0 + i * 54), ln, 40, 600, INK, anchor='ms', a=a)

def star(d, cx, cy, r, fill):
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)

def capstart(sid, i):
    return [c for c in TL['caps'] if c['scene'] == sid][i]['start']


# ---------------- scenes ----------------
def scn(i): return TL['scenes'][i]
def capstart(sid, i):
    return [c for c in TL['caps'] if c['scene'] == sid][i]['start']

def hl_lines(d, t, lines, y0=760, size=96, step=116, start=0.5):
    for i, (ln, hl) in enumerate(lines):
        p = ease_out(prog(t, start + i * 0.45, 0.6)); f = font(size, 800)
        yy = y0 + i * step + (1 - p) * 30
        if hl and p > 0:
            wp = ease_out(prog(t, start + i * 0.45 + 0.3, 0.6)); tw = f.getlength(ln)
            d.rectangle([M - 14, yy - int(size * .92), M - 14 + (tw + 28) * wp, yy + int(size * .23)], fill=mix(BG, AMB, p))
            T(d, (M, yy), ln, size, 800, (17, 17, 17) if wp > .5 else INK, a=p)
        else:
            T(d, (M, yy), ln, size, 800, INK, a=p)

def s1(d, t, gt):
    topbar(d, ease_out(prog(t, 0.1, 0.8)))
    hl_lines(d, t, [(l, AMB if k == len(CFG['hook']) - 1 else None) for k, l in enumerate(CFG['hook'])])

def s2(d, t, gt):
    topbar(d); chapter(d, t, 'THE PROBLEM'); bignum(d, t, CFG['stat'])
    label(d, t, CFG['stat_label'])
    if CFG['visual'] == 'shortlist':
        keep = {1, 6, 8}; cw, ch, gx, gy = 196, 84, 22, 22
        x0 = (W - (4 * cw + 3 * gx)) // 2; y0 = 1010
        for k in range(12):
            r_, c_ = divmod(k, 4); x = x0 + c_ * (cw + gx); y = y0 + r_ * (ch + gy)
            a = ease_out(prog(t, 0.9 + k * 0.04, 0.4)); cut = ease_in_out(prog(t, 2.2, 0.8))
            col = mix(mix(BG, LINE, a), AMB, cut) if k in keep else mix(mix(BG, LINE, a), mix(BG, LINE, 0.35), cut)
            d.rounded_rectangle([x, y, x + cw, y + ch], 16, fill=col)
    else:
        a = ease_out(prog(t, 0.9, 0.5)); p = ease_in_out(prog(t, 1.2, 2.6))
        cx, cy, R = W // 2, 1180, 170
        d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=mix(BG, LINE, a), width=22)
        if p > 0: d.arc([cx - R, cy - R, cx + R, cy + R], -90, -90 + 360 * p, fill=mix(BG, AMB, a), width=22)
        T(d, (cx, cy + 22), '30', 96, 800, INK, anchor='ms', a=a)
        T(d, (cx, cy + 70), 'MINUTES', 26, 700, MUTE, anchor='ms', a=a)
    source(d, t, CFG['source'])

def s3(d, t, gt):
    topbar(d); chapter(d, t, 'THE BLACK FRIDAY DEAL')
    a = ease_out(prog(t, 0.3, 0.6)); f = font(150, 800)
    sz = 150
    while font(sz, 800).getlength('BLACK FRIDAY') > W - 2 * M: sz -= 4
    T(d, (M - 4, 640), 'BLACK FRIDAY', sz, 800, INK, a=a)
    t2 = capstart('s3', 1) - scn(2)['start']
    p = ease_out(prog(t, t2 + 0.3, 0.6)); big = 230
    while font(big, 800).getlength('50% OFF') > W - 2 * M - 40: big -= 4
    tw = font(big, 800).getlength('50% OFF'); y = 720
    if p > 0:
        d.rectangle([M, y, M + (tw + 40) * p, y + big - 6], fill=mix(BG, AMB, p))
        T(d, (M + 20, y + int(big * .86)), '50% OFF', big, 800, (17, 17, 17), a=p)
    q = ease_out(prog(t, t2 + 0.8, 0.5)); yy = y + big + 84
    T(d, (M, yy), 'your first month', 70, 800, INK, a=q)
    T(d, (M, yy + 70), 'Starter $149.50 · Local $299.50', 44, 700, MUTE, a=q)
    if CFG.get('founding'):
        T(d, (M, yy + 124), 'Then the founding rate, locked 12 months', 34, 600, MUTE, a=q)

def s4(d, t, gt):
    topbar(d); chapter(d, t, 'ENDS MONDAY')
    a = ease_out(prog(t, 0.3, 0.6))
    T(d, (M - 4, 620), 'MON, NOV 30', 132, 800, INK, a=a)
    T(d, (M, 712), '11:59 PM CENTRAL', 60, 800, AMB, a=ease_out(prog(t, 0.7, 0.6)))
    t2 = capstart('s4', 1) - scn(3)['start']
    b = ease_out(prog(t, t2 - 0.3, 0.6))
    lg = logo(380, 'dark', alpha=b); IMG.alpha_composite(lg, (M, 900))
    cs = 52
    while font(cs, 800).getlength('Book a 30 minute marketing review') > W - 2 * M: cs -= 2
    T(d, (M, 1110), 'Book a 30 minute marketing review', cs, 800, INK, a=b)
    T(d, (M, 1180), 'Link in the caption', 42, 700, AMB, a=b)
    T(d, (M, 1236), CFG['url'], 36, 600, MUTE, a=b)

FUN = {'s1': s1, 's2': s2, 's3': s3, 's4': s4}

IMG = None

def frame(sc, f):
    global IMG
    t = f / FPS; gt = sc['start'] + t
    IMG = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(IMG)
    FUN[sc['id']](d, t, gt)
    caption(d, gt)
    if sc['id'] != 's4':
        lg = logo(200, 'dark', alpha=0.85); IMG.alpha_composite(lg, (M, 1800 - lg.height))
    fin = 0.45; fout = 0.4
    fade = min(1, t / fin) if sc['id'] != 's1' else min(1, t / 0.8)
    if sc['id'] != 's4': fade = min(fade, (sc['dur'] - t) / fout)
    else: fade = min(fade, (sc['dur'] - t) / 1.2)
    return finish(IMG, int(gt * FPS), max(0.0, min(1.0, fade)))

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for spec in sys.argv[2:]:
            sid, tt = spec.split('@'); sc = next(s for s in TL['scenes'] if s['id'] == sid)
            frame(sc, int(float(tt) * FPS)).save(f'/tmp/doc_{sid}_{tt}.png')
    else:
        os.makedirs('scenes', exist_ok=True)
        for sc in TL['scenes']:
            if len(sys.argv) > 2 and sc['id'] not in sys.argv[2:]: continue
            w = SceneWriter(f"scenes/{sc['id']}.mp4", W, H, FPS)
            for f in range(sc['frames']): w.write(frame(sc, f))
            w.close(); print('scene', sc['id'], flush=True)
