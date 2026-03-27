"""
Geometry of Feeling — Pride: Shelter
Nested superellipse arches on slate — protective canopy shape.
Each arch narrows and flattens inward, transitioning through
a softened trans/pride palette from white through pink, blue,
gold, and violet.
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


def smooth_palette(cols, n):
    rgba = np.array([plt.matplotlib.colors.to_rgba(c) for c in cols])
    xs = np.linspace(0, 1, len(rgba))
    t = np.linspace(0, 1, n)
    return np.column_stack([np.interp(t, xs, rgba[:, k]) for k in range(4)])


def render():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    n = 24
    cols = smooth_palette(['#f6f2ef', '#f5a9b8', '#5bcffb', '#ffd100', '#7f2dbd'], n)
    s = np.linspace(-1, 1, 1000)

    for i in range(n):
        u = i / (n - 1)
        w = 0.35 - 0.009 * i
        h = 0.72 - 0.020 * i
        p = 1.10 + 0.45 * u
        x = 0.5 + w * s
        y = 0.18 + h * (1 - np.abs(s) ** p)
        ax.plot(x, y, color=cols[i], lw=1.1 if i < 6 else 1.0, alpha=0.95)

    # Equation label
    ax.text(0.06, 0.06, "y=h(1\u2212|s|^p)",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "pride_shelter.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
