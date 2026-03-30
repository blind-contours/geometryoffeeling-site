"""
Geometry of Feeling — Resilience: Resilience Repair
Standalone render script
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

def save(fig,name):
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR,name),
                format='pdf',facecolor=BG)
    plt.close(fig); print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def render():
    fig,ax=make_fig()
    np.random.seed(101)
    t=np.linspace(0,1,3000); xs=PAD_L+PW*t
    n=18
    for i in range(n):
        frac=i/(n-1)
        y_base=PAD_B+PH*(0.06+frac*0.84)
        # gentle curve
        ys=y_base+PH*0.03*np.sin(2*np.pi*t+frac*3)
        # fracture points — random breaks
        n_breaks=3+int(frac*4)
        break_positions=np.sort(np.random.uniform(0.1,0.9,n_breaks))
        break_width=0.015+frac*0.008
        if frac<0.3: col=ASH
        elif frac<0.6: col=STEEL
        else: col=SILVER
        # draw the curve in segments between breaks
        prev=0
        for bp in break_positions:
            bp_start=max(0,bp-break_width)
            bp_end=min(1,bp+break_width)
            seg_mask=(t>=prev)&(t<=bp_start)
            if seg_mask.sum()>=3:
                draw_lc(ax,xs[seg_mask],ys[seg_mask],col,
                        lw=0.5+0.8*(1-abs(frac-0.5)),
                        alpha=0.15+0.40*(1-abs(frac-0.5)),zo=3,smooth=3)
            # gold repair at break
            repair_mask=(t>=bp_start)&(t<=bp_end)
            if repair_mask.sum()>=3:
                # slight vertical offset at break — the scar is visible
                ys_repair=ys[repair_mask]+PH*0.004*np.sin(np.pi*(t[repair_mask]-bp_start)/(bp_end-bp_start))
                draw_lc(ax,xs[repair_mask],ys_repair,GOLD,
                        lw=1.0+1.2*frac,alpha=0.45+0.35*frac,zo=5,smooth=1)
            prev=bp_end
        # final segment after last break
        seg_mask=t>=prev
        if seg_mask.sum()>=3:
            draw_lc(ax,xs[seg_mask],ys[seg_mask],col,
                    lw=0.5+0.8*(1-abs(frac-0.5)),
                    alpha=0.15+0.40*(1-abs(frac-0.5)),zo=3,smooth=3)
    label(ax,"y(t)=y\u2080+A\u00b7sin(2\u03c0t) ; y_r=y(t_b)+\u03b4\u00b7sin(\u03c0(t\u2212t_b)/w)")
    save(fig,"resilience_repair.pdf")


if __name__ == '__main__':
    render()
