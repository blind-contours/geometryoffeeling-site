"""
Geometry of Feeling — Pride: Waves
Many Waves, One Sea — ocean surface lines in a softened Pride palette.
72 perspective-projected wave lines moving through the classic rainbow,
blended toward the warm paper background so it reads as art, not poster.
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


def render():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    bg_rgb = hex_to_rgb01(BG_COLOR)

    # Classic rainbow Pride palette, softened toward background
    pride_hex = ["#E40303", "#FF8C00", "#FFED00", "#008026", "#24408E", "#732982"]
    pride_rgb = [hex_to_rgb01(c) for c in pride_hex]
    softened_pride = [blend(c, bg_rgb, 0.22) for c in pride_rgb]

    z_min, z_max, n_lines = 0.34, 8.2, 72
    t = np.linspace(0, 1, n_lines)
    z_values = z_min + (t ** 1.75) * (z_max - z_min)
    z_values = z_values[::-1]

    x_limit = 9.5
    camera_offset = 1.05

    for idx, z in enumerate(z_values):
        x = np.linspace(-x_limit, x_limit, 2600)

        h = (
            0.095 * np.cos(0.78 * x + 1.72 * z - 0.30) * np.exp(-0.080 * z)
            + 0.032 * np.cos(2.10 * x - 1.30 * z + 1.05) * np.exp(-0.10 * z)
            + 0.165 * np.exp(-((z - 1.55) / 1.10) ** 2) * np.exp(-((x - 0.55) / 4.15) ** 2)
            + 0.080 * np.exp(-((z - 0.92) / 0.72) ** 2) * np.exp(-((x + 2.25) / 2.35) ** 2)
        )

        d = z + camera_offset
        x_screen = 0.5 + 0.455 * (x / d)
        y_screen = 0.665 - 0.585 / d + 0.39 * (h / d)

        depth_norm = (z - z_min) / (z_max - z_min)
        alpha = 0.14 + 0.80 * (1 - depth_norm) ** 0.70
        lw = 0.52 + 0.92 * (1 - depth_norm) ** 0.60

        u = idx / (n_lines - 1)
        u = 0.06 + 0.88 * (0.5 - 0.5 * np.cos(np.pi * u))
        line_rgb = interpolate_palette(softened_pride, u)

        ax.plot(x_screen, y_screen, color=line_rgb, lw=lw, alpha=alpha,
                solid_capstyle='round', clip_on=True)

    # Equation label
    ax.text(0.06, 0.06, "h=\u03a3A\u1d62cos(k\u1d62x\u2212\u03c9\u1d62t)",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "pride_waves.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
