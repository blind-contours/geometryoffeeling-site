"""
Geometry of Feeling — Growth: Venation
A single leaf rendered as branching veins — midrib to secondary
veins to fine venules. The vascular architecture that feeds every
cell, drawn as a leaf-shaped network of flowing green.
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
    rng = np.random.default_rng(123)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    bg_rgb = hex_to_rgb01(BG_COLOR)
    palette_hex = ['#1A3A1A', '#2D5A2D', '#3A6B3A', '#4A7C4A',
                   '#5C9A3A', '#6BAF4A', '#8BC362', '#A8C890']
    palette = [blend(hex_to_rgb01(h), bg_rgb, 0.04) for h in palette_hex]

    all_veins = []  # (xs, ys, lw, depth_frac, alpha)

    # Leaf shape parameters (slightly asymmetric for natural feel)
    # Leaf center line goes from bottom-center to top-center
    leaf_base_x, leaf_base_y = 0.50, 0.06
    leaf_tip_x, leaf_tip_y = 0.50, 0.94
    leaf_length = leaf_tip_y - leaf_base_y

    # Leaf width at each height (widest at ~40% from base)
    def leaf_half_width(t):
        """Half-width of leaf at normalized position t along midrib."""
        # Elliptical with peak at t=0.38
        w = 0.28 * np.sin(np.pi * t ** 0.75) ** 0.85
        return w

    # --- Midrib ---
    n_mid = 200
    mid_t = np.linspace(0, 1, n_mid)
    mid_x = leaf_base_x + 0.008 * np.sin(2.5 * np.pi * mid_t)
    mid_y = leaf_base_y + leaf_length * mid_t
    all_veins.append((mid_x, mid_y, 3.0, 0.0, 0.90))

    # --- Leaf outline (very subtle) ---
    outline_t = np.linspace(0, 1, 400)
    outline_hw = np.array([leaf_half_width(t) for t in outline_t])
    # Right side
    right_x = leaf_base_x + outline_hw + 0.005 * np.sin(8 * np.pi * outline_t)
    right_y = leaf_base_y + leaf_length * outline_t
    all_veins.append((right_x, right_y, 0.6, 0.5, 0.25))
    # Left side
    left_x = leaf_base_x - outline_hw - 0.005 * np.sin(8 * np.pi * outline_t + 0.3)
    left_y = leaf_base_y + leaf_length * outline_t
    all_veins.append((left_x, left_y, 0.6, 0.5, 0.25))

    max_depth = 5

    def add_vein(x0, y0, angle, length, width, depth, t_on_midrib):
        if depth > max_depth or length < 0.005 or width < 0.08:
            return

        n = 35
        t = np.linspace(0, 1, n)
        # Veins curve slightly toward leaf tip
        tip_pull = 0.08 * (1 - t_on_midrib)
        curve = rng.normal(0, 0.06) + tip_pull
        wobble = 0.008 * np.sin(rng.uniform(3, 8) * np.pi * t)
        theta = angle + curve * t + wobble

        step = length / n
        xs = np.zeros(n)
        ys = np.zeros(n)
        xs[0], ys[0] = x0, y0
        for i in range(1, n):
            xs[i] = xs[i - 1] + step * np.cos(theta[i])
            ys[i] = ys[i - 1] + step * np.sin(theta[i])

        # Clip to leaf boundary
        for i in range(n):
            local_t = (ys[i] - leaf_base_y) / leaf_length
            local_t = np.clip(local_t, 0, 1)
            hw = leaf_half_width(local_t) * 0.95
            max_dist = leaf_base_x + hw
            min_dist = leaf_base_x - hw
            if xs[i] > max_dist or xs[i] < min_dist:
                xs = xs[:i]
                ys = ys[:i]
                break

        if len(xs) < 3:
            return

        depth_frac = depth / max_depth
        alpha = 0.75 - 0.25 * depth_frac
        all_veins.append((xs, ys, width, depth_frac, alpha))

        # Sub-veins
        if depth < max_depth:
            n_sub = rng.integers(2, 4) if depth < 3 else rng.integers(1, 3)
            for _ in range(n_sub):
                bp = rng.uniform(0.30, 0.85)
                bi = min(int(bp * (len(xs) - 1)), len(xs) - 1)

                # Sub-veins angle away from midrib, slightly toward tip
                sub_angle = theta[min(bi, len(theta) - 1)] + rng.uniform(-0.3, 0.3)
                sub_length = length * rng.uniform(0.35, 0.60)
                sub_width = width * rng.uniform(0.50, 0.70)
                sub_t = (ys[bi] - leaf_base_y) / leaf_length
                add_vein(xs[bi], ys[bi], sub_angle, sub_length, sub_width,
                         depth + 1, sub_t)

    # --- Secondary veins from midrib ---
    n_secondary = 18
    for i in range(n_secondary):
        t_pos = 0.08 + 0.84 * (i / (n_secondary - 1))
        idx = int(t_pos * (n_mid - 1))
        vx, vy = mid_x[idx], mid_y[idx]

        hw = leaf_half_width(t_pos)

        # Veins go both left and right from midrib
        for side in [-1, 1]:
            # Angle: roughly perpendicular to midrib, tilted toward tip
            base_angle = side * (np.pi / 2)
            # Tilt toward tip more at base, less at tip
            tilt = 0.35 * (1 - t_pos) * side
            angle = base_angle - tilt

            length = hw * rng.uniform(0.75, 0.95)
            width = 1.6 - 0.8 * t_pos  # thicker near base
            width *= rng.uniform(0.85, 1.0)

            add_vein(vx, vy, angle, length, max(width, 0.4), 1, t_pos)

    # Render: thick first
    all_veins.sort(key=lambda v: -v[2])

    for (xs, ys, lw, depth_frac, alpha) in all_veins:
        color = interpolate_palette(palette, depth_frac)
        ax.plot(xs, ys, color=(*color, alpha), lw=lw, solid_capstyle='round')

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_venation.pdf")
    add_signature(fig, ax, BG_COLOR)
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    render()
