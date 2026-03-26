"""
Geometry of Feeling — Confusion: Confusion Knot
Standalone render script
"""

"""
Geometry of Feeling — Confusion (Final Series)
Five pieces: Tangle, Knot, Labyrinth, Vertigo, Aliased

Mathematical primitives: Lissajous curves with irrational ratios,
torus knot projections, maze-like random walks with right-angle turns,
conflicting clockwise/counterclockwise spirals, Moire-like aliasing artifacts

Background: #E8E4E0 (light, uncertain)
Palette: muted pastels all mixed — no color hierarchy

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os


DPI=300; FIG_W=12; FIG_H=8
BG="#E8E4E0"

# Palette: muddled, uncertain — no color dominates
MURK="#6A6A68"; TANGLE_COL="#7A6A58"; FOG="#8A8A88"
UNCERTAIN="#5A6A70"; CROSSED="#7A5A68"; KNOT_COL="#6A5A50"
HAZE="#9A9A90"; DRIFT="#5A7070"; STATIC="#7A7A80"
MAUVE="#8A6A7A"; SAGE="#6A7A68"; CLAY="#8A7A60"

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

PAD_L=0.40; PAD_R=0.30; PAD_T=0.35; PAD_B=0.60
PW=FIG_W-PAD_L-PAD_R; PH=FIG_H-PAD_T-PAD_B
cx=PAD_L+PW/2; cy=PAD_B+PH/2

def label(ax,eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.15,0.15,0.20,0.22),transform=ax.transData)
def split_segments(xs, ys, mask):
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
# 2. KNOT — mathematical trefoil knot projections
#    (p,q)-torus knot with tangling secondary curves
# ===============================================================================
def render():
    fig,ax=make_fig()
    n_knots=22
    cols=[MURK,TANGLE_COL,UNCERTAIN,CROSSED,KNOT_COL,
          DRIFT,FOG,HAZE,MAUVE,SAGE,CLAY]
    for k in range(n_knots):
        frac=k/(n_knots-1)
        t=np.linspace(0,2*np.pi,4000)
        # torus knot parametric projection with varying parameters
        p=2+k*0.08; q=3+k*0.12
        r_base=PW*0.30*(0.28+frac*0.72)
        r_mod=r_base*0.38
        xs_k=cx+(r_base+r_mod*np.cos(q*t))*np.cos(p*t)
        ys_k=cy+(r_base+r_mod*np.cos(q*t))*np.sin(p*t)*(PH/PW)
        mask=((xs_k>PAD_L)&(xs_k<PAD_L+PW)&
              (ys_k>PAD_B)&(ys_k<PAD_B+PH))
        col=cols[k%len(cols)]
        for seg_xs, seg_ys in split_segments(xs_k, ys_k, mask):
            alpha=0.08+0.40*(1-abs(frac-0.5)*1.2)
            lw=0.35+1.2*(1-abs(frac-0.5))
            draw_lc(ax,seg_xs,seg_ys,col,lw=lw,alpha=alpha,zo=3+k,smooth=2)

    # additional tangling curves weaving through the knots
    for i in range(34):
        frac=i/33
        t=np.linspace(0,2*np.pi,2000)
        r=PW*0.42*(0.18+frac*0.82)
        # different harmonic ratios for each
        xs_t=cx+r*np.sin(3*t+frac*np.pi)
        ys_t=cy+r*0.70*np.cos(2*t+frac*1.8)
        mask=((xs_t>PAD_L)&(xs_t<PAD_L+PW)&
              (ys_t>PAD_B)&(ys_t<PAD_B+PH))
        for seg_xs, seg_ys in split_segments(xs_t, ys_t, mask):
            col=cols[i%len(cols)]
            draw_lc(ax,seg_xs,seg_ys,col,lw=0.28,alpha=0.04+frac*0.10,zo=2,smooth=3)
    label(ax,"(p,q)-torus knot projection")
    save(fig,"confusion_knot.pdf")


if __name__ == '__main__':
    render()
