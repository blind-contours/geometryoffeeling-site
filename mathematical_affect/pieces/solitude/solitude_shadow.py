"""
Geometry of Feeling — Solitude: Shadow
A single gold vertical form casting a long diagonal shadow across the canvas.
One presence and the proof that it exists.
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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI=300; FIG_W=12; FIG_H=8
BG="#E0DDD6"

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

def draw_lc(ax,xs,ys,col,lw,alpha,zo=4,smooth=0):
    if smooth>0:
        ys=gaussian_filter1d(ys,smooth)
    pts=np.array([xs,ys]).T.reshape(-1,1,2)
    segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
    lc=mc.LineCollection(segs,linewidths=lw,colors=[rgba(col,alpha)],
                         capstyle='round',joinstyle='round',zorder=zo)
    ax.add_collection(lc)

def save(fig,name):
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR,name),
                format='pdf',facecolor=BG)
    plt.close(fig); print(f"saved {name}")

def render():
    fig, ax = make_fig()

    # The "figure" — a narrow vertical cluster of lines
    fig_x = cx - PW*0.05
    fig_bottom = PAD_B + PH * 0.20
    fig_top = PAD_B + PH * 0.65

    for i in range(8):
        offset = (i - 3.5) * PW * 0.003
        alpha = 0.75 - abs(i-3.5) * 0.10
        lw = 2.8 - abs(i-3.5) * 0.3
        draw_lc(ax, np.array([fig_x + offset, fig_x + offset]),
                np.array([fig_bottom, fig_top]),
                LONE_GOLD, lw, alpha, zo=5)

    # Shadow — extending diagonally to the right
    t = np.linspace(0, 1, 1500)
    shadow_xs = fig_x + PW * 0.45 * t
    shadow_ys = fig_bottom - PH * 0.08 * t

    for i in range(6):
        offset = (i - 2.5) * PW * 0.004
        alpha = 0.35 * np.exp(-i * 0.20)
        lw = 2.0 * np.exp(-i * 0.15)
        # Fade along length
        n_pts = len(shadow_xs)
        pts = np.array([shadow_xs + offset, shadow_ys]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        alphas = np.linspace(alpha, 0.02, len(segs))
        colors = [rgba(CHARCOAL, float(a)) for a in alphas]
        lws = np.linspace(lw, 0.3, len(segs))
        lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                               capstyle='round', zorder=3)
        ax.add_collection(lc)

    # Gold dot at top of figure
    ax.add_patch(Circle((fig_x, fig_top + PW*0.01), PW*0.007,
                         facecolor=rgba(LONE_GOLD, 0.7), edgecolor='none', zorder=6))

    add_signature(fig, ax, BG)
    save(fig, "solitude_shadow")

if __name__ == '__main__':
    render()
