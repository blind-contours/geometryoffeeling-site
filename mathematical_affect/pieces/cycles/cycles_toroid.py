"""
Geometry of Feeling — Cycles: Cycles Toroid
Standalone render script
"""

"""
Geometry of Feeling — Cycles v2 (20 candidates)
Return, repetition, the loop that never quite closes the same way.

Dependencies: matplotlib, numpy, scipy
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
# 20. TOROID — torus cross-sections, nested loops
# ═══════════════════════════════════════════════════════════════
def render():
    fig,ax=make_fig()
    theta=np.linspace(0,2*np.pi,2000)

    R=PW*0.25  # major radius — slightly smaller to center better
    r=PH*0.18  # minor radius
    cols=[SPRING,SUMMER,AUTUMN,WINTER]

    # --- Back-side sections first (behind the torus, thinner/fainter) ---
    n_back=10
    for si in range(n_back):
        frac_back=si/(n_back-1)
        # back-side phi goes from pi to 2*pi (the far side)
        phi=np.pi + frac_back*np.pi
        # project the torus section
        xs_t=cx+(R+r*np.cos(theta))*np.cos(phi)
        ys_t=cy+r*np.sin(theta)
        # perspective: back sections are smaller
        scale=0.8+0.2*np.cos(phi)  # will be <1 for back
        xs_t=cx+(xs_t-cx)*scale
        ys_t=cy+(ys_t-cy)*scale

        season_idx=int(frac_back*4)%4
        col=cols[season_idx]
        # much fainter and thinner for back-side depth effect
        depth_factor=0.3+0.3*(1-abs(frac_back-0.5)*1.2)
        alpha=0.12*depth_factor
        lw=0.4*depth_factor
        draw_lc_xy(ax,xs_t,ys_t,col,lw=lw,alpha=alpha,zo=1+si)

    # --- Front-side sections (the visible ones, on top) ---
    n_sections=14
    for si in range(n_sections):
        frac=si/(n_sections-1)
        # front-side phi goes from 0 to pi
        phi=frac*np.pi
        # project the torus section
        xs_t=cx+(R+r*np.cos(theta))*np.cos(phi)
        ys_t=cy+r*np.sin(theta)
        # add perspective depth
        scale=0.8+0.2*np.cos(phi)
        xs_t=cx+(xs_t-cx)*scale
        ys_t=cy+(ys_t-cy)*scale

        season_idx=int(frac*4)%4
        col=cols[season_idx]
        # depth-based alpha
        alpha=(0.08+0.40*scale)*(1-abs(frac-0.5)*0.5)
        lw=(0.3+1.0*scale)*(1-abs(frac-0.5)*0.5)
        draw_lc_xy(ax,xs_t,ys_t,col,lw=lw,alpha=alpha,zo=3+n_back+si)

    label(ax,"(R+r\u00b7cos\u03b8)\u00b7cos\u03c6, r\u00b7sin\u03b8")
    save(fig,"cycles_toroid")


# =============================================================================


if __name__ == '__main__':
    render()
