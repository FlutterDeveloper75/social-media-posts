import lib
lib.BRAND = "/home/claude/v2/assets"
from PIL import Image, ImageDraw
from lib import *
import images as I
W, H, M = 1080, 1350, 88

def hvac_reviews(t=99):
    img = Image.new("RGBA", (W, H), L_BG)
    d = ImageDraw.Draw(img)
    I.eyebrow(d, M, M, "FOR HVAC OWNERS", L_INK, False)
    stack(d, t, ["Furnace out tonight?", "They call the shop",
                 {"text": "with fresh reviews.", "hl": AMBER, "hl_ink": L_INK}],
          M, 250, 80, L_BG, L_INK, weight=800)
    y = 610
    d.rectangle([M, y, W - M, y + 330], fill=L_ALT)
    draw_text(d, (M + 40, y + 70), "furnace repair near me", font(30, 600), L_MUTED)
    d.line([M + 40, y + 108, W - M - 40, y + 108], fill=L_LINE, width=2)
    rows = [("Your shop", "Last review 8 months ago", RED_TEXT),
            ("Next shop", "Last review 2 days ago", L_INK)]
    for i, (name, sub, col) in enumerate(rows):
        yy = y + 180 + i * 75
        draw_text(d, (M + 40, yy), name, font(32, 700), L_INK)
        draw_text(d, (W - M - 40, yy), sub, font(30, 600), col, anchor="rs")
    draw_text(d, (M + 40, y + 305), "Illustrative example", font(22, 500), L_MUTED)
    I.footer(img, d, False, "Book a 30 minute marketing review", "platsera.com/growth")
    return img

hvac_reviews().convert("RGB").save("out/fb-hvac-winter-reviews.png")
