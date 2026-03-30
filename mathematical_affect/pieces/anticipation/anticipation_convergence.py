"""
Geometry of Feeling — Anticipation: Anticipation Convergence
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
BG="#F8F6F2"

# Palette: dawn — the colors just before the sun rises
PALE_GOLD="#D4B870"; SOFT_PEACH="#D8A080"; LILAC="#9888B8"
DAWN_BLUE="#7898C0"; BLUSH="#C8908A"; APRICOT="#D89860"
CREAM_ROSE="#C8A098"; SOFT_AMBER="#C8A048"; PALE_VIOLET="#A890C0"
WARM_GREY="#A09888"; FAINT_CORAL="#C09080"; HORIZON="#88A8C8"

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
            color=(0.25,0.22,0.18,0.22),transform=ax.transData)
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
    np.random.seed(42)
    target_x=PAD_L+PW*0.88; target_y=cy
    n_walks=30
    for i in range(n_walks):
        frac=i/(n_walks-1)
        # start from left edge, scattered vertically
        x0=PAD_L+PW*0.03
        y0=PAD_B+PH*(0.05+frac*0.90)
        n_steps=800
        t=np.linspace(0,1,n_steps)
        # drift toward target with random noise
        drift_x=(target_x-x0)
        drift_y=(target_y-y0)
        noise_scale=PH*0.015*(1-t)  # noise decreases as they converge
        xs_w=x0+drift_x*t+np.cumsum(np.random.randn(n_steps)*noise_scale/n_steps**0.5)
        ys_w=y0+drift_y*t+np.cumsum(np.random.randn(n_steps)*noise_scale/n_steps**0.5)
        # boundary check
        mask=((xs_w>PAD_L)&(xs_w<PAD_L+PW)&
              (ys_w>PAD_B)&(ys_w<PAD_B+PH))
        if mask.sum()<3: continue
        cols=[DAWN_BLUE,LILAC,SOFT_PEACH,PALE_GOLD,BLUSH,
              HORIZON,PALE_VIOLET,APRICOT,CREAM_ROSE,WARM_GREY]
        col=cols[i%len(cols)]
        draw_lc_gradient(ax,xs_w[mask],ys_w[mask],col,
                        0.3,0.8,0.08,0.35,zo=3,smooth=4)
    # target glow
    for r,a in [(0.15,0.04),(0.08,0.10),(0.03,0.22)]:
        ax.add_patch(Circle((target_x,target_y),radius=r,
                    facecolor=rgba(PALE_GOLD,a),edgecolor='none',zorder=6))
    label(ax,"dX=\u03bc\u00b7dt+\u03c3(1\u2212t)\u00b7dW")
    save(fig,"anticipation_convergence.pdf")


if __name__ == '__main__':
    render()
