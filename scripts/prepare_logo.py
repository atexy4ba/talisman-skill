#!/usr/bin/env python3
"""Prepare a logo asset for LaTeX and report its dominant background color.

pdflatex can't read .webp (common for app logos) or .svg. This converts to PNG
via Pillow and samples the corner pixel so you know the logo's background color —
useful for the full-bleed cover trick: make the cover the SAME color as the logo's
square background, and the monogram appears to float with no visible seam.

Usage:
    python prepare_logo.py <input.webp|png|jpg> <output.png>

For .svg logos, Pillow won't help — use `rsvg-convert`, `inkscape`, or `cairosvg`
if available, otherwise ask the user for a raster version.
"""
import sys

from PIL import Image


def main(src, dst):
    im = Image.open(src).convert("RGBA")
    print("size:", im.size)
    rgb = im.convert("RGB")
    # sample a few corners; app icons usually have a solid background
    for name, xy in [("top-left", (2, 2)),
                     ("top-right", (im.width - 3, 2)),
                     ("center", (im.width // 2, im.height // 2))]:
        px = rgb.getpixel(xy)
        print("%-10s rgb%s -> #%02X%02X%02X" % (name, px, *px))
    im.save(dst)
    print("saved:", dst)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python prepare_logo.py <input> <output.png>")
    main(sys.argv[1], sys.argv[2])
