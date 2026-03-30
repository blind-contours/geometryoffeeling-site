"""
Geometry of Feeling — Wonder: Wonder Mandelbrot Orbit
Standalone render script
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
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig); print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def render():
    fig, ax = make_fig()
    np.random.seed(99)
    n_orbits = 30
    for i in range(n_orbits):
        frac = i / (n_orbits - 1)
        # points along the cardioid boundary
        theta = 2 * np.pi * frac
        c_real = 0.5 * np.cos(theta) - 0.25 * np.cos(2 * theta)
        c_imag = 0.5 * np.sin(theta) - 0.25 * np.sin(2 * theta)
        # perturb slightly outside
        c_real += np.random.uniform(-0.02, 0.08)
        c_imag += np.random.uniform(-0.02, 0.02)
        c = complex(c_real, c_imag)
        # iterate
        z = complex(0, 0)
        orbit_x = []; orbit_y = []
        for _ in range(80):
            z = z * z + c
            if abs(z) > 4:
                break
            orbit_x.append(z.real)
            orbit_y.append(z.imag)
        if len(orbit_x) < 5:
            continue
        xs_o = np.array(orbit_x)
        ys_o = np.array(orbit_y)
        # ENLARGED scale: PW*0.38 (was 0.22)
        scale = PW * 0.38
        xs_m = cx + xs_o * scale
        ys_m = cy + ys_o * scale * (PH / PW)
        mask = ((xs_m > PAD_L) & (xs_m < PAD_L + PW) &
                (ys_m > PAD_B) & (ys_m < PAD_B + PH))
        if mask.sum() < 3:
            continue
        cols = [PALE_VIOLET, GOLD, COSMIC_TEAL, INDIGO, NEBULA,
                DEEP_BLUE, WARM_GOLD, ICE, AURORA, DIM_BLUE]
        col = cols[i % len(cols)]
        for seg_xs, seg_ys in split_segments(xs_m, ys_m, mask):
            pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            n_s = len(segs)
            # Alpha +40%: 0.40->0.56, 0.08->0.112
            alphas = np.linspace(0.56, 0.112, n_s)
            lws = np.linspace(1.6, 0.4, n_s)
            colors = [rgba(col, float(a)) for a in alphas]
            lc_obj = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                       capstyle='round', zorder=3)
            ax.add_collection(lc_obj)

    label(ax, "z_{n+1}=z_n\u00b2+c")
    save(fig, "wonder_mandelbrot_orbit.pdf")


if __name__ == '__main__':
    render()
