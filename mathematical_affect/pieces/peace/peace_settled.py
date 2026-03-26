"""
Geometry of Feeling — Peace: Peace Settled
Standalone render script
"""

"""
Geometry of Feeling — Peace (20 Candidates, V2)

True stillness. Not absence of tension but resolution of it. Equilibrium achieved.

Problem with V1: Pure white backgrounds with nearly invisible lines. Not sellable.
Direction: Calm but VISIBLE. Rothko color fields, zen gardens with actual presence,
still water with visible depth. Warmer background (#F0EDE8), much stronger alpha
values, deeper colors.

20 mathematical concepts:
  1. Resolved       — damped oscillation at rest (deeper colors)
  2. Zen Garden     — concentric circles, visible presence
  3. Sand           — zen raking patterns with depth
  4. Cloud          — Gaussian forms with real weight
  5. Settled        — many damped lines finding rest
  6. Still Water    — horizontal layers like a glassy lake
  7. Equilibrium    — Laplacian steady state contours
  8. Breath         — sinusoidal inhale/exhale cycle
  9. Horizon        — Rothko-style color field bands
 10. Moss           — organic spreading, soft growth on stone
 11. Fog            — layered atmospheric density
 12. Meditation     — mandala-like concentric geometry
 13. Tide Pool      — nested concentric forms with depth
 14. Dew            — point patterns with gentle connections
 15. Harmonic       — standing wave patterns, resolved
 16. Canopy         — overlapping leaf-like arcs
 17. Watershed      — water finding its level
 18. Silence        — sparse but present — negative space with anchor
 19. Strata         — geological layers of deep time
 20. Petal          — soft radial curves like a flower at rest

Dependencies: matplotlib, numpy, scipy
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle, Ellipse
from scipy.ndimage import gaussian_filter1d
import os


DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#F0EDE8"  # warm parchment — NOT pure white

# Palette: deep but calm — visible against warm background
DEEP_SAGE = "#4A6A52"; OCEAN = "#3A5A6A"; WARM_GREY = "#6A6860"
CLAY = "#8A7A68"; LICHEN = "#5A7A5A"; STONE = "#7A7A72"
CEDAR = "#5A5040"; MOSS = "#3A5A3A"; DUSK = "#6A5A7A"
WATER = "#4A6A80"; EARTH = "#6A5A48"; FOG_COL = "#8A8A82"
SKY = "#7A8A9A"; BARK = "#5A4A38"; FERN = "#4A6A4A"
RUST = "#8A6A4A"; PLUM = "#6A4A5A"; SAND_COL = "#9A8A72"
MINERAL = "#5A6A6A"; SHADOW = "#4A4A48"

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
            color=(0.40,0.45,0.40,0.22),transform=ax.transData)
def split_segments(xs, ys, mask):
    segments = []; in_seg = False; start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg: start = j; in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3: segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3: segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if len(xs) < 2: return
    if smooth > 0: ys = gaussian_filter1d(ys, smooth)
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


# ============================================================================
# 5. SETTLED — twenty voices finding quiet
# ============================================================================
def render():
    fig, ax = make_fig()
    t = np.linspace(0, 1, 2500); xs = PAD_L + PW * t
    n = 28
    cols = [DEEP_SAGE, OCEAN, LICHEN, CLAY, STONE, WATER, EARTH, DUSK,
            FERN, MOSS, CEDAR, MINERAL]
    for i in range(n):
        frac = i / (n - 1)
        y_base = PAD_B + PH * (0.04 + frac * 0.92)
        omega = 7 * np.pi * (1 + i * 0.25)
        # Settled center around t=0.48, with wide flat zone
        settle_center = 0.48
        settle_width = 0.15  # width of the calm zone
        amp = PH * 0.065
        # Distance from the calm zone (not just center point)
        dist = np.maximum(0, np.abs(t - settle_center) - settle_width)
        # Left side: sharper onset of agitation
        gamma_left = 22 + i * 0.5
        # Right side: slightly gentler agitation that builds
        gamma_right = 15 + i * 0.4
        # Use different gammas for left and right
        gamma_arr = np.where(t < settle_center, gamma_left, gamma_right)
        # Envelope: 0 in center, rises toward edges
        envelope = 1.0 - np.exp(-gamma_arr * dist**2)
        # Right side is less agitated than left (about 60%)
        right_atten = np.where(t > settle_center + settle_width, 0.55, 1.0)
        envelope = envelope * right_atten
        ys = y_base + amp * envelope * np.sin(omega * t + i * 1.1)
        col = cols[i % len(cols)]
        # More color: boost alpha and linewidth
        alpha = 0.55 + 0.15 * np.sin(np.pi * frac)
        lw = 1.1 + 0.5 * np.sin(np.pi * frac)
        draw_lc(ax, xs, ys, col, lw=lw, alpha=alpha, zo=3, smooth=2)
    label(ax, "f_n(t)=Ae^(\u2212\u03b3_nt)\u00b7sin(\u03c9_nt)")
    save(fig, "peace_settled.pdf")


if __name__ == '__main__':
    render()
