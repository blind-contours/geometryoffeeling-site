"""
Geometry of Feeling — Euphoria: Euphoria Firework
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
BG="#FEFCF8"  # near-white — the flash of too much light

# Palette: electric, oversaturated, almost painful
ELECTRIC_VIOLET="#8828D0"; HOT_PINK="#E02888"; ACID_YELLOW="#D8D020"
VIVID_CYAN="#20C8D0"; FLASH_ORANGE="#F08020"
MAGENTA="#D020A0"; NEON_GREEN="#40E040"; ULTRAVIOLET="#6020E0"
PLASMA="#E848A0"; WHITE_HOT="#F8F0E0"

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
            color=(0.35,0.20,0.40,0.22),transform=ax.transData)
def split_segments(xs, ys, mask):
    """Split masked arrays into contiguous segments to avoid straight-line jumps."""
    segments = []
    in_seg = False
    start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j; in_seg = True
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

def save(fig,name):
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR,name),
                format='pdf',facecolor=BG)
    plt.close(fig); print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def render():
    fig,ax=make_fig()
    np.random.seed(88)
    burst_configs=[
        (PAD_L+PW*0.18, cy+PH*0.25, HOT_PINK),
        (PAD_L+PW*0.42, cy+PH*0.35, ACID_YELLOW),
        (cx, cy+PH*0.10, VIVID_CYAN),
        (PAD_L+PW*0.68, cy+PH*0.30, FLASH_ORANGE),
        (PAD_L+PW*0.85, cy+PH*0.15, ELECTRIC_VIOLET),
        (PAD_L+PW*0.30, cy-PH*0.05, NEON_GREEN),
        (PAD_L+PW*0.75, cy-PH*0.10, MAGENTA),
    ]
    for bx,by,col in burst_configs:
        n_particles=35
        for p in range(n_particles):
            angle=2*np.pi*p/n_particles+np.random.uniform(-0.08,0.08)
            speed=PH*(0.20+np.random.uniform(0,0.30))
            t_pts=np.linspace(0,0.55,400)
            xs_p=bx+speed*np.cos(angle)*t_pts
            ys_p=by+speed*np.sin(angle)*t_pts-PH*0.7*t_pts**2
            mask=((xs_p>PAD_L)&(xs_p<PAD_L+PW)&
                  (ys_p>PAD_B)&(ys_p<PAD_B+PH))
            if mask.sum()<3: continue
            pts=np.array([xs_p[mask],ys_p[mask]]).T.reshape(-1,1,2)
            segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
            n_s=len(segs)
            alphas=np.linspace(0.65,0.02,n_s)
            lws=np.linspace(1.8,0.2,n_s)
            colors=[rgba(col,float(a)) for a in alphas]
            lc=mc.LineCollection(segs,linewidths=lws,colors=colors,
                                 capstyle='round',zorder=3)
            ax.add_collection(lc)
        # burst glow
        for r,a in [(0.20,0.05),(0.10,0.12),(0.04,0.30)]:
            ax.add_patch(Circle((bx,by),radius=r,
                        facecolor=rgba(col,a),edgecolor='none',zorder=5))
    label(ax,"r(t)=v\u2080t,  y\u2212=\u00bdgt\u00b2")
    save(fig,"euphoria_firework.pdf")


if __name__ == '__main__':
    render()
