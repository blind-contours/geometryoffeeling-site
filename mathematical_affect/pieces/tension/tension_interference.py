"""
Geometry of Feeling — Tension: Tension Interference
2D Interference Field — two point sources emitting concentric circular waves.
Constructive interference zones are bright and bold; destructive zones fade away.
Classic physics interference pattern evoking two forces in tension.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import os


DPI    = 300
FIG_W  = 12
FIG_H  = 8

BG = "#0A0A12"

# Warm constructive colors
BRIGHT_RED   = "#E04030"
AMBER        = "#E89030"
HOT_WHITE    = "#F0D8C0"

# Cool neutral / destructive colors
TEAL         = "#206880"
COOL_BLUE    = "#1A3050"

# Source glow colors
SOURCE_A_CLR = "#E04030"   # red-orange
SOURCE_B_CLR = "#3080C0"   # contrasting blue

PAD_L = 0.65; PAD_R = 0.55; PAD_T = 0.60; PAD_B = 0.85
PW = FIG_W - PAD_L - PAD_R
PH = FIG_H - PAD_T  - PAD_B
cx = PAD_L + PW / 2
cy = PAD_B + PH / 2


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))


def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax  = fig.add_subplot(111)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def label(ax, eq):
    ax.text(0.75, 0.75, eq, fontfamily='monospace', fontsize=10,
            color=(1, 1, 1, 0.20), transform=ax.transData)


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


# =============================================================================
# INTERFERENCE — 2D interference field from two point sources
#   amplitude(x,y) = sin(k * d1) + sin(k * d2)
#   where d1, d2 are distances from each source
# =============================================================================
def render():
    fig, ax = make_fig()

    # --- Source positions: horizontally separated, centered vertically ---
    separation = PW * 0.40
    src_a = (cx - separation / 2, cy)
    src_b = (cx + separation / 2, cy)

    # Wave parameters
    wavelength = 0.55            # spatial wavelength in figure units
    k = 2 * np.pi / wavelength   # wave number
    n_scan_lines = 70            # horizontal scan lines
    n_pts = 2000                 # points per scan line

    # Precompute color arrays
    bright_red_rgb = np.array(hex_to_rgb(BRIGHT_RED))
    amber_rgb      = np.array(hex_to_rgb(AMBER))
    hot_white_rgb  = np.array(hex_to_rgb(HOT_WHITE))
    teal_rgb       = np.array(hex_to_rgb(TEAL))
    cool_blue_rgb  = np.array(hex_to_rgb(COOL_BLUE))

    # --- Vertical extent: fill the canvas well ---
    y_margin = 0.25
    y_min = PAD_B + y_margin
    y_max = PAD_B + PH - y_margin
    x_min = PAD_L + 0.10
    x_max = PAD_L + PW - 0.10

    y_lines = np.linspace(y_min, y_max, n_scan_lines)

    for y_val in y_lines:
        x_arr = np.linspace(x_min, x_max, n_pts)

        # Distances from each source
        d1 = np.sqrt((x_arr - src_a[0])**2 + (y_val - src_a[1])**2)
        d2 = np.sqrt((x_arr - src_b[0])**2 + (y_val - src_b[1])**2)

        # Wave amplitudes from each source (with 1/sqrt(r) decay)
        decay1 = 1.0 / np.sqrt(np.maximum(d1, 0.05))
        decay2 = 1.0 / np.sqrt(np.maximum(d2, 0.05))
        wave1 = decay1 * np.sin(k * d1)
        wave2 = decay2 * np.sin(k * d2)

        # Combined interference amplitude
        combined = wave1 + wave2

        # Normalize to [-1, 1] range for color/alpha mapping
        max_possible = np.max(np.abs(combined))
        if max_possible > 0:
            norm_combined = combined / max_possible
        else:
            norm_combined = combined

        # --- Build per-segment colors and linewidths ---
        # Constructive (|amplitude| high) -> bright warm colors, thick lines
        # Destructive (|amplitude| low) -> faint cool colors, thin lines
        intensity = np.abs(norm_combined)  # 0 = destructive, 1 = constructive

        # Smooth the intensity slightly for aesthetic transitions
        kernel_size = 15
        kernel = np.ones(kernel_size) / kernel_size
        intensity_smooth = np.convolve(intensity, kernel, mode='same')

        # Color mapping: interpolate between cool (destructive) and warm (constructive)
        # Also encode sign: positive combined -> red/amber, negative -> slightly shifted
        n_segs = n_pts - 1
        colors = np.zeros((n_segs, 4))
        widths = np.zeros(n_segs)

        for i in range(n_segs):
            t = intensity_smooth[i]  # 0..1
            t = np.clip(t, 0, 1)

            # Sign gives warm vs slightly cooler warm
            sign_val = norm_combined[i]

            if t < 0.25:
                # Destructive zone: cool blue/teal, very faint
                base_color = cool_blue_rgb * (1 - t*2) + teal_rgb * (t*2)
                alpha = 0.03 + 0.08 * t
                lw = 0.3 + 0.4 * t
            elif t < 0.55:
                # Transition zone: teal to warm
                u = (t - 0.25) / 0.30
                base_color = teal_rgb * (1 - u) + bright_red_rgb * u
                alpha = 0.10 + 0.30 * u
                lw = 0.6 + 0.8 * u
            else:
                # Constructive zone: bright warm, bold
                u = (t - 0.55) / 0.45
                u = np.clip(u, 0, 1)
                if sign_val > 0:
                    base_color = bright_red_rgb * (1 - u*0.5) + amber_rgb * (u*0.5)
                else:
                    base_color = bright_red_rgb * (1 - u*0.4) + hot_white_rgb * (u*0.4)
                alpha = 0.40 + 0.50 * u
                lw = 1.2 + 1.5 * u

            colors[i, :3] = np.clip(base_color, 0, 1)
            colors[i, 3] = np.clip(alpha, 0, 1)
            widths[i] = lw

        # Build line segments
        pts = np.column_stack([x_arr, np.full_like(x_arr, y_val)])
        pts = pts.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)

        lc = mc.LineCollection(segs, linewidths=widths, colors=colors,
                               capstyle='round', joinstyle='round', zorder=3)
        ax.add_collection(lc)

    # --- Draw concentric ring hints from each source ---
    # Faint concentric circles to reinforce the wave-source concept
    max_radius = np.sqrt(PW**2 + PH**2)
    n_rings = int(max_radius / wavelength) + 1

    for src, clr in [(src_a, SOURCE_A_CLR), (src_b, SOURCE_B_CLR)]:
        for ring_i in range(1, n_rings):
            r = ring_i * wavelength
            theta = np.linspace(0, 2 * np.pi, 300)
            rx = src[0] + r * np.cos(theta)
            ry = src[1] + r * np.sin(theta)

            # Clip to visible area
            visible = (rx >= x_min) & (rx <= x_max) & (ry >= y_min) & (ry <= y_max)
            if not np.any(visible):
                continue

            # Alpha fades with distance
            alpha = 0.06 * np.exp(-0.15 * ring_i)
            if alpha < 0.005:
                continue

            # Draw only visible segments
            pts_r = np.column_stack([rx, ry]).reshape(-1, 1, 2)
            segs_r = np.concatenate([pts_r[:-1], pts_r[1:]], axis=1)

            # Mask for visible segments
            vis_segs = visible[:-1] & visible[1:]
            if np.any(vis_segs):
                lc_r = mc.LineCollection(segs_r[vis_segs],
                                         linewidths=0.4,
                                         colors=[rgba(clr, alpha)],
                                         capstyle='round', zorder=2)
                ax.add_collection(lc_r)

    # --- Source point glows ---
    for src, clr in [(src_a, SOURCE_A_CLR), (src_b, SOURCE_B_CLR)]:
        # Layered glow effect
        for r, a in [(0.25, 0.04), (0.15, 0.08), (0.08, 0.15), (0.04, 0.30)]:
            circle = plt.Circle(src, r, color=rgba(clr, a),
                                linewidth=0, zorder=9)
            ax.add_patch(circle)
        # Bright center dot
        ax.plot(src[0], src[1], 'o', color=rgba(clr, 0.90),
                markersize=4, markeredgewidth=0, zorder=10)

    label(ax, "A(x,y) = sin(k\u00b7d\u2081) + sin(k\u00b7d\u2082)")
    save(fig, "tension_interference")


if __name__ == '__main__':
    render()
