#!/usr/bin/env python3
"""Convert CSS oklch() colors to sRGB hex.

Usage:
    # Single color
    python oklch_to_hex.py 0.26624 0.15944 267.227

    # From stdin (one "L C H" triple per line)
    printf '0.26624 0.15944 267.227\n0.8936 0.1794 97.56\n' | python oklch_to_hex.py

    # Auto-extract from CSS (grep oklch values)
    grep -oP 'oklch\\([^)]+\\)' app.css | python oklch_to_hex.py --css

L is 0..1. C is chroma (~0..0.4). H is hue degrees.
"""
import math
import re
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


def parse_oklch(s):
    """Parse 'oklch(0.26624 0.15944 267.227)' or with percentages."""
    s = s.strip().removeprefix("oklch(").removesuffix(")")
    parts = s.split()
    if len(parts) >= 3:
        L = float(parts[0].replace("%", "")) / 100 if "%" in parts[0] else float(parts[0])
        C = float(parts[1])
        H = float(parts[2].replace("%", ""))
        return L, C, H
    return None


def emit(L, C, h):
    r, g, b = oklch_to_srgb(L, C, h)
    print("oklch(%.5f %.5f %.3f) -> #%02X%02X%02X  rgb(%d, %d, %d)"
          % (L, C, h, r, g, b, r, g, b))


if __name__ == "__main__":
    css_mode = "--css" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--css"]

    if len(args) == 3:
        emit(float(args[0]), float(args[1]), float(args[2]))
    else:
        for line in sys.stdin:
            if css_mode:
                for match in re.finditer(r'oklch\([^)]+\)', line):
                    parsed = parse_oklch(match.group())
                    if parsed:
                        emit(*parsed)
            else:
                parts = line.split()
                if len(parts) == 3:
                    emit(float(parts[0]), float(parts[1]), float(parts[2]))
