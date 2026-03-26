"""
Geometry of Feeling — Desire: Desire Inspiral
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
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
from matplotlib.patches import Circle
import os


DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#2A2018"

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

def label(ax, eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.85,0.75,0.65,0.50),transform=ax.transData)
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
    for r, a in [(r_max, 0.03), (r_max*0.6, 0.08), (r_max*0.3, 0.20), (r_max*0.12, 0.45)]:
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
# 2. INSPIRAL (improved — much bigger, more layers)
# =============================================================================
def render():
    fig, ax = make_fig()
    n_layers = 14
    for i in range(n_layers):
        frac = i / (n_layers - 1)
        theta = np.linspace(0, 14 * np.pi, 8000)
        r0 = PH * (0.15 + frac * 0.42)
        gamma_d = 0.030 + frac * 0.040
        r = r0 * np.exp(-gamma_d * theta)
        xs_a = cx + r * np.cos(theta + i * np.pi / n_layers)
        ys_a = cy + r * np.sin(theta + i * np.pi / n_layers) * 0.85
        xs_b = cx + r * np.cos(theta + np.pi + i * np.pi / n_layers)
        ys_b = cy + r * np.sin(theta + np.pi + i * np.pi / n_layers) * 0.85
        cols = [CRIMSON, HEATED, FLAME, PULSE_COL, BURGUNDY,
                DARKROSE, GILT, WINE, SMOLDER, EMBER, SCARLET,
                CRIMSON, HEATED, FLAME]
        col_a = cols[i]; col_b = cols[(i + 5) % len(cols)]
        for xs_c, ys_c, col in [(xs_a, ys_a, col_a), (xs_b, ys_b, col_b)]:
            mask = ((xs_c > PAD_L) & (xs_c < PAD_L + PW) &
                    (ys_c > PAD_B) & (ys_c < PAD_B + PH))
            if mask.sum() < 3: continue
            for seg_xs, seg_ys in split_segments(xs_c, ys_c, mask):
                pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
                segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
                n_s = len(segs)
                alphas = np.linspace(0.05, 0.65, n_s)
                lws = np.linspace(0.2, 2.2, n_s)
                colors = [rgba(col, float(a)) for a in alphas]
                lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                       capstyle='round', zorder=3 + i)
                ax.add_collection(lc)
    glow(ax, cx, cy, FLAME, 0.30)
    label(ax, "r(\u03b8)=r\u2080\u00b7e^(\u2212\u03b3\u03b8)")
    save(fig, "desire_inspiral")


if __name__ == '__main__':
    render()
