"""
Geometry of Feeling — Cycles: Cycles Loom
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
BG="#F0E8DA"

# Palette: seasonal color rotation
SPRING="#5A9A50"; SUMMER="#C8A030"; AUTUMN="#B85A30"; WINTER="#4A6A90"
BLOSSOM="#C87898"; HARVEST="#9A7020"; FROST="#7A90A8"; EARTH="#6A5A40"
RENEWAL="#70B060"; DUSK="#8A6A50"; SAGE="#7A9A70"; AMBER="#D0A020"
DEEP_WINTER="#2A4A6A"; MOSS="#4A6A3A"

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
    mask = (xs>PAD_L-0.1)&(xs<PAD_L+PW+0.1)&(ys>PAD_B-0.1)&(ys<PAD_B+PH+0.1)
    segs = split_segments(xs, ys, mask)
    for sx, sy in segs:
        if len(sx)<3: continue
        pts=np.array([sx,sy]).T.reshape(-1,1,2)
        s=np.concatenate([pts[:-1],pts[1:]],axis=1)
        lc=mc.LineCollection(s,linewidths=lw,colors=[rgba(col,alpha)],
                             capstyle='round',joinstyle='round',zorder=zo)
        ax.add_collection(lc)

def draw_lc_xy(ax,xs,ys,col,lw,alpha,zo=4):
    """Draw with clipping on both axes."""
    mask = (xs>PAD_L-0.1)&(xs<PAD_L+PW+0.1)&(ys>PAD_B-0.1)&(ys<PAD_B+PH+0.1)
    segs = split_segments(xs, ys, mask)
    for sx, sy in segs:
        if len(sx)<3: continue
        pts=np.array([sx,sy]).T.reshape(-1,1,2)
        s=np.concatenate([pts[:-1],pts[1:]],axis=1)
        lc=mc.LineCollection(s,linewidths=lw,colors=[rgba(col,alpha)],
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
    np.random.seed(42)
    n_warp=32; n_weft=26
    warp_cols=[SPRING,SUMMER,AUTUMN,WINTER,BLOSSOM,FROST,HARVEST,RENEWAL]
    weft_cols=[EARTH,AUTUMN,WINTER,BLOSSOM,SPRING,HARVEST,FROST,SUMMER]
    warp_spacing=PH*0.92/(n_warp-1)
    weft_spacing=PW*0.92/(n_weft-1)
    warp_k=2*np.pi*3.5/PW
    weft_k=2*np.pi*4.0/PH
    warp_amp=PW*0.022
    weft_amp=PH*0.020
    n_pts=1400

    for i in range(n_warp):
        frac_w=i/(n_warp-1)
        y_offset=PAD_B+PH*0.04+frac_w*PH*0.92
        phi=frac_w*1.7+0.3*np.sin(i*0.9)
        t=np.linspace(0,1,n_pts)
        xs_base=PAD_L+PW*0.04+t*PW*0.92
        ys_base=y_offset+warp_amp*np.sin(warp_k*(xs_base-PAD_L)+phi)
        col=warp_cols[i%len(warp_cols)]
        pts=np.array([xs_base,ys_base]).T.reshape(-1,1,2)
        segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
        n_s=len(segs)
        colors=[]; lws_arr=[]
        for j in range(n_s):
            x_mid=0.5*(xs_base[j]+xs_base[j+1])
            weft_idx=int(round((x_mid-(PAD_L+PW*0.04))/weft_spacing))
            weft_idx=max(0,min(n_weft-1,weft_idx))
            is_over=(i+weft_idx)%2==0
            if is_over:
                a=0.14+0.40*(1-abs(frac_w-0.5)*1.3); lw=0.7+1.0*(1-abs(frac_w-0.5))
            else:
                a=0.05+0.16*(1-abs(frac_w-0.5)*1.3); lw=0.3+0.4*(1-abs(frac_w-0.5))
            colors.append(rgba(col,a)); lws_arr.append(lw)
        lc=mc.LineCollection(segs,linewidths=lws_arr,colors=colors,capstyle='round',joinstyle='round',zorder=4)
        ax.add_collection(lc)

    for m in range(n_weft):
        frac_f=m/(n_weft-1)
        x_offset=PAD_L+PW*0.04+frac_f*PW*0.92
        phi=frac_f*2.1+0.4*np.sin(m*1.1)
        t=np.linspace(0,1,n_pts)
        ys_base=PAD_B+PH*0.04+t*PH*0.92
        xs_base=x_offset+weft_amp*np.sin(weft_k*(ys_base-PAD_B)+phi)
        col=weft_cols[m%len(weft_cols)]
        pts=np.array([xs_base,ys_base]).T.reshape(-1,1,2)
        segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
        n_s=len(segs)
        colors=[]; lws_arr=[]
        for j in range(n_s):
            y_mid=0.5*(ys_base[j]+ys_base[j+1])
            warp_idx=int(round((y_mid-(PAD_B+PH*0.04))/warp_spacing))
            warp_idx=max(0,min(n_warp-1,warp_idx))
            is_over=(warp_idx+m)%2==1
            if is_over:
                a=0.14+0.40*(1-abs(frac_f-0.5)*1.3); lw=0.7+1.0*(1-abs(frac_f-0.5))
            else:
                a=0.05+0.16*(1-abs(frac_f-0.5)*1.3); lw=0.3+0.4*(1-abs(frac_f-0.5))
            colors.append(rgba(col,a)); lws_arr.append(lw)
        lc=mc.LineCollection(segs,linewidths=lws_arr,colors=colors,capstyle='round',joinstyle='round',zorder=5)
        ax.add_collection(lc)

    label(ax,"warp: y\u2099=A\u00b7sin(kx+\u03c6), weft: x\u2098=B\u00b7sin(ky+\u03c8)")
    save(fig,"cycles_loom")


if __name__ == '__main__':
    render()
