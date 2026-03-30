"""
Geometry of Feeling — Joy: Joy Confetti
Standalone render script
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle, Polygon
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import Voronoi
import os

DPI=300; FIG_W=12; FIG_H=8
BG="#FFFFFF"  # white background per spec

# Palette: vivid primaries, full saturation
RED="#E52020"; BLUE="#2060E0"; YELLOW="#F0C010"
GREEN="#20B040"; ORANGE="#F07010"; PURPLE="#8030D0"
CYAN="#10B8D8"; MAGENTA="#D020A0"; LIME="#80D010"
CORAL="#E05040"; SKY="#3090F0"; GOLD="#E0A010"
ROSE="#E04080"; TEAL="#10A898"

PRIMARIES = [RED, BLUE, YELLOW, GREEN, ORANGE, PURPLE,
             CYAN, MAGENTA, LIME, CORAL, SKY, GOLD, ROSE, TEAL]

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
            color=(0.20,0.20,0.25,0.25),transform=ax.transData)
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
    np.random.seed(42)
    # Generate random seed points within the plot area
    n_cells = 180
    pts_x = PAD_L + PW*np.random.uniform(0.0, 1.0, n_cells)
    pts_y = PAD_B + PH*np.random.uniform(0.0, 1.0, n_cells)
    points = np.column_stack([pts_x, pts_y])

    # Add mirror points for bounded Voronoi
    margin_pts = []
    for px, py in points:
        margin_pts.append([2*PAD_L - px, py])
        margin_pts.append([2*(PAD_L+PW) - px, py])
        margin_pts.append([px, 2*PAD_B - py])
        margin_pts.append([px, 2*(PAD_B+PH) - py])
    all_pts = np.vstack([points, np.array(margin_pts)])
    vor = Voronoi(all_pts)

    # Draw filled Voronoi cells for the original points only
    for i in range(n_cells):
        region_idx = vor.point_region[i]
        region = vor.regions[region_idx]
        if -1 in region or len(region) < 3:
            continue
        verts = vor.vertices[region]
        # Clip to plot area
        verts_clipped = np.clip(verts, [PAD_L, PAD_B], [PAD_L+PW, PAD_B+PH])

        col = PRIMARIES[i % len(PRIMARIES)]
        # Vary saturation/alpha for depth
        dist_from_center = np.sqrt((pts_x[i]-cx)**2 + (pts_y[i]-cy)**2)
        max_dist = np.sqrt((PW/2)**2 + (PH/2)**2)
        norm_dist = dist_from_center / max_dist
        fill_alpha = 0.18 + 0.35 * (1 - norm_dist * 0.5)
        edge_alpha = 0.40 + 0.30 * (1 - norm_dist * 0.5)

        poly = Polygon(verts_clipped, closed=True,
                       facecolor=rgba(col, fill_alpha),
                       edgecolor=rgba(col, edge_alpha),
                       linewidth=0.8, zorder=3)
        ax.add_patch(poly)

    # Add small circular highlights at cell centers
    for i in range(n_cells):
        col = PRIMARIES[i % len(PRIMARIES)]
        dot_size = np.random.uniform(0.03, 0.08)
        ax.add_patch(Circle((pts_x[i], pts_y[i]), radius=dot_size,
                    facecolor=rgba(col, 0.45),
                    edgecolor='none', zorder=5))

    label(ax,"f(p)=V(p)={x:|x\u2212p|\u2264|x\u2212q|}")
    save(fig,"joy_confetti.pdf")


if __name__ == '__main__':
    render()
