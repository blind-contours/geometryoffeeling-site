"""
Geometry of Feeling — Awe: Awe Eclipse
Standalone render script
"""

import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle, Ellipse
from scipy.ndimage import gaussian_filter1d, gaussian_filter
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#0A0A10"
MARGIN_COLOR = "#534027"

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
    from matplotlib.patches import FancyBboxPatch, Rectangle
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(MARGIN_COLOR)
    ax.set_facecolor(MARGIN_COLOR)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), FIG_W, FIG_H, facecolor=MARGIN_COLOR,
                            edgecolor='none', zorder=-10))
    ml = FIG_W * 0.07; mr = FIG_W * 0.07
    mb = FIG_H * 0.08; mt = FIG_H * 0.08
    ax.add_patch(FancyBboxPatch((ml, mb), FIG_W - ml - mr, FIG_H - mb - mt,
                                 boxstyle="square,pad=0",
                                 facecolor=BG, edgecolor='none', zorder=0))
    zo = 1000
    ax.add_patch(Rectangle((0, 0), FIG_W, mb, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, FIG_H - mt), FIG_W, mt, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, 0), ml, FIG_H, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((FIG_W - mr, 0), mr, FIG_H, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
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
PRINT_DIR = os.path.join(SCRIPT_DIR, '..', '..', '..', 'public', 'prints', 'awe')

def render(alpha_boost=1.0, lw_boost=1.0):
    fig, ax = make_fig()
    np.random.seed(11)
    moon_r = PW * 0.14
    # Corona streams — radial filaments from behind the disk
    n_streams = 200
    for i in range(n_streams):
        angle = i / n_streams * 2 * np.pi
        t = np.linspace(0, 1, 600)
        # Stream length varies — longer at equator, shorter at poles
        equatorial_factor = 1.0 - 0.5 * abs(np.sin(angle))
        length = PW * (0.2 + 0.35 * equatorial_factor) * np.random.uniform(0.7, 1.3)
        r = moon_r * 0.95 + t * length
        # Streamers have subtle helical twist
        twist = PW * 0.015 * np.sin(t * 3 * np.pi + angle * 3) * equatorial_factor
        xs = cx + r * np.cos(angle) + twist * np.cos(angle + np.pi / 2)
        ys = cy + r * np.sin(angle) + twist * np.sin(angle + np.pi / 2)
        mask = ((xs > PAD_L) & (xs < PAD_L + PW) &
                (ys > PAD_B) & (ys < PAD_B + PH))
        if mask.sum() < 3: continue
        col = CORONA if i % 3 == 0 else (STARLIGHT if i % 3 == 1 else IVORY)
        for seg_xs, seg_ys in split_segments(xs, ys, mask):
            draw_tapered(ax, seg_xs, seg_ys, col,
                          1.2 * lw_boost, 0.05 * lw_boost,
                          min(0.40 * alpha_boost, 0.95),
                          min(0.01 * alpha_boost, 0.95), zo=3)
    # Inner corona glow
    for r_, a_ in [(moon_r * 1.8, 0.04), (moon_r * 1.4, 0.10), (moon_r * 1.15, 0.25)]:
        ax.add_patch(Circle((cx, cy), radius=r_,
                    facecolor=rgba(CORONA, min(a_ * alpha_boost, 0.95)),
                    edgecolor='none', zorder=4))
    # Chromosphere — thin red ring
    theta = np.linspace(0, 2 * np.pi, 600)
    cr_xs = cx + moon_r * 1.02 * np.cos(theta)
    cr_ys = cy + moon_r * 1.02 * np.sin(theta)
    draw_lc(ax, cr_xs, cr_ys, CRIMSON,
            lw=1.5 * lw_boost,
            alpha=min(0.5 * alpha_boost, 0.95), zo=5)
    # Moon disk — pure black
    ax.add_patch(Circle((cx, cy), radius=moon_r,
                facecolor=rgba(BG, 1.0), edgecolor='none', zorder=6))
    # Diamond ring effect — single bright point at edge
    dr_angle = np.pi * 0.25
    dr_x = cx + moon_r * np.cos(dr_angle)
    dr_y = cy + moon_r * np.sin(dr_angle)
    for r_, a_ in [(0.15, 0.06), (0.08, 0.15), (0.03, 0.50), (0.012, 0.90)]:
        ax.add_patch(Circle((dr_x, dr_y), radius=r_ * lw_boost,
                    facecolor=rgba(STARLIGHT, min(a_ * alpha_boost, 0.98)),
                    edgecolor='none', zorder=8))
    add_signature(fig, ax, MARGIN_COLOR, margin_piece=True, margin_bottom=FIG_H * 0.08)
    return fig


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PRINT_DIR, exist_ok=True)
    print("═══ Awe: Eclipse ═══")

    # Print PDF — faithful to the original
    fig = render(alpha_boost=1.0, lw_boost=1.0)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    pdf_path = os.path.join(OUTPUT_DIR, "awe_eclipse.pdf")
    fig.savefig(pdf_path, format='pdf', facecolor=MARGIN_COLOR)
    print(f"  saved {pdf_path}")
    plt.close(fig)

    # Punchier version for web thumbnail
    fig = render(alpha_boost=1.9, lw_boost=1.9)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    jpg_path = os.path.join(PRINT_DIR, "awe_eclipse.jpg")
    fig.savefig(jpg_path, facecolor=MARGIN_COLOR, dpi=DPI,
                pil_kwargs={"quality": 96})
    print(f"  saved {jpg_path}")
    plt.close(fig)

    print("═══ Done ═══")
