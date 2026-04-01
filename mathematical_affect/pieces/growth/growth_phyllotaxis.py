"""
Geometry of Feeling — Growth: Phyllotaxis
Two sunflower spirals — one mature, one just beginning —
leaning toward each other on curved stems. Vogel's model:
r = c√n, θ = n × 137.508°. The golden angle packs seeds
the way nature does. Parent and child, same rule, different scale.
"""

import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 320
FIG_W = 12
FIG_H = 8
BG_COLOR = '#F5F0E6'

GOLDEN_ANGLE = 137.50776405003785
STEM_COLOR = '#5A7A3A'
LEAF_COLOR = '#6A9A4A'


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def lerp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    t = np.clip(t, 0, 1)
    return (r1 + (r2-r1)*t, g1 + (g2-g1)*t, b1 + (b2-b1)*t)


def bezier_point(p0, p1, p2, t):
    return ((1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0],
            (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1])


def draw_stem(ax, base_x, base_y, head_x, head_y, thickness, color, alpha,
              lean=0.0):
    n_pts = 40
    t = np.linspace(0, 1, n_pts)
    mid_x = (base_x + head_x) / 2 + lean
    mid_y = (base_y + head_y) / 2
    p0 = (base_x, base_y)
    p1 = (mid_x, mid_y)
    p2 = (head_x, head_y)

    sx = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
    sy = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]

    pts = np.array([sx, sy]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    widths = thickness * (1.0 - t[:-1] * 0.35)
    colors_arr = [(*hex_to_rgb(color), alpha)] * len(segs)

    lc = LineCollection(segs, linewidths=widths, colors=colors_arr,
                        capstyle='round', joinstyle='round', zorder=3)
    ax.add_collection(lc)
    return p0, p1, p2


def draw_leaf_on_stem(ax, stem_p0, stem_p1, stem_p2, t_pos, side, length,
                      width, color, alpha, rng):
    stem_x, stem_y = bezier_point(stem_p0, stem_p1, stem_p2, t_pos)
    dx = 2*(1-t_pos)*(stem_p1[0]-stem_p0[0]) + 2*t_pos*(stem_p2[0]-stem_p1[0])
    dy = 2*(1-t_pos)*(stem_p1[1]-stem_p0[1]) + 2*t_pos*(stem_p2[1]-stem_p1[1])
    tangent_angle = np.arctan2(dy, dx)
    leaf_angle = tangent_angle + side * (np.pi/3 + rng.uniform(-0.3, 0.3))

    tip_x = stem_x + length * np.cos(leaf_angle)
    tip_y = stem_y + length * np.sin(leaf_angle)

    n = 20
    t = np.linspace(0, 1, n)
    nx_ = -np.sin(leaf_angle)
    ny_ = np.cos(leaf_angle)
    w_profile = np.sin(np.pi * t) ** 0.7 * width

    lx = stem_x + t * (tip_x - stem_x)
    ly = stem_y + t * (tip_y - stem_y)
    ux = lx + nx_ * w_profile * 0.5
    uy = ly + ny_ * w_profile * 0.5
    lbx = lx - nx_ * w_profile * 0.5
    lby = ly - ny_ * w_profile * 0.5

    leaf_x = np.concatenate([ux, lbx[::-1]])
    leaf_y = np.concatenate([uy, lby[::-1]])

    ax.fill(leaf_x, leaf_y, color=(*hex_to_rgb(color), alpha * 0.55), zorder=2)
    ax.plot(lx, ly, '-', color=(*hex_to_rgb(color), alpha * 0.7),
            linewidth=0.35, zorder=2)


def draw_phyllotaxis(ax, cx, cy, n_seeds, scale, color_inner, color_mid,
                     color_outer, max_size, min_size, alpha_base, rng,
                     angle_offset=0, size_variation=0.25, overlap_centers=None):
    ns = np.arange(1, n_seeds + 1)
    r = scale * np.sqrt(ns)
    theta = np.radians(ns * GOLDEN_ANGLE + angle_offset)

    x = cx + r * np.cos(theta)
    y = cy + r * np.sin(theta)
    fracs = ns / n_seeds

    for i in range(len(ns)):
        if not (0.05 < x[i] < FIG_W - 0.05 and 0.05 < y[i] < FIG_H - 0.05):
            continue

        f = fracs[i]
        if f < 0.5:
            col = lerp_color(color_inner, color_mid, f * 2)
        else:
            col = lerp_color(color_mid, color_outer, (f - 0.5) * 2)

        base_size = max_size * (1.0 - f * 0.55)
        jitter = rng.uniform(1.0 - size_variation, 1.0 + size_variation)
        s = max(min_size, base_size * jitter)

        alpha = alpha_base - f * 0.28
        alpha = max(0.12, alpha)

        in_overlap = False
        if overlap_centers:
            for (ox, oy, o_r) in overlap_centers:
                dist = np.sqrt((x[i] - ox)**2 + (y[i] - oy)**2)
                if dist < o_r:
                    in_overlap = True
                    break

        if in_overlap:
            s *= 0.82
            alpha *= 0.70
            col = (col[0] * 0.8 + 0.2 * 0.95,
                   col[1] * 0.8 + 0.2 * 0.82,
                   col[2] * 0.8 + 0.2 * 0.38)

        ax.plot(x[i], y[i], 'o', color=(*col, alpha),
                markersize=s, markeredgewidth=0, zorder=5)


def get_bloom_radius(n_seeds, scale):
    return scale * np.sqrt(n_seeds)


# ── Flower definitions (parent/child — E variant) ──

FLOWERS = [
    {   # Large mature bloom — left, leaning slightly right
        'x': 4.2, 'y': 5.3, 'base_x': 3.8, 'lean': 0.4,
        'n_seeds': 900, 'scale': 0.118, 'max_size': 9.0, 'min_size': 2.0,
        'size_variation': 0.22,
        'color_inner': '#F0D060', 'color_mid': '#D4A832', 'color_outer': '#3A6A2A',
        'stem_width': 2.4, 'leaf_size': 0.65, 'alpha': 0.92, 'stem_alpha': 0.75,
        'leaf_positions': [0.15, 0.32, 0.48], 'leaf_sides': [-1, 1, -1],
    },
    {   # Small emerging bloom — right, leaning slightly left
        'x': 8.8, 'y': 3.5, 'base_x': 9.2, 'lean': -0.3,
        'n_seeds': 180, 'scale': 0.060, 'max_size': 3.5, 'min_size': 0.5,
        'size_variation': 0.38,
        'color_inner': '#E8D878', 'color_mid': '#C8B050', 'color_outer': '#8A9A6A',
        'stem_width': 0.8, 'leaf_size': 0.28, 'alpha': 0.75, 'stem_alpha': 0.50,
        'leaf_positions': [0.30, 0.55], 'leaf_sides': [1, -1],
    },
]


def render():
    rng = np.random.RandomState(390)

    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')

    # Pre-compute bloom info for overlap detection
    bloom_info = [(f['x'], f['y'], get_bloom_radius(f['n_seeds'], f['scale']))
                  for f in FLOWERS]

    # Draw smallest first (background), largest last (foreground)
    order = sorted(range(len(FLOWERS)), key=lambda i: FLOWERS[i]['n_seeds'])

    for fi in order:
        flower = FLOWERS[fi]

        # Stem
        stem_ctrl = draw_stem(ax, flower['base_x'], -0.3,
                              flower['x'], flower['y'],
                              flower['stem_width'], STEM_COLOR,
                              flower['stem_alpha'], lean=flower['lean'])

        # Leaves
        for t_pos, side in zip(flower['leaf_positions'], flower['leaf_sides']):
            l_size = flower['leaf_size'] * rng.uniform(0.8, 1.2)
            draw_leaf_on_stem(ax, stem_ctrl[0], stem_ctrl[1], stem_ctrl[2],
                              t_pos, side, l_size, l_size * 0.35,
                              LEAF_COLOR, flower['stem_alpha'], rng)

        # Overlap detection (other blooms)
        other = [(bx, by, br * 0.7)
                 for j, (bx, by, br) in enumerate(bloom_info) if j != fi]

        # Phyllotaxis head
        angle_offset = rng.uniform(0, 360)
        draw_phyllotaxis(ax, flower['x'], flower['y'],
                         flower['n_seeds'], flower['scale'],
                         flower['color_inner'], flower['color_mid'],
                         flower['color_outer'],
                         flower['max_size'], flower['min_size'],
                         flower['alpha'], rng,
                         angle_offset=angle_offset,
                         size_variation=flower['size_variation'],
                         overlap_centers=other)

    add_signature(fig, ax, BG_COLOR)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_phyllotaxis.pdf")
    fig.savefig(pdf_path, format='pdf', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
