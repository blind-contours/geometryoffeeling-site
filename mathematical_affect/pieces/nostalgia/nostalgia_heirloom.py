"""
Geometry of Feeling — Nostalgia: Nostalgia Heirloom
Standalone render script
"""

import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
from scipy.interpolate import CubicSpline
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#F0E8D8"

# Palette — memory colors
AMBER = "#B8863A"; SEPIA = "#8A6A42"; FADED_BLUE = "#6A88A8"
OCHRE = "#C4963A"; DUSTY_ROSE = "#A07868"; OLD_GOLD = "#A89048"
WARM_BROWN = "#7A5A3A"; TARNISH = "#887858"; FADED_WINE = "#886068"
DARK_AMBER = "#7A5A20"; LAVENDER = "#8878A8"; SAGE = "#788868"

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))

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
cx = PAD_L + PW/2; cy = PAD_B + PH/2

def split_segments(xs, ys, mask):
    segments = []
    in_seg = False; start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j; in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3:
                segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3:
        segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def draw_lc_gradient(ax, xs, ys, col, lw_start, lw_end, a_start, a_end, zo=4, smooth=0):
    """Draw a line collection with gradient alpha and linewidth."""
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    n = len(segs)
    alphas = np.linspace(a_start, a_end, n)
    lws = np.linspace(lw_start, lw_end, n)
    colors = [rgba(col, float(a)) for a in alphas]
    lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
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
    np.random.seed(166)

    # A shape (vessel/vase profile) repeated at different scales, each fainter
    n_generations = 10
    cols_list = [DARK_AMBER, AMBER, SEPIA, OLD_GOLD, DUSTY_ROSE,
                 FADED_BLUE, WARM_BROWN, TARNISH, FADED_WINE, SAGE]

    t = np.linspace(0, 2 * np.pi, 600)

    for i in range(n_generations):
        frac = i / (n_generations - 1)

        # Vase/vessel profile — superposition of harmonics
        r = 1.0 + 0.3 * np.cos(2*t) + 0.15 * np.cos(3*t) + 0.08 * np.cos(5*t)

        # Each generation slightly distorted
        distort = 1.0 + frac * 0.15 * np.sin(7 * t + i * 0.5)
        r = r * distort

        scale = PW * (0.12 + frac * 0.22)
        xs_h = cx + scale * r * np.cos(t)
        ys_h = cy + scale * r * np.sin(t) * (PH / PW)

        # Clip
        mask = ((xs_h > PAD_L) & (xs_h < PAD_L + PW) &
                (ys_h > PAD_B) & (ys_h < PAD_B + PH))

        alpha = 0.50 * (1 - frac * 0.7)
        lw = 2.0 * (1 - frac * 0.5) + 0.3

        for seg_xs, seg_ys in split_segments(xs_h, ys_h, mask):
            if len(seg_xs) < 5: continue
            draw_lc(ax, seg_xs, seg_ys, cols_list[i], lw=lw, alpha=alpha, zo=10-i, smooth=1)

    add_signature(fig, ax, BG)
    save(fig, "nostalgia_heirloom.pdf")

if __name__ == '__main__':
    render()
