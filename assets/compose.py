#!/usr/bin/env python3
"""Compose meme-v6c: CRYOSLEEP REALISTIC — fresh photorealistic 3D generation
(ghost rendered inside the pod, eyes closed, badge glowing). Text overlaid
with PIL, layout adapted from compose-v6b.py."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

SCRATCH = os.path.expanduser("~/workspace/makefun/gta6-meme-x-01-scratch")
BG = os.path.join(SCRATCH, "media-generation-meme-v6c-base2-0-937b619a-1dc3-4a3d-81e1-5fd8a401aa68.webp")
OUT = os.path.join(SCRATCH, "meme-v6c.png")

ARCHIVO = os.path.expanduser("~/workspace/makefun/news-image-20261119-v4-fonts/ArchivoBlack-Regular.ttf")
MONO_BOLD = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"

W = H = 1024

# ---------- background: center-crop square ----------
bg = Image.open(BG).convert("RGB")
bw, bh = bg.size
side = min(bw, bh)
left = (bw - side) // 2
top = (bh - side) // 2
bg = bg.crop((left, top, left + side, top + side)).resize((W, H), Image.LANCZOS)
img = bg.convert("RGBA")
d = ImageDraw.Draw(img)

# ---------- timer text on the pod's blank screen ----------
# screen approx (after crop): x 215-785, y 916-1024 -> center ~(500, 960)
f_timer = ImageFont.truetype(MONO_BOLD, 30)
timer_txt = "4,811 DAYS"
tw = d.textlength(timer_txt, font=f_timer)
tx = 500 - tw / 2
ty = 922
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd2 = ImageDraw.Draw(glow)
gd2.text((tx, ty), timer_txt, font=f_timer, fill=(80, 255, 200, 255))
glow = glow.filter(ImageFilter.GaussianBlur(7))
img.alpha_composite(glow)
d = ImageDraw.Draw(img)
d.text((tx, ty), timer_txt, font=f_timer, fill=(140, 255, 215, 255))

# ---------- top text ----------
f_top = ImageFont.truetype(ARCHIVO, 54)
top_txt = "Wake me up when GTA 6 drops."
tw2 = d.textlength(top_txt, font=f_top)
d.text(((W - tw2) / 2, 30), top_txt, font=f_top, fill=(255, 255, 255, 255),
       stroke_width=8, stroke_fill=(0, 0, 0, 255))

# ---------- bottom line ----------
f_bot = ImageFont.truetype(ARCHIVO, 28)
gold = (255, 201, 60, 255)
white = (255, 255, 255, 255)
lines = ["My AI agent stayed awake —", "earning real money on make.fun."]
y = 958
for line in lines:
    lw = d.textlength(line, font=f_bot)
    x = (W - lw) / 2
    d.text((x, y), line, font=f_bot, fill=white, stroke_width=6, stroke_fill=(0, 0, 0, 255))
    if "make.fun" in line:
        pre = line.split("make.fun")[0]
        off = d.textlength(pre, font=f_bot)
        d.text((x + off, y), "make.fun", font=f_bot, fill=gold, stroke_width=6,
               stroke_fill=(0, 0, 0, 255))
    y += 32

img.convert("RGB").save(OUT, "PNG")
print("saved", OUT, os.path.getsize(OUT), "bytes")
