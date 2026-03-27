"""
Geometry of Feeling — Growth: Thaw
Dormancy giving way to life — bare branches at the base
become lush growth at the crown. A single tree waking up.
Color warms and density increases from root to tip.
"""

import os
import numpy as np
import matplotlib
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
    rng = np.random.default_rng(55)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    bg_rgb = hex_to_rgb01(BG_COLOR)

    # Dormant palette (gray/brown) → alive palette (green/spring)
    dormant_hex = ['#4A4540', '#5C5650', '#6B6560', '#7A746E', '#8A847E']
    alive_hex = ['#2D5A2D', '#3A6B3A', '#4A7C4A', '#6BAF4A', '#8BC362', '#A8C890']

    dormant_pal = [blend(hex_to_rgb01(h), bg_rgb, 0.06) for h in dormant_hex]
    alive_pal = [blend(hex_to_rgb01(h), bg_rgb, 0.04) for h in alive_hex]

    trunk_hex = ['#3D2B1F', '#5C4033', '#6B4226']
    trunk_pal = [blend(hex_to_rgb01(h), bg_rgb, 0.04) for h in trunk_hex]

    all_branches = []  # (xs, ys, lw, alpha, color_rgb)

    max_depth = 8

    def branch_color(depth, branch_y):
        """Color blends from dormant (low) to alive (high) based on y position."""
        depth_frac = depth / max_depth
        # Transition zone: y=0.30 (dormant) to y=0.65 (alive)
        thaw_frac = np.clip((branch_y - 0.25) / 0.40, 0.0, 1.0)
        thaw_frac = thaw_frac ** 0.7  # slightly more dormant below

        if thaw_frac < 0.3:
            # Dormant: browns and grays
            c = interpolate_palette(trunk_pal + dormant_pal, depth_frac * 0.7)
        elif thaw_frac > 0.7:
            # Alive: rich greens
            c = interpolate_palette(trunk_pal + alive_pal, depth_frac)
        else:
            # Transition: blend
            c_dormant = interpolate_palette(trunk_pal + dormant_pal, depth_frac * 0.7)
            c_alive = interpolate_palette(trunk_pal + alive_pal, depth_frac)
            blend_t = (thaw_frac - 0.3) / 0.4
            c = blend(c_dormant, c_alive, blend_t)
        return c

    def add_branch(x0, y0, angle, length, width, depth):
        if depth > max_depth or length < 0.004 or width < 0.06:
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

        avg_y = np.mean(ys)
        depth_frac = depth / max_depth
        color = branch_color(depth, avg_y)

        # Higher branches get more children (thaw = more growth)
        thaw = np.clip((avg_y - 0.25) / 0.45, 0.0, 1.0)
        alpha = 0.60 + 0.30 * thaw ** 0.5 - 0.10 * depth_frac

        all_branches.append((xs, ys, width, alpha, color))

        # More branching at higher positions (spring growth)
        base_children = 1 if thaw < 0.3 else 2
        if depth < 3:
            n_children = base_children + rng.integers(1, 3 + int(thaw * 2))
        elif depth < 5:
            n_children = base_children + rng.integers(0, 2 + int(thaw * 2))
        else:
            n_children = rng.integers(1, 2 + int(thaw * 1.5))

        for _ in range(n_children):
            bp = rng.uniform(0.45, 0.95)
            bi = int(bp * (n - 1))
            bx, by = xs[bi], ys[bi]

            spread = rng.uniform(-0.55, 0.55)
            child_angle = theta[bi] + spread
            child_angle *= 0.92

            child_length = length * rng.uniform(0.48, 0.70)
            child_width = width * rng.uniform(0.50, 0.68)
            add_branch(bx, by, child_angle, child_length, child_width, depth + 1)

    # --- Trunk ---
    trunk_n = 60
    trunk_t = np.linspace(0, 1, trunk_n)
    trunk_xs = 0.50 + 0.005 * np.sin(1.8 * np.pi * trunk_t)
    trunk_ys = 0.04 + 0.30 * trunk_t
    trunk_color = interpolate_palette(trunk_pal, 0.3)
    all_branches.append((trunk_xs, trunk_ys, 5.0, 0.92, trunk_color))

    # --- Main branches ---
    trunk_top = 0.34
    main_angles = [-0.60, -0.35, -0.12, 0.10, 0.32, 0.58]
    for angle in main_angles:
        a = angle + rng.normal(0, 0.05)
        add_branch(0.50, trunk_top, a, rng.uniform(0.22, 0.36),
                   rng.uniform(2.0, 3.2), 1)

    # Lower branches (these will be dormant)
    for y_frac in [0.55, 0.70, 0.82]:
        by = trunk_ys[int(y_frac * (trunk_n - 1))]
        bx = trunk_xs[int(y_frac * (trunk_n - 1))]
        for side in [-1, 1]:
            a = side * rng.uniform(0.5, 0.8)
            add_branch(bx, by, a, rng.uniform(0.10, 0.18),
                       rng.uniform(1.2, 1.8), 2)

    # Render thick first
    all_branches.sort(key=lambda b: -b[2])

    for (xs, ys, lw, alpha, color) in all_branches:
        ax.plot(xs, ys, color=(*color, alpha), lw=lw, solid_capstyle='round')

    # Equation label
    ax.text(0.06, 0.06, "G(t)=G\u2080\u00b7\u03c3(r(t\u2212t\u2080))",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_thaw.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
