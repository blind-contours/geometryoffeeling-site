"""
Geometry of Feeling — Growth: Phyllotaxis
Golden-angle spirals — each element placed 137.508° from the last.
Fibonacci spirals traced through the arrangement. The same rule
sunflowers use to pack seeds, rendered as botanical geometry.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#F5F0E6'

GOLDEN_ANGLE = 137.50776405  # degrees


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

    # Rich green-gold palette
    palette_hex = ['#1A3A1A', '#1F4F1F', '#2D5A2D', '#3A6B3A',
                   '#4A7C4A', '#5C9A3A', '#6BAF4A', '#8BC362',
                   '#A8C890', '#C89028', '#D4A832', '#D8C878']
    palette = [blend(hex_to_rgb01(h), bg_rgb, 0.04) for h in palette_hex]

    cx, cy = 0.50, 0.50
    aspect = 8.0 / 12.0
    n_elements = 1400
    max_r = 0.44

    # Generate all positions
    xs = np.zeros(n_elements)
    ys = np.zeros(n_elements)
    rs = np.zeros(n_elements)

    for n in range(n_elements):
        theta = np.radians((n + 1) * GOLDEN_ANGLE)
        r = max_r * np.sqrt((n + 1) / n_elements)
        xs[n] = cx + r * np.cos(theta) * aspect
        ys[n] = cy + r * np.sin(theta)
        rs[n] = r

    # --- Draw Fibonacci spiral curves ---
    # Connect elements separated by Fibonacci numbers
    for fib_step in [13, 21, 34]:
        spiral_segs = []
        spiral_colors = []
        spiral_widths = []

        for n in range(fib_step, n_elements):
            dist = np.sqrt((xs[n] - xs[n - fib_step]) ** 2 +
                           (ys[n] - ys[n - fib_step]) ** 2)
            if dist < 0.08:
                spiral_segs.append([(xs[n], ys[n]), (xs[n - fib_step], ys[n - fib_step])])
                u = (rs[n] / max_r) ** 0.5
                c = interpolate_palette(palette, u)
                outer_frac = rs[n] / max_r
                alpha = 0.06 + 0.18 * (1 - outer_frac) ** 0.5
                w = 0.20 + 0.45 * (1 - outer_frac)
                spiral_colors.append((*c, alpha))
                spiral_widths.append(w)

        if spiral_segs:
            lc = LineCollection(spiral_segs, colors=spiral_colors,
                                linewidths=spiral_widths, capstyle='round')
            ax.add_collection(lc)

    # --- Draw seed elements ---
    for n in range(n_elements):
        u = (rs[n] / max_r) ** 0.50
        c = interpolate_palette(palette, u)

        # Size: small at center, larger at edges
        frac = (n + 1) / n_elements
        size = 2.0 + 7.5 * frac ** 0.50
        alpha = 0.55 + 0.40 * frac ** 0.25

        ax.plot(xs[n], ys[n], 'o', color=(*c, alpha),
                markersize=size, markeredgewidth=0)

    # Equation label
    ax.text(0.06, 0.06, "\u03b8\u2099=n\u00b7137.508\u00b0, r\u2099=c\u221an",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_phyllotaxis.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
