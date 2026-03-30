"""
Geometry of Feeling — Confusion: Confusion Vertigo
Standalone render script
"""

"""
Geometry of Feeling — Confusion (Final Series)
Five pieces: Tangle, Knot, Labyrinth, Vertigo, Aliased

Mathematical primitives: Lissajous curves with irrational ratios,
torus knot projections, maze-like random walks with right-angle turns,
conflicting clockwise/counterclockwise spirals, Moire-like aliasing artifacts

Background: #E8E4E0 (light, uncertain)
Palette: muted pastels all mixed — no color hierarchy

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
"""

import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os

DPI=300; FIG_W=12; FIG_H=8
BG="#E8E4E0"

# Palette: muddled, uncertain — no color dominates
MURK="#6A6A68"; TANGLE_COL="#7A6A58"; FOG="#8A8A88"
UNCERTAIN="#5A6A70"; CROSSED="#7A5A68"; KNOT_COL="#6A5A50"
HAZE="#9A9A90"; DRIFT="#5A7070"; STATIC="#7A7A80"
MAUVE="#8A6A7A"; SAGE="#6A7A68"; CLAY="#8A7A60"

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

def split_segments(xs, ys, mask):
    segments = []
    in_seg = False
    start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j
            in_seg = True
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

def draw_lc_gradient(ax,xs,ys,col,lw_start,lw_end,a_start,a_end,zo=4,smooth=0):
    if smooth>0:
        ys=gaussian_filter1d(ys,smooth)
    pts=np.array([xs,ys]).T.reshape(-1,1,2)
    segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
    n=len(segs)
    alphas=np.linspace(a_start,a_end,n)
    lws=np.linspace(lw_start,lw_end,n)
    colors=[rgba(col,float(a)) for a in alphas]
    lc=mc.LineCollection(segs,linewidths=lws,colors=colors,
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

# ===============================================================================
# 4. VERTIGO — spiral curves with conflicting orientations
#    Alternating clockwise and counterclockwise Archimedean spirals
#    all overlapping, creating disorienting rotational conflict
# ===============================================================================
def render():
    fig,ax=make_fig()
    cols=[MURK,TANGLE_COL,FOG,UNCERTAIN,CROSSED,KNOT_COL,
          HAZE,DRIFT,STATIC,MAUVE,SAGE,CLAY]

    # --- Main spirals — many more, higher contrast ---
    n_spirals=40
    for i in range(n_spirals):
        frac=i/(n_spirals-1)
        t=np.linspace(0,6*np.pi,3000)
        direction=1 if i%2==0 else -1
        a=PW*0.015; b=PW*0.042*(0.25+frac*0.75)
        r=a+b*t/(6*np.pi)
        cx_i=cx+PW*0.18*np.sin(frac*3.7*np.pi)
        cy_i=cy+PH*0.13*np.cos(frac*2.9*np.pi)
        xs_s=cx_i+r*np.cos(direction*t+frac*np.pi)
        ys_s=cy_i+r*np.sin(direction*t+frac*np.pi)*(PH/PW)
        mask=((xs_s>PAD_L)&(xs_s<PAD_L+PW)&
              (ys_s>PAD_B)&(ys_s<PAD_B+PH))
        col=cols[i%len(cols)]
        for seg_xs, seg_ys in split_segments(xs_s, ys_s, mask):
            alpha=0.20+0.50*(1-abs(frac-0.5)*1.2)
            lw=0.5+1.4*(1-abs(frac-0.5))
            draw_lc(ax,seg_xs,seg_ys,col,lw=lw,alpha=alpha,zo=3+i,smooth=2)

    # --- Additional medium spirals for density ---
    np.random.seed(99)
    for k in range(25):
        kfrac=k/24
        t_m=np.linspace(0,5*np.pi,2000)
        direction=1 if k%2==0 else -1
        a_m=PW*0.01; b_m=PW*0.032*(0.3+kfrac*0.7)
        r_m=a_m+b_m*t_m/(5*np.pi)
        cx_m=cx+PW*0.20*np.sin(kfrac*5.1*np.pi+1.2)
        cy_m=cy+PH*0.15*np.cos(kfrac*3.3*np.pi+0.8)
        xs_m=cx_m+r_m*np.cos(direction*t_m+kfrac*2*np.pi)
        ys_m=cy_m+r_m*np.sin(direction*t_m+kfrac*2*np.pi)*(PH/PW)
        mask_m=((xs_m>PAD_L)&(xs_m<PAD_L+PW)&
                (ys_m>PAD_B)&(ys_m<PAD_B+PH))
        col=cols[k%len(cols)]
        for seg_xs, seg_ys in split_segments(xs_m, ys_m, mask_m):
            alpha=0.15+0.40*(1-abs(kfrac-0.5)*1.2)
            lw=0.4+1.0*(1-abs(kfrac-0.5))
            draw_lc(ax,seg_xs,seg_ys,col,lw=lw,alpha=alpha,zo=2+k,smooth=2)

    # --- Small tight spirals scattered — more of them, higher contrast ---
    np.random.seed(42)
    for j in range(50):
        jfrac=j/49
        t_sm=np.linspace(0,4*np.pi,500)
        r_sm=PW*0.005+PW*0.02*t_sm/(4*np.pi)
        dir_sm=1 if np.random.random()>0.5 else -1
        cx_sm=PAD_L+PW*np.random.uniform(0.05,0.95)
        cy_sm=PAD_B+PH*np.random.uniform(0.05,0.95)
        xs_sm=cx_sm+r_sm*np.cos(dir_sm*t_sm)
        ys_sm=cy_sm+r_sm*np.sin(dir_sm*t_sm)*(PH/PW)
        mask_sm=((xs_sm>PAD_L)&(xs_sm<PAD_L+PW)&
                 (ys_sm>PAD_B)&(ys_sm<PAD_B+PH))
        col=cols[j%len(cols)]
        for seg_xs, seg_ys in split_segments(xs_sm, ys_sm, mask_sm):
            draw_lc(ax,seg_xs,seg_ys,col,lw=0.5,alpha=0.22,zo=2,smooth=1)

    # --- Extra concentric ring clusters — pure circles for density ---
    np.random.seed(77)
    for rc in range(45):
        # organic random positioning
        cx_rc=PAD_L+PW*np.random.uniform(0.05,0.95)
        cy_rc=PAD_B+PH*np.random.uniform(0.05,0.95)
        n_rings=np.random.randint(3,6)
        col=cols[rc%len(cols)]
        for ring in range(n_rings):
            r_ring=PW*0.005*(ring+1)+PW*np.random.uniform(0,0.002)
            t_ring=np.linspace(0,2*np.pi,300)
            xs_rc=cx_rc+r_ring*np.cos(t_ring)
            ys_rc=cy_rc+r_ring*np.sin(t_ring)*(PH/PW)
            mask_rc=((xs_rc>PAD_L)&(xs_rc<PAD_L+PW)&
                     (ys_rc>PAD_B)&(ys_rc<PAD_B+PH))
            for seg_xs, seg_ys in split_segments(xs_rc, ys_rc, mask_rc):
                draw_lc(ax,seg_xs,seg_ys,col,lw=0.5+0.3*ring,
                         alpha=0.30+0.18*(n_rings-ring)/n_rings,zo=50+rc,smooth=0)

    add_signature(fig, ax, BG)
    save(fig,"confusion_vertigo.pdf")

if __name__ == '__main__':
    render()
