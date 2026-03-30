"""
Geometry of Feeling — Grief: Grief Heaviside Cascade
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
    t=np.linspace(0,1,2000)
    xs=PAD_L+PW*t

    n_steps=10
    np.random.seed(37)
    drop_times=np.sort(np.concatenate([
        [0.06], np.random.uniform(0.12,0.84,n_steps-2), [0.90]
    ]))
    heights=np.linspace(PH*0.93, PH*0.07, n_steps)
    colors_step=[DEEP,NAVY,DIMBLUE,BLUE,SLATE,DUSTY,MAUVE,CHAR,ASH,GREY]

    for si in range(n_steps):
        t_drop=drop_times[si]
        h_before=heights[si]
        h_after=heights[min(si+1,n_steps-1)] if si<n_steps-1 else PH*0.03

        k_sharp=65
        step=1/(1+np.exp(k_sharp*(t-t_drop)))
        ys_step=PAD_B+h_after+(h_before-h_after)*step

        col=colors_step[si]

        n_echoes=4
        for ei in range(n_echoes):
            echo_frac=ei/n_echoes
            y_echo=PAD_B+h_before+PH*0.006*(ei-n_echoes/2)
            wave=PH*0.004*(1-echo_frac)*np.sin((8+ei*2)*np.pi*t+ei*0.7)
            ys_echo=y_echo+wave
            fade=np.clip(1-10*(t-t_drop+0.05),0,1)
            alpha_echo=0.05+0.16*(1-echo_frac)
            mask_echo=fade>0.05
            segs=split_segments(xs,ys_echo,mask_echo)
            for sx,sy in segs:
                if len(sx)>3:
                    pts=np.array([sx,sy]).T.reshape(-1,1,2)
                    seg_pairs=np.concatenate([pts[:-1],pts[1:]],axis=1)
                    t_seg=(sx-PAD_L)/PW
                    fade_seg=np.clip(1-10*(t_seg[:-1]-t_drop+0.05),0,1)
                    colors_arr=[rgba(col,alpha_echo*f) for f in fade_seg]
                    lc=mc.LineCollection(seg_pairs,linewidths=0.5+0.3*(1-echo_frac),
                                        colors=colors_arr,capstyle='round',joinstyle='round',zorder=3)
                    ax.add_collection(lc)

        alpha=0.22+0.55*(1-si/(n_steps-1))
        lw=0.9+2.0*(1-si/(n_steps-1))
        draw_lc(ax,xs,ys_step,col,lw=lw,alpha=alpha,zo=5+si,smooth=2)
        ys_step_smooth=gaussian_filter1d(ys_step,3)
        ax.fill_between(xs,PAD_B+PH*0.03,ys_step_smooth,
                        color=rgba(col,0.03+0.02*si),linewidth=0,zorder=2)

        x_drop=PAD_L+PW*t_drop
        ax.plot([x_drop,x_drop],[PAD_B+h_after,PAD_B+h_before],
                color=rgba(col,alpha*0.6),linewidth=0.9,zorder=4)

    label(ax,"f(t)=\u03a3 h\u2096\u00b7H(t\u2096\u2212t)")
    save(fig,"grief_heaviside_cascade")


if __name__ == '__main__':
    render()
