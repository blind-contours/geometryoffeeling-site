"""
Geometry of Feeling — Confusion: Confusion Labyrinth
Standalone render script
"""

import numpy as np
import matplotlib
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

def label(ax,eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.15,0.15,0.20,0.22),transform=ax.transData)
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

def save(fig,name):
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR,name),
                format='pdf',facecolor=BG)
    plt.close(fig); print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def render():
    fig,ax=make_fig()
    np.random.seed(55)
    n_paths=28
    for p in range(n_paths):
        frac=p/(n_paths-1)
        # random walk with right-angle turns — maze corridors
        n_steps=120
        x=PAD_L+PW*np.random.uniform(0.05,0.95)
        y=PAD_B+PH*np.random.uniform(0.05,0.95)
        step_size=PW*0.020
        xs_path=[x]; ys_path=[y]
        direction=np.random.choice(4)  # 0=right,1=up,2=left,3=down
        for s in range(n_steps):
            # turn more often — creates denser maze feel
            if np.random.random()<0.40:
                direction=(direction+np.random.choice([-1,1]))%4
            # occasionally reverse (dead end, turn around)
            if np.random.random()<0.08:
                direction=(direction+2)%4
            dx=[step_size,0,-step_size,0][direction]
            dy=[0,step_size,0,-step_size][direction]
            nx_=x+dx; ny_=y+dy
            # boundary checking
            if nx_<PAD_L+PW*0.02 or nx_>PAD_L+PW*0.98:
                direction=(direction+2)%4; continue
            if ny_<PAD_B+PH*0.02 or ny_>PAD_B+PH*0.98:
                direction=(direction+2)%4; continue
            x=nx_; y=ny_
            xs_path.append(x); ys_path.append(y)
        xs_arr=np.array(xs_path); ys_arr=np.array(ys_path)
        if len(xs_arr)<5: continue
        cols=[MURK,TANGLE_COL,FOG,UNCERTAIN,CROSSED,KNOT_COL,
              HAZE,DRIFT,STATIC,MAUVE,SAGE,CLAY]
        col=cols[p%len(cols)]
        alpha=0.10+0.32*(1-abs(frac-0.5)*1.2)
        lw=0.35+0.85*(1-abs(frac-0.5))
        # draw with very light smoothing to keep right-angle feel
        draw_lc(ax,xs_arr,ys_arr,col,lw=lw,alpha=alpha,zo=3,smooth=2)

    # faint grid lines underneath — the maze structure
    n_grid=25
    for i in range(n_grid):
        gfrac=i/(n_grid-1)
        # vertical grid lines
        gx=PAD_L+PW*(0.04+gfrac*0.92)
        ax.plot([gx,gx],[PAD_B+PH*0.02,PAD_B+PH*0.98],
                color=rgba(FOG,0.04),linewidth=0.2,zorder=2)
        # horizontal grid lines
        gy=PAD_B+PH*(0.04+gfrac*0.92)
        ax.plot([PAD_L+PW*0.02,PAD_L+PW*0.98],[gy,gy],
                color=rgba(FOG,0.04),linewidth=0.2,zorder=2)

    label(ax,"random walk, \u03b8\u2208{0,\u03c0/2,\u03c0,3\u03c0/2}")
    save(fig,"confusion_labyrinth.pdf")


if __name__ == '__main__':
    render()
