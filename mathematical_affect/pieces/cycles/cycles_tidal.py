"""
Geometry of Feeling — Cycles: Cycles Tidal
Standalone render script
"""

"""
Geometry of Feeling — Cycles v2 (20 candidates)
Return, repetition, the loop that never quite closes the same way.

Dependencies: matplotlib, numpy, scipy
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
from matplotlib.patches import Circle
import os


DPI=300; FIG_W=12; FIG_H=8
BG="#F0E8DA"

# Palette: seasonal color rotation
SPRING="#5A9A50"; SUMMER="#C8A030"; AUTUMN="#B85A30"; WINTER="#4A6A90"
BLOSSOM="#C87898"; HARVEST="#9A7020"; FROST="#7A90A8"; EARTH="#6A5A40"
RENEWAL="#70B060"; DUSK="#8A6A50"; SAGE="#7A9A70"; AMBER="#D0A020"
DEEP_WINTER="#2A4A6A"; MOSS="#4A6A3A"

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
            color=(0.15,0.15,0.20,0.25),transform=ax.transData)
def split_segments(xs, ys, mask):
    segments = []
    in_seg = False; start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg: start = j; in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3: segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3:
        segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax,xs,ys,col,lw,alpha,zo=4,smooth=0):
    if smooth>0: ys=gaussian_filter1d(ys,smooth)
    mask = (xs>PAD_L-0.1)&(xs<PAD_L+PW+0.1)&(ys>PAD_B-0.1)&(ys<PAD_B+PH+0.1)
    segs = split_segments(xs, ys, mask)
    for sx, sy in segs:
        if len(sx)<3: continue
        pts=np.array([sx,sy]).T.reshape(-1,1,2)
        s=np.concatenate([pts[:-1],pts[1:]],axis=1)
        lc=mc.LineCollection(s,linewidths=lw,colors=[rgba(col,alpha)],
                             capstyle='round',joinstyle='round',zorder=zo)
        ax.add_collection(lc)

def draw_lc_xy(ax,xs,ys,col,lw,alpha,zo=4):
    """Draw with clipping on both axes."""
    mask = (xs>PAD_L-0.1)&(xs<PAD_L+PW+0.1)&(ys>PAD_B-0.1)&(ys<PAD_B+PH+0.1)
    segs = split_segments(xs, ys, mask)
    for sx, sy in segs:
        if len(sx)<3: continue
        pts=np.array([sx,sy]).T.reshape(-1,1,2)
        s=np.concatenate([pts[:-1],pts[1:]],axis=1)
        lc=mc.LineCollection(s,linewidths=lw,colors=[rgba(col,alpha)],
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


# ═══════════════════════════════════════════════════════════════
# 11. TIDAL — coupled oscillators with beating
# ═══════════════════════════════════════════════════════════════
def render():
    fig,ax=make_fig()
    t=np.linspace(0,1,3000)
    xs=PAD_L+PW*t
    n_pairs=14

    for pi_idx in range(n_pairs):
        frac=pi_idx/(n_pairs-1)
        # two slightly detuned frequencies create beating
        f1=6+pi_idx*0.5
        f2=f1+0.3+0.2*frac
        signal=np.sin(2*np.pi*f1*t)+np.sin(2*np.pi*f2*t)
        y_base=PAD_B+PH*(0.06+0.88*frac)
        amplitude=PH*0.03
        ys=y_base+amplitude*signal

        if frac<0.25: col=WINTER
        elif frac<0.50: col=SPRING
        elif frac<0.75: col=SUMMER
        else: col=AUTUMN
        alpha=0.10+0.45*(1-abs(frac-0.5)*1.3)
        lw=0.4+1.2*(1-abs(frac-0.5))
        draw_lc(ax,xs,ys,col,lw=lw,alpha=alpha,zo=3+pi_idx)

    label(ax,"f(t)=sin(\u03c9\u2081t)+sin(\u03c9\u2082t)")
    save(fig,"cycles_tidal")


if __name__ == '__main__':
    render()
