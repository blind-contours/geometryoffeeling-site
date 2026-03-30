"""
Geometry of Feeling — Growth: Branch
Symmetric fractal canopy — L-system A→F[−θA][+θA],
13 levels deep. The classic branching tree, generated
from a single recursive rule. θ=35°, scale ratio 0.82.
"""

import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#F5F0E6'

# Full-bleed — no margins
cx = FIG_W / 2
XL = 0.0; XR = FIG_W
YB_CLIP = 0.0; YT_CLIP = FIG_H

# Palette
DARK_G = '#2A4A1A'
PALE_G = '#C8D8A8'

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def clip_seg(x1, y1, x2, y2):
    """Cohen–Sutherland line clipping to plot area."""
    def code(x, y):
        return (1 if x < XL else 2 if x > XR else 0) | \
               (4 if y < YB_CLIP else 8 if y > YT_CLIP else 0)
    c1, c2 = code(x1, y1), code(x2, y2)
    for _ in range(12):
        if not (c1 | c2):
            return x1, y1, x2, y2
        if c1 & c2:
            return None
        c = c1 or c2
        dx = x2 - x1 + 1e-12
        dy = y2 - y1 + 1e-12
        if c & 8:
            x = x1 + dx * (YT_CLIP - y1) / dy; y = YT_CLIP
        elif c & 4:
            x = x1 + dx * (YB_CLIP - y1) / dy; y = YB_CLIP
        elif c & 2:
            y = y1 + dy * (XR - x1) / dx; x = XR
        else:
            y = y1 + dy * (XL - x1) / dx; x = XL
        if c == c1:
            x1, y1, c1 = x, y, code(x, y)
        else:
            x2, y2, c2 = x, y, code(x, y)
    return None

def collect(x, y, angle, length, depth, spread, scale, sb, segs):
    """Recursive L-system: A → F[−θA][+θA]"""
    if depth == 0 or length < 0.004:
        return
    rad = np.radians(angle)
    x2 = x + length * np.sin(rad)
    y2 = y + length * np.cos(rad)
    segs.append((x, y, x2, y2, depth))
    seed = abs(int(sb * 997 + depth * 173 + int(angle * 51))) % (2**31)
    np.random.seed(seed)
    w1 = (np.random.rand() - 0.5) * 14
    w2 = (np.random.rand() - 0.5) * 14
    collect(x2, y2, angle - spread + w1, length * scale,
            depth - 1, spread, scale, sb * 2 + 1, segs)
    collect(x2, y2, angle + spread + w2, length * scale,
            depth - 1, spread, scale, sb * 2 + 2, segs)

def draw_branches(ax, segs, max_depth, col_dark, col_light):
    """Render branches with depth-based color and thickness."""
    cd = hex_to_rgb(col_dark)
    cl = hex_to_rgb(col_light)
    for (x1, y1, x2, y2, depth) in segs:
        seg = clip_seg(x1, y1, x2, y2)
        if not seg:
            continue
        frac = depth / max_depth
        col = tuple(cd[i] + (cl[i] - cd[i]) * (1 - frac) for i in range(3))
        ax.plot([seg[0], seg[2]], [seg[1], seg[3]],
                color=(*col, min(1.0, 0.12 + 0.80 * frac)),
                linewidth=max(0.18, 2.8 * (frac ** 0.8)),
                solid_capstyle='round',
                zorder=max(1, int(depth)))

def render():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')

    # Collect L-system segments: 13 levels, θ=35°, scale=0.82
    segs = []
    collect(cx, 0.55, 0, FIG_H * 0.19, 13, 35, 0.82, 0, segs)
    draw_branches(ax, segs, 13, DARK_G, PALE_G)

    add_signature(fig, ax, BG_COLOR)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_branch.pdf")
    fig.savefig(pdf_path, format='pdf', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    render()
