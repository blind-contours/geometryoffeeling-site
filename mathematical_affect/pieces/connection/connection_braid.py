"""
Geometry of Feeling — Connection: Connection Braid
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
    return fig, ax

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW/2; cy = PAD_B + PH/2

def label(ax, eq, note=None):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.85,0.80,0.75,0.55),transform=ax.transData)
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
# 13. BRAID — over/under weaving
# ============================================================================
def render():
    fig, ax = make_fig()
    t = np.linspace(0, 1, 3000); xs = PAD_L + PW*t
    freq = 4; amp = PH*0.25
    ys1 = cy + amp*np.sin(2*np.pi*freq*t)
    ys2 = cy + amp*np.sin(2*np.pi*freq*t + np.pi)
    cross_phase = np.sin(2*np.pi*freq*t)
    is_1_front = cross_phase > 0
    for xs_c, ys_c, col, front_mask in [
        (xs, ys1, ROSE_GOLD, is_1_front),
        (xs, ys2, GOLD, ~is_1_front)
    ]:
        pts = np.array([xs_c, ys_c]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        n = len(segs)
        alphas = np.where(front_mask[:n], 0.55, 0.15)
        lws = np.where(front_mask[:n], 1.8, 0.8)
        colors = [rgba(col, float(a)) for a in alphas]
        lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                               capstyle='round', joinstyle='round', zorder=4)
        ax.add_collection(lc)
    label(ax, "y\u2081=sin(\u03c9t), y\u2082=sin(\u03c9t+\u03c0)")
    save(fig, "connection_braid.pdf")


if __name__ == '__main__':
    render()
