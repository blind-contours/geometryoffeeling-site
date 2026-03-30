"""
Geometry of Feeling — Fractured: Fractured Seismic Fault
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
                             capstyle='butt', joinstyle='miter',
                             antialiaseds=False,
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
# 3. SEISMIC FAULT
#    Parallel geological strata (smooth curves) displaced along diagonal
#    fault planes. Each stratum is a continuous function that suffers
#    strike-slip displacement at each fault crossing.
#
#    Model: y_i(x) = base_i + A_i sin(k_i x + phi_i), displaced at faults
#    Displacement: delta_y = D * sign(fault_angle) at each fault intersection
# =============================================================================
def render():
    fig, ax = make_fig()
    np.random.seed(31)

    n_strata = 18
    n_faults = 5

    # Fault positions (x-coordinates) and their displacement magnitudes
    fault_xs = np.sort(PAD_L + PW * np.array([0.18, 0.35, 0.52, 0.72, 0.88]))
    fault_disps = np.array([0.28, -0.42, 0.35, -0.55, 0.22]) * PH * 0.12

    # Strata: smooth curves spanning the canvas
    strata_base = np.linspace(PAD_B + PH * 0.06, PAD_B + PH * 0.94, n_strata)
    strata_colors = [COBALT, TEAL, FOREST, NAVY, SIENNA, OCHRE,
                     COBALT, TEAL, FOREST, NAVY, SIENNA, OCHRE,
                     COBALT, TEAL, FOREST, NAVY, SIENNA, OCHRE]

    t = np.linspace(0, 1, 2000)
    xs_full = PAD_L + PW * t

    for si in range(n_strata):
        # Each stratum has its own gentle undulation
        freq = 1.5 + 0.5 * np.sin(si * 0.7)
        amp = PH * 0.012 * (1.0 + 0.5 * np.sin(si * 1.3))
        phase = si * 0.9
        ys_base = strata_base[si] + amp * np.sin(2 * np.pi * freq * t + phase)

        # Add cumulative fault displacement
        cumulative_disp = np.zeros_like(t)
        for fi in range(n_faults):
            # Sharp offset at fault crossing
            past_fault = xs_full > fault_xs[fi]
            cumulative_disp[past_fault] += fault_disps[fi]

        ys_displaced = ys_base + cumulative_disp

        # Split at each fault to create gaps
        col = strata_colors[si % len(strata_colors)]
        alpha_base = 0.65 + 0.25 * (si / n_strata)
        lw_base = 1.1 + 0.85 * (1.0 - si / n_strata)

        # Create segments between faults
        boundaries = np.concatenate([[PAD_L], fault_xs, [PAD_L + PW]])
        for bi in range(len(boundaries) - 1):
            x_lo = boundaries[bi]
            x_hi = boundaries[bi + 1]

            # Small gap at fault boundary
            gap = PW * 0.004
            seg_mask = (xs_full > x_lo + gap) & (xs_full < x_hi - gap)
            if seg_mask.sum() < 3:
                continue

            seg_xs = xs_full[seg_mask]
            seg_ys = ys_displaced[seg_mask]

            # Clip to canvas
            in_bounds = ((seg_ys > PAD_B) & (seg_ys < PAD_B + PH))
            if in_bounds.sum() < 3:
                continue

            for s_xs, s_ys in split_segments(seg_xs, seg_ys, in_bounds):
                draw_lc(ax, s_xs, s_ys, col, lw=lw_base,
                        alpha=alpha_base, zo=3)

        # Draw dots at fault-crossing endpoints
        for fi in range(n_faults):
            fx = fault_xs[fi]
            # Find y-value just before and just after fault
            idx_before = np.searchsorted(xs_full, fx) - 1
            idx_after = idx_before + 1
            if 0 <= idx_before < len(ys_displaced) and idx_after < len(ys_displaced):
                y_before = ys_displaced[idx_before]
                y_after = ys_displaced[idx_after]
                for yp in [y_before, y_after]:
                    if PAD_B < yp < PAD_B + PH:
                        ax.plot(fx, yp, 'o', color=rgba(col, alpha_base * 0.8),
                                markersize=2.5, markeredgewidth=0, zorder=5)

    # Draw fault lines themselves: diagonal lines
    fault_angles = [72, 78, 68, 75, 82]  # degrees from horizontal
    for fi in range(n_faults):
        fx = fault_xs[fi]
        angle_rad = np.radians(fault_angles[fi])
        fault_len = PH * 1.2
        fy_lo = PAD_B - 0.2
        fy_hi = PAD_B + PH + 0.2

        # Slight diagonal
        dx = fault_len * np.cos(angle_rad) * 0.15
        xs_f = np.array([fx - dx, fx + dx])
        ys_f = np.array([fy_lo, fy_hi])

        # Clip
        mask_f = ((xs_f > PAD_L) & (xs_f < PAD_L + PW) &
                  (ys_f > PAD_B) & (ys_f < PAD_B + PH))
        # Just draw the full line
        draw_lc(ax, xs_f, ys_f, CRIMSON, lw=1.7, alpha=0.50, zo=5)

        # Dashed extension
        n_dashes = 30
        for di in range(n_dashes):
            frac_lo = di / n_dashes
            frac_hi = (di + 0.4) / n_dashes
            dash_xs = np.array([fx - dx + 2 * dx * frac_lo,
                                fx - dx + 2 * dx * frac_hi])
            dash_ys = np.array([fy_lo + (fy_hi - fy_lo) * frac_lo,
                                fy_lo + (fy_hi - fy_lo) * frac_hi])
            clip = ((dash_xs > PAD_L) & (dash_xs < PAD_L + PW) &
                    (dash_ys > PAD_B) & (dash_ys < PAD_B + PH))
            if clip.all():
                draw_lc(ax, dash_xs, dash_ys, CRIMSON,
                        lw=0.6, alpha=0.20, zo=2)

    add_signature(fig, ax, BG)
    save(fig, "fractured_seismic_fault.pdf")

if __name__ == '__main__':
    render()
