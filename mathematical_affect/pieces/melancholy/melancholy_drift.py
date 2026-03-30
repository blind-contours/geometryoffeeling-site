"""
Geometry of Feeling — Melancholy: Melancholy Drift
Standalone render script
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os

DPI=300; FIG_W=12; FIG_H=8
BG="#888888"  # cool mid-grey -- heavier than grief's grey

# Palette: slate blue, grey-mauve, faded green, desaturated cool tones
SLATE="#6A7080"; LAVENDER="#7A7090"; PEWTER="#8A8A90"
DUSK="#5A5A70"; PLUM="#6A5A78"; ASH="#9A9A98"
RAIN="#6A7A88"; BRUISE="#5A5068"; DOVE="#A0A0A0"

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

def label(ax,eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.15,0.15,0.20,0.28),transform=ax.transData)
def split_segments(xs, ys, mask):
    """Split masked arrays into contiguous segments to avoid straight-line jumps
    when a curve exits and re-enters the boundary."""
    segments = []
    in_seg = False
    start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j
            in_seg = True
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
    np.random.seed(30)
    n_walks=22
    cols=[SLATE,RAIN,DUSK,LAVENDER,PEWTER,BRUISE,PLUM,ASH,DOVE,RAIN]
    for i in range(n_walks):
        frac=i/(n_walks-1)
        n_steps=2500
        dx=np.random.randn(n_steps)*PW*0.003
        dy=np.random.randn(n_steps)*PH*0.003-PH*0.00035
        x0=PAD_L+PW*(0.05+frac*0.90)
        y0=PAD_B+PH*0.82
        xs_w=x0+np.cumsum(dx)
        ys_w=y0+np.cumsum(dy)
        mask=((xs_w>PAD_L)&(xs_w<PAD_L+PW)&
              (ys_w>PAD_B)&(ys_w<PAD_B+PH))
        col=cols[i%len(cols)]
        for seg_xs,seg_ys in split_segments(xs_w,ys_w,mask):
            if len(seg_xs)<3: continue
            pts=np.array([seg_xs,seg_ys]).T.reshape(-1,1,2)
            segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
            n_s=len(segs)
            alphas=np.linspace(0.25,0.06,n_s)
            lws=np.linspace(0.6,0.2,n_s)
            colors=[rgba(col,float(a)) for a in alphas]
            lc=mc.LineCollection(segs,linewidths=lws,colors=colors,
                                 capstyle='round',zorder=3)
            ax.add_collection(lc)
    label(ax,"Y(n)=Y(n\u22121)+\u03be\u2212\u03b4")
    save(fig,"melancholy_drift.pdf")


if __name__ == '__main__':
    render()
