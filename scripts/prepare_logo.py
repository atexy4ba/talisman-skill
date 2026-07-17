#!/usr/bin/env python3
"""Prepare a logo asset for LaTeX and report its dominant background color.

Converts webp/png/jpg/bmp/gif to PNG via Pillow. For SVG, tries cairosvg or
rsvg-convert before falling back to asking for a raster version.

Usage:
    python prepare_logo.py <input> <output.png>

Output: PNG file + printed background color for the cover color-match trick.
"""
import os
import subprocess
import sys
from PIL import Image


def convert_svg(src, dst):
    """Try cairosvg then rsvg-convert for SVG input."""
    try:
        import cairosvg
        cairosvg.svg2png(url=src, write_to=dst)
        return True
    except ImportError:
        pass
    try:
        subprocess.run(
            ["rsvg-convert", "-f", "png", "-o", dst, src],
            capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    return False


def main(src, dst):
    ext = os.path.splitext(src)[1].lower()
    if ext == ".svg":
        if not convert_svg(src, dst):
            sys.exit(
                "SVG conversion failed. Install cairosvg (`pip install cairosvg`) "
                "or rsvg-convert (`apt install librsvg2-bin`). "
                "Alternatively provide a PNG version.")
    else:
        im = Image.open(src).convert("RGBA")
        im.save(dst)

    # Sample background color from converted PNG
    im = Image.open(dst).convert("RGB")
    print("size:", im.size)
    for name, xy in [("top-left", (2, 2)),
                     ("top-right", (im.width - 3, 2)),
                     ("center", (im.width // 2, im.height // 2))]:
        px = im.getpixel(xy)
        print("%-10s rgb%s -> #%02X%02X%02X" % (name, px, *px))
    print("saved:", dst)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python prepare_logo.py <input> <output.png>")
    main(sys.argv[1], sys.argv[2])
