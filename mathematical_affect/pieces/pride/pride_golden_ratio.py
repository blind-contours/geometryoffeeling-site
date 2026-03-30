"""
Geometry of Feeling — Pride: Pride Golden Ratio
Standalone render script

Golden Angle Sunflower Pattern — petals placed using the golden angle (137.508deg)
in a Fibonacci/sunflower spiral. Pride colors radiate outward from center.
Subtle golden spiral overlays connect the pattern to phi visually.
"""

import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#f3eee7"

# Full LGBTQ+ spectrum — rainbow + trans colors woven in
PRIDE_RED    = "#E40303"
PRIDE_ORANGE = "#FF8C00"
PRIDE_YELLOW = "#FFED00"
PRIDE_GREEN  = "#008026"
PRIDE_BLUE   = "#004DFF"
PRIDE_VIOLET = "#750787"

# Trans flag colors
TRANS_PINK   = "#F5A9B8"
TRANS_BLUE   = "#5BCEFA"
TRANS_WHITE  = "#FFFFFF"

# Interleaved: trans pink → red → orange → trans blue → yellow → trans white →
#              green → trans pink → blue → violet → trans blue
PRIDE_COLORS = [TRANS_PINK, PRIDE_RED, PRIDE_ORANGE, TRANS_BLUE,
                PRIDE_YELLOW, TRANS_WHITE, PRIDE_GREEN, TRANS_PINK,
                PRIDE_BLUE, PRIDE_VIOLET, TRANS_BLUE]

# Golden angle in radians
GOLDEN_ANGLE = np.pi * (3 - np.sqrt(5))  # ~137.508 degrees

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def lerp_color(c1_hex, c2_hex, t):
    """Linearly interpolate between two hex colors."""
    c1 = hex_to_rgb(c1_hex)
    c2 = hex_to_rgb(c2_hex)
    return tuple(c1[i] + (c2[i] - c1[i]) * t for i in range(3))

def pride_color_at_radius(frac):
    """Map a 0-1 fraction to a pride color, smoothly interpolating across the 6 stripes."""
    frac = np.clip(frac, 0, 0.999)
    n = len(PRIDE_COLORS)
    scaled = frac * (n - 1)
    idx = int(scaled)
    t = scaled - idx
    if idx >= n - 1:
        return hex_to_rgb(PRIDE_COLORS[-1])
    c1 = hex_to_rgb(PRIDE_COLORS[idx])
    c2 = hex_to_rgb(PRIDE_COLORS[idx + 1])
    return tuple(c1[i] + (c2[i] - c1[i]) * t for i in range(3))

def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    return fig, ax

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2; cy = PAD_B + PH / 2

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def render():
    fig, ax = make_fig()
    phi = (1 + np.sqrt(5)) / 2

    # =========================================================================
    # 1. SUNFLOWER PETAL PATTERN — golden angle placement
    # =========================================================================
    n_petals = 350
    max_radius = PH * 0.46  # slightly larger bloom

    for i in range(1, n_petals + 1):
        # Golden angle positioning
        r = max_radius * np.sqrt(i / n_petals)
        theta = i * GOLDEN_ANGLE

        # Position
        x = cx + r * np.cos(theta)
        y = cy + r * np.sin(theta)

        # Skip if out of bounds
        if x < PAD_L or x > PAD_L + PW or y < PAD_B or y > PAD_B + PH:
            continue

        # Radius fraction for color mapping (0=center, 1=edge)
        frac = np.sqrt(i / n_petals)

        # Petal size — bolder, more flower-like; larger dots that overlap slightly
        base_size = 0.07 + 0.10 * frac
        # Subtle variation for organic feel
        size_var = 1.0 + 0.15 * np.sin(i * 0.618)
        petal_r = base_size * size_var

        # Color from pride palette based on radial position
        rgb = pride_color_at_radius(frac)

        # Draw concentric rings for each petal — bolder, more opaque
        n_rings = 4
        for ring in range(n_rings):
            ring_frac = ring / (n_rings - 1)
            ring_r = petal_r * (1.0 - ring_frac * 0.65)
            # Bolder alpha — more saturated, more present
            alpha = 0.15 + 0.70 * (1.0 - ring_frac)
            # Slight color brightening toward center of each petal
            brighten = 1.0 + 0.25 * (1.0 - ring_frac)
            bright_rgb = tuple(min(1.0, c * brighten) for c in rgb)

            circle = Circle((x, y), ring_r,
                           facecolor=(*bright_rgb, alpha),
                           edgecolor='none',
                           zorder=3 + ring)
            ax.add_patch(circle)

    # =========================================================================
    # 2. GOLDEN SPIRAL OVERLAYS — subtle phi-based spirals tracing through
    # =========================================================================
    n_overlay_spirals = 3
    spiral_configs = [
        {'a': 0.015, 'rotation': 0,           'color': PRIDE_VIOLET, 'alpha': 0.12, 'lw': 0.6},
        {'a': 0.012, 'rotation': np.pi * 0.5, 'color': TRANS_BLUE,   'alpha': 0.10, 'lw': 0.5},
        {'a': 0.018, 'rotation': np.pi * 1.0, 'color': TRANS_PINK,   'alpha': 0.10, 'lw': 0.5},
    ]

    for cfg in spiral_configs:
        theta_sp = np.linspace(0, 4.5 * np.pi, 3000)
        a = PW * cfg['a']
        r_sp = a * phi ** (2 * theta_sp / np.pi)

        xs = cx + r_sp * np.cos(theta_sp + cfg['rotation'])
        ys = cy + r_sp * np.sin(theta_sp + cfg['rotation'])

        # Mask to canvas bounds
        mask = ((xs > PAD_L) & (xs < PAD_L + PW) &
                (ys > PAD_B) & (ys < PAD_B + PH))

        # Split into contiguous segments to avoid straight-line jumps
        segments = []
        in_seg = False
        start = 0
        for j in range(len(mask)):
            if mask[j] and not in_seg:
                start = j; in_seg = True
            elif not mask[j] and in_seg:
                if j - start >= 3:
                    segments.append((xs[start:j], ys[start:j]))
                in_seg = False
        if in_seg and len(mask) - start >= 3:
            segments.append((xs[start:], ys[start:]))

        col_rgba = rgba(cfg['color'], cfg['alpha'])
        for seg_xs, seg_ys in segments:
            pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            lc = mc.LineCollection(segs, linewidths=cfg['lw'],
                                   colors=[col_rgba],
                                   capstyle='round', joinstyle='round',
                                   zorder=8)
            ax.add_collection(lc)

    # =========================================================================
    # 3. SOFT CENTER GLOW — warm radial highlight at the heart
    # =========================================================================
    for glow_r, glow_a in [(1.8, 0.03), (1.2, 0.05), (0.6, 0.07)]:
        glow = Circle((cx, cy), glow_r,
                      facecolor=(0.95, 0.75, 0.80, glow_a),
                      edgecolor='none', zorder=1)
        ax.add_patch(glow)

    # =========================================================================
    # 4. EQUATION LABEL
    # =========================================================================

    add_signature(fig, ax, BG)
    save(fig, "pride_golden_ratio")

if __name__ == '__main__':
    render()
