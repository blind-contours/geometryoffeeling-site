"""
Geometry of Feeling — Awe: Awe Singularity
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
    np.random.seed(42)
    inclination = 0.38
    n_orbits = 100
    r_min = PW * 0.06; r_max = PW * 0.52
    for i in range(n_orbits):
        frac = i / (n_orbits - 1)
        r_base = r_min + (r_max - r_min) * frac
        phi = np.linspace(0, 2 * np.pi, 1200)
        wobble = r_base * 0.03 * np.sin(4 * phi) * (1.0 - frac * 0.5)
        r = r_base + wobble
        xs_o = cx + r * np.cos(phi)
        ys_o = cy + r * np.sin(phi) * inclination
        mask = ((xs_o > PAD_L) & (xs_o < PAD_L + PW) &
                (ys_o > PAD_B) & (ys_o < PAD_B + PH))
        if mask.sum() < 3: continue
        if frac < 0.12: col = CORONA
        elif frac < 0.25: col = GOLD
        elif frac < 0.45: col = AMBER
        elif frac < 0.65: col = NEBULA_P
        elif frac < 0.82: col = COSMIC
        else: col = INDIGO
        alpha = 0.55 * (1.0 - frac * 0.6) + 0.08
        lw = 1.6 * (1.0 - frac * 0.5) + 0.15
        for seg_xs, seg_ys in split_segments(xs_o, ys_o, mask):
            draw_lc(ax, seg_xs, seg_ys, col, lw=lw, alpha=alpha, zo=3)
    # Radiating lines
    n_rays = 180
    for i in range(n_rays):
        angle = i / n_rays * 2 * np.pi
        t = np.linspace(0, 1, 800)
        r_ray = r_max * 0.08 + t * (PW * 0.55)
        xs_ray = cx + r_ray * np.cos(angle)
        ys_ray = cy + r_ray * np.sin(angle) * inclination
        mask = ((xs_ray > PAD_L) & (xs_ray < PAD_L + PW) &
                (ys_ray > PAD_B) & (ys_ray < PAD_B + PH))
        if mask.sum() < 3: continue
        for seg_xs, seg_ys in split_segments(xs_ray, ys_ray, mask):
            pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            n_s = len(segs)
            alphas = np.linspace(0.30, 0.02, n_s)
            lws = np.linspace(0.8, 0.10, n_s)
            col_ray = [CORONA, GOLD, AMBER, NEBULA_P][i % 4]
            colors = [rgba(col_ray, float(a_)) for a_ in alphas]
            lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                   capstyle='round', zorder=2)
            ax.add_collection(lc)
    # Lensing arcs
    for sign in [1, -1]:
        for j in range(12):
            j_frac = j / 11
            arc_r = PW * (0.06 + j_frac * 0.42)
            phi_arc = np.linspace(-np.pi * 0.45, np.pi * 0.45, 500)
            xs_arc = cx + arc_r * np.cos(phi_arc)
            ys_arc = cy + sign * (PH * 0.08 + arc_r * 0.35 * np.abs(np.sin(phi_arc)))
            mask_a = ((xs_arc > PAD_L) & (xs_arc < PAD_L + PW) &
                      (ys_arc > PAD_B) & (ys_arc < PAD_B + PH))
            if mask_a.sum() < 3: continue
            arc_col = [CORONA, AMBER, NEBULA_P, COSMIC][min(int(j_frac * 4), 3)]
            for seg_xs, seg_ys in split_segments(xs_arc, ys_arc, mask_a):
                draw_lc(ax, seg_xs, seg_ys, arc_col, lw=0.5, alpha=0.18 * (1 - j_frac * 0.7), zo=2)
    # Event horizon
    for r_, a_ in [(0.22, 1.0), (0.28, 0.7), (0.34, 0.4)]:
        ax.add_patch(Circle((cx, cy), radius=r_,
                    facecolor=rgba(BG, a_), edgecolor='none', zorder=6))
    # Photon ring
    phi_ring = np.linspace(0, 2 * np.pi, 800)
    r_ring = PW * 0.055
    xs_ring = cx + r_ring * np.cos(phi_ring)
    ys_ring = cy + r_ring * np.sin(phi_ring) * inclination
    for a_r, lw_r in [(0.55, 1.5), (0.35, 2.5), (0.18, 4.0)]:
        draw_lc(ax, xs_ring, ys_ring, CORONA, lw=lw_r, alpha=a_r, zo=7)
    add_signature(fig, ax, BG)
    save(fig, "awe_singularity.pdf")

if __name__ == '__main__':
    render()
