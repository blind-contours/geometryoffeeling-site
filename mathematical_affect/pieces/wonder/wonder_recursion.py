"""
Geometry of Feeling — Wonder: Wonder Recursion
Standalone render script
"""

"""
Geometry of Feeling -- Wonder (Final Series)
Five pieces: Recursion, Mandelbrot Orbit, Strange Attractor, Apollonian Gasket, Harmonograph

Mathematical primitives: fractal self-similarity, Mandelbrot boundary orbits,
Rossler strange attractor, Descartes circle packing, damped pendulum harmonics

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
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
BG = "#0A0A14"

# Palette: cosmic -- deep indigo, gold, pale violet, white accent
INDIGO = "#2838A0"; DEEP_BLUE = "#182868"; GOLD = "#C8A030"
PALE_VIOLET = "#8878C0"; COSMIC_TEAL = "#2888A0"; NEBULA = "#4838A0"
STAR_WHITE = "#E8E4E0"; DIM_BLUE = "#384888"; AURORA = "#38A888"
DEEP_VIOLET = "#3828A0"; WARM_GOLD = "#D8B840"; ICE = "#88A8D0"
BRIGHT_GOLD = "#F0D060"; BRIGHT_VIOLET = "#A090E0"


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


PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2; cy = PAD_B + PH / 2


def label(ax, eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.85,0.80,0.75,0.55),transform=ax.transData)
def split_segments(xs, ys, mask):
    segments = []
    in_seg = False
    start = 0
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


def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Ensure name ends with .pdf
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


# =============================================================================
# 1. RECURSION -- Koch snowflake recursive subdivision (KEEP AS IS from series)
#    Koch: subdivide -> project -> repeat
# =============================================================================
def render():
    fig, ax = make_fig()

    def koch_points(p1, p2, depth):
        if depth == 0:
            return [p1]
        dx = p2[0] - p1[0]; dy = p2[1] - p1[1]
        a = (p1[0] + dx / 3, p1[1] + dy / 3)
        b = (p1[0] + 2 * dx / 3, p1[1] + 2 * dy / 3)
        # peak point
        px = p1[0] + dx / 2 - dy * np.sqrt(3) / 6
        py = p1[1] + dy / 2 + dx * np.sqrt(3) / 6
        peak = (px, py)
        pts = []
        pts.extend(koch_points(p1, a, depth - 1))
        pts.extend(koch_points(a, peak, depth - 1))
        pts.extend(koch_points(peak, b, depth - 1))
        pts.extend(koch_points(b, p2, depth - 1))
        return pts

    # draw Koch at multiple depths, each fainter
    for depth in range(1, 6):
        frac = (depth - 1) / 4
        scale = PW * 0.40
        # equilateral triangle vertices
        cy_shifted = cy - PH * 0.08  # shift down so top isn't cut off
        v1 = (cx - scale, cy_shifted - scale * np.sqrt(3) / 3)
        v2 = (cx + scale, cy_shifted - scale * np.sqrt(3) / 3)
        v3 = (cx, cy_shifted + scale * 2 * np.sqrt(3) / 3)
        sides = [(v1, v2), (v2, v3), (v3, v1)]
        for si, (p1, p2) in enumerate(sides):
            pts = koch_points(p1, p2, depth)
            pts.append(p2)
            xs_k = np.array([p[0] for p in pts])
            ys_k = np.array([p[1] for p in pts])
            mask = ((xs_k > PAD_L) & (xs_k < PAD_L + PW) &
                    (ys_k > PAD_B) & (ys_k < PAD_B + PH))
            if mask.sum() < 3:
                continue
            cols = [DEEP_BLUE, INDIGO, PALE_VIOLET, GOLD, WARM_GOLD]
            col = cols[depth - 1]
            alpha = 0.80 * (1 - frac * 0.5)
            lw = 2.8 * (1 - frac * 0.7) + 0.3
            for seg_xs, seg_ys in split_segments(xs_k, ys_k, mask):
                draw_lc(ax, seg_xs, seg_ys, col, lw=lw, alpha=alpha, zo=3 + depth)

    label(ax, "Koch: subdivide \u2192 project \u2192 repeat")
    save(fig, "wonder_recursion.pdf")


if __name__ == '__main__':
    render()
