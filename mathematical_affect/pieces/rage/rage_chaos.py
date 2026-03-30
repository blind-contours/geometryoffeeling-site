"""
Geometry of Feeling — Rage: Rage Chaos
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
    sigma = 10.0; rho = 28.0; beta = 8.0 / 3.0
    dt = 0.005; n_steps = 15000
    n_traj = 8
    np.random.seed(66)
    cols_list = [CRIMSON, EXPLOSIVE, SCAR, FURNACE, WOUND, EMBER, BLOOD, CRIMSON]
    # First pass: compute attractor bounds to properly center and scale
    np.random.seed(66)
    all_xs = []; all_zs = []
    init_states = []
    for ti in range(n_traj):
        x0 = 1.0 + np.random.randn() * 0.01
        y0 = 1.0 + np.random.randn() * 0.01
        z0 = 1.0 + np.random.randn() * 0.01
        init_states.append((x0, y0, z0))
        x, y, z = x0, y0, z0
        for k in range(n_steps):
            dx = sigma * (y - x) * dt
            dy = (x * (rho - z) - y) * dt
            dz = (x * y - beta * z) * dt
            x += dx; y += dy; z += dz
            all_xs.append(x); all_zs.append(z)
    all_xs = np.array(all_xs); all_zs = np.array(all_zs)
    x_center = (all_xs.max() + all_xs.min()) / 2
    z_center = (all_zs.max() + all_zs.min()) / 2
    x_range = all_xs.max() - all_xs.min()
    z_range = all_zs.max() - all_zs.min()
    # Scale independently per axis to fill the drawing area
    scale_x = PW * 0.90 / (x_range + 1e-6)
    scale_z = PH * 0.82 / (z_range + 1e-6)

    for ti in range(n_traj):
        x, y, z = init_states[ti]
        xs_l = []; ys_l = []
        for k in range(n_steps):
            dx = sigma * (y - x) * dt
            dy = (x * (rho - z) - y) * dt
            dz = (x * y - beta * z) * dt
            x += dx; y += dy; z += dz
            xs_l.append(x); ys_l.append(z)
        xs_arr = np.array(xs_l); ys_arr = np.array(ys_l)
        # Center on canvas, scale each axis independently for best fill
        xs_n = cx + (xs_arr - x_center) * scale_x
        ys_n = cy + (ys_arr - z_center) * scale_z
        mask = ((xs_n > PAD_L) & (xs_n < PAD_L + PW) &
                (ys_n > PAD_B) & (ys_n < PAD_B + PH))
        if mask.sum() < 3:
            continue
        col = cols_list[ti % len(cols_list)]
        for seg_xs, seg_ys in split_segments(xs_n, ys_n, mask):
            pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            n_s = len(segs)
            alphas = np.linspace(0.65, 0.12, n_s)
            lws = np.linspace(2.8, 0.7, n_s)
            colors = [rgba(col, float(a)) for a in alphas]
            lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                   capstyle='round', zorder=3 + ti)
            ax.add_collection(lc)
    add_signature(fig, ax, BG)
    save(fig, "rage_chaos.pdf")

if __name__ == '__main__':
    render()
