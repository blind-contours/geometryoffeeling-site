"""
Geometry of Feeling — Joy: Joy Pinwheel
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
    n_arms = 8
    max_r = min(PW, PH) * 0.48
    arm_colors = [RED, BLUE, YELLOW, GREEN, ORANGE, PURPLE, CYAN, MAGENTA]

    for arm in range(n_arms):
        base_angle = 2*np.pi*arm/n_arms
        col = arm_colors[arm]

        # Each arm is a logarithmic spiral with sinusoidal modulation
        theta = np.linspace(0, 4*np.pi, 3000)
        # Logarithmic spiral: r = a * exp(b*theta)
        a_spiral = 0.08
        b_spiral = 0.18
        r = a_spiral * np.exp(b_spiral * theta)
        # Modulate with sinusoidal wobble for visual interest
        r = r * (1 + 0.15*np.sin(6*theta))
        # Clip to max radius
        r = np.minimum(r, max_r)

        xs_arm = cx + r*np.cos(theta + base_angle)
        ys_arm = cy + r*np.sin(theta + base_angle)

        mask = ((xs_arm > PAD_L) & (xs_arm < PAD_L+PW) &
                (ys_arm > PAD_B) & (ys_arm < PAD_B+PH))
        if mask.sum() < 3:
            continue

        pts = np.array([xs_arm[mask], ys_arm[mask]]).T.reshape(-1,1,2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        n_s = len(segs)

        # Alpha and linewidth gradient: bright at center, fading outward
        alphas = np.linspace(0.60, 0.08, n_s)
        lws = np.linspace(2.4, 0.4, n_s)
        colors = [rgba(col, float(a)) for a in alphas]
        lc_obj = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                   capstyle='round', zorder=3+arm)
        ax.add_collection(lc_obj)

        # Add a secondary thinner arm slightly rotated for depth
        theta2 = np.linspace(0, 3.5*np.pi, 2000)
        r2 = a_spiral * 0.6 * np.exp(b_spiral * 1.1 * theta2)
        r2 = r2 * (1 + 0.20*np.sin(8*theta2 + np.pi/4))
        r2 = np.minimum(r2, max_r * 0.85)
        rot_offset = np.pi / (n_arms * 2)  # slight rotation
        xs2 = cx + r2*np.cos(theta2 + base_angle + rot_offset)
        ys2 = cy + r2*np.sin(theta2 + base_angle + rot_offset)
        mask2 = ((xs2 > PAD_L) & (xs2 < PAD_L+PW) &
                 (ys2 > PAD_B) & (ys2 < PAD_B+PH))
        if mask2.sum() < 3:
            continue
        pts2 = np.array([xs2[mask2], ys2[mask2]]).T.reshape(-1,1,2)
        segs2 = np.concatenate([pts2[:-1], pts2[1:]], axis=1)
        n_s2 = len(segs2)
        alphas2 = np.linspace(0.35, 0.04, n_s2)
        lws2 = np.linspace(1.4, 0.2, n_s2)
        colors2 = [rgba(col, float(a)) for a in alphas2]
        lc2 = mc.LineCollection(segs2, linewidths=lws2, colors=colors2,
                                capstyle='round', zorder=2+arm)
        ax.add_collection(lc2)

    # Center glow
    for rad, a in [(0.22, 0.04), (0.12, 0.10), (0.05, 0.28)]:
        ax.add_patch(Circle((cx, cy), radius=rad,
                    facecolor=rgba(GOLD, a), edgecolor='none', zorder=12))

    label(ax,"f(t)=ae^(b\u03b8)\u00b7(1+c\u00b7sin(n\u03b8))")
    save(fig,"joy_pinwheel.pdf")


if __name__ == '__main__':
    render()
