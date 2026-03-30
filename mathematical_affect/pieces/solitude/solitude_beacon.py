"""
Geometry of Feeling — Solitude: Solitude Beacon
Standalone render script
"""

"""
Geometry of Feeling -- Solitude (Final Series v2)

Curated target: One isolated "person" (concentric circles with gold center)
at the top-right, radiating outward in blue/grey. Many small "people"
(concentric circle clusters) gathered at the bottom-left like droplets.
The solitary beacon stands apart, radiating.

Background: cool parchment (#E0DDD6)
Palette: deep grey, dark green, warm gold accent
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
BG="#E0DDD6"

# Palette
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

def draw_ripple_droplet(ax, px, py, n_rings, max_r, wavelength=None,
                        color_func=None, alpha_base=0.35, lw_base=0.8,
                        center_color=None, center_radius=0.0, zo_base=4):
    """Draw a physics-based water droplet ripple — perfect concentric circles.

    Physics model:
    - Rings are evenly spaced (constant wavelength, like real water waves)
    - Alpha decreases with 1/sqrt(r) (energy conservation in 2D circular waves)
    - Linewidth also decreases with distance from center
    - No wobble — viewed from above, water ripples are perfect circles
    """
    theta = np.linspace(0, 2*np.pi, 600)

    # Constant wavelength: evenly spaced rings
    if wavelength is None:
        wavelength = max_r / max(n_rings, 1)

    for i in range(n_rings):
        r = wavelength * (i + 1)
        if r > max_r:
            break

        # Physics: amplitude ~ 1/sqrt(r) for 2D circular waves
        r_frac = r / max_r
        decay = 1.0 / np.sqrt(1.0 + 4.0 * r_frac)

        alpha = alpha_base * decay
        lw = lw_base * decay

        # Get color from color function
        if color_func is not None:
            col = color_func(r_frac)
        else:
            col = "#3A6A9A"

        # Perfect circles — no wobble
        xs = px + r * np.cos(theta)
        ys = py + r * np.sin(theta)

        draw_lc(ax, xs, ys, col, lw=max(lw, 0.12), alpha=max(alpha, 0.02),
                zo=zo_base + max(0, int((1 - r_frac) * 3)))

    # Center dot
    if center_color is not None and center_radius > 0:
        ax.add_patch(Circle((px, py), radius=center_radius,
                    facecolor=center_color, edgecolor='none',
                    zorder=zo_base + 5))

def beacon_color(frac):
    """Color function for the beacon droplet: gold -> warm -> blue -> grey mist."""
    if frac < 0.08:
        return "#D4A840"    # gold center
    elif frac < 0.15:
        return "#C8963A"    # warm accent
    elif frac < 0.20:
        return "#B08030"    # transition warm-to-blue
    elif frac < 0.50:
        return "#3A6A9A"    # bold blue
    elif frac < 0.65:
        return "#4A7AAA"    # medium blue
    elif frac < 0.80:
        return "#8A9AA8"    # grey mist
    else:
        return "#BAC8D4"    # light grey mist

def crowd_color(frac):
    """Color function for crowd droplets: blue tones throughout, darker for contrast."""
    if frac < 0.30:
        return "#2A5A8A"    # deep blue (darker for inner rings)
    elif frac < 0.60:
        return "#3A6A9A"    # bold blue
    else:
        return "#4A7AAA"    # medium blue

def render():
    fig, ax = make_fig()
    np.random.seed(42)

    # ================================================================
    # THE BEACON — one large, prominent droplet at top-right
    # ================================================================
    beacon_x = cx + PW * 0.28
    beacon_y = cy + PH * 0.22
    beacon_max_r = min(PW, PH) * 0.32
    beacon_n_rings = 28

    # Beacon: gold center glow (layered circles for soft gradient)
    beacon_center_r = beacon_max_r * 0.035
    for r_g, a_g in [(beacon_center_r * 3.0, 0.08),
                     (beacon_center_r * 2.0, 0.18),
                     (beacon_center_r * 1.2, 0.40),
                     (beacon_center_r, 0.65)]:
        ax.add_patch(Circle((beacon_x, beacon_y), radius=r_g,
                    facecolor=rgba("#D4A840", a_g), edgecolor='none',
                    zorder=8))

    # Beacon ripple rings — physics-based
    # Inner gold rings (2-3), then blue rings (5-6 bold), then grey fade
    beacon_wavelength = beacon_max_r / beacon_n_rings

    def beacon_alpha(frac):
        """Higher contrast for beacon: strong inner, fading outer."""
        if frac < 0.15:
            return 0.65     # gold rings: very visible
        elif frac < 0.50:
            return 0.40     # blue rings: bold
        else:
            # Fade from 0.25 down to 0.04
            t = (frac - 0.50) / 0.50
            return 0.25 * (1 - t) + 0.04 * t

    theta = np.linspace(0, 2*np.pi, 600)
    for i in range(beacon_n_rings):
        r = beacon_wavelength * (i + 1)
        if r > beacon_max_r:
            break
        frac = r / beacon_max_r
        col = beacon_color(frac)

        # Physics: 1/sqrt(r) decay for linewidth
        decay_lw = 1.0 / np.sqrt(1.0 + 3.5 * frac)
        lw = 1.4 * decay_lw
        alpha = beacon_alpha(frac)

        xs = beacon_x + r * np.cos(theta)
        ys = beacon_y + r * np.sin(theta)

        draw_lc(ax, xs, ys, col, lw=max(lw, 0.15), alpha=max(alpha, 0.02),
                zo=5 + max(0, int((1 - frac) * 3)))

    # ================================================================
    # THE CROWD — 14 smaller droplets scattered across bottom-left
    # ================================================================
    # Wide spatial distribution; each creates independent ripples
    crowd_center_x = cx - PW * 0.22
    crowd_center_y = cy - PH * 0.18

    n_crowd = 14

    # Pre-defined spread: use uniform random in a wide region
    # rather than exponential from a center, to get better spread
    crowd_positions = []
    rng = np.random.RandomState(42)

    for i in range(n_crowd):
        # Spread across the bottom-left quadrant with wide distribution
        px = crowd_center_x + rng.uniform(-PW * 0.32, PW * 0.28)
        py = crowd_center_y + rng.uniform(-PH * 0.28, PH * 0.32)

        # Keep within canvas bounds, biased toward bottom-left
        px = np.clip(px, PAD_L + 0.4, cx + PW * 0.08)
        py = np.clip(py, PAD_B + 0.3, cy + PH * 0.12)
        crowd_positions.append((px, py))

    # Assign varied sizes: some tiny (3 rings), some medium (6-8 rings)
    crowd_ring_counts = [
        3, 6, 4, 8, 3, 5, 7, 4, 3, 6, 5, 8, 3, 4
    ]
    crowd_sizes = [
        0.30, 0.55, 0.38, 0.65, 0.25, 0.45, 0.60, 0.35,
        0.28, 0.50, 0.42, 0.62, 0.26, 0.38
    ]

    blue_colors = ["#3A6A9A", "#4A7AAA", "#5A8ABB"]

    for i, (px, py) in enumerate(crowd_positions):
        n_rings = crowd_ring_counts[i % len(crowd_ring_counts)]
        size_factor = crowd_sizes[i % len(crowd_sizes)]
        max_r = size_factor * min(PW, PH) * 0.12

        wavelength = max_r / max(n_rings, 1)

        # Draw ripple rings — blue, high contrast
        for j in range(n_rings):
            r = wavelength * (j + 1)
            if r > max_r:
                break
            frac = r / max_r

            # Physics: 1/sqrt(r) energy decay — gentler falloff
            decay = 1.0 / np.sqrt(1.0 + 1.5 * frac)

            # High contrast: inner rings 0.55, outer fade to 0.10
            alpha = 0.55 * decay
            if frac > 0.6:
                alpha *= (1.0 - 0.5 * (frac - 0.6) / 0.4)
            alpha = max(alpha, 0.10)

            lw = 1.0 * decay
            col = crowd_color(frac)

            xs = px + r * np.cos(theta)
            ys = py + r * np.sin(theta)

            draw_lc(ax, xs, ys, col, lw=max(lw, 0.20),
                    alpha=max(alpha, 0.06), zo=3)

        # Small dark center dot for each crowd droplet
        dot_r = max_r * 0.07
        ax.add_patch(Circle((px, py), radius=max(dot_r, 0.03),
                    facecolor=rgba("#2A3A4A", 0.55), edgecolor='none',
                    zorder=6))

    # ================================================================
    # EQUATION LABEL
    # ================================================================
    add_signature(fig, ax, BG)
    save(fig, "solitude_beacon")

if __name__ == '__main__':
    render()
