"""
Geometry of Feeling — Pride: Pride Flourish
Standalone render script
"""

"""
Geometry of Feeling — Pride (Final Series)
Five pieces: Flourish, Spire, Unfurl, Golden Ratio, Crown

Mathematical primitives: calligraphic parametric sweeps, narrow Gaussian spires,
power-law unfurling, golden-spiral/phi-rectangle nesting, crowned peaked curves

Background: deep dark purple-black (#1A1420) — the regal darkness
Palette: royal purple, gold, rich burgundy, strong blue

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
from matplotlib.patches import Circle
import os


DPI=300; FIG_W=12; FIG_H=8
BG="#1A1420"

# Palette: regal — the colors of earned dignity
ROYAL="#5A2A8A"; GOLD="#D4A830"; BURGUNDY="#7A2040"; NAVY="#2A3A6A"
CROWN="#C8A020"; REGAL="#6A3090"; BANNER="#3A4A80"; CREST="#8A6020"
VELVET="#5A2060"

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
            color=(0.85,0.78,0.65,0.55),transform=ax.transData)
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

def draw_lc_gradient(ax,xs,ys,col,lw_start,lw_end,a_start,a_end,zo=4,smooth=0):
    """Draw line collection with gradient alpha and linewidth."""
    if smooth>0:
        ys=gaussian_filter1d(ys,smooth)
    pts=np.array([xs,ys]).T.reshape(-1,1,2)
    segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
    n=len(segs)
    alphas=np.linspace(a_start,a_end,n)
    lws=np.linspace(lw_start,lw_end,n)
    colors=[rgba(col,float(a)) for a in alphas]
    lc=mc.LineCollection(segs,linewidths=lws,colors=colors,
                         capstyle='round',joinstyle='round',zorder=zo)
    ax.add_collection(lc)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Ensure name ends with .pdf
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


# ===============================================================================
# 1. FLOURISH — confident calligraphic-style sweeping curves
#    parametric: x(t)=t+a*sin(2pi*t), y(t)=b*sin(pi*t)^c
# ===============================================================================
def render():
    fig,ax=make_fig()
    n=16
    for i in range(n):
        frac=i/(n-1)
        t=np.linspace(0,1,2000)
        # calligraphic sweep: horizontal with vertical flourish
        a_sweep=0.06+frac*0.08
        xs_f=PAD_L+PW*(t+a_sweep*np.sin(2*np.pi*t))
        # vertical shape: elegant arch
        c_pow=0.6+frac*0.8
        height=PH*(0.10+frac*0.75)
        ys_f=PAD_B+PH*0.06+height*np.sin(np.pi*t)**c_pow
        mask=((xs_f>PAD_L)&(xs_f<PAD_L+PW)&
              (ys_f>PAD_B)&(ys_f<PAD_B+PH))
        if mask.sum()<3: continue
        cols=[ROYAL,GOLD,BURGUNDY,REGAL,CROWN,NAVY,VELVET,CREST,
              BANNER,ROYAL,GOLD,BURGUNDY,REGAL,CROWN,NAVY,VELVET]
        col=cols[i%len(cols)]
        # variable width for calligraphic feel
        for seg_xs,seg_ys in split_segments(xs_f,ys_f,mask):
            pts=np.array([seg_xs,seg_ys]).T.reshape(-1,1,2)
            segs_lc=np.concatenate([pts[:-1],pts[1:]],axis=1)
            n_s=len(segs_lc)
            # thick at middle, thin at ends (nib effect)
            t_seg=np.linspace(0,1,n_s)
            lws=0.42+2.52*np.sin(np.pi*t_seg)*(0.5+frac*0.5)
            base_a=0.17+0.76*(1-abs(frac-0.5)*1.2)
            colors=[rgba(col,base_a) for _ in range(n_s)]
            lc=mc.LineCollection(segs_lc,linewidths=lws,colors=colors,
                                 capstyle='round',joinstyle='round',zorder=3+i)
            ax.add_collection(lc)
    label(ax,"x(t)=t+a\u00b7sin(2\u03c0t),  y(t)=H\u00b7sin(\u03c0t)^c")
    save(fig,"pride_flourish.pdf")


if __name__ == '__main__':
    render()
