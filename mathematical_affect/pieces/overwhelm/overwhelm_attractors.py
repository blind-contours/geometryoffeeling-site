"""
Geometry of Feeling — Overwhelm: Overwhelm Attractors
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

DPI = 300
FIG_W = 12
FIG_H = 8
BG = "#0A0A12"

# Palette: 10+ vivid colors competing for attention
ACID = "#E8D820"
FIRE = "#E05010"
COBALT = "#2255C8"
CRIMSON = "#C82050"
EMERALD = "#20B870"
VIOLET = "#A020C8"
AMBER = "#E8A020"
CYAN = "#20C8C8"
MAGENTA = "#C82888"
LIME = "#88C820"
COLS = [ACID, FIRE, COBALT, CRIMSON, EMERALD,
        VIOLET, AMBER, CYAN, MAGENTA, LIME]

PAD_L = 0.72
PAD_R = 0.60
PAD_T = 0.65
PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R
PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2
cy = PAD_B + PH / 2

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')
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
    print(f"  saved {name}")

# =============================================================================
# 1. ATTRACTORS — Four strange attractors overlaid in the same visual space
#    Lorenz, Rossler, Chen, and Halvorsen systems — each with its own topology,
#    all fighting for the same canvas. Multiple trajectories per system.
#
#    Lorenz:    dx=sigma(y-x), dy=x(rho-z)-y, dz=xy-beta*z
#    Rossler:   dx=-y-z, dy=x+a*y, dz=b+z(x-c)
#    Chen:      dx=a(y-x), dy=(c-a)x-xz+cy, dz=xy-bz
#    Halvorsen: dx=-a*x-4y-4z-y^2, dy=-a*y-4z-4x-z^2, dz=-a*z-4x-4y-x^2
# =============================================================================
def _integrate_lorenz(x0, y0, z0, dt, n, sigma=10, rho=28, beta=8/3):
    xs, ys, zs = [x0], [y0], [z0]
    x, y, z = x0, y0, z0
    for _ in range(n):
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        x += dx; y += dy; z += dz
        xs.append(x); ys.append(y); zs.append(z)
    return np.array(xs), np.array(ys), np.array(zs)

def _integrate_rossler(x0, y0, z0, dt, n, a=0.2, b=0.2, c=5.7):
    xs, ys, zs = [x0], [y0], [z0]
    x, y, z = x0, y0, z0
    for _ in range(n):
        dx = (-y - z) * dt
        dy = (x + a * y) * dt
        dz = (b + z * (x - c)) * dt
        x += dx; y += dy; z += dz
        xs.append(x); ys.append(y); zs.append(z)
    return np.array(xs), np.array(ys), np.array(zs)

def _integrate_chen(x0, y0, z0, dt, n, a=35, b=3, c=28):
    xs, ys, zs = [x0], [y0], [z0]
    x, y, z = x0, y0, z0
    for _ in range(n):
        dx = (a * (y - x)) * dt
        dy = ((c - a) * x - x * z + c * y) * dt
        dz = (x * y - b * z) * dt
        x += dx; y += dy; z += dz
        xs.append(x); ys.append(y); zs.append(z)
    return np.array(xs), np.array(ys), np.array(zs)

def _integrate_halvorsen(x0, y0, z0, dt, n, a=1.89):
    xs, ys, zs = [x0], [y0], [z0]
    x, y, z = x0, y0, z0
    for _ in range(n):
        dx = (-a * x - 4 * y - 4 * z - y**2) * dt
        dy = (-a * y - 4 * z - 4 * x - z**2) * dt
        dz = (-a * z - 4 * x - 4 * y - x**2) * dt
        x += dx; y += dy; z += dz
        xs.append(x); ys.append(y); zs.append(z)
    return np.array(xs), np.array(ys), np.array(zs)

def _normalize_to_canvas(raw_x, raw_y, pad_frac=0.08):
    """Map arbitrary-range data to canvas drawing area."""
    xmin, xmax = raw_x.min(), raw_x.max()
    ymin, ymax = raw_y.min(), raw_y.max()
    xr = xmax - xmin if xmax != xmin else 1
    yr = ymax - ymin if ymax != ymin else 1
    nx = PAD_L + PW * (pad_frac + (1 - 2*pad_frac) * (raw_x - xmin) / xr)
    ny = PAD_B + PH * (pad_frac + (1 - 2*pad_frac) * (raw_y - ymin) / yr)
    return nx, ny

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def render():
    fig, ax = make_fig()
    np.random.seed(42)

    # --- Lorenz: 4 trajectories, project x-z ---
    lorenz_cols = [FIRE, CRIMSON, AMBER, MAGENTA]
    all_lx, all_lz = [], []
    lorenz_data = []
    for i in range(4):
        lx, ly, lz = _integrate_lorenz(
            1.0 + np.random.randn()*0.5,
            1.0 + np.random.randn()*0.5,
            1.0 + np.random.randn()*0.5,
            dt=0.004, n=18000)
        all_lx.extend(lx); all_lz.extend(lz)
        lorenz_data.append((lx, lz))
    all_lx, all_lz = np.array(all_lx), np.array(all_lz)
    lx_min, lx_max = all_lx.min(), all_lx.max()
    lz_min, lz_max = all_lz.min(), all_lz.max()
    lx_range = lx_max - lx_min if lx_max != lx_min else 1
    lz_range = lz_max - lz_min if lz_max != lz_min else 1

    for i, (lx, lz) in enumerate(lorenz_data):
        nx = PAD_L + PW * (0.05 + 0.90 * (lx - lx_min) / lx_range)
        ny = PAD_B + PH * (0.05 + 0.90 * (lz - lz_min) / lz_range)
        mask = ((nx > PAD_L) & (nx < PAD_L + PW) &
                (ny > PAD_B) & (ny < PAD_B + PH))
        for seg_xs, seg_ys in split_segments(nx, ny, mask):
            draw_lc(ax, seg_xs, seg_ys, lorenz_cols[i],
                    lw=0.7, alpha=0.45, zo=3 + i)

    # --- Rossler: 4 trajectories, project x-y ---
    rossler_cols = [COBALT, CYAN, EMERALD, LIME]
    all_rx, all_ry = [], []
    rossler_data = []
    for i in range(4):
        rx, ry, rz = _integrate_rossler(
            1.0 + np.random.randn()*0.3,
            0.5 + np.random.randn()*0.3,
            0.5 + np.random.randn()*0.3,
            dt=0.005, n=16000)
        all_rx.extend(rx); all_ry.extend(ry)
        rossler_data.append((rx, ry))
    all_rx, all_ry = np.array(all_rx), np.array(all_ry)
    rx_min, rx_max = all_rx.min(), all_rx.max()
    ry_min, ry_max = all_ry.min(), all_ry.max()
    rx_range = rx_max - rx_min if rx_max != rx_min else 1
    ry_range = ry_max - ry_min if ry_max != ry_min else 1

    for i, (rx, ry) in enumerate(rossler_data):
        nx = PAD_L + PW * (0.05 + 0.90 * (rx - rx_min) / rx_range)
        ny = PAD_B + PH * (0.05 + 0.90 * (ry - ry_min) / ry_range)
        mask = ((nx > PAD_L) & (nx < PAD_L + PW) &
                (ny > PAD_B) & (ny < PAD_B + PH))
        for seg_xs, seg_ys in split_segments(nx, ny, mask):
            draw_lc(ax, seg_xs, seg_ys, rossler_cols[i],
                    lw=0.6, alpha=0.40, zo=7 + i)

    # --- Chen: 3 trajectories, project x-z ---
    chen_cols = [VIOLET, MAGENTA, ACID]
    all_cx_list, all_cz = [], []
    chen_data = []
    for i in range(3):
        chx, chy, chz = _integrate_chen(
            -0.1 + np.random.randn()*2,
            0.5 + np.random.randn()*2,
            14.0 + np.random.randn()*2,
            dt=0.001, n=25000)
        all_cx_list.extend(chx); all_cz.extend(chz)
        chen_data.append((chx, chz))
    all_cx_arr, all_cz_arr = np.array(all_cx_list), np.array(all_cz)
    cx_min, cx_max = all_cx_arr.min(), all_cx_arr.max()
    cz_min, cz_max = all_cz_arr.min(), all_cz_arr.max()
    cx_range = cx_max - cx_min if cx_max != cx_min else 1
    cz_range = cz_max - cz_min if cz_max != cz_min else 1

    for i, (chx, chz) in enumerate(chen_data):
        nx = PAD_L + PW * (0.05 + 0.90 * (chx - cx_min) / cx_range)
        ny = PAD_B + PH * (0.05 + 0.90 * (chz - cz_min) / cz_range)
        mask = ((nx > PAD_L) & (nx < PAD_L + PW) &
                (ny > PAD_B) & (ny < PAD_B + PH))
        for seg_xs, seg_ys in split_segments(nx, ny, mask):
            draw_lc(ax, seg_xs, seg_ys, chen_cols[i],
                    lw=0.55, alpha=0.38, zo=11 + i)

    # --- Halvorsen: 3 trajectories, project x-y ---
    halv_cols = [AMBER, LIME, CYAN]
    all_hx, all_hy = [], []
    halv_data = []
    for i in range(3):
        hx, hy, hz = _integrate_halvorsen(
            -1.5 + np.random.randn()*0.5,
            -1.5 + np.random.randn()*0.5,
            -1.5 + np.random.randn()*0.5,
            dt=0.003, n=15000)
        all_hx.extend(hx); all_hy.extend(hy)
        halv_data.append((hx, hy))
    all_hx, all_hy = np.array(all_hx), np.array(all_hy)
    hx_min, hx_max = all_hx.min(), all_hx.max()
    hy_min, hy_max = all_hy.min(), all_hy.max()
    hx_range = hx_max - hx_min if hx_max != hx_min else 1
    hy_range = hy_max - hy_min if hy_max != hy_min else 1

    for i, (hx, hy) in enumerate(halv_data):
        nx = PAD_L + PW * (0.05 + 0.90 * (hx - hx_min) / hx_range)
        ny = PAD_B + PH * (0.05 + 0.90 * (hy - hy_min) / hy_range)
        mask = ((nx > PAD_L) & (nx < PAD_L + PW) &
                (ny > PAD_B) & (ny < PAD_B + PH))
        for seg_xs, seg_ys in split_segments(nx, ny, mask):
            draw_lc(ax, seg_xs, seg_ys, halv_cols[i],
                    lw=0.5, alpha=0.35, zo=14 + i)

    add_signature(fig, ax, BG)
    save(fig, "overwhelm_attractors.pdf")

if __name__ == '__main__':
    render()
