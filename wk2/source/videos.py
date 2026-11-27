"""Three sample 9:16 videos with kinetic type, faceless, curiosity hook first."""
import sys, os, math, subprocess
from PIL import Image, ImageDraw
from lib import *

W, H, FPS = 1080, 1920, 30
M = 96
TMP = "/home/claude/pm/tmp"
OUT = "/home/claude/pm/out"


def new(bg):
    img = Image.new("RGBA", (W, H), bg)
    return img, ImageDraw.Draw(img)


def end_card(t, dark, question, url, tagline, bg=None, cta="Book a 30 minute marketing review"):
    bg = bg or (D_BG if dark else L_BG)
    ink = D_INK if dark else L_INK
    muted = D_MUTED if dark else L_MUTED
    panel = D_ALT if dark else (L_BG if bg != L_BG else L_ALT)
    img, d = new(bg)
    bw = 96 * ease_out(prog(t, 0.0, 0.4))
    d.rectangle([M, 300, M + bw, 308], fill=RED)
    f = font(64, 750)
    stack(d, t, wrap(question, f, W - 2 * M), M, 400, 64, bg, ink, start=0.15, stagger=0.12, weight=750, lh=1.2)
    # CTA block
    p = ease_out(prog(t, 1.0, 0.5))
    if p > 0:
        y0 = 900 + (1 - p) * 40
        d.rectangle([M, y0, W - M, y0 + 400], fill=mix(bg, panel, p))
        cf = font(62, 850)
        yy = y0 + 120
        for ln in wrap(cta, cf, W - 2 * M - 120):
            draw_text(d, (W / 2, yy), ln, cf, mix(bg, ink, p), anchor="ms"); yy += 78
        draw_text(d, (W / 2, yy + 30), "Link in the caption", font(38, 600), mix(bg, muted, p), anchor="ms")
        draw_text(d, (W / 2, yy + 100), url, font(46, 800), mix(bg, AMBER if dark else ink, p), anchor="ms")
    p2 = ease_out(prog(t, 1.6, 0.5))
    if p2 > 0:
        lw = 420
        lg = logo(lw, "dark" if dark else "light", alpha=p2)
        paste(img, lg, (W - lw) / 2, 1400 + (1 - p2) * 30)
        draw_text(d, (W / 2, 1560), tagline, font(32, 500), mix(bg, muted, p2), anchor="ms")
    return img


# ----------------------------------------------------------- Video 1: Restaurant (dark)
def r_a(t):
    img, d = new(D_BG)
    p = prog(t, 0.05, 0.3) * (1 - ease_in_out(prog(t, 2.75, 0.3)))
    draw_text(d, (M, 640), "POV:", font(56, 700), mix(D_BG, AMBER, p))
    stack(d, t, ["Your food", "is amazing."], M, 690, 132, D_BG, D_INK, start=0.35, stagger=0.25, weight=850, out_start=2.75)
    return img


def r_b(t):
    img, d = new(D_BG)
    stack(d, t, ["But your", "page says",
                 {"text": "“WE’RE", "hl": AMBER, "hl_ink": L_INK, "weight": 900},
                 {"text": "CLOSED.”", "hl": AMBER, "hl_ink": L_INK, "weight": 900}],
          M, 600, 132, D_BG, D_INK, start=0.1, stagger=0.28, weight=850, lh=1.18, out_start=2.8)
    return img


def r_c(t):
    img, d = new(D_BG)
    out = ease_in_out(prog(t, 3.1, 0.35))
    pin = ease_out(prog(t, 0.0, 0.5))
    stack(d, t, ["Customers check", "your page first."], M, 300, 70, D_BG, D_INK, start=0.1, weight=750, out_start=3.05)
    # phone
    pw, ph = 600, 1020
    px = (W - pw) / 2
    py = 560 + (1 - pin) * 120 + out * 80
    col = mix(D_BG, D_LINE, pin * (1 - out))
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=60, outline=mix(D_BG, D_MUTED, pin * (1 - out)), width=6)
    # header
    hc = mix(D_BG, D_ALT, pin * (1 - out))
    d.ellipse([px + 50, py + 90, px + 150, py + 190], fill=hc)
    d.rectangle([px + 180, py + 110, px + 480, py + 130], fill=hc)
    d.rectangle([px + 180, py + 150, px + 400, py + 166], fill=hc)
    cell = (pw - 80) / 3
    for i in range(9):
        r, c = divmod(i, 3)
        x0 = px + 30 + c * (cell + 10); y0 = py + 260 + r * (cell + 10)
        fade = prog(t, 0.6 + i * 0.07, 0.3)
        d.rectangle([x0, y0, x0 + cell, y0 + cell], fill=mix(D_BG, D_ALT, fade * (1 - out)))
    # badge
    bp = back_out(prog(t, 1.5, 0.45))
    if bp > 0 and out < 1:
        bw, bh = 640 * min(1, bp), 120
        bx = (W - 640) / 2; by = py + 820
        d.rectangle([bx, by, bx + bw, by + bh], fill=mix(D_BG, AMBER, 1 - out))
        if bp > 0.6:
            draw_text(d, (W / 2, by + bh / 2 + 4), "Last post: 11 weeks ago", font(42, 800), mix(AMBER, L_INK, 1 - out), anchor="mm")
    return img


def r_d(t):
    img, d = new(D_BG)
    stack(d, t, ["You run", "the kitchen.", {"text": "We keep your", "color": D_MUTED}, {"text": "page", "color": D_MUTED},
                 {"text": "cooking.", "hl": AMBER, "hl_ink": L_INK, "weight": 900}],
          M, 560, 124, D_BG, D_INK, start=0.1, stagger=0.24, weight=850, out_start=2.85)
    return img


VIDEO1 = [(3.2, r_a), (3.2, r_b), (3.5, r_c), (3.3, r_d),
          (4.6, lambda t: end_card(t, True, "When did your page last post something new?",
                                   "platsera.com/growth", "Social media for restaurants"))]


# ----------------------------------------------------------- Video 2: HVAC (light)
BG2 = L_ALT


def call_card(d, t, x, y, missed_p):
    w, h = W - 2 * M, 200
    d.rectangle([x, y, x + w, y + h], fill=L_BG, outline=L_LINE, width=2)
    bar = mix((40, 160, 80), RED, missed_p)
    d.rectangle([x, y, x + 12, y + h], fill=bar)
    label = "Incoming call" if missed_p < 0.5 else "Missed call"
    lc = L_INK if missed_p < 0.5 else RED_TEXT
    draw_text(d, (x + 56, y + 90), label, font(54, 800), lc)
    draw_text(d, (x + 56, y + 150), "(630) 555-0142", font(36, 500), L_MUTED)
    # ringing pulse
    cx, cy = x + w - 110, y + h / 2
    if missed_p < 0.5:
        for k in range(3):
            ph = ((t * 1.2) + k / 3) % 1
            r = 20 + ph * 70
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=mix(L_BG, (40, 160, 80), 1 - ph), width=4)
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(40, 160, 80))
    else:
        d.line([cx - 26, cy - 26, cx + 26, cy + 26], fill=RED, width=10)
        d.line([cx - 26, cy + 26, cx + 26, cy - 26], fill=RED, width=10)


def h_a(t):
    img, d = new(BG2)
    out = ease_in_out(prog(t, 3.0, 0.35))
    p = ease_out(prog(t, 0.05, 0.45))
    draw_text(d, (M, 560 + (1 - p) * 40), "7:42 PM", font(210, 850), mix(BG2, L_INK, p * (1 - out)))
    stack(d, t, ["Your phone", "rings."], M, 640, 112, BG2, L_INK, start=0.5, stagger=0.2, weight=800, out_start=3.0)
    cp = ease_out(prog(t, 1.2, 0.5))
    if cp > 0 and out < 1:
        y = 1150 + (1 - cp) * 80 + out * 60
        call_card(d, t, M, y, 0)
    return img


def h_b(t):
    img, d = new(BG2)
    out = ease_in_out(prog(t, 2.7, 0.35))
    call_card(d, t, M, 1150 + out * 60, ease_out(prog(t, 0.5, 0.2)))
    stack(d, t, ["Nobody", "answers."], M, 560, 140, BG2, L_INK, start=0.7, stagger=0.25, weight=850, out_start=2.7)
    if out > 0:  # fade card by drawing bg over it
        ov = Image.new("RGBA", (W, H), BG2 + (int(255 * out),))
        img.alpha_composite(ov)
    return img


def h_c(t):
    img, d = new(BG2)
    stack(d, t, ["So they call", {"text": "the next", "color": L_MUTED}, {"text": "company.", "color": L_MUTED}],
          M, 520, 124, BG2, L_INK, start=0.1, stagger=0.24, weight=850, out_start=2.85)
    # three generic listings, the top one is not you
    names = ["Another HVAC Co.", "Your business", "Third result"]
    for i, n in enumerate(names):
        p = ease_out(prog(t, 0.9 + i * 0.15, 0.4)) * (1 - ease_in_out(prog(t, 2.85, 0.3)))
        if p <= 0:
            continue
        y = 1080 + i * 150 + (1 - p) * 50
        x = M
        fill = L_BG
        d.rectangle([x, y, W - M, y + 120], fill=mix(BG2, fill, p), outline=mix(BG2, L_LINE, p), width=2)
        tc = L_INK if i != 1 else L_MUTED
        draw_text(d, (x + 40, y + 76), n, font(42, 700 if i != 1 else 500), mix(BG2, tc, p))
        if i == 0:
            bp = back_out(prog(t, 1.7, 0.4))
            if bp > 0:
                d.rectangle([W - M - 230, y + 30, W - M - 230 + 190 * min(1, bp), y + 90], fill=mix(BG2, RED, p))
                if bp > 0.6:
                    draw_text(d, (W - M - 135, y + 62), "Booked", font(34, 800), mix(BG2, L_INK, p), anchor="mm")
    return img


def h_d(t):
    img, d = new(BG2)
    stack(d, t, ["Every", "missed call", "is a", {"text": "missed job.", "hl": RED, "hl_ink": L_INK, "weight": 900}],
          M, 620, 136, BG2, L_INK, start=0.1, stagger=0.24, weight=850, out_start=2.75)
    return img


def h_e(t):
    img, d = new(BG2)
    lines = ["We help HVAC and", "service businesses", "answer every lead,", "even after hours."]
    stack(d, t, lines, M, 700, 76, BG2, L_INK, start=0.1, stagger=0.15, weight=700, lh=1.25, out_start=2.7)
    return img


VIDEO2 = [(3.4, h_a), (3.1, h_b), (3.2, h_c), (3.1, h_d), (3.1, h_e),
          (4.6, lambda t: end_card(t, False, "How many calls went unanswered last week?",
                                   "platsera.com/growth", "Marketing for service businesses", bg=BG2))]


# ----------------------------------------------------------- Video 3: LinkedIn integration (light)
BG3 = L_BG


def l_a(t):
    img, d = new(BG3)
    stack(d, t, ["Someone on", "your team is", {"text": "a human API.", "hl": RED, "hl_ink": L_INK, "weight": 900}],
          M, 700, 124, BG3, L_INK, start=0.15, stagger=0.3, weight=850, out_start=2.8)
    return img


def boxes(d, t, appear, out, gap_state):
    """gap_state 0 = dashed red gap, 1 = connected."""
    bw, bh = 330, 220
    y = 960
    p = ease_out(appear) * (1 - out)
    for i, (lab, sub) in enumerate([("ERP", "Orders"), ("WMS", "Shipments")]):
        x = M if i == 0 else W - M - bw
        d.rectangle([x, y, x + bw, y + bh], fill=BG3, outline=mix(BG3, L_INK, p), width=4)
        draw_text(d, (x + bw / 2, y + bh / 2 + 6), lab, font(68, 850), mix(BG3, L_INK, p), anchor="mm")
        draw_text(d, (x + bw / 2, y + bh + 60), sub, font(34, 500), mix(BG3, L_MUTED, p), anchor="ms")
    gx0, gx1, gy = M + bw + 20, W - M - bw - 20, y + bh / 2
    return gx0, gx1, gy, p


def doc_icon(d, x, y, c, bg):
    d.rectangle([x - 26, y - 34, x + 26, y + 34], fill=bg, outline=c, width=4)
    for k in range(3):
        d.line([x - 14, y - 14 + k * 14, x + 14, y - 14 + k * 14], fill=c, width=3)


def l_b(t):
    img, d = new(BG3)
    out = ease_in_out(prog(t, 3.65, 0.3))
    stack(d, t, ["Orders live in one", "system. Shipping", "in another."], M, 460, 78, BG3, L_INK,
          start=0.05, stagger=0.15, weight=800, out_start=3.6)
    gx0, gx1, gy, p = boxes(d, t, prog(t, 0.5, 0.5), out, 0)
    if p > 0:
        import lib
        x = gx0 - ((t * 20) % 30)
        while x < gx1:
            a, b = max(x, gx0), min(x + 18, gx1)
            if b > a:
                d.line([a, gy, b, gy], fill=mix(BG3, RED, p), width=6)
            x += 30
        # documents carried slowly, by hand
        for k in range(2):
            ph = prog(t, 1.2 + k * 1.1, 1.6)
            if 0 < ph < 1:
                xx = lerp(gx0 - 60, gx1 + 60, ease_in_out(ph))
                yy = gy - 180 + math.sin(ph * math.pi * 6) * 8
                doc_icon(d, xx, yy, mix(BG3, L_INK, p), BG3)
    lp = prog(t, 1.4, 0.4) * (1 - out)
    if lp > 0:
        draw_text(d, (W / 2, 1420), "Retyped by hand. Every day.", font(44, 700), mix(BG3, RED_TEXT, lp), anchor="ms")
    return img


def l_c(t):
    img, d = new(BG3)
    out = ease_in_out(prog(t, 3.2, 0.3))
    stack(d, t, ["Close the gap", "and the work", "moves itself."], M, 460, 78, BG3, L_INK,
          start=0.05, stagger=0.15, weight=800, out_start=3.15)
    gx0, gx1, gy, p = boxes(d, t, 1, out, 1)
    fill = ease_in_out(prog(t, 0.4, 0.6))
    # remaining dashed part
    xs = lerp(gx0, gx1, fill)
    x = xs
    while x < gx1:
        d.line([x, gy, min(x + 18, gx1), gy], fill=mix(BG3, RED, p), width=6); x += 30
    if fill > 0:
        d.line([gx0, gy, xs, gy], fill=mix(BG3, L_INK, p), width=8)
    if fill >= 1:
        for k in range(4):
            ph = ((t - 1.0) * 1.4 + k / 4) % 1
            xx = lerp(gx0, gx1, ph)
            d.rectangle([xx - 9, gy - 9, xx + 9, gy + 9], fill=mix(BG3, RED, p))
    lp = prog(t, 1.2, 0.4) * (1 - out)
    if lp > 0:
        draw_text(d, (W / 2, 1420), "Synced automatically.", font(44, 700), mix(BG3, L_INK, lp), anchor="ms")
    return img


def l_d(t):
    img, d = new(BG3)
    stack(d, t, ["We build", "the bridge", {"text": "between the", "color": L_MUTED}, {"text": "systems you", "color": L_MUTED},
                 {"text": "already have.", "color": L_MUTED}],
          M, 560, 118, BG3, L_INK, start=0.1, stagger=0.2, weight=850, out_start=2.95)
    return img


VIDEO3 = [(3.3, l_a), (4.0, l_b), (3.5, l_c), (3.3, l_d),
          (4.6, lambda t: end_card(t, False, "Who is the human API in your company?",
                                   "platsera.com", "Custom software and AI agents", cta="Book a free technology review"))]


# ----------------------------------------------------------- render
def render(name, scenes, frames_only=None):
    files = []
    for si, (dur, fn) in enumerate(scenes):
        path = f"{TMP}/{name}_s{si}.mp4"
        if os.environ.get("ONLY_LAST") and si < len(scenes) - 1 and os.path.exists(path):
            files.append(path); continue
        n = int(round(dur * FPS))
        w = SceneWriter(path, W, H, FPS)
        for i in range(n):
            w.write(fn(i / FPS))
        w.close()
        files.append(path)
    lst = f"{TMP}/{name}.txt"
    open(lst, "w").write("".join(f"file '{p}'\n" for p in files))
    silent = f"{TMP}/{name}_silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
    return silent, sum(s[0] for s in scenes)


def stills(name, scenes, times):
    """times: list of (scene_index, t)"""
    for k, (si, t) in enumerate(times):
        scenes[si][1](t).convert("RGB").save(f"{TMP}/{name}_check{k}.png")


VIDEOS = {"v1": VIDEO1, "v2": VIDEO2, "v3": VIDEO3}

if __name__ == "__main__":
    mode = sys.argv[1]
    name = sys.argv[2]
    if mode == "stills":
        sc = VIDEOS[name]
        stills(name, sc, [(i, min(sc[i][0] - 0.5, 2.4)) for i in range(len(sc))])
    else:
        print(render(name, VIDEOS[name]))
