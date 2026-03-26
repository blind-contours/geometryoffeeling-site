"""
Geometry of Feeling — Envy: Envy Mirror
Standalone render script
"""

"""
Geometry of Feeling -- Envy (Final Series)
Five pieces: Covet, Watch, Glass Ceiling, Shadow, Mirror

Mathematical primitives: asymptotic approach, radial surveillance spirals,
capped saturation curves, parametric reflection gap, diminished reflection

Background: mid-grey (#B0B0A8) -- bile-tinged neutrality
Palette: envious greens, sickly yellows, bitter cold accents
Equation opacity 0.28, series label 0.18

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
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
BG="#B0B0A8"  # mid-grey

# Palette: envious greens, sickly yellows, bitter cold accents
BILE="#7A8A30"; COVET="#3A5A30"; BITTER="#5A6A38"; ACID="#8A9A28"
JEALOUS="#4A6A3A"; THORN="#5A5A28"; PALLID="#8A9A70"; VENOM="#4A5A20"
SHADOW_COL="#4A4A40"

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
            color=(0.15,0.15,0.20,0.28),transform=ax.transData)
def split_segments(xs, ys, mask):
    """Split masked arrays into contiguous segments."""
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
    """Draw line collection with gradient alpha and linewidth."""
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


# =============================================================================
# 5. MIRROR -- a function reflected across an axis, but the reflection
#    is slightly diminished/distorted -- always less than the original
# =============================================================================
def render():
    fig,ax=make_fig()
    t=np.linspace(0,1,2500); xs=PAD_L+PW*t

    # Mirror axis
    mirror_y = cy
    ax.plot([PAD_L, PAD_L+PW], [mirror_y, mirror_y],
            color=rgba(SHADOW_COL, 0.17), linewidth=0.7, linestyle=':', zorder=2)

    n_pairs = 14
    for i in range(n_pairs):
        frac = i / (n_pairs - 1)
        omega = 2 + frac * 5
        amp = PH * (0.04 + frac * 0.08)
        phase = frac * 0.8

        # The original -- full amplitude above the mirror
        wave = amp * np.sin(omega * np.pi * t + phase)
        ys_orig = mirror_y + PH*0.04 + np.abs(wave) + PH*0.005*np.sin(3.7*omega*np.pi*t)

        # The reflection -- below the mirror, diminished
        # Shrink factor varies per curve and along the curve (non-uniform distortion)
        shrink_base = 0.35 + frac * 0.20  # always less than 1
        # Add spatial distortion -- the reflection warps
        distortion = 1 + 0.15 * np.sin(1.5 * np.pi * t + frac * 2.0)
        shrink = shrink_base * distortion

        ys_refl = mirror_y - PH*0.04 - np.abs(wave) * shrink - PH*0.003*np.sin(3.7*omega*np.pi*t)

        # Original: vivid
        if frac < 0.3: col_o = ACID; col_r = SHADOW_COL
        elif frac < 0.6: col_o = BILE; col_r = BITTER
        else: col_o = PALLID; col_r = COVET

        draw_lc(ax, xs, ys_orig, col_o, lw=1.4+0.7*frac, alpha=0.65+0.20*frac, zo=5, smooth=3)
        draw_lc(ax, xs, ys_refl, col_r, lw=0.6+0.4*frac, alpha=0.28+0.15*frac, zo=3, smooth=3)

        # Faint fill between mirror and each curve to show the asymmetry
        if i % 3 == 0:
            ax.fill_between(xs, mirror_y, ys_orig,
                            color=rgba(ACID, 0.022 + 0.008*frac), linewidth=0, zorder=1)
            ax.fill_between(xs, ys_refl, mirror_y,
                            color=rgba(COVET, 0.015 + 0.005*frac), linewidth=0, zorder=1)

    # Label the asymmetry
    ax.text(PAD_L + PW*0.02, mirror_y + PH*0.32, "f(t)",
            fontfamily='monospace', fontsize=6, color=rgba(ACID, 0.25))
    ax.text(PAD_L + PW*0.02, mirror_y - PH*0.25, "\u03b1\u00b7f(t)",
            fontfamily='monospace', fontsize=6, color=rgba(COVET, 0.20))

    label(ax,"g(t)=\u03b1(t)\u00b7f(t),  \u03b1<1")
    save(fig,"envy_mirror.pdf")


if __name__ == '__main__':
    render()
