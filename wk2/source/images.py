"""Four sample static posts, 1080x1350 (4:5)."""
from PIL import Image, ImageDraw
from lib import *

W, H = 1080, 1350
M = 88
OUT = "/home/claude/pm/out"


def footer(img, d, dark, cta, url, bg=None):
    ink = D_INK if dark else L_INK
    muted = D_MUTED if dark else L_MUTED
    line = D_LINE if dark else L_LINE
    y = H - 300
    d.line([M, y, W - M, y], fill=line, width=2)
    draw_text(d, (M, y + 74), cta, font(44, 800), ink)
    draw_text(d, (M, y + 122), "Link in the caption", font(30, 500), muted)
    lg = logo(250, "dark" if dark else "light")
    paste(img, lg, M, H - 88 - lg.height)
    draw_text(d, (W - M, H - 88 - lg.height / 2 + 10), url, font(30, 700), AMBER if dark else ink, anchor="rs")


def eyebrow(d, x, y, txt, color, dark):
    f = font(24, 700)
    d.rectangle([x, y, x + 56, y + 6], fill=RED)
    draw_text(d, (x, y + 52), txt, f, color)


def static(fn, t=99):
    return fn(t)


# 1. Restaurant, Facebook growth line, dark theme ------------------------
def restaurant(t=99, img=None):
    img = Image.new("RGBA", (W, H), D_BG)
    d = ImageDraw.Draw(img)
    eyebrow(d, M, M, "FOR RESTAURANT OWNERS", AMBER, True)
    stack(d, t, ["Your food is", "amazing.", "Your page says", {"text": "“we’re closed.”", "hl": AMBER, "hl_ink": L_INK}],
          M, 250, 92, D_BG, D_INK)
    # phone mock: last post long ago
    px, py, pw, ph = 600, 720, 330, 300
    d.rectangle([px, py, px + pw, py + ph], outline=D_LINE, width=3)
    cell = (pw - 40) / 3
    for r in range(2):
        for c in range(3):
            x0 = px + 10 + c * (cell + 10); y0 = py + 70 + r * (cell + 10)
            d.rectangle([x0, y0, x0 + cell, y0 + cell], fill=D_ALT)
    draw_text(d, (px + 14, py + 46), "Last post", font(24, 600), D_MUTED)
    draw_text(d, (px + pw - 14, py + 46), "11 weeks ago", font(24, 700), AMBER, anchor="rs")
    f = font(34, 500)
    yy = 790
    for ln in ["You run the kitchen.", "We keep your page", "posting, every week."]:
        draw_text(d, (M, yy), ln, f, D_INK); yy += 48
    footer(img, d, True, "Book a 30 minute marketing review", "platsera.com/growth")
    return img


# 2. HVAC, Facebook growth line, light theme -----------------------------
def hvac(t=99):
    img = Image.new("RGBA", (W, H), L_ALT)
    d = ImageDraw.Draw(img)
    eyebrow(d, M, M, "FOR HVAC AND SERVICE BUSINESSES", L_INK, False)
    draw_text(d, (M, 330), "7:42 PM", font(150, 800), L_INK)
    stack(d, t, ["Phone rings.", "Nobody answers.", {"text": "They call the", "color": L_MUTED}, {"text": "next company.", "color": L_MUTED}],
          M, 380, 78, L_ALT, L_INK, weight=700)
    # missed call card
    cx, cy, cw, ch = M, 820, W - 2 * M, 120
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=L_BG, outline=L_LINE, width=2)
    d.rectangle([cx, cy, cx + 10, cy + ch], fill=RED)
    draw_text(d, (cx + 44, cy + 54), "Missed call", font(34, 700), RED_TEXT)
    draw_text(d, (cx + 44, cy + 96), "(630) 555-0142  ·  no voicemail", font(26, 500), L_MUTED)
    draw_text(d, (cx + cw - 40, cy + 54), "7:42 PM", font(28, 600), L_MUTED, anchor="rs")
    # footer on alt bg
    footer(img, d, False, "Book a 30 minute marketing review", "platsera.com/growth")
    return img


def footer_light_alt(img, d, q, url):
    y = H - 300
    d.line([M, y, W - M, y], fill=L_LINE, width=2)
    f = font(36, 600); ly = y + 70
    for ln in wrap(q, f, W - 2 * M):
        draw_text(d, (M, ly), ln, f, L_INK); ly += 48
    lg = logo(250, "light")
    paste(img, lg, M, H - 88 - lg.height)
    draw_text(d, (W - M, H - 88 - lg.height / 2 + 10), url, font(28, 600), L_MUTED, anchor="rs")


# 3. LinkedIn engineering: integration gap, light ------------------------
def system_box(d, x, y, w, h, label, sub, ink=L_INK):
    d.rectangle([x, y, x + w, y + h], fill=L_BG, outline=ink, width=3)
    draw_text(d, (x + w / 2, y + h / 2 + 4), label, font(44, 800), ink, anchor="mm")
    draw_text(d, (x + w / 2, y + h + 44), sub, font(24, 500), L_MUTED, anchor="ms")


def dashed(d, x0, x1, y, color, dash=18, gap=12, width=5, offset=0):
    x = x0 - (offset % (dash + gap))
    while x < x1:
        a, b = max(x, x0), min(x + dash, x1)
        if b > a:
            d.line([a, y, b, y], fill=color, width=width)
        x += dash + gap


def integration(t=99):
    img = Image.new("RGBA", (W, H), L_BG)
    d = ImageDraw.Draw(img)
    eyebrow(d, M, M, "CUSTOM SOFTWARE AND AUTOMATION", L_INK, False)
    stack(d, t, ["Your ERP and", "your WMS don’t talk.", {"text": "So someone on your", "color": L_MUTED}, {"text": "team does it for them.", "color": L_MUTED}],
          M, 250, 74, L_BG, L_INK, weight=750)
    by = 700
    system_box(d, M, by, 260, 150, "ERP", "Orders, invoices")
    system_box(d, W - M - 260, by, 260, 150, "WMS", "Picks, shipments")
    gx0, gx1, gy = M + 260 + 24, W - M - 260 - 24, by + 75
    dashed(d, gx0, gx1, gy, RED)
    d.rectangle([(gx0 + gx1) / 2 - 92, gy - 30, (gx0 + gx1) / 2 + 92, gy + 30], fill=RED_SOFT)
    draw_text(d, ((gx0 + gx1) / 2, gy + 2), "The gap", font(26, 700), RED_TEXT, anchor="mm")
    f = font(32, 500); yy = 965
    for ln in ["We connect the systems you already have,", "so your people stop retyping data."]:
        draw_text(d, (M, yy), ln, f, L_INK); yy += 44
    footer(img, d, False, "Book a free technology review", "platsera.com")
    return img


# 4. LinkedIn engineering: AI agents, light ------------------------------
def agents(t=99):
    img = Image.new("RGBA", (W, H), L_BG)
    d = ImageDraw.Draw(img)
    eyebrow(d, M, M, "AI AGENTS FOR OPERATIONS", L_INK, False)
    stack(d, t, ["AI agents won’t", "replace your team.", {"text": "They replace the", "color": L_MUTED}, {"text": "copy and paste.", "hl": RED, "hl_ink": L_INK}],
          M, 250, 74, L_BG, L_INK, weight=750)
    tasks = ["Read the PO from the inbox", "Check stock in the WMS", "Draft the order in the ERP"]
    y = 700
    panel = [M, y - 20, W - M, y + 3 * 74 + 110]
    d.rectangle(panel, fill=L_ALT)
    for i, tk in enumerate(tasks):
        yy = y + 30 + i * 74
        d.rectangle([M + 36, yy - 14, M + 64, yy + 14], fill=L_INK)
        d.line([M + 42, yy, M + 48, yy + 7, M + 59, yy - 7], fill=L_BG, width=4)
        draw_text(d, (M + 92, yy + 11), tk, font(32, 600), L_INK)
        draw_text(d, (W - M - 36, yy + 11), "Agent", font(24, 600), L_MUTED, anchor="rs")
    yy = y + 30 + 3 * 74
    d.rectangle([M + 36, yy - 14, M + 64, yy + 14], outline=RED, width=4)
    draw_text(d, (M + 92, yy + 11), "Approve anything unusual", font(32, 700), RED_TEXT)
    draw_text(d, (W - M - 36, yy + 11), "Your team", font(24, 700), L_INK, anchor="rs")
    footer(img, d, False, "Book a free technology review", "platsera.com")
    return img


if __name__ == "__main__":
    for name, fn in [("01_fb_restaurant", restaurant), ("02_fb_hvac", hvac),
                     ("03_li_integration_gap", integration), ("04_li_ai_agents", agents)]:
        fn().convert("RGB").save(f"{OUT}/{name}.png")
        print("saved", name)
