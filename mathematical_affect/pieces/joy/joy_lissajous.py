"""
Geometry of Feeling — Joy: Joy Lissajous
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
from matplotlib.patches import Circle, Polygon
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import Voronoi
import os

DPI=300; FIG_W=12; FIG_H=8
BG="#FFFFFF"  # white background per spec

# Palette: vivid primaries, full saturation
RED="#E52020"; BLUE="#2060E0"; YELLOW="#F0C010"
GREEN="#20B040"; ORANGE="#F07010"; PURPLE="#8030D0"
CYAN="#10B8D8"; MAGENTA="#D020A0"; LIME="#80D010"
CORAL="#E05040"; SKY="#3090F0"; GOLD="#E0A010"
ROSE="#E04080"; TEAL="#10A898"

PRIMARIES = [RED, BLUE, YELLOW, GREEN, ORANGE, PURPLE,
             CYAN, MAGENTA, LIME, CORAL, SKY, GOLD, ROSE, TEAL]

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
    fig.savefig(os.path.join(OUTPUT_DIR,name),
                format='pdf',facecolor=BG)
    plt.close(fig); print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def render():
    fig,ax=make_fig()
    configs=[
        (3, 2, 0.0,  PW*0.46, RED,    0.52, 1.8),
        (5, 4, 0.3,  PW*0.42, BLUE,   0.48, 1.6),
        (7, 6, 0.5,  PW*0.38, YELLOW, 0.42, 1.4),
        (4, 3, 0.7,  PW*0.34, GREEN,  0.38, 1.2),
        (5, 3, 0.15, PW*0.30, ORANGE, 0.35, 1.1),
        (7, 4, 0.4,  PW*0.26, PURPLE, 0.30, 0.9),
        (3, 4, 0.6,  PW*0.22, MAGENTA,0.28, 0.8),
    ]
    for a_freq,b_freq,delta,scale,col,alpha,lw in configs:
        t=np.linspace(0,2*np.pi*b_freq,5000)
        xs_l=cx+scale*0.46*np.sin(a_freq*t+delta)
        ys_l=cy+scale*0.46*(PH/PW)*np.sin(b_freq*t)
        mask=((xs_l>PAD_L)&(xs_l<PAD_L+PW)&
              (ys_l>PAD_B)&(ys_l<PAD_B+PH))
        if mask.sum()<3: continue
        # color gradient along curve
        pts=np.array([xs_l[mask],ys_l[mask]]).T.reshape(-1,1,2)
        segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
        n_s=len(segs)
        phase = np.linspace(0, 2*np.pi, n_s)
        seg_alphas = alpha * (0.5 + 0.5*np.sin(phase)**2)
        colors=[rgba(col,float(a)) for a in seg_alphas]
        lws = lw * (0.6 + 0.4*np.sin(phase)**2)
        lc_obj=mc.LineCollection(segs,linewidths=lws,colors=colors,
                             capstyle='round',zorder=3)
        ax.add_collection(lc_obj)
    add_signature(fig, ax, BG)
    save(fig,"joy_lissajous.pdf")

if __name__ == '__main__':
    render()
