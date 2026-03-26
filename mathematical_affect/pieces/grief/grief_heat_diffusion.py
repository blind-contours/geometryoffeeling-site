"""
Geometry of Feeling — Grief: Grief Heat Diffusion
Standalone render script
"""

"""
Geometry of Feeling — Grief v2 (20 candidates)
Loss, absence, the shape of what's missing.

Dependencies: matplotlib, numpy, scipy
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

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Ensure name ends with .pdf
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


# ═══════════════════════════════════════════════════════════════
# 4. HEAT DIFFUSION (improved — stronger initial pulse)
# ═══════════════════════════════════════════════════════════════
def render():
    fig,ax=make_fig()
    x=np.linspace(-2.0,2.0,2000)  # zoomed in from (-3,3)
    xs=PAD_L+PW*(x-x.min())/(x.max()-x.min())
    sigma_0=0.10  # wider initial pulse for better visibility

    times=np.concatenate([
        np.linspace(0.001,0.05,8),
        np.linspace(0.08,0.30,6),
        np.linspace(0.45,1.5,5),
        np.linspace(2.5,8.0,3)
    ])

    colors_time=[DEEP,NAVY,NAVY,DIMBLUE,DIMBLUE,BLUE,BLUE,SLATE,
                 DUSTY,MAUVE,LILAC,PALE,ICE,FROST,FROST,
                 MIST,MIST,ASH,ASH,GREY,BONE,BONE]

    for i,time_val in enumerate(times):
        sigma_t=np.sqrt(sigma_0**2+2*0.08*time_val)
        u=(1.0/(sigma_t*np.sqrt(2*np.pi)))*np.exp(-x**2/(2*sigma_t**2))
        u_max_initial=1.0/(sigma_0*np.sqrt(2*np.pi))
        u_norm=u/u_max_initial

        frac=i/(len(times)-1)
        y_base=PAD_B+PH*0.05
        amplitude=PH*0.90
        ys=y_base+amplitude*u_norm

        col=colors_time[i % len(colors_time)]
        alpha=0.10+0.65*np.exp(-1.5*frac)
        lw=0.4+2.4*np.exp(-1.8*frac)

        draw_lc(ax,xs,ys,col,lw=lw,alpha=alpha,zo=3+len(times)-i,smooth=4)
        ys_smooth=gaussian_filter1d(ys,8)
        ax.fill_between(xs,y_base,ys_smooth,
                        color=rgba(col,alpha*0.08),linewidth=0,zorder=2)

    for r,a in [(0.4,0.025),(0.2,0.04),(0.1,0.06)]:
        ax.add_patch(Circle((cx,PAD_B+PH*0.05+PH*0.42),radius=r,
                    facecolor=rgba(NAVY,a),edgecolor='none',zorder=1))

    label(ax,"\u2202u/\u2202t=\u03b1\u00b7\u2202\u00b2u/\u2202x\u00b2")
    save(fig,"grief_heat_diffusion")


if __name__ == '__main__':
    render()
