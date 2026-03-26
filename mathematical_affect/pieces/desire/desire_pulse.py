"""
Geometry of Feeling — Desire: Desire Pulse
Standalone render script
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#E8D8D0"

CRIMSON   = "#9A2030"; HEATED  = "#C88030"; BURGUNDY = "#6A2038"
DARKROSE  = "#8A3848"; FLAME   = "#D06020"; WINE     = "#5A1828"
PULSE_COL = "#B83040"; SMOLDER = "#7A4028"; GILT     = "#C4A040"
EMBER     = "#C05030"; SCARLET = "#D02838"

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

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if smooth > 0: ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

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


def render():
    fig, ax = make_fig()
    np.random.seed(42)
    t = np.linspace(0, 1, 4000)
    xs = PAD_L + PW * t

    # Pairs of lines with body-like organic curves that converge
    n_pairs = 12
    for p in range(n_pairs):
        p_frac = p / (n_pairs - 1)
        y_center = PAD_B + PH * (0.08 + p_frac * 0.84)

        gap_base = PH * 0.028
        # Pulse points where lines meet
        n_pulses = 2 + int(p_frac * 4)
        pulse_centers = np.linspace(0.18, 0.82, n_pulses) + np.random.uniform(-0.04, 0.04, n_pulses)

        # Gap function — closes at pulse points
        gap = np.ones_like(t) * gap_base
        for pc in pulse_centers:
            width = 0.05 + np.random.uniform(0, 0.04)
            depth = 0.88 + np.random.uniform(0, 0.10)
            gap *= 1 - depth * np.exp(-((t - pc) / width)**2)

        # Body-like organic undulation — multiple slow harmonics
        # Like the curve of a hip, a shoulder, a torso
        body_curve = np.zeros_like(t)
        n_harmonics = 3 + np.random.randint(0, 3)
        for h in range(n_harmonics):
            freq_h = 0.8 + h * 0.6 + np.random.uniform(-0.2, 0.2)
            amp_h = PH * (0.012 + np.random.uniform(0, 0.008)) / (1 + h * 0.4)
            phase_h = np.random.uniform(0, 2 * np.pi)
            body_curve += amp_h * np.sin(2 * np.pi * freq_h * t + phase_h)

        # Smooth the body curve for flowing organic shapes
        body_curve = gaussian_filter1d(body_curve, sigma=40)

        # Slight asymmetry — top and bottom lines have different body shapes
        body_curve2 = np.zeros_like(t)
        for h in range(n_harmonics):
            freq_h = 0.7 + h * 0.5 + np.random.uniform(-0.2, 0.2)
            amp_h = PH * (0.010 + np.random.uniform(0, 0.008)) / (1 + h * 0.4)
            phase_h = np.random.uniform(0, 2 * np.pi)
            body_curve2 += amp_h * np.sin(2 * np.pi * freq_h * t + phase_h)
        body_curve2 = gaussian_filter1d(body_curve2, sigma=40)

        curves = [body_curve, body_curve2]
        for idx, sign in enumerate([1, -1]):
            ys = y_center + sign * gap + curves[idx]

            if p_frac < 0.2: col = BURGUNDY
            elif p_frac < 0.4: col = WINE
            elif p_frac < 0.6: col = CRIMSON
            elif p_frac < 0.8: col = EMBER
            else: col = FLAME

            alpha = 0.30 + 0.45 * (1 - abs(p_frac - 0.5) * 1.3)
            lw_base = 0.8 + 1.2 * (1 - abs(p_frac - 0.5))

            # Intensify where gap closes
            gap_norm = gap / gap_base
            lws = lw_base * (1 + 1.0 * (1 - gap_norm))
            alphas = np.clip(alpha * (1 + 0.5 * (1 - gap_norm)), 0, 1)

            pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            colors = [rgba(col, float(a)) for a in alphas[:-1]]
            lc = mc.LineCollection(segs, linewidths=lws[:-1], colors=colors,
                                   capstyle='round', joinstyle='round', zorder=3 + p % 3)
            ax.add_collection(lc)

        # Faint wisps where lines nearly touch
        for pc in pulse_centers:
            mask = np.abs(t - pc) < 0.012
            if mask.sum() < 3: continue
            xs_w = xs[mask]
            ys_top = y_center + gap[mask] + curves[0][mask]
            ys_bot = y_center - gap[mask] + curves[1][mask]
            for j in range(0, len(xs_w), 4):
                ax.plot([xs_w[j], xs_w[j]], [ys_bot[j], ys_top[j]],
                        color=rgba(DARKROSE, 0.10), lw=0.3, zorder=2)

    label(ax, "f(t)=A\u00b7exp(\u2212(t mod T)/\u03c3)")
    save(fig, "desire_pulse")


if __name__ == '__main__':
    render()
