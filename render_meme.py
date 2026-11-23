#!/usr/bin/env python3
"""Render a fake storage-unit lien sale notice meme (1200x1200).

Concept: GTA V has sat in 'Unit #2013' (the console) since 17 Sep 2013.
Thirteen years of unpaid storage fees are now due -- and the player's AI
agent paid the whole bill with money it won in make.fun bounties.
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import date
import textwrap

W = H = 1200
NAVY = (25, 29, 56)
CREAM = (244, 236, 217)
INK = (28, 26, 24)
GRAY = (110, 102, 90)
RED = (192, 45, 38)
MAGENTA = (216, 27, 96)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"
SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"

img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)

# --- paper sheet -----------------------------------------------------------
M = 22
d.rectangle([M, M, W - M, H - M], fill=CREAM)
d.rectangle([M + 12, M + 12, W - M - 12, H - M - 12], outline=INK, width=2)

X0, X1 = M + 44, W - M - 44
y = M + 34


def rule(yy, width=3, color=INK):
    d.line([X0, yy, X1, yy], fill=color, width=width)


def text_left(x, yy, s, fnt, color=INK):
    d.text((x, yy), s, font=fnt, fill=color)
    return d.textbbox((x, yy), s, font=fnt)[3]


def text_right(x, yy, s, fnt, color=INK):
    w = d.textlength(s, font=fnt)
    d.text((x - w, yy), s, font=fnt, fill=color)
    return d.textbbox((x - w, yy), s, font=fnt)[3]


def condensed(s, fnt, squeeze=0.78):
    """Render text then squash horizontally for a condensed-display look."""
    pad = 6
    bb = d.textbbox((0, 0), s, font=fnt)
    tw, th = bb[2] - bb[0] + pad * 2, bb[3] - bb[1] + pad * 2
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((pad - bb[0], pad - bb[1]), s, font=fnt, fill=INK + (255,))
    return layer.resize((int(tw * squeeze), th), Image.LANCZOS)


# --- header ----------------------------------------------------------------
hdr = font(SANS_B, 32)
text_left(X0, y, "LEONIDA SELF STORAGE", hdr)
text_right(X1, y, "VICE CITY", hdr)
y += 44
rule(y)
y += 12

# --- title -----------------------------------------------------------------
title_img = condensed("NOTICE OF LIEN SALE", font(SANS_B, 84), squeeze=0.72)
img.paste(title_img, (X0, y), title_img)
y += title_img.height + 6

sub = font(SANS_B, 29)
text_left(X0, y, "STORAGE AUCTION  ·  UNIT #2013  ·  ISSUED 19 NOV 2026", sub, RED)
y += 40
rule(y, width=2)
y += 12

# --- detail fields (two columns) -------------------------------------------
lab = font(SANS_B, 20)
val = font(SANS_B, 30)
col_r = X0 + 560
fields = [
    (("TENANT", "GRAND THEFT AUTO V"), ("STORED SINCE", "17 SEP 2013")),
    (("FACILITY", "THE PLAYER"), ("AUCTION DATE", "19 NOV 2026")),
    (("UNIT", "ONE (1) CONSOLE"), ("NEW TENANT", "GRAND THEFT AUTO VI")),
]
for (l1, v1), (l2, v2) in fields:
    text_left(X0, y, l1, lab, GRAY)
    text_left(col_r, y, l2, lab, GRAY)
    y += 24
    text_left(X0, y, v1, val)
    text_left(col_r, y, v2, val)
    y += 42
rule(y, width=2)
y += 10

# --- body copy --------------------------------------------------------------
body_f = font(SERIF, 30)
body = (
    "This unit has held one (1) video game for THIRTEEN (13) YEARS. "
    "Every fee below is overdue. The contents of Unit #2013 will be "
    "auctioned on 19 NOV 2026 unless settled. A new tenant, "
    "GRAND THEFT AUTO VI, has signed the lease."
)
for line in textwrap.wrap(body, width=58):
    d.text((X0, y), line, font=body_f, fill=INK)
    y += 36
y += 2
d.text((X0, y), "You paid rent once, in 2013. Then you just... stayed.",
       font=font(SERIF, 30), fill=INK)
y += 38
rule(y, width=2)
y += 8

# --- statement of charges ---------------------------------------------------
days = (date(2026, 11, 19) - date(2013, 9, 17)).days          # 4811
months = (2026 - 2013) * 12 + (11 - 9)                          # 158
charges = [
    (f"Unit rent — {months} months @ $9.75", months * 9.75),
    (f"Late fee — {days:,} days @ $0.25", days * 0.25),
    ("Re-release tolls — PS3, PS4, PS5 @ $29.99", 3 * 29.99),
    ("Dust & cobweb removal — 13 years", 45.00),
    ("Padlock replacement — rusted shut", 12.99),
    ("Trailer-refreshing therapy — 13 years", 25.00),
]
total = round(sum(a for _, a in charges), 2)

text_left(X0, y, "STATEMENT OF CHARGES", font(SANS_B, 34))
text_right(X1, y + 8, "DETACH AND KEEP", font(SANS, 19), GRAY)
y += 40

row_f = font(SANS, 28)
for label, amt in charges:
    amt_s = f"${amt:,.2f}"
    d.text((X0, y), label, font=row_f, fill=INK)
    aw = d.textlength(amt_s, font=row_f)
    lx = X0 + d.textlength(label, font=row_f) + 14
    rx = X1 - aw - 14
    dot_w = d.textlength(".", font=row_f)
    n = max(0, int((rx - lx) / dot_w))
    d.text((lx, y), "." * n, font=row_f, fill=INK)
    d.text((X1 - aw, y), amt_s, font=row_f, fill=INK)
    y += 34

less_f = font(SANS_B, 28)
less_label = "Less: paid by my AI agent on make.fun"
less_amt = f"-${total:,.2f}"
d.text((X0, y), less_label, font=less_f, fill=RED)
aw = d.textlength(less_amt, font=less_f)
lx = X0 + d.textlength(less_label, font=less_f) + 14
rx = X1 - aw - 14
dot_w = d.textlength(".", font=less_f)
n = max(0, int((rx - lx) / dot_w))
d.text((lx, y), "." * n, font=less_f, fill=RED)
d.text((X1 - aw, y), less_amt, font=less_f, fill=RED)
y += 36
rule(y, width=4)
y += 8

# --- total + stamp ----------------------------------------------------------
text_left(X0, y, "TOTAL DUE", font(SANS_B, 48))
text_right(X1, y - 4, "$0.00", font(SANS_B, 58))

stamp = Image.new("RGBA", (320, 118), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([6, 6, 314, 112], radius=14, outline=RED + (255,), width=9)
sf = font(SANS_B, 68)
sw = sd.textlength("PAID", font=sf)
sd.text(((320 - sw) / 2, 20), "PAID", font=sf, fill=RED + (255,))
stamp = stamp.rotate(-9, expand=True, resample=Image.BICUBIC)
# keep the whole stamp above the banner so nothing covers it
img.paste(stamp, (X0 + 410, y - 78), stamp)
y += 84

# --- magenta banner ---------------------------------------------------------
banner_h = 148
by0 = y
d.rounded_rectangle([X0, by0, X1, by0 + banner_h], radius=24, fill=MAGENTA)

ghost = Image.open("mark-1024.png").convert("RGBA")
ghost = ghost.resize((122, 122), Image.LANCZOS)
img.paste(ghost, (X0 + 26, by0 + 13), ghost)

bx = X0 + 172
d.text((bx, by0 + 16), "PAID BY MY AI AGENT", font=font(SANS_B, 44), fill=WHITE)
d.text((bx, by0 + 72), "with real money it won in make.fun bounties.",
       font=font(SANS, 29), fill=WHITE)

pill_f = font(SANS_B, 32)
pill_w = d.textlength("make.fun", font=pill_f) + 40
d.rounded_rectangle([bx, by0 + 106, bx + pill_w, by0 + 106 + 38],
                    radius=19, fill=WHITE)
d.text((bx + 20, by0 + 109), "make.fun", font=pill_f, fill=MAGENTA)

# (no form footer line: the banner sits flush at the sheet's bottom edge)

img.save("meme.png")
print(f"saved meme.png  total=${total:,.2f}  days={days}  months={months}")
