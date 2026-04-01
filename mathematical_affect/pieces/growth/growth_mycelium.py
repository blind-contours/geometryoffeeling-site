"""
Geometry of Feeling — Growth: Mycelium
Space colonization algorithm (Runions et al. 2007) —
a single spore site grows a branching network through
clustered nutrient zones, shifting color as it discovers
each one. Thick trunk hyphae taper to gossamer tips
via the pipe model.

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
"""

import os
import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
PRINT_DIR = os.path.join(SCRIPT_DIR, '..', '..', '..', 'public', 'prints', 'growth')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#F5F0E6'

# ── Growth Series Palette ─────────────────────────────────────────────────────
DEEP_MOSS    = '#1A3A1A'
DARK_GREEN   = '#1A4D2E'
FOREST       = '#2E8B4A'
SPRING       = '#6BBF6E'
LIME         = '#A8D86E'
GOLD         = '#E8D878'
TEAL         = '#2A7A6A'
AMBER        = '#C8A030'
WARM_OCHRE   = '#D4A832'


def hex_to_rgb01(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)]) / 255.0


def blend(c1, c2, t):
    return (1 - t) * np.asarray(c1) + t * np.asarray(c2)


# ── Space Colonization ─────────────────────────────────────────────────────────
def space_colonize(attractors, root, step=0.005, influence=0.10,
                   kill=0.005, max_iter=1000):
    """
    Runions et al. 2007 space colonization algorithm.
    Operates in normalized coordinates (0..1, 0..1).
    Returns nodes, parents, and depth for each node.
    """
    att = np.array(attractors, dtype=float).copy()
    nodes = [np.array(root, dtype=float)]
    parents = [-1]
    depths = [0]

    for _ in range(max_iter):
        if len(att) == 0:
            break
        na = np.array(nodes)
        tree = KDTree(na)
        dists, closest = tree.query(att)

        growth = {}
        for ai, (d, ni) in enumerate(zip(dists, closest)):
            if d < influence:
                dr = att[ai] - nodes[ni]
                n2 = np.linalg.norm(dr)
                if n2 > 1e-10:
                    dr /= n2
                growth.setdefault(ni, []).append(dr)

        if not growth:
            break

        for ni, dirs in growth.items():
            avg = np.mean(dirs, axis=0)
            n2 = np.linalg.norm(avg)
            if n2 > 1e-10:
                avg /= n2
            nodes.append(nodes[ni] + avg * step)
            parents.append(ni)
            depths.append(depths[ni] + 1)

        na = np.array(nodes)
        tree = KDTree(na)
        dists, _ = tree.query(att)
        att = att[dists > kill]

    return nodes, parents, depths


def pipe_model(parents, n_nodes):
    """Compute subtree size for each node (pipe model thickness)."""
    cc = np.ones(n_nodes)
    for i in range(n_nodes - 1, -1, -1):
        p = parents[i]
        if p >= 0:
            cc[p] += cc[i]
    return cc


def render_network(ax, nodes, parents, depths, palette_func,
                   lw_max=5.0, lw_min=0.08, alpha_trunk=0.92,
                   alpha_tip=0.12):
    """Render network with pipe-model thickness and zone-aware color."""
    n = len(nodes)
    if n < 2:
        return

    cc = pipe_model(parents, n)
    max_cc = cc.max()
    max_depth = max(depths) if depths else 1

    for i in range(1, n):
        p = parents[i]
        if p < 0:
            continue

        frac = (cc[i] / max_cc) ** 0.4
        lw = lw_min + (lw_max - lw_min) * (frac ** 0.7)

        depth_frac = depths[i] / max_depth if max_depth > 0 else 0
        col = palette_func(depth_frac, nodes[i])

        alpha = alpha_tip + (alpha_trunk - alpha_tip) * frac

        ax.plot([nodes[p][0], nodes[i][0]],
                [nodes[p][1], nodes[i][1]],
                color=(*col, alpha),
                linewidth=lw,
                solid_capstyle='round',
                zorder=max(1, int(frac * 10)))


def make_nutrient_palette(base_colors_hex, zone_specs):
    """Palette that shifts color near nutrient discovery zones."""
    base_colors = [hex_to_rgb01(h) for h in base_colors_hex]

    def palette_func(depth_frac, pos):
        # Base color interpolated by depth
        t = np.clip(depth_frac, 0, 1)
        idx = t * (len(base_colors) - 1)
        i = int(np.floor(idx))
        f = idx - i
        if i >= len(base_colors) - 1:
            base = np.array(base_colors[-1])
        else:
            base = np.array(blend(base_colors[i], base_colors[i + 1], f))

        # Shift color near nutrient zones
        pos = np.array(pos)
        for (zx, zy, radius, color_hex) in zone_specs:
            zc = hex_to_rgb01(color_hex)
            d = np.sqrt((pos[0] - zx)**2 + (pos[1] - zy)**2)
            if d < radius:
                mix = (1.0 - (d / radius)) ** 1.5
                base = blend(base, zc, mix * 0.75)

        return tuple(base)
    return palette_func


def render():
    rng = np.random.default_rng(2020)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Nutrient-rich zones with gaps between them
    nutrient_centers = [
        (0.35, 0.55), (0.60, 0.35), (0.75, 0.70),
        (0.45, 0.82), (0.85, 0.50),
    ]

    # Clustered attractors around nutrient centers
    all_att = []
    for cx, cy in nutrient_centers:
        pts = np.column_stack([
            rng.normal(cx, 0.16, 500),
            rng.normal(cy, 0.16, 500)
        ])
        pts = pts[(pts[:, 0] > 0.06) & (pts[:, 0] < 0.94) &
                  (pts[:, 1] > 0.06) & (pts[:, 1] < 0.94)]
        all_att.append(pts)

    # Sparse background attractors for connective tendrils
    att_bg = np.column_stack([
        rng.uniform(0.06, 0.94, 800),
        rng.uniform(0.06, 0.94, 800)
    ])
    all_att.append(att_bg)
    att = np.vstack(all_att)

    # Single origin — bottom left
    nodes, parents, depths = space_colonize(
        att, (0.08, 0.12),
        step=0.005,
        influence=0.10,
        kill=0.005,
        max_iter=1000
    )

    # Nutrient zones: network shifts color as it finds each one
    zone_specs = [
        (0.35, 0.55, 0.14, AMBER),
        (0.60, 0.35, 0.12, WARM_OCHRE),
        (0.75, 0.70, 0.13, GOLD),
        (0.45, 0.82, 0.11, LIME),
        (0.85, 0.50, 0.12, TEAL),
    ]
    palette = make_nutrient_palette(
        [DEEP_MOSS, DARK_GREEN, FOREST, SPRING], zone_specs
    )

    render_network(ax, nodes, parents, depths, palette,
                   lw_max=5.0, lw_min=0.08,
                   alpha_trunk=0.92, alpha_tip=0.12)

    add_signature(fig, ax, BG_COLOR)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_mycelium.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    print(f"saved {pdf_path}")

    # Also save JPG for site
    os.makedirs(PRINT_DIR, exist_ok=True)
    jpg_path = os.path.join(PRINT_DIR, "growth_mycelium.jpg")
    fig.savefig(jpg_path, facecolor=BG_COLOR, dpi=DPI, format='jpg')
    print(f"saved {jpg_path}")

    plt.close(fig)
    return pdf_path


if __name__ == '__main__':
    render()
