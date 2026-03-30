"""
Geometry of Feeling — Wonder: Transform
Joukowski-like conformal mapping — circles become airfoils.
A pole singularity warps concentric circles into nested lobes,
revealing hidden structure in simple geometry.
"""
import os
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#4f5d71'

def render():
    SERIES_BG = '#DDD9D2'  # matching wonder_recursion margin color

    blue = '#90a6cf'
    gold = '#d6b876'
    ring = '#efe2bf'

    theta = np.linspace(0, 2 * np.pi, 3200)
    curves = []

    pole = 0.40
    strength = 0.48
    yscale = 0.86

    for R in np.linspace(0.79, 1.74, 38):
        z = R * np.exp(1j * theta)
        w = z + strength / (z - (pole + 0j))
        x = np.real(w)
        y = np.imag(w) * yscale
        curves.append((x, y))

    xmin = min(x.min() for x, y in curves)
    xmax = max(x.max() for x, y in curves)
    ymin = min(y.min() for x, y in curves)
    ymax = max(y.max() for x, y in curves)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=SERIES_BG)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(SERIES_BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Explicit full-canvas background to prevent edge bleeding in PDF→PNG
    from matplotlib.patches import Rectangle
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=SERIES_BG,
                            edgecolor='none', zorder=-10))

    # Content area with piece background — matted inside series frame
    margin_l, margin_r = 0.07, 0.07
    margin_b, margin_t = 0.08, 0.08
    from matplotlib.patches import FancyBboxPatch
    content_rect = FancyBboxPatch(
        (margin_l, margin_b),
        1 - margin_l - margin_r,
        1 - margin_b - margin_t,
        boxstyle="square,pad=0",
        facecolor=BG_COLOR, edgecolor='none', zorder=0)
    ax.add_patch(content_rect)

    # Map curves into the content area
    cx0 = margin_l + 0.06
    cx1 = 1 - margin_r - 0.06
    cy0 = margin_b + 0.08
    cy1 = 1 - margin_t - 0.08

    for i, (x, y) in enumerate(curves):
        X = cx0 + (cx1 - cx0) * (x - xmin) / (xmax - xmin)
        Y = cy0 + (cy1 - cy0) * (y - ymin) / (ymax - ymin)
        col = gold if i % 2 == 0 else blue
        ax.plot(X, Y, color=col,
                lw=0.72 if i % 2 == 0 else 0.68,
                alpha=0.86 if i % 2 == 0 else 0.78,
                solid_capstyle='round', zorder=1)

    # Center ring (the viewer)
    center_x = cx0 + (cx1 - cx0) * (0.55 - 0.12) / 0.76  # preserve relative position
    center_y = cy0 + (cy1 - cy0) * (0.50 - 0.16) / 0.68
    t = np.linspace(0, 2 * np.pi, 400)
    for rr, alpha in [(0.007, 0.88), (0.014, 0.22)]:
        ax.plot(center_x + rr * np.cos(t), center_y + rr * np.sin(t),
                color=ring, lw=1.15, alpha=alpha, zorder=2)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "wonder_transform.pdf")
    add_signature(fig, ax, BG_COLOR)
    fig.savefig(pdf_path, facecolor=SERIES_BG, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    render()
