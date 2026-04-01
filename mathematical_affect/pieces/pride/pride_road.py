"""
Geometry of Feeling — Pride: Road
Rainbow road receding toward a warm vanishing-point glow.
44 lines span the full bottom edge, converging to a single point above.
Irregular speed bumps — big near the viewer, smaller in the distance,
with a couple more visible on the road ahead. The path isn't smooth.
"""

import os
import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
JPEG_DIR = os.path.join(SCRIPT_DIR, '..', '..', '..', 'public', 'prints', 'pride')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#f3eee7'


def hex_to_rgb(h):
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


# Full LGBTQ+ palette: trans blue/pink/white woven through classic rainbow
PALETTE_HEX = [
    "#5BCEFA", "#F5A9B8", "#F8F8F8", "#F5A9B8", "#5BCEFA",
    "#E40303", "#FF8C00", "#FFED00", "#008026", "#24408E",
    "#732982", "#5BCEFA", "#F5A9B8", "#F8F8F8",
]
PALETTE_RGB = [hex_to_rgb(c) for c in PALETTE_HEX]
bg_rgb = hex_to_rgb(BG_COLOR)


def soften(palette, amount=0.10):
    out = []
    for c in palette:
        if np.mean(c) > 0.92:
            c = blend(c, hex_to_rgb("#d8dde4"), 0.26)
            out.append(blend(c, bg_rgb, 0.08))
        else:
            out.append(blend(c, bg_rgb, amount))
    return out


def render():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    palette = soften(PALETTE_RGB, 0.10)

    # Parameters (v50)
    n_lines = 44
    vp_x, vp_y = 0.50, 0.88
    bottom_y = -0.03
    lw_near, lw_far, lw_power = 5.0, 0.20, 2.0
    alpha_near, alpha_far = 0.92, 0.26
    color_fade = 0.50
    asymmetry = 0.20
    perspective_power = 0.55
    bump_perspective_power = 1.2

    bumps = [
        (0.16, 0.024, 0.065),       # big early
        (0.30, 0.018, 0.048),       # close behind — double hit
        (0.50, 0.015, 0.028),       # gap then mid
        (0.72, 0.011, 0.010),       # small
        (0.81, 0.012, 0.035),       # real bump in the distance
        (0.90, 0.010, 0.025),       # another one — road keeps going
    ]

    # --- VP glow: soft warm radial bloom ---
    glow_color = np.array([0.96, 0.90, 0.76])
    n_rings = 40
    for r_i in range(n_rings, 0, -1):
        frac = r_i / n_rings
        r = 0.08 * frac
        a = 0.16 * (1 - frac ** 0.5)
        circle = plt.Circle((vp_x, vp_y), r, color=glow_color,
                            alpha=a, fill=True, linewidth=0)
        ax.add_patch(circle)

    # Bottom edge spans full width: corners to corners
    bottom_xs = np.linspace(-0.06, 1.06, n_lines)
    n_pts = 800

    for i, bx in enumerate(bottom_xs):
        u = i / (n_lines - 1)
        side = (u - 0.5) * 2  # -1 to 1

        ts = np.linspace(0, 1, n_pts)
        xs = bx + (vp_x - bx) * ts
        ys = bottom_y + (vp_y - bottom_y) * ts

        # Perpendicular direction
        line_dx = vp_x - bx
        line_dy = vp_y - bottom_y
        line_mag = np.sqrt(line_dx**2 + line_dy**2)
        perp_x = -line_dy / line_mag
        perp_y = line_dx / line_mag
        # Ensure perpendicular always points "up" so bumps are symmetric
        if perp_y < 0:
            perp_x = -perp_x
            perp_y = -perp_y

        # Bump displacement with asymmetry
        displacement = np.zeros_like(ts)
        for center, width, height in bumps:
            gaussian = np.exp(-0.5 * ((ts - center) / width) ** 2)
            perspective = (1.0 - ts) ** bump_perspective_power
            # Asymmetry: bump height varies by side
            side_factor = 1.0 + asymmetry * side * (0.3 * np.sin(center * 7.3) + 0.15)
            height_adj = height * max(side_factor, 0.5)
            displacement += height_adj * gaussian * perspective

        xs += displacement * perp_x
        ys += displacement * perp_y

        col = interpolate_palette(palette, u)

        # Depth
        depth = ts ** perspective_power
        pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        n = len(segs)

        alphas = alpha_near * (1 - depth[:n]) + alpha_far * depth[:n]

        # Dramatic lineweight: steep power curve
        lw_depth = depth[:n] ** lw_power
        lws = lw_near * (1 - lw_depth) + lw_far * lw_depth

        # Atmospheric color fade
        colors = []
        for j, a in enumerate(alphas):
            fade = depth[j] * color_fade
            r = col[0] * (1 - fade) + bg_rgb[0] * fade
            g = col[1] * (1 - fade) + bg_rgb[1] * fade
            b = col[2] * (1 - fade) + bg_rgb[2] * fade
            colors.append((float(r), float(g), float(b), float(a)))

        lc = mc.LineCollection(segs, colors=colors, linewidths=lws,
                               capstyle='round', joinstyle='round')
        ax.add_collection(lc)

    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "pride_road.pdf")
    add_signature(fig, ax, BG_COLOR)
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)

    # Also save JPG for web
    os.makedirs(JPEG_DIR, exist_ok=True)
    jpg_path = os.path.join(JPEG_DIR, "pride_road.jpg")
    fig.savefig(jpg_path, facecolor=BG_COLOR, dpi=150, format='jpg')

    plt.close(fig)
    print(f"saved {pdf_path}")
    print(f"saved {jpg_path}")
    return pdf_path


if __name__ == '__main__':
    render()
