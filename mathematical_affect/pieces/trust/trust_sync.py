"""
Geometry of Feeling — Trust: Trust Sync
Standalone render script
"""

"""
Geometry of Feeling — Trust (Final Series)
Five pieces: Sync, Handshake, Weave, Mirror, Breath Together

Mathematical primitives: Kuramoto coupled oscillators, parametric clasp,
alternating-zorder sinusoidal weave, near-perfect reflection, frequency convergence

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

# =============================================================================
# 1. SYNC — two oscillators gradually synchronizing (Kuramoto model)
#    dtheta_i/dt = omega_i + K*sin(theta_j - theta_i)
# =============================================================================
def render():
    fig,ax=make_fig()
    dt=0.002; steps=2000
    t_arr=np.arange(steps)*dt
    xs=PAD_L+PW*t_arr/t_arr[-1]
    n_pairs=8
    for p in range(n_pairs):
        frac=p/(n_pairs-1)
        omega1=4*np.pi+frac*2*np.pi
        omega2=6*np.pi-frac*1.5*np.pi
        K=3.0+frac*4.0  # coupling strength
        theta1=np.zeros(steps); theta2=np.zeros(steps)
        theta1[0]=0; theta2[0]=np.pi*(0.5+frac*0.8)
        for s in range(1,steps):
            d1=omega1+K*np.sin(theta2[s-1]-theta1[s-1])
            d2=omega2+K*np.sin(theta1[s-1]-theta2[s-1])
            theta1[s]=theta1[s-1]+d1*dt
            theta2[s]=theta2[s-1]+d2*dt
        amp=PH*0.04
        y_base=PAD_B+PH*(0.08+frac*0.84)
        y1=y_base+amp*np.sin(theta1)
        y2=y_base+amp*np.sin(theta2)
        col1=SAGE if frac<0.5 else WILLOW
        col2=GENTLE_BLUE if frac<0.5 else TRUST_BLUE
        alpha=0.35+0.55*(1-abs(frac-0.5)*0.8)
        lw=0.85+1.1*(1-abs(frac-0.5))
        draw_lc(ax,xs,y1,col1,lw=lw,alpha=alpha,zo=3,smooth=3)
        draw_lc(ax,xs,y2,col2,lw=lw,alpha=alpha,zo=3,smooth=3)
    add_signature(fig, ax, BG)
    save(fig,"trust_sync.pdf")

if __name__ == '__main__':
    render()
