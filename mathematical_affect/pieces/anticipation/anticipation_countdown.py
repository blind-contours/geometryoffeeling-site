"""
Geometry of Feeling — Anticipation: Anticipation Countdown
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
BG="#F8F6F2"

# Palette: dawn — the colors just before the sun rises
PALE_GOLD="#D4B870"; SOFT_PEACH="#D8A080"; LILAC="#9888B8"
DAWN_BLUE="#7898C0"; BLUSH="#C8908A"; APRICOT="#D89860"
CREAM_ROSE="#C8A098"; SOFT_AMBER="#C8A048"; PALE_VIOLET="#A890C0"
WARM_GREY="#A09888"; FAINT_CORAL="#C09080"; HORIZON="#88A8C8"

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
    n_marks=40
    # geometric spacing — marks get closer together toward right
    positions=1-np.geomspace(0.01,1,n_marks)[::-1]
    for i,pos in enumerate(positions):
        frac=i/(n_marks-1)
        x=PAD_L+PW*pos
        # height increases as marks get closer
        h=PH*(0.20+frac*0.70)
        y_bot=cy-h/2; y_top=cy+h/2
        if frac<0.3: col=DAWN_BLUE
        elif frac<0.6: col=LILAC
        elif frac<0.8: col=SOFT_PEACH
        else: col=PALE_GOLD
        alpha=0.08+0.50*frac
        lw=0.3+1.5*frac
        ax.plot([x,x],[y_bot,y_top],color=rgba(col,alpha),
                linewidth=lw,solid_capstyle='round',zorder=3)
    # connecting curves through the tops and bottoms
    xs_top=[PAD_L+PW*p for p in positions]
    ys_top=[cy+PH*(0.10+i/(n_marks-1)*0.35) for i in range(n_marks)]
    ys_bot=[cy-PH*(0.10+i/(n_marks-1)*0.35) for i in range(n_marks)]
    draw_lc(ax,np.array(xs_top),np.array(ys_top),PALE_GOLD,lw=0.5,alpha=0.15,zo=2,smooth=3)
    draw_lc(ax,np.array(xs_top),np.array(ys_bot),DAWN_BLUE,lw=0.5,alpha=0.15,zo=2,smooth=3)
    add_signature(fig, ax, BG)
    save(fig,"anticipation_countdown.pdf")

if __name__ == '__main__':
    render()
