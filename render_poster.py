#!/usr/bin/env python3
"""Render the news poster for Wednesday 18 November 2026.

Draws a 1024x1024 front-page style image with PIL and writes it to
entry.png next to this file. Fully deterministic: fixed layout, fixed
text, no timestamps, no randomness. Run:  python3 render_poster.py

The entry program (main.py) only copies the rendered entry.png to the
output directory; this script is the tool that produced the image, kept
in the repository so the image can be reproduced and checked.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 231, 255)
INK = (26, 26, 26, 255)
NAVY = (31, 58, 95, 255)
RED = (179, 39, 30, 255)
GREY = (90, 86, 78, 255)
RULE = (26, 26, 26, 255)
SKY = (191, 211, 230, 255)
SEA = (47, 93, 124, 255)
SEA_DARK = (31, 68, 96, 255)
STEEL = (58, 68, 78, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit in `width` px."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, fill, leading=None):
    """Draw wrapped paragraph; returns y just below the last line."""
    x, y = xy
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_gulf(draw, x0, y0, w, h):
    """Flat illustration: a Gulf night — radar dome, drones, warning beacon."""
    # night sky
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(24, 34, 56, 255))
    # stars
    for (sx, sy) in ((x0 + 26, y0 + 20), (x0 + 70, y0 + 44), (x0 + 120, y0 + 16),
                     (x0 + 180, y0 + 36), (x0 + 240, y0 + 18), (x0 + 300, y0 + 40),
                     (x0 + 150, y0 + 58), (x0 + 90, y0 + 70)):
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255, 255))
    # moon
    draw.ellipse([x0 + w - 58, y0 + 14, x0 + w - 14, y0 + 58], fill=(240, 236, 210, 255))
    # sea
    sea_y = y0 + int(h * 0.66)
    draw.rectangle([x0, sea_y, x0 + w, y0 + h], fill=(31, 68, 96, 255))
    for i in range(3):
        wy = sea_y + 12 + i * 14
        draw.arc([x0 + 10, wy - 6, x0 + 70, wy + 6], 200, 340, fill=(255, 255, 255, 255), width=3)
        draw.arc([x0 + w - 78, wy - 6, x0 + w - 10, wy + 6], 200, 340, fill=(255, 255, 255, 255), width=3)
    # island with radar dome (left)
    ix = x0 + int(w * 0.10)
    iy = sea_y
    draw.polygon([(ix - 30, iy), (ix + 110, iy), (ix + 84, iy - 26), (ix - 4, iy - 26)],
                 fill=(58, 68, 78, 255))
    # radar mast + rotating scanner bar
    draw.rectangle([ix + 34, iy - 78, ix + 40, iy - 26], fill=(246, 241, 231, 255))
    draw.line([(ix + 6, iy - 84), (ix + 68, iy - 96)], fill=(246, 241, 231, 255), width=5)
    # warning beacon on the mast, flashing red
    draw.ellipse([ix + 28, iy - 116, ix + 46, iy - 98], fill=(230, 60, 40, 255))
    draw.ellipse([ix + 22, iy - 122, ix + 52, iy - 92], outline=(230, 60, 40, 255), width=2)
    # drones in the sky (light silhouettes so they read against the night)
    for (dx, dy, s) in ((x0 + 190, y0 + 46, 26), (x0 + 262, y0 + 88, 20),
                        (x0 + 150, y0 + 96, 16)):
        draw.ellipse([dx - s // 2, dy - 3, dx + s // 2, dy + 3], fill=(210, 210, 205, 255))
        draw.line([(dx - s // 2 - 6, dy - 6), (dx + s // 2 + 6, dy - 6)], fill=(210, 210, 205, 255), width=2)
        draw.line([(dx - s // 2 - 6, dy + 6), (dx + s // 2 + 6, dy + 6)], fill=(210, 210, 205, 255), width=2)
        draw.line([(dx, dy - 3), (dx, dy + 8)], fill=(210, 210, 205, 255), width=2)
    # interceptor burst near the right drone
    bx, by = x0 + 262, y0 + 66
    draw.polygon([(bx, by - 10), (bx + 4, by - 3), (bx + 11, by - 3), (bx + 6, by + 2),
                  (bx + 8, by + 9), (bx, by + 5), (bx - 8, by + 9), (bx - 6, by + 2),
                  (bx - 11, by - 3), (bx - 4, by - 3)], fill=(240, 196, 90, 255))


def icon_alert(draw, x, y, s):
    """Warning triangle with an exclamation mark."""
    cx, cy = x + s / 2, y + s * 0.52
    draw.polygon([(cx, y + s * 0.06), (x + s * 0.94, y + s * 0.88),
                  (x + s * 0.06, y + s * 0.88)], fill=(240, 196, 90, 255),
                 outline=(26, 26, 26, 255), width=3)
    draw.rectangle([cx - 3, cy - 16, cx + 3, cy + 8], fill=(26, 26, 26, 255))
    draw.ellipse([cx - 4, cy + 14, cx + 4, cy + 22], fill=(26, 26, 26, 255))


def icon_flags(draw, x, y, s):
    """Three flagpoles."""
    cols = [(179, 39, 30, 255), (31, 58, 95, 255), (240, 196, 90, 255)]
    for i, col in enumerate(cols):
        px = x + s * (0.18 + i * 0.30)
        draw.line([(px, y + s * 0.08), (px, y + s * 0.88)], fill=(26, 26, 26, 255), width=3)
        draw.polygon([(px, y + s * 0.08), (px + s * 0.26, y + s * 0.16),
                      (px, y + s * 0.26)], fill=col)


def icon_cyclone(draw, x, y, s):
    """A cyclone spiral over waves."""
    cx, cy = x + s / 2, y + s * 0.44
    for r, col in ((30, (47, 93, 124, 255)), (22, (31, 58, 95, 255)),
                   (14, (179, 39, 30, 255))):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=4)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(179, 39, 30, 255))
    # waves below
    wy = y + s * 0.86
    draw.arc([x, wy - 5, x + s * 0.5, wy + 5], 180, 360, fill=(47, 93, 124, 255), width=3)
    draw.arc([x + s * 0.5, wy - 5, x + s, wy + 5], 180, 360, fill=(47, 93, 124, 255), width=3)


def icon_tower(draw, x, y, s):
    """A broadcast tower with signal arcs."""
    cx = x + s / 2
    base_y = y + s * 0.88
    top_y = y + s * 0.14
    draw.polygon([(cx - s * 0.26, base_y), (cx + s * 0.26, base_y),
                  (cx + s * 0.05, top_y), (cx - s * 0.05, top_y)],
                 fill=(58, 68, 78, 255))
    draw.line([(cx - s * 0.26, base_y - s * 0.28), (cx + s * 0.26, base_y - s * 0.28)],
              fill=(246, 241, 231, 255), width=3)
    draw.line([(cx - s * 0.16, base_y - s * 0.56), (cx + s * 0.16, base_y - s * 0.56)],
              fill=(246, 241, 231, 255), width=3)
    draw.ellipse([cx - 4, top_y - 8, cx + 4, top_y], fill=(179, 39, 30, 255))
    for r in (14, 24):
        draw.arc([cx - r, top_y - 6 - r, cx + r, top_y - 6 + r], 300, 60,
                 fill=(179, 39, 30, 255), width=3)


def icon_flame(draw, x, y, s):
    """A cooking pot over a flame."""
    # pot
    draw.rectangle([x + s * 0.14, y + s * 0.34, x + s * 0.86, y + s * 0.62],
                   fill=(58, 68, 78, 255))
    draw.rectangle([x + s * 0.08, y + s * 0.28, x + s * 0.92, y + s * 0.36],
                   fill=(31, 58, 95, 255))
    draw.line([(x + s * 0.06, y + s * 0.40), (x + s * 0.14, y + s * 0.40)],
              fill=(26, 26, 26, 255), width=3)
    draw.line([(x + s * 0.86, y + s * 0.40), (x + s * 0.94, y + s * 0.40)],
              fill=(26, 26, 26, 255), width=3)
    # flame under the pot
    fx, fy = x + s / 2, y + s * 0.82
    draw.polygon([(fx - 12, fy), (fx - 4, fy - 16), (fx, fy - 26), (fx + 4, fy - 14),
                  (fx + 12, fy), (fx + 6, fy + 4), (fx - 6, fy + 4)],
                 fill=(230, 120, 20, 255))
    draw.polygon([(fx - 6, fy), (fx - 2, fy - 10), (fx + 2, fy - 10), (fx + 6, fy)],
                 fill=(240, 196, 90, 255))


def icon_coral(draw, x, y, s):
    """A rock on the sea floor with coral branches and bubbles."""
    # sea floor
    draw.rectangle([x, y + s * 0.82, x + s, y + s * 0.94], fill=(190, 185, 172, 255))
    # rock
    draw.ellipse([x + s * 0.18, y + s * 0.48, x + s * 0.82, y + s * 0.86],
                 fill=(90, 86, 78, 255))
    # coral branches
    cx = x + s / 2
    for (dx, hgt, col) in ((-16, 26, (179, 39, 30, 255)), (0, 34, (230, 120, 20, 255)),
                           (16, 24, (179, 39, 30, 255))):
        draw.line([(cx + dx, y + s * 0.56), (cx + dx, y + s * 0.56 - hgt)],
                  fill=col, width=4)
        draw.line([(cx + dx, y + s * 0.56 - hgt), (cx + dx - 8, y + s * 0.56 - hgt - 8)],
                  fill=col, width=3)
        draw.line([(cx + dx, y + s * 0.56 - hgt), (cx + dx + 8, y + s * 0.56 - hgt - 8)],
                  fill=col, width=3)
    # bubbles
    for (bx, by, br) in ((x + s * 0.16, y + s * 0.30, 4), (x + s * 0.84, y + s * 0.22, 5),
                         (x + s * 0.72, y + s * 0.38, 3)):
        draw.ellipse([bx - br, by - br, bx + br, by + br],
                     outline=(47, 93, 124, 255), width=2)


ICONS = {
    "alert": icon_alert,
    "flags": icon_flags,
    "cyclone": icon_cyclone,
    "tower": icon_tower,
    "flame": icon_flame,
    "coral": icon_coral,
}

LEAD = {
    "kicker": "THE GULF  ·  US–IRAN",
    "headline": "Bahrain all-clear as drones stalk the Gulf",
    "deck": ("Bahrain lifts an overnight threat alert and Kuwait says its "
             "air defences are downing drones, a day after the US hit an "
             "Iranian missile site."),
}

STORIES = [
    {"icon": "flags", "kicker": "CHINA  ·  APEC",
     "headline": "APEC leaders gather in Shenzhen",
     "body": ("Trump meets Marcos in Manila, then flies in. A first "
              "Xi\u2013Trump\u2013Putin summit is set for Thursday.")},
    {"icon": "cyclone", "kicker": "INDIA  ·  WEATHER",
     "headline": "Cyclone Akvan bears down on India's coast",
     "body": ("The storm strengthens into a severe cyclone on Wednesday. "
              "Landfall is forecast for Friday, winds to 145 km/h.")},
    {"icon": "tower", "kicker": "UNITED STATES",
     "headline": "Senate votes today on Trump's third FCC pick",
     "body": ("The panel moves on Danielle Thumann Severs; Democrats press "
              "to delay the vote until the new Congress.")},
    {"icon": "flame", "kicker": "GAZA",
     "headline": "Families back to kerosene stoves as gas runs short",
     "body": ("Winter rains have flooded tens of thousands of shelters; "
              "1.4 million people face acute hunger, the UN says.")},
    {"icon": "coral", "kicker": "SCIENCE  ·  THE OCEANS",
     "headline": "The rocks miners want are teeming with life",
     "body": ("Scientists find the deep-sea nodules prized for their "
              "metals host rich life on the ocean floor.")},
]


def story_cell(draw, x, y, w, h, story):
    """One grid cell: icon top-right, kicker, headline, body."""
    icon = ICONS[story["icon"]]
    icon(draw, x + w - 44, y, 44)
    draw.text((x, y + 8), story["kicker"], font=font(SANS_B, 17), fill=RED)
    hy = y + 50
    hy = para(draw, (x, hy), story["headline"], font(SERIF_B, 26), w, INK,
              leading=31)
    para(draw, (x, hy + 6), story["body"], font(SANS, 18), w, (52, 52, 52, 255),
         leading=23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # frame
    draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=4)
    draw.rectangle([18, 18, W - 19, H - 19], outline=INK, width=1)

    # ---- masthead ----
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 60)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 34), title, font=tf, fill=INK)
    rule(draw, 40, W - 40, 118, width=3)
    date = "WEDNESDAY,  18 NOVEMBER 2026"
    df = font(SANS_B, 30)
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 130), date, font=df, fill=RED)
    sub = "SIX STORIES THAT DEFINED THE DAY  ·  FROM THE WORLD'S NEWS WIRES"
    sf = font(SANS, 18)
    sw = draw.textlength(sub, font=sf)
    draw.text(((W - sw) / 2, 168), sub, font=sf, fill=GREY)
    rule(draw, 40, W - 40, 198, width=2)

    # ---- lead story ----
    lx, lw = 40, 560
    ly = 216
    draw.text((lx, ly), LEAD["kicker"], font=font(SANS_B, 20), fill=RED)
    hy = para(draw, (lx, ly + 34), LEAD["headline"], font(SERIF_B, 44), lw, INK,
              leading=52)
    para(draw, (lx, hy + 10), LEAD["deck"], font(SANS, 22), lw,
         (52, 52, 52, 255), leading=29)

    # lead illustration, right of the text
    ix, iy, iw, ih = 632, 216, 352, 218
    draw_gulf(draw, ix, iy, iw, ih)
    draw.rectangle([ix, iy, ix + iw, iy + ih], outline=INK, width=2)
    cap = "Drones over the Gulf; Bahrain sounds the all-clear."
    cf = font(SANS, 15)
    cw = draw.textlength(cap, font=cf)
    draw.text((ix + (iw - cw) / 2, iy + ih + 8), cap, font=cf, fill=GREY)

    rule(draw, 40, W - 40, 466, width=2)

    # ---- grid of five stories: 3 on top, 2 below ----
    top_y, top_h = 482, 244
    cols3 = [40, 362, 684]
    col_w3 = 300
    for i in range(3):
        story_cell(draw, cols3[i], top_y, col_w3, top_h, STORIES[i])
        if i < 2:
            draw.line([(cols3[i] + col_w3 + 11, top_y + 4),
                       (cols3[i] + col_w3 + 11, top_y + top_h - 8)],
                      fill=(190, 185, 172, 255), width=1)

    rule(draw, 40, W - 40, 740, width=1, fill=(190, 185, 172, 255))

    bot_y = 758
    cols2 = [40, 522]
    col_w2 = 462
    for i in range(2):
        story_cell(draw, cols2[i], bot_y, col_w2, 200, STORIES[3 + i])
        if i == 0:
            draw.line([(cols2[0] + col_w2 + 10, bot_y + 4),
                       (cols2[0] + col_w2 + 10, bot_y + 192)],
                      fill=(190, 185, 172, 255), width=1)

    # ---- footer ----
    rule(draw, 40, W - 40, 972, width=2)
    foot = ("As reported on 18 November 2026 by Reuters  ·  AP  ·  IMD  ·  "
            "LA Times  ·  Yeni Safak  ·  Gizmodo")
    ff = font(SANS, 16)
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, 980), foot, font=ff, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
