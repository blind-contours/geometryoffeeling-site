"""
Geometry of Feeling — Surrender: Surrender Settle
Standalone render script
"""

"""
Geometry of Feeling -- Surrender v2 (20 candidates)

Surrender is letting go — not defeat but completion.
The moment a system stops resisting and allows the natural process to finish.

User feedback on v1: All too light. Dissolution needs to be bigger.
Settle needs centering. Melt bigger. Shed too boring.

Direction: More contrast while maintaining softness. Elements bigger on canvas.
Darker starting states that dissolve to light.

Dependencies: matplotlib, numpy, scipy
"""

import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os, glob

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#E8E4DE"  # slightly darker warm cream for more contrast

# Deeper palette -- more visible than v1
DARK     = "#5A5048"
MED_DARK = "#7A7068"
SOFT     = "#9A9088"
WARM     = "#B0A898"
LIGHT    = "#C8C0B4"
LAVENDER = "#8A7E98"
BLUE_GR  = "#6A7A88"
RUST     = "#987868"
CLAY     = "#8A7060"
MIST     = "#A0A8A0"

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

def draw_lc_gradient(ax, xs, ys, col, lw_s, lw_e, a_s, a_e, zo=4, smooth=0):
    if smooth > 0:
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

def draw_lc_gradient_xy(ax, xs, ys, col, lw_s, lw_e, a_s, a_e, zo=4, smooth=0):
    """Gradient that also smooths xs."""
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
# 1. SETTLE (improved — centered, bigger, more contrast)
#    Underdamped oscillations settling to equilibrium — centered composition
# =============================================================================
def render():
    fig, ax = make_fig()
    t = np.linspace(0, 1, 2500)
    xs = PAD_L + PW * t
    y_eq = cy  # centered now
    # faint equilibrium line
    ax.plot([PAD_L, PAD_L + PW], [y_eq, y_eq],
            color=rgba(WARM, 0.12), linewidth=0.6, linestyle=':', zorder=2)
    n = 24
    for i in range(n):
        frac = i / (n - 1)
        y0 = cy + PH * 0.45 * (frac - 0.5) * 2  # symmetric around center
        tau = 0.12 + frac * 0.20
        omega_d = 6 + frac * 14
        displacement = y0 - y_eq
        envelope = np.exp(-t / tau)
        ys = y_eq + displacement * envelope * np.cos(omega_d * np.pi * t + frac * 0.5)
        if frac < 0.25: col = DARK
        elif frac < 0.50: col = MED_DARK
        elif frac < 0.75: col = SOFT
        else: col = WARM
        alpha = 0.15 + 0.55 * (1 - abs(frac - 0.5) * 1.3)
        lw = 0.6 + 1.4 * (1 - abs(frac - 0.5))
        draw_lc(ax, xs, ys, col, lw=lw, alpha=alpha, zo=3, smooth=2)
    add_signature(fig, ax, BG)
    save(fig, "surrender_settle")

if __name__ == '__main__':
    render()
