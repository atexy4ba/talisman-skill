#!/usr/bin/env python3
"""Convert CSS oklch() colors to sRGB hex.

Modern web apps (Tailwind v4, shadcn) define brand colors in oklch, which LaTeX
can't use directly. Extract the brand palette from the app's CSS, feed the values
here, and get the hex codes for your \\definecolor lines.

Usage:
    # single color
    python oklch_to_hex.py 0.26624 0.15944 267.227

    # many at once, one "L C H" triple per line on stdin
    printf '0.26624 0.15944 267.227\\n0.8936 0.1794 97.56\\n' | python oklch_to_hex.py

L is 0..1 (percentages: divide by 100). C is chroma (~0..0.4). H is hue degrees.
"""
import math
import sys


def oklch_to_srgb(L, C, h_deg):
    h = math.radians(h_deg)
    a = C * math.cos(h)
    b = C * math.sin(h)
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bl = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    def f(x):
        x = max(0.0, min(1.0, x))
        return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055

    return tuple(round(f(v) * 255) for v in (r, g, bl))


def emit(L, C, h):
    r, g, b = oklch_to_srgb(L, C, h)
    print("oklch(%.5f %.5f %.3f) -> #%02X%02X%02X  rgb(%d, %d, %d)"
          % (L, C, h, r, g, b, r, g, b))


if __name__ == "__main__":
    if len(sys.argv) == 4:
        emit(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
    else:
        for line in sys.stdin:
            parts = line.split()
            if len(parts) == 3:
                emit(float(parts[0]), float(parts[1]), float(parts[2]))
