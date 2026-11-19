#!/usr/bin/env python3
"""Build meme.png: base scene + PIL caption overlay (top/bottom bands)."""
from PIL import Image, ImageDraw, ImageFont
import os

SRC = "/home/hatch/workspace/gta6-meme-x/media-generation-gta6-meme-base-0-e8d3f8b9-412f-4476-85a6-15b6baf80abe.png"
OUT = "/home/hatch/workspace/gta6-meme-x/meme.png"
CHECK = "/tmp/meme-480-check.png"

W, H = 1200, 675

def find_font():
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]:
        if os.path.exists(p):
            return p
    raise SystemExit("no bold font found")

FONT = find_font()
print("font:", FONT)

im = Image.open(SRC).convert("RGB").resize((W, H), Image.LANCZOS)

# semi-transparent black bands top/bottom for caption readability
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
od.rectangle([0, 0, W, 92], fill=(0, 0, 0, 165))
od.rectangle([0, H - 92, W, H], fill=(0, 0, 0, 165))
im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
d = ImageDraw.Draw(im)

def fit_font(text, start, max_w):
    size = start
    while size > 20:
        f = ImageFont.truetype(FONT, size)
        if d.textbbox((0, 0), text, font=f, stroke_width=3)[2] <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(FONT, 20)

def draw_centered(text, y, start_size):
    f = fit_font(text, start_size, W - 40)
    bbox = d.textbbox((0, 0), text, font=f, stroke_width=4)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2 - bbox[0]
    d.text((x, y), text, font=f, fill="white", stroke_width=4, stroke_fill="black")
    print(f"text {text!r} size={f.size} width={tw} y={y}")

draw_centered("SORRY BOSS, I'VE GOT LEONIDA FLU", 14, 54)
draw_centered("GTA 6 LAUNCH DAY", H - 82, 58)

im.save(OUT, "PNG")
print("saved", OUT, im.size, os.path.getsize(OUT), "bytes")

# 480px-wide downscale check (judge view shrinks to ~768x432; 480px is stricter)
small = im.resize((480, 270), Image.LANCZOS)
small.save(CHECK, "PNG")
print("saved", CHECK, small.size)
