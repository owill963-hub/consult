#!/usr/bin/env python3
"""
OWC OG/Twitter card generator — ink navy / ordnance red brand system.
Downloads Archivo Black + IBM Plex Mono at runtime (no local font deps).
Outputs quantized PNGs directly into the consult repo.
"""
import os, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont

REPO = "/Users/gratus_one/Documents/GitHub/consult"
FONT_DIR = "/tmp/owc_fonts"
os.makedirs(FONT_DIR, exist_ok=True)

INK       = (16, 28, 44)      # #101C2C
PORCELAIN = (238, 241, 242)   # #EEF1F2
SIGNAL    = (191, 43, 26)     # #BF2B1A
STEEL     = (143, 161, 179)   # #8FA1B3 (hero eyebrow tone)
GRID      = (26, 38, 48)      # ink + 4.5% porcelain

FONTS = {
    "archivo": "https://raw.githubusercontent.com/google/fonts/main/ofl/archivoblack/ArchivoBlack-Regular.ttf",
    "mono":    "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/IBMPlexMono-Regular.ttf",
    "mono_md": "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/IBMPlexMono-Medium.ttf",
}

def get_font(key, size):
    path = os.path.join(FONT_DIR, key + ".ttf")
    if not os.path.exists(path):
        print(f"downloading {key} ...")
        urllib.request.urlretrieve(FONTS[key], path)
    return ImageFont.truetype(path, size)

def draw_grid(d, w, h, step=56):
    for x in range(0, w, step):
        d.line([(x, 0), (x, h)], fill=GRID, width=1)
    for y in range(0, h, step):
        d.line([(0, y), (w, y)], fill=GRID, width=1)

def seg_text(d, x, y, segments, font, tracking=0):
    """Draw sequential colored segments on one baseline; returns end x."""
    for text, color in segments:
        d.text((x, y), text, font=font, fill=color)
        x += d.textlength(text, font=font) + tracking
    return x

def render(w, h, out_name):
    img = Image.new("RGB", (w, h), INK)
    d = ImageDraw.Draw(img)
    draw_grid(d, w, h)

    M = 80  # left margin
    f_eye  = get_font("mono_md", 21)
    f_head = get_font("archivo", 66)
    f_brand = get_font("mono_md", 26)
    f_tags = get_font("mono", 20)

    top = 72 if h == 630 else 58

    # eyebrow
    seg_text(d, M, top, [
        ("VETERAN-OWNED", PORCELAIN), ("   ", STEEL), ("\u25cf", SIGNAL), ("   ", STEEL),
        ("MARYLAND / DC / VIRGINIA", STEEL), ("   ", STEEL), ("\u25cf", SIGNAL), ("   ", STEEL),
        ("REMOTE NATIONWIDE", STEEL),
    ], f_eye)

    # headline — 4 lines, 'THE FULL STACK' as outline (hero <em> treatment)
    y = top + 72
    lh = 74
    d.text((M, y),        "SECURITY IS", font=f_head, fill=PORCELAIN)
    d.text((M, y + lh),   "THE FOUNDATION.", font=f_head, fill=PORCELAIN)
    d.text((M, y + 2*lh), "THE FULL STACK", font=f_head, fill=INK,
           stroke_width=2, stroke_fill=PORCELAIN)
    d.text((M, y + 3*lh), "IS THE MISSION.", font=f_head, fill=PORCELAIN)

    # red rule
    ry = y + 4*lh + 26
    d.rectangle([M, ry, M + 130, ry + 6], fill=SIGNAL)

    # brand line + domain (right-aligned)
    by = ry + 26
    seg_text(d, M, by, [
        ("O WILLIAMS", PORCELAIN), (" // ", SIGNAL), ("CONSULTING", PORCELAIN),
    ], f_brand)
    dom = "OWILLIAMSCONSULTING.COM"
    dw = d.textlength(dom, font=f_brand)
    d.text((w - M - dw, by), dom, font=f_brand, fill=STEEL)

    # service tags
    d.text((M, by + 44), "CMMC \u00b7 vCISO \u00b7 NIST 800-171 \u00b7 ECOMMERCE \u00b7 CLOUD \u00b7 AI APPS",
           font=f_tags, fill=STEEL)

    out = os.path.join(REPO, out_name)
    img.convert("P", palette=Image.ADAPTIVE, colors=256).save(out, optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)//1024} KB)")

if __name__ == "__main__":
    render(1200, 630, "og-image-1200x630.png")
    render(1200, 600, "twitter-card-1200x600.png")
    print("done")
