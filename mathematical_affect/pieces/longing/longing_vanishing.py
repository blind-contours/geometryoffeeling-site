"""
Geometry of Feeling — Longing: Longing Vanishing
Standalone render script
"""

"""
Geometry of Feeling — Longing (Final Series)
Five pieces: Vanishing, Magnetic, Zeno, Harmonic Decay, Tantalus

Mathematical primitives: perspective convergence, dipole field arcs,
Zeno staircase accumulation, damped oscillation, bounded surge/rebound

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
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

# ═══════════════════════════════════════════════════════════════════════════════
# VANISHING POINT — parallel curves converge toward a point never reached
# y(t) = cy + d/(1+k·t)
# ═══════════════════════════════════════════════════════════════════════════════
def render():
    fig,ax=make_fig()
    t=np.linspace(0,1,1500); xs=PAD_L+PW*t
    vp_y=cy
    n=28
    offsets=np.linspace(-PH*0.44,PH*0.44,n)
    for i,d0 in enumerate(offsets):
        frac=abs(d0)/(PH*0.44)
        k=3.5
        ys=vp_y+d0/(1+k*t)
        wave=PH*0.003*(1-frac)*np.sin(5*np.pi*t+i*0.3)
        ys=ys+wave
        dist=abs(d0)/(PH*0.44)
        if dist<0.25: col=AMBER
        elif dist<0.50: col=COPPER
        elif dist<0.75: col=ROSE
        else: col=INDIGO
        alpha=0.10+0.50*(1-dist*0.5)
        lw=0.3+1.4*(1-dist*0.4)
        draw_lc(ax,xs,ys,col,lw=lw,alpha=alpha,zo=3,smooth=8)
    for r,a in [(0.15,0.06),(0.08,0.12),(0.03,0.25)]:
        ax.add_patch(Circle((PAD_L+PW*0.98,vp_y),radius=r,
                    facecolor=rgba(HONEY,a),edgecolor='none',zorder=6))
    add_signature(fig, ax, BG)
    save(fig,"longing_vanishing.pdf")

if __name__ == '__main__':
    render()
