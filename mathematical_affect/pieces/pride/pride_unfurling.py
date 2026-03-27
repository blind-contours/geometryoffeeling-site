"""
Geometry of Feeling — Pride: Unfurling
Lines converge at a pointed root and unfurl upward through the full
LGBTQ+ palette — trans blue/pink/white woven through the classic rainbow.
Something that was contained, choosing to open.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#f3eee7'


def hex_to_rgb01(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)]) / 255.0


def blend(c1, c2, t):
    return (1 - t) * np.asarray(c1) + t * np.asarray(c2)


def interpolate_palette(colors, u):
    colors = [np.asarray(c) for c in colors]
    u = np.clip(u, 0.0, 1.0)
    if u <= 0:
        return colors[0]
    if u >= 1:
        return colors[-1]
    pos = u * (len(colors) - 1)
    i = int(np.floor(pos))
    frac = pos - i
    return blend(colors[i], colors[i + 1], frac)


def soft_palette():
    bg_rgb = hex_to_rgb01(BG_COLOR)
    palette_hex = [
        "#5BCEFA", "#F5A9B8", "#F8F8F8", "#F5A9B8", "#5BCEFA",
        "#E40303", "#FF8C00", "#FFED00", "#008026", "#24408E", "#732982"
    ]
    out = []
    for hx in palette_hex:
        c = hex_to_rgb01(hx)
        if np.mean(c) > 0.92:
            c = blend(c, hex_to_rgb01("#d9dfe6"), 0.28)
            out.append(blend(c, bg_rgb, 0.09))
        else:
            out.append(blend(c, bg_rgb, 0.16))
    return out


def render():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    palette = soft_palette()

    n = 62
    s = np.linspace(0, 1, 1800)
    offsets = np.linspace(-1, 1, n)

    for i, a in enumerate(offsets):
        spread = (np.abs(a) ** 0.92) * np.sign(a)
        root_open = s ** 1.75
        root_wobble = s ** 2.15
        upper_release = s ** 1.55

        x = (
            0.5
            + 0.355 * spread * root_open
            + 0.028 * np.sin(2.4 * np.pi * s + 0.85 * a) * upper_release * (0.45 + 0.55 * np.abs(a))
            + 0.010 * np.sin(5.0 * np.pi * s + 1.4 * a) * root_wobble
        )
        x += 0.016 * (s ** 2.4) * (1 - a**2)

        y = (
            0.075
            + 0.825 * s
            - 0.042 * (1 - s) ** 1.55 * np.abs(a)
            + 0.019 * np.sin(np.pi * s) ** 1.6 * (1 - np.abs(a))
        )
        y += 0.012 * np.exp(-((s - 0.92) / 0.12) ** 2) * (0.25 - np.abs(a))

        lw = 0.52 + 1.00 * (1 - abs(a)) ** 0.7
        alpha = 0.28 + 0.64 * (1 - 0.60 * abs(a))

        u = i / (n - 1)
        u = 0.05 + 0.90 * (0.5 - 0.5 * np.cos(np.pi * u))
        color = interpolate_palette(palette, u)

        ax.plot(x, y, color=color, lw=lw, alpha=alpha, solid_capstyle='round')

    # Equation label
    ax.text(0.06, 0.06, "x=x\u2080+A\u00b7s\u1d56\u00b7sin(\u03c9s)",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "pride_unfurling.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
