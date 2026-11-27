import sys, json, os, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/claude/social-media-posts/wk2/source')
import lib
lib.BRAND = '/home/claude/v2/assets'
from lib import font, logo, draw_text, wrap, ease_out, ease_in_out, prog, clamp, mix, SceneWriter, AMBER, RED

W, H, FPS, M = 1080, 1920, 30, 90
TL = json.load(open('timeline.json'))
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
    T(d, (M, 166), 'HOW LOCAL CUSTOMERS CHOOSE', 26, 700, MUTE, a=a)

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
def s1(d, t, gt):
    topbar(d, ease_out(prog(t, 0.1, 0.8)))
    lines = [('Before a customer', None), ('calls you,', None), ('the decision', None), ('is already made.', AMB)]
    y = 760
    for i, (ln, hl) in enumerate(lines):
        p = ease_out(prog(t, 0.6 + i * 0.45, 0.6)); f = font(96, 800)
        yy = y + i * 116 + (1 - p) * 30
        if hl and p > 0:
            wp = ease_out(prog(t, 0.6 + i * 0.45 + 0.3, 0.6)); tw = f.getlength(ln)
            d.rectangle([M - 14, yy - 88, M - 14 + (tw + 28) * wp, yy + 22], fill=mix(BG, hl, p))
            T(d, (M, yy), ln, 96, 800, (17, 17, 17), a=p) if wp > 0.5 else T(d, (M, yy), ln, 96, 800, INK, a=p)
        else:
            T(d, (M, yy), ln, 96, 800, INK, a=p)

def s2(d, t, gt):
    topbar(d); chapter(d, t, '01 · THE SEARCH'); bignum(d, t, 73)
    label(d, t, 'of local searches start on a phone')
    a = ease_out(prog(t, 1.0, 0.6)); cx, cy = W // 2, 1180
    d.rounded_rectangle([cx - 110, cy - 200, cx + 110, cy + 200], 34, outline=mix(BG, MUTE, a), width=5)
    d.rounded_rectangle([cx - 80, cy - 160, cx + 80, cy - 122], 18, outline=mix(BG, AMB, a), width=4)
    for k in range(3):
        pk = ease_out(prog(t, 1.4 + k * 0.25, 0.4))
        d.rounded_rectangle([cx - 80, cy - 100 + k * 72, cx - 80 + 160 * pk, cy - 52 + k * 72], 10, fill=mix(BG, LINE, pk))
    source(d, t, 'Source: BrightLocal, Consumer Search Behavior 2026 (1,227 US consumers)')

def s3(d, t, gt):
    topbar(d); chapter(d, t, '02 · THE SHORTLIST'); bignum(d, t, 72)
    label(d, t, 'look at three or fewer businesses before they decide')
    keep = {1, 6, 8}; cw, ch, gx, gy = 196, 84, 22, 22
    x0 = (W - (4 * cw + 3 * gx)) // 2; y0 = 1010
    for k in range(12):
        r_, c_ = divmod(k, 4); x = x0 + c_ * (cw + gx); y = y0 + r_ * (ch + gy)
        a = ease_out(prog(t, 0.9 + k * 0.04, 0.4)); cut = ease_in_out(prog(t, 2.2, 0.8))
        if k in keep:
            col = mix(mix(BG, LINE, a), AMB, cut); outline = None
        else:
            col = mix(mix(BG, LINE, a), mix(BG, LINE, 0.35), cut)
        d.rounded_rectangle([x, y, x + cw, y + ch], 16, fill=col)
    source(d, t, 'Source: BrightLocal, Consumer Search Behavior 2026')

def s4(d, t, gt):
    topbar(d); chapter(d, t, '03 · THE REVIEWS')
    t2 = capstart('s4', 1) - TL['scenes'][3]['start']
    bignum(d, t, 74, start=t2 - 0.3)
    label(d, t, 'only care about reviews from the last three months', start=t2 + 0.2)
    rows = [('2 days ago', 1.0), ('3 weeks ago', 1.0), ('9 months ago', 0.32)]
    for k, (txt, op) in enumerate(rows):
        a = ease_out(prog(t, 0.3 + k * 0.25, 0.5)); fade = 1 - (1 - op) * ease_in_out(prog(t, t2 + 0.8, 0.8))
        y = 1040 + k * 110; aa = a * fade
        d.rounded_rectangle([M, y, W - M, y + 88], 18, fill=mix(BG, (30, 29, 27), a))
        for s_ in range(5): star(d, M + 44 + s_ * 40, y + 44, 15, mix(BG, AMB, aa))
        T(d, (W - M - 30, y + 56), txt, 32, 700, INK, anchor='rs', a=aa)
    T(d, (M, 1392), 'Illustrative', 22, 500, DIM, a=ease_out(prog(t, 1, .5)))
    source(d, t, 'Source: BrightLocal, Local Consumer Review Survey 2026 (1,002 US adults)', start=t2 + 0.6)

def s5(d, t, gt):
    topbar(d); chapter(d, t, '04 · THE GAP')
    t2 = capstart('s5', 1) - TL['scenes'][4]['start']
    def row(y, txt, st, col):
        a = ease_out(prog(t, st, 0.5)); p = ease_out(prog(t, st, 1.1)); n = int(round(47 * p))
        T(d, (M - 6, y), f'{n}%', 190, 800, col, a=a)
        f = font(40, 600)
        for i, ln in enumerate(wrap(txt, f, W - 2 * M)):
            T(d, (M, y + 66 + i * 52), ln, 40, 600, INK, a=ease_out(prog(t, st + 0.3, 0.5)))
    row(640, 'of customers won’t choose a business with fewer than 20 reviews', 0.4, INK)
    row(1060, 'of small businesses have fewer than 20 reviews', t2 - 0.2, AMB)
    source(d, t, 'Source: BrightLocal, Small Business Marketing Report 2026', start=t2 + 0.5)

def s6(d, t, gt):
    topbar(d); chapter(d, t, '05 · THE FEED'); bignum(d, t, 30)
    label(d, t, 'check social media during their search')
    t2 = capstart('s6', 1) - TL['scenes'][5]['start']
    a = ease_out(prog(t, 1.1, 0.6)); q = ease_in_out(prog(t, t2, 0.8))
    x0, y0 = M, 1000
    d.rounded_rectangle([x0, y0, W - M, y0 + 330], 26, fill=mix(BG, (30, 29, 27), a))
    d.ellipse([x0 + 34, y0 + 34, x0 + 104, y0 + 104], fill=mix(BG, LINE, a))
    d.rounded_rectangle([x0 + 124, y0 + 44, x0 + 420, y0 + 66], 10, fill=mix(BG, LINE, a))
    d.rounded_rectangle([x0 + 34, y0 + 136, W - M - 34, y0 + 296], 18, fill=mix(BG, mix(LINE, BG, 0.4 * q), a))
    T(d, (W - M - 34, y0 + 90), 'Last post: 4 months ago', 30, 700, mix(MUTE, (196, 45, 4), q), anchor='rs', a=a)
    T(d, (M, 1372), 'Illustrative', 22, 500, DIM, a=a)
    source(d, t, 'Source: BrightLocal, Consumer Search Behavior 2026')

def s7(d, t, gt):
    topbar(d); chapter(d, t, 'WHAT IT MEANS')
    sc = TL['scenes'][6]; c2 = [c for c in TL['caps'] if c['scene'] == 's7'][1]
    t2 = c2['start'] - sc['start']; d2 = c2['end'] - c2['start']
    a = ease_out(prog(t, 0.5, 0.5)); strike = ease_out(prog(t, 2.4, 0.6))
    f = font(84, 800); txt = 'Not going viral.'; tw = f.getlength(txt)
    T(d, (M, 620), txt, 84, 800, mix(INK, MUTE, strike), a=a)
    if strike > 0: d.rectangle([M, 590, M + tw * strike, 598], fill=mix(BG, RED, a))
    words = ['Showing up.', 'Current.', 'Consistent.', 'Every week.']
    marks = [0.05, 0.35, 0.52, 0.70]
    for k, w_ in enumerate(words):
        p = ease_out(prog(t, t2 + marks[k] * d2, 0.45)); y = 820 + k * 124 + (1 - p) * 24
        if k == 3 and p > 0:
            ff = font(96, 800); ww = ff.getlength(w_)
            hp = ease_out(prog(t, t2 + marks[k] * d2 + 0.25, 0.5))
            d.rectangle([M - 14, y - 86, M - 14 + (ww + 28) * hp, y + 22], fill=mix(BG, AMB, p))
            T(d, (M, y), w_, 96, 800, (17, 17, 17) if hp > .5 else INK, a=p)
        else:
            T(d, (M, y), w_, 96, 800, INK, a=p)

def s8(d, t, gt):
    a = ease_out(prog(t, 0.3, 0.8))
    lg = logo(520, 'dark', alpha=a); IMG.alpha_composite(lg, ((W - lg.width) // 2, 470))
    c2 = capstart('s8', 1) - TL['scenes'][7]['start']
    b = ease_out(prog(t, c2 - 0.2, 0.6))
    T(d, (W // 2, 860), 'Book a 30 minute', 70, 800, INK, anchor='ms', a=b)
    T(d, (W // 2, 950), 'marketing review', 70, 800, INK, anchor='ms', a=b)
    T(d, (W // 2, 1040), 'Link in the caption', 44, 700, AMB, anchor='ms', a=b)
    T(d, (W // 2, 1100), 'platsera.com/growth', 38, 600, MUTE, anchor='ms', a=b)
    s = ease_out(prog(t, c2 + 1.0, 0.8))
    for i, ln in enumerate(['Sources: BrightLocal Consumer Search Behavior 2026 (1,227 US consumers);',
                            'Local Consumer Review Survey 2026 (1,002 US adults);',
                            'Small Business Marketing Report 2026 (1,002 US business owners).']):
        T(d, (W // 2, 1300 + i * 34), ln, 22, 500, MUTE, anchor='ms', a=s)

FUN = {'s1': s1, 's2': s2, 's3': s3, 's4': s4, 's5': s5, 's6': s6, 's7': s7, 's8': s8}
IMG = None

def frame(sc, f):
    global IMG
    t = f / FPS; gt = sc['start'] + t
    IMG = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(IMG)
    FUN[sc['id']](d, t, gt)
    caption(d, gt)
    if sc['id'] != 's8':
        lg = logo(200, 'dark', alpha=0.85); IMG.alpha_composite(lg, (M, 1800 - lg.height))
    fin = 0.45; fout = 0.4
    fade = min(1, t / fin) if sc['id'] != 's1' else min(1, t / 0.8)
    if sc['id'] != 's8': fade = min(fade, (sc['dur'] - t) / fout)
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
