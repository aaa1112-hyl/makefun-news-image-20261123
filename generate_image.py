"""Draw the front page for THE WORLD, Monday 23 November 2026.

A single 1024x1024 PNG summing up the day's world news: one lead story
plus seven captioned panels, all drawn in code with Pillow so every word
stays crisp. Run: python3 generate_image.py  (writes entry.png next to it)
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
RED = (176, 42, 32)
TEAL = (14, 107, 107)
GREEN = (26, 122, 46)
GREY = (90, 86, 78)
LIGHT = (226, 219, 203)
BLUE = (28, 74, 128)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, spacing=4):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def burst(draw, cx, cy, r, fill):
    """Simple starburst (explosion) of triangles around a centre."""
    import math

    pts = []
    for i in range(12):
        ang = math.pi * i / 6
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def waves(draw, x0, y, x1, fill=BLUE):
    for x in range(x0, x1, 26):
        draw.arc([x, y, x + 24, y + 14], 180, 360, fill=fill, width=3)

def draw_chip_chart(draw, x, y, w, h):
    """Green microchip with a rising stock chart above it."""
    # chart
    pts = [(x + 8, y + h - 78), (x + 52, y + h - 96), (x + 92, y + h - 84),
           (x + 132, y + h - 118), (x + 176, y + h - 132), (x + 216, y + h - 152)]
    draw.line(pts, fill=GREEN, width=7, joint="curve")
    draw.polygon([(x + 216, y + h - 152), (x + 196, y + h - 150),
                  (x + 212, y + h - 132)], fill=GREEN)
    draw.text((x + 8, y + 4), "+30%", font=SANS_B(34), fill=GREEN)
    # chip
    cx, cy, cw, ch = x + 70, y + h - 62, 120, 52
    for dx in (-14, 0, 14):
        pass
    for i in range(3):
        px = cx + 18 + i * 42
        draw.line([(px, cy - 12), (px, cy)], fill=INK, width=4)
        draw.line([(px, cy + ch), (px, cy + ch + 12)], fill=INK, width=4)
    for j in range(2):
        py = cy + 14 + j * 24
        draw.line([(cx - 12, py), (cx, py)], fill=INK, width=4)
        draw.line([(cx + cw, py), (cx + cw + 12, py)], fill=INK, width=4)
    draw.rectangle([cx, cy, cx + cw, cy + ch], fill=GREEN, outline=INK, width=3)
    draw.rectangle([cx + 40, cy + 14, cx + 80, cy + ch - 14],
                   fill=(210, 240, 210), outline=INK, width=2)


def draw_warship(draw, x, y, w, h):
    """Grey warship with an orange explosion above it, on waves."""
    burst(draw, x + w - 52, y + 26, 34, (240, 140, 30))
    burst(draw, x + w - 52, y + 26, 20, (250, 210, 60))
    # hull
    draw.polygon([(x + 10, y + h - 52), (x + w - 16, y + h - 52),
                  (x + w - 46, y + h - 22), (x + 34, y + h - 22)], fill=(96, 100, 104))
    draw.rectangle([x + 60, y + h - 84, x + 150, y + h - 52], fill=(120, 124, 128))
    draw.line([(x + 92, y + h - 118), (x + 92, y + h - 84)], fill=INK, width=5)
    draw.line([(x + 92, y + h - 118), (x + 128, y + h - 104)], fill=RED, width=5)
    waves(draw, x + 6, y + h - 16, x + w - 6)


def draw_tanker_mine(draw, x, y, w, h):
    """Oil tanker passing a spiked sea mine, on waves."""
    # mine (kept well left of the text column)
    mx, my = x + 112, y + 56
    draw.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=INK)
    for dx, dy in [(-15, 0), (15, 0), (0, -15), (0, 15), (-11, -11),
                   (11, -11), (-11, 11), (11, 11)]:
        draw.line([(mx, my), (mx + dx, my + dy)], fill=INK, width=3)
    # tanker
    draw.polygon([(x + 8, y + h - 62), (x + w - 40, y + h - 62),
                  (x + w - 60, y + h - 30), (x + 28, y + h - 30)], fill=(150, 60, 40))
    for i in range(3):
        tx = x + 30 + i * 34
        draw.ellipse([tx, y + h - 88, tx + 28, y + h - 62], fill=(200, 200, 200),
                     outline=INK, width=2)
    draw.rectangle([x + w - 78, y + h - 92, x + w - 46, y + h - 62],
                   fill=(220, 220, 220), outline=INK, width=2)
    waves(draw, x + 6, y + h - 22, x + w - 6)


def draw_building_smoke(draw, x, y, w, h):
    """Apartment block with smoke rising from a damaged corner."""
    draw.rectangle([x + 26, y + 44, x + 96, y + h - 20], fill=(150, 140, 120),
                   outline=INK, width=3)
    draw.rectangle([x + 96, y + 66, x + 150, y + h - 20], fill=(120, 112, 96),
                   outline=INK, width=3)
    for r in range(3):
        for c in range(2):
            wx = x + 38 + c * 28
            wy = y + 58 + r * 26
            draw.rectangle([wx, wy, wx + 16, wy + 14], fill=(240, 235, 220),
                           outline=INK, width=1)
    # broken corner + smoke (kept inside the icon box, left of the text)
    draw.polygon([(x + 96, y + 44), (x + 150, y + 66), (x + 150, y + 44)],
                 fill=(60, 58, 52))
    for i, (sx, sy, sr) in enumerate([(118, 26, 9), (132, 12, 11), (144, 24, 8)]):
        draw.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                     fill=(170, 168, 160))


def draw_globe_crack(draw, x, y, w, h):
    """A globe split by a crack, over a conference table line."""
    cx, cy, r = x + w // 2, y + h // 2 - 6, 52
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 180, 200),
                 outline=INK, width=3)
    draw.ellipse([cx - 26, cy - 30, cx + 6, cy - 2], fill=(90, 160, 90))
    draw.ellipse([cx - 4, cy + 12, cx + 30, cy + 34], fill=(90, 160, 90))
    draw.line([(cx - 8, cy - 52), (cx + 4, cy - 18), (cx - 10, cy + 6),
               (cx + 8, cy + 30), (cx - 2, cy + 52)], fill=RED, width=5)
    draw.line([(x + 10, y + h - 14), (x + w - 10, y + h - 14)], fill=INK, width=4)


def draw_ball(draw, x, y, w, h):
    """A football with a black pentagon, next to a small trophy cup."""
    cx, cy, r = x + 58, y + h // 2, 46
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 250, 250),
                 outline=INK, width=3)
    import math
    pent = [(cx + 16 * math.cos(math.pi / 2 + i * 2 * math.pi / 5),
             cy - 16 * math.sin(math.pi / 2 + i * 2 * math.pi / 5)) for i in range(5)]
    draw.polygon(pent, fill=INK)
    for i in range(5):
        px, py = pent[i]
        draw.line([(px, py), (px + (cx - px) * 0.55, py + (cy - py) * 0.55)],
                  fill=INK, width=2)
    # trophy
    tx, ty = x + w - 62, y + 26
    draw.polygon([(tx, ty), (tx + 34, ty), (tx + 30, ty + 30), (tx + 4, ty + 30)],
                 fill=(212, 175, 55), outline=INK, width=2)
    draw.line([(tx + 17, ty + 30), (tx + 17, ty + 44)], fill=INK, width=4)
    draw.line([(tx + 4, ty + 44), (tx + 30, ty + 44)], fill=INK, width=4)


def draw_spacecraft(draw, x, y, w, h):
    """A small probe with solar panels flying past a cratered planet."""
    px, py, pr = x + w - 46, y + h - 40, 34
    draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(170, 165, 155),
                 outline=INK, width=3)
    for (cx0, cy0, cr0) in [(px - 12, py - 8, 7), (px + 10, py + 10, 5),
                            (px + 4, py - 16, 4)]:
        draw.ellipse([cx0 - cr0, cy0 - cr0, cx0 + cr0, cy0 + cr0],
                     fill=(130, 125, 115))
    # probe body + panels
    bx, by = x + 22, y + 22
    draw.rectangle([bx, by, bx + 34, by + 24], fill=(200, 200, 210),
                   outline=INK, width=2)
    draw.rectangle([bx - 26, by + 4, bx, by + 20], fill=(40, 90, 180),
                   outline=INK, width=2)
    draw.rectangle([bx + 34, by + 4, bx + 60, by + 20], fill=(40, 90, 180),
                   outline=INK, width=2)
    draw.line([(bx + 8, by + 24), (bx + 8, by + 34)], fill=INK, width=3)


def draw_chart_down(draw, x, y, w, h):
    """A red falling market chart with an arrowhead."""
    pts = [(x + 10, y + 18), (x + 56, y + 30), (x + 96, y + 22),
           (x + 140, y + 52), (x + 182, y + 66), (x + w - 12, y + h - 26)]
    draw.line(pts, fill=RED, width=7, joint="curve")
    ex, ey = x + w - 12, y + h - 26
    draw.polygon([(ex, ey), (ex - 20, ey - 2), (ex - 4, ey - 20)], fill=RED)
    draw.text((x + 10, y + h - 30), "-3.3%", font=SANS_B(28), fill=RED)

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # margin
    X1 = W - M

    # ---- masthead ----
    d.text((W // 2, 16), "THE WORLD", font=SERIF_B(66), fill=INK, anchor="ma")
    date_line = "M O N D A Y   2 3   N O V E M B E R   2 0 2 6"
    d.text((W // 2, 96), date_line, font=SANS_B(19), fill=INK, anchor="ma")
    rule(d, M, 128, X1, 3)
    rule(d, M, 134, X1, 1)

    # ---- lead story: Nvidia ----
    ly0, ly1 = 146, 468
    d.rectangle([M, ly0, X1, ly1], outline=INK, width=2)
    d.text((M + 16, ly0 + 12), "BUSINESS  ·  TECHNOLOGY", font=SANS_B(17),
           fill=RED)
    y = ly0 + 40
    y = draw_wrapped(d, M + 16, y, "NVIDIA BRINGS BACK HUANG",
                     SERIF_B(52), 560, spacing=2)
    y += 6
    y = draw_wrapped(d, M + 16, y,
                     "Board reinstates Jensen Huang as chief "
                     "executive, 11 days after he resigned; "
                     "shares jump about 30%.",
                     SANS(23), 560, spacing=6)
    draw_chip_chart(d, 640, ly0 + 30, 340, ly1 - ly0 - 46)

    # ---- six-panel grid ----
    panels = [
        ("UKRAINE  ·  LIBYA",
         "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
         "Zelensky says seven sea drones sank the corvette "
         "Merkury at Benghazi; a cargo ship was hit too.",
         draw_warship),
        ("IRAN  ·  HORMUZ",
         "IRAN VOWS TO DEFY US BLOCKADE",
         "Tehran says it will use \u201call means\u201d as tankers "
         "strike mines east of the Strait of Hormuz.",
         draw_tanker_mine),
        ("UKRAINE  ·  KYIV",
         "15 KILLED IN STRIKES AROUND KYIV",
         "At least 11 die in an apartment-block strike in "
         "Dymer, officials say.",
         draw_building_smoke),
        ("CLIMATE  ·  ANTALYA",
         "COP31 ENDS WITH NO DEAL",
         "Antalya summit collapses over fossil fuels; "
         "Erdo\u011fan says 46 decisions were adopted.",
         draw_globe_crack),
        ("SPORT  ·  FOOTBALL",
         "UK TO HOST 2035 WOMEN\u2019S WORLD CUP",
         "FIFA confirms England, Scotland, Wales and "
         "Northern Ireland as joint hosts.",
         draw_ball),
        ("SCIENCE  ·  SPACE",
         "BEPICOLOMBO REACHES MERCURY",
         "European-Japanese craft enters orbit after an "
         "eight-year journey.",
         draw_spacecraft),
    ]
    gx0, gx1 = M, X1
    col_w = (gx1 - gx0 - 16) // 2
    row_h, row_gap = 126, 12
    gy = 484
    for i, (kicker, head, sub, art) in enumerate(panels):
        col = i % 2
        row = i // 2
        px = gx0 + col * (col_w + 16)
        py = gy + row * (row_h + row_gap)
        d.rectangle([px, py, px + col_w, py + row_h], outline=INK, width=2)
        art(d, px + 8, py + 8, 150, row_h - 16)
        tx = px + 168
        d.text((tx, py + 8), kicker, font=SANS_B(13), fill=RED)
        ty = draw_wrapped(d, tx, py + 28, head, SANS_B(20), col_w - 178,
                          spacing=1)
        draw_wrapped(d, tx, ty + 2, sub, SANS(15), col_w - 178, spacing=2,
                     fill=GREY)

    # ---- bottom strip: markets ----
    by0 = gy + 3 * row_h + 2 * row_gap + 12
    by1 = 992
    d.rectangle([M, by0, X1, by1], outline=INK, width=2)
    draw_chart_down(d, M + 12, by0 + 8, 250, by1 - by0 - 16)
    tx = M + 280
    d.text((tx, by0 + 10), "MARKETS  ·  ASIA", font=SANS_B(14), fill=RED)
    ty = draw_wrapped(d, tx, by0 + 32, "ASIAN TECH SHARES SLIDE",
                      SANS_B(24), X1 - tx - 16, spacing=1)
    draw_wrapped(d, tx, ty + 4,
                 "AI sell-off deepens across Asia; Seoul\u2019s Kospi "
                 "falls 3.3% as Wall Street steadies.",
                 SANS(17), X1 - tx - 16, spacing=2, fill=GREY)
    return img


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
