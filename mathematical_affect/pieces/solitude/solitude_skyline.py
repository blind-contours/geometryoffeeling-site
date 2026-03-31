"""
Geometry of Feeling — Solitude: Skyline
Dense band of horizontal lines near the bottom, one gold line floating high above.
Separated from everything below by pure empty space.
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
    rng = np.random.RandomState(55)

    # Dense band of lines near the bottom third
    for i in range(40):
        y = PAD_B + PH * (0.15 + 0.30 * rng.beta(2, 3))
        xs = np.array([PAD_L + PW*0.03, PAD_L + PW*0.97])
        ys_line = np.array([y, y + PH * rng.uniform(-0.01, 0.01)])
        col = [SLATE, DEEP_GREY, TEAL, MIST, CHARCOAL][i % 5]
        draw_lc(ax, xs, ys_line, col, rng.uniform(0.5, 2.0),
                rng.uniform(0.15, 0.45), zo=3)

    # One gold line, high up, alone
    gold_y = PAD_B + PH * 0.78
    xs = np.linspace(PAD_L + PW*0.15, PAD_L + PW*0.85, 1000)
    ys = gold_y + PH * 0.005 * np.sin(4*np.pi*np.linspace(0,1,1000))
    draw_lc(ax, xs, ys, LONE_GOLD, 2.8, 0.80, zo=5)

    # Faint glow
    for offset, alpha in [(0.03, 0.12), (0.06, 0.06), (-0.03, 0.12)]:
        draw_lc(ax, xs, ys + offset, WARM_ACCENT, 1.0, alpha, zo=4)

    add_signature(fig, ax, BG)
    save(fig, "solitude_skyline")

if __name__ == '__main__':
    render()
