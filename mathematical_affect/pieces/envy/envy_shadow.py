"""
Geometry of Feeling — Envy: Envy Shadow
Standalone render script
"""

"""
Geometry of Feeling -- Envy (Final Series)

Curated target: Two waveforms spanning the full width, same general shape
but slightly different. One always above (the one who has), one always
below (the one who envies). The gap between them is the envy - filled
with a subtle wash. Same color family (greens) for both.

Background: mid-grey (#B0B0A8)
Palette: envious greens, sickly yellows
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
BG="#B0B0A8"

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
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


# =============================================================================
# SHADOW -- two waveforms, same shape moved up and down,
#    slightly different, gap between = the envy
# =============================================================================
def render():
    fig,ax=make_fig()
    np.random.seed(77)

    n_pts = 3000
    t = np.linspace(0, 4*np.pi, n_pts)
    xs = PAD_L + PW * (t - t.min()) / (t.max() - t.min())

    # Base waveform - rich, organic undulation
    base_wave = (PH * 0.10 * np.sin(t * 0.8) +
                 PH * 0.06 * np.sin(t * 1.7 + 0.5) +
                 PH * 0.04 * np.cos(t * 2.9 + 1.2) +
                 PH * 0.025 * np.sin(t * 4.1 + 2.0))
    base_wave = gaussian_filter1d(base_wave, 15)

    # Center of the composition - upper portion of canvas
    center_y = cy + PH * 0.12

    # Gap between the curves
    gap = PH * 0.12

    # --- Upper curve (the one who has everything) ---
    # Slightly different shape - more elevated, confident undulation
    upper_variation = (PH * 0.02 * np.sin(t * 3.2 + 1.0) +
                       PH * 0.015 * np.cos(t * 5.1 + 0.3))
    upper_variation = gaussian_filter1d(upper_variation, 10)
    upper_y = center_y + gap/2 + base_wave + upper_variation

    # --- Lower curve (the one who envies) ---
    # Same general shape but slightly different - it follows but never catches up
    lower_variation = (PH * 0.025 * np.sin(t * 2.8 + 2.5) +
                       PH * 0.018 * np.cos(t * 4.5 + 1.8))
    lower_variation = gaussian_filter1d(lower_variation, 12)
    lower_y = center_y - gap/2 + base_wave + lower_variation

    # Ensure upper is always above lower
    min_gap = PH * 0.04
    for j in range(len(upper_y)):
        if upper_y[j] - lower_y[j] < min_gap:
            mid = (upper_y[j] + lower_y[j]) / 2
            upper_y[j] = mid + min_gap/2
            lower_y[j] = mid - min_gap/2

    # --- Fill the gap (the envy itself) ---
    ax.fill_between(xs, lower_y, upper_y,
                    color=rgba(JEALOUS, 0.08), linewidth=0, zorder=2)

    # --- Vertical gap indicators ---
    n_indicators = 50
    idx_positions = np.linspace(30, n_pts-30, n_indicators).astype(int)
    for idx in idx_positions:
        gap_here = upper_y[idx] - lower_y[idx]
        gap_norm = gap_here / (PH * 0.30)
        ax.plot([xs[idx], xs[idx]],
                [lower_y[idx], upper_y[idx]],
                color=rgba(ACID, 0.04 + 0.06 * gap_norm),
                linewidth=0.3, zorder=2)

    # --- Draw upper curve - vivid, in acid/olive green ---
    draw_lc(ax, xs, upper_y, ACID, lw=1.8, alpha=0.60, zo=6, smooth=3)

    # --- Draw lower curve - darker green, same weight ---
    draw_lc(ax, xs, lower_y, COVET, lw=1.4, alpha=0.50, zo=5, smooth=3)

    # --- Underneath set: fainter echo lines below the lower curve ---
    # These create depth — like the envy has layers beneath
    for echo_i in range(5):
        echo_offset = PH * (0.06 + echo_i * 0.04)
        echo_variation = (PH * 0.015 * np.sin(t * (2.5 + echo_i * 0.6) + echo_i * 1.2) +
                          PH * 0.01 * np.cos(t * (3.8 + echo_i * 0.4) + echo_i * 0.7))
        echo_variation = gaussian_filter1d(echo_variation, 14)
        echo_y = lower_y - echo_offset + echo_variation
        echo_alpha = 0.30 - echo_i * 0.05
        echo_lw = 1.0 - echo_i * 0.12
        echo_col = SHADOW_COL if echo_i % 2 == 0 else BITTER
        draw_lc(ax, xs, echo_y, echo_col, lw=echo_lw, alpha=echo_alpha, zo=4 - echo_i, smooth=4)

    label(ax,"d(t)=f(t)\u2212g(t)>0  \u2200t   \u2014   shadow:  one always above,  one always reaching,  the gap is the envy")
    save(fig,"envy_shadow.pdf")


if __name__ == '__main__':
    render()
