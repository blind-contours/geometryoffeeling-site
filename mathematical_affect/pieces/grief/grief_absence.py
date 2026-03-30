"""
Geometry of Feeling — Grief: Grief Absence
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
    np.random.seed(71)

    # The "figure" — a rounded rectangular absence slightly off-center
    abs_cx = cx - PW*0.05
    abs_cy = cy
    abs_w = PW*0.15
    abs_h = PH*0.55

    def is_in_absence(x,y,margin=0):
        # soft rounded rectangle
        dx = abs(x-abs_cx)/(abs_w+margin)
        dy = abs(y-abs_cy)/(abs_h+margin)
        return (dx**4 + dy**4) < 1.0

    # dense horizontal lines filling the canvas
    n_lines = 80
    y_positions = np.linspace(PAD_B+PH*0.02, PAD_B+PH*0.98, n_lines)
    t = np.linspace(0,1,2000)
    xs = PAD_L+PW*t

    for li, y_base in enumerate(y_positions):
        # subtle wave
        wave = PH*0.003*np.sin(4*np.pi*t + li*0.15)
        ys = y_base + wave

        mask = np.array([not is_in_absence(xs[j],ys[j],margin=PH*0.01) for j in range(len(t))])

        # distance from absence edge affects density
        dist_to_abs = abs(y_base - abs_cy)/abs_h
        if dist_to_abs < 0.3:
            col = NAVY; alpha=0.35; lw=1.2
        elif dist_to_abs < 0.7:
            col = DIMBLUE if li%2==0 else BLUE; alpha=0.22; lw=0.8
        elif dist_to_abs < 1.2:
            col = SLATE if li%3==0 else DUSTY; alpha=0.15; lw=0.6
        else:
            col = PALE if li%2==0 else MIST; alpha=0.08; lw=0.4

        segments = split_segments(xs,ys,mask)
        for sx,sy in segments:
            if len(sx)>3:
                draw_lc(ax,sx,sy,col,lw=lw,alpha=alpha,zo=3,smooth=3)

    label(ax,"\u222b\u222b \u03c1(x,y) dA \u2192 0")
    save(fig,"grief_absence")


if __name__ == '__main__':
    render()
