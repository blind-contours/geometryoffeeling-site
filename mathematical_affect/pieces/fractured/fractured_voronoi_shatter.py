"""
Geometry of Feeling — Fractured: Fractured Voronoi Shatter
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
    from scipy.spatial import Voronoi
    fig, ax = make_fig()
    np.random.seed(77)

    # Impact point -- slightly off-center for asymmetry
    impact_x = cx - PW * 0.12
    impact_y = cy + PH * 0.08

    # Generate seed points across the canvas region
    n_seeds = 220
    seeds_x = PAD_L + PW * np.random.uniform(0.02, 0.98, n_seeds)
    seeds_y = PAD_B + PH * np.random.uniform(0.02, 0.98, n_seeds)
    seeds = np.column_stack([seeds_x, seeds_y])

    # Add far-away mirror points so all Voronoi regions are finite
    margin = 8.0
    mirror = np.array([
        [-margin, -margin], [FIG_W + margin, -margin],
        [-margin, FIG_H + margin], [FIG_W + margin, FIG_H + margin],
        [FIG_W / 2, -margin], [FIG_W / 2, FIG_H + margin],
        [-margin, FIG_H / 2], [FIG_W + margin, FIG_H / 2],
    ])
    all_seeds = np.vstack([seeds, mirror])
    vor = Voronoi(all_seeds)

    # Palette cycling for cells
    cell_colors = [COBALT, FOREST, TEAL, NAVY, SIENNA, OCHRE, CRIMSON, RUST]

    # Draw each Voronoi cell, displaced from impact
    for idx in range(n_seeds):
        region_idx = vor.point_region[idx]
        region = vor.regions[region_idx]
        if -1 in region or len(region) < 3:
            continue

        verts = np.array([vor.vertices[v] for v in region])
        centroid = np.mean(verts, axis=0)

        # Distance from impact
        dx = centroid[0] - impact_x
        dy = centroid[1] - impact_y
        dist = np.sqrt(dx**2 + dy**2)
        if dist < 0.01:
            dist = 0.01

        # Displacement: stronger near impact, radially outward
        max_disp = PW * 0.065
        displacement = max_disp / (dist**0.6 + 0.3)
        disp_x = displacement * dx / dist
        disp_y = displacement * dy / dist

        # Displace all vertices of this cell
        displaced = verts.copy()
        displaced[:, 0] += disp_x
        displaced[:, 1] += disp_y

        # Close the polygon
        poly_x = np.append(displaced[:, 0], displaced[0, 0])
        poly_y = np.append(displaced[:, 1], displaced[0, 1])

        # Clip check
        in_bounds = ((poly_x > PAD_L - 0.5) & (poly_x < PAD_L + PW + 0.5) &
                     (poly_y > PAD_B - 0.5) & (poly_y < PAD_B + PH + 0.5))
        if in_bounds.sum() < 3:
            continue

        col = cell_colors[idx % len(cell_colors)]
        # Fill: very light wash
        fill_alpha = 0.06 + 0.04 * (displacement / max_disp)
        ax.fill(poly_x, poly_y, color=rgba(col, fill_alpha),
                linewidth=0, zorder=2)

        # Edge: the fracture lines
        # Vary weight: thicker near impact where stress is highest
        edge_alpha = 0.35 + 0.40 * min(1.0, displacement / max_disp)
        edge_lw = 0.6 + 1.2 * min(1.0, displacement / max_disp)
        draw_lc(ax, poly_x, poly_y, col, lw=edge_lw,
                alpha=edge_alpha, zo=3)

    # Impact point: small starburst
    for r_, a_ in [(0.18, 0.06), (0.10, 0.12), (0.04, 0.28)]:
        ax.add_patch(Circle((impact_x, impact_y), radius=r_,
                    facecolor=rgba(CRIMSON, a_), edgecolor='none', zorder=6))

    # Radial stress lines from impact (faint)
    n_stress = 36
    for i in range(n_stress):
        angle = 2 * np.pi * i / n_stress
        t = np.linspace(0, 1, 400)
        r = PW * 0.55 * t
        xs_s = impact_x + r * np.cos(angle)
        ys_s = impact_y + r * np.sin(angle) * (PH / PW)
        mask = ((xs_s > PAD_L) & (xs_s < PAD_L + PW) &
                (ys_s > PAD_B) & (ys_s < PAD_B + PH))
        if mask.sum() < 3:
            continue
        for seg_xs, seg_ys in split_segments(xs_s, ys_s, mask):
            pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            n_s = len(segs)
            alphas = np.linspace(0.14, 0.01, n_s)
            lws = np.linspace(0.8, 0.15, n_s)
            colors = [rgba(CRIMSON, float(a_)) for a_ in alphas]
            lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                   capstyle='round', zorder=1)
            ax.add_collection(lc)

    add_signature(fig, ax, BG)
    save(fig, "fractured_voronoi_shatter.pdf")

if __name__ == '__main__':
    render()
