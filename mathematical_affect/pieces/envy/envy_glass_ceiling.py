"""
Geometry of Feeling — Envy: Envy Glass Ceiling
Standalone render script
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

def label(ax,eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.15,0.15,0.20,0.28),transform=ax.transData)
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
    ceiling=PAD_B+PH*0.72
    n=22
    for i in range(n):
        frac=i/(n-1)
        y_base=PAD_B+PH*(0.04+frac*0.55)
        k=2.5+frac*4.0
        # curves that want to go higher but are capped
        raw_height=PH*(0.25+frac*0.55)
        ys=y_base+raw_height*(1-np.exp(-k*t))
        # soft clamping near the ceiling
        over=ys-ceiling
        ys=np.where(over>0,ceiling+PH*0.002*np.tanh(over/(PH*0.01)),ys)
        ys=np.minimum(ys,ceiling+PH*0.003)
        if frac<0.3: col=COVET
        elif frac<0.6: col=BITTER
        elif frac<0.8: col=BILE
        else: col=JEALOUS
        alpha=0.08+0.40*(1-abs(frac-0.5)*1.3)
        lw=0.4+0.9*(1-abs(frac-0.5))
        draw_lc(ax,xs,ys,col,lw=lw,alpha=alpha,zo=3,smooth=3)
    # the ceiling -- faint but immovable
    ax.plot([PAD_L,PAD_L+PW],[ceiling,ceiling],
            color=rgba(SHADOW_COL,0.20),linewidth=1.0,linestyle='--',zorder=6)
    # a single curve above the ceiling -- the one that got through
    ys_above=ceiling+PH*0.08+PH*0.04*np.sin(3*np.pi*t)
    draw_lc(ax,xs,ys_above,ACID,lw=1.4,alpha=0.55,zo=7,smooth=4)
    label(ax,"f(t)=min(y(t), C)")
    save(fig,"envy_glass_ceiling.pdf")


if __name__ == '__main__':
    render()
