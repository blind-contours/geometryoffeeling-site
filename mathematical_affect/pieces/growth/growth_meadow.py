"""
Geometry of Feeling — Growth: Meadow
55 stems at variable heights — a field in growth.
Heights drawn from Beta(3, 1.5), giving a natural
distribution: most stems tall, a few still rising.
y_n(t) = h_n · t, h_n ~ Beta(3, 1.5).
"""

import os
import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#F5F0E6'

# Layout
PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R
PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2

# Palette
DARK_G = '#2A4A1A'
LEAF = '#6A9A4A'
PALE_G = '#C8D8A8'

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def render():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')

    np.random.seed(77)
    n_lines = 55
    t = np.linspace(0, 1, 600)
    xs_pos = np.linspace(PAD_L + 0.04, PAD_L + PW - 0.04, n_lines)
    heights = np.random.beta(3, 1.5, n_lines) * 0.86 + 0.08

    dark_r = hex_to_rgb(DARK_G)
    mid_r = hex_to_rgb(LEAF)
    light_r = hex_to_rgb(PALE_G)

    for i, (x_base, h_frac) in enumerate(zip(xs_pos, heights)):
        frac = i / n_lines
        dist = x_base - cx

        xs_line = np.clip(
            x_base - dist * 0.14 * t +
            np.sin(t * np.pi * (2.5 + frac * 2) + frac * 3) * PW * 0.005 * h_frac,
            PAD_L + 0.02, PAD_L + PW - 0.02
        )
        ys_line = PAD_B + PH * 0.03 + PH * h_frac * t

        lw_profile = np.sin(t * np.pi) * 2.0 + 0.25
        n = len(xs_line) - 1

        pts = np.array([xs_line, ys_line]).T.reshape(-1, 1, 2)
        s = np.concatenate([pts[:-1], pts[1:]], axis=1)

        colors = []
        for j in range(n):
            tf = j / n
            if tf < 0.45:
                c = tuple(dark_r[k] + (mid_r[k] - dark_r[k]) * min(1, tf * 2.2)
                          for k in range(3))
            else:
                c = tuple(mid_r[k] + (light_r[k] - mid_r[k]) * (tf - 0.45) * 1.8
                          for k in range(3))
            colors.append((*c, 0.18 + 0.45 * (1 - abs(frac - 0.5) * 1.4)))

        lc = mc.LineCollection(s, linewidths=lw_profile[:n], colors=colors,
                               capstyle='round', zorder=3)
        ax.add_collection(lc)

    add_signature(fig, ax, BG_COLOR)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_meadow.pdf")
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    render()
