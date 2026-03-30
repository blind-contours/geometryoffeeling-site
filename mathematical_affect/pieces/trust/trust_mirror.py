"""
Geometry of Feeling — Trust: Trust Mirror
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
BG="#F2F0EC"  # very light — trust is an open space

# Palette: soft sage, warm white, gentle blue, pale green, quiet gold
SAGE="#6A9878"; WARM_WHITE="#E8E0D8"; GENTLE_BLUE="#7090B0"
PALE_GREEN="#88B898"; QUIET_GOLD="#B8A870"
DOVE="#A0A8A0"; WILLOW="#7A9A78"; CALM="#8098A8"
LINEN="#D8D0C0"; TRUST_BLUE="#6888A8"

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
            color=(0.20,0.25,0.20,0.22),transform=ax.transData)
def split_segments(xs, ys, mask):
    """Split masked arrays into contiguous segments to avoid straight-line jumps."""
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
    t=np.linspace(0,1,2000); xs=PAD_L+PW*t
    n_pairs=7
    for i in range(n_pairs):
        frac=i/(n_pairs-1)
        # generate rich waveform
        freq1=1.5+frac*2
        freq2=freq1*1.618
        amp=PH*(0.04+frac*0.06)
        f_base=amp*(np.sin(2*np.pi*freq1*t)+0.4*np.sin(2*np.pi*freq2*t+0.5))
        y1=cy+f_base
        # near-perfect mirror with tiny imperfection
        epsilon=PH*0.003*np.sin(15*np.pi*t+i*2.0)
        y2=2*cy-y1+epsilon
        mask1=((y1>PAD_B)&(y1<PAD_B+PH))
        mask2=((y2>PAD_B)&(y2<PAD_B+PH))
        col1=SAGE if frac<0.5 else WILLOW
        col2=GENTLE_BLUE if frac<0.5 else TRUST_BLUE
        alpha=0.12+0.40*(1-abs(frac-0.5)*1.5)
        lw=0.6+0.8*(1-abs(frac-0.5))
        for sx,sy in split_segments(xs,y1,mask1):
            draw_lc(ax,sx,sy,col1,lw=lw,alpha=alpha,zo=3,smooth=3)
        for sx,sy in split_segments(xs,y2,mask2):
            draw_lc(ax,sx,sy,col2,lw=lw,alpha=alpha,zo=3,smooth=3)
    # axis of symmetry
    ax.plot([PAD_L,PAD_L+PW],[cy,cy],
            color=rgba(LINEN,0.18),linewidth=0.5,linestyle='--',zorder=2)
    label(ax,"y\u2082(t)=2c\u2212y\u2081(t)+\u03b5")
    save(fig,"trust_mirror.pdf")


if __name__ == '__main__':
    render()
