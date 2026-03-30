"""
Geometry of Feeling — Growth: Roots
What's below — a mirror of the canopy, reaching downward.
Branching roots spread through invisible soil, anchoring
everything we see above. Warm earth tones on cream.
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
    rng = np.random.default_rng(88)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    bg_rgb = hex_to_rgb01(BG_COLOR)

    # Warm earth palette: dark soil → amber → sienna → ochre
    palette_hex = ['#2E1A0E', '#3D2B1F', '#5C4033', '#6B4226',
                   '#8B6914', '#A06030', '#C89028', '#D4A832', '#D8C878']
    palette = [blend(hex_to_rgb01(h), bg_rgb, 0.04) for h in palette_hex]

    all_roots = []  # (xs, ys, lw, depth_frac, alpha)

    max_depth = 9

    def add_root(x0, y0, angle, length, width, depth):
        """Grow a root downward — angle 0 = straight down."""
        if depth > max_depth or length < 0.004 or width < 0.06:
            return

        n = 42
        t = np.linspace(0, 1, n)
        curve = rng.normal(0, 0.12)
        wobble = 0.018 * np.sin(rng.uniform(2, 6) * np.pi * t + rng.uniform(0, 6))
        theta = angle + curve * t + wobble

        step = length / n
        xs = np.zeros(n)
        ys = np.zeros(n)
        xs[0], ys[0] = x0, y0
        for i in range(1, n):
            # Roots grow downward: sin for x, -cos for y
            xs[i] = xs[i - 1] + step * np.sin(theta[i])
            ys[i] = ys[i - 1] - step * np.cos(theta[i])

        # Clip at edges
        for i in range(n):
            if xs[i] < 0.03 or xs[i] > 0.97 or ys[i] < 0.04:
                xs = xs[:i]
                ys = ys[:i]
                break

        if len(xs) < 3:
            return

        depth_frac = depth / max_depth
        alpha = 0.85 - 0.25 * depth_frac
        all_roots.append((xs, ys, width, depth_frac, alpha))

        # Branching — roots branch more at tips
        if depth < 2:
            n_children = rng.integers(3, 6)
        elif depth < 4:
            n_children = rng.integers(2, 5)
        elif depth < 6:
            n_children = rng.integers(2, 4)
        else:
            n_children = rng.integers(1, 3)

        for _ in range(n_children):
            bp = rng.uniform(0.40, 0.95)
            bi = min(int(bp * (len(xs) - 1)), len(xs) - 1)
            bx, by = xs[bi], ys[bi]

            spread = rng.uniform(-0.60, 0.60)
            child_angle = theta[min(bi, len(theta) - 1)] + spread
            # Slight gravitropism: pull toward straight down
            child_angle = child_angle * 0.90

            child_length = length * rng.uniform(0.48, 0.72)
            child_width = width * rng.uniform(0.50, 0.68)
            add_root(bx, by, child_angle, child_length, child_width, depth + 1)

    # --- Taproot (main vertical root) ---
    tap_n = 50
    tap_t = np.linspace(0, 1, tap_n)
    tap_x = 0.50 + 0.005 * np.sin(1.5 * np.pi * tap_t)
    tap_y = 0.92 - 0.55 * tap_t
    all_roots.append((tap_x, tap_y, 5.0, 0.0, 0.94))

    # Small trunk stub above ground
    stub_x = np.array([0.50, 0.50])
    stub_y = np.array([0.95, 0.92])
    all_roots.append((stub_x, stub_y, 5.5, 0.0, 0.94))

    # --- Primary lateral roots ---
    root_top = 0.90
    main_angles = [-0.65, -0.40, -0.15, 0.12, 0.38, 0.62]
    for angle in main_angles:
        a = angle + rng.normal(0, 0.06)
        add_root(0.50, root_top, a, rng.uniform(0.24, 0.38),
                 rng.uniform(2.2, 3.4), 1)

    # Roots from along the taproot
    for t_frac in [0.20, 0.40, 0.55, 0.70]:
        idx = int(t_frac * (tap_n - 1))
        bx, by = tap_x[idx], tap_y[idx]
        for side in [-1, 1]:
            a = side * rng.uniform(0.45, 0.85)
            add_root(bx, by, a, rng.uniform(0.12, 0.24),
                     rng.uniform(1.4, 2.2), 2)

    # Render thick first
    all_roots.sort(key=lambda r: -r[2])

    for (xs, ys, lw, depth_frac, alpha) in all_roots:
        color = interpolate_palette(palette, depth_frac)
        ax.plot(xs, ys, color=(*color, alpha), lw=lw, solid_capstyle='round')

    # Subtle ground line
    ax.axhline(y=0.92, color=(*blend(hex_to_rgb01('#8B6914'), bg_rgb, 0.50), 0.15),
               lw=0.5, xmin=0.10, xmax=0.90)

    # Equation label
    ax.text(0.06, 0.06, "\u2207\u00b7J=\u2212\u2202\u03c1/\u2202t",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_roots.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
