"""
Geometry of Feeling — Shame: Shame Crumple
Standalone render script
"""

"""
Geometry of Feeling — Shame (Final Series)
Five pieces: Shrink, Contraction, Fold, Crumple, Veil

Mathematical primitives: logarithmic spirals collapsing inward,
contraction mappings, lemniscate self-intersections,
progressive frequency crumpling, semi-transparent layered obscuration

Background: #3A3430 (warm dim — curtains drawn)
Palette: muddy brown, dark grey, washed-out burgundy

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
BG="#3A3430"

# Palette: muddy brown, dark grey, washed-out burgundy
UMBER="#5A4A38"; SHADOW="#3A3028"; FLUSH="#8A4A40"
HIDE="#4A4038"; SMOKE="#6A6058"; EMBER="#7A5030"
COPPER="#8A6A48"; DUST="#6A5A48"; VEIL_COL="#5A5048"
BURGUNDY="#6A3838"; MUDDY="#5A5040"; ASHEN="#4A4A44"

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

def draw_lc_gradient(ax,xs,ys,col,lw_start,lw_end,a_start,a_end,zo=4,smooth=0):
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

# ===============================================================================
# 4. CRUMPLE — a smooth curve that progressively folds back on itself
#    amplitude decreases while frequency increases toward center
#    like crumpling paper: the exterior is wide, the interior is compressed
# ===============================================================================
def render():
    fig,ax=make_fig()
    n_curves=18
    for i in range(n_curves):
        frac=i/(n_curves-1)
        t=np.linspace(0,1,4000)
        xs=PAD_L+PW*t
        y_base=PAD_B+PH*(0.06+frac*0.85)

        # crumple: frequency increases toward center, amplitude decreases
        # this creates a curve that starts smooth and becomes increasingly
        # crumpled/compressed in the middle
        center=0.5
        dist_from_center=np.abs(t-center)
        # frequency: low at edges, high near center
        local_freq=4+60*(1-dist_from_center)**3
        # amplitude: high at edges, low near center (crumpling = compression)
        local_amp=PH*(0.04+frac*0.03)*(0.08+dist_from_center*1.8)
        local_amp=np.clip(local_amp,0,PH*0.06)
        # phase accumulation for continuous curve
        phase=np.cumsum(local_freq*np.pi/len(t)*2)
        ys=y_base+local_amp*np.sin(phase+frac*2.5)

        ys=np.clip(ys,PAD_B,PAD_B+PH)

        if frac<0.20: col=UMBER
        elif frac<0.40: col=FLUSH
        elif frac<0.60: col=BURGUNDY
        elif frac<0.80: col=DUST
        else: col=SMOKE
        # alpha and linewidth: stronger in middle zone, fading at edges
        base_alpha=0.17+0.82*(1-abs(frac-0.5)*1.3)
        base_lw=0.42+1.54*(1-abs(frac-0.5))

        # segment-level alpha variation — denser in center
        pts=np.array([xs,ys]).T.reshape(-1,1,2)
        segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
        n_s=len(segs)
        # make center segments slightly brighter
        center_boost=np.exp(-((t[:-1]-0.5)**2)/(2*0.15**2))
        seg_alphas=[float(base_alpha*(0.6+0.4*cb)) for cb in center_boost]
        seg_lws=[float(base_lw*(0.7+0.3*cb)) for cb in center_boost]
        colors=[rgba(col,a) for a in seg_alphas]
        lc=mc.LineCollection(segs,linewidths=seg_lws,colors=colors,
                             capstyle='round',joinstyle='round',zorder=3)
        ax.add_collection(lc)

    # faint vertical emphasis at center — the crumple zone
    ax.plot([cx,cx],[PAD_B+PH*0.05,PAD_B+PH*0.95],
            color=rgba(SHADOW,0.085),linewidth=0.56,linestyle=':',zorder=2)
    add_signature(fig, ax, BG)
    save(fig,"shame_crumple.pdf")

if __name__ == '__main__':
    render()
