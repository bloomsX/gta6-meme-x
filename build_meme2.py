#!/usr/bin/env python3
"""Round 2 meme v5: COMIC STRIP — 4 panels, varied scenes, clear story flow.

The user said the single-image versions are monotonous: this is a 2x2
comic strip with a beginning, middle and punchline, each panel a
DIFFERENT scene, with numbered time-label pills so the story reads
instantly:
  1 · 2013            — young hopeful Speed: "GTA 6 is coming... right?"
  2 · 13 YEARS LATER  — calendars fly, years tick by, greyed-out Speed:
                        "any day now..."
  3 · 2026            — GTA VI is here: real Lucia & Jason key art,
                        Speed screaming "IT'S HERE!!"
  4 · 13 MINUTES LATER— smug make.fun ghost on a money pile:
                        "ALREADY PAID! in 13 minutes, bro"
Title strip keeps "ISHOWSPEED WAITED 13 YEARS FOR GTA 6"; footer keeps
"MY AI AGENT GOT PAID IN 13 MINUTES" in gold.
Reuses the real GTA VI key art (gta6-keyart-beach-logos.jpg) and the real
IShowSpeed photo cutout (speed-cutout.png). PIL only — no AI image gen.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os
import random

BASE = "/home/hatch/workspace/gta6-meme-x/gta6-keyart-beach-logos.jpg"
CUTOUT = "/home/hatch/workspace/gta6-meme-x/speed-cutout.png"
OUT = "/home/hatch/workspace/gta6-meme-x/meme.png"
CHECK = "/tmp/meme2-480-check.png"
W, H = 1200, 675
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PW, PH = 582, 270          # panel size
TITLE_H, FOOT_H = 50, 49
M = 12                     # margin / gutter
PANEL_X = (M, M + PW + M)          # 12, 606
PANEL_Y = (TITLE_H + M, TITLE_H + M + PH + M)  # 62, 344


def F(size):
    return ImageFont.truetype(FONT_PATH, size)


def vgrad(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)
    return img


def pill(d, x, y, text, size=20, bg="black", fg="white"):
    f = F(size)
    b = d.textbbox((0, 0), text, font=f)
    w = b[2] - b[0] + 24
    h = size + 14
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2,
                        fill=bg, outline="white", width=2)
    d.text((x + 12 - b[0], y + 6), text, font=f, fill=fg)
    return w, h


def bubble(d, box, lines, tail_pt=None, tail_side="bottom"):
    """lines: list of (text, font). White rounded bubble + optional tail."""
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=14, fill="white", outline="black",
                        width=3)
    if tail_pt:
        mx = min(max(tail_pt[0], x0 + 22), x1 - 22)
        if tail_side == "bottom":
            d.polygon([(mx - 13, y1 - 2), tail_pt, (mx + 13, y1 - 2)],
                      fill="white", outline="black")
            d.line([(mx - 13, y1 - 2), (mx + 13, y1 - 2)], fill="white",
                   width=3)
        else:
            d.polygon([(mx - 13, y0 + 2), tail_pt, (mx + 13, y0 + 2)],
                      fill="white", outline="black")
            d.line([(mx - 13, y0 + 2), (mx + 13, y0 + 2)], fill="white",
                   width=3)
    th = sum(f.size for _, f in lines) + 5 * (len(lines) - 1)
    y = y0 + (y1 - y0 - th) // 2
    for text, f in lines:
        b = d.textbbox((0, 0), text, font=f)
        d.text(((x0 + x1 - (b[2] - b[0])) // 2 - b[0], y), text, font=f,
               fill="black")
        y += f.size + 5


def make_bill():
    bill = Image.new("RGBA", (64, 30), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bill)
    bd.rounded_rectangle([0, 0, 63, 29], radius=4, fill=(18, 150, 60, 255),
                         outline=(8, 90, 35, 255), width=2)
    bd.text((24, 4), "$", font=F(18), fill="white")
    return bill


def ghost_layer():
    """Smug make.fun ghost with sunglasses, cash fan, coin, money bag
    and money pile — drawn once on a transparent layer, then scaled."""
    L = Image.new("RGBA", (340, 360), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    # body + wavy hem
    d.rounded_rectangle([105, 60, 215, 225], radius=48, fill="white",
                        outline="black", width=5)
    for cx in (105, 135, 160, 185, 215):
        d.ellipse([cx - 15, 208, cx + 15, 242], fill="white",
                  outline="black", width=4)
    # sunglasses + smug smile
    d.rounded_rectangle([122, 92, 156, 120], radius=8, fill="black")
    d.rounded_rectangle([164, 92, 198, 120], radius=8, fill="black")
    d.line([(156, 106), (164, 106)], fill="black", width=4)
    d.line([(130, 98), (146, 98)], fill="white", width=3)
    d.line([(174, 98), (190, 98)], fill="white", width=3)
    d.arc([146, 124, 174, 148], 15, 165, fill="black", width=3)
    # right arm + magenta coin with white star
    d.line([(210, 175), (252, 148)], fill="white", width=9)
    d.ellipse([236, 118, 282, 164], fill=(255, 46, 136),
              outline="white", width=3)
    scx, scy, sr = 259, 141, 12
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rr = sr if i % 2 == 0 else sr * 0.42
        pts.append((scx + rr * math.cos(a), scy + rr * math.sin(a)))
    d.polygon(pts, fill="white")
    # left arm fanning a wad of cash
    d.line([(105, 175), (72, 152)], fill="white", width=9)
    for k, ang in enumerate((-35, 0, 35)):
        fan = Image.new("RGBA", (36, 20), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fan)
        fd.rounded_rectangle([0, 0, 35, 19], radius=3,
                             fill=(18, 150, 60, 255),
                             outline=(8, 90, 35, 255), width=2)
        fd.text((13, 3), "$", font=F(13), fill="white")
        fan = fan.rotate(ang, expand=True, resample=Image.BICUBIC)
        L.paste(fan, (38 + k * 13, 118 + k * 7), fan)
    # money bag at feet
    d.ellipse([136, 228, 184, 262], fill=(34, 139, 34),
              outline="black", width=3)
    d.polygon([(148, 230), (172, 230), (160, 214)], fill=(34, 139, 34),
              outline="black")
    d.text((152, 238), "$", font=F(20), fill="white", stroke_width=2,
           stroke_fill="black")
    # money pile under the body
    for (bx, by) in [(196, 258), (200, 246), (196, 234)]:
        d.rounded_rectangle([bx, by, bx + 56, by + 15], radius=3,
                            fill=(18, 150, 60), outline=(8, 90, 35),
                            width=2)
        d.text((bx + 24, by + 1), "$", font=F(11), fill="white")
    return L


# --- shared assets ---------------------------------------------------------
cut = Image.open(CUTOUT).convert("RGBA")
# rembg leaves a faint grey halo around the hair — crop to solid pixels
_alpha = cut.split()[3]
_mask = _alpha.point(lambda a: 255 if a > 140 else 0)
_bbox = _mask.getbbox()
if _bbox:
    cut = cut.crop(_bbox)
_grey = cut.convert("L")
cut_grey = Image.merge("RGBA", (_grey, _grey, _grey, cut.split()[3]))
print("speed cutout:", cut.size)


def place_speed(p, img, height, x, y):
    w = int(img.width * height / img.height)
    c = img.resize((w, height), Image.LANCZOS)
    p.paste(c, (x, y), c)
    return (x, y, w, height)


# --- panel 1: 2013 — bright hopeful morning ------------------------------
def panel1():
    p = vgrad(PW, PH, (126, 200, 247), (223, 243, 255))
    d = ImageDraw.Draw(p, "RGBA")
    # sun peeking between bubble and Speed
    d.ellipse([340, 6, 382, 48], fill=(255, 220, 60),
              outline="white", width=3)
    # clouds
    for (cx, cy, s) in [(60, 42, 1.0), (250, 26, 0.8)]:
        d.ellipse([cx, cy, cx + 70 * s, cy + 26 * s], fill="white")
        d.ellipse([cx + 18 * s, cy - 12 * s, cx + 62 * s, cy + 14 * s],
                  fill="white")
    # grass strip
    d.rectangle([0, PH - 26, PW, PH], fill=(110, 190, 80))
    # little 2013 calendar
    cal = Image.new("RGBA", (120, 86), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cal)
    cd.rounded_rectangle([0, 0, 119, 85], radius=8, fill="white",
                         outline="black", width=3)
    cd.rectangle([3, 3, 116, 28], fill=(220, 40, 40))
    cd.text((30, 6), "2013", font=F(18), fill="white")
    for i in range(3):
        for j in range(4):
            cd.rectangle([12 + i * 28, 36 + j * 12, 34 + i * 28,
                          44 + j * 12], outline=(150, 150, 150), width=1)
    cd.ellipse([66, 38, 88, 54], outline=(220, 40, 40), width=3)
    p.paste(cal, (28, 168), cal)
    # bubble
    bubble(d, (18, 50, 332, 126),
           [("GTA 6 is coming...", F(24)), ("right?", F(24))],
           tail_pt=(450, 150))
    # Speed, big and excited, bottom-right (right-aligned, head clears top)
    _w1 = int(cut.width * 200 / cut.height)
    place_speed(p, cut, 200, PW - _w1 - 8, PH - 200 - 4)
    pill(d, 12, 10, "1 · 2013")
    return p


# --- panel 2: 13 YEARS LATER — calendars fly, years tick by ---------------
def panel2():
    p = vgrad(PW, PH, (96, 84, 128), (205, 195, 220))
    d = ImageDraw.Draw(p, "RGBA")
    # flying calendar pages (kept clear of Speed's head, top-right)
    for (px, py, ang, yr) in [(40, 52, -18, "2015"), (290, 36, 12, "2019"),
                              (415, 30, -8, "2023")]:
        pg = Image.new("RGBA", (86, 60), (0, 0, 0, 0))
        g = ImageDraw.Draw(pg)
        g.rounded_rectangle([0, 0, 85, 59], radius=6, fill="white",
                            outline="black", width=2)
        g.rectangle([2, 2, 83, 20], fill=(180, 60, 60))
        g.text((28, 4), yr, font=F(14), fill="white")
        for i in range(3):
            g.line([(10, 28 + i * 9), (76, 28 + i * 9)],
                   fill=(170, 170, 170), width=1)
        pg = pg.rotate(ang, expand=True, resample=Image.BICUBIC)
        p.paste(pg, (px, py), pg)
    # timeline 2013 -> 2026 (2026 end sits behind Speed's head)
    d.line([(30, 132), (552, 132)], fill="white", width=4)
    for tx in (30, 135, 240, 345, 450, 552):
        d.ellipse([tx - 6, 126, tx + 6, 138], fill=(255, 210, 0),
                  outline="black", width=2)
    d.text((30, 142), "2013", font=F(18), fill="white", stroke_width=2,
           stroke_fill="black")
    # bubble (tail up toward the tired grey Speed)
    bubble(d, (18, 168, 300, 232), [("any day now...", F(26))],
           tail_pt=(450, 140), tail_side="top")
    # greyed-out, worn-out Speed, bottom-right (head clears top)
    _w2 = int(cut_grey.width * 180 / cut_grey.height)
    place_speed(p, cut_grey, 180, PW - _w2 - 8, PH - 180 - 4)
    pill(d, 12, 10, "2 · 13 YEARS LATER")
    return p


# --- panel 3: 2026 — GTA VI is here (real key art) -------------------------
def panel3():
    p = vgrad(PW, PH, (255, 110, 170), (255, 180, 70))
    d = ImageDraw.Draw(p, "RGBA")
    # real Lucia & Jason key art on the right 380 px
    ka = Image.open(BASE).convert("RGB")
    crop = ka.crop((850, 0, 1920, 760)).resize((380, PH), Image.LANCZOS)
    p.paste(crop, (PW - 380, 0))
    d.line([(PW - 380, 0), (PW - 380, PH)], fill="black", width=4)
    # "IT'S HERE!!" starburst behind Speed's head (clears his hair)
    bcx, bcy = 95, 42
    pts = []
    for i in range(16):
        a = math.radians(i * 22.5)
        rr = 46 if i % 2 == 0 else 28
        pts.append((bcx + rr * math.cos(a), bcy + rr * math.sin(a)))
    d.polygon(pts, fill=(255, 211, 25), outline="black")
    for j, line in enumerate(["IT'S", "HERE!!"]):
        f = F(20)
        b = d.textbbox((0, 0), line, font=f, stroke_width=2)
        d.text((bcx - (b[2] - b[0]) // 2 - b[0], bcy - 24 + j * 24), line,
               font=f, fill="black", stroke_width=2, stroke_fill="white")
    # Speed screaming with joy, bottom-left zone (head clears top)
    place_speed(p, cut, 175, 4, PH - 175 - 4)
    pill(d, 430, 10, "3 · 2026")
    return p


# --- panel 4: 13 MINUTES LATER — the ghost got paid ------------------------
def panel4():
    p = vgrad(PW, PH, (28, 10, 48), (74, 22, 104))
    d = ImageDraw.Draw(p, "RGBA")
    # money raining
    random.seed(7)
    for (bx, by) in [(220, 70), (270, 120), (520, 80), (560, 150),
                     (250, 180)]:
        b = make_bill().rotate(random.randint(-40, 40), expand=True,
                               resample=Image.BICUBIC)
        p.paste(b, (bx, by), b)
    # ghost bubble (tail down to the ghost's head)
    bubble(d, (285, 8, 575, 66),
           [("ALREADY PAID!", F(22)), ("in 13 minutes, bro", F(18))],
           tail_pt=(430, 80))
    # smug ghost on his money pile, right side
    g = ghost_layer()
    gh = 195
    gw = int(g.width * gh / g.height)
    g = g.resize((gw, gh), Image.LANCZOS)
    p.paste(g, (360, PH - gh - 4), g)
    # small deflated Speed, bottom-left
    bubble(d, (12, 48, 205, 98), [("wait... what?", F(20))],
           tail_pt=(85, 120))
    place_speed(p, cut, 150, 10, PH - 150 - 4)
    pill(d, 12, 10, "4 · 13 MINUTES LATER")
    return p


# --- assemble the comic page ------------------------------------------------
page = Image.new("RGB", (W, H), "white")
dp = ImageDraw.Draw(page)

panels = [panel1(), panel2(), panel3(), panel4()]
for (px, py), pan in zip(
        [(PANEL_X[0], PANEL_Y[0]), (PANEL_X[1], PANEL_Y[0]),
         (PANEL_X[0], PANEL_Y[1]), (PANEL_X[1], PANEL_Y[1])], panels):
    page.paste(pan, (px, py))
    dp.rectangle([px, py, px + PW - 1, py + PH - 1], outline="black",
                 width=4)


def draw_centered(text, y, size, fill="white"):
    f = F(size)
    b = dp.textbbox((0, 0), text, font=f, stroke_width=4)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    dp.text((x, y), text, font=f, fill=fill, stroke_width=4,
            stroke_fill="black")


dp.rectangle([0, 0, W, TITLE_H], fill="black")
draw_centered("ISHOWSPEED WAITED 13 YEARS FOR GTA 6", 8, 34)
dp.rectangle([0, H - FOOT_H, W, H], fill="black")
draw_centered("MY AI AGENT GOT PAID IN 13 MINUTES", H - FOOT_H + 8, 34,
              fill=(255, 210, 0))

page.save(OUT, "PNG")
print("saved", OUT, page.size, os.path.getsize(OUT), "bytes")
small = page.resize((480, 270), Image.LANCZOS)
small.save(CHECK, "PNG")
print("saved", CHECK, small.size)
