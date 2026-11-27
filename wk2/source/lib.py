"""Shared drawing helpers for Platsera sample media."""
import math, subprocess, os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

MONT = "/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf"
BRAND = "/home/claude/brand"

# Platsera tokens
RED = (240, 55, 6)
RED_TEXT = (196, 45, 4)
RED_SOFT = (253, 230, 221)
AMBER = (255, 192, 0)
L_BG = (255, 255, 255); L_ALT = (247, 245, 242); L_LINE = (229, 225, 219)
L_INK = (0, 0, 0); L_MUTED = (92, 88, 82)
D_BG = (17, 17, 17); D_ALT = (28, 28, 28); D_LINE = (51, 48, 44)
D_INK = (245, 243, 240); D_MUTED = (168, 163, 156)


@lru_cache(maxsize=256)
def font(size, weight=700):
    f = ImageFont.truetype(MONT, int(size))
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


@lru_cache(maxsize=8)
def _logo(kind):
    im = Image.open(f"{BRAND}/logo-{kind}.png").convert("RGBA")
    return im.crop(im.getbbox())


def logo(width, kind="light", alpha=1.0):
    im = _logo(kind)
    h = round(im.height * width / im.width)
    im = im.resize((int(width), h), Image.LANCZOS)
    if alpha < 1:
        a = im.getchannel("A").point(lambda v: int(v * alpha))
        im.putalpha(a)
    return im


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(p):
    p = clamp(p)
    return 1 - (1 - p) ** 3


def ease_in_out(p):
    p = clamp(p)
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


def back_out(p, s=1.6):
    p = clamp(p)
    p -= 1
    return p * p * ((s + 1) * p + s) + 1


def lerp(a, b, p):
    return a + (b - a) * p


def mix(c1, c2, p):
    p = clamp(p)
    return tuple(int(round(lerp(a, b, p))) for a, b in zip(c1, c2))


def prog(t, start, dur):
    return clamp((t - start) / dur)


def text_w(txt, f):
    return f.getlength(txt)


def draw_text(d, xy, txt, f, fill, anchor="ls"):
    d.text(xy, txt, font=f, fill=fill, anchor=anchor)


def wrap(txt, f, maxw):
    words, lines, cur = txt.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if f.getlength(trial) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def stack(d, t, lines, x, y, size, bg, ink, start=0.0, stagger=0.18, dur=0.4,
          weight=800, lh=1.12, rise=46, out_start=None, out_dur=0.3, align="left", W=1080):
    """Kinetic stacked headline. lines: list of str or dict(text, hl=color, hl_ink=color, color=)
    Returns bottom y."""
    cy = y
    for i, ln in enumerate(lines):
        if isinstance(ln, str):
            ln = {"text": ln}
        sz = ln.get("size", size)
        f = font(sz, ln.get("weight", weight))
        cy += sz * lh if i else sz
        p = ease_out(prog(t, start + i * stagger, dur))
        po = 0.0
        if out_start is not None:
            po = ease_in_out(prog(t, out_start + i * 0.05, out_dur))
        vis = p * (1 - po)
        if vis <= 0:
            continue
        dy = (1 - p) * rise - po * rise * 0.6
        tw = text_w(ln["text"], f)
        lx = x if align == "left" else (W - tw) / 2
        col = ln.get("color", ink)
        hl = ln.get("hl")
        if hl:
            # wipe-in block behind the line
            wp = ease_out(prog(t, start + i * stagger + 0.12, 0.45)) * (1 - po)
            pad_x, pad_t, pad_b = sz * 0.22, sz * 0.86, sz * 0.26
            bx0 = lx - pad_x
            bx1 = bx0 + (tw + 2 * pad_x) * wp
            if wp > 0:
                d.rectangle([bx0, cy + dy - pad_t, bx1, cy + dy + pad_b], fill=hl)
            col = mix(col, ln.get("hl_ink", col), wp)
            draw_text(d, (lx, cy + dy), ln["text"], f, mix(bg, col, vis))
        else:
            draw_text(d, (lx, cy + dy), ln["text"], f, mix(bg, col, vis))
    return cy


def paste(img, im, x, y):
    img.alpha_composite(im, (int(x), int(y))) if img.mode == "RGBA" else img.paste(im, (int(x), int(y)), im)


class SceneWriter:
    """Pipes raw frames into ffmpeg; one mp4 per scene."""
    def __init__(self, path, W, H, fps=30):
        self.path, self.tmp = path, path[:-4] + ".part.mp4"
        self.p = subprocess.Popen([
            "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-r", str(fps), self.tmp], stdin=subprocess.PIPE)

    def write(self, img):
        self.p.stdin.write(img.convert("RGB").tobytes())

    def close(self):
        self.p.stdin.close()
        if self.p.wait() == 0:
            os.replace(self.tmp, self.path)
        else:
            raise RuntimeError("ffmpeg failed " + self.path)
