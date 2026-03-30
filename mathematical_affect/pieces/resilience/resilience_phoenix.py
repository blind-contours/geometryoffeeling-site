"""
Geometry of Feeling — Resilience: Resilience Phoenix
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
BG="#1A1818"

# Palette: kintsugi — gold at the breaks, warmth in the repair
GOLD="#C4A030"; EMBER="#B85A30"; STEEL="#5A7088"
ASH="#4A4A4A"; IRON="#3A3A3E"; SILVER="#8A8A90"
FLAME="#D07030"; RUST="#8A5030"; BONE="#B0A890"

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
    t=np.linspace(0,1,2000); xs=PAD_L+PW*t
    n=18
    for i in range(n):
        frac=i/(n-1)
        # descent then ascent — cubic with minimum
        t0=0.35+frac*0.08  # nadir shifts slightly
        depth=PH*(0.10+frac*0.18)
        rise=PH*(0.15+frac*0.25)  # rises HIGHER than it fell
        ratio=np.clip((t-t0)/(1-t0),0,None)
        ys=np.where(t<t0,
                    cy-depth*((t-t0)/t0)**2+PH*0.02*frac,
                    cy-depth+rise*ratio**1.5+PH*0.02*frac)
        ys=np.clip(ys,PAD_B+PH*0.02,PAD_B+PH*0.98)
        if frac<0.3: col=RUST
        elif frac<0.5: col=EMBER
        elif frac<0.7: col=FLAME
        else: col=GOLD
        alpha_v=0.10+0.50*(1-abs(frac-0.5)*1.2)
        lw=0.4+1.2*(1-abs(frac-0.5))
        draw_lc(ax,xs,ys,col,lw=lw,alpha=alpha_v,zo=3,smooth=5)
        # gold glow at the nadir — the turning point
        nadir_idx=int(t0*len(t))
        if nadir_idx<len(xs):
            ax.add_patch(Circle((xs[nadir_idx],ys[nadir_idx]),
                        radius=0.03+0.015*frac,
                        facecolor=rgba(GOLD,0.15+0.20*frac),
                        edgecolor='none',zorder=6))
    add_signature(fig, ax, BG)
    save(fig,"resilience_phoenix.pdf")

if __name__ == '__main__':
    render()
