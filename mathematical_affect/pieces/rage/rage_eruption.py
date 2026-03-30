"""
Geometry of Feeling — Rage: Rage Eruption
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
from matplotlib.patches import Circle
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#0E0E12"  # very dark — rage lives in darkness

# Palette: violent contrast against near-black
CRIMSON = "#C02020"; BLACK_ACCENT = "#181818"; EXPLOSIVE = "#E06020"
BLOOD = "#8A1818"; HOT_WHITE = "#F0E8E0"
SCAR = "#E04030"; EMBER = "#D05020"; ASH = "#808088"
FURNACE = "#C83818"; WOUND = "#A02028"

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2; cy = PAD_B + PH / 2

EQ_OPACITY = 0.55
SERIES_OPACITY = 0.38

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

def split_segments(xs, ys, mask):
    """Split masked arrays into contiguous segments to avoid straight-line jumps."""
    segments = []
    in_seg = False
    start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j
            in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3:
                segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3:
        segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4):
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def render():
    fig, ax = make_fig()
    np.random.seed(77)
    n_rays = 100
    for i in range(n_rays):
        angle = np.random.uniform(0, 2 * np.pi)
        t = np.linspace(0, 1, 400)
        speed = np.random.uniform(0.6, 1.0)
        r = PW * 0.52 * t * speed
        # Very slight wobble — explosive rays, not coiled springs
        wobble_amp = np.random.uniform(0.01, 0.04)
        wobble = wobble_amp * np.sin(np.random.uniform(2, 6) * np.pi * t +
                                      np.random.uniform(0, 6))
        xs_r = cx + r * np.cos(angle + wobble)
        ys_r = cy + r * np.sin(angle + wobble)
        mask = ((xs_r > PAD_L) & (xs_r < PAD_L + PW) &
                (ys_r > PAD_B) & (ys_r < PAD_B + PH))
        if mask.sum() < 3:
            continue
        cols = [CRIMSON, EXPLOSIVE, SCAR, FURNACE, EMBER, WOUND, HOT_WHITE, BLOOD]
        col = cols[i % len(cols)]
        for seg_xs, seg_ys in split_segments(xs_r, ys_r, mask):
            pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            n_s = len(segs)
            alphas = np.linspace(0.80, 0.08, n_s)
            lws = np.linspace(3.5, 0.4, n_s)
            colors = [rgba(col, float(a)) for a in alphas]
            lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                   capstyle='round', zorder=3 + i % 5)
            ax.add_collection(lc)
    # white-hot core
    for r_c, a in [(0.30, 0.06), (0.15, 0.18), (0.06, 0.45), (0.02, 0.80)]:
        ax.add_patch(Circle((cx, cy), radius=r_c,
                    facecolor=rgba(HOT_WHITE, a), edgecolor='none', zorder=8))
    add_signature(fig, ax, BG)
    save(fig, "rage_eruption.pdf")

if __name__ == '__main__':
    render()
