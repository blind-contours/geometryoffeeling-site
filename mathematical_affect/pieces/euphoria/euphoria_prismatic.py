"""
Geometry of Feeling — Euphoria: Euphoria Prismatic
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
    t=np.linspace(0,1,3000); xs=PAD_L+PW*t
    # spectrum colors in order
    spectrum=[ULTRAVIOLET,ELECTRIC_VIOLET,MAGENTA,HOT_PINK,PLASMA,
              FLASH_ORANGE,ACID_YELLOW,NEON_GREEN,VIVID_CYAN]
    n_bands=len(spectrum)
    # converge on left, diverge on right — prism refraction
    for i,col in enumerate(spectrum):
        frac=i/(n_bands-1)
        # vertical spread increases with x
        spread=PH*0.005+PH*0.08*frac  # per-band offset at max
        divergence=t**1.5  # nonlinear divergence
        y_center=cy
        offset=(frac-0.5)*2  # -1 to 1
        ys=y_center+offset*spread*divergence*(1+PH*0.5)
        # add subtle wavelike undulation
        wave_amp=PH*0.008*(1+t*2)
        ys=ys+wave_amp*np.sin(12*np.pi*t+frac*np.pi*0.5)
        # multiple passes for thickness
        for j in range(5):
            y_shift=PH*0.003*(j-2)
            alpha=0.60-abs(j-2)*0.12
            lw=2.0-abs(j-2)*0.4
            draw_lc(ax,xs,ys+y_shift,col,lw=lw,alpha=alpha,zo=3+j,smooth=3)
    # white convergence line on far left
    draw_lc(ax,xs[:300],np.full(300,cy),WHITE_HOT,lw=3.0,alpha=0.35,zo=6)
    label(ax,"n(\u03bb)\u00b7sin(\u03b8)=\u0394")
    save(fig,"euphoria_prismatic.pdf")


if __name__ == '__main__':
    render()
