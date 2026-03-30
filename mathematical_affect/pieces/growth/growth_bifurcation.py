"""
Geometry of Feeling — Growth: Growth Bifurcation
Standalone render script
"""

"""
Geometry of Feeling — Growth Series v2 (Final)
Five pieces: Logistic Cascade, Bifurcation, Reaction-Diffusion, Dendrite, Lissajous Bloom

Mathematical primitives: logistic S-curves, period-doubling map,
expanding wavefronts, crystalline branching, harmonic parametric curves

Dependencies: matplotlib, numpy
    pip install matplotlib numpy
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

DPI=300; FIG_W=12; FIG_H=8
BG="#F5F0E6"

# Palette
MOSS="#4A7A3A"; LEAF="#6A9A4A"; GOLD="#C8920A"; AMBER="#D4A832"
CORAL="#C8603A"; SAGE="#7A9A6A"; SPRING="#8AB84A"; DARK_G="#2A4A1A"; TEAL="#3A8A6A"

def hex_to_rgb(h):
    h=h.lstrip('#')
    return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))

def rgba(h,a):
    c=hex_to_rgb(h)
    return (c[0],c[1],c[2],float(np.clip(a,0,1)))

def make_fig():
    fig=plt.figure(figsize=(FIG_W,FIG_H),dpi=DPI)
    ax=fig.add_subplot(111)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0,FIG_W); ax.set_ylim(0,FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    return fig,ax

PAD_L=0.72; PAD_R=0.60; PAD_T=0.65; PAD_B=0.88
PW=FIG_W-PAD_L-PAD_R; PH=FIG_H-PAD_T-PAD_B
cx=PAD_L+PW/2; cy=PAD_B+PH/2

def split_segments(xs, ys):
    """Convert x,y arrays into line segments for LineCollection."""
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    return segs

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4):
    segs = split_segments(xs, ys)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

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
# 2. BIFURCATION — period-doubling route from order to chaos
#    x_{n+1} = r * x_n * (1 - x_n)
#    The logistic map: as growth rate increases, stability shatters.
# =============================================================================
def render():
    fig, ax = make_fig()

    # Map the bifurcation diagram onto the canvas
    # r ranges from ~2.5 (stable) to 4.0 (chaos)
    r_min, r_max = 2.5, 4.0
    n_r = 2000  # number of r values to sample
    n_transient = 300  # iterations to discard
    n_plot = 120  # iterations to plot per r

    r_vals = np.linspace(r_min, r_max, n_r)

    # Build the bifurcation data
    all_segs = []
    all_colors = []
    all_lws = []

    for ri, r in enumerate(r_vals):
        x = 0.5 + 0.1 * np.sin(ri * 0.01)  # slight variation in IC
        # Discard transient
        for _ in range(n_transient):
            x = r * x * (1 - x)

        # Collect attractor points
        points_y = []
        for _ in range(n_plot):
            x = r * x * (1 - x)
            points_y.append(x)

        # Map to canvas coordinates
        px = PAD_L + PW * (r - r_min) / (r_max - r_min)

        for py_frac in points_y:
            py = PAD_B + PH * 0.04 + PH * 0.90 * py_frac

            # Color based on r value (order -> chaos)
            frac = (r - r_min) / (r_max - r_min)
            if frac < 0.25:
                col = DARK_G
            elif frac < 0.45:
                col = MOSS
            elif frac < 0.60:
                col = LEAF
            elif frac < 0.75:
                col = GOLD
            elif frac < 0.88:
                col = AMBER
            else:
                col = CORAL

            # Draw as small horizontal dashes to create the classic diagram
            dash_w = PW / n_r * 0.8
            seg_xs = np.array([px - dash_w / 2, px + dash_w / 2])
            seg_ys = np.array([py, py])

            pts = np.array([[seg_xs[0], seg_ys[0]], [seg_xs[1], seg_ys[1]]]).reshape(1, 2, 2)
            all_segs.append(pts[0])

            # More transparent in chaotic region to avoid solid mass
            if frac > 0.7:
                alpha = 0.06 + 0.14 * (1 - frac)
            else:
                alpha = 0.25 + 0.45 * (1 - frac)
            all_colors.append(rgba(col, alpha))
            all_lws.append(0.15 + 0.6 * (1 - frac * 0.5))

    # Draw all segments at once for efficiency
    lc = mc.LineCollection(all_segs, linewidths=all_lws, colors=all_colors,
                           capstyle='round', zorder=3)
    ax.add_collection(lc)

    # Add vertical lines at key bifurcation points
    # First bifurcation: r = 3.0, second: r ~ 3.449, onset of chaos: r ~ 3.5699
    bif_points = [3.0, 3.449, 3.5441, 3.5699]
    for bp in bif_points:
        bx = PAD_L + PW * (bp - r_min) / (r_max - r_min)
        ax.plot([bx, bx], [PAD_B + PH * 0.02, PAD_B + PH * 0.96],
                color=rgba(TEAL, 0.06), linewidth=0.4, zorder=2)

    # Overlay a few continuous orbit curves to add flow
    # Trace a single orbit path as r increases slowly
    for seed_offset in [0.1, 0.3, 0.5, 0.7, 0.9]:
        trace_xs = []
        trace_ys = []
        x = seed_offset
        n_trace = 4000
        for ti in range(n_trace):
            r = r_min + (r_max - r_min) * ti / n_trace
            x = r * x * (1 - x)
            if ti > n_transient:
                px = PAD_L + PW * (r - r_min) / (r_max - r_min)
                py = PAD_B + PH * 0.04 + PH * 0.90 * x
                trace_xs.append(px)
                trace_ys.append(py)

        if len(trace_xs) > 10:
            trace_xs = np.array(trace_xs)
            trace_ys = np.array(trace_ys)
            draw_lc(ax, trace_xs, trace_ys, SAGE, lw=0.25, alpha=0.08, zo=2)

    add_signature(fig, ax, BG)
    save(fig, "growth_bifurcation.pdf")

if __name__ == '__main__':
    render()
