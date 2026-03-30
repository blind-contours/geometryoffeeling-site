"""
Geometry of Feeling — Solitude: Basin
Parabolic bowl with circles aggregating at the bottom, one alone at the tip
y = a(x - h)^2 + k
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
from matplotlib.patches import Circle
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI=300; FIG_W=12; FIG_H=8
BG="#E0DDD6"

DEEP_GREY="#404850"; DARK_GREEN="#2A4A3A"; WARM_ACCENT="#C8963A"
SLATE="#5A6878"; CHARCOAL="#353D45"; MOSS="#3A5A42"
MIST="#8A9AA8"; LONE_GOLD="#D4A840"; IRON="#2A3038"
TEAL="#3A6A68"; SAGE="#5A7A60"; DUSK="#4A5068"
BONE="#C8C4B8"; NIGHT="#1A2028"

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
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig.savefig(os.path.join(OUTPUT_DIR,name),
                format='pdf',facecolor=BG)
    plt.close(fig); print(f"saved {name}")

def render():
    fig, ax = make_fig()
    rng = np.random.RandomState(77)

    h = PAD_L + PW * 0.22
    k = PAD_B + PH * 0.08

    x_target = PAD_L + PW * 0.92
    y_target = PAD_B + PH * 0.88
    a = (y_target - k) / (x_target - h)**2

    x_left = PAD_L + PW * 0.04
    x_right = PAD_L + PW * 0.94
    n_pts = 3000
    x_para = np.linspace(x_left, x_right, n_pts)
    y_para = a * (x_para - h)**2 + k

    y_max_left = PAD_B + PH * 0.40
    mask = np.ones(len(x_para), dtype=bool)
    for i in range(len(x_para)):
        if x_para[i] < h and y_para[i] > y_max_left:
            mask[i] = False
        if y_para[i] > PAD_B + PH * 0.96:
            mask[i] = False

    for offset, col, lw_v, alpha in [
        (0.00, CHARCOAL, 4.2, 0.85),
        (-0.04, DEEP_GREY, 2.5, 0.54),
        (0.04, DEEP_GREY, 2.5, 0.54),
        (-0.08, SLATE, 1.4, 0.31),
        (0.08, SLATE, 1.4, 0.31),
        (-0.13, MIST, 0.7, 0.14),
        (0.13, MIST, 0.7, 0.14),
    ]:
        xs_line = x_para[mask]
        ys_line = y_para[mask] + offset
        draw_lc(ax, xs_line, ys_line, col, lw=lw_v, alpha=alpha, zo=3)

    n_crowd = 60
    circle_r_base = PW * 0.013

    placed = []

    for i in range(n_crowd):
        r_c = circle_r_base * (0.6 + rng.rand() * 0.8)

        for attempt in range(300):
            dx = rng.randn() * PW * 0.08
            trial_x = h + dx + abs(dx) * 0.3
            trial_y_surface = a * (trial_x - h)**2 + k
            trial_y = trial_y_surface + r_c + rng.rand() * PH * 0.012

            ok = True
            for px, py, pr in placed:
                dist = np.sqrt((trial_x - px)**2 + (trial_y - py)**2)
                if dist < r_c + pr + 0.008:
                    ok = False
                    break

            if ok and PAD_L + 0.05 < trial_x < h + PW * 0.25:
                if trial_y < k + PH * 0.25:
                    placed.append((trial_x, trial_y, r_c))
                    break
        else:
            dx = rng.randn() * PW * 0.05
            trial_x = h + dx
            trial_y = k + r_c + abs(dx) * 0.2 + rng.rand() * PH * 0.02
            r_c *= 0.6
            placed.append((trial_x, trial_y, r_c))

    for px, py, pr in placed:
        dist_from_h = abs(px - h) / (PW * 0.25)
        alpha = 0.42 + 0.51 * (1 - min(dist_from_h, 1))

        col = DEEP_GREY if rng.rand() < 0.5 else SLATE
        theta = np.linspace(0, 2*np.pi, 400)
        cx_c = px + pr * np.cos(theta)
        cy_c = py + pr * np.sin(theta)
        draw_lc(ax, cx_c, cy_c, col, lw=1.4 + 0.7*pr/circle_r_base,
                alpha=alpha, zo=5)

        ax.add_patch(Circle((px, py), radius=pr,
                    facecolor=rgba(col, alpha * 0.20),
                    edgecolor='none', zorder=4))

    lone_x = PAD_L + PW * 0.90
    lone_y_surface = a * (lone_x - h)**2 + k
    lone_r = circle_r_base * 1.4
    lone_y = lone_y_surface + lone_r * 2.5

    theta = np.linspace(0, 2*np.pi, 600)

    for dr, lw_v, al in [(0, 3.5, 0.90), (0.018, 1.8, 0.54), (0.035, 0.84, 0.20)]:
        lx_r = lone_x + (lone_r + dr) * np.cos(theta)
        ly_r = lone_y + (lone_r + dr) * np.sin(theta)
        draw_lc(ax, lx_r, ly_r, LONE_GOLD, lw=lw_v, alpha=al, zo=6)

    ax.add_patch(Circle((lone_x, lone_y), radius=lone_r * 0.8,
                facecolor=rgba(LONE_GOLD, 0.37),
                edgecolor='none', zorder=5))
    ax.add_patch(Circle((lone_x, lone_y), radius=lone_r * 2.5,
                facecolor=rgba(WARM_ACCENT, 0.085),
                edgecolor='none', zorder=4))

    add_signature(fig, ax, BG)
    save(fig, "solitude_basin.pdf")

if __name__ == '__main__':
    render()
