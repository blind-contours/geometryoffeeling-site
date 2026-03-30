"""
Geometry of Feeling — Longing: Longing Magnetic
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
BG="#E2DDD5"

# Palette: warm yearning tones + cool distance tones
INDIGO="#3B4F7A"; TWILIGHT="#5A4A6A"; AMBER="#B8863A"
ROSE="#8A5A5A"; HONEY="#C4A050"; DUSK="#6A5A72"
COPPER="#9A6A3A"; STEEL="#6A7888"; MIST="#9AA0B0"

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
    pole_L=(PAD_L+PW*0.15, cy)
    pole_R=(PAD_L+PW*0.85, cy)
    n_lines=20
    for i in range(n_lines):
        frac=i/(n_lines-1)
        arc_h=PH*(0.04+frac*0.42)
        for sign in [1,-1]:
            t=np.linspace(0,1,600)
            xs_arc=pole_L[0]+(pole_R[0]-pole_L[0])*t
            ys_arc=cy+sign*4*arc_h*t*(1-t)
            mask=(ys_arc>PAD_B)&(ys_arc<PAD_B+PH)
            if mask.sum()<3: continue
            if frac<0.3: col=AMBER
            elif frac<0.6: col=COPPER
            else: col=ROSE
            alpha=0.12+0.50*(1-frac)
            lw=0.4+1.4*(1-frac)
            draw_lc(ax,xs_arc[mask],ys_arc[mask],col,lw=lw,alpha=alpha,zo=3,smooth=4)
    for px,py in [pole_L,pole_R]:
        for r,a in [(0.12,0.08),(0.06,0.18),(0.025,0.40)]:
            ax.add_patch(Circle((px,py),radius=r,
                        facecolor=rgba(HONEY,a),edgecolor='none',zorder=6))
    label(ax,"B(r)=\u03bc\u2080/(4\u03c0)\u00b7(3(m\u00b7r\u0302)r\u0302\u2212m)/r\u00b3")
    save(fig,"longing_magnetic.pdf")


if __name__ == '__main__':
    render()
