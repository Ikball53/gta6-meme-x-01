"""Compose the gta6-meme-x-01 meme: make.fun ghost as a Leonida quest giver."""
import re
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ENTRY = HERE.parent
SIZE = 1024
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# --- 1. Ghost alone from the press-kit mark (drop the magenta disc) ---
svg = (HERE / "mark.svg").read_text()
svg = re.sub(r'<circle cx="16" cy="16" r="15\.1"[^/]*/>', "", svg)
ghost_png = HERE / "ghost-only.png"
cairosvg.svg2png(bytestring=svg.encode(), write_to=str(ghost_png),
                 output_width=1024, output_height=1024)
ghost = Image.open(ghost_png).convert("RGBA")
ghost = ghost.crop(ghost.getbbox())
print("ghost cropped:", ghost.size)

# --- 2. Background fitted to a square ---
bg_src = next(HERE.glob("media-generation-leonida-street-bg-*.png"))
img = ImageOps.fit(Image.open(bg_src).convert("RGB"), (SIZE, SIZE)).convert("RGBA")

# --- 3. Mission-marker glow behind the ghost ---
GHOST_W = 540
ghost_big = ghost.resize((GHOST_W, int(GHOST_W * ghost.height / ghost.width)),
                         Image.LANCZOS)
gx = (SIZE - GHOST_W) // 2
gy = int(SIZE * 0.17)
cx, cy = SIZE // 2, gy + ghost_big.height // 2

glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
r = 330
gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 210, 60, 110))
glow = glow.filter(ImageFilter.GaussianBlur(90))
img.alpha_composite(glow)

# --- 4. Ground ring + soft shadow under the ghost ---
ring = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
rd = ImageDraw.Draw(ring)
ry = gy + ghost_big.height + 26
rd.ellipse([cx - 230, ry - 34, cx + 230, ry + 34], outline=(255, 214, 64, 255), width=10)
rd.ellipse([cx - 190, ry - 22, cx + 190, ry + 22], fill=(0, 0, 0, 90))
ring = ring.filter(ImageFilter.GaussianBlur(3))
img.alpha_composite(ring)

# --- 5. The ghost itself ---
img.alpha_composite(ghost_big, (gx, gy))

# --- 6. Glowing chevron marker above the ghost ---
chev = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
cd = ImageDraw.Draw(chev)
top = gy - 92
cd.polygon([(cx - 62, top), (cx + 62, top), (cx, top + 58)], fill=(255, 214, 64, 255))
chev_glow = chev.filter(ImageFilter.GaussianBlur(14))
img.alpha_composite(chev_glow)
img.alpha_composite(chev)

# --- 7. Meme text, big enough to read at 480px ---
draw = ImageDraw.Draw(img)


def centered(text, y, size, fill=(255, 255, 255, 255)):
    font = ImageFont.truetype(FONT, size)
    w = draw.textlength(text, font=font)
    draw.text(((SIZE - w) / 2, y), text, font=font, fill=fill,
              stroke_width=max(4, size // 9), stroke_fill=(10, 8, 12, 255))
    return w


print("top width:", centered("NEW QUEST IN LEONIDA", 26, 62))
print("mid width:", centered("Every GTA mission pays fake cash.", int(SIZE * 0.655), 50))
print("bot width:", centered("This one pays REAL money.", int(SIZE * 0.725), 56,
                             fill=(255, 214, 64, 255)))

out = ENTRY / "meme.png"
img.convert("RGB").save(out, optimize=True)
img.convert("RGB").resize((480, 480), Image.LANCZOS).save(HERE / "meme-480.png")
print("wrote", out, out.stat().st_size, "bytes")
