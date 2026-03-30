"""
Geometry of Feeling — Surrender: Surrender Flow
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
# 4. FLOW (improved — more visible, stronger convergence)
# =============================================================================
def render():
    fig, ax = make_fig()
    np.random.seed(33)
    n_curves = 30
    t = np.linspace(0, 1, 1500)
    flow_y = cy + PH * 0.06 * np.sin(2 * np.pi * t * 0.7)
    for i in range(n_curves):
        frac = i / (n_curves - 1)
        xs_f = PAD_L + PW * t
        y_start = PAD_B + PH * (0.05 + frac * 0.90)
        merge_rate = 2.5 + np.random.uniform(0, 2.5)
        blend = 1 - np.exp(-merge_rate * t)
        noise = np.cumsum(np.random.randn(len(t)) * PH * 0.003 * (1 - blend))
        noise = gaussian_filter1d(noise, 15)
        ys_f = y_start * (1 - blend) + flow_y * blend + noise
        mask = (ys_f > PAD_B) & (ys_f < PAD_B + PH)
        if mask.sum() < 3: continue
        cols = [DARK, MED_DARK, SOFT, RUST, CLAY, BLUE_GR, WARM, LAVENDER, MIST]
        col = cols[i % len(cols)]
        alpha = 0.22 + 0.70 * (1 - abs(frac - 0.5) * 1.2)
        lw = 0.7 + 1.4 * (1 - abs(frac - 0.5))
        for seg_xs, seg_ys in split_segments(xs_f, ys_f, mask):
            draw_lc(ax, seg_xs, seg_ys, col, lw=lw, alpha=alpha, zo=3, smooth=5)
    draw_lc(ax, PAD_L + PW * t, flow_y, DARK, lw=2.1, alpha=0.42, zo=2, smooth=5)
    add_signature(fig, ax, BG)
    save(fig, "surrender_flow")

if __name__ == '__main__':
    render()
