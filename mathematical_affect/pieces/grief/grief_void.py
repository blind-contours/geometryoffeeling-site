"""
Geometry of Feeling — Grief: Grief Void
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
# 1. VOID (improved — lower center, arcs stay on page)
# ═══════════════════════════════════════════════════════════════
def render():
    fig,ax=make_fig()
    void_cx=cx; void_cy=cy-PH*0.02  # slightly lower
    void_rx=PW*0.16; void_ry=PH*0.36
    # Superellipse exponent: <2 = more pointed/diamond, >2 = more square
    void_exp=1.6  # extended top/bottom with rounder tips

    def is_in_void(x,y,margin=0):
        rx=void_rx+margin; ry=void_ry+margin
        if rx<=0 or ry<=0: return False
        return (abs((x-void_cx)/rx)**void_exp + abs((y-void_cy)/ry)**void_exp) < 1.0

    n_lines=60
    y_positions=np.linspace(PAD_B+PH*0.03, PAD_B+PH*0.97, n_lines)
    t=np.linspace(0,1,2000)
    xs_base=PAD_L+PW*t

    for li,y_base in enumerate(y_positions):
        dy=y_base-void_cy
        dist_y=abs(dy)/void_ry

        deflection=np.zeros_like(t)
        for j,xv in enumerate(xs_base):
            dx=xv-void_cx
            # Use superellipse distance for consistent deflection
            r_super=(abs(dx/void_rx)**void_exp + abs(dy/void_ry)**void_exp)**(1.0/void_exp)
            if r_super<0.01: r_super=0.01
            if r_super<2.5:
                push_strength=np.exp(-1.8*(r_super-0.6))
                sign=1 if dy>=0 else -1
                x_nearness=np.exp(-2.0*(abs(dx/void_rx)**void_exp))
                # clamp deflection so arcs stay on canvas
                deflection[j]=sign*min(PH*0.20, PH*0.25*push_strength*x_nearness)

        ys=y_base+deflection
        # clamp to canvas bounds
        ys=np.clip(ys, PAD_B+PH*0.01, PAD_B+PH*0.99)

        wave_amp=PH*0.003*(1+0.5*np.exp(-dist_y))
        wave=wave_amp*np.sin(6*np.pi*t+li*0.2)
        ys=ys+wave

        mask=np.array([not is_in_void(xs_base[j],ys[j],margin=PH*0.005) for j in range(len(t))])

        if dist_y<0.5: col=NAVY if abs(dy)<void_ry*0.3 else DIMBLUE
        elif dist_y<1.0: col=BLUE if li%2==0 else SLATE
        elif dist_y<1.8: col=DUSTY if li%3==0 else MAUVE
        else: col=PALE if li%2==0 else MIST

        nearness=np.exp(-0.8*max(0,dist_y-0.3))
        alpha=0.08+0.55*nearness
        lw=0.3+1.8*nearness

        segments=split_segments(xs_base,ys,mask)
        for sx,sy in segments:
            if len(sx)>3:
                draw_lc(ax,sx,sy,col,lw=lw,alpha=alpha,zo=3,smooth=5)

    # Draw superellipse border rings and fill
    from matplotlib.patches import Polygon
    def superellipse_points(cx_,cy_,rx_,ry_,exp_,n_pts=500):
        t_=np.linspace(0,2*np.pi,n_pts)
        xs_=cx_+rx_*np.sign(np.cos(t_))*np.abs(np.cos(t_))**(2.0/exp_)
        ys_=cy_+ry_*np.sign(np.sin(t_))*np.abs(np.sin(t_))**(2.0/exp_)
        return np.column_stack([xs_,ys_])

    for i in range(8):
        margin=PH*0.005*(i+1)
        pts_ring=superellipse_points(void_cx,void_cy,void_rx+margin,void_ry+margin,void_exp)
        ring=Polygon(pts_ring,closed=True,
                     facecolor='none',edgecolor=rgba(NAVY,0.04-i*0.004),
                     linewidth=0.6-i*0.05,zorder=5)
        ax.add_patch(ring)

    pts_void=superellipse_points(void_cx,void_cy,void_rx,void_ry,void_exp)
    void_patch=Polygon(pts_void,closed=True,
                       facecolor=BG,edgecolor='none',zorder=10)
    ax.add_patch(void_patch)

    label(ax,"(x\u2212cx)\u00b2/a\u00b2+(y\u2212cy)\u00b2/b\u00b2=1")
    save(fig,"grief_void")


if __name__ == '__main__':
    render()
