"""
Geometry of Feeling — Growth: Bloom
A flower opening — concentric layers of petals unfurling from
a tight center. Each petal is a parametric curve whose opening
angle increases with ring number. The culmination of growth.
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
    rng = np.random.default_rng(33)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    bg_rgb = hex_to_rgb01(BG_COLOR)
    aspect = 8.0 / 12.0  # y/x on canvas

    # Palette: tight center (dark green) → mid petals → outer petals (warm)
    palette_hex = ['#1A3A1A', '#2D5A2D', '#3A6B3A', '#4A7C4A',
                   '#6BAF4A', '#8BC362', '#C89028', '#D4A832',
                   '#C86848', '#D8C878']
    palette = [blend(hex_to_rgb01(h), bg_rgb, 0.04) for h in palette_hex]

    cx, cy = 0.50, 0.48

    # --- Stem ---
    stem_t = np.linspace(0, 1, 100)
    stem_x = cx + 0.006 * np.sin(2 * np.pi * stem_t)
    stem_y = 0.02 + 0.46 * stem_t
    stem_color = interpolate_palette(palette, 0.15)
    ax.plot(stem_x, stem_y, color=(*stem_color, 0.75), lw=2.0, solid_capstyle='round')

    # --- Petal rings ---
    n_rings = 12
    for ring in range(n_rings):
        ring_frac = ring / (n_rings - 1)

        # Inner rings: tight, many small petals
        # Outer rings: open, fewer large petals
        n_petals = 13 - ring  # 13 inner → 2 outer
        if n_petals < 3:
            n_petals = 3

        base_radius = 0.02 + 0.30 * ring_frac ** 0.75
        petal_length = 0.04 + 0.18 * ring_frac ** 0.6
        opening = 0.15 + 0.85 * ring_frac  # how wide petals open

        # Golden angle offset between rings
        ring_offset = ring * 137.508 * np.pi / 180

        for j in range(n_petals):
            theta0 = ring_offset + j * (2 * np.pi / n_petals)
            theta0 += rng.normal(0, 0.08)

            # Petal as parametric curve
            t = np.linspace(0, 1, 80)

            # Petal shape: starts at base, curves outward, then curves back
            # Creates a teardrop/petal shape
            r = base_radius + petal_length * t * (1 - 0.3 * t)
            # Petal opening: wider at tip
            spread = opening * 0.15 * np.sin(np.pi * t) * (0.5 + 0.5 * t)

            angle = theta0 + spread * rng.choice([-1, 1])

            # Add slight asymmetry
            angle += 0.03 * np.sin(3 * np.pi * t + rng.uniform(0, 6))

            px = cx + r * np.cos(angle) * aspect
            py = cy + r * np.sin(angle)

            # Color from ring
            color = interpolate_palette(palette, ring_frac)
            lw = 0.4 + 1.2 * ring_frac ** 0.4
            alpha = 0.50 + 0.40 * (1 - ring_frac * 0.3)

            ax.plot(px, py, color=(*color, alpha), lw=lw, solid_capstyle='round')

    # --- Small leaves on stem ---
    for leaf_y in [0.18, 0.30]:
        for side in [-1, 1]:
            lt = np.linspace(0, 1, 40)
            leaf_len = 0.08
            leaf_angle = side * 0.7 + 0.15
            lx = cx + side * leaf_len * lt * np.cos(leaf_angle) * aspect
            ly = leaf_y + leaf_len * lt * np.sin(leaf_angle) * (1 - 0.4 * lt)
            leaf_color = interpolate_palette(palette, 0.25)
            ax.plot(lx, ly, color=(*leaf_color, 0.55), lw=0.7, solid_capstyle='round')

    # Equation label
    ax.text(0.06, 0.06, "r(\u03b8)=a\u00b7cos(k\u03b8)",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_bloom.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
