"""Render the "New Phone Who Dis" meme: a dark DM thread, 1024x1024.

The ghost texts "GTA 6 when?" every year from 2013 to 2025, Rockstar
finally answers "it's out.", and the ghost replies "new phone who dis".
Run with Pillow installed:  python3 assets/compose.py
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (18, 18, 22)
GRAY_BUBBLE = (58, 58, 64)
MUTED = (150, 150, 158)
WHITE = (245, 245, 247)
YELLOW = (250, 199, 44)
BLUE = (29, 155, 240)
MAGENTA = (226, 0, 116)


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def gradient_bubble(draw, box, radius=26):
    """Purple-to-pink horizontal gradient clipped to a rounded rect."""
    x0, y0, x1, y1 = box
    strip = Image.new("RGB", (x1 - x0, y1 - y0))
    px = strip.load()
    for x in range(strip.width):
        t = x / max(1, strip.width - 1)
        r = int(124 + (255 - 124) * t)
        g = int(58 + (94 - 58) * t)
        b = int(237 + (168 - 237) * t)
        for y in range(strip.height):
            px[x, y] = (r, g, b)
    mask = Image.new("L", strip.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, strip.width, strip.height], radius, fill=255)
    canvas.paste(strip, (x0, y0), mask)


def sent_bubble(draw, y, text, fnt):
    tw = draw.textlength(text, font=fnt)
    x1 = W - 48
    x0 = int(x1 - tw - 56)
    gradient_bubble(draw, (x0, y, x1, y + 64))
    draw.text((x0 + 28, y + 14), text, font=fnt, fill=WHITE)
    return y + 64


def draw_ghost(draw, cx, cy, r=30):
    """White make.fun ghost: dome head, wavy hem, two eyes."""
    draw.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=WHITE)
    draw.rectangle([cx - r, cy, cx + r, cy + r - 6], fill=WHITE)
    for i in range(3):
        x = cx - r + i * (2 * r // 3)
        draw.ellipse([x, cy + r - 14, x + 2 * r // 3, cy + r + 2], fill=BG)
    for dx in (-10, 10):
        draw.ellipse([cx + dx - 4, cy - 8, cx + dx + 4, cy + 2], fill=BG)


canvas = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(canvas)
f_name, f_body, f_small = font(34, True), font(30), font(22)

# --- top bar: avatar, handle, verified check, divider ---
d.ellipse([36, 28, 108, 100], fill=YELLOW)
d.text((58, 44), "R", font=font(44, True), fill=(20, 20, 20))
d.polygon([(96, 84), (108, 72), (96, 60), (84, 72)], fill=(20, 20, 20))
d.text((128, 42), "rockstar", font=f_name, fill=WHITE)
vx = 128 + d.textlength("rockstar", font=f_name) + 12
d.ellipse([vx, 46, vx + 30, 76], fill=BLUE)
d.line([(vx + 8, 61), (vx + 13, 67), (vx + 23, 54)], fill=WHITE, width=4)
d.line([(0, 124), (W, 124)], fill=(44, 44, 50), width=2)

# --- the yearly "GTA 6 when?" column ---
y = 150
for year in range(2013, 2026):
    label = str(year)
    lw = d.textlength(label, font=f_small)
    d.text(((W - lw) / 2, y), label, font=f_small, fill=MUTED)
    y = sent_bubble(d, y + 30, "GTA 6 when?", f_body) + 10

# --- Rockstar finally replies ---
d.text((48, y), "Nov 2026", font=f_small, fill=MUTED)
y += 32
d.rounded_rectangle([48, y, 48 + 210, y + 64], 26, fill=GRAY_BUBBLE)
d.text((76, y + 14), "it's out.", font=f_body, fill=WHITE)
y += 84

# --- the ghost answers back ---
draw_ghost(d, W - 470, y + 32)
d.polygon([(W - 430, y + 6), (W - 414, y + 22), (W - 430, y + 38), (W - 446, y + 22)], fill=MAGENTA)
sent_bubble(d, y, "new phone who dis", f_body)

# --- message input bar ---
d.rounded_rectangle([32, H - 96, W - 32, H - 28], 34, outline=(70, 70, 78), width=2)
d.text((64, H - 80), "Message...", font=f_body, fill=MUTED)

canvas.save("meme.png")
print("wrote meme.png (1024x1024)")
