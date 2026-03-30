"""
Geometry of Feeling — Tension: Tension Torsion
Standalone render script
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle
import os

DPI    = 300
FIG_W  = 12
FIG_H  = 8

BG       = "#1A1A1A"
ACID     = "#E8D820"
DIM      = "#888810"
HOT      = "#D04010"
RED      = "#C03010"
ELECTRIC = "#E0E020"
ORANGE   = "#E87020"

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
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(1,1,1,0.20),transform=ax.transData)
def split_segments(xs, ys, mask):
    """Split arrays into contiguous segments where mask is True."""
    segments = []
    in_seg = False
    start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j
            in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3:
                segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3:
        segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4):
    pts  = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc   = mc.LineCollection(segs, linewidths=lw,
                             colors=[rgba(col, alpha)],
                             capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def render():
    fig, ax = make_fig()
    Y_MIN = PAD_B + 0.02
    Y_MAX = PAD_B + PH - 0.02
    X_MIN = PAD_L
    X_MAX = PAD_L + PW

    acid_rgb = hex_to_rgb(ACID)
    hot_rgb  = hex_to_rgb(HOT)
    red_rgb  = hex_to_rgb(RED)
    orange_rgb = hex_to_rgb(ORANGE)
    elec_rgb = hex_to_rgb(ELECTRIC)

    # --- Torsion parameters ---
    # Twist angle increases with radius: phi(r) = tau * r / (G * J)
    # For visualization: phi(r) = max_twist * (r / R_max)^power
    max_twist = 2.8  # radians at outer edge
    R_max = min(PW, PH) * 0.44
    twist_power = 1.2  # slightly superlinear — outer fibers twist more

    # --- Draw concentric circles (cross-section) ---
    n_circles = 18
    radii = np.linspace(R_max * 0.06, R_max, n_circles)
    N_pts = 500

    for r_idx, r in enumerate(radii):
        theta = np.linspace(0, 2 * np.pi, N_pts)
        # Apply twist: each circle is rotated by phi(r)
        twist = max_twist * (r / R_max) ** twist_power
        theta_twisted = theta + twist

        # Convert to cartesian, centered on canvas
        px = cx + r * np.cos(theta_twisted)
        py = cy + r * np.sin(theta_twisted)

        # Shear strain visualization: the twist creates ovalization
        # Add strain deformation: elliptical distortion increasing with r
        strain = 0.12 * (r / R_max) ** 1.5
        px += strain * r * np.cos(2 * theta_twisted) * 0.3
        py += strain * r * np.sin(2 * theta_twisted) * 0.3

        # Color based on radial position (shear stress increases with r)
        t_r = r / R_max
        if t_r < 0.4:
            cr = acid_rgb[0] * (1 - t_r/0.4) + elec_rgb[0] * t_r/0.4
            cg = acid_rgb[1] * (1 - t_r/0.4) + elec_rgb[1] * t_r/0.4
            cb = acid_rgb[2] * (1 - t_r/0.4) + elec_rgb[2] * t_r/0.4
        elif t_r < 0.7:
            t2 = (t_r - 0.4) / 0.3
            cr = elec_rgb[0] * (1 - t2) + orange_rgb[0] * t2
            cg = elec_rgb[1] * (1 - t2) + orange_rgb[1] * t2
            cb = elec_rgb[2] * (1 - t2) + orange_rgb[2] * t2
        else:
            t2 = (t_r - 0.7) / 0.3
            cr = orange_rgb[0] * (1 - t2) + red_rgb[0] * t2
            cg = orange_rgb[1] * (1 - t2) + red_rgb[1] * t2
            cb = orange_rgb[2] * (1 - t2) + red_rgb[2] * t2

        alpha = 0.20 + 0.60 * t_r
        lw = 0.5 + 1.5 * t_r

        # Clip and draw
        mask = (px >= X_MIN) & (px <= X_MAX) & (py >= Y_MIN) & (py <= Y_MAX)
        segments = split_segments(px, py, mask)
        for sx, sy in segments:
            if len(sx) < 3:
                continue
            pts = np.array([sx, sy]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            col_rgba = (cr, cg, cb, float(np.clip(alpha, 0, 1)))
            lc = mc.LineCollection(segs, linewidths=lw, colors=[col_rgba],
                                   capstyle='round', zorder=3 + r_idx)
            ax.add_collection(lc)

    # --- Draw radial lines (material fibers) ---
    n_radials = 24
    angles_base = np.linspace(0, 2 * np.pi, n_radials, endpoint=False)
    N_r = 300

    for a_idx, angle in enumerate(angles_base):
        r_param = np.linspace(0, R_max, N_r)
        # Each point on the radial line is twisted by phi(r)
        twist_r = max_twist * (r_param / R_max) ** twist_power
        theta_r = angle + twist_r

        px = cx + r_param * np.cos(theta_r)
        py = cy + r_param * np.sin(theta_r)

        # Strain deformation
        strain_r = 0.12 * (r_param / R_max) ** 1.5
        px += strain_r * r_param * np.cos(2 * theta_r) * 0.3
        py += strain_r * r_param * np.sin(2 * theta_r) * 0.3

        mask = (px >= X_MIN) & (px <= X_MAX) & (py >= Y_MIN) & (py <= Y_MAX)
        segments = split_segments(px, py, mask)

        for sx, sy in segments:
            n_s = len(sx)
            if n_s < 3:
                continue
            pts = np.array([sx, sy]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            colors = []
            lws = []
            for i in range(n_s - 1):
                t_local = i / max(n_s - 2, 1)
                # Radial position determines stress color
                r_local = r_param[int(t_local * (N_r - 1))] / R_max
                if r_local < 0.5:
                    t2 = r_local * 2
                    cr = acid_rgb[0] * (1 - t2) + orange_rgb[0] * t2
                    cg = acid_rgb[1] * (1 - t2) + orange_rgb[1] * t2
                    cb = acid_rgb[2] * (1 - t2) + orange_rgb[2] * t2
                else:
                    t2 = (r_local - 0.5) * 2
                    cr = orange_rgb[0] * (1 - t2) + hot_rgb[0] * t2
                    cg = orange_rgb[1] * (1 - t2) + hot_rgb[1] * t2
                    cb = orange_rgb[2] * (1 - t2) + hot_rgb[2] * t2
                a = 0.15 + 0.50 * r_local
                colors.append((cr, cg, cb, float(np.clip(a, 0, 1))))
                lws.append(0.4 + 1.0 * r_local)
            lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                   capstyle='round', zorder=2)
            ax.add_collection(lc)

    # --- Center point: axis of rotation (no stress) ---
    center_dot = Circle((cx, cy), 0.04, facecolor=rgba(ACID, 0.50),
                         edgecolor='none', zorder=25)
    ax.add_patch(center_dot)

    # --- Outer edge: maximum shear stress ring (faint hot glow) ---
    theta_glow = np.linspace(0, 2 * np.pi, 400)
    twist_glow = max_twist * 1.0 ** twist_power
    theta_g = theta_glow + twist_glow
    gx = cx + R_max * np.cos(theta_g)
    gy = cy + R_max * np.sin(theta_g)
    # Strain deformation on glow ring
    strain_g = 0.12 * 1.0
    gx += strain_g * R_max * np.cos(2 * theta_g) * 0.3
    gy += strain_g * R_max * np.sin(2 * theta_g) * 0.3

    mask_g = (gx >= X_MIN) & (gx <= X_MAX) & (gy >= Y_MIN) & (gy <= Y_MAX)
    segs_glow = split_segments(gx, gy, mask_g)
    for sx, sy in segs_glow:
        if len(sx) < 3:
            continue
        # Draw as thick dim glow
        draw_lc(ax, sx, sy, RED, 3.5, 0.12, zo=1)
        draw_lc(ax, sx, sy, HOT, 1.8, 0.25, zo=22)

    # --- Torque direction arrows near outer edge ---
    for angle_a in [0.3, np.pi * 0.7, np.pi * 1.3, np.pi * 1.9]:
        r_a = R_max * 0.92
        twist_a = max_twist * (r_a / R_max) ** twist_power
        theta_a = angle_a + twist_a
        ax_x = cx + r_a * np.cos(theta_a)
        ax_y = cy + r_a * np.sin(theta_a)
        # Arrow tangent to circle (torque direction)
        dx = -np.sin(theta_a) * 0.25
        dy = np.cos(theta_a) * 0.25
        if (X_MIN < ax_x < X_MAX and Y_MIN < ax_y < Y_MAX and
            X_MIN < ax_x + dx < X_MAX and Y_MIN < ax_y + dy < Y_MAX):
            ax.annotate('', xy=(ax_x + dx, ax_y + dy), xytext=(ax_x, ax_y),
                        arrowprops=dict(arrowstyle='->', color=rgba(RED, 0.45),
                                        lw=1.0), zorder=23)

    label(ax, "\u03c6(r) = \u03c4\u00b7r/(GJ),  \u03c4_max = T\u00b7r/J")
    save(fig, "tension_torsion.pdf")


if __name__ == '__main__':
    render()
