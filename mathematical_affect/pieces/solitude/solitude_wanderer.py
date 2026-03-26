"""
Geometry of Feeling — Solitude: Solitude Wanderer
Standalone render script
"""

"""
Geometry of Feeling -- Solitude (Final Series v2)
Twenty candidates: 5 enhanced originals + 15 new concepts

User feedback: "Wanderer good but feels lost. Lighthouse needs much more.
Colors are good but images too boring/light."
Direction: Keep the cool palette but DRAMATICALLY increase visual presence.
Stronger signals, more atmospheric depth, bolder marks.

Background: cool parchment (#E0DDD6) -- slightly warmer than v1
Palette: deep grey, dark green, warm gold accent -- but alpha cranked up
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
BG="#E0DDD6"

# Palette — same hues as v1, but richer
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

def label(ax,eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.25,0.28,0.30,0.25),transform=ax.transData)
def split_segments(xs, ys, mask):
    segments = []
    in_seg = False; start = 0
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


# =============================================================================
# 1. WANDERER (ENHANCED) -- much longer, bolder random walk
#    Path is thicker, higher alpha, with atmospheric haze around it
# =============================================================================
def render():
    fig,ax=make_fig()
    np.random.seed(12)
    n_steps=30000

    dx = np.random.randn(n_steps) * PW * 0.003
    dy = np.random.randn(n_steps) * PH * 0.003
    drift_freq = 2 * np.pi * np.arange(n_steps) / n_steps
    dx += PW * 0.0010 * np.sin(drift_freq * 3.0 + 0.5)
    dy += PH * 0.0008 * np.cos(drift_freq * 2.3 + 1.2)
    dx += PW * 0.0006 * np.cos(drift_freq * 5.7 + 2.1)
    dy += PH * 0.0005 * np.sin(drift_freq * 4.1 + 0.8)

    xs_w = cx - PW*0.3 + np.cumsum(dx)
    ys_w = cy - PH*0.2 + np.cumsum(dy)

    for _ in range(3):
        xs_w = np.where(xs_w < PAD_L + PW*0.02, 2*(PAD_L + PW*0.02) - xs_w, xs_w)
        xs_w = np.where(xs_w > PAD_L + PW*0.98, 2*(PAD_L + PW*0.98) - xs_w, xs_w)
        ys_w = np.where(ys_w < PAD_B + PH*0.02, 2*(PAD_B + PH*0.02) - ys_w, ys_w)
        ys_w = np.where(ys_w > PAD_B + PH*0.98, 2*(PAD_B + PH*0.98) - ys_w, ys_w)

    mask = ((xs_w > PAD_L) & (xs_w < PAD_L+PW) &
            (ys_w > PAD_B) & (ys_w < PAD_B+PH))

    step_frac = np.arange(n_steps) / n_steps
    fade = (0.5 + 0.5 * np.sin(2*np.pi*step_frac*7.3 + 0.4)
            * np.sin(2*np.pi*step_frac*3.1 + 1.7))
    fade *= (0.6 + 0.4 * np.sin(2*np.pi*step_frac*11.7 + 2.3))
    fade *= (0.7 + 0.3 * np.sin(2*np.pi*step_frac*23.0 + 0.9))
    fade = (fade - fade.min()) / (fade.max() - fade.min() + 1e-9)
    fade = fade ** 1.2  # less aggressive power curve -- more visible overall

    # Atmospheric haze layer -- thick, very faint, shows the general territory
    for seg_xs, seg_ys in split_segments(xs_w, ys_w, mask):
        if len(seg_xs) < 10:
            continue
        # Haze: smoothed, thick, faint
        draw_lc(ax, seg_xs, seg_ys, MIST, lw=4.9, alpha=0.07, zo=2, smooth=40)

    # Main path with enhanced visibility
    for seg_xs, seg_ys in split_segments(xs_w, ys_w, mask):
        if len(seg_xs) < 5:
            continue
        pts = np.array([seg_xs, seg_ys]).T.reshape(-1,1,2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        n_s = len(segs)

        dists = (xs_w - seg_xs[0])**2 + (ys_w - seg_ys[0])**2
        start_idx = np.argmin(dists)
        seg_fade = fade[start_idx:start_idx+n_s]
        if len(seg_fade) < n_s:
            seg_fade = np.pad(seg_fade, (0, n_s-len(seg_fade)), mode='edge')

        # MUCH higher alphas than v1
        alphas = 0.14 + 0.93 * seg_fade
        lws = 0.42 + 1.68 * seg_fade

        colors = []
        for k in range(n_s):
            idx = start_idx + k
            phase = np.sin(2*np.pi*(idx/n_steps)*5.0)
            if phase > 0.3:
                colors.append(rgba(DEEP_GREY, float(alphas[k])))
            elif phase < -0.3:
                colors.append(rgba(DARK_GREEN, float(alphas[k] * 0.85)))
            else:
                colors.append(rgba(SLATE, float(alphas[k] * 0.7)))

        lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                               capstyle='round', zorder=3)
        ax.add_collection(lc)

    if mask.sum() > 0:
        last_valid = np.where(mask)[0][-1]
        ax.plot(xs_w[last_valid], ys_w[last_valid], 'o',
                color=rgba(WARM_ACCENT, 0.95), markersize=5.5,
                markeredgewidth=0, zorder=6)

    label(ax,"x(n)=x(n\u22121)+\u03be")
    save(fig,"solitude_wanderer")


if __name__ == '__main__':
    render()
