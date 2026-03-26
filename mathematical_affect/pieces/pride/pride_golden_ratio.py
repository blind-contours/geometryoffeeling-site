"""
Geometry of Feeling — Pride: Pride Golden Ratio
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
# 4. GOLDEN RATIO — phi-based proportions in nested rectangles and spiral
#    r(theta) = a*phi^(2*theta/pi), the golden spiral
#    ENLARGED: spiral scale and rectangle sizes increased to fill ~80% of canvas
# ===============================================================================
def render():
    fig,ax=make_fig()
    phi=(1+np.sqrt(5))/2
    # golden spiral — enlarged: increase base scale factor
    n_spirals=8
    for i in range(n_spirals):
        frac=i/(n_spirals-1)
        theta=np.linspace(0,4*np.pi,2000)
        a=PW*0.008*(1+frac*0.8)  # increased from 0.005
        r=a*phi**(2*theta/np.pi)
        xs_s=cx+r*np.cos(theta+frac*np.pi/4)
        ys_s=cy+r*np.sin(theta+frac*np.pi/4)*(PH/PW)
        mask=((xs_s>PAD_L)&(xs_s<PAD_L+PW)&
              (ys_s>PAD_B)&(ys_s<PAD_B+PH))
        if mask.sum()<3: continue
        cols=[GOLD,ROYAL,CROWN,REGAL,BURGUNDY,NAVY,CREST,VELVET]
        col=cols[i%len(cols)]
        for seg_xs,seg_ys in split_segments(xs_s,ys_s,mask):
            draw_lc_gradient(ax,seg_xs,seg_ys,col,
                            0.56,2.1,0.17,0.93,zo=3+i,smooth=3)
    # golden rectangles — concentric, enlarged to fill ~80% of canvas
    n_rects=10
    for k in range(n_rects):
        scale=phi**(-k)*PW*0.48    # increased from 0.44
        scale_y=phi**(-k)*PH*0.48  # increased from 0.44
        rect_alpha=0.085+0.24*(1-k/n_rects)
        col=GOLD if k%2==0 else CROWN
        x1,x2=cx-scale,cx+scale
        y1,y2=cy-scale_y,cy+scale_y
        rect_xs=np.array([x1,x2,x2,x1,x1])
        rect_ys=np.array([y1,y1,y2,y2,y1])
        draw_lc(ax,rect_xs,rect_ys,col,lw=0.7,alpha=rect_alpha,zo=2)
    label(ax,"r(\u03b8)=a\u00b7\u03c6^(2\u03b8/\u03c0),  \u03c6=(1+\u221a5)/2")
    save(fig,"pride_golden_ratio.pdf")


if __name__ == '__main__':
    render()
