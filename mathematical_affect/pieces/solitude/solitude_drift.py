"""
Geometry of Feeling — Solitude: Drift
28 wave equations flowing horizontally at different heights.
One gold line cuts diagonally from bottom-left to top-right,
riding the crests — surfing from one wave peak to the next.
η(x) = A₁sin(k₁x + φ₁) + A₂cos(k₂x + φ₂)
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

OCEAN_DEEP="#2B4A6B"; OCEAN_MID="#3D6B8E"
OCEAN_STEEL="#4A7A9A"; OCEAN_FOAM="#6A9AB8"
OCEAN_PALE="#8AB4CC"

WAVE_COLORS = [OCEAN_DEEP, OCEAN_MID, OCEAN_STEEL, OCEAN_FOAM, OCEAN_PALE,
               TEAL, SLATE, DUSK, MIST, CHARCOAL]

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
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR,name),
                format='pdf',facecolor=BG)
    plt.close(fig); print(f"saved {name}")

def render():
    fig, ax = make_fig()
    rng = np.random.RandomState(31)

    n_pts = 4000
    t = np.linspace(0, 1, n_pts)
    xs = PAD_L + PW * t

    n_waves = 28
    wave_amp = 0.04
    wave_spread = 0.82

    waves = []

    for i in range(n_waves):
        frac = i / (n_waves - 1)
        y_center = PAD_B + PH * (0.10 + wave_spread * frac)

        freq1 = rng.uniform(2.5, 8.0)
        freq2 = rng.uniform(1.0, 4.0)
        phase1 = rng.uniform(0, 2 * np.pi)
        phase2 = rng.uniform(0, 2 * np.pi)
        amp1 = wave_amp * PH * rng.uniform(0.6, 1.0)
        amp2 = wave_amp * PH * rng.uniform(0.2, 0.5)

        eta = (amp1 * np.sin(2 * np.pi * freq1 * t + phase1) +
               amp2 * np.cos(2 * np.pi * freq2 * t + phase2))

        ys = y_center + eta
        waves.append((y_center, ys))

        col = WAVE_COLORS[i % len(WAVE_COLORS)]
        alpha = 0.30 * rng.uniform(0.7, 1.0)
        lw = 0.8 * rng.uniform(0.7, 1.3)
        draw_lc(ax, xs, ys, col, lw, alpha, zo=3, smooth=2)
        draw_lc(ax, xs, ys + PH * 0.008, col, lw * 0.4, alpha * 0.2, zo=2, smooth=4)

    # Gold line — diagonal path riding the wave crests
    guide_y_start = PAD_B + PH * 0.08
    guide_y_end = PAD_B + PH * 0.92
    guide_ys = guide_y_start + (guide_y_end - guide_y_start) * t

    gold_ys = np.zeros(n_pts)
    gold_snap_strength = 1.2

    for j in range(n_pts):
        best_score = np.inf
        best_y = guide_ys[j]

        for wi, (y_center, ys) in enumerate(waves):
            wave_y = ys[j]
            dist = abs(wave_y - guide_ys[j])

            if j > 5 and j < n_pts - 5:
                local_region = ys[j-5:j+5]
                is_near_peak = (wave_y >= np.max(local_region) - PH * 0.005)
                peak_bonus = 0.0 if is_near_peak else PH * 0.08
            else:
                peak_bonus = 0.0

            score = dist * gold_snap_strength + peak_bonus
            if score < best_score:
                best_score = score
                best_y = wave_y

        gold_ys[j] = best_y

    gold_ys = gaussian_filter1d(gold_ys, sigma=30)

    draw_lc(ax, xs, gold_ys, LONE_GOLD, 2.5, 0.85, zo=6, smooth=3)
    for offset, alpha, lw in [(PH*0.006, 0.30, 1.25),
                               (PH*0.012, 0.12, 0.75),
                               (-PH*0.004, 0.18, 1.0)]:
        draw_lc(ax, xs, gold_ys + offset, WARM_ACCENT, lw, alpha, zo=5, smooth=5)

    add_signature(fig, ax, BG)
    save(fig, "solitude_drift")

if __name__ == '__main__':
    render()
