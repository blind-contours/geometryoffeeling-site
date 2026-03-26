"""
Geometry of Feeling — Desire: Inspiral Concept 1
"The Unreachable Center"

Two logarithmic spirals from opposite poles converging on a center they
never reach, with echo spirals trailing behind. The empty center is the
person you can't have — everything moves toward it, nothing arrives.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
from matplotlib.patches import Circle
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#E8D8D0"

CRIMSON   = "#9A2030"; HEATED  = "#C88030"; BURGUNDY = "#6A2038"
DARKROSE  = "#8A3848"; FLAME   = "#D06020"; WINE     = "#5A1828"
PULSE_COL = "#B83040"; SMOLDER = "#7A4028"; GILT     = "#C4A040"
EMBER     = "#C05030"; SCARLET = "#D02838"; COPPER = "#C49A3C"

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2; cy = PAD_B + PH / 2

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

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

def label(ax, eq):
    ax.text(0.75, 0.75, eq, fontfamily='monospace', fontsize=10,
            color=(0.55, 0.40, 0.35, 0.40), transform=ax.transData)

def draw_lc_gradient_xy(ax, xs, ys, col, lw_s, lw_e, a_s, a_e, zo=4, smooth=0):
    if len(xs) < 2: return
    if smooth > 0:
        xs = gaussian_filter1d(xs, smooth)
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    n = len(segs)
    alphas = np.linspace(a_s, a_e, n)
    lws = np.linspace(lw_s, lw_e, n)
    colors = [rgba(col, float(a)) for a in alphas]
    lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name), format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def render():
    fig, ax = make_fig()
    np.random.seed(42)

    # --- The Void: subtle deepening toward center on light bg ---
    for r, a in [(0.50, 0.03), (0.30, 0.06), (0.18, 0.10),
                 (0.10, 0.16), (0.05, 0.25)]:
        ax.add_patch(Circle((cx, cy), radius=r, facecolor=rgba(DARKROSE, a),
                     edgecolor='none', zorder=6))
    # Pale center — the empty space where desire focuses
    ax.add_patch(Circle((cx, cy), radius=0.05, facecolor=rgba(BG, 0.85),
                 edgecolor='none', zorder=7))

    # --- TWO SPIRALS from opposite edges ---
    # Archimedean spiral (r = a + b*theta) gives even spacing between arms
    # Much more visible spiral structure than logarithmic

    # Spiral A: SCARLET/CRIMSON — enters from left, spirals CW inward
    # Spiral B: GILT/GOLD — enters from right, spirals CCW inward
    # They approach the void from opposite sides, never touching

    spiral_configs = [
        {
            'direction': 1,                 # CW
            'start_angle': np.pi * 0.65,    # upper-left entry
            'r_max': PH * 0.58,
            'r_min': 0.22,
            'n_turns': 3.5,
            'main_col': CRIMSON,
            'echo_cols': [FLAME, HEATED, SCARLET, EMBER, PULSE_COL],
            'main_lw': (0.6, 2.5),
            'main_alpha': (0.20, 0.75),
        },
        {
            'direction': -1,                # CCW — opposite rotation
            'start_angle': np.pi * 1.75,    # lower-right entry
            'r_max': PH * 0.52,
            'r_min': 0.28,
            'n_turns': 3.0,
            'main_col': BURGUNDY,
            'echo_cols': [DARKROSE, WINE, SMOLDER, DARKROSE, BURGUNDY],
            'main_lw': (0.5, 2.2),
            'main_alpha': (0.18, 0.70),
        },
    ]

    for cfg in spiral_configs:
        n_pts = 6000
        theta = np.linspace(0, cfg['n_turns'] * 2 * np.pi, n_pts)

        # Archimedean spiral going inward: r decreases linearly with theta
        r = cfg['r_max'] - (cfg['r_max'] - cfg['r_min']) * theta / theta[-1]

        xs = cx + r * np.cos(cfg['start_angle'] + cfg['direction'] * theta)
        ys = cy + r * np.sin(cfg['start_angle'] + cfg['direction'] * theta) * 0.88

        # Main spiral — bold, intensifying toward center
        draw_lc_gradient_xy(ax, xs, ys, cfg['main_col'],
                           lw_s=cfg['main_lw'][0], lw_e=cfg['main_lw'][1],
                           a_s=cfg['main_alpha'][0], a_e=cfg['main_alpha'][1],
                           zo=5, smooth=3)

        # Echo spirals — 2 on each side of main, clearly separated
        n_echoes = 4
        for e in range(n_echoes):
            e_num = e + 1
            side = 1 if e % 2 == 0 else -1
            # Offset in radius — creates parallel spiral arms
            r_offset = side * (0.12 + (e_num // 2) * 0.10)
            r_e = r + r_offset

            # Clip negative radii
            valid = r_e > cfg['r_min'] * 0.8
            if valid.sum() < 50: continue

            xs_e = cx + r_e[valid] * np.cos(cfg['start_angle'] + cfg['direction'] * theta[valid])
            ys_e = cy + r_e[valid] * np.sin(cfg['start_angle'] + cfg['direction'] * theta[valid]) * 0.88

            col_e = cfg['echo_cols'][e % len(cfg['echo_cols'])]
            e_frac = e_num / (n_echoes + 1)
            alpha_max = 0.55 - e_frac * 0.30
            lw_max = 2.0 - e_frac * 1.0
            if alpha_max < 0.12: alpha_max = 0.12
            if lw_max < 0.4: lw_max = 0.4

            draw_lc_gradient_xy(ax, xs_e, ys_e, col_e,
                               lw_s=0.25, lw_e=lw_max,
                               a_s=0.08, a_e=alpha_max,
                               zo=4, smooth=2)

    # --- Scattered thought-fragments: tiny spiral arcs near the void ---
    for w in range(20):
        angle = np.random.uniform(0, 2 * np.pi)
        r_w = np.random.uniform(0.15, 0.60)
        arc_len = np.random.uniform(0.5, 1.2)
        t_w = np.linspace(0, arc_len, 150)
        # Tiny spiral arcs that curve inward
        r_arc = r_w - 0.04 * t_w
        xs_w = cx + r_arc * np.cos(angle + t_w * 1.5)
        ys_w = cy + r_arc * np.sin(angle + t_w * 1.5) * 0.88
        col_w = [FLAME, CRIMSON, BURGUNDY, HEATED, EMBER, DARKROSE,
                 WINE, SMOLDER, PULSE_COL, CRIMSON][w % 10]
        draw_lc_gradient_xy(ax, xs_w, ys_w, col_w,
                           lw_s=0.15, lw_e=0.5,
                           a_s=0.04, a_e=0.15,
                           zo=3, smooth=1)

    label(ax, "r(\u03b8)=r\u2080\u2212b\u03b8, r\u2192\u0338 0")
    save(fig, "desire_inspiral")


if __name__ == '__main__':
    render()
