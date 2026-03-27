"""
Geometry of Feeling — Cycles: Quasi-periodic Winding (Toroid)

A single continuous trajectory winding around a torus with golden-ratio
winding number phi = (1+sqrt(5))/2. The path never closes — it fills
the torus surface with dense, shimmering near-repeats. Rendered with
z-depth shading: closer segments are darker/bolder navy, farther segments
are lighter/thinner mauve-grey.

The irrationality of phi means eternal near-return — the essence of
cycles that almost repeat but never do.
"""

import colorsys
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#F0E8DA'


def render():
    # --- Golden ratio winding number ---
    phi = (1.0 + np.sqrt(5.0)) / 2.0

    # --- Torus geometry (in normalized [0,1] coords) ---
    R = 0.28        # major radius
    r = 0.14        # minor radius
    cx, cy = 0.5, 0.5   # center in normalized coords

    # Tilt angle: rotate torus around x-axis so we see into the hole
    tilt = np.radians(25.0)

    # --- Trajectory: wind for many turns ---
    n_turns = 100
    n_points = n_turns * 800  # enough resolution for smooth lines
    t = np.linspace(0, n_turns * 2 * np.pi, n_points)

    # Toroidal coordinates: t is the "long way around", phi*t is the "short way"
    # x(t) = (R + r*cos(phi*t)) * cos(t)
    # y(t) = (R + r*cos(phi*t)) * sin(t)
    # z(t) = r * sin(phi*t)
    cos_phi_t = np.cos(phi * t)
    sin_phi_t = np.sin(phi * t)
    cos_t = np.cos(t)
    sin_t = np.sin(t)

    x3d = (R + r * cos_phi_t) * cos_t
    y3d = (R + r * cos_phi_t) * sin_t
    z3d = r * sin_phi_t

    # Apply tilt rotation around x-axis
    y_rot = y3d * np.cos(tilt) - z3d * np.sin(tilt)
    z_rot = y3d * np.sin(tilt) + z3d * np.cos(tilt)
    x_rot = x3d

    # Project to 2D (orthographic) and center on canvas
    x2d = cx + x_rot
    y2d = cy + y_rot
    z_depth = z_rot  # used for shading

    # --- Normalize z for depth mapping ---
    z_min = z_depth.min()
    z_max = z_depth.max()
    z_norm = (z_depth - z_min) / (z_max - z_min)  # 0 = far, 1 = near

    # --- Color palette: navy (near) to mauve (far) ---
    # Anchors matching grief_void family:
    #   near/dark:  #2E425E (navy-indigo)
    #   mid:        #55647E, #6A7088
    #   far/light:  #907C8E, #9E7E88 (mauve blue-grey)
    anchors_z = np.array([0.0, 0.25, 0.50, 0.75, 1.0])
    anchors_rgb = np.array([
        [0x9E, 0x7E, 0x88],   # z=0  far:  mauve
        [0x90, 0x7C, 0x8E],   # z=.25      blue-mauve
        [0x6A, 0x70, 0x88],   # z=.50      mid blue-grey
        [0x42, 0x54, 0x70],   # z=.75      slate navy
        [0x2E, 0x42, 0x5E],   # z=1  near: deep navy
    ], dtype=float) / 255.0

    # --- Set up figure (grief_void boilerplate) ---
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # --- Build line segments with per-segment depth styling ---
    # Process in chunks to manage memory and allow z-ordering
    # We split into "back" and "front" passes for proper occlusion

    # Segment midpoint z values for sorting
    z_mid = 0.5 * (z_norm[:-1] + z_norm[1:])

    # Build all segments
    pts = np.column_stack([x2d, y2d]).reshape(-1, 1, 2)
    segments = np.concatenate([pts[:-1], pts[1:]], axis=1)

    # Per-segment colors, linewidths, alphas
    n_seg = len(segments)

    # Interpolate RGB from depth
    seg_r = np.interp(z_mid, anchors_z, anchors_rgb[:, 0])
    seg_g = np.interp(z_mid, anchors_z, anchors_rgb[:, 1])
    seg_b = np.interp(z_mid, anchors_z, anchors_rgb[:, 2])

    # Linewidth:  far (z_mid~0) -> 0.3,  near (z_mid~1) -> 1.2
    seg_lw = 0.3 + 0.9 * z_mid

    # Alpha:  far -> 0.20,  near -> 0.85
    seg_alpha = 0.20 + 0.65 * z_mid

    # Boost saturation slightly on the outer (mauve) segments
    seg_colors = np.column_stack([seg_r, seg_g, seg_b, seg_alpha])

    # --- Render in two passes: back first (low z), then front (high z) ---
    # This gives proper depth layering
    threshold = 0.45

    # Back pass
    back_mask = z_mid < threshold
    if np.any(back_mask):
        back_segs = segments[back_mask]
        back_cols = seg_colors[back_mask]
        back_lws = seg_lw[back_mask]
        lc_back = mc.LineCollection(
            back_segs, linewidths=back_lws, colors=back_cols,
            capstyle='round', joinstyle='round', zorder=1
        )
        ax.add_collection(lc_back)

    # Front pass
    front_mask = z_mid >= threshold
    if np.any(front_mask):
        front_segs = segments[front_mask]
        front_cols = seg_colors[front_mask]
        front_lws = seg_lw[front_mask]
        lc_front = mc.LineCollection(
            front_segs, linewidths=front_lws, colors=front_cols,
            capstyle='round', joinstyle='round', zorder=2
        )
        ax.add_collection(lc_front)

    # --- Equation label ---
    ax.text(0.06, 0.06, "\u03c9=\u03c6=(1+\u221a5)/2",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    # --- Save ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "cycles_toroid.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
