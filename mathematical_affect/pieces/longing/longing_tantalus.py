"""
Geometry of Feeling — Longing: Longing Tantalus
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
BG="#E2DDD5"

# Palette: warm yearning tones + cool distance tones
INDIGO="#3B4F7A"; TWILIGHT="#5A4A6A"; AMBER="#B8863A"
ROSE="#8A5A5A"; HONEY="#C4A050"; DUSK="#6A5A72"
COPPER="#9A6A3A"; STEEL="#6A7888"; MIST="#9AA0B0"

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
    ceiling=PAD_B+PH*0.92; floor=PAD_B+PH*0.08
    n_up=12
    for i in range(n_up):
        frac=i/(n_up-1)
        rest_y=cy+PH*0.02*(frac-0.5)
        freq=3+frac*6
        approach=np.abs(np.sin(freq*np.pi*t))
        max_reach=ceiling-rest_y
        surge=max_reach*0.85*(1-np.exp(-3*(0.3+frac*0.7)*approach))
        ys=rest_y+surge
        ys=np.minimum(ys,ceiling-PH*0.005)
        if frac<0.35: col=STEEL
        elif frac<0.65: col=ROSE
        else: col=AMBER
        alpha=0.08+0.42*frac; lw=0.3+1.0*frac
        ax.fill_between(xs,rest_y,ys,color=rgba(col,alpha*0.15),linewidth=0,zorder=2)
        draw_lc(ax,xs,ys,col,lw=lw,alpha=alpha,zo=3,smooth=4)
    n_dn=10
    for i in range(n_dn):
        frac=i/(n_dn-1)
        rest_y=cy-PH*0.02*(frac-0.5)
        freq=2.5+frac*5
        approach=np.abs(np.sin(freq*np.pi*t+1.2))
        max_reach=rest_y-floor
        surge=max_reach*0.80*(1-np.exp(-3*(0.3+frac*0.7)*approach))
        ys=rest_y-surge
        ys=np.maximum(ys,floor+PH*0.005)
        if frac<0.35: col=MIST
        elif frac<0.65: col=INDIGO
        else: col=COPPER
        alpha=0.08+0.38*frac; lw=0.3+0.9*frac
        ax.fill_between(xs,ys,rest_y,color=rgba(col,alpha*0.15),linewidth=0,zorder=2)
        draw_lc(ax,xs,ys,col,lw=lw,alpha=alpha,zo=3,smooth=4)
    for y_b in [ceiling,floor]:
        ax.plot([PAD_L,PAD_L+PW],[y_b,y_b],color=rgba(HONEY,0.22),linewidth=1.2,zorder=6)
    add_signature(fig, ax, BG)
    save(fig,"longing_tantalus.pdf")

if __name__ == '__main__':
    render()
