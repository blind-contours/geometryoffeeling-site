"""
Geometry of Feeling — Fractured: Fractured Catastrophe Fold
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
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"  saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def render():
    fig, ax = make_fig()

    # We draw slices of the equilibrium surface x^3 + a*x + b = 0
    # For each value of a, solve for x as a function of b
    # At a < 0 the cubic has a fold (two turning points) -> discontinuous jump

    n_slices = 40
    a_vals = np.linspace(-2.5, 1.5, n_slices)

    colors_cycle = [COBALT, TEAL, FOREST, NAVY, SIENNA, OCHRE, CRIMSON, RUST]

    # Parameter mapping to canvas
    b_range = (-4.0, 4.0)
    x_range = (-3.0, 3.0)

    def b_to_canvas(b):
        return PAD_L + PW * (b - b_range[0]) / (b_range[1] - b_range[0])

    def x_to_canvas(x):
        return PAD_B + PH * (x - x_range[0]) / (x_range[1] - x_range[0])

    for si, a in enumerate(a_vals):
        # For this a, generate the equilibrium curve x^3 + a*x + b = 0
        # Rearrange: b = -(x^3 + a*x)
        # Parametrize by x, compute b
        x_param = np.linspace(x_range[0], x_range[1], 1200)
        b_param = -(x_param**3 + a * x_param)

        # Canvas coordinates
        cx_pts = b_to_canvas(b_param)
        cy_pts = x_to_canvas(x_param)

        # Only draw points within b_range and canvas
        mask = ((cx_pts > PAD_L) & (cx_pts < PAD_L + PW) &
                (cy_pts > PAD_B) & (cy_pts < PAD_B + PH) &
                (b_param > b_range[0]) & (b_param < b_range[1]))

        if mask.sum() < 3:
            continue

        # Color: transition from cool (positive a, no fold) to warm (negative a, folded)
        a_frac = (a - a_vals[0]) / (a_vals[-1] - a_vals[0])
        if a_frac < 0.25:
            col = CRIMSON     # deeply folded
        elif a_frac < 0.40:
            col = RUST
        elif a_frac < 0.55:
            col = OCHRE
        elif a_frac < 0.65:
            col = SIENNA
        elif a_frac < 0.75:
            col = FOREST
        elif a_frac < 0.85:
            col = TEAL
        else:
            col = COBALT      # unfolded / smooth

        # Alpha: make folded curves (low a) more prominent
        alpha = 0.15 + 0.40 * (1.0 - a_frac)
        lw = 0.5 + 1.0 * (1.0 - a_frac)

        # For folded curves, the curve doubles back in b
        # We want to show the fold explicitly
        # Split into segments and draw
        for seg_xs, seg_ys in split_segments(cx_pts, cy_pts, mask):
            draw_lc(ax, seg_xs, seg_ys, col, lw=lw,
                    alpha=alpha, zo=3 + si)

    # Draw the bifurcation set (cusp): 4a^3 + 27b^2 = 0
    # Parametrize: a = -3t^2, b = 2t^3
    t_cusp = np.linspace(-1.6, 1.6, 600)
    a_cusp = -3 * t_cusp**2
    b_cusp = 2 * t_cusp**3

    # For the cusp curve in the (b, a) plane, we need to show it on our canvas
    # We map b to horizontal, but we need to show the cusp on the same axes
    # Actually, our canvas shows (b, x*). The cusp boundary is where the fold
    # happens. Let's draw it as the envelope of the fold points.
    # At a fold point: dV/dx^2 = 0 -> 3x^2 + a = 0 -> x = +/- sqrt(-a/3)
    # Substituting back: b = -(x^3 + ax) = -(+/-(-a/3)^{3/2} +/- a*sqrt(-a/3))
    # For a < 0: x_fold = sqrt(-a/3), b_fold = 2(-a/3)^{3/2}
    a_env = np.linspace(-2.5, -0.01, 400)
    for sign in [1, -1]:
        x_fold = sign * np.sqrt(-a_env / 3.0)
        b_fold = -(x_fold**3 + a_env * x_fold)
        cx_fold = b_to_canvas(b_fold)
        cy_fold = x_to_canvas(x_fold)

        mask_fold = ((cx_fold > PAD_L) & (cx_fold < PAD_L + PW) &
                     (cy_fold > PAD_B) & (cy_fold < PAD_B + PH))
        if mask_fold.sum() < 3:
            continue

        for seg_xs, seg_ys in split_segments(cx_fold, cy_fold, mask_fold):
            # Draw as dashed emphasis
            pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            n_s = len(segs)
            # Varying alpha along the fold line
            alphas = np.linspace(0.50, 0.15, n_s)
            lws = np.linspace(2.0, 0.8, n_s)
            colors = [rgba(CRIMSON, float(a_)) for a_ in alphas]
            lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                   capstyle='round', zorder=n_slices + 5)
            ax.add_collection(lc)

    # Draw arrows indicating the discontinuous jump
    # At a = -2.0 for example, there is a hysteresis loop
    # Upper and lower stable branches jump at fold points
    a_demo = -2.0
    x_fold_val = np.sqrt(-a_demo / 3.0)
    b_fold_upper = -(x_fold_val**3 + a_demo * x_fold_val)
    b_fold_lower = -(-x_fold_val**3 + a_demo * (-x_fold_val))

    # Draw vertical jump arrows at fold points
    for b_jump, x_from, x_to in [(b_fold_upper, x_fold_val, -2.0),
                                   (b_fold_lower, -x_fold_val, 1.5)]:
        arrow_cx = b_to_canvas(b_jump)
        arrow_y1 = x_to_canvas(x_from)
        arrow_y2 = x_to_canvas(x_to)
        # Draw as dashed vertical line
        n_dash = 20
        for di in range(n_dash):
            frac_lo = di / n_dash
            frac_hi = (di + 0.45) / n_dash
            y_lo = arrow_y1 + (arrow_y2 - arrow_y1) * frac_lo
            y_hi = arrow_y1 + (arrow_y2 - arrow_y1) * frac_hi
            if PAD_B < y_lo < PAD_B + PH and PAD_B < y_hi < PAD_B + PH:
                draw_lc(ax,
                        np.array([arrow_cx, arrow_cx]),
                        np.array([y_lo, y_hi]),
                        CRIMSON, lw=1.0, alpha=0.35, zo=n_slices + 3)

    # Arrowheads (small triangles)
    arrow_size = 0.10
    for b_jump, x_from, x_to in [(b_fold_upper, x_fold_val, -2.0),
                                   (b_fold_lower, -x_fold_val, 1.5)]:
        acx = b_to_canvas(b_jump)
        acy = x_to_canvas(x_to)
        direction = 1 if x_to > x_from else -1
        tri_y = [acy, acy - direction * arrow_size,
                 acy - direction * arrow_size]
        tri_x = [acx, acx - arrow_size * 0.5, acx + arrow_size * 0.5]
        ax.fill(tri_x, tri_y, color=rgba(CRIMSON, 0.40), zorder=n_slices + 6)

    add_signature(fig, ax, BG)
    save(fig, "fractured_catastrophe_fold.pdf")

# ── run ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    render()
