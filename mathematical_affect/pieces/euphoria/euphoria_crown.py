"""
Geometry of Feeling — Euphoria: Euphoria Crown
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
BG="#FEFCF8"  # near-white — the flash of too much light

# Palette: electric, oversaturated, almost painful
ELECTRIC_VIOLET="#8828D0"; HOT_PINK="#E02888"; ACID_YELLOW="#D8D020"
VIVID_CYAN="#20C8D0"; FLASH_ORANGE="#F08020"
MAGENTA="#D020A0"; NEON_GREEN="#40E040"; ULTRAVIOLET="#6020E0"
PLASMA="#E848A0"; WHITE_HOT="#F8F0E0"

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
    """Split masked arrays into contiguous segments to avoid straight-line jumps."""
    segments = []
    in_seg = False
    start = 0
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

def save(fig,name):
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR,name),
                format='pdf',facecolor=BG)
    plt.close(fig); print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def render():
    fig,ax=make_fig()
    configs=[
        (7, 1, PW*0.44, HOT_PINK, 0.50, 1.8),
        (11, 2, PW*0.38, ELECTRIC_VIOLET, 0.45, 1.5),
        (13, 3, PW*0.34, VIVID_CYAN, 0.40, 1.3),
        (17, 4, PW*0.30, ACID_YELLOW, 0.35, 1.1),
        (19, 5, PW*0.26, FLASH_ORANGE, 0.30, 0.9),
        (23, 6, PW*0.22, MAGENTA, 0.28, 0.7),
        (29, 7, PW*0.18, NEON_GREEN, 0.25, 0.6),
    ]
    for R_int, r_int, scale, col, alpha, lw in configs:
        R=R_int; r=r_int
        periods=r
        theta=np.linspace(0,2*np.pi*periods,5000)
        xs_e=scale*0.35*((R+r)*np.cos(theta)-r*np.cos((R+r)*theta/r))/R
        ys_e=scale*0.35*((R+r)*np.sin(theta)-r*np.sin((R+r)*theta/r))/R
        xs_e+=cx; ys_e+=cy
        mask=((xs_e>PAD_L)&(xs_e<PAD_L+PW)&
              (ys_e>PAD_B)&(ys_e<PAD_B+PH))
        if mask.sum()<3: continue
        for seg_xs,seg_ys in split_segments(xs_e,ys_e,mask):
            draw_lc(ax,seg_xs,seg_ys,col,lw=lw,alpha=alpha,zo=3)
    for rad,a in [(0.15,0.06),(0.08,0.15),(0.03,0.35)]:
        ax.add_patch(Circle((cx,cy),radius=rad,
                    facecolor=rgba(PLASMA,a),edgecolor='none',zorder=6))
    add_signature(fig, ax, BG)
    save(fig,"euphoria_crown.pdf")

if __name__ == '__main__':
    render()
