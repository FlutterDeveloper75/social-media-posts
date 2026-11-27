import lib
lib.BRAND = "/home/claude/v2/assets"
from PIL import Image, ImageDraw
from lib import *
W, H, M = 1080, 1350, 88
CW = W - 2 * M

def fit(txt, size, weight, maxw):
    while font(size, weight).getlength(txt) > maxw and size > 20: size -= 2
    return font(size, weight), size

def post(band, band_sub, tag, hook, prices, note, deadline, url, out):
    img = Image.new("RGBA", (W, H), L_BG); d = ImageDraw.Draw(img)
    # Black Friday banner
    d.rectangle([0, 0, W, 230], fill=D_BG)
    f, s = fit(band, 112, 800, CW)
    draw_text(d, (M, 150), band, f, (255, 255, 255))
    if band_sub:
        draw_text(d, (M, 205), band_sub, font(34, 700), AMBER)
    # audience + hook
    draw_text(d, (M, 312), tag, font(32, 800), RED_TEXT)
    y = 312 + 26
    hs = min(fit(ln, 58, 800, CW)[1] for ln in hook)
    for ln in hook:
        y += int(hs * 1.18); draw_text(d, (M, y), ln, font(hs, 800), L_INK)
    # the deal
    y += 70
    txt = "50% OFF"; big, bs = fit(txt, 200, 800, CW - 40)
    tw = big.getlength(txt)
    d.rectangle([M, y + 4, M + tw + 36, y + bs - 4], fill=AMBER)
    draw_text(d, (M + 18, y + int(bs * .86)), txt, big, L_INK)
    y += bs + 76
    draw_text(d, (M, y), "your first month", font(64, 800), L_INK)
    y += 62
    draw_text(d, (M, y), prices, font(44, 700), L_MUTED)
    if note:
        y += 50; draw_text(d, (M, y), note, font(34, 600), L_MUTED)
    y += 66
    draw_text(d, (M, y), deadline, font(44, 800), RED_TEXT)
    # footer
    fy = H - 250
    d.line([M, fy, W - M, fy], fill=L_LINE, width=2)
    draw_text(d, (M, fy + 70), "Book a 30 minute marketing review", fit("Book a 30 minute marketing review", 50, 800, CW)[0], L_INK)
    draw_text(d, (M, fy + 118), "Link in the caption", font(34, 600), L_MUTED)
    lg = logo(230, "light"); paste(img, lg, M, H - 64 - lg.height)
    uf, _ = fit(url, 34, 700, CW - 270)
    draw_text(d, (W - M, H - 64 - lg.height / 2 + 12), url, uf, L_INK, anchor="rs")
    img.convert("RGB").save(out)
    return y

DL = "Ends Mon, Nov 30, 11:59 PM CT"
HV = "platsera.com/growth/home-services"
RS = "platsera.com/growth"
O = "/home/claude/social-media-posts/bf2026/"
print(post("BLACK FRIDAY", None, "FOR HVAC OWNERS", ["Furnaces work hard this weekend.", "Can homeowners find you?"],
     "Starter $149.50 · Local $299.50", None, DL, HV, O + "bf1-hvac-fri.png"))
print(post("BLACK FRIDAY", "SMALL BUSINESS SATURDAY", "FOR RESTAURANT OWNERS", ["People pick a local spot today.", "Will they pick you?"],
     "Starter $149.50 · Local $299.50", "Then the founding rate, locked 12 months", DL, RS, O + "bf2-restaurant-sat.png"))
print(post("BLACK FRIDAY", None, "FOR PLUMBERS", ["Holiday guests, busy pipes.", "Is your Google profile ready?"],
     "Starter $149.50 · Local $299.50", None, DL, HV, O + "bf3-plumbers-sun.png"))
print(post("BLACK FRIDAY", "LAST DAY · CYBER MONDAY", "FOR RESTAURANT OWNERS", ["Last day to lock in the deal."],
     "Starter $149.50 · Local $299.50", "Then the founding rate, locked 12 months", "Ends tonight, 11:59 PM CT", RS, O + "bf4-restaurant-mon.png"))
print(post("BLACK FRIDAY", "LAST CALL", "RESTAURANTS AND SERVICE BUSINESSES", ["Ends tonight.", "We take on 6 new businesses a month."],
     "Starter $149.50 · Local $299.50", None, "Ends tonight, 11:59 PM CT", RS, O + "bf5-lastcall-mon.png"))
