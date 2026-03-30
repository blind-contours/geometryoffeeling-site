"""
Geometry of Feeling — Desire: Desire Pursuit
Standalone render script
"""

"""
Geometry of Feeling -- Desire v2 (20 candidates)

Desire is pursuit, hunger, heat. Always moving toward, never arriving.
The mathematics of attraction — gravitational wells, pursuit curves, orbital decay.

User feedback on v1: Pursuit is best. Inspiral bigger. Hunger boring.
Flame needs to be bigger/more dynamic.

Direction: More heat, more urgency. Bigger spirals, more dynamic flames.

Dependencies: matplotlib, numpy, scipy
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
from matplotlib.patches import Circle
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#E8D8D0"

# Palette: deep crimson, heated gold, burgundy, dark rose, flame
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
    if smooth > 0: ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def draw_lc_gradient(ax, xs, ys, col, lw_s, lw_e, a_s, a_e, zo=4, smooth=0):
    if smooth > 0: ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    n = len(segs)
    alphas = np.linspace(a_s, a_e, n)
    lws = np.linspace(lw_s, lw_e, n)
    colors = [rgba(col, float(a)) for a in alphas]
    lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def draw_lc_gradient_xy(ax, xs, ys, col, lw_s, lw_e, a_s, a_e, zo=4, smooth=0):
    if smooth > 0:
        xs = gaussian_filter1d(xs, smooth)
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    n = len(segs)
    alphas = np.linspace(a_s, a_e, n)
    lws = np.linspace(lw_s, lw_e, n)
    colors = [rgba(col, float(a)) for a in alphas]
    lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def glow(ax, x, y, col, r_max=0.20):
    """Draw a glowing point."""
    for r, a in [(r_max, 0.06), (r_max*0.6, 0.14), (r_max*0.3, 0.35), (r_max*0.12, 0.70)]:
        ax.add_patch(Circle((x, y), radius=r, facecolor=rgba(col, a),
                     edgecolor='none', zorder=6))

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Ensure name ends with .pdf
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

# =============================================================================
# 1. PURSUIT (kept — Lotka-Volterra phase-space orbits)
# =============================================================================
def render():
    fig, ax = make_fig()
    alpha_lv = 1.0; beta_lv = 0.1; delta_lv = 0.075; gamma_lv = 1.5
    dt = 0.002; steps = 18000
    configs = [
        (10.0, 5.0,  CRIMSON,   HEATED,   0.90, 2.5),
        (8.0,  8.0,  PULSE_COL, GILT,     0.85, 2.2),
        (15.0, 3.0,  BURGUNDY,  FLAME,    0.80, 2.0),
        (12.0, 6.0,  DARKROSE,  SMOLDER,  0.75, 1.7),
        (6.0,  10.0, WINE,      HEATED,   0.72, 1.4),
        (20.0, 2.0,  FLAME,     GILT,     0.68, 1.8),
        (4.0,  12.0, CRIMSON,   DARKROSE, 0.65, 1.3),
        (18.0, 4.0,  HEATED,    BURGUNDY, 0.62, 1.5),
    ]
    x_star = gamma_lv / delta_lv
    y_star = alpha_lv / beta_lv
    for x0, y0, col_x, col_y, alpha_base, lw in configs:
        x_vals = [float(x0)]; y_vals = [float(y0)]
        for _ in range(steps):
            xv, yv = x_vals[-1], y_vals[-1]
            dx_dt = (alpha_lv * xv - beta_lv * xv * yv) * dt
            dy_dt = (delta_lv * xv * yv - gamma_lv * yv) * dt
            x_vals.append(max(0.01, xv + dx_dt))
            y_vals.append(max(0.01, yv + dy_dt))
        x_arr = np.array(x_vals); y_arr = np.array(y_vals)
        x_min, x_max = 0.5, max(x_arr.max(), 35)
        y_min, y_max = 0.5, max(y_arr.max(), 18)
        x_norm = (x_arr - x_min) / (x_max - x_min + 1e-9)
        y_norm = (y_arr - y_min) / (y_max - y_min + 1e-9)
        xs_p = PAD_L + PW * 0.04 + PW * 0.92 * x_norm
        ys_p = PAD_B + PH * 0.04 + PH * 0.92 * y_norm
        mask = ((xs_p > PAD_L) & (xs_p < PAD_L + PW) &
                (ys_p > PAD_B) & (ys_p < PAD_B + PH))
        for sx, sy in split_segments(xs_p, ys_p, mask):
            pts = np.array([sx, sy]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            n_s = len(segs)
            col_x_rgb = hex_to_rgb(col_x); col_y_rgb = hex_to_rgb(col_y)
            colors = []
            for k in range(n_s):
                phase = 0.5 + 0.5 * np.sin(2 * np.pi * k / n_s * 3)
                r = col_x_rgb[0]*(1-phase)+col_y_rgb[0]*phase
                g = col_x_rgb[1]*(1-phase)+col_y_rgb[1]*phase
                b = col_x_rgb[2]*(1-phase)+col_y_rgb[2]*phase
                colors.append((r, g, b, alpha_base))
            lws = np.linspace(lw * 0.4, lw, n_s)
            lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                   capstyle='round', zorder=3)
            ax.add_collection(lc)
    x_s = PAD_L + PW * 0.04 + PW * 0.92 * (x_star - 0.5) / (35 - 0.5)
    y_s = PAD_B + PH * 0.04 + PH * 0.92 * (y_star - 0.5) / (18 - 0.5)
    glow(ax, x_s, y_s, GILT, 0.35)
    add_signature(fig, ax, BG)
    save(fig, "desire_pursuit")

if __name__ == '__main__':
    render()
