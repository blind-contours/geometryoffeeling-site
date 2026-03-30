"""
Geometry of Feeling — Rage: Rage Detonation
Standalone render script
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#0E0E12"  # very dark — rage lives in darkness

# Palette: violent contrast against near-black
CRIMSON = "#C02020"; BLACK_ACCENT = "#181818"; EXPLOSIVE = "#E06020"
BLOOD = "#8A1818"; HOT_WHITE = "#F0E8E0"
SCAR = "#E04030"; EMBER = "#D05020"; ASH = "#808088"
FURNACE = "#C83818"; WOUND = "#A02028"

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2; cy = PAD_B + PH / 2

EQ_OPACITY = 0.55
SERIES_OPACITY = 0.38

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
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.85,0.80,0.75,EQ_OPACITY),transform=ax.transData)
def split_segments(xs, ys, mask):
    """Split masked arrays into contiguous segments to avoid straight-line jumps."""
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
    if in_seg and len(mask) - start >= 3:
        segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4):
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def render():
    fig, ax = make_fig()
    np.random.seed(404)

    n_rays = 90
    for i in range(n_rays):
        angle = 2 * np.pi * i / n_rays + np.random.uniform(-0.02, 0.02)

        # Each ray is a Dirac-like spike: thin, sharp, tall
        n_pts = 500
        r_max = PW * 0.52
        r_vals = np.linspace(0, r_max, n_pts)

        # Dirac approximation along the radial direction —
        # multiple sharp spikes at different radii
        n_spikes = np.random.randint(2, 6)
        spike_positions = np.sort(np.random.uniform(0.08, 0.90, n_spikes)) * r_max
        spike_widths = np.random.uniform(0.005, 0.02, n_spikes) * r_max
        spike_heights = np.random.uniform(0.3, 1.0, n_spikes)

        # Build the radial profile: base radius + spikes
        radial_offset = np.zeros(n_pts)
        for si in range(n_spikes):
            spike = spike_heights[si] * np.exp(
                -((r_vals - spike_positions[si]) / spike_widths[si]) ** 2)
            radial_offset += spike

        # Convert to cartesian — spikes push the line perpendicular to the ray
        perp_angle = angle + np.pi / 2
        spike_amp = PW * 0.06
        xs_r = cx + r_vals * np.cos(angle) + spike_amp * radial_offset * np.cos(perp_angle)
        ys_r = cy + r_vals * np.sin(angle) + spike_amp * radial_offset * np.sin(perp_angle)

        # Random gaps — some rays interrupted
        visible = np.ones(n_pts, dtype=bool)
        n_gaps = np.random.randint(0, 4)
        for _ in range(n_gaps):
            gap_start = np.random.randint(30, n_pts - 50)
            gap_len = np.random.randint(15, 45)
            visible[gap_start:gap_start + gap_len] = False

        mask = (visible &
                (xs_r > PAD_L) & (xs_r < PAD_L + PW) &
                (ys_r > PAD_B) & (ys_r < PAD_B + PH))
        if mask.sum() < 3:
            continue

        cols = [CRIMSON, EXPLOSIVE, SCAR, FURNACE, WOUND, EMBER, HOT_WHITE, BLOOD]
        col = cols[i % len(cols)]

        for seg_xs, seg_ys in split_segments(xs_r, ys_r, mask):
            if len(seg_xs) < 3:
                continue
            pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            n_s = len(segs)
            alphas = np.linspace(0.70, 0.08, n_s)
            lws = np.linspace(2.8, 0.6, n_s)
            colors = [rgba(col, float(a)) for a in alphas]
            lc_obj = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                       capstyle='round', zorder=3 + i % 4)
            ax.add_collection(lc_obj)

    # Detonation core — layered hot glow
    for r_c, a in [(0.35, 0.05), (0.20, 0.12), (0.10, 0.30),
                   (0.04, 0.60), (0.015, 0.90)]:
        ax.add_patch(Circle((cx, cy), radius=r_c,
                    facecolor=rgba(HOT_WHITE, a), edgecolor='none', zorder=9))

    label(ax, "\u03b4_\u03b5(r)=(1/\u03b5\u221a\u03c0)\u00b7e^(\u2212(r/\u03b5)\u00b2),  90 radial rays")
    save(fig, "rage_detonation.pdf")


if __name__ == '__main__':
    render()
