"""
Geometry of Feeling — Euphoria: Euphoria Stained Glass
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
BG="#FEFCF8"  # near-white — the flash of too much light

# Palette: electric, oversaturated, almost painful
ELECTRIC_VIOLET="#8828D0"; HOT_PINK="#E02888"; ACID_YELLOW="#D8D020"
VIVID_CYAN="#20C8D0"; FLASH_ORANGE="#F08020"
MAGENTA="#D020A0"; NEON_GREEN="#40E040"; ULTRAVIOLET="#6020E0"
PLASMA="#E848A0"; WHITE_HOT="#F8F0E0"

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
            color=(0.35,0.20,0.40,0.22),transform=ax.transData)
def split_segments(xs, ys, mask):
    """Split masked arrays into contiguous segments to avoid straight-line jumps."""
    segments = []
    in_seg = False
    start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j; in_seg = True
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
    n_points=60
    # generate seed points
    px=PAD_L+PW*np.random.uniform(0.02,0.98,n_points)
    py=PAD_B+PH*np.random.uniform(0.02,0.98,n_points)
    cols=[HOT_PINK,ELECTRIC_VIOLET,ACID_YELLOW,VIVID_CYAN,FLASH_ORANGE,
          MAGENTA,NEON_GREEN,ULTRAVIOLET,PLASMA,WHITE_HOT]
    from scipy.spatial import Voronoi
    points=np.column_stack([px,py])
    # add mirror points for bounded Voronoi
    mirror_pts=np.vstack([
        points,
        np.column_stack([2*PAD_L-px, py]),
        np.column_stack([2*(PAD_L+PW)-px, py]),
        np.column_stack([px, 2*PAD_B-py]),
        np.column_stack([px, 2*(PAD_B+PH)-py]),
    ])
    vor=Voronoi(mirror_pts)
    # draw ridges
    for ri,ridge in enumerate(vor.ridge_vertices):
        if -1 in ridge: continue
        v0=vor.vertices[ridge[0]]
        v1=vor.vertices[ridge[1]]
        xs_r=np.array([v0[0],v1[0]])
        ys_r=np.array([v0[1],v1[1]])
        # clip to canvas
        if np.any(xs_r<PAD_L-0.1) or np.any(xs_r>PAD_L+PW+0.1): continue
        if np.any(ys_r<PAD_B-0.1) or np.any(ys_r>PAD_B+PH+0.1): continue
        col=cols[ri%len(cols)]
        # dark leading lines
        ax.plot(xs_r,ys_r,color=rgba('#1A1020',0.60),linewidth=2.5,
                solid_capstyle='round',zorder=5)
        ax.plot(xs_r,ys_r,color=rgba(col,0.30),linewidth=1.2,
                solid_capstyle='round',zorder=6)
    # fill cells with color
    for ri,region_idx in enumerate(vor.point_region[:n_points]):
        region=vor.regions[region_idx]
        if not region or -1 in region: continue
        polygon=np.array([vor.vertices[v] for v in region])
        if np.any(polygon[:,0]<PAD_L-0.5) or np.any(polygon[:,0]>PAD_L+PW+0.5): continue
        if np.any(polygon[:,1]<PAD_B-0.5) or np.any(polygon[:,1]>PAD_B+PH+0.5): continue
        col=cols[ri%len(cols)]
        ax.fill(polygon[:,0],polygon[:,1],color=rgba(col,0.15),linewidth=0,zorder=2)
    label(ax,"Voronoi(P)")
    save(fig,"euphoria_stained_glass.pdf")


if __name__ == '__main__':
    render()
