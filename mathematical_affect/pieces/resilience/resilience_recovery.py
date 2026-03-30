"""
Geometry of Feeling — Resilience: Resilience Recovery
Standalone render script
"""

"""
Geometry of Feeling — Resilience (Final Series)
Five pieces: Forged, Phoenix, Recovery, Repair, Growth

Mathematical primitives: compression and deformation, cubic descent/ascent,
amplitude recovery envelopes, fracture repair with gold fill,
truncated curves with divergent regrowth branches

Background: near-black warm charcoal (#1A1818) — the forge
Palette: kintsugi gold, ember orange, steel blue, ash grey, iron

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
# 3. RECOVERY — waves knocked down, rebuilding higher
#    A(t) = (1 − 0.7·e^(−(t−t₀)²/2σ²)) · (1 + 0.3·max(2(t−0.5),0))
# ═══════════════════════════════════════════════════════════════════════════════
def render():
    fig,ax=make_fig()
    t=np.linspace(0,1,3000); xs=PAD_L+PW*t
    n=14
    for i in range(n):
        frac=i/(n-1)
        y_base=PAD_B+PH*(0.08+frac*0.80)
        # wave with amplitude that dips then recovers
        omega=8+frac*8
        # envelope: drops at t=0.3, recovers by t=0.7
        dip_center=0.35
        dip_width=0.12
        recovery=1-0.7*np.exp(-((t-dip_center)**2)/(2*dip_width**2))
        # after dip, amplitude grows higher than original
        growth=1+0.3*np.clip((t-0.5)*2,0,1)
        envelope=recovery*growth
        amp=PH*(0.010+frac*0.020)
        ys=y_base+amp*envelope*np.sin(omega*np.pi*t+frac*2)
        if frac<0.3: col=STEEL
        elif frac<0.6: col=SILVER
        else: col=BONE
        alpha_v=0.17+0.76*(1-abs(frac-0.5)*0.8)
        lw=0.56+1.26*(1-abs(frac-0.5)*0.8)
        draw_lc(ax,xs,ys,col,lw=lw,alpha=alpha_v,zo=3,smooth=2)
    # gold band at the recovery zone
    for i in range(5):
        gy=cy+PH*(0.05*i-0.10)
        ax.plot([PAD_L+PW*0.32,PAD_L+PW*0.43],[gy,gy],
                color=rgba(EMBER,0.07),linewidth=0.7,zorder=2)
    add_signature(fig, ax, BG)
    save(fig,"resilience_recovery.pdf")

if __name__ == '__main__':
    render()
