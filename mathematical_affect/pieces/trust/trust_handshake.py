"""
Geometry of Feeling — Trust: Trust Handshake
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
    t=np.linspace(0,1,2000)

    n_pairs=9
    for i in range(n_pairs):
        frac=i/(n_pairs-1)
        # vertical spread: outermost pairs wider, inner pairs tighter
        spread=PH*(0.04+frac*0.20)
        # meeting point smoothness — logistic blend
        blend=1/(1+np.exp(-18*(t-0.5)))

        # before meeting: two separate paths from opposite sides
        # gentle oscillation fading out as they approach center
        osc_pre=spread*0.15*np.sin(8*np.pi*t+frac*2)*np.exp(-4*(t-0.2)**2)

        # upper curve: starts high on left, descends to center
        y_upper_start=cy+spread
        y_lower_start=cy-spread
        y_shared=cy+PH*0.005*np.sin(4*np.pi*t+frac*1.5)  # gentle shared wander

        y_upper=(1-blend)*(y_upper_start+osc_pre)+blend*y_shared
        y_lower=(1-blend)*(y_lower_start-osc_pre)+blend*y_shared

        xs=PAD_L+PW*t

        # at meeting point, brief intertwine — a crossing twist
        twist_amp=spread*0.12
        twist_env=np.exp(-80*(t-0.50)**2)  # very localized Gaussian at meeting
        twist=twist_amp*np.sin(16*np.pi*t+frac*1.0)*twist_env
        y_upper=y_upper+twist
        y_lower=y_lower-twist

        col1=SAGE if frac<0.5 else WILLOW
        col2=GENTLE_BLUE if frac<0.5 else TRUST_BLUE
        alpha=0.12+0.40*(1-abs(frac-0.5)*1.5)
        lw=0.5+0.9*(1-abs(frac-0.5))
        draw_lc(ax,xs,y_upper,col1,lw=lw,alpha=alpha,zo=3,smooth=5)
        draw_lc(ax,xs,y_lower,col2,lw=lw,alpha=alpha,zo=3,smooth=5)

    # very faint vertical marker at meeting point
    ax.plot([cx,cx],[PAD_B+PH*0.15,PAD_B+PH*0.85],
            color=rgba(QUIET_GOLD,0.08),linewidth=0.4,linestyle=':',zorder=2)

    label(ax,"clasp(t)=(1\u2212\u03c3(t))\u00b7separate + \u03c3(t)\u00b7together")
    save(fig,"trust_handshake.pdf")


if __name__ == '__main__':
    render()
