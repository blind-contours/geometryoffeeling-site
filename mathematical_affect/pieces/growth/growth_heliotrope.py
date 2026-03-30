"""
Geometry of Feeling — Growth: Heliotrope
Fifty-five stems curving toward an unseen light source —
phototropism rendered as continuous arcs. Each stem bends
at a rate proportional to its distance from the light.
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
    rng = np.random.default_rng(77)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    bg_rgb = hex_to_rgb01(BG_COLOR)

    # Palette: dark root → forest → spring → gold tip
    palette_hex = ['#2E1A0E', '#1A3A1A', '#2D5A2D', '#3A6B3A',
                   '#4A7C4A', '#6BAF4A', '#8BC362', '#C89028', '#D8C878']
    palette = [blend(hex_to_rgb01(h), bg_rgb, 0.04) for h in palette_hex]

    # Light source above center
    light = np.array([0.50, 1.25])

    n_stems = 55
    base_positions = np.linspace(0.06, 0.94, n_stems)

    for i in range(n_stems):
        base_x = base_positions[i] + rng.normal(0, 0.008)
        base_y = 0.04 + rng.uniform(0, 0.03)

        # Stem properties
        max_height = rng.uniform(0.55, 0.88)
        tropism_strength = 0.025 + 0.015 * rng.random()
        stem_wobble = rng.uniform(0.003, 0.008)

        # Grow stem step by step
        pos = np.array([base_x, base_y])
        direction = np.array([rng.normal(0, 0.03), 1.0])
        direction /= np.linalg.norm(direction)

        step_size = 0.003
        n_steps = int(max_height / step_size)
        xs = np.zeros(n_steps)
        ys = np.zeros(n_steps)

        for s in range(n_steps):
            xs[s], ys[s] = pos

            # Phototropism: bend toward light
            to_light = light - pos
            to_light /= np.linalg.norm(to_light) + 1e-12
            direction += tropism_strength * to_light
            # Small random wobble
            direction += rng.normal(0, stem_wobble, 2)
            direction /= np.linalg.norm(direction) + 1e-12

            pos = pos + step_size * direction

            if pos[1] > 0.96:
                xs = xs[:s + 1]
                ys = ys[:s + 1]
                break

        # Color: based on position (outer stems = warmer)
        u_pos = abs(base_x - 0.50) / 0.48
        u_color = 0.10 + 0.80 * u_pos
        color = interpolate_palette(palette, u_color)

        # Width: thicker at base, thinner at tip
        lw = 0.6 + 1.0 * (1 - abs(base_x - 0.50) / 0.50) ** 0.5
        alpha = 0.55 + 0.35 * (1 - u_pos ** 0.8)

        ax.plot(xs, ys, color=(*color, alpha), lw=lw, solid_capstyle='round')

    # Equation label
    ax.text(0.06, 0.06, "d\u03b8/ds=\u03ba\u00b7sin(\u03b1\u2212\u03b8)",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_heliotrope.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
