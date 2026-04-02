"""
Geometry of Feeling — Peace: Field Guardian

Two charges, one large and one small — V(r) = 1.8/|r−r₁| + 0.5/|r−r₂|.
The larger field wraps around the smaller one the way a parent's calm
extends around a child. Equipotential contour lines trace the invisible
architecture of protection. Not symmetry — shelter.

Coulomb potential field with asymmetric charges, sage/ocean/cedar palette.
"""

import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W, FIG_H = 12, 8
BG = "#F0EDE8"

# Standard Peace series margins
PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R
PH = FIG_H - PAD_T - PAD_B
CX = PAD_L + PW / 2
CY = PAD_B + PH / 2

# Palette — muted natural tones
DEEP_SAGE = "#4A6A52"; OCEAN = "#3A5A6A"; WARM_GREY = "#6A6860"
CLAY = "#8A7A68"; CEDAR = "#5A5040"; DUSK = "#6A5A7A"
WATER = "#4A6A80"; STONE = "#7A7A72"; MINERAL = "#5A6A6A"
SKY = "#7A8A9A"


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))


def extract_contours(ax, X, Y, field, levels):
    """Extract contour paths from a scalar field."""
    paths = []
    for i, level in enumerate(levels):
        cs = ax.contour(X, Y, field, levels=[level], colors='none')
        try:
            for seg_list in cs.allsegs:
                for seg in seg_list:
                    if len(seg) > 8:
                        paths.append((seg, i))
        except AttributeError:
            for coll in cs.collections:
                for path in coll.get_paths():
                    if len(path.vertices) > 8:
                        paths.append((path.vertices, i))
    return paths


def clip_and_split(verts):
    """Clip vertices to art area and split into continuous segments."""
    mask = ((verts[:, 0] >= PAD_L) & (verts[:, 0] <= FIG_W - PAD_R) &
            (verts[:, 1] >= PAD_B) & (verts[:, 1] <= FIG_H - PAD_T))
    segments = []
    in_seg = False
    start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j; in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 5:
                segments.append(verts[start:j])
            in_seg = False
    if in_seg and len(mask) - start >= 5:
        segments.append(verts[start:])
    return segments


def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if len(xs) < 2:
        return
    if smooth > 0:
        ys = gaussian_filter1d(ys.copy(), smooth)
        xs = gaussian_filter1d(xs.copy(), smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)


def render():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')

    # ── Compute Coulomb potential field ──
    # Compute over a slightly larger region for smooth contour extraction,
    # but all drawing will be clipped to the art area.
    overshoot = 0.5
    x_lo, x_hi = PAD_L - overshoot, FIG_W - PAD_R + overshoot
    y_lo, y_hi = PAD_B - overshoot * PH / PW, FIG_H - PAD_T + overshoot * PH / PW

    res = 1200
    x = np.linspace(x_lo, x_hi, res)
    y = np.linspace(y_lo, y_hi, int(res * PH / PW))
    X, Y = np.meshgrid(x, y)

    # Two charges: large parent, small child
    charges = [
        (CX - PW * 0.15, CY,              1.8),   # parent
        (CX + PW * 0.22, CY + PH * 0.08,  0.5),   # child
    ]
    softening = 0.18

    V = np.zeros_like(X)
    for cx, cy, q in charges:
        r = np.sqrt((X - cx)**2 + (Y - cy)**2)
        V += q / (r + softening)

    # ── Subtle fill overlay — clipped to art area ──
    V_norm = (V - np.percentile(V, 2)) / (np.percentile(V, 98) - np.percentile(V, 2) + 1e-10)
    V_norm = np.clip(V_norm, 0, 1)

    fill_rgb = np.array(hex_to_rgb(DEEP_SAGE))
    fill_alpha = 0.04
    img = np.ones((*V_norm.shape, 4))
    for ch in range(3):
        img[:, :, ch] = fill_rgb[ch]
    img[:, :, 3] = V_norm * fill_alpha

    # Place fill exactly within the art area (margin stays clean)
    art_extent = [PAD_L, FIG_W - PAD_R, PAD_B, FIG_H - PAD_T]
    ax.imshow(img, extent=art_extent, origin='lower', aspect='auto',
              zorder=1, interpolation='bilinear')

    # ── Extract and draw contour lines ──
    n_levels = 18
    v_lo, v_hi = np.percentile(V, 6), np.percentile(V, 90)
    levels = np.linspace(v_lo, v_hi, n_levels)
    contours = extract_contours(ax, X, Y, V, levels)

    cols = [DEEP_SAGE, OCEAN, CEDAR, WATER, DUSK, MINERAL, STONE, SKY, CLAY]

    for verts, idx in contours:
        col = cols[idx % len(cols)]
        frac = idx / max(n_levels - 1, 1)
        mid_boost = np.sin(np.pi * frac)
        alpha = 0.30 + 0.45 * mid_boost
        lw = 1.0 + 1.5 * mid_boost

        for seg in clip_and_split(verts):
            draw_lc(ax, seg[:, 0], seg[:, 1], col, lw=lw, alpha=alpha,
                    zo=3, smooth=2)

    # ── Signature and save ──
    add_signature(fig, ax, BG)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_path = os.path.join(OUTPUT_DIR, 'peace_field_guardian.pdf')
    fig.savefig(pdf_path, format='pdf', facecolor=BG)
    print(f"saved {pdf_path}")

    # JPG for website (three levels up from pieces/peace/ to project root)
    jpg_path = os.path.join(SCRIPT_DIR, '..', '..', '..', 'public', 'prints', 'peace',
                            'peace_field_guardian.jpg')
    os.makedirs(os.path.dirname(jpg_path), exist_ok=True)
    fig.savefig(jpg_path, format='jpg', facecolor=BG, dpi=150)
    print(f"saved {jpg_path}")

    plt.close(fig)
    return pdf_path


if __name__ == '__main__':
    render()
