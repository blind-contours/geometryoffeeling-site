"""
Geometry of Feeling — Growth: Growth Logistic Cascade
Standalone render script
"""

import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import os

DPI=300; FIG_W=12; FIG_H=8
BG="#F5F0E6"

# Palette
MOSS="#4A7A3A"; LEAF="#6A9A4A"; GOLD="#C8920A"; AMBER="#D4A832"
CORAL="#C8603A"; SAGE="#7A9A6A"; SPRING="#8AB84A"; DARK_G="#2A4A1A"; TEAL="#3A8A6A"

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

def split_segments(xs, ys):
    """Convert x,y arrays into line segments for LineCollection."""
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    return segs

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4):
    segs = split_segments(xs, ys)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def render():
    fig, ax = make_fig()
    t = np.linspace(0, 1, 1500)
    xs = PAD_L + PW * t

    n_curves = 40
    np.random.seed(42)

    # Create a field of logistic curves at varying carrying capacities and rates
    # Each curve represents a population finding its own ceiling
    carrying_caps = np.linspace(0.08, 0.95, n_curves)
    growth_rates = np.linspace(6, 18, n_curves)

    colors_list = [DARK_G, MOSS, LEAF, SAGE, SPRING, TEAL, GOLD, AMBER, CORAL]

    for i in range(n_curves):
        frac = i / (n_curves - 1)

        K = PAD_B + PH * carrying_caps[i]  # carrying capacity in plot coords
        P0_frac = 0.02 + 0.03 * np.random.rand()  # small initial population
        P0 = PAD_B + PH * P0_frac
        r = growth_rates[i] + np.random.randn() * 0.8

        # Logistic equation
        ys = K / (1.0 + ((K - P0) / (P0 + 1e-9)) * np.exp(-r * t))

        # Add subtle organic variation
        wobble = PH * 0.003 * np.sin(t * np.pi * (4 + frac * 3) + i * 0.7) * (1 - t**2)
        ys = np.clip(ys + wobble, PAD_B + PH * 0.01, PAD_B + PH * 0.98)

        # Color by carrying capacity height
        ci = int(frac * (len(colors_list) - 1))
        col = colors_list[ci]

        # Alpha and linewidth: inner curves more visible
        center_dist = abs(frac - 0.5) * 2
        alpha = 0.12 + 0.52 * (1 - center_dist * 0.6)
        lw = 0.3 + 1.8 * (1 - center_dist * 0.4)

        draw_lc(ax, xs, ys, col, lw=lw, alpha=alpha, zo=3)

        # Draw faint carrying capacity line
        ax.plot([PAD_L, PAD_L + PW], [K, K],
                color=rgba(col, 0.04), linewidth=0.25, zorder=2)

    # Add the inflection envelope — the line where growth rate is maximum
    # For logistic: inflection at P = K/2
    env_t = np.linspace(0, 1, 200)
    env_ys = PAD_B + PH * np.linspace(0.04, 0.475, 200)
    env_xs = np.full_like(env_ys, PAD_L + PW * 0.5)
    # Vertical line marking midpoint of S-curves
    draw_lc(ax, np.full(200, cx), env_ys, GOLD, lw=0.5, alpha=0.10, zo=2)

    add_signature(fig, ax, BG)
    save(fig, "growth_logistic_cascade.pdf")

if __name__ == '__main__':
    render()
