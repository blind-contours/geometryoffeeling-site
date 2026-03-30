"""
Geometry of Feeling — Growth: Canopy
Recursive branching tree — smooth curves split and split again,
each branch a continuous arc reaching upward. Da Vinci's pipe
model determines the width of every limb.
"""

import os
import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

def interpolate_palette(colors, u):
    colors = [np.asarray(c) for c in colors]
    u = np.clip(u, 0.0, 1.0)
    if u <= 0:
        return colors[0]
    if u >= 1:
        return colors[-1]
    pos = u * (len(colors) - 1)
    i = int(np.floor(pos))
    frac = pos - i
    return blend(colors[i], colors[i + 1], frac)

def render():
    rng = np.random.default_rng(42)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    bg_rgb = hex_to_rgb01(BG_COLOR)

    # Palette: rich earthy trunk → lush green canopy
    palette_hex = ['#2E1A0E', '#3D2B1F', '#5C4033', '#6B4226',
                   '#1A3A1A', '#2D5A2D', '#3A6B3A', '#4A7C4A',
                   '#5C9A3A', '#6BAF4A', '#8BC362', '#A8C890']
    palette = [blend(hex_to_rgb01(h), bg_rgb, 0.04) for h in palette_hex]

    all_branches = []  # (xs, ys, lw, depth_frac, alpha)

    max_depth = 9

    def add_branch(x0, y0, angle, length, width, depth):
        if depth > max_depth or length < 0.004 or width < 0.06:
            return

        # Smooth arc for this branch
        n = 45
        t = np.linspace(0, 1, n)

        # Gentle curvature with slight wobble
        curve = rng.normal(0, 0.12)
        wobble = 0.018 * np.sin(rng.uniform(2, 6) * np.pi * t + rng.uniform(0, 6))
        theta = angle + curve * t + wobble

        # Build smooth path
        step = length / n
        xs = np.zeros(n)
        ys = np.zeros(n)
        xs[0], ys[0] = x0, y0
        for i in range(1, n):
            xs[i] = xs[i - 1] + step * np.sin(theta[i])
            ys[i] = ys[i - 1] + step * np.cos(theta[i])

        depth_frac = depth / max_depth
        alpha = 0.88 - 0.28 * depth_frac
        all_branches.append((xs, ys, width, depth_frac, alpha))

        # More branching at every level for density
        if depth < 2:
            n_children = rng.integers(3, 6)
        elif depth < 4:
            n_children = rng.integers(2, 5)
        elif depth < 6:
            n_children = rng.integers(2, 4)
        else:
            n_children = rng.integers(1, 3)

        for _ in range(n_children):
            # Branch point along this segment
            bp = rng.uniform(0.40, 0.95) if depth > 0 else rng.uniform(0.75, 1.0)
            bi = int(bp * (n - 1))
            bx, by = xs[bi], ys[bi]

            # Child angle: spread outward with upward bias
            spread = rng.uniform(-0.60, 0.60)
            child_angle = theta[bi] + spread
            child_angle = child_angle * 0.90  # gentle pull toward vertical

            # Taper
            child_length = length * rng.uniform(0.48, 0.72)
            child_width = width * rng.uniform(0.50, 0.68)

            add_branch(bx, by, child_angle, child_length, child_width, depth + 1)

    # --- Trunk ---
    trunk_n = 60
    trunk_t = np.linspace(0, 1, trunk_n)
    trunk_xs = 0.50 + 0.005 * np.sin(1.8 * np.pi * trunk_t) + 0.003 * np.sin(4.1 * np.pi * trunk_t)
    trunk_ys = 0.05 + 0.28 * trunk_t
    all_branches.append((trunk_xs, trunk_ys, 5.2, 0.0, 0.94))

    # --- Main branches from trunk top ---
    trunk_top_x, trunk_top_y = 0.50, 0.33
    main_angles = [-0.62, -0.38, -0.15, 0.08, 0.30, 0.52, 0.70]

    for i, base_angle in enumerate(main_angles):
        angle = base_angle + rng.normal(0, 0.05)
        length = rng.uniform(0.26, 0.40)
        width = rng.uniform(2.4, 3.5)
        add_branch(trunk_top_x, trunk_top_y, angle, length, width, 1)

    # Branches lower on trunk for fullness
    for y_frac, spread in [(0.60, 0.8), (0.72, 0.65), (0.85, 0.55)]:
        bx = trunk_xs[int(y_frac * (trunk_n - 1))]
        by = trunk_ys[int(y_frac * (trunk_n - 1))]
        for side in [-1, 1]:
            angle = side * rng.uniform(spread * 0.7, spread * 1.1)
            add_branch(bx, by, angle, rng.uniform(0.12, 0.22), rng.uniform(1.4, 2.2), 2)

    # --- Render: thickest (background) first, thinnest (foreground) last ---
    all_branches.sort(key=lambda b: -b[2])

    for (xs, ys, lw, depth_frac, alpha) in all_branches:
        color = interpolate_palette(palette, depth_frac)
        ax.plot(xs, ys, color=(*color, alpha), lw=lw, solid_capstyle='round')

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_canopy.pdf")
    add_signature(fig, ax, BG_COLOR)
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    render()
