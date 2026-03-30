"""
Geometry of Feeling — Fractured: Fractured Glass Fracture
Standalone render script
"""

import numpy as np
import matplotlib
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

def label(ax, eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.15,0.15,0.20,0.25),transform=ax.transData)
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
    np.random.seed(19)

    # Impact point
    imp_x = cx + PW * 0.05
    imp_y = cy - PH * 0.04

    max_r = PW * 0.50

    # ---- RADIAL CRACKS with branching ----
    n_primary = 14
    primary_angles = np.linspace(0, 2 * np.pi, n_primary, endpoint=False)
    primary_angles += np.random.uniform(-0.08, 0.08, n_primary)

    crack_colors = [NAVY, COBALT, TEAL, SIENNA, CRIMSON, RUST, OCHRE, FOREST]

    # Store all crack paths for concentric ring gap detection
    all_crack_paths = []

    def draw_crack(start_x, start_y, angle, length, depth, col_idx):
        """Recursively draw a crack that may branch."""
        n_pts = 300
        t = np.linspace(0, 1, n_pts)

        # Crack path: mostly straight with small random wobble
        wobble_freq = 3 + depth * 2
        wobble_amp = length * 0.025 * (1 + depth * 0.5)
        wobble = wobble_amp * np.cumsum(np.random.randn(n_pts)) / np.sqrt(n_pts)

        r = length * t
        xs_c = start_x + r * np.cos(angle) + wobble * np.cos(angle + np.pi / 2)
        ys_c = start_y + r * np.sin(angle) * (PH / PW) + wobble * np.sin(angle + np.pi / 2) * (PH / PW)

        # Clip to canvas
        mask = ((xs_c > PAD_L) & (xs_c < PAD_L + PW) &
                (ys_c > PAD_B) & (ys_c < PAD_B + PH))
        if mask.sum() < 3:
            return

        col = crack_colors[col_idx % len(crack_colors)]
        alpha = 0.50 - depth * 0.12
        lw = 1.4 - depth * 0.35

        for seg_xs, seg_ys in split_segments(xs_c, ys_c, mask):
            draw_lc(ax, seg_xs, seg_ys, col, lw=max(lw, 0.3),
                    alpha=max(alpha, 0.10), zo=4 + depth)

        # Store path for gap detection
        all_crack_paths.append((xs_c[mask], ys_c[mask]))

        # Branch at ~60% and ~85% of crack length (if not too deep)
        if depth < 3:
            for branch_frac in [0.55, 0.80]:
                if np.random.random() < 0.65 - depth * 0.15:
                    bi = int(branch_frac * n_pts)
                    if bi < len(xs_c) and mask[bi]:
                        branch_angle = angle + np.random.choice([-1, 1]) * (
                            0.25 + np.random.uniform(0, 0.35))
                        branch_len = length * (0.25 + np.random.uniform(0, 0.2))
                        draw_crack(xs_c[bi], ys_c[bi], branch_angle,
                                   branch_len, depth + 1, col_idx + depth + 1)

    for i, angle in enumerate(primary_angles):
        crack_len = max_r * (0.7 + 0.3 * np.random.random())
        draw_crack(imp_x, imp_y, angle, crack_len, 0, i)

    # ---- CONCENTRIC STRESS RINGS ----
    n_rings = 22
    for ri in range(1, n_rings + 1):
        r = max_r * ri / n_rings
        theta = np.linspace(0, 2 * np.pi, 800)
        xs_r = imp_x + r * np.cos(theta)
        ys_r = imp_y + r * np.sin(theta) * (PH / PW)

        # Create gaps near radial cracks
        gap_mask = np.ones(len(theta), dtype=bool)
        for crack_xs, crack_ys in all_crack_paths:
            for ci in range(len(crack_xs)):
                dists = np.sqrt((xs_r - crack_xs[ci])**2 +
                                (ys_r - crack_ys[ci])**2)
                gap_mask &= (dists > 0.08 + 0.04 * (ri / n_rings))

        # Also clip to canvas
        bounds_mask = ((xs_r > PAD_L) & (xs_r < PAD_L + PW) &
                       (ys_r > PAD_B) & (ys_r < PAD_B + PH))
        combined = gap_mask & bounds_mask

        if combined.sum() < 3:
            continue

        ring_alpha = 0.18 + 0.20 * (1 - ri / n_rings)
        ring_lw = 0.4 + 0.6 * (1 - ri / n_rings)
        ring_col = TEAL if ri % 3 == 0 else (COBALT if ri % 3 == 1 else NAVY)

        for seg_xs, seg_ys in split_segments(xs_r, ys_r, combined):
            draw_lc(ax, seg_xs, seg_ys, ring_col, lw=ring_lw,
                    alpha=ring_alpha, zo=3)

    # Impact point glow
    for r_, a_ in [(0.15, 0.08), (0.08, 0.18), (0.03, 0.35)]:
        ax.add_patch(Circle((imp_x, imp_y), radius=r_,
                    facecolor=rgba(CRIMSON, a_), edgecolor='none', zorder=7))

    label(ax, "\u03c3(r) ~ K_IC / \u221a(2\u03c0r)")
    save(fig, "fractured_glass_fracture.pdf")


if __name__ == '__main__':
    render()
