"""
Geometry of Feeling — Shame: Damped Radiance
A bold warm radial pattern hidden behind a curtain of fine lines.

The radiant self — concentric rose curves in crimson and blush —
lives behind a dense screen of horizontal veil lines that almost
hide it. The warmth bleeds through the gaps.

Damped radiance: I(r,theta) = I_0 * exp(-gamma*r) * cos(n*theta + alpha*r)
Modulated by line-screen transfer function T(y) = 0.5 + 0.5*sign(sin(2*pi*y/spacing))
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#DDD9D2'

# Warm palette — the radiant self
CRIMSON = '#8B2020'
ROSE = '#9E5060'
BLUSH = '#B87080'
DUSTY_PINK = '#C08890'
DEEP_ROSE = '#A03848'
WARM_CORAL = '#B06068'

# Veil color — close to BG but slightly darker/cooler
VEIL_COLOR = '#C5C1BA'
VEIL_DARK = '#BAB6AE'


def hex_to_rgba(h, a):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    return (r, g, b, float(np.clip(a, 0, 1)))


def render():
    np.random.seed(42)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    cx, cy = 0.5, 0.5

    # ===================================================================
    # LAYER 1: THE RADIANT SELF
    # Concentric/spiral rose curves in warm crimson/blush/rose tones
    # Bold, beautiful, alive — what shame tries to hide
    # ===================================================================

    warm_colors = [CRIMSON, DEEP_ROSE, ROSE, WARM_CORAL, BLUSH, DUSTY_PINK]
    n_radial = 45  # number of concentric/spiral curves

    for i in range(n_radial):
        frac = i / (n_radial - 1)

        # Radius for this curve — from tight center to filling most of canvas
        r_base = 0.02 + 0.42 * frac

        # Rose curve parameters — vary petal count and spiral twist
        n_petals = np.random.choice([3, 4, 5, 6, 7, 8])
        alpha_twist = np.random.uniform(0.5, 3.0)  # spiral twist factor
        phase = np.random.uniform(0, 2 * np.pi)

        # Damped radiance equation: I(r,theta) = I_0 * exp(-gamma*r) * cos(n*theta + alpha*r)
        gamma = np.random.uniform(0.8, 2.5)

        theta = np.linspace(0, 2 * np.pi, 800)

        # Rose-curve radius modulated by damped radiance
        r_mod = r_base * np.exp(-gamma * frac) * (0.5 + 0.5 * np.cos(n_petals * theta + alpha_twist * r_base * 10))
        # Add some baseline radius so curves don't collapse to zero
        r = 0.03 + r_base * 0.6 + r_mod * 0.5

        # Convert polar to cartesian (canvas is 0-1 on both axes)
        x = cx + r * np.cos(theta + phase)
        y = cy + r * np.sin(theta + phase)

        # Color selection — inner curves more crimson, outer more blush
        if frac < 0.25:
            col_choices = [CRIMSON, DEEP_ROSE]
        elif frac < 0.55:
            col_choices = [DEEP_ROSE, ROSE, WARM_CORAL]
        else:
            col_choices = [BLUSH, DUSTY_PINK, WARM_CORAL]
        col = col_choices[i % len(col_choices)]

        # Line weight and alpha — bolder in the center, softer at edges
        lw = 1.5 - 0.7 * frac  # 1.5 to 0.8
        alpha = 0.80 - 0.30 * frac  # 0.80 to 0.50

        ax.plot(x, y, color=hex_to_rgba(col, alpha), lw=lw,
                solid_capstyle="round", zorder=2)

    # Add some additional spiral arcs for richness
    for i in range(15):
        theta = np.linspace(0, np.pi * np.random.uniform(1.5, 4.0), 600)
        r_start = np.random.uniform(0.03, 0.10)
        r_growth = np.random.uniform(0.04, 0.10)
        r = r_start + r_growth * theta / (2 * np.pi)
        phase = np.random.uniform(0, 2 * np.pi)

        x = cx + r * np.cos(theta + phase)
        y = cy + r * np.sin(theta + phase)

        col = np.random.choice(warm_colors)
        alpha = np.random.uniform(0.45, 0.70)
        lw = np.random.uniform(0.8, 1.3)

        ax.plot(x, y, color=hex_to_rgba(col, alpha), lw=lw,
                solid_capstyle="round", zorder=2)

    # ===================================================================
    # LAYER 2: THE VEIL
    # Dense screen of fine horizontal lines — like a curtain or
    # venetian blinds. Partially obscures the radiant pattern.
    # The warmth bleeds through the gaps between lines.
    # ===================================================================

    n_veil_lines = 160
    y_positions = np.linspace(0.0, 1.0, n_veil_lines)

    for i, y_pos in enumerate(y_positions):
        # Slight variation in y position for organic feel
        y_jitter = np.random.uniform(-0.0008, 0.0008)
        y_line = y_pos + y_jitter

        x_line = np.array([0.0, 1.0])
        y_line_arr = np.array([y_line, y_line])

        # Veil line properties — thick enough to partially obscure
        # Alternate slightly between two veil tones for texture
        if i % 3 == 0:
            col = VEIL_DARK
        else:
            col = VEIL_COLOR

        # Alpha varies slightly — denser in center where radiance is strongest
        dist_from_center = abs(y_pos - 0.5) / 0.5
        center_boost = 0.08 * np.exp(-dist_from_center ** 2 / 0.3)
        alpha = 0.58 + center_boost + np.random.uniform(-0.03, 0.03)
        alpha = np.clip(alpha, 0.55, 0.70)

        # Line weight — slightly thicker toward center
        lw = 2.0 + 0.4 * np.exp(-dist_from_center ** 2 / 0.4)
        lw += np.random.uniform(-0.15, 0.15)
        lw = np.clip(lw, 1.5, 2.5)

        ax.plot(x_line, y_line_arr, color=hex_to_rgba(col, alpha), lw=lw,
                solid_capstyle="butt", zorder=3)

    # ===================================================================
    # Equation label
    # ===================================================================
    ax.text(0.06, 0.06, "I(r)=I\u2080\u00b7exp(\u2212\u03b3r)\u00b7T(y)",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    # ===================================================================
    # Save
    # ===================================================================
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "shame_veil.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
