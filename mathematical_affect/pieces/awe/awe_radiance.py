"""
Geometry of Feeling — Awe: Awe Radiance
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
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
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
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

# ============================================================================
# 1. RADIANCE — inverse-square light rays from center
# ============================================================================
def render():
    fig, ax = make_fig()
    n_rays = 150
    # Shorter rays — end well before canvas edges, trail off like eyelashes
    max_r = 3.8
    for i in range(n_rays):
        frac = i / (n_rays - 1)
        angle = frac * 2 * np.pi
        t = np.linspace(0, 1, 900)
        r = max_r * t
        curve = PW * 0.032 * np.sin(3 * t * np.pi + frac * 5)
        xs_r = cx + r * np.cos(angle) + curve * np.cos(angle + np.pi / 2)
        ys_r = cy + r * np.sin(angle) * (PH / PW) + curve * np.sin(angle + np.pi / 2) * (PH / PW)
        pts = np.array([xs_r, ys_r]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        n_s = len(segs)
        # Smooth Gaussian falloff based on distance from center
        seg_cx = 0.5 * (xs_r[:-1] + xs_r[1:])
        seg_cy = 0.5 * (ys_r[:-1] + ys_r[1:])
        dist = np.sqrt((seg_cx - cx)**2 + ((seg_cy - cy) * (PW / PH))**2)
        sigma = 2.8
        alphas = 0.55 * np.exp(-0.5 * (dist / sigma)**2)
        lws = np.clip(2.0 * np.exp(-0.5 * (dist / (sigma * 1.1))**2), 0.08, 2.0)
        col = CORONA if frac * n_rays % 3 < 1 else (STARLIGHT if frac * n_rays % 3 < 2 else AZURE)
        colors = [rgba(col, float(a_)) for a_ in alphas]
        lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                               capstyle='round', zorder=3)
        ax.add_collection(lc)
    # Tiny warm accent at the very core — small and subtle so the glow
    # comes from ray convergence, not from a separate halo.
    n_glow = 30
    max_glow_r = 0.35  # small core accent only
    for k in range(n_glow):
        glow_r = max_glow_r * (1 - k / n_glow)
        glow_a = 0.025 * np.exp(-0.5 * (glow_r / 0.10)**2)
        ax.add_patch(Circle((cx, cy), radius=glow_r,
                    facecolor=rgba(CORONA, glow_a), edgecolor='none', zorder=8))
    add_signature(fig, ax, BG)
    save(fig, "awe_radiance.pdf")

if __name__ == '__main__':
    render()
