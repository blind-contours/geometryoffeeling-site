"""
Geometry of Feeling — Awe: Awe Cosmic Web
Standalone render script
"""

"""
Geometry of Feeling — Awe: Cosmic Sublime (20 Candidates)

The overwhelming encounter with something vast, incomprehensible, beautiful.
Burke's "sublime", Kant's "dynamical sublime", the Overview Effect,
cathedral architecture, the Hubble Deep Field.

20 mathematical concepts embodying cosmic awe:
  1. Radiance (kept)       — inverse-square light emanation
  2. Singularity (kept)    — black hole accretion disk
  3. Nebula                — interstellar gas cloud (Perlin noise density)
  4. Solar Flare           — magnetic field eruption from a surface
  5. Murmuration           — emergent swarm (Boids-like)
  6. Cosmic Web            — large-scale filamentary structure
  7. Supernova             — radial shell expansion
  8. Spiral Galaxy         — logarithmic spiral arms
  9. Aurora                — charged-particle curtains
 10. Deep Field            — thousands of point sources at depth
 11. Eclipse               — solar corona during totality
 12. Gravitational Waves   — spacetime ripples
 13. Pulsar                — rotating beam sweep
 14. Stellar Nursery       — star-forming pillars
 15. Overview Effect       — thin blue line of atmosphere
 16. Cosmic Inflation      — exponential expansion
 17. Dark Matter Halo      — NFW profile density field
 18. Cathedral (kept)      — gothic arch geometry
 19. Chladni (kept)        — vibration plate patterns
 20. Emergence             — evolution of complexity from simplicity

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
"""

import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle, Ellipse
from scipy.ndimage import gaussian_filter1d, gaussian_filter
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#0A0A10"
MARGIN_COLOR = "#151b31"

# Palette: cosmic vast
COSMIC = "#2A3A8A"; NEBULA_P = "#5A3A8A"; STARLIGHT = "#C8C8D0"
VOID = "#1A1A40"; AZURE = "#3A5AA0"; CORONA = "#D0A040"
ULTRAVIOLET = "#4A2A7A"; DEEP = "#1A2A5A"; ICE = "#A0B0C8"
GOLD = "#D4AA40"; AMBER = "#C88030"; INDIGO = "#1A1A60"
CRIMSON = "#8A2020"; IVORY = "#D8D0C0"; SLATE = "#4A5A6A"
ROSE = "#8A3050"; TEAL = "#2A6A6A"; CYAN = "#3A8AAA"
PEACH = "#C89070"; MAGENTA = "#7A2A6A"; SILVER = "#A0A8B8"

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def make_fig():
    from matplotlib.patches import FancyBboxPatch, Rectangle
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(MARGIN_COLOR)
    ax.set_facecolor(MARGIN_COLOR)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), FIG_W, FIG_H, facecolor=MARGIN_COLOR,
                            edgecolor='none', zorder=-10))
    ml = FIG_W * 0.07; mr = FIG_W * 0.07
    mb = FIG_H * 0.08; mt = FIG_H * 0.08
    ax.add_patch(FancyBboxPatch((ml, mb), FIG_W - ml - mr, FIG_H - mb - mt,
                                 boxstyle="square,pad=0",
                                 facecolor=BG, edgecolor='none', zorder=0))
    zo = 1000
    ax.add_patch(Rectangle((0, 0), FIG_W, mb, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, FIG_H - mt), FIG_W, mt, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, 0), ml, FIG_H, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((FIG_W - mr, 0), mr, FIG_H, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    return fig, ax

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2; cy = PAD_B + PH / 2

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

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if len(xs) < 2: return
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def draw_tapered(ax, xs, ys, col, lw_start, lw_end, a_start, a_end, zo=4):
    """Draw a line with tapering width and alpha."""
    if len(xs) < 2: return
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    n = len(segs)
    alphas = np.linspace(a_start, a_end, n)
    lws = np.linspace(lw_start, lw_end, n)
    colors = [rgba(col, float(a)) for a in alphas]
    lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Ensure name ends with .pdf
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=MARGIN_COLOR)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

# ============================================================================
# 6. COSMIC WEB — large-scale filamentary structure
#    Nodes (galaxies) connected by filaments (dark matter)
# ============================================================================
def render():
    fig, ax = make_fig()
    np.random.seed(88)
    # Generate nodes via Poisson disk sampling approximation
    n_nodes = 120
    nodes_x = np.random.uniform(PAD_L + PW * 0.05, PAD_L + PW * 0.95, n_nodes)
    nodes_y = np.random.uniform(PAD_B + PH * 0.05, PAD_B + PH * 0.95, n_nodes)
    # Connect nearby nodes with filaments
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            dx = nodes_x[j] - nodes_x[i]
            dy = nodes_y[j] - nodes_y[i]
            dist = np.sqrt(dx**2 + dy**2)
            if dist < PW * 0.18:
                # Draw filament with some curvature
                t = np.linspace(0, 1, 200)
                mid_offset_x = np.random.normal(0, dist * 0.1)
                mid_offset_y = np.random.normal(0, dist * 0.1)
                # Quadratic Bezier
                mx = (nodes_x[i] + nodes_x[j]) / 2 + mid_offset_x
                my = (nodes_y[i] + nodes_y[j]) / 2 + mid_offset_y
                xs = (1 - t)**2 * nodes_x[i] + 2 * (1 - t) * t * mx + t**2 * nodes_x[j]
                ys = (1 - t)**2 * nodes_y[i] + 2 * (1 - t) * t * my + t**2 * nodes_y[j]
                # Thicker/brighter for shorter connections (denser regions)
                prox = 1 - dist / (PW * 0.18)
                alpha = 0.10 + 0.30 * prox
                lw = 0.25 + 0.55 * prox
                col = ICE if dist < PW * 0.06 else (AZURE if dist < PW * 0.10 else COSMIC)
                draw_lc(ax, xs, ys, col, lw=lw, alpha=alpha, zo=3)
                # Add a faint wider glow pass for close filaments
                if dist < PW * 0.08:
                    draw_lc(ax, xs, ys, AZURE, lw=lw * 2.0, alpha=alpha * 0.15, zo=2)
    # Draw nodes with glow
    for i in range(n_nodes):
        # Node brightness based on connectivity
        connections = sum(1 for j in range(n_nodes) if j != i and
                         np.sqrt((nodes_x[j]-nodes_x[i])**2+(nodes_y[j]-nodes_y[i])**2) < PW*0.18)
        brightness = min(connections / 6, 1.0)
        # Outer glow halo — tight pinprick effect
        for r_, a_ in [(0.08, 0.03 * brightness), (0.05, 0.10 * brightness),
                        (0.028, 0.25 * brightness), (0.013, 0.55 * brightness)]:
            ax.add_patch(Circle((nodes_x[i], nodes_y[i]), radius=r_,
                        facecolor=rgba(STARLIGHT, a_), edgecolor='none', zorder=5))
        # Bright white core
        if brightness > 0.15:
            ax.add_patch(Circle((nodes_x[i], nodes_y[i]), radius=0.008,
                        facecolor=rgba('#FFFFFF', 0.75 * brightness), edgecolor='none', zorder=6))
    add_signature(fig, ax, MARGIN_COLOR, margin_piece=True, margin_bottom=FIG_H * 0.08)
    save(fig, "awe_cosmic_web.pdf")

if __name__ == '__main__':
    render()
