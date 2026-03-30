"""
Geometry of Feeling — Growth: Meridian
Fifty-five logistic-growth stems rising from a shared baseline.
Each one accelerates, plateaus, and reaches a different height —
a meadow of sigmoidal curves drifting in a slow wind.
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


def fbm(t, octaves=4, seed=0):
    """Fractional Brownian motion for organic drift."""
    rng = np.random.default_rng(seed)
    result = np.zeros_like(t)
    amp = 1.0
    freq = 1.0
    for _ in range(octaves):
        phase = rng.uniform(0, 2 * np.pi)
        result += amp * np.sin(freq * 2 * np.pi * t + phase)
        amp *= 0.5
        freq *= 2.0
    return result


def render():
    rng = np.random.default_rng(101)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    bg_rgb = hex_to_rgb01(BG_COLOR)

    # Palette: root → stem → leaf → tip
    palette_hex = ['#2E1A0E', '#3D2B1F', '#1A3A1A', '#2D5A2D',
                   '#4A7C4A', '#6BAF4A', '#8BC362', '#A8C890']
    palette = [blend(hex_to_rgb01(h), bg_rgb, 0.05) for h in palette_hex]

    n_stems = 55
    s = np.linspace(0, 1, 800)

    for i in range(n_stems):
        u = i / (n_stems - 1)

        # Base position
        base_x = 0.06 + 0.88 * u
        base_y = 0.04 + rng.uniform(0, 0.03)

        # Height: taller in center, shorter at edges
        center_dist = abs(u - 0.50) / 0.50
        max_height = 0.88 - 0.30 * center_dist ** 0.8 + rng.uniform(-0.08, 0.08)
        max_height = np.clip(max_height, 0.35, 0.92)

        # Logistic growth curve: y = base + height * sigmoid(s)
        # Sigmoid with varying steepness
        steepness = rng.uniform(5.0, 9.0)
        midpoint = rng.uniform(0.35, 0.55)
        sigmoid = 1.0 / (1.0 + np.exp(-steepness * (s - midpoint)))

        y = base_y + max_height * sigmoid * s ** 0.15

        # Horizontal drift: fBm for organic sway
        drift_amp = 0.020 + 0.015 * rng.random()
        drift = drift_amp * fbm(s, octaves=4, seed=rng.integers(0, 100000))
        # Stems lean slightly from center
        lean = 0.04 * (u - 0.50) * s ** 1.5

        x = base_x + drift * s ** 0.7 + lean

        # Color from position
        color_u = 0.08 + 0.84 * (0.5 - 0.5 * np.cos(np.pi * u))
        color = interpolate_palette(palette, color_u)

        # Width and alpha
        lw = 0.5 + 0.9 * (1 - center_dist) ** 0.5
        alpha = 0.45 + 0.45 * (1 - center_dist * 0.5)

        ax.plot(x, y, color=(*color, alpha), lw=lw, solid_capstyle='round')

    # Equation label
    ax.text(0.06, 0.06, "dN/dt=rN(1\u2212N/K)",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_meridian.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
