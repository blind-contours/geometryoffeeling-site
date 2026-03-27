"""
Geometry of Feeling — Connection: Connection Entanglement
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
# 5. ENTANGLEMENT — enhanced with more visual "spice"
# ============================================================================
def render():
    fig, ax = make_fig()
    np.random.seed(66)
    t = np.linspace(0, 1, 3000)

    n_modes = 12  # more modes for richer signal
    signal = np.zeros_like(t)
    for k in range(n_modes):
        freq = 2 + k*2.5
        phase = np.random.uniform(0, 2*np.pi)
        amp = 1.0/(k+1)**0.7
        signal += amp*np.sin(freq*np.pi*t + phase)
    signal = signal/np.max(np.abs(signal))

    # Left particle
    xs1 = PAD_L + PW*0.05 + PW*0.38*t
    ys1 = cy + PH*0.35*signal
    # Right particle — mirrored and slightly stretched
    xs2 = PAD_L + PW*0.57 + PW*0.38*t
    ys2 = cy - PH*0.35*signal

    draw_lc_gradient(ax, xs1, ys1, ROSE_GOLD, 0.8, 2.0, 0.28, 0.58, zo=4, smooth=1)
    draw_lc_gradient(ax, xs2, ys2, GOLD, 0.8, 2.0, 0.28, 0.58, zo=5, smooth=1)

    # Dots at the start of each line
    head(ax, xs1[0], ys1[0])
    head(ax, xs2[0], ys2[0])

    # Richer connecting lines — curved arcs instead of straight lines
    n_links = 35
    link_idx = np.linspace(100, len(t)-100, n_links, dtype=int)
    for idx in link_idx:
        # Curved arc between the two
        arc_t = np.linspace(0, 1, 50)
        arc_x = xs1[idx] + (xs2[idx]-xs1[idx])*arc_t
        # Arc bows outward based on signal value
        bow = PH*0.08*signal[idx]*np.sin(np.pi*arc_t)
        arc_y = ys1[idx] + (ys2[idx]-ys1[idx])*arc_t + bow
        alpha = 0.12 + 0.18*np.abs(signal[idx])
        draw_lc(ax, arc_x, arc_y, PALE_GOLD, lw=0.6, alpha=alpha, zo=2)

    # Glowing dots at key correlation peaks
    peaks = np.where(np.abs(np.diff(signal)) < 0.001)[0][:8]
    for p in peaks:
        if p < len(xs1) and p < len(xs2):
            for xx, yy in [(xs1[p], ys1[p]), (xs2[p], ys2[p])]:
                ax.plot(xx, yy, 'o', color=rgba(WARM_WHITE, 0.15),
                        markersize=6, markeredgewidth=0, zorder=7)

    label(ax, "|\u03c8\u27e9 = (|01\u27e9 - |10\u27e9)/\u221a2")
    save(fig, "connection_entanglement.pdf")


if __name__ == '__main__':
    render()
