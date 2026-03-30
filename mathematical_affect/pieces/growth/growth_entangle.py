"""
Geometry of Feeling — Growth: Entangle
Two trees growing toward each other — one warm, one cool.
Their canopies interweave into a single crown, separate roots
converging into shared light.
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
    rng = np.random.default_rng(99)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    bg_rgb = hex_to_rgb01(BG_COLOR)

    # Two palettes: warm (amber/sienna) and cool (green/teal)
    warm_hex = ['#3D2B1F', '#6B4226', '#8B6914', '#A07828',
                '#C89028', '#D4A832', '#D8C878']
    cool_hex = ['#1A3A1A', '#2D5A2D', '#3A6B3A', '#4A7C4A',
                '#5C9A3A', '#6BAF4A', '#A8C890']
    warm_pal = [blend(hex_to_rgb01(h), bg_rgb, 0.04) for h in warm_hex]
    cool_pal = [blend(hex_to_rgb01(h), bg_rgb, 0.04) for h in cool_hex]

    all_branches = []  # (xs, ys, lw, depth_frac, alpha, palette)

    max_depth = 8

    def add_branch(x0, y0, angle, length, width, depth, pal, lean_toward):
        if depth > max_depth or length < 0.005 or width < 0.08:
            return

        n = 40
        t = np.linspace(0, 1, n)
        curve = rng.normal(0, 0.10)
        wobble = 0.015 * np.sin(rng.uniform(2, 5) * np.pi * t + rng.uniform(0, 6))
        theta = angle + curve * t + wobble

        step = length / n
        xs = np.zeros(n)
        ys = np.zeros(n)
        xs[0], ys[0] = x0, y0
        for i in range(1, n):
            xs[i] = xs[i - 1] + step * np.sin(theta[i])
            ys[i] = ys[i - 1] + step * np.cos(theta[i])

        depth_frac = depth / max_depth
        alpha = 0.85 - 0.25 * depth_frac
        all_branches.append((xs, ys, width, depth_frac, alpha, pal))

        # Branching
        if depth < 2:
            n_children = rng.integers(2, 5)
        elif depth < 4:
            n_children = rng.integers(2, 4)
        elif depth < 6:
            n_children = rng.integers(1, 3)
        else:
            n_children = rng.integers(1, 3)

        for _ in range(n_children):
            bp = rng.uniform(0.45, 0.95)
            bi = int(bp * (n - 1))
            bx, by = xs[bi], ys[bi]

            spread = rng.uniform(-0.55, 0.55)
            child_angle = theta[bi] + spread
            # Lean toward the other tree's side
            child_angle += lean_toward * 0.04
            child_angle *= 0.92

            child_length = length * rng.uniform(0.50, 0.70)
            child_width = width * rng.uniform(0.52, 0.68)
            add_branch(bx, by, child_angle, child_length, child_width,
                       depth + 1, pal, lean_toward)

    # --- Left tree (warm palette) ---
    # Trunk
    trunk_n = 50
    trunk_t = np.linspace(0, 1, trunk_n)
    left_trunk_x = 0.28 + 0.005 * np.sin(2 * np.pi * trunk_t)
    left_trunk_y = 0.05 + 0.28 * trunk_t
    all_branches.append((left_trunk_x, left_trunk_y, 4.0, 0.0, 0.92, warm_pal))

    # Main branches — lean right
    for angle in [-0.40, -0.10, 0.15, 0.40, 0.60]:
        a = angle + rng.normal(0, 0.05)
        add_branch(0.28, 0.33, a, rng.uniform(0.18, 0.30), rng.uniform(1.8, 2.8),
                   1, warm_pal, lean_toward=0.5)

    # --- Right tree (cool palette) ---
    right_trunk_x = 0.72 + 0.005 * np.sin(2 * np.pi * trunk_t + 1.0)
    right_trunk_y = 0.05 + 0.28 * trunk_t
    all_branches.append((right_trunk_x, right_trunk_y, 4.0, 0.0, 0.92, cool_pal))

    for angle in [-0.60, -0.40, -0.15, 0.10, 0.40]:
        a = angle + rng.normal(0, 0.05)
        add_branch(0.72, 0.33, a, rng.uniform(0.18, 0.30), rng.uniform(1.8, 2.8),
                   1, cool_pal, lean_toward=-0.5)

    # Render: thick first
    all_branches.sort(key=lambda b: -b[2])

    for (xs, ys, lw, depth_frac, alpha, pal) in all_branches:
        color = interpolate_palette(pal, depth_frac)
        ax.plot(xs, ys, color=(*color, alpha), lw=lw, solid_capstyle='round')

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_entangle.pdf")
    add_signature(fig, ax, BG_COLOR)
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    render()
