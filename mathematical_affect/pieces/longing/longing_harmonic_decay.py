"""
Geometry of Feeling — Longing: Longing Harmonic Decay
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
    t=np.linspace(0,1,2000); xs=PAD_L+PW*t
    target=cy
    ax.plot([PAD_L,PAD_L+PW],[target,target],
            color=rgba(AMBER,0.12),linewidth=0.8,linestyle='--',zorder=2)
    n=16
    for i in range(n):
        frac=i/(n-1)
        gamma=1.5+frac*3.0
        omega=8+frac*14
        amp=PH*(0.18+0.22*(1-frac))
        phase=frac*np.pi*0.8
        ys=target+amp*np.exp(-gamma*t)*np.sin(omega*np.pi*t+phase)
        if frac<0.3: col=TWILIGHT
        elif frac<0.6: col=ROSE
        else: col=COPPER
        alpha=0.10+0.50*(1-frac*0.5)
        lw=0.5+1.2*(1-frac*0.4)
        draw_lc(ax,xs,ys,col,lw=lw,alpha=alpha,zo=3,smooth=4)
    for sign in [1,-1]:
        env_amp=PH*0.38
        env=target+sign*env_amp*np.exp(-2.0*t)
        draw_lc(ax,xs,env,HONEY,lw=0.6,alpha=0.18,zo=2)
    label(ax,"f(t)=c+A\u00b7e^(\u2212\u03b3t)\u00b7sin(\u03c9t)")
    save(fig,"longing_harmonic_decay.pdf")


if __name__ == '__main__':
    render()
