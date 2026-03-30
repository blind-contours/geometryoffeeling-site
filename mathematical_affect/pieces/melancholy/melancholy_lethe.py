"""
Geometry of Feeling — Melancholy: Melancholy Lethe
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
import os

DPI=300; FIG_W=12; FIG_H=8
BG="#888888"  # cool mid-grey -- heavier than grief's grey

# Palette: slate blue, grey-mauve, faded green, desaturated cool tones
SLATE="#6A7080"; LAVENDER="#7A7090"; PEWTER="#8A8A90"
DUSK="#5A5A70"; PLUM="#6A5A78"; ASH="#9A9A98"
RAIN="#6A7A88"; BRUISE="#5A5068"; DOVE="#A0A0A0"

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
    """Split masked arrays into contiguous segments to avoid straight-line jumps
    when a curve exits and re-enters the boundary."""
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
    np.random.seed(160)
    t=np.linspace(0,1,2500); xs=PAD_L+PW*t
    n=18
    cols=[PLUM,DUSK,LAVENDER,BRUISE,SLATE,RAIN,PEWTER,ASH,DOVE,PLUM]
    y_eq=cy  # equilibrium -- all curves forget toward the same level
    for i in range(n):
        frac=i/(n-1)
        # diverse initial conditions
        y0=PAD_B+PH*(0.08+frac*0.84)
        lam=2.0+frac*1.5
        # forgetting: exponential relaxation toward equilibrium
        memory=np.exp(-lam*t)
        ys_deterministic=y0*memory+y_eq*(1-memory)
        # noise grows as memory fades
        noise_amp=PH*0.015*(1-memory)
        noise=gaussian_filter1d(np.random.randn(len(t)),8)*noise_amp
        ys=ys_deterministic+noise
        col=cols[i%len(cols)]
        # alpha decreases as the curve forgets
        pts=np.array([xs,ys]).T.reshape(-1,1,2)
        segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
        base_alpha=0.12+0.35*(0.5+0.5*np.sin(np.pi*frac))
        mem_env=0.3+0.7*memory[:-1]
        seg_alphas=[float(base_alpha*m) for m in mem_env]
        colors_seg=[rgba(col,a) for a in seg_alphas]
        base_lw=0.4+0.9*(0.5+0.5*np.sin(np.pi*frac))
        lws=[float(base_lw*max(0.15,m)) for m in mem_env]
        lc=mc.LineCollection(segs,linewidths=lws,colors=colors_seg,
                             capstyle='round',zorder=3)
        ax.add_collection(lc)
    # faint equilibrium line
    ax.plot([PAD_L,PAD_L+PW],[y_eq,y_eq],
            color=rgba(DOVE,0.08),linewidth=0.4,linestyle=':',zorder=2)
    add_signature(fig, ax, BG)
    save(fig,"melancholy_lethe.pdf")

if __name__ == '__main__':
    render()
