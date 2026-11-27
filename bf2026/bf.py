import lib
lib.BRAND = "/home/claude/v2/assets"
from PIL import Image, ImageDraw
from lib import *
import images as I
W, H, M = 1080, 1350, 88

def post(tag, lines, offer, sub, url, out, deadline="Book your review by Mon, Nov 30, 11:59 PM CT"):
    img = Image.new("RGBA", (W, H), L_BG)
    d = ImageDraw.Draw(img)
    I.eyebrow(d, M, M, tag, L_INK, False)
    bottom = stack(d, 99, lines, M, 250, 78, L_BG, L_INK, weight=800)
    y = int(bottom) + 70
    d.rectangle([M, y, W - M, y + 300], fill=L_ALT)
    draw_text(d, (M + 44, y + 92), offer, font(58, 800), L_INK)
    yy = y + 150
    for ln in sub:
        draw_text(d, (M + 44, yy), ln, font(30, 600), L_MUTED); yy += 44
    draw_text(d, (M + 44, y + 266), deadline, font(28, 700), RED_TEXT)
    I.footer(img, d, False, "Book a 30 minute marketing review", url)
    img.convert("RGB").save(out)

O = "out/"
post("FOR HVAC OWNERS · BLACK FRIDAY",
     ["Furnaces work hard", "this weekend.", "Can homeowners", {"text": "find you fast?", "hl": AMBER, "hl_ink": L_INK}],
     "First month half off", ["Starter $149.50 or Local $299.50", "for your first month"],
     "platsera.com/growth/home-services", O + "bf1-hvac-fri.png")
post("FOR RESTAURANT OWNERS · SMALL BUSINESS SATURDAY",
     ["Today people choose", "a local spot.", {"text": "Will they choose you?", "hl": AMBER, "hl_ink": L_INK}],
     "First month half off", ["Then the founding rate, locked", "for 12 months (first 20 restaurants)"],
     "platsera.com/growth", O + "bf2-restaurant-sat.png")
post("FOR PLUMBERS · HOLIDAY WEEKEND",
     ["Holiday guests,", "busy pipes.", "Is your Google", {"text": "profile ready?", "hl": AMBER, "hl_ink": L_INK}],
     "First month half off", ["Starter $149.50 or Local $299.50", "for your first month"],
     "platsera.com/growth/home-services", O + "bf3-plumbers-sun.png")
post("FOR RESTAURANT OWNERS · CYBER MONDAY",
     ["Last day for", {"text": "half off", "hl": AMBER, "hl_ink": L_INK}, "your first month."],
     "Ends tonight", ["Starter $149.50 or Local $299.50 first month,", "then the founding rate for 12 months"],
     "platsera.com/growth", O + "bf4-restaurant-mon.png")
post("RESTAURANTS AND SERVICE BUSINESSES",
     ["Last call.", "Half off your first", {"text": "month ends tonight.", "hl": AMBER, "hl_ink": L_INK}],
     "Ends 11:59 PM Central", ["We take on 6 new businesses a month.", "Book the review, then decide."],
     "platsera.com/growth", O + "bf5-lastcall-mon.png", deadline="Book your review by tonight, Mon, Nov 30")
print("built")
