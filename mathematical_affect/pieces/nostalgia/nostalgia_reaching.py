"""
Geometry of Feeling — Nostalgia: Reaching
Moving forward but always reaching back
y(t) -> inf, dy/dt -> 0
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
BG="#F0E8D8"

AMBER="#B8863A"; SEPIA="#8A6A42"; FADED_BLUE="#6A88A8"
OCHRE="#C4963A"; DUSTY_ROSE="#A07868"; OLD_GOLD="#A89048"
WARM_BROWN="#7A5A3A"; TARNISH="#887858"; FADED_WINE="#886068"

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
    if smooth>0: ys=gaussian_filter1d(ys,smooth)
    pts=np.array([xs,ys]).T.reshape(-1,1,2)
    segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
    lc=mc.LineCollection(segs,linewidths=lw,colors=[rgba(col,alpha)],
                         capstyle='round',joinstyle='round',zorder=zo)
    ax.add_collection(lc)

def draw_lc_tapered(ax, xs, ys, col, lw_start, lw_end, alpha_start, alpha_end, zo=4):
    n = len(xs)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    fracs = np.linspace(0, 1, n-1)
    lws = lw_start + (lw_end - lw_start) * fracs
    alphas = alpha_start + (alpha_end - alpha_start) * fracs
    colors = [rgba(col, float(a)) for a in alphas]
    lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def save(fig,name):
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig.savefig(os.path.join(OUTPUT_DIR,name),
                format='pdf',facecolor=BG)
    plt.close(fig); print(f"saved {name}")

def render():
    fig, ax = make_fig()
    rng = np.random.RandomState(42)

    origin_x = PAD_L + PW * 0.05
    origin_y = PAD_B + PH * 0.05
    dest_x = PAD_L + PW * 0.95
    dest_y = PAD_B + PH * 0.95

    n_stem = 3000
    t = np.linspace(0, 1, n_stem)

    stem_x = origin_x + (dest_x - origin_x) * t + PW * 0.06 * np.sin(t * np.pi * 2.2) * t
    stem_y = origin_y + (dest_y - origin_y) * t + PH * 0.04 * np.sin(t * np.pi * 1.8) * t

    for offset_x, offset_y, col, lw_base, alpha_base in [
        (0.0, 0.0, SEPIA, 6.3, 1.0),
        (-0.015, 0.015, WARM_BROWN, 3.92, 0.65),
        (0.015, -0.015, WARM_BROWN, 3.92, 0.65),
        (-0.04, 0.04, TARNISH, 1.96, 0.34),
        (0.04, -0.04, TARNISH, 1.96, 0.34),
        (-0.08, 0.08, TARNISH, 0.98, 0.14),
        (0.08, -0.08, TARNISH, 0.98, 0.14),
    ]:
        sx = stem_x + offset_x
        sy = stem_y + offset_y
        draw_lc_tapered(ax, sx, sy, col,
                        lw_start=lw_base, lw_end=lw_base * 0.06,
                        alpha_start=alpha_base, alpha_end=alpha_base * 0.20,
                        zo=5)

    n_tendrils = 22
    tendril_positions = np.linspace(0.08, 0.95, n_tendrils)

    cols = [AMBER, OCHRE, SEPIA, OLD_GOLD, WARM_BROWN, DUSTY_ROSE,
            FADED_BLUE, TARNISH, FADED_WINE, AMBER, OCHRE, SEPIA]

    for ti, pos in enumerate(tendril_positions):
        idx = int(pos * (n_stem - 1))
        dep_x = stem_x[idx]
        dep_y = stem_y[idx]

        n_arc = 1000
        t_arc = np.linspace(0, 1, n_arc)

        side = 1 if ti % 2 == 0 else -1
        swing_mag = PW * (0.06 + 0.22 * pos)

        perp_x = -side * 0.7
        perp_y = side * 0.7

        reach_back = 0.5 + 0.4 * pos
        end_x = dep_x + (origin_x - dep_x) * reach_back + rng.randn() * PW * 0.02
        end_y = dep_y + (origin_y - dep_y) * reach_back + rng.randn() * PH * 0.02

        mid_x = (dep_x + end_x) * 0.5 + swing_mag * perp_x
        mid_y = (dep_y + end_y) * 0.5 + swing_mag * perp_y

        ctrl1_x = dep_x + (mid_x - dep_x) * 0.6 + rng.randn() * PW * 0.02
        ctrl1_y = dep_y + (mid_y - dep_y) * 0.6 + rng.randn() * PH * 0.02
        ctrl2_x = mid_x + (end_x - mid_x) * 0.4 + rng.randn() * PW * 0.02
        ctrl2_y = mid_y + (end_y - mid_y) * 0.4 + rng.randn() * PH * 0.02

        arc_x = ((1-t_arc)**3 * dep_x +
                 3*(1-t_arc)**2*t_arc * ctrl1_x +
                 3*(1-t_arc)*t_arc**2 * ctrl2_x +
                 t_arc**3 * end_x)
        arc_y = ((1-t_arc)**3 * dep_y +
                 3*(1-t_arc)**2*t_arc * ctrl1_y +
                 3*(1-t_arc)*t_arc**2 * ctrl2_y +
                 t_arc**3 * end_y)

        thickness = 3.08 * (1 - pos * 0.5) * (0.7 + 0.3 * rng.rand())
        alpha = 0.77 * (1 - pos * 0.3)

        col = cols[ti % len(cols)]

        draw_lc_tapered(ax, arc_x, arc_y, col,
                        lw_start=thickness, lw_end=thickness * 0.10,
                        alpha_start=alpha, alpha_end=alpha * 0.15,
                        zo=3)

    for r_g, a_g in [(0.08, 0.85), (0.20, 0.34), (0.40, 0.12)]:
        ax.add_patch(Circle((origin_x, origin_y), radius=r_g,
                    facecolor=rgba(AMBER, a_g), edgecolor='none', zorder=6))

    add_signature(fig, ax, BG)
    save(fig, "nostalgia_reaching.pdf")

if __name__ == '__main__':
    render()
