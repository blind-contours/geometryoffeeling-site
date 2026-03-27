"""
Geometry of Feeling — Growth: Mycelium
Space colonization algorithm (Runions et al. 2007) —
six spore germination sites each grow a branching
network through a shared attractor field. Thick trunk
hyphae taper to gossamer tips via the pipe model.

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#F5F0E6'


def hex_to_rgb01(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)]) / 255.0


def blend(c1, c2, t):
    return (1 - t) * np.asarray(c1) + t * np.asarray(c2)


# ── Space Colonization ─────────────────────────────────────────────────────────
def space_colonize(attractors, root, step=0.008, influence=0.12,
                   kill=0.008, max_iter=600):
    """
    Runions et al. 2007 space colonization algorithm.
    Operates in normalized coordinates (0..1, 0..1).
    """
    att = np.array(attractors, dtype=float).copy()
    nodes = [np.array(root, dtype=float)]
    parents = [-1]

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

        na = np.array(nodes)
        tree = KDTree(na)
        dists, _ = tree.query(att)
        att = att[dists > kill]

    return nodes, parents


def pipe_model(parents, n_nodes):
    """Compute subtree size for each node (pipe model thickness)."""
    cc = np.ones(n_nodes)
    for i in range(n_nodes - 1, -1, -1):
        p = parents[i]
        if p >= 0:
            cc[p] += cc[i]
    return cc


def render_network(ax, nodes, parents, col_dark, col_light,
                   lw_max=2.8, alpha_base=0.10, alpha_max=0.75):
    """Render tree with depth-based color/thickness."""
    n = len(nodes)
    if n < 2:
        return

    cc = pipe_model(parents, n)
    max_cc = cc.max()

    cd = hex_to_rgb01(col_dark)
    cl = hex_to_rgb01(col_light)

    for i in range(1, n):
        p = parents[i]
        if p < 0:
            continue

        frac = (cc[i] / max_cc) ** 0.35
        col = tuple(cd[k] + (cl[k] - cd[k]) * (1 - frac) for k in range(3))
        alpha = alpha_base + (alpha_max - alpha_base) * frac
        lw = max(0.12, lw_max * (frac ** 0.8))

        ax.plot([nodes[p][0], nodes[i][0]],
                [nodes[p][1], nodes[i][1]],
                color=(*col, alpha),
                linewidth=lw,
                solid_capstyle='round',
                zorder=max(1, int(frac * 10)))


def render():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    rng = np.random.default_rng(2026)

    # Attractor field across the canvas
    n_attractors = 2500
    att_all = np.column_stack([
        rng.uniform(0.04, 0.96, n_attractors),
        rng.uniform(0.06, 0.94, n_attractors)
    ])

    # 6 seed points — spore germination sites
    seeds = [
        (0.18, 0.45),
        (0.50, 0.25),
        (0.82, 0.50),
        (0.38, 0.72),
        (0.68, 0.78),
        (0.50, 0.52),
    ]

    # Color pairs: dark trunk → light tips
    color_pairs = [
        ('#2A4A1A', '#C8D8A8'),   # deep green → pale green
        ('#4A7A3A', '#E8D898'),   # moss → pale amber
        ('#7A5A2A', '#D4A832'),   # umber → amber
        ('#3A8A6A', '#7A9A6A'),   # teal → sage
        ('#2A4A1A', '#8AB84A'),   # dark → spring green
        ('#C06030', '#B87A2A'),   # sienna → ochre
    ]

    for (sx, sy), (col_d, col_l) in zip(seeds, color_pairs):
        # Each seed colonizes attractors within reach
        dists = np.sqrt((att_all[:, 0] - sx)**2 + (att_all[:, 1] - sy)**2)
        local = att_all[dists < 0.30]
        if len(local) < 20:
            continue
        if len(local) > 400:
            idx = rng.choice(len(local), 400, replace=False)
            local = local[idx]

        nodes, parents = space_colonize(
            local, (sx, sy),
            step=0.006,
            influence=0.10,
            kill=0.006,
            max_iter=600
        )

        render_network(ax, nodes, parents, col_d, col_l,
                       lw_max=3.0, alpha_base=0.08, alpha_max=0.78)

    # Equation label
    ax.text(0.06, 0.06,
            "6\u00d7SC(attract, kill, step)",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_mycelium.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
