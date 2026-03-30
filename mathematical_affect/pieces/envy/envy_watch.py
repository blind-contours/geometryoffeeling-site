"""
Geometry of Feeling — Envy: Envy Watch
Standalone render script
"""

"""
Geometry of Feeling -- Envy (Final Series)

Curated target: An eye-like shape zoomed in and bold. Central bright point
with radiating curves that look like eyelashes. The composition fills
much more of the canvas. Bold colors, strong presence. The shape is wider
than tall, like a watching eye.

Background: mid-grey (#B0B0A8)
Palette: envious greens, sickly yellows
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

def draw_lc(ax,xs,ys,col,lw,alpha,zo=4,smooth=0):
    if smooth>0:
        ys=gaussian_filter1d(ys,smooth)
    pts=np.array([xs,ys]).T.reshape(-1,1,2)
    segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
    lc=mc.LineCollection(segs,linewidths=lw,colors=[rgba(col,alpha)],
                         capstyle='round',joinstyle='round',zorder=zo)
    ax.add_collection(lc)

def draw_lc_gradient(ax,xs,ys,col,lw_start,lw_end,a_start,a_end,zo=4,smooth=0):
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
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

# =============================================================================
# WATCH -- zoomed in, bold eye-like shape with eyelash-like radiating curves
# =============================================================================
def render():
    fig,ax=make_fig()
    np.random.seed(53)

    # Eye center
    eye_cx = cx
    eye_cy = cy

    # --- The watched one: bright center (iris/pupil) ---
    # Much larger glowing center
    for r, a in [(0.50, 0.04), (0.35, 0.08), (0.20, 0.14),
                 (0.12, 0.25), (0.06, 0.40), (0.03, 0.55)]:
        ax.add_patch(Circle((eye_cx, eye_cy), radius=r,
                    facecolor=rgba(ACID, a), edgecolor='none', zorder=7))

    # Small bright center dot
    ax.add_patch(Circle((eye_cx, eye_cy), radius=0.015,
                facecolor=rgba(BILE, 0.70), edgecolor='none', zorder=8))

    # --- Eyelash curves: radiating outward from center ---
    # These are the main visual element - bold, sweeping curves
    n_curves = 28
    cols = [COVET, BITTER, JEALOUS, VENOM, BILE, THORN, SHADOW_COL, PALLID]

    for i in range(n_curves):
        frac = i / (n_curves - 1)
        angle = 2 * np.pi * frac + np.random.uniform(-0.06, 0.06)

        t = np.linspace(0, 1, 600)

        # Start from center area, curve outward like eyelashes
        # Eye shape: wider horizontally, narrower vertically
        r_start = 0.20 + np.random.uniform(-0.05, 0.05)
        r_end = min(PW, PH) * 0.52 + np.random.uniform(-0.2, 0.4)

        r_t = r_start + (r_end - r_start) * t**0.6

        # Slight spiral/curve to make them look like lashes
        spiral = 0.15 * t + np.random.uniform(-0.05, 0.05)
        angle_t = angle + spiral

        # Eye aspect ratio - wider than tall
        x_stretch = 1.5  # horizontal stretch
        y_stretch = 0.7  # vertical compression

        xs_c = eye_cx + r_t * np.cos(angle_t) * x_stretch
        ys_c = eye_cy + r_t * np.sin(angle_t) * y_stretch

        # Clip to canvas
        mask = ((xs_c > PAD_L) & (xs_c < PAD_L + PW) &
                (ys_c > PAD_B) & (ys_c < PAD_B + PH))
        if mask.sum() < 3:
            continue

        col = cols[i % len(cols)]

        # Bold: thicker lines, higher alpha - gradient from center outward
        lw_start = 1.8 + np.random.uniform(-0.3, 0.3)
        lw_end = 0.5 + np.random.uniform(-0.2, 0.2)
        a_start = 0.55
        a_end = 0.15

        # Find contiguous segments
        in_seg = False; start = 0; segments = []
        for j in range(len(mask)):
            if mask[j] and not in_seg:
                start = j; in_seg = True
            elif not mask[j] and in_seg:
                if j - start >= 3:
                    segments.append((xs_c[start:j], ys_c[start:j]))
                in_seg = False
        if in_seg and len(mask) - start >= 3:
            segments.append((xs_c[start:], ys_c[start:]))

        for seg_xs, seg_ys in segments:
            draw_lc_gradient(ax, seg_xs, seg_ys, col,
                            lw_start, lw_end, a_start, a_end,
                            zo=3 + i % 3, smooth=2)

    # --- Additional subtle eyelash details: shorter, finer curves ---
    for i in range(40):
        angle = np.random.uniform(0, 2*np.pi)
        t = np.linspace(0, 1, 300)
        r_start = 0.30 + np.random.uniform(-0.05, 0.10)
        r_end = 0.60 + np.random.uniform(0, 0.80)
        r_t = r_start + (r_end - r_start) * t**0.5
        spiral = np.random.uniform(-0.1, 0.2) * t
        angle_t = angle + spiral
        xs_c = eye_cx + r_t * np.cos(angle_t) * 1.5
        ys_c = eye_cy + r_t * np.sin(angle_t) * 0.7
        mask = ((xs_c > PAD_L) & (xs_c < PAD_L + PW) &
                (ys_c > PAD_B) & (ys_c < PAD_B + PH))
        if mask.sum() < 3:
            continue
        col = cols[i % len(cols)]
        in_seg = False; start = 0; segments = []
        for j in range(len(mask)):
            if mask[j] and not in_seg:
                start = j; in_seg = True
            elif not mask[j] and in_seg:
                if j - start >= 3:
                    segments.append((xs_c[start:j], ys_c[start:j]))
                in_seg = False
        if in_seg and len(mask) - start >= 3:
            segments.append((xs_c[start:], ys_c[start:]))
        for seg_xs, seg_ys in segments:
            draw_lc(ax, seg_xs, seg_ys, col, lw=0.5, alpha=0.15, zo=2)

    add_signature(fig, ax, BG)
    save(fig,"envy_watch.pdf")

if __name__ == '__main__':
    render()
