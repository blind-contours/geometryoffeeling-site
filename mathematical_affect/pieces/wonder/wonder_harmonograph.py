"""
Geometry of Feeling — Wonder: Wonder Harmonograph
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

    # Multiple harmonograph patterns with different frequency ratios
    # Near-integer ratios create beautiful spirograph-like patterns
    configs = [
        # (freq_ratio_x, freq_ratio_y, phase1, phase2, decay1, decay2, color, alpha_boost)
        (2, 3, 0.0, np.pi / 4, 0.003, 0.004, PALE_VIOLET, 1.0),
        (3, 2, np.pi / 6, 0.0, 0.004, 0.003, GOLD, 0.9),
        (2, 3, np.pi / 3, np.pi / 2, 0.005, 0.005, COSMIC_TEAL, 0.85),
        (3, 4, 0.0, np.pi / 3, 0.003, 0.004, WARM_GOLD, 0.8),
        (4, 3, np.pi / 4, 0.0, 0.004, 0.003, BRIGHT_VIOLET, 0.75),
        (5, 4, np.pi / 6, np.pi / 6, 0.005, 0.006, ICE, 0.7),
        (3, 5, 0.0, np.pi / 4, 0.004, 0.005, AURORA, 0.65),
    ]

    # Add slight detuning for organic feel
    np.random.seed(42)

    for idx, (fx, fy, p1, p2, d1, d2, col, a_boost) in enumerate(configs):
        # Time parameter -- long enough for pattern to develop
        t = np.linspace(0, 80, 12000)

        # Base frequency
        base_freq = 2 * np.pi

        # Slight detuning from exact integer ratios (0.2-0.5% off)
        detune = 1.0 + np.random.uniform(-0.005, 0.005)

        w1 = fx * base_freq * detune
        w2 = fy * base_freq

        # Amplitude fills the frame
        A1 = PW * 0.42
        A2 = PH * 0.42

        # Compute pendulum paths
        x_vals = A1 * np.sin(w1 * t + p1) * np.exp(-d1 * t)
        y_vals = A2 * np.sin(w2 * t + p2) * np.exp(-d2 * t)

        # Map to canvas
        xs_h = cx + x_vals
        ys_h = cy + y_vals

        # Clip to bounds
        mask = ((xs_h > PAD_L) & (xs_h < PAD_L + PW) &
                (ys_h > PAD_B) & (ys_h < PAD_B + PH))
        if mask.sum() < 10:
            continue

        # Draw with fading alpha as the pendulum decays
        pts = np.array([xs_h, ys_h]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        n_s = len(segs)

        colors = []
        rgb = hex_to_rgb(col)
        for j in range(n_s):
            frac = j / n_s
            # Decay envelope
            envelope = np.exp(-(d1 + d2) / 2 * t[j])
            # Base alpha boosted significantly
            base_alpha = (0.15 + 0.55 * envelope) * a_boost
            # Pulse effect
            pulse = 0.8 + 0.2 * np.sin(frac * 12 * np.pi)
            alpha = base_alpha * pulse
            colors.append((rgb[0], rgb[1], rgb[2], float(np.clip(alpha, 0, 1))))

        # Line width also follows envelope
        lws = np.array([max(0.2, (0.3 + 1.0 * np.exp(-(d1 + d2) / 2 * t[j])))
                        for j in range(n_s)])

        lc_obj = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                   capstyle='round', zorder=3 + idx)
        ax.add_collection(lc_obj)

    # Small bright center point where pendulums converge
    for r, a in [(0.08, 0.06), (0.04, 0.14), (0.015, 0.32)]:
        ax.add_patch(Circle((cx, cy), radius=r,
                    facecolor=rgba(STAR_WHITE, a), edgecolor='none', zorder=10))

    label(ax, "x(t)=A\u2081sin(\u03c9\u2081t+\u03c6\u2081)e^(\u2212d\u2081t)")
    save(fig, "wonder_harmonograph.pdf")


if __name__ == '__main__':
    render()
