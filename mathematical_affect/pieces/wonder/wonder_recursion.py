"""
Geometry of Feeling — Wonder: Fractal Horizon
Recursive midpoint displacement rendered as landscape ridgelines
receding into atmospheric depth.
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


def midpoint_displacement(x0, y0, x1, y1, depth, roughness, H, rng):
    """Recursive midpoint displacement fractal.

    Parameters
    ----------
    x0, y0 : float  — left endpoint
    x1, y1 : float  — right endpoint
    depth  : int     — recursion levels remaining
    roughness : float — amplitude scaling factor
    H : float        — Hurst exponent (0 < H < 1)
    rng : np.random.Generator

    Returns
    -------
    xs, ys : np.ndarray — sorted arrays of fractal points
    """
    if depth == 0:
        return np.array([x0, x1]), np.array([y0, y1])

    mx = (x0 + x1) / 2.0
    seg_len = x1 - x0
    # displacement scaled by roughness * segment_length^H
    displacement = rng.uniform(-1, 1) * roughness * (seg_len ** H)
    my = (y0 + y1) / 2.0 + displacement

    # recurse on both halves
    xs_left, ys_left = midpoint_displacement(x0, y0, mx, my, depth - 1,
                                             roughness, H, rng)
    xs_right, ys_right = midpoint_displacement(mx, my, x1, y1, depth - 1,
                                               roughness, H, rng)

    # merge (skip duplicate midpoint)
    xs = np.concatenate([xs_left, xs_right[1:]])
    ys = np.concatenate([ys_left, ys_right[1:]])
    return xs, ys


def render():
    rng = np.random.default_rng(42)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI,
                           facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ---- ridgeline configuration ----
    n_ridges = 10
    # base_y goes from bottom (front) to top (back)
    base_ys = np.linspace(0.22, 0.82, n_ridges)

    # color palette: front (deep navy) -> middle (blue-grey) -> back (pale mauve)
    color_anchors_t = np.array([0.0, 0.25, 0.5, 0.7, 0.85, 1.0])
    color_anchors_rgb = np.array([
        [0x2E, 0x42, 0x5E],   # deep navy
        [0x35, 0x4A, 0x65],   # dark steel
        [0x55, 0x64, 0x78],   # blue-grey
        [0x6A, 0x70, 0x88],   # mid grey-blue
        [0x90, 0x7C, 0x8E],   # pale mauve
        [0xB0, 0xA0, 0xA8],   # faint lilac
    ], dtype=float) / 255.0

    x_left = 0.07
    x_right = 0.93

    H = 0.6  # Hurst exponent

    for i, base_y in enumerate(base_ys):
        # t=0 is front (bottom), t=1 is back (top)
        t = i / (n_ridges - 1)

        # ---- recursion parameters ----
        # front: 10 levels, back: 5 levels
        depth = int(round(10 - 5 * t))
        # roughness: front 0.55, back 0.35
        roughness = 0.55 - 0.20 * t
        # displacement amplitude: front large, back small
        amplitude = 0.12 * (1.0 - 0.70 * t)

        # ---- generate fractal ridgeline ----
        xs, ys = midpoint_displacement(x_left, 0.0, x_right, 0.0,
                                       depth, roughness, H, rng)
        # scale displacements and shift to base height
        ys = ys * (amplitude / max(abs(ys.max()), abs(ys.min()), 1e-9))
        ys = ys + base_y

        # ---- atmospheric attenuation ----
        # alpha: front 0.92, back 0.18
        alpha = 0.92 * np.exp(-2.2 * t)
        alpha = max(alpha, 0.18)

        # fill alpha: subtle layered depth
        fill_alpha = 0.08 * (1.0 - 0.7 * t)
        fill_alpha = max(fill_alpha, 0.03)

        # ---- line weight ----
        lw = 1.4 - 1.0 * t
        lw = max(lw, 0.35)

        # ---- color interpolation ----
        r = np.interp(t, color_anchors_t, color_anchors_rgb[:, 0])
        g = np.interp(t, color_anchors_t, color_anchors_rgb[:, 1])
        b = np.interp(t, color_anchors_t, color_anchors_rgb[:, 2])
        line_color = (r, g, b, alpha)
        fill_color = (r, g, b, fill_alpha)

        # ---- draw filled region below ridgeline ----
        # fill down to the bottom of the canvas
        ax.fill_between(xs, ys, 0.10, color=fill_color, zorder=2 + i,
                        linewidth=0)

        # ---- draw ridgeline ----
        ax.plot(xs, ys, color=line_color, lw=lw, solid_capstyle="round",
                zorder=12 + i)

    # ---- equation label ----
    ax.text(0.06, 0.06,
            "H(x)=\u03A3\u03B4\u1D62\u00B72^(\u2212iH), H\u2208(0,1)",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25),
            transform=ax.transAxes)

    # ---- save ----
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "wonder_recursion.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
