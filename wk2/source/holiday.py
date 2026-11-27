from PIL import Image, ImageDraw
from lib import *
import images as I
W, H, M = 1080, 1350, 88

def holiday(t=99):
    img = Image.new("RGBA", (W, H), L_BG)
    d = ImageDraw.Draw(img)
    I.eyebrow(d, M, M, "FOR LOCAL SHOP OWNERS", L_INK, False)
    stack(d, t, ["Open till 9 for", "the holidays?", {"text": "Google says 6 PM.", "hl": AMBER, "hl_ink": L_INK}],
          M, 250, 80, L_BG, L_INK, weight=800)
    y = 590
    d.rectangle([M, y, W - M, y + 390], fill=L_ALT)
    draw_text(d, (M + 40, y + 70), "Your door", font(32, 600), L_INK)
    draw_text(d, (W - M - 40, y + 70), "Open till 9 PM", font(32, 800), L_INK, anchor="rs")
    d.line([M + 40, y + 108, W - M - 40, y + 108], fill=L_LINE, width=2)
    for i, app in enumerate(["Google", "Apple Maps", "Yelp"]):
        yy = y + 175 + i * 75
        draw_text(d, (M + 40, yy), app, font(32, 500), L_MUTED)
        draw_text(d, (W - M - 40, yy), "Closes 6 PM", font(32, 700), RED_TEXT, anchor="rs")
    draw_text(d, (M + 40, y + 360), "Illustrative example", font(22, 500), L_MUTED)
    I.footer(img, d, False, "Book a 30 minute marketing review", "platsera.com/growth")
    return img

holiday().convert("RGB").save("out/08_fb_retail_holiday_hours.png")
