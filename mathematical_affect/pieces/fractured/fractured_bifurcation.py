"""
Geometry of Feeling — Fractured: Fractured Bifurcation
Standalone render script
"""

"""
Geometry of Feeling -- Fractured: Final Five
Voronoi Shatter, Bifurcation Cascade, Seismic Fault, Glass Fracture, Catastrophe Fold

Five distinct mathematical approaches to fracture:
  1. Voronoi Shatter   - displaced Voronoi cells radiating from impact
  2. Bifurcation        - logistic map period-doubling cascade into chaos
  3. Seismic Fault      - parallel strata violently offset along fault planes
  4. Glass Fracture     - radial + concentric Hertzian cone crack from impact
  5. Catastrophe Fold   - cusp catastrophe with discontinuous jumps

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
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

# ── config ────────────────────────────────────────────────────────────────────

DPI   = 300
FIG_W = 12
FIG_H = 8

BG = "#F0EBE2"   # warm paper -- fractures are the subject

# Palette
COBALT  = "#2255A4"
FOREST  = "#1A6B3A"
CRIMSON = "#C8392B"
OCHRE   = "#B87A2A"
NAVY    = "#1C3755"
TEAL    = "#1A5C8A"
SIENNA  = "#A85A2A"
RUST    = "#C84A20"

PAD_L = 0.78; PAD_R = 0.65; PAD_T = 0.72; PAD_B = 1.05
PW = FIG_W - PAD_L - PAD_R
PH = FIG_H - PAD_T  - PAD_B
cx = PAD_L + PW / 2
cy = PAD_B + PH / 2

# ── helpers ───────────────────────────────────────────────────────────────────

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax  = fig.add_subplot(111)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax

def split_segments(xs, ys, mask):
    """Split arrays into contiguous segments where mask is True."""
    segments = []
    in_seg = False
    start = 0
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

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4):
    """Draw a curve as a LineCollection."""
    if len(xs) < 2:
        return
    pts  = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc   = mc.LineCollection(segs, linewidths=lw,
                             colors=[rgba(col, alpha)],
                             capstyle='round', joinstyle='round',
                             zorder=zo)
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
# 2. BIFURCATION CASCADE
#    The logistic map x_{n+1} = r * x_n * (1 - x_n) iterated across
#    increasing r, showing period-doubling route to chaos.
#    Order literally fractures into disorder.
#
#    Horizontal axis: r from 2.5 to 4.0
#    Vertical axis: attractor values x*
# =============================================================================
def render():
    fig, ax = make_fig()
    np.random.seed(42)

    r_min, r_max = 2.5, 4.0
    n_r = 2000      # resolution along r-axis
    n_iter = 300     # iterations to settle
    n_last = 120     # attractor points to plot per r

    r_vals = np.linspace(r_min, r_max, n_r)

    # Colors transition: stable region is cool, chaotic region is warm
    # The fracture boundary is around r ~ 3.57 (onset of chaos)

    # Build all attractor points
    all_points_r = []
    all_points_x = []
    for ri, r in enumerate(r_vals):
        x = 0.1 + 0.8 * np.random.random()
        # Iterate to settle
        for _ in range(n_iter):
            x = r * x * (1.0 - x)
        # Collect attractor
        for _ in range(n_last):
            x = r * x * (1.0 - x)
            all_points_r.append(r)
            all_points_x.append(x)

    all_points_r = np.array(all_points_r)
    all_points_x = np.array(all_points_x)

    # Map to canvas coordinates
    canvas_x = PAD_L + PW * (all_points_r - r_min) / (r_max - r_min)
    canvas_y = PAD_B + PH * all_points_x

    # Draw as tiny dots using scatter with varying color
    # Color based on r value: blue in stable, transitioning to red in chaos
    r_frac = (all_points_r - r_min) / (r_max - r_min)

    # Render in vertical strips using LineCollection for consistency
    # Group by r-value bins and draw vertical scatter strips
    # Batch all segments by color group for performance
    n_bins = 800
    r_edges = np.linspace(r_min, r_max, n_bins + 1)

    # Determine color for each point based on r-fraction
    rf_all = (all_points_r - r_min) / (r_max - r_min)

    color_groups = [
        (0.00, 0.35, COBALT),   # stable period-1
        (0.35, 0.50, TEAL),     # period-2
        (0.50, 0.65, FOREST),   # period-4 and beyond
        (0.65, 0.78, OCHRE),    # edge of chaos
        (0.78, 0.88, RUST),     # chaos
        (0.88, 1.01, CRIMSON),  # deep chaos
    ]

    dash_half = PW / n_bins * 0.3

    for rf_lo, rf_hi, col in color_groups:
        gmask = (rf_all >= rf_lo) & (rf_all < rf_hi)
        if gmask.sum() < 2:
            continue

        gx = canvas_x[gmask]
        gy = canvas_y[gmask]
        grf = rf_all[gmask]

        # Build all dash segments at once
        left_x = gx - dash_half
        right_x = gx + dash_half
        segs = np.zeros((len(gx), 2, 2))
        segs[:, 0, 0] = left_x
        segs[:, 0, 1] = gy
        segs[:, 1, 0] = right_x
        segs[:, 1, 1] = gy

        avg_rf = (rf_lo + rf_hi) / 2.0
        alpha = 0.12 + 0.25 * avg_rf
        lw = 0.3 + 0.4 * avg_rf

        lc = mc.LineCollection(segs, linewidths=lw,
                               colors=[rgba(col, alpha)],
                               capstyle='round', joinstyle='round',
                               zorder=3)
        ax.add_collection(lc)

    # Mark the key bifurcation points with faint vertical lines
    bif_r_vals = [3.0, 3.449, 3.544, 3.5644, 3.5688]  # period doublings
    for br in bif_r_vals:
        bx_line = PAD_L + PW * (br - r_min) / (r_max - r_min)
        ys_line = np.array([PAD_B, PAD_B + PH])
        xs_line = np.array([bx_line, bx_line])
        draw_lc(ax, xs_line, ys_line, NAVY, lw=0.5, alpha=0.10, zo=2)

    # Onset-of-chaos line at r ~ 3.5699 (Feigenbaum point)
    feig_x = PAD_L + PW * (3.5699 - r_min) / (r_max - r_min)
    ax.plot([feig_x, feig_x], [PAD_B, PAD_B + PH],
            color=rgba(CRIMSON, 0.18), linewidth=1.0,
            linestyle='--', zorder=2)

    # Axis hints: faint r-labels
    for r_tick in [2.5, 3.0, 3.5, 4.0]:
        tx = PAD_L + PW * (r_tick - r_min) / (r_max - r_min)

    add_signature(fig, ax, BG)
    save(fig, "fractured_bifurcation.pdf")

if __name__ == '__main__':
    render()
