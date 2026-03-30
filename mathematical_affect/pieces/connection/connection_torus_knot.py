"""
Geometry of Feeling — Connection: Connection Torus Knot
Standalone render script
"""

"""
Geometry of Feeling — Connection v3 (revised based on feedback)
Key changes:
- Rose gold + gold as the two-curve palette
- "Orbiting but not merging" as core direction
- Regenerate: Lorenz→orbit-pair, Magnetic→field-focused, Murmuration→coherent
- Enhance: Entanglement, Double Helix, Pendulum with rose gold
- Keep favorites: Coupled, Lissajous, Torus Knot, Rossler, Phase Sync, Weave
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
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#0A0A12"
MARGIN_COLOR = "#E8D8B8"

# ROSE GOLD + GOLD palette (user request)
ROSE_GOLD = "#C8887A"
WARM_ROSE = "#D4988A"
SOFT_ROSE = "#B87A70"
GOLD = "#E8C878"
AMBER = "#D4A856"
PALE_GOLD = "#F0D890"
WARM_WHITE = "#F0E8D8"
COPPER = "#C49A3C"
BRONZE = "#B08830"

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def make_fig():
    from matplotlib.patches import FancyBboxPatch, Rectangle
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(MARGIN_COLOR)
    ax.set_facecolor(MARGIN_COLOR)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    # Gold cream margin background
    ax.add_patch(Rectangle((0, 0), FIG_W, FIG_H, facecolor=MARGIN_COLOR,
                            edgecolor='none', zorder=-10))
    # Black content rectangle inside margins
    ml = FIG_W * 0.07; mr = FIG_W * 0.07
    mb = FIG_H * 0.08; mt = FIG_H * 0.08
    ax.add_patch(FancyBboxPatch((ml, mb), FIG_W - ml - mr, FIG_H - mb - mt,
                                 boxstyle="square,pad=0",
                                 facecolor=BG, edgecolor='none', zorder=0))
    # Margin masks — paint over any content that bleeds outside the content area
    zo = 1000
    ax.add_patch(Rectangle((0, 0), FIG_W, mb, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, FIG_H - mt), FIG_W, mt, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, 0), ml, FIG_H, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((FIG_W - mr, 0), mr, FIG_H, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
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
    if len(xs) < 2: return
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def draw_lc_gradient(ax, xs, ys, col, lw_s, lw_e, a_s, a_e, zo=4, smooth=0):
    if len(xs) < 2: return
    if smooth > 0:
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

def head(ax, x, y):
    ax.plot(x, y, 'o', color=rgba(WARM_WHITE, 0.10), markersize=18, markeredgewidth=0, zorder=8)
    ax.plot(x, y, 'o', color=rgba(WARM_WHITE, 0.25), markersize=9, markeredgewidth=0, zorder=9)
    ax.plot(x, y, 'o', color=rgba(WARM_WHITE, 0.55), markersize=4, markeredgewidth=0, zorder=10)

def save(fig, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Ensure name ends with .pdf
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=MARGIN_COLOR)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

# ============================================================================
# 4. TORUS KNOT — rose gold + gold (keep, enhanced)
# ============================================================================
def render():
    fig, ax = make_fig()
    t = np.linspace(0, 2*np.pi, 4000)
    p, q = 3, 5
    R, r_t = PW*0.27, PW*0.12
    for i, (phase, col) in enumerate([(0, ROSE_GOLD), (np.pi/p, GOLD)]):
        r_curve = R + r_t*np.cos(q*(t+phase))
        xs_k = cx + r_curve*np.cos(p*(t+phase))
        ys_k = cy + r_curve*np.sin(p*(t+phase))*(PH/PW)
        z = r_t*np.sin(q*(t+phase))
        z_norm = (z-z.min())/(z.max()-z.min())
        pts = np.array([xs_k, ys_k]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        n = len(segs)
        alphas = 0.12 + 0.42*z_norm[:n]
        lws = 0.4 + 1.4*z_norm[:n]
        colors = [rgba(col, float(a)) for a in alphas]
        lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                               capstyle='round', joinstyle='round', zorder=4+i)
        ax.add_collection(lc)
    add_signature(fig, ax, MARGIN_COLOR, margin_piece=True, margin_bottom=FIG_H * 0.08)
    save(fig, "connection_torus_knot.pdf")

if __name__ == '__main__':
    render()
