"""
Geometry of Feeling — Rage: Rage Shockwave
Standalone render script
"""

import numpy as np
import matplotlib
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

def label(ax, eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.85,0.80,0.75,EQ_OPACITY),transform=ax.transData)
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
    np.random.seed(166)
    n_rings = 30
    for i in range(n_rings):
        frac = i / (n_rings - 1)
        r = PW * 0.03 + frac * PW * 0.48
        # polygon ring with sharp edges (not smooth circle)
        n_sides = np.random.randint(5, 12)
        angles = np.linspace(0, 2 * np.pi, n_sides + 1)
        # add perturbation to radius at each vertex
        r_perturbed = r + np.random.uniform(-r * 0.12, r * 0.12, n_sides + 1)
        r_perturbed[-1] = r_perturbed[0]  # close the polygon
        xs_r = cx + r_perturbed * np.cos(angles)
        ys_r = cy + r_perturbed * np.sin(angles) * (PH / PW)
        mask = ((xs_r > PAD_L) & (xs_r < PAD_L + PW) &
                (ys_r > PAD_B) & (ys_r < PAD_B + PH))
        if mask.sum() < 3:
            continue
        for seg_xs, seg_ys in split_segments(xs_r, ys_r, mask):
            if len(seg_xs) < 2:
                continue
            col_choices = [CRIMSON, EXPLOSIVE, SCAR, FURNACE, WOUND, EMBER]
            col = col_choices[i % len(col_choices)]
            lw = 3.5 - frac * 2.0
            alpha = 0.70 - frac * 0.50
            draw_lc(ax, seg_xs, seg_ys, col, lw=max(0.8, lw),
                    alpha=max(0.12, alpha), zo=5 - i % 3)
        # also interpolate for denser rings
        if n_sides < 20:
            theta_dense = np.linspace(0, 2 * np.pi, 200)
            r_interp = np.interp(theta_dense, angles, r_perturbed)
            xs_d = cx + r_interp * np.cos(theta_dense)
            ys_d = cy + r_interp * np.sin(theta_dense) * (PH / PW)
            mask_d = ((xs_d > PAD_L) & (xs_d < PAD_L + PW) &
                      (ys_d > PAD_B) & (ys_d < PAD_B + PH))
            for seg_xs, seg_ys in split_segments(xs_d, ys_d, mask_d):
                if len(seg_xs) < 3:
                    continue
                col = col_choices[i % len(col_choices)]
                draw_lc(ax, seg_xs, seg_ys, col, lw=max(0.6, lw * 0.7),
                        alpha=max(0.08, alpha * 0.6), zo=4 - i % 3)
    # hot core
    for r_c, a in [(0.18, 0.10), (0.08, 0.30), (0.03, 0.65)]:
        ax.add_patch(Circle((cx, cy), radius=r_c,
                    facecolor=rgba(HOT_WHITE, a), edgecolor='none', zorder=8))
    label(ax, "concentric polygonal fronts,  r_k=r\u2080+k\u0394r")
    save(fig, "rage_shockwave.pdf")


if __name__ == '__main__':
    render()
