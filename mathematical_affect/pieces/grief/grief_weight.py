"""
Geometry of Feeling — Grief: Grief Weight
Standalone render script
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
from matplotlib.patches import Circle, Ellipse
import os, sys

DPI=300; FIG_W=12; FIG_H=8
BG="#DDD9D2"

# Palette: muted blue-grey, dusty mauve, cool navy
SLATE="#6A7A8A"; DUSTY="#7A6A8A"; BLUE="#4A5A7A"
GREY="#8A8A8A"; MAUVE="#8A6A7A"; PALE="#AAA0B0"
DIMBLUE="#3A4A6A"; NAVY="#2A3A5A"; LILAC="#9A88AA"
ICE="#8AAABB"; FROST="#AAB8C4"; MIST="#BAC8D4"
ASH="#7A7878"; CHAR="#4A4858"; BONE="#C8C0B8"
DEEP="#1A2A3A"; STORM="#5A6878"; SMOKE="#A0A0A0"

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
    mask = (xs>=PAD_L-0.05)&(xs<=PAD_L+PW+0.05)&(ys>=PAD_B-0.05)&(ys<=PAD_B+PH+0.15)
    segs = split_segments(xs, ys, mask)
    for sx, sy in segs:
        if len(sx) < 3: continue
        pts=np.array([sx,sy]).T.reshape(-1,1,2)
        s=np.concatenate([pts[:-1],pts[1:]],axis=1)
        lc=mc.LineCollection(s,linewidths=lw,colors=[rgba(col,alpha)],
                             capstyle='round',joinstyle='round',zorder=zo)
        ax.add_collection(lc)

def draw_lc_gradient(ax,xs,ys,col,lw_start,lw_end,a_start,a_end,zo=4,smooth=0):
    if smooth>0: ys=gaussian_filter1d(ys,smooth)
    n=len(xs)-1
    pts=np.array([xs,ys]).T.reshape(-1,1,2)
    segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
    frac=np.linspace(0,1,n)
    lws=lw_start+(lw_end-lw_start)*frac
    cols=[rgba(col,a_start+(a_end-a_start)*f) for f in frac]
    lc=mc.LineCollection(segs,linewidths=lws,colors=cols,
                         capstyle='round',joinstyle='round',zorder=zo)
    ax.add_collection(lc)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def save(fig, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith('.pdf'):
        name = name + '.pdf'
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f'saved {name}')


def render():
    fig,ax=make_fig()
    x_left=PAD_L+PW*0.02; x_right=PAD_L+PW*0.98
    y_anchor_base=PAD_B+PH*0.92

    n_cables=25
    t=np.linspace(0,1,1500)
    xs=x_left+(x_right-x_left)*t
    x_mid=(x_left+x_right)/2
    span=x_right-x_left

    for ci in range(n_cables):
        frac=ci/(n_cables-1)
        y_anchor=y_anchor_base-PH*0.02*frac
        a_val=span*(2.0-1.85*frac**0.7)
        if a_val<0.15: a_val=0.15

        x_centered=(xs-x_mid)
        cosh_vals=np.cosh(np.clip(x_centered/a_val,-50,50))
        cosh_min=1.0
        cosh_max=np.cosh(np.clip((span/2)/a_val,-50,50))

        if cosh_max-cosh_min<1e-6:
            ys_cat=np.full_like(xs,y_anchor)
        else:
            ys_norm=(cosh_vals-cosh_min)/(cosh_max-cosh_min)
            sag_depth=PH*(0.03+0.78*frac**0.8)
            ys_cat=y_anchor-sag_depth*(1-ys_norm)

        tremble_amp=PH*0.003*(1+2*frac)*np.exp(-3*abs(t-0.5))
        tremble=tremble_amp*np.sin((12+ci*1.5)*np.pi*t+ci*0.4)
        ys=np.clip(ys_cat+tremble, PAD_B+PH*0.02, PAD_B+PH*0.97)

        if frac<0.15: col=MIST
        elif frac<0.30: col=FROST
        elif frac<0.45: col=SLATE
        elif frac<0.55: col=BLUE
        elif frac<0.65: col=DUSTY
        elif frac<0.75: col=DIMBLUE
        elif frac<0.85: col=NAVY
        else: col=CHAR

        alpha=0.10+0.58*frac
        lw=0.4+2.0*frac
        draw_lc(ax,xs,ys,col,lw=lw,alpha=alpha,zo=3+ci,smooth=3)

        if frac>0.3:
            ys_smooth=gaussian_filter1d(ys,6)
            ax.fill_between(xs,PAD_B+PH*0.02,ys_smooth,
                            color=rgba(col,0.01+0.018*frac),linewidth=0,zorder=2)

    for x_anch in [x_left,x_right]:
        for r,a in [(0.08,0.08),(0.04,0.15),(0.015,0.25)]:
            ax.add_patch(Circle((x_anch,y_anchor_base),radius=r,
                        facecolor=rgba(NAVY,a),edgecolor='none',zorder=8))

    ax.plot([x_left,x_right],[y_anchor_base+PH*0.01,y_anchor_base+PH*0.01],
            color=rgba(GREY,0.20),linewidth=1.2,zorder=7)

    label(ax,"y(x)=a\u00b7cosh((x\u2212c)/a)")
    save(fig,"grief_weight")


if __name__ == '__main__':
    render()
