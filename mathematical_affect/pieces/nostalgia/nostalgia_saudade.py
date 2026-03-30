"""
Geometry of Feeling — Nostalgia: Nostalgia Saudade
Standalone render script
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
from scipy.interpolate import CubicSpline
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#F0E8D8"

# Palette — memory colors
AMBER = "#B8863A"; SEPIA = "#8A6A42"; FADED_BLUE = "#6A88A8"
OCHRE = "#C4963A"; DUSTY_ROSE = "#A07868"; OLD_GOLD = "#A89048"
WARM_BROWN = "#7A5A3A"; TARNISH = "#887858"; FADED_WINE = "#886068"
DARK_AMBER = "#7A5A20"; LAVENDER = "#8878A8"; SAGE = "#788868"

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
            color=(0.35,0.28,0.18,0.25),transform=ax.transData)
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

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def draw_lc_gradient(ax, xs, ys, col, lw_start, lw_end, a_start, a_end, zo=4, smooth=0):
    """Draw a line collection with gradient alpha and linewidth."""
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    n = len(segs)
    alphas = np.linspace(a_start, a_end, n)
    lws = np.linspace(lw_start, lw_end, n)
    colors = [rgba(col, float(a)) for a in alphas]
    lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def save(fig, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith('.pdf'):
        name = name + '.pdf'
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f'saved {name}')


def render():
    fig, ax = make_fig()
    np.random.seed(77)

    # Multiple spirals, all trying to return to center but failing
    n_spirals = 6
    cols_list = [AMBER, SEPIA, FADED_BLUE, DUSTY_ROSE, OLD_GOLD, WARM_BROWN]

    for i in range(n_spirals):
        frac = i / (n_spirals - 1)
        theta = np.linspace(0, 8 * np.pi, 2000)

        # Spiral that ALMOST closes but drifts slightly each revolution
        drift_rate = 0.008 + frac * 0.006
        r_base = PW * (0.08 + frac * 0.28)

        # The key: radius oscillates (trying to return) but net drift is outward
        r = r_base + r_base * drift_rate * theta + r_base * 0.03 * np.sin(3 * theta)

        phase_offset = i * np.pi / 3
        xs_s = cx + r * np.cos(theta + phase_offset)
        ys_s = cy + r * np.sin(theta + phase_offset) * (PH / PW)

        # Clip to bounds
        mask = ((xs_s > PAD_L) & (xs_s < PAD_L + PW) &
                (ys_s > PAD_B) & (ys_s < PAD_B + PH))

        for seg_xs, seg_ys in split_segments(xs_s, ys_s, mask):
            if len(seg_xs) < 5: continue
            draw_lc_gradient(ax, seg_xs, seg_ys, cols_list[i],
                           1.6, 0.4, 0.45, 0.08, zo=3 + i, smooth=2)

    # Small dot at center — home
    ax.plot(cx, cy, 'o', color=rgba(AMBER, 0.30), markersize=6, markeredgewidth=0, zorder=12)
    ax.plot(cx, cy, 'o', color=rgba(AMBER, 0.12), markersize=18, markeredgewidth=0, zorder=11)

    label(ax, "r(\u03b8) = r\u2080 + \u03b5\u03b8 + a\u00b7sin(3\u03b8)")
    save(fig, "nostalgia_saudade.pdf")


if __name__ == '__main__':
    render()
