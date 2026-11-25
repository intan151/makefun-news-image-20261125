#!/usr/bin/env python3
"""Draw "The World in One Day" -- Wednesday, 25 November 2026.

A newspaper front page summing up six verified world-news stories of
25 November 2026 in a 2 x 3 grid of panels. Drawn entirely with
Pillow: no photographs, no network, no randomness, no timestamps in
the output -- two runs write byte-identical PNGs.

Usage:  python3 draw_news.py
Writes entry.png (1024x1024, PNG, <= 1 MiB) next to this file.
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
EDGE = 32
GAP = 16

BG = (247, 243, 232)
CARD_BG = (255, 253, 246)
INK = (26, 24, 21)
MUTED = (102, 96, 86)
RED = (158, 30, 30)
BLUE = (26, 72, 110)
GREEN = (42, 104, 60)
GOLD = (162, 118, 38)
TEAL = (18, 96, 96)
RULE = (208, 199, 176)
HALO = (233, 226, 208)

FONT_DIRS = [
    ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", "serif_b"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "sans_b"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "sans"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", "serif"),
]


def _load(kind, size):
    for path, tag in FONT_DIRS:
        if tag != kind:
            continue
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            pass
    return ImageFont.load_default(size=size)


def make_fonts():
    return {
        "masthead": _load("serif_b", 54),
        "date": _load("sans_b", 22),
        "kick": _load("sans_b", 14),
        "head": _load("serif_b", 21),
        "body": _load("sans", 15),
        "foot": _load("sans", 13),
        "num": _load("serif_b", 22),
    }


def wrap_text(draw, text, font, width):
    """Split text into lines that fit width (greedy, word by word)."""
    words = text.split()
    lines = []
    line = ""
    for word in words:
        cand = word if line == "" else line + " " + word
        if draw.textlength(cand, font=font) <= width:
            line = cand
        else:
            if line != "":
                lines.append(line)
            line = word
    if line != "":
        lines.append(line)
    return lines


def text_block(draw, x, y, text, font, width, colour, leading, limit=None):
    """Draw wrapped text starting at (x, y); return the y below it."""
    lines = wrap_text(draw, text, font, width)
    if limit is not None:
        lines = lines[:limit]
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=colour)
        y += leading
    return y


def disc(draw, x, y, s):
    draw.ellipse([x, y, x + s, y + s], fill=HALO)
    return x + s // 2, y + s // 2


# ------------------------------------------------------------------ icons
# Each icon draws on a pale disc of side s at (x, y), in colour fg.

def icon_tanker(d, x, y, s, fg):
    cx, _ = disc(d, x, y, s)
    hy = y + 40
    d.polygon([(cx - 30, hy), (cx + 30, hy), (cx + 23, hy + 15),
               (cx - 23, hy + 15)], fill=fg)
    d.rectangle([cx - 9, hy - 13, cx + 9, hy], fill=fg)
    d.rectangle([cx - 2, hy - 22, cx + 2, hy - 13], fill=fg)
    for yy in (hy + 23, hy + 30):
        for off in (-20, 0, 20):
            d.arc([cx + off - 8, yy, cx + off + 8, yy + 8],
                  180, 360, fill=fg, width=3)


def icon_flame(d, x, y, s, fg):
    cx, _ = disc(d, x, y, s)
    base = y + s - 16
    d.polygon([(cx, y + 12), (cx + 16, y + 34), (cx + 8, y + 30),
               (cx + 20, base), (cx - 20, base), (cx - 8, y + 30),
               (cx - 16, y + 34)], fill=fg)
    d.rectangle([cx - 26, base, cx + 26, base + 5], fill=fg)


def icon_drone(d, x, y, s, fg):
    cx, cy = disc(d, x, y, s)
    d.rectangle([cx - 12, cy - 7, cx + 12, cy + 7], fill=fg)
    for sx in (-1, 1):
        for sy in (-1, 1):
            ax, ay = cx + sx * 24, cy + sy * 14
            d.ellipse([ax - 7, ay - 7, ax + 7, ay + 7], outline=fg, width=3)
            d.line([cx + sx * 10, cy + sy * 5, ax, ay], fill=fg, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=HALO)


def icon_treaty(d, x, y, s, fg):
    cx, _ = disc(d, x, y, s)
    top = y + 16
    d.rectangle([cx - 22, top, cx + 22, top + 40], outline=fg, width=4)
    for i, yy in enumerate((top + 9, top + 19, top + 29)):
        d.line([cx - 14, yy, cx + 14 - i * 4, yy], fill=fg, width=3)
    d.ellipse([cx + 8, top + 34, cx + 24, top + 50], fill=fg)
    d.ellipse([cx + 12, top + 38, cx + 20, top + 46], fill=HALO)


def icon_shield(d, x, y, s, fg):
    cx, _ = disc(d, x, y, s)
    top = y + 14
    d.polygon([(cx, top), (cx + 24, top + 8), (cx + 24, top + 30),
               (cx, top + 52), (cx - 24, top + 30), (cx - 24, top + 8)],
              fill=fg)
    d.line([cx - 10, top + 28, cx - 2, top + 36, cx + 12, top + 20],
           fill=HALO, width=4)


def icon_rocket(d, x, y, s, fg):
    cx, _ = disc(d, x, y, s)
    top = y + 12
    d.polygon([(cx, top), (cx + 12, top + 26), (cx + 12, top + 44),
               (cx - 12, top + 44), (cx - 12, top + 26)], fill=fg)
    d.ellipse([cx - 5, top + 22, cx + 5, top + 32], fill=HALO)
    d.polygon([(cx - 12, top + 40), (cx - 22, top + 54), (cx - 12, top + 50)],
              fill=fg)
    d.polygon([(cx + 12, top + 40), (cx + 22, top + 54), (cx + 12, top + 50)],
              fill=fg)
    d.polygon([(cx - 6, top + 44), (cx + 6, top + 44), (cx, top + 60)],
              fill=fg)


ICONS = {
    "tanker": icon_tanker,
    "flame": icon_flame,
    "drone": icon_drone,
    "treaty": icon_treaty,
    "shield": icon_shield,
    "rocket": icon_rocket,
}

# --------------------------------------------------------------- stories
# (number, kicker, headline, summary, source, icon, accent)
STORIES = [
    (1, "STRAIT OF HORMUZ  ·  MIDDLE EAST",
     "Two oil tankers hit naval mines and catch fire in the Strait of Hormuz",
     "Iran's Revolutionary Guards said two tankers struck mines, "
     "exploded and caught fire, and warned ships to coordinate passage.",
     "REUTERS", "tanker", RED),
    (2, "SAUDI ARABIA  ·  CONFLICT",
     "Houthis say they struck Saudi Arabia's biggest oil refinery",
     "The Houthis claimed an attack on the Ras Tanura refinery and on "
     "Riyadh's financial district; the coalition said it downed drones.",
     "REUTERS", "flame", RED),
    (3, "SUDAN  ·  WAR",
     "RSF drone strikes kill 19 civilians in two Sudanese cities",
     "Emergency Lawyers said paramilitary Rapid Support Forces drone "
     "strikes killed 19 civilians and wounded 20 others.",
     "JUST SECURITY", "drone", GOLD),
    (4, "PACIFIC  ·  DIPLOMACY",
     "Solomon Islands signs security treaty with Australia",
     "The treaty makes Canberra the islands' defence partner of choice "
     "and pledges no foreign military base will ever stand there.",
     "REUTERS", "treaty", BLUE),
    (5, "COLOMBIA  ·  RESCUE",
     "All hostages freed as forces storm Cartagena supermarket",
     "Security forces ended a day-long siege at an Exito store, freeing "
     "every remaining hostage; one captor was killed in the raid.",
     "REUTERS", "shield", GREEN),
    (6, "SPACE  ·  CHINA",
     "Shenzhou-24 docks at Tiangong with Pakistan's first astronaut",
     "China's Shenzhou-24 launched and docked in hours; Muhammad "
     "Zeeshan Ali is the first Pakistani in orbit, and the first "
     "foreigner aboard Tiangong.",
     "REUTERS", "rocket", TEAL),
]


def draw_panel(draw, fonts, story, x, y, w, h):
    num, kicker, head, body, source, icon, accent = story
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD_BG, outline=RULE, width=1)
    pad = 18
    ix, iy = x + pad, y + pad
    # Number badge + kicker.
    draw.ellipse([ix, iy, ix + 30, iy + 30], fill=accent)
    num_text = str(num)
    tw = draw.textlength(num_text, font=fonts["num"])
    draw.text((ix + (30 - tw) / 2, iy + 3), num_text,
              font=fonts["num"], fill=CARD_BG)
    draw.text((ix + 40, iy + 6), kicker, font=fonts["kick"], fill=accent)
    # Headline.
    hy = iy + 42
    hy = text_block(draw, ix, hy, head, fonts["head"], w - 2 * pad,
                    INK, 26, limit=3)
    # Rule, then icon + summary.
    ry = y + h - 96
    draw.line([ix, ry, x + w - pad, ry], fill=RULE, width=1)
    ICONS[icon](draw, ix, ry + 10, 68, accent)
    text_block(draw, ix + 82, ry + 12, body, fonts["body"],
               w - 2 * pad - 82, MUTED, 19, limit=4)
    # Source label, bottom right.
    sw = draw.textlength(source, font=fonts["foot"])
    draw.text((x + w - pad - sw, y + h - 24), source,
              font=fonts["foot"], fill=MUTED)


def main():
    fonts = make_fonts()
    img = Image.new("RGB", CANVAS, BG)
    draw = ImageDraw.Draw(img)

    # Masthead.
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=fonts["masthead"])
    draw.text(((CANVAS[0] - tw) / 2, 22), title,
              font=fonts["masthead"], fill=INK)
    date = "Wednesday, 25 November 2026"
    dw = draw.textlength(date, font=fonts["date"])
    draw.text(((CANVAS[0] - dw) / 2, 88), date,
              font=fonts["date"], fill=RED)
    draw.line([EDGE, 122, CANVAS[0] - EDGE, 122], fill=INK, width=3)
    draw.line([EDGE, 127, CANVAS[0] - EDGE, 127], fill=RULE, width=1)

    # 2 x 3 grid of panels.
    col_w = (CANVAS[0] - 2 * EDGE - GAP) // 2
    grid_top = 140
    grid_bottom = CANVAS[1] - 46
    row_h = (grid_bottom - grid_top - 2 * GAP) // 3
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        px = EDGE + col * (col_w + GAP)
        py = grid_top + row * (row_h + GAP)
        draw_panel(draw, fonts, story, px, py, col_w, row_h)

    # Footer.
    foot = "Six stories, verified 25 November 2026  ·  Sources: Reuters, Just Security"
    fw = draw.textlength(foot, font=fonts["foot"])
    draw.text(((CANVAS[0] - fw) / 2, CANVAS[1] - 32), foot,
              font=fonts["foot"], fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
