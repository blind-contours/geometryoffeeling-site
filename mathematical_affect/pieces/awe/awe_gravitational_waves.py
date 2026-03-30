"""
Geometry of Feeling — Awe: Awe Gravitational Waves
Standalone render script
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle, Ellipse
from scipy.ndimage import gaussian_filter1d, gaussian_filter
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#0A0A10"

# Palette: cosmic vast
COSMIC = "#2A3A8A"; NEBULA_P = "#5A3A8A"; STARLIGHT = "#C8C8D0"
VOID = "#1A1A40"; AZURE = "#3A5AA0"; CORONA = "#D0A040"
ULTRAVIOLET = "#4A2A7A"; DEEP = "#1A2A5A"; ICE = "#A0B0C8"
GOLD = "#D4AA40"; AMBER = "#C88030"; INDIGO = "#1A1A60"
CRIMSON = "#8A2020"; IVORY = "#D8D0C0"; SLATE = "#4A5A6A"
ROSE = "#8A3050"; TEAL = "#2A6A6A"; CYAN = "#3A8AAA"
PEACH = "#C89070"; MAGENTA = "#7A2A6A"; SILVER = "#A0A8B8"

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
    if len(xs) < 2: return
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def draw_tapered(ax, xs, ys, col, lw_start, lw_end, a_start, a_end, zo=4):
    """Draw a line with tapering width and alpha."""
    if len(xs) < 2: return
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
    # Concentric ripples expanding from center, with chirp (increasing freq)
    n_rings = 80
    for i in range(n_rings):
        frac = i / (n_rings - 1)
        r = PW * 0.03 + frac * PW * 0.55
        theta = np.linspace(0, 2 * np.pi, 800)
        # Quadrupole pattern: amplitude varies as cos(2θ)
        quad = 1.0 + 0.3 * np.cos(2 * theta)
        r_actual = r * quad
        # Plus polarization distortion
        xs = cx + r_actual * np.cos(theta) * (1 + 0.05 * np.sin(frac * 15))
        ys = cy + r_actual * np.sin(theta) * (1 - 0.05 * np.sin(frac * 15))
        mask = ((xs > PAD_L) & (xs < PAD_L + PW) &
                (ys > PAD_B) & (ys < PAD_B + PH))
        if mask.sum() < 3: continue
        # Inner = stronger signal
        alpha = 0.40 * (1 - frac * 0.7) + 0.04
        lw = 1.2 * (1 - frac * 0.5) + 0.15
        col = AZURE if frac < 0.3 else (COSMIC if frac < 0.6 else DEEP)
        for seg_xs, seg_ys in split_segments(xs, ys, mask):
            draw_lc(ax, seg_xs, seg_ys, col, lw=lw, alpha=alpha, zo=3)
    # Two inspiraling source points near center
    for sign in [1, -1]:
        for r_, a_ in [(0.06, 0.10), (0.03, 0.35), (0.012, 0.70)]:
            ax.add_patch(Circle((cx + sign * PW * 0.03, cy), radius=r_,
                        facecolor=rgba(CORONA, a_), edgecolor='none', zorder=7))
    label(ax, "h(r,t)=A\u00b7cos(kr\u2212\u03c9t)/r")
    save(fig, "awe_gravitational_waves.pdf")


if __name__ == '__main__':
    render()
