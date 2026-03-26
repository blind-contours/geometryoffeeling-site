"""
Geometry of Feeling — Shame: Shame Contraction
Standalone render script
"""

"""
Geometry of Feeling — Shame (Final Series)
Five pieces: Shrink, Contraction, Fold, Crumple, Veil

Mathematical primitives: logarithmic spirals collapsing inward,
contraction mappings, lemniscate self-intersections,
progressive frequency crumpling, semi-transparent layered obscuration

Background: #3A3430 (warm dim — curtains drawn)
Palette: muddy brown, dark grey, washed-out burgundy

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
BG="#3A3430"

# Palette: muddy brown, dark grey, washed-out burgundy
UMBER="#5A4A38"; SHADOW="#3A3028"; FLUSH="#8A4A40"
HIDE="#4A4038"; SMOKE="#6A6058"; EMBER="#7A5030"
COPPER="#8A6A48"; DUST="#6A5A48"; VEIL_COL="#5A5048"
BURGUNDY="#6A3838"; MUDDY="#5A5040"; ASHEN="#4A4A44"

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
            color=(0.85,0.78,0.68,0.40),transform=ax.transData)
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
# 2. CONTRACTION — curves getting smaller with each iteration
#    f_n(t) = c^n * f(t), c<1 — contraction mapping
# ===============================================================================
def render():
    fig,ax=make_fig()
    t=np.linspace(0,2*np.pi,2000)
    n=22
    c=0.88  # contraction factor
    for i in range(n):
        frac=i/(n-1)
        scale=c**i
        # elliptical shape contracting with slight rotation
        a=PW*0.46*scale
        b=PH*0.44*scale
        rotation=i*0.12
        xs_e=cx+a*np.cos(t+rotation)*np.cos(i*0.08)-b*np.sin(t+rotation)*np.sin(i*0.08)
        ys_e=cy+a*np.cos(t+rotation)*np.sin(i*0.08)+b*np.sin(t+rotation)*np.cos(i*0.08)
        mask=((xs_e>PAD_L)&(xs_e<PAD_L+PW)&
              (ys_e>PAD_B)&(ys_e<PAD_B+PH))
        if mask.sum()<3: continue
        if frac<0.20: col=COPPER
        elif frac<0.40: col=UMBER
        elif frac<0.60: col=DUST
        elif frac<0.80: col=SMOKE
        else: col=SHADOW
        alpha=0.15+0.70*scale
        lw=0.35+1.75*scale
        for seg_xs, seg_ys in split_segments(xs_e, ys_e, mask):
            draw_lc(ax,seg_xs,seg_ys,col,lw=lw,alpha=alpha,zo=3,smooth=2)
    # faint inner mark at the fixed point
    from matplotlib.patches import Circle
    for r_c,a_c in [(0.05,0.14),(0.02,0.25)]:
        ax.add_patch(Circle((cx,cy),radius=r_c,
                    facecolor=rgba(BURGUNDY,a_c),edgecolor='none',zorder=2))
    label(ax,"f_n=c^n\u00b7f,  c=0.88")
    save(fig,"shame_contraction.pdf")


if __name__ == '__main__':
    render()
