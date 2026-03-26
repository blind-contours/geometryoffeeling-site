"""
Geometry of Feeling — Resilience: Resilience Growth
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

def label(ax,eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.85,0.80,0.65,0.55),transform=ax.transData)
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
# 5. GROWTH — truncated curves sprouting new branches from the cut
#    y(t>t_c) = y(t_c) + Σ aᵢ·(t−t_c)^(1.5+0.5i) · sin(5π(t−t_c)+φᵢ)
# ═══════════════════════════════════════════════════════════════════════════════
def render():
    fig,ax=make_fig()
    np.random.seed(808)
    t=np.linspace(0,1,2000); xs=PAD_L+PW*t
    n=14
    for i in range(n):
        frac=i/(n-1)
        y_base=PAD_B+PH*(0.08+frac*0.78)
        # original curve — truncated
        cut_point=0.35+frac*0.15
        orig_mask=t<=cut_point
        ys_orig=y_base+PH*0.01*np.sin(3*np.pi*t+frac*2)
        if frac<0.3: col=ASH
        elif frac<0.6: col=STEEL
        else: col=SILVER
        alpha_v=0.25+0.60*(1-abs(frac-0.5)*1.3)
        lw=0.70+0.98*(1-abs(frac-0.5))
        if orig_mask.sum()>=3:
            draw_lc(ax,xs[orig_mask],ys_orig[orig_mask],col,
                    lw=lw,alpha=alpha_v,zo=3,smooth=3)
        # cut mark — gold dot
        cut_idx=int(cut_point*len(t))
        if cut_idx<len(xs):
            ax.add_patch(Circle((xs[cut_idx],ys_orig[cut_idx]),
                        radius=0.03+0.015*frac,
                        facecolor=rgba(GOLD,0.60+0.30*frac),
                        edgecolor='none',zorder=6))
        # new growth — multiple branches from cut point
        n_branches=2+int(frac*2)
        for b in range(n_branches):
            b_frac=b/(max(n_branches-1,1))
            regrow_mask=t>=cut_point
            if regrow_mask.sum()<3: continue
            dt=t[regrow_mask]-cut_point
            # each branch goes in slightly different direction
            angle=PH*(0.03+b_frac*0.04)*((-1)**b)
            growth_speed=1.5+b_frac*0.5
            ys_new=ys_orig[cut_idx]+angle*dt**growth_speed/(1-cut_point)**growth_speed
            ys_new+=PH*0.005*np.sin(5*np.pi*dt/(1-cut_point)+b*1.5)
            ys_new=np.clip(ys_new,PAD_B+PH*0.02,PAD_B+PH*0.98)
            # new growth is greener/more vibrant — gold-touched
            grow_col=GOLD if b==0 else EMBER
            grow_alpha=0.34+0.51*(1-abs(frac-0.5))
            draw_lc_gradient(ax,xs[regrow_mask],ys_new,grow_col,
                            0.42,lw*0.8,0.14,grow_alpha,zo=4,smooth=3)
    label(ax,"y(t>t_c)=y(t_c)+\u03a3a\u1d62\u00b7(t\u2212t_c)^(1.5+0.5i)\u00b7sin(5\u03c0(t\u2212t_c)+\u03c6\u1d62)")
    save(fig,"resilience_growth.pdf")


if __name__ == '__main__':
    render()
