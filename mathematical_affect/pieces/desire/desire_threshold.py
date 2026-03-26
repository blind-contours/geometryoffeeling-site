"""
Geometry of Feeling — Desire: Desire Threshold
Standalone render script
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#E8D8D0"

CRIMSON   = "#9A2030"; HEATED  = "#C88030"; BURGUNDY = "#6A2038"
DARKROSE  = "#8A3848"; FLAME   = "#D06020"; WINE     = "#5A1828"
PULSE_COL = "#B83040"; SMOLDER = "#7A4028"; GILT     = "#C4A040"
EMBER     = "#C05030"; SCARLET = "#D02838"

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2; cy = PAD_B + PH / 2

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    return fig, ax

def label(ax, eq):
    ax.text(0.75, 0.75, eq, fontfamily='monospace', fontsize=10,
            color=(0.55, 0.40, 0.35, 0.40), transform=ax.transData)

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if smooth > 0: ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def render():
    fig, ax = make_fig()
    y_thresh = PAD_B + PH * 0.85
    ax.plot([PAD_L, PAD_L + PW], [y_thresh, y_thresh],
            color=rgba(GILT, 0.08), linewidth=0.6, linestyle=':', zorder=2)
    t = np.linspace(0, 1, 2000)
    xs = PAD_L + PW * t
    n = 22
    for i in range(n):
        frac = i / (n - 1)
        k = 3 + frac * 12
        y_start = PAD_B + PH * (0.05 + frac * 0.15)
        y_range = y_thresh - y_start
        ys = y_start + y_range * (1 / (1 + np.exp(-k * (t - 0.5))))
        if frac < 0.25: col = BURGUNDY
        elif frac < 0.5: col = CRIMSON
        elif frac < 0.75: col = FLAME
        else: col = HEATED
        alpha = 0.12 + 0.50 * (1 - abs(frac - 0.5) * 1.3)
        lw = 0.5 + 1.2 * (1 - abs(frac - 0.5))
        draw_lc(ax, xs, ys, col, lw=lw, alpha=alpha, zo=3)
    label(ax, "y=L/(1+e^(\u2212k(t\u2212t\u2080)))")
    save(fig, "desire_threshold")


if __name__ == '__main__':
    render()
