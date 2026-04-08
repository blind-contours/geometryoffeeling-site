"""
Geometry of Feeling — Connection: Lorenz
Standalone render script
Two trajectories on the same strange attractor, diverging from nearly identical starts.
"""

import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#0A0A12"
MARGIN_COLOR = "#E8D8B8"

AMBER = "#D4A856"
GOLD = "#E8C878"
WARM_WHITE = "#F0E8D8"

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
    ax.add_patch(Rectangle((0, 0), FIG_W, FIG_H, facecolor=MARGIN_COLOR,
                            edgecolor='none', zorder=-10))
    ml = FIG_W * 0.07; mr = FIG_W * 0.07
    mb = FIG_H * 0.08; mt = FIG_H * 0.08
    ax.add_patch(FancyBboxPatch((ml, mb), FIG_W - ml - mr, FIG_H - mb - mt,
                                 boxstyle="square,pad=0",
                                 facecolor=BG, edgecolor='none', zorder=0))
    zo = 1000
    ax.add_patch(Rectangle((0, 0), FIG_W, mb, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, FIG_H - mt), FIG_W, mt, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, 0), ml, FIG_H, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((FIG_W - mr, 0), mr, FIG_H, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    return fig, ax

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B

def draw_lc_gradient(ax, xs, ys, col, lw_s, lw_e, a_s, a_e, zo=4):
    if len(xs) < 2: return
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    n = len(segs)
    alphas = np.linspace(a_s, a_e, n)
    lws = np.linspace(lw_s, lw_e, n)
    colors = [rgba(col, float(a)) for a in alphas]
    # butt capstyle prevents beading artifacts where adjacent segments
    # are shorter than the line's width (happens in slow trajectory regions)
    lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                           capstyle='butt', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def head(ax, x, y):
    ax.plot(x, y, 'o', color=rgba(WARM_WHITE, 0.10), markersize=18, markeredgewidth=0, zorder=8)
    ax.plot(x, y, 'o', color=rgba(WARM_WHITE, 0.25), markersize=9, markeredgewidth=0, zorder=9)
    ax.plot(x, y, 'o', color=rgba(WARM_WHITE, 0.55), markersize=4, markeredgewidth=0, zorder=10)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
PRINT_DIR = os.path.join(SCRIPT_DIR, '..', '..', '..', 'public', 'prints', 'connection')


def render(alpha_boost=1.0, lw_boost=1.0):
    fig, ax = make_fig()

    sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
    # Densify integration so line segments are short relative to linewidth
    # — this removes the beaded/dotted look in the slow-moving regions.
    dt = 0.003
    n_steps = 16000

    def lorenz_trajectory(x0, y0, z0):
        xs, ys, zs = [x0], [y0], [z0]
        x, y, z = x0, y0, z0
        for _ in range(n_steps):
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            x += dx * dt; y += dy * dt; z += dz * dt
            xs.append(x); ys.append(y); zs.append(z)
        return np.array(xs), np.array(ys), np.array(zs)

    lx1, ly1, lz1 = lorenz_trajectory(1.0, 1.0, 1.0)
    lx2, ly2, lz2 = lorenz_trajectory(1.001, 1.0, 1.0)

    def normalize(arr, lo, hi):
        mn, mx = arr.min(), arr.max()
        return lo + (hi - lo) * (arr - mn) / (mx - mn + 1e-10)

    px1 = normalize(lx1, PAD_L + PW * 0.05, PAD_L + PW * 0.95)
    py1 = normalize(lz1, PAD_B + PH * 0.05, PAD_B + PH * 0.95)
    px2 = normalize(lx2, PAD_L + PW * 0.05, PAD_L + PW * 0.95)
    py2 = normalize(lz2, PAD_B + PH * 0.05, PAD_B + PH * 0.95)

    draw_lc_gradient(ax, px1, py1, AMBER,
                     0.3 * lw_boost, 1.4 * lw_boost,
                     min(0.08 * alpha_boost, 0.95),
                     min(0.45 * alpha_boost, 0.95),
                     zo=4)
    draw_lc_gradient(ax, px2, py2, GOLD,
                     0.3 * lw_boost, 1.4 * lw_boost,
                     min(0.08 * alpha_boost, 0.95),
                     min(0.45 * alpha_boost, 0.95),
                     zo=5)

    head(ax, px1[-1], py1[-1])
    head(ax, px2[-1], py2[-1])

    add_signature(fig, ax, MARGIN_COLOR, margin_piece=True, margin_bottom=FIG_H * 0.08)
    return fig


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PRINT_DIR, exist_ok=True)
    print("═══ Connection: Lorenz ═══")

    # Print PDF — modest boost matches the thumbnail
    fig = render(alpha_boost=1.35, lw_boost=1.35)
    pdf_path = os.path.join(OUTPUT_DIR, "connection_lorenz.pdf")
    fig.savefig(pdf_path, format='pdf', facecolor=MARGIN_COLOR)
    print(f"  saved {pdf_path}")
    plt.close(fig)

    # Web thumbnail — same boost, full DPI
    fig = render(alpha_boost=1.35, lw_boost=1.35)
    jpg_path = os.path.join(PRINT_DIR, "connection_lorenz.jpg")
    fig.savefig(jpg_path, facecolor=MARGIN_COLOR, dpi=DPI,
                pil_kwargs={"quality": 96})
    print(f"  saved {jpg_path}")
    plt.close(fig)

    print("═══ Done ═══")
