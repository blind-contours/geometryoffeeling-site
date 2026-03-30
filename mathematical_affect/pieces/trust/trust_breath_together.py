"""
Geometry of Feeling — Trust: Trust Breath Together
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
# 5. BREATH TOGETHER — two sine waves with slightly different periods,
#    gradually synchronizing
#    y1 = sin(omega1*t),  y2 = sin(omega2(t)*t),  omega2(t) -> omega1
# =============================================================================
def render():
    fig,ax=make_fig()
    t=np.linspace(0,1,2000); xs=PAD_L+PW*t
    n_pairs=7
    for i in range(n_pairs):
        frac=i/(n_pairs-1)
        omega1=4+frac*3
        # omega2 starts different, converges to omega1
        omega2_start=omega1*(1.4-frac*0.3)
        omega2=omega1+(omega2_start-omega1)*np.exp(-4*t)
        amp=PH*0.04
        y_base=PAD_B+PH*(0.08+frac*0.84)
        y1=y_base+amp*np.sin(2*np.pi*omega1*t)
        y2=y_base+amp*np.sin(2*np.pi*omega2*t)
        col1=SAGE if frac<0.5 else WILLOW
        col2=GENTLE_BLUE if frac<0.5 else TRUST_BLUE
        alpha=0.30+0.60*(1-abs(frac-0.5)*1.2)
        lw=0.85+1.0*(1-abs(frac-0.5))
        draw_lc(ax,xs,y1,col1,lw=lw,alpha=alpha,zo=3,smooth=2)
        draw_lc(ax,xs,y2,col2,lw=lw,alpha=alpha,zo=3,smooth=2)
        # faint fill where they coincide (right side)
        diff=np.abs(y1-y2)
        for j in range(0,len(t)-1,4):
            if diff[j]<amp*0.3:
                ax.fill([xs[j],xs[j+1],xs[j+1],xs[j]],
                        [min(y1[j],y2[j]),min(y1[j+1],y2[j+1]),
                         max(y1[j+1],y2[j+1]),max(y1[j],y2[j])],
                        color=rgba(LINEN,0.10),linewidth=0,zorder=2)
    add_signature(fig, ax, BG)
    save(fig,"trust_breath_together.pdf")

if __name__ == '__main__':
    render()
