"""
Geometry of Feeling — Wonder: Meditation
Circle inversion transforms parallel lines into a family of circles
converging through a focal point. Two unequal bodies — one circular,
one elliptical — meet at a luminous passage. The lines taper from
bold sweeps at the edges to whispers at the center, and the glow
comes from the convergence itself.

Mathematics: w = R²/z̄ (circle inversion in the complex plane)
"""
import os
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import FancyBboxPatch, Rectangle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
PRINT_DIR = os.path.join(SCRIPT_DIR, '..', '..', '..', 'public', 'prints', 'wonder')
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PRINT_DIR, exist_ok=True)

DPI = 300
FIG_W = 12
FIG_H = 8
MARGIN_COLOR = "#DDD9D2"
AR = FIG_H / FIG_W

PALE_VIOLET = "#8878C0"
ICE = "#88A8D0"
WARM_GOLD = "#D8B840"
BRIGHT_GOLD = "#F0D060"

ML, MR, MB, MT = 0.07, 0.07, 0.08, 0.08


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))


def render():
    content_bg = "#1a2540"

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=MARGIN_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=MARGIN_COLOR,
                            edgecolor='none', zorder=-10))
    ax.add_patch(FancyBboxPatch((ML, MB), 1 - ML - MR, 1 - MB - MT,
                                 boxstyle="square,pad=0",
                                 facecolor=content_bg, edgecolor='none', zorder=0))

    inv_cx = ML + (1 - ML - MR) * 0.46
    inv_cy = MB + (1 - MB - MT) * 0.42
    R_inv_upper = 0.23
    R_inv_lower = 0.17

    content_l = ML + 0.01
    content_r = 1 - MR - 0.01
    content_b = MB + 0.01
    content_t = 1 - MT - 0.01

    edge_fade = 0.04

    n_circle_pts = 3000
    tc = np.linspace(0, 2 * np.pi, n_circle_pts)

    n_upper = 18
    n_lower = 20
    lower_y_stretch = 1.12

    all_lines = []
    for i in range(1, n_upper + 1):
        d = 0.012 * i + 0.005
        all_lines.append((d, R_inv_upper, False))
    for i in range(1, n_lower + 1):
        d = 0.012 * i + 0.005
        all_lines.append((-d, R_inv_lower, True))

    for d, R_inv, is_lower in all_lines:
        if abs(d) < 0.001:
            continue

        circle_r_visual = R_inv ** 2 / (2 * abs(d))
        circle_cy = inv_cy + R_inv ** 2 / (2 * d)
        circle_cx = inv_cx

        if circle_r_visual > 1.5 or circle_r_visual < 0.003:
            continue

        actual_pts = tc
        if circle_r_visual > 0.3:
            actual_pts = np.linspace(0, 2 * np.pi,
                                     max(n_circle_pts, int(n_circle_pts * circle_r_visual / 0.3)))

        xs = circle_cx + circle_r_visual * AR * np.cos(actual_pts)
        ys = circle_cy + circle_r_visual * np.sin(actual_pts)

        if is_lower:
            ys = inv_cy + (ys - inv_cy) * lower_y_stretch

        mask = ((xs >= content_l) & (xs <= content_r) &
                (ys >= content_b) & (ys <= content_t))

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
        if in_seg and len(xs) - start >= 3:
            segments.append((xs[start:], ys[start:]))

        t_norm = min(circle_r_visual / 0.5, 1.0)

        if t_norm < 0.3:
            col = PALE_VIOLET
            alpha = 0.04 + t_norm * 0.45
            lw_base = 0.2 + t_norm * 0.6
        elif t_norm < 0.6:
            col = ICE
            alpha = 0.25 + (t_norm - 0.3) * 0.4
            lw_base = 0.6 + (t_norm - 0.3) * 0.8
        else:
            col = WARM_GOLD
            outer_fade = min(1.0, (1.0 - t_norm) / 0.12) if t_norm > 0.88 else 1.0
            alpha = (0.40 + (t_norm - 0.6) * 0.4) * outer_fade
            lw_base = 1.0 + (t_norm - 0.6) * 1.0

        for seg_x, seg_y in segments:
            pts = np.array([seg_x, seg_y]).T.reshape(-1, 1, 2)
            segs_lc = np.concatenate([pts[:-1], pts[1:]], axis=1)

            mid_x = (seg_x[:-1] + seg_x[1:]) / 2
            mid_y = (seg_y[:-1] + seg_y[1:]) / 2
            dist = np.sqrt((mid_x - inv_cx) ** 2 + (mid_y - inv_cy) ** 2)

            max_dist = 0.45
            dist_norm = np.clip(dist / max_dist, 0, 1)

            taper_w = 0.2 + 0.8 * dist_norm ** 0.7
            lw_arr = lw_base * taper_w

            proximity = 1.0 - dist_norm
            glow_strength = proximity ** 2.5

            dist_to_left = mid_x - content_l
            dist_to_right = content_r - mid_x
            dist_to_bottom = mid_y - content_b
            dist_to_top = content_t - mid_y
            dist_to_edge = np.minimum(np.minimum(dist_to_left, dist_to_right),
                                       np.minimum(dist_to_bottom, dist_to_top))
            edge_alpha = np.clip(dist_to_edge / edge_fade, 0, 1)

            col_rgb = hex_to_rgb(col)
            bright_rgb = hex_to_rgb(BRIGHT_GOLD)
            seg_colors = []
            for si in range(len(segs_lc)):
                g = glow_strength[si]
                r = col_rgb[0] + (bright_rgb[0] - col_rgb[0]) * g
                gr_c = col_rgb[1] + (bright_rgb[1] - col_rgb[1]) * g
                b = col_rgb[2] + (bright_rgb[2] - col_rgb[2]) * g
                a = min(alpha + g * 0.4, 0.95) * edge_alpha[si]
                seg_colors.append((r, gr_c, b, a))

            lc = mc.LineCollection(segs_lc, linewidths=lw_arr,
                                   colors=seg_colors,
                                   capstyle='round', joinstyle='round',
                                   zorder=3 + int(t_norm * 5))
            ax.add_collection(lc)

    # Signature
    add_signature(fig, ax, MARGIN_COLOR, margin_piece=True,
                  margin_bottom=FIG_H * 0.08)

    # Save PDF
    pdf_path = os.path.join(OUTPUT_DIR, "wonder_meditation.pdf")
    fig.savefig(pdf_path, format='pdf', facecolor=MARGIN_COLOR, dpi=DPI)
    print(f"  saved {pdf_path}")

    # Save JPG
    jpg_path = os.path.join(PRINT_DIR, "wonder_meditation.jpg")
    fig.savefig(jpg_path, facecolor=MARGIN_COLOR, dpi=DPI,
                pil_kwargs={"quality": 96})
    print(f"  saved {jpg_path}")

    plt.close(fig)


if __name__ == '__main__':
    print("═══ Wonder: Meditation ═══")
    render()
    print("═══ Done ═══")
