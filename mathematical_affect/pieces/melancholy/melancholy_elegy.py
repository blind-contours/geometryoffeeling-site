"""
Geometry of Feeling — Melancholy: Melancholy Elegy
Standalone render script
"""

"""
Geometry of Feeling -- Melancholy (Final Series)
Five pieces: Elegy, Lethe, Dissolve, Drift, Entropy

Melancholy is heavy, slow, quiet -- but not boring. These five pieces
achieve stillness through complexity: many layers all barely moving,
structure that is present but dimming, the weight of things slowly sinking.

Palette: slate blue, grey-mauve, faded green. Cool mid-grey background.
Mathematical primitives: slowly decaying curves, random walk with
downward drift, order dissolving into noise, forgetting, echoes fading.

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
"""

import numpy as np
import matplotlib
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

def label(ax,eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.15,0.15,0.20,0.28),transform=ax.transData)
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
# 1. ELEGY -- single strong curve surrounded by fading echoes
#    echo_n(t) = A*e^(-lambda*n) * sin(omega*(t - n*tau))
#    One voice surrounded by its own fading repetitions
# =============================================================================
def render():
    fig,ax=make_fig()
    t=np.linspace(0,1,3000); xs=PAD_L+PW*t
    omega=5*np.pi
    amp_main=PH*0.18
    ys_main=cy+amp_main*np.sin(omega*t*2)
    # echoes -- copies with decreasing amplitude and increasing phase shift
    n_echoes=16
    cols=[LAVENDER,DUSK,SLATE,RAIN,PEWTER,BRUISE,PLUM,ASH]
    for i in range(n_echoes):
        frac=(i+1)/(n_echoes+1)
        decay=np.exp(-2.5*frac)
        phase_shift=frac*1.5
        amp_echo=amp_main*decay
        # slight vertical spread
        y_offset=PH*0.04*(i-n_echoes/2)/n_echoes
        ys_echo=cy+y_offset+amp_echo*np.sin(omega*(t-phase_shift)*2)
        col=cols[i%len(cols)]
        alpha=0.06+0.25*decay
        lw=0.2+0.8*decay
        draw_lc(ax,xs,ys_echo,col,lw=lw,alpha=alpha,zo=3,smooth=3)
    # the main curve -- strongest
    draw_lc(ax,xs,ys_main,SLATE,lw=1.4,alpha=0.50,zo=5,smooth=3)
    label(ax,"echo_n(t)=Ae^(\u2212\u03bbn)\u00b7sin(\u03c9(t\u2212n\u03c4))")
    save(fig,"melancholy_elegy.pdf")


if __name__ == '__main__':
    render()
