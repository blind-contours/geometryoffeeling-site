"""
Geometry of Feeling — Solitude: Solitude Canopy
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
from scipy.ndimage import gaussian_filter1d
from matplotlib.patches import Circle
import os

DPI=300; FIG_W=12; FIG_H=8
BG="#E0DDD6"

# Palette — same hues as v1, but richer
DEEP_GREY="#404850"; DARK_GREEN="#2A4A3A"; WARM_ACCENT="#C8963A"
SLATE="#5A6878"; CHARCOAL="#353D45"; MOSS="#3A5A42"
MIST="#8A9AA8"; LONE_GOLD="#D4A840"; IRON="#2A3038"
TEAL="#3A6A68"; SAGE="#5A7A60"; DUSK="#4A5068"
BONE="#C8C4B8"; NIGHT="#1A2028"

def hex_to_rgb(h):
    h=h.lstrip('#')
    return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))

def rgba(h,a):
    c=hex_to_rgb(h)
    return (c[0],c[1],c[2],float(np.clip(a,0,1)))

def make_fig():
    fig=plt.figure(figsize=(FIG_W,FIG_H),dpi=DPI)
    ax=fig.add_subplot(111)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0,FIG_W); ax.set_ylim(0,FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    return fig,ax

PAD_L=0.72; PAD_R=0.60; PAD_T=0.65; PAD_B=0.88
PW=FIG_W-PAD_L-PAD_R; PH=FIG_H-PAD_T-PAD_B
cx=PAD_L+PW/2; cy=PAD_B+PH/2

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

def draw_lc(ax,xs,ys,col,lw,alpha,zo=4,smooth=0):
    if smooth>0:
        ys=gaussian_filter1d(ys,smooth)
    pts=np.array([xs,ys]).T.reshape(-1,1,2)
    segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
    lc=mc.LineCollection(segs,linewidths=lw,colors=[rgba(col,alpha)],
                         capstyle='round',joinstyle='round',zorder=zo)
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
    fig,ax=make_fig()
    np.random.seed(33)

    # Recursive branching tree
    branches = []

    def branch(x, y, angle, length, depth, max_depth=9):
        if depth > max_depth or length < PH * 0.008:
            return
        x2 = x + length * np.cos(angle)
        y2 = y + length * np.sin(angle)
        branches.append((x, y, x2, y2, depth))

        # Two branches with some randomness
        spread = 0.35 + np.random.uniform(-0.08, 0.08)
        shrink = 0.68 + np.random.uniform(-0.05, 0.05)

        branch(x2, y2, angle + spread, length * shrink, depth + 1, max_depth)
        branch(x2, y2, angle - spread, length * shrink, depth + 1, max_depth)

        # Occasional third branch
        if np.random.random() < 0.25 and depth < max_depth - 2:
            branch(x2, y2, angle + np.random.uniform(-0.15, 0.15),
                   length * shrink * 0.7, depth + 1, max_depth)

    # Start from bottom center, growing upward
    root_x = cx
    root_y = PAD_B + PH * 0.08
    branch(root_x, root_y, np.pi/2, PH * 0.22, 0)

    # Draw all branches
    for bx1, by1, bx2, by2, depth in branches:
        depth_frac = depth / 9
        alpha = 0.55 * (1 - depth_frac * 0.5)
        lw = 1.8 * (1 - depth_frac * 0.75)

        if depth < 3:
            col = CHARCOAL
        elif depth < 6:
            col = DARK_GREEN
        else:
            col = MOSS

        ax.plot([bx1, bx2], [by1, by2], color=rgba(col, alpha),
                linewidth=max(lw, 0.15), zorder=4 - depth * 0.1,
                solid_capstyle='round')

    # Warm point at root
    ax.plot(root_x, root_y, 'o', color=rgba(WARM_ACCENT, 0.50),
            markersize=3.0, markeredgewidth=0, zorder=7)

    add_signature(fig, ax, BG)
    save(fig,"solitude_canopy")

if __name__ == '__main__':
    render()
