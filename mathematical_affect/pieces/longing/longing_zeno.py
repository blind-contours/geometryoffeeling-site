"""
Geometry of Feeling — Longing: Longing Zeno
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
    n_paths=18
    t=np.linspace(0,1,2000); xs=PAD_L+PW*t
    for p in range(n_paths):
        frac=p/(n_paths-1)
        ceiling=PAD_B+PH*(0.15+frac*0.78)
        base=PAD_B+PH*0.04
        total_h=ceiling-base
        n_steps=20
        ys=np.zeros_like(t)
        current_h=0
        for k in range(n_steps):
            step_h=(total_h-current_h)*0.5
            step_start=k/n_steps
            step_end=(k+1)/n_steps
            mask=(t>=step_start)&(t<step_end)
            t_local=(t[mask]-step_start)/(step_end-step_start+1e-9)
            transition=1/(1+np.exp(-12*(t_local-0.5)))
            ys[mask]=base+current_h+step_h*transition
            current_h+=step_h
        ys[t>=1-1/n_steps]=base+current_h
        ys+=PH*0.002*np.sin(8*np.pi*t+frac*3)
        if frac<0.20: col=INDIGO
        elif frac<0.40: col=TWILIGHT
        elif frac<0.60: col=DUSK
        elif frac<0.80: col=ROSE
        else: col=AMBER
        alpha=0.08+0.45*(1-abs(frac-0.5)*1.5)
        lw=0.4+1.1*(1-abs(frac-0.5)*1.2)
        ax.fill_between(xs,base,ys,color=rgba(col,alpha*0.18),linewidth=0,zorder=2)
        draw_lc(ax,xs,ys,col,lw=lw,alpha=alpha,zo=3)
        ax.plot([PAD_L,PAD_L+PW],[ceiling,ceiling],
                color=rgba(col,0.06),linewidth=0.3,zorder=2)
    add_signature(fig, ax, BG)
    save(fig,"longing_zeno.pdf")

if __name__ == '__main__':
    render()
