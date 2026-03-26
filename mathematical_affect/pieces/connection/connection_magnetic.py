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
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
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

    # Two poles: N (source) on the left, S (sink) on the right
    # This gives classic bar magnet field lines flowing left to right
    n_x = cx - PW * 0.20  # North pole (left, larger)
    n_y = cy + PH * 0.06
    s_x = cx + PW * 0.25  # South pole (right, smaller)
    s_y = n_y

    poles = [
        (n_x, n_y, +1.5),   # N pole (source, stronger = larger appearance)
        (s_x, s_y, -1.5),   # S pole (sink)
    ]

    gold_cols = [GOLD, AMBER, PALE_GOLD, COPPER, BRONZE]

    # --- Field lines emanating from N pole ---
    # Trace from various angles around the N pole
    n_lines = 22
    angles = np.linspace(0.0, 2*np.pi, n_lines, endpoint=False)

    for i, angle in enumerate(angles):
        r_start = 0.18
        x0 = n_x + r_start * np.cos(angle)
        y0 = n_y + r_start * np.sin(angle)

        xs_f, ys_f = trace_field_line(x0, y0, poles, step=0.012,
                                       max_steps=2000, direction=1)
        mask = ((xs_f > PAD_L - 0.3) & (xs_f < PAD_L + PW + 0.3) &
                (ys_f > PAD_B - 0.3) & (ys_f < PAD_B + PH + 0.3))
        col = gold_cols[i % len(gold_cols)]

        # Bolder lines - varying by angle for visual interest
        lw = 1.0 + 0.8 * abs(np.sin(angle))
        alpha = 0.55 + 0.20 * abs(np.cos(angle))

        for seg_xs, seg_ys in split_segments(xs_f, ys_f, mask):
            if len(seg_xs) < 5: continue
            draw_lc(ax, seg_xs, seg_ys, col, lw=lw, alpha=alpha, zo=4, smooth=1)

    # --- Concentric orbits around N pole (left, larger) ---
    n_orbits_left = 12
    for i in range(n_orbits_left):
        r = 0.15 + i * 0.08
        n_pts = 500
        theta = np.linspace(0, 2*np.pi, n_pts)
        # Slight spiral
        r_vals = r + 0.003 * theta
        aspect = 0.85
        xs_o = n_x + r_vals * np.cos(theta + i * 0.15)
        ys_o = n_y + r_vals * np.sin(theta + i * 0.15) * aspect
        mask = ((xs_o > PAD_L) & (xs_o < PAD_L + PW) &
                (ys_o > PAD_B) & (ys_o < PAD_B + PH))
        col = gold_cols[i % len(gold_cols)]
        alpha = 0.55 - i * 0.03
        lw = 0.9 - i * 0.04
        if alpha < 0.15: alpha = 0.15
        if lw < 0.3: lw = 0.3
        for seg_xs, seg_ys in split_segments(xs_o, ys_o, mask):
            if len(seg_xs) < 5: continue
            draw_lc(ax, seg_xs, seg_ys, col, lw=lw, alpha=alpha, zo=5, smooth=1)

    # --- Concentric orbits around S pole (right, smaller) ---
    n_orbits_right = 8
    for i in range(n_orbits_right):
        r = 0.12 + i * 0.06
        n_pts = 500
        theta = np.linspace(0, 2*np.pi, n_pts)
        r_vals = r + 0.002 * theta
        aspect = 0.80
        xs_o = s_x + r_vals * np.cos(theta + i * 0.2)
        ys_o = s_y + r_vals * np.sin(theta + i * 0.2) * aspect
        mask = ((xs_o > PAD_L) & (xs_o < PAD_L + PW) &
                (ys_o > PAD_B) & (ys_o < PAD_B + PH))
        col = gold_cols[(i + 2) % len(gold_cols)]
        alpha = 0.50 - i * 0.04
        lw = 0.8 - i * 0.05
        if alpha < 0.15: alpha = 0.15
        if lw < 0.3: lw = 0.3
        for seg_xs, seg_ys in split_segments(xs_o, ys_o, mask):
            if len(seg_xs) < 5: continue
            draw_lc(ax, seg_xs, seg_ys, col, lw=lw, alpha=alpha, zo=5, smooth=1)

    # --- Glowing pole centers ---
    # Left pole (larger, more prominent)
    ax.plot(n_x, n_y, 'o', color=rgba(GOLD, 0.05), markersize=45,
            markeredgewidth=0, zorder=7)
    ax.plot(n_x, n_y, 'o', color=rgba(WARM_WHITE, 0.14), markersize=20,
            markeredgewidth=0, zorder=8)
    ax.plot(n_x, n_y, 'o', color=rgba(WARM_WHITE, 0.35), markersize=9,
            markeredgewidth=0, zorder=9)
    ax.plot(n_x, n_y, 'o', color=rgba(WARM_WHITE, 0.60), markersize=4,
            markeredgewidth=0, zorder=10)

    # Right pole (smaller)
    ax.plot(s_x, s_y, 'o', color=rgba(GOLD, 0.04), markersize=35,
            markeredgewidth=0, zorder=7)
    ax.plot(s_x, s_y, 'o', color=rgba(WARM_WHITE, 0.12), markersize=14,
            markeredgewidth=0, zorder=8)
    ax.plot(s_x, s_y, 'o', color=rgba(WARM_WHITE, 0.28), markersize=7,
            markeredgewidth=0, zorder=9)
    ax.plot(s_x, s_y, 'o', color=rgba(WARM_WHITE, 0.52), markersize=3,
            markeredgewidth=0, zorder=10)

    label(ax, "B = B\u2081 + B\u2082, \u2207\u00d7B = \u03bcJ   \u2014   magnetic: field lines connecting two poles")
    save(fig, "connection_magnetic.pdf")


if __name__ == '__main__':
    render()
