"""
Geometry of Feeling -- Solitude: Solitude Beacon (Water Variant)
Standalone render script

Concept: Water droplets on a still water surface, viewed from above.
One isolated droplet (the beacon) creates bold ripples at top-right.
A crowd of smaller droplets scatter across the bottom-left quadrant.
Each droplet creates independent concentric circular ripples.
Physics: amplitude ~ 1/sqrt(r), constant wavelength, superposition.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle
import os


DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#E0DDD6"

# Palette
BLUE_BOLD = "#3A6A9A"
BLUE_MED = "#4A7AAA"
BLUE_LIGHT = "#5A8ABB"
GOLD_CENTER = "#D4A840"
GOLD_WARM = "#C8963A"
DOT_DARK = "#2A3A4A"


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))


def lerp_color(c1_hex, c2_hex, t):
    """Linearly interpolate between two hex colors."""
    r1, g1, b1 = hex_to_rgb(c1_hex)
    r2, g2, b2 = hex_to_rgb(c2_hex)
    t = np.clip(t, 0, 1)
    return (r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t)


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


def label(ax, eq):
    ax.text(0.75, 0.75, eq, fontfamily='monospace', fontsize=10,
            color=(0.25, 0.28, 0.30, 0.25), transform=ax.transData)


def draw_lc(ax, xs, ys, col, lw, alpha, zo=4):
    """Draw a line collection from x,y arrays with given color, linewidth, alpha."""
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    if isinstance(col, str):
        color = rgba(col, alpha)
    else:
        # col is an (r,g,b) tuple
        color = (col[0], col[1], col[2], float(np.clip(alpha, 0, 1)))
    lc = mc.LineCollection(segs, linewidths=lw, colors=[color],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")


def draw_ripple(ax, droplet_x, droplet_y, n_rings, max_r,
                ring_color_inner, ring_color_outer,
                ring_alpha_start=0.50, lw_start=1.2,
                center_color=None, center_alpha=0.50, center_r_factor=0.04,
                zo_base=5):
    """Draw a water droplet impact as concentric circular ripples.

    Physics:
    - Evenly spaced rings (constant wavelength)
    - Amplitude decays as 1/sqrt(r) (energy conservation in 2D)
    - Perfect circles (no wobble -- viewed from above)
    """
    theta = np.linspace(0, 2 * np.pi, 500)

    # Center dot(s)
    if center_color is not None:
        # Glow layers for center
        for r_g, a_g in [(max_r * center_r_factor * 2.5, center_alpha * 0.25),
                         (max_r * center_r_factor * 1.5, center_alpha * 0.50),
                         (max_r * center_r_factor, center_alpha)]:
            ax.add_patch(Circle((droplet_x, droplet_y), radius=r_g,
                        facecolor=rgba(center_color, a_g), edgecolor='none',
                        zorder=zo_base + 5))

    # Concentric ripple rings -- evenly spaced (constant wavelength)
    wavelength = max_r / max(n_rings, 1)

    for i in range(n_rings):
        r = wavelength * (i + 1)
        if r > max_r:
            break

        frac = r / max_r  # 0..1, distance fraction

        # Physics: amplitude ~ 1/sqrt(r)
        amplitude_decay = 1.0 / np.sqrt(1.0 + 3.0 * frac)

        alpha = ring_alpha_start * amplitude_decay
        lw = lw_start * amplitude_decay

        # Color: interpolate from inner to outer
        col = lerp_color(ring_color_inner, ring_color_outer, frac)

        # Perfect circles
        xs = droplet_x + r * np.cos(theta)
        ys = droplet_y + r * np.sin(theta)

        draw_lc(ax, xs, ys, col, lw=max(lw, 0.15), alpha=max(alpha, 0.02),
                zo=zo_base)


def render():
    fig, ax = make_fig()
    np.random.seed(42)

    # ================================================================
    # THE BEACON -- one large, prominent droplet at top-right
    # ================================================================
    beacon_x = cx + PW * 0.28
    beacon_y = cy + PH * 0.22
    beacon_max_r = min(PW, PH) * 0.33
    beacon_n_rings = 28

    # Gold/amber center glow (layered concentric filled circles)
    glow_r = beacon_max_r * 0.035
    for r_g, a_g in [(glow_r * 4.0, 0.06),
                     (glow_r * 3.0, 0.12),
                     (glow_r * 2.0, 0.25),
                     (glow_r * 1.3, 0.50),
                     (glow_r, 0.70)]:
        ax.add_patch(Circle((beacon_x, beacon_y), radius=r_g,
                    facecolor=rgba(GOLD_CENTER, a_g), edgecolor='none',
                    zorder=9))

    # Beacon ripple rings -- custom alpha curve for high contrast
    beacon_wavelength = beacon_max_r / beacon_n_rings
    theta = np.linspace(0, 2 * np.pi, 600)

    for i in range(beacon_n_rings):
        r = beacon_wavelength * (i + 1)
        if r > beacon_max_r:
            break

        frac = r / beacon_max_r

        # Color: start gold at very center, transition to blue, fade to grey-blue
        if frac < 0.07:
            col = lerp_color(GOLD_CENTER, GOLD_WARM, frac / 0.07)
        elif frac < 0.15:
            col = lerp_color(GOLD_WARM, BLUE_BOLD, (frac - 0.07) / 0.08)
        elif frac < 0.55:
            col = lerp_color(BLUE_BOLD, BLUE_MED, (frac - 0.15) / 0.40)
        else:
            col = lerp_color(BLUE_MED, "#8A9EAE", (frac - 0.55) / 0.45)

        # Alpha: strong inner, decaying outward
        # Inner rings (frac < 0.2): bold 0.55-0.70
        # Mid rings (0.2-0.5): solid 0.35-0.50
        # Outer rings (0.5-1.0): fading with physics decay
        if frac < 0.15:
            alpha = 0.65
        elif frac < 0.50:
            alpha = 0.50 * (1.0 / np.sqrt(1.0 + 2.0 * frac))
        else:
            decay = 1.0 / np.sqrt(1.0 + 3.5 * frac)
            alpha = 0.30 * decay

        # Linewidth: physics decay
        decay_lw = 1.0 / np.sqrt(1.0 + 3.0 * frac)
        lw = 1.4 * decay_lw

        # Perfect circles
        xs = beacon_x + r * np.cos(theta)
        ys = beacon_y + r * np.sin(theta)

        draw_lc(ax, xs, ys, col, lw=max(lw, 0.15), alpha=max(alpha, 0.02),
                zo=5 + max(0, int((1 - frac) * 3)))

    # ================================================================
    # THE CROWD -- 14 smaller droplets scattered across bottom-left
    # ================================================================
    # Wide spatial spread: use full bottom-left quadrant
    rng = np.random.RandomState(42)

    # Define crowd droplets with explicit positions for good spread
    # Mix of positions across the bottom-left area
    crowd_specs = [
        # (offset_x, offset_y, n_rings, size_factor)
        # Far left column
        (-0.40, -0.30, 6, 0.55),
        (-0.38, -0.05, 4, 0.35),
        (-0.42,  0.10, 3, 0.28),
        # Left-center column
        (-0.25, -0.35, 8, 0.70),
        (-0.22, -0.12, 5, 0.45),
        (-0.28,  0.05, 3, 0.30),
        # Center column (still in left half)
        (-0.08, -0.32, 7, 0.62),
        (-0.10, -0.15, 4, 0.38),
        (-0.05, -0.02, 3, 0.25),
        # Slightly right of center (but still left side)
        ( 0.02, -0.28, 6, 0.50),
        ( 0.05, -0.10, 4, 0.35),
        # Bottom row
        (-0.32, -0.38, 5, 0.42),
        (-0.15, -0.40, 3, 0.30),
        ( 0.00, -0.36, 4, 0.38),
    ]

    n_crowd = len(crowd_specs)

    for i, (off_x, off_y, n_rings, size_factor) in enumerate(crowd_specs):
        # Add small random jitter to prevent looking too grid-like
        jitter_x = rng.uniform(-0.02, 0.02) * PW
        jitter_y = rng.uniform(-0.02, 0.02) * PH

        px = cx + off_x * PW + jitter_x
        py = cy + off_y * PH + jitter_y

        # Clamp within canvas
        px = np.clip(px, PAD_L + 0.3, cx + PW * 0.10)
        py = np.clip(py, PAD_B + 0.2, cy + PH * 0.15)

        max_r = size_factor * min(PW, PH) * 0.12
        wavelength = max_r / max(n_rings, 1)

        # Draw ripple rings -- blue, individually readable
        for j in range(n_rings):
            r = wavelength * (j + 1)
            if r > max_r:
                break
            frac = r / max_r

            # Physics: 1/sqrt(r) energy decay
            decay = 1.0 / np.sqrt(1.0 + 2.5 * frac)

            # Alpha: 0.35-0.45 inner, fading outward
            alpha_base = 0.35 + 0.10 * (1.0 - i / n_crowd)  # slight variation per droplet
            alpha = alpha_base * decay
            if frac > 0.6:
                alpha *= (1.0 - 0.6 * (frac - 0.6) / 0.4)
            alpha = max(alpha, 0.06)

            # Linewidth
            lw = 0.9 * decay

            # Color: blue tones, interpolated
            col = lerp_color(BLUE_BOLD, BLUE_LIGHT, frac)

            xs = px + r * np.cos(theta)
            ys = py + r * np.sin(theta)

            draw_lc(ax, xs, ys, col, lw=max(lw, 0.15),
                    alpha=max(alpha, 0.04), zo=3)

        # Small dark center dot for each crowd droplet
        dot_r = max(max_r * 0.06, 0.025)
        ax.add_patch(Circle((px, py), radius=dot_r,
                    facecolor=rgba(DOT_DARK, 0.55), edgecolor='none',
                    zorder=6))

    # ================================================================
    # EQUATION LABEL
    # ================================================================
    label(ax, "A(r)=A\u2080/r\u00b2")
    save(fig, "solitude_beacon")


if __name__ == '__main__':
    render()
