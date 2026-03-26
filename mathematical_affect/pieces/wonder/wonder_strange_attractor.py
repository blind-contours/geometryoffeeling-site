"""
Geometry of Feeling — Wonder: Wonder Strange Attractor
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
# 3. STRANGE ATTRACTOR -- Rossler attractor projected to 2D
#    dx=-y-z, dy=x+ay, dz=b+z(x-c)  (opacity significantly increased)
# =============================================================================
def render():
    fig, ax = make_fig()
    # Rossler attractor parameters
    a, b, c_param = 0.2, 0.2, 5.7
    dt = 0.005; n_steps = 40000
    x, y, z = 1.0, 1.0, 0.0
    xs_a = []; ys_a = []
    for _ in range(n_steps):
        dx = -y - z; dy = x + a * y; dz = b + z * (x - c_param)
        x += dx * dt; y += dy * dt; z += dz * dt
        xs_a.append(x); ys_a.append(y)
    xs_a = np.array(xs_a); ys_a = np.array(ys_a)
    # scale to canvas
    x_range = xs_a.max() - xs_a.min(); y_range = ys_a.max() - ys_a.min()
    xs_m = PAD_L + PW * 0.08 + (xs_a - xs_a.min()) / x_range * PW * 0.84
    ys_m = PAD_B + PH * 0.08 + (ys_a - ys_a.min()) / y_range * PH * 0.80
    # draw with color gradient -- significantly increased opacity
    pts = np.array([xs_m, ys_m]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    n_s = len(segs)
    colors = []
    for j in range(n_s):
        frac = j / n_s
        if frac < 0.25:
            col = DEEP_BLUE
        elif frac < 0.50:
            col = PALE_VIOLET
        elif frac < 0.75:
            col = COSMIC_TEAL
        else:
            col = GOLD
        rgb = hex_to_rgb(col)
        # BOOSTED opacity: was 0.20+0.50*(...), now 0.35+0.60*(...)
        alpha = 0.35 + 0.60 * (0.5 + 0.5 * np.sin(frac * 20 * np.pi))
        colors.append((rgb[0], rgb[1], rgb[2], alpha))
    # Thicker lines for visibility: was 0.7, now 1.0
    lws = np.full(n_s, 1.0)
    lc_obj = mc.LineCollection(segs, linewidths=lws, colors=colors,
                               capstyle='round', zorder=3)
    ax.add_collection(lc_obj)

    label(ax, "dx=\u2212y\u2212z,  dy=x+ay,  dz=b+z(x\u2212c)")
    save(fig, "wonder_strange_attractor.pdf")


if __name__ == '__main__':
    render()
