"""
Geometry of Feeling — Envy: Envy Covet
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
BG="#B0B0A8"  # mid-grey

# Palette: envious greens, sickly yellows, bitter cold accents
BILE="#7A8A30"; COVET="#3A5A30"; BITTER="#5A6A38"; ACID="#8A9A28"
JEALOUS="#4A6A3A"; THORN="#5A5A28"; PALLID="#8A9A70"; VENOM="#4A5A20"
SHADOW_COL="#4A4A40"

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
    """Split masked arrays into contiguous segments."""
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

def save(fig,name):
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR,name),
                format='pdf',facecolor=BG)
    plt.close(fig); print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def render():
    fig,ax=make_fig()
    t=np.linspace(0,1,2000); xs=PAD_L+PW*t
    # the coveted object -- a bright point above
    obj_x=cx; obj_y=PAD_B+PH*0.88
    for r,a in [(0.18,0.06),(0.10,0.14),(0.04,0.30)]:
        ax.add_patch(Circle((obj_x,obj_y),radius=r,
                    facecolor=rgba(ACID,a),edgecolor='none',zorder=7))
    n=20
    np.random.seed(44)
    for i in range(n):
        frac=i/(n-1)
        # curves rising from various starting points, curving toward the object
        x_start=PAD_L+PW*(0.05+frac*0.90)
        y_start=PAD_B+PH*(0.04+np.random.uniform(0,0.20))
        # parametric approach toward the object
        approach=1-np.exp(-3*t)
        xs_c=x_start+(obj_x-x_start)*approach
        ys_c=y_start+(obj_y-y_start)*approach*0.88  # never quite reaches
        # slight wavering
        ys_c+=PH*0.008*np.sin(8*np.pi*t+i*0.7)
        mask=((xs_c>PAD_L)&(xs_c<PAD_L+PW)&
              (ys_c>PAD_B)&(ys_c<PAD_B+PH))
        if mask.sum()<3: continue
        cols=[COVET,BITTER,JEALOUS,VENOM,BILE,THORN,SHADOW_COL,PALLID,COVET,BITTER]
        col=cols[i%len(cols)]
        for seg_xs, seg_ys in split_segments(xs_c, ys_c, mask):
            draw_lc_gradient(ax,seg_xs,seg_ys,col,
                            0.3,1.0,0.10,0.40,zo=3,smooth=4)
    add_signature(fig, ax, BG)
    save(fig,"envy_covet.pdf")

if __name__ == '__main__':
    render()
