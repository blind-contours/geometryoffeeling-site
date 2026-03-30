"""
Geometry of Feeling — Peace: Peace Harmonic
Standalone render script
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle, Ellipse
from scipy.ndimage import gaussian_filter1d
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#F0EDE8"  # warm parchment — NOT pure white

# Palette: deep but calm — visible against warm background
DEEP_SAGE = "#4A6A52"; OCEAN = "#3A5A6A"; WARM_GREY = "#6A6860"
CLAY = "#8A7A68"; LICHEN = "#5A7A5A"; STONE = "#7A7A72"
CEDAR = "#5A5040"; MOSS = "#3A5A3A"; DUSK = "#6A5A7A"
WATER = "#4A6A80"; EARTH = "#6A5A48"; FOG_COL = "#8A8A82"
SKY = "#7A8A9A"; BARK = "#5A4A38"; FERN = "#4A6A4A"
RUST = "#8A6A4A"; PLUM = "#6A4A5A"; SAND_COL = "#9A8A72"
MINERAL = "#5A6A6A"; SHADOW = "#4A4A48"

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

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2; cy = PAD_B + PH / 2

def label(ax, eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.40,0.45,0.40,0.22),transform=ax.transData)
def split_segments(xs, ys, mask):
    segments = []; in_seg = False; start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg: start = j; in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3: segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3: segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if len(xs) < 2: return
    if smooth > 0: ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def save(fig, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith('.pdf'):
        name = name + '.pdf'
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f'saved {name}')


def render():
    fig, ax = make_fig()
    n = 16
    cols = [DEEP_SAGE, OCEAN, WATER, LICHEN, STONE, MINERAL, DUSK, CEDAR,
            MOSS, FERN, CLAY, WARM_GREY, SKY, PLUM, EARTH, RUST]
    t = np.linspace(0, 1, 2000)
    xs = PAD_L + PW * t
    for i in range(n):
        frac = i / (n - 1)
        y_base = PAD_B + PH * (0.06 + frac * 0.88)
        # Standing wave: sin(nπx)
        mode = i + 1
        amp = PH * 0.03 * (1 - frac * 0.3)
        ys = y_base + amp * np.sin(mode * np.pi * t)
        col = cols[i]
        alpha = 0.45 + 0.10 * np.sin(np.pi * frac)
        lw = 0.8 + 0.5 * (1 - frac * 0.5)
        draw_lc(ax, xs, ys, col, lw=lw, alpha=alpha, zo=3, smooth=2)
    label(ax, "\u03c8=A\u00b7sin(n\u03c0x/L)\u00b7sin(n\u03c0y/L)")
    save(fig, "peace_harmonic.pdf")


if __name__ == '__main__':
    render()
