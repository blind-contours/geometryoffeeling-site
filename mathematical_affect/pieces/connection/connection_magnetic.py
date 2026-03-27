"""
Geometry of Feeling — Connection: Connection Magnetic
Standalone render script
"""

"""
Geometry of Feeling — Connection v3

Curated target: Two magnetic poles on dark background with bold gold field
lines flowing between them. Classic magnetic field line pattern like two
attracting magnets. Fewer but bolder lines. Left pole larger/more prominent,
right pole smaller. Lines arc from one to the other above and below.

Background: #0A0A12 (near-black)
Palette: gold, amber, warm white
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os


DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#0A0A12"
MARGIN_COLOR = "#E8D8B8"

# GOLD palette
GOLD = "#E8C878"
AMBER = "#D4A856"
PALE_GOLD = "#F0D890"
WARM_WHITE = "#F0E8D8"
COPPER = "#C49A3C"
BRONZE = "#B08830"

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def make_fig():
    from matplotlib.patches import FancyBboxPatch, Rectangle
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(MARGIN_COLOR)
    ax.set_facecolor(MARGIN_COLOR)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    # Gold cream margin background
    ax.add_patch(Rectangle((0, 0), FIG_W, FIG_H, facecolor=MARGIN_COLOR,
                            edgecolor='none', zorder=-10))
    # Black content rectangle inside margins
    ml = FIG_W * 0.07; mr = FIG_W * 0.07
    mb = FIG_H * 0.08; mt = FIG_H * 0.08
    ax.add_patch(FancyBboxPatch((ml, mb), FIG_W - ml - mr, FIG_H - mb - mt,
                                 boxstyle="square,pad=0",
                                 facecolor=BG, edgecolor='none', zorder=0))
    return fig, ax

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW/2; cy = PAD_B + PH/2

def label(ax, eq, note=None):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.85,0.80,0.75,0.55),transform=ax.transData)

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if len(xs) < 2: return
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def split_segments(xs, ys, mask):
    segments = []
    in_seg = False; start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j; in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3:
                segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3:
        segments.append((xs[start:], ys[start:]))
    return segments

def save(fig, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=MARGIN_COLOR)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def trace_field_line(x, y, poles, step=0.012, max_steps=2000, direction=1):
    """Trace a field line through monopole field.
    poles: list of (px, py, charge) where charge>0 is source (N), <0 is sink (S).
    Field points from N to S.
    """
    xs_f, ys_f = [x], [y]
    for _ in range(max_steps):
        bx, by = 0.0, 0.0
        for px, py, charge in poles:
            ddx, ddy = x - px, y - py
            r = np.sqrt(ddx**2 + ddy**2) + 0.05
            # Field from monopole: radial, strength ~ charge/r^2
            bx += charge * ddx / r**3
            by += charge * ddy / r**3
        bmag = np.sqrt(bx**2 + by**2) + 1e-12
        x += direction * step * bx / bmag
        y += direction * step * by / bmag
        xs_f.append(x)
        ys_f.append(y)
        if not (PAD_L - 2.0 < x < PAD_L + PW + 2.0 and
                PAD_B - 2.0 < y < PAD_B + PH + 2.0):
            break
        # Stop if reached a sink
        for px, py, charge in poles:
            if charge < 0 and np.sqrt((x - px)**2 + (y - py)**2) < 0.15:
                return np.array(xs_f), np.array(ys_f)
    return np.array(xs_f), np.array(ys_f)


def render():
    fig, ax = make_fig()
    np.random.seed(42)
    from matplotlib.patches import Circle

    # Two poles — left larger, right smaller
    n_x = cx - PW * 0.18
    n_y = cy + PH * 0.06
    s_x = cx + PW * 0.26
    s_y = n_y
    pole_dist = s_x - n_x
    mid_x = (n_x + s_x) / 2

    gold_cols = [GOLD, AMBER, PALE_GOLD, COPPER, BRONZE]

    # --- A) CONNECTING ARCS: parametric arcs from N to S pole ---
    # Fan out from poles rather than converging to a point
    t = np.linspace(0, 1, 800)
    n_arcs = 18
    for i in range(n_arcs):
        frac = i / (n_arcs - 1)
        arc_h = PH * (0.06 + frac * 0.50)
        for sign in [1, -1]:
            # Start/end offset from pole — larger arcs start further from center
            start_offset = 0.15 + frac * 0.12
            end_offset = 0.10 + frac * 0.06
            start_angle = sign * (0.3 + frac * 0.8)  # fan angle from N pole
            end_angle = sign * (0.2 + frac * 0.5)    # fan angle into S pole
            x_start = n_x + start_offset * np.cos(start_angle)
            y_start = n_y + start_offset * np.sin(start_angle)
            x_end = s_x + end_offset * np.cos(np.pi - end_angle)
            y_end = s_y + end_offset * np.sin(np.pi - end_angle)
            xs_a = x_start + (x_end - x_start) * t
            bulge = 0.55 + 0.25 * frac
            arc_shape = np.sin(np.pi * t**bulge)
            ys_a = y_start + (y_end - y_start) * t + sign * arc_h * arc_shape
            wobble = 0.006 * np.sin(7 * np.pi * t + i * 1.3)
            ys_a += wobble

            mask = ((xs_a > PAD_L - 0.3) & (xs_a < PAD_L + PW + 0.3) &
                    (ys_a > PAD_B - 0.3) & (ys_a < PAD_B + PH + 0.3))
            col = gold_cols[i % len(gold_cols)]
            alpha = 0.50 - 0.20 * frac
            lw = 0.85 - 0.30 * frac
            if alpha < 0.15: alpha = 0.15
            if lw < 0.30: lw = 0.30
            for seg_xs, seg_ys in split_segments(xs_a, ys_a, mask):
                if len(seg_xs) < 5: continue
                draw_lc(ax, seg_xs, seg_ys, col, lw=lw, alpha=alpha, zo=4, smooth=1)

    # --- B) ESCAPE LINES: field lines that shoot off from N pole ---
    # Lines at angles not pointing toward S pole — sweep off edges
    escape_angles = [
        # Upper-left fan
        np.pi * 0.55, np.pi * 0.62, np.pi * 0.70, np.pi * 0.78,
        np.pi * 0.85, np.pi * 0.92, np.pi * 1.00,
        # Lower-left fan
        np.pi * 1.08, np.pi * 1.15, np.pi * 1.22, np.pi * 1.30,
        np.pi * 1.38, np.pi * 1.45,
    ]
    for i, angle in enumerate(escape_angles):
        ray_len = PW * (0.35 + 0.25 * abs(np.sin(angle)))
        t_r = np.linspace(0, 1, 500)
        r_vals = 0.15 + ray_len * t_r
        # Slight curve toward the field
        curve = 0.15 * np.sin(np.pi * t_r) * np.cos(angle - np.pi)
        xs_e = n_x + r_vals * np.cos(angle + curve)
        ys_e = n_y + r_vals * np.sin(angle + curve)
        mask = ((xs_e > PAD_L - 0.3) & (xs_e < PAD_L + PW + 0.3) &
                (ys_e > PAD_B - 0.3) & (ys_e < PAD_B + PH + 0.3))
        col = gold_cols[i % len(gold_cols)]
        for seg_xs, seg_ys in split_segments(xs_e, ys_e, mask):
            if len(seg_xs) < 5: continue
            draw_lc(ax, seg_xs, seg_ys, col, lw=0.7, alpha=0.45, zo=3, smooth=1)

    # --- C) Dense concentric spiral orbits around N pole (LEFT, LARGER) ---
    n_orbits_left = 35
    for i in range(n_orbits_left):
        r = 0.08 + i * 0.04
        n_pts = 900
        n_turns = 1.1 + 0.25 * np.sin(i * 0.4)
        theta = np.linspace(0, 2*np.pi * n_turns, n_pts)
        r_vals = r + 0.004 * theta
        aspect = 0.68 + 0.06 * np.sin(i * 0.5)  # wider horizontally
        rot = i * 0.09
        xs_o = n_x + r_vals * np.cos(theta + rot)
        ys_o = n_y + r_vals * np.sin(theta + rot) * aspect
        mask = ((xs_o > PAD_L - 0.3) & (xs_o < PAD_L + PW + 0.3) &
                (ys_o > PAD_B - 0.3) & (ys_o < PAD_B + PH + 0.3))
        col = gold_cols[i % len(gold_cols)]
        frac = i / n_orbits_left
        alpha = 0.55 * (1.0 - 0.5 * frac)
        lw = 0.85 * (1.0 - 0.4 * frac)
        if alpha < 0.10: alpha = 0.10
        if lw < 0.20: lw = 0.20
        for seg_xs, seg_ys in split_segments(xs_o, ys_o, mask):
            if len(seg_xs) < 5: continue
            draw_lc(ax, seg_xs, seg_ys, col, lw=lw, alpha=alpha, zo=5, smooth=1)

    # --- D) Concentric orbits around S pole (RIGHT, similar size to left) ---
    n_orbits_right = 28
    for i in range(n_orbits_right):
        r = 0.06 + i * 0.035
        n_pts = 800
        n_turns = 1.1 + 0.20 * np.sin(i * 0.5)
        theta = np.linspace(0, 2*np.pi * n_turns, n_pts)
        r_vals = r + 0.003 * theta
        aspect = 0.68 + 0.06 * np.sin(i * 0.6)
        rot = i * 0.10
        xs_o = s_x + r_vals * np.cos(theta + rot)
        ys_o = s_y + r_vals * np.sin(theta + rot) * aspect
        mask = ((xs_o > PAD_L - 0.3) & (xs_o < PAD_L + PW + 0.3) &
                (ys_o > PAD_B - 0.3) & (ys_o < PAD_B + PH + 0.3))
        col = gold_cols[(i + 2) % len(gold_cols)]
        frac = i / n_orbits_right
        alpha = 0.50 * (1.0 - 0.45 * frac)
        lw = 0.80 * (1.0 - 0.40 * frac)
        if alpha < 0.10: alpha = 0.10
        if lw < 0.20: lw = 0.20
        for seg_xs, seg_ys in split_segments(xs_o, ys_o, mask):
            if len(seg_xs) < 5: continue
            draw_lc(ax, seg_xs, seg_ys, col, lw=lw, alpha=alpha, zo=5, smooth=1)

    # --- D2) Escape lines from S pole (right side) ---
    escape_angles_r = [
        0.0, np.pi * 0.08, np.pi * 0.16,
        -np.pi * 0.08, -np.pi * 0.16, -np.pi * 0.24,
        np.pi * 0.24, np.pi * 0.32, np.pi * 0.40,
        -np.pi * 0.32, -np.pi * 0.40, -np.pi * 0.48,
    ]
    for i, angle in enumerate(escape_angles_r):
        ray_len = PW * (0.30 + 0.20 * abs(np.sin(angle)))
        t_r = np.linspace(0, 1, 500)
        r_vals = 0.12 + ray_len * t_r
        curve = 0.12 * np.sin(np.pi * t_r) * np.cos(angle)
        xs_e = s_x + r_vals * np.cos(angle + curve)
        ys_e = s_y + r_vals * np.sin(angle + curve)
        mask = ((xs_e > PAD_L - 0.3) & (xs_e < PAD_L + PW + 0.3) &
                (ys_e > PAD_B - 0.3) & (ys_e < PAD_B + PH + 0.3))
        col = gold_cols[i % len(gold_cols)]
        for seg_xs, seg_ys in split_segments(xs_e, ys_e, mask):
            if len(seg_xs) < 5: continue
            draw_lc(ax, seg_xs, seg_ys, col, lw=0.65, alpha=0.40, zo=3, smooth=1)

    # --- E) Glowing pole centers ---
    # Left pole — dark core with gold glow
    ax.add_patch(Circle((n_x, n_y), radius=0.15,
                 facecolor=rgba(BG, 0.95), edgecolor='none', zorder=7))
    for r_c, a in [(0.50, 0.03), (0.30, 0.06), (0.18, 0.12),
                    (0.12, 0.20), (0.07, 0.35), (0.035, 0.55)]:
        ax.add_patch(Circle((n_x, n_y), radius=r_c,
                     facecolor=rgba(GOLD, a), edgecolor='none', zorder=8))
    ax.add_patch(Circle((n_x, n_y), radius=0.020,
                 facecolor=rgba(WARM_WHITE, 0.70), edgecolor='none', zorder=9))

    # Right pole — dark core with gold glow (smaller)
    ax.add_patch(Circle((s_x, s_y), radius=0.10,
                 facecolor=rgba(BG, 0.95), edgecolor='none', zorder=7))
    for r_c, a in [(0.30, 0.03), (0.18, 0.05), (0.12, 0.10),
                    (0.07, 0.18), (0.04, 0.30), (0.020, 0.50)]:
        ax.add_patch(Circle((s_x, s_y), radius=r_c,
                     facecolor=rgba(GOLD, a), edgecolor='none', zorder=8))
    ax.add_patch(Circle((s_x, s_y), radius=0.015,
                 facecolor=rgba(WARM_WHITE, 0.65), edgecolor='none', zorder=9))

    label(ax, "B = B\u2081 + B\u2082, \u2207\u00d7B = \u03bcJ")
    save(fig, "connection_magnetic.pdf")


if __name__ == '__main__':
    render()
