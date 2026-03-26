"""
Geometry of Feeling — Awe: Awe Deep Field
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

def label(ax, eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.85,0.80,0.75,0.55),transform=ax.transData)
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
# 10. DEEP FIELD — thousands of point sources at varying depths
#     Hubble Ultra Deep Field: every speck is a galaxy
# ============================================================================
def render():
    fig, ax = make_fig()
    np.random.seed(99)

    # Tiny background point sources for density
    n_bg = 3000
    bg_x = np.random.uniform(PAD_L, PAD_L + PW, n_bg)
    bg_y = np.random.uniform(PAD_B, PAD_B + PH, n_bg)
    bg_cols = [np.random.choice([STARLIGHT, ICE, AZURE, GOLD, AMBER, '#7A3A9A',
               CRIMSON, TEAL, PEACH, CYAN]) for _ in range(n_bg)]
    bg_alphas = np.random.uniform(0.02, 0.10, n_bg)
    for i in range(n_bg):
        ax.plot(bg_x[i], bg_y[i], '.', color=rgba(bg_cols[i], bg_alphas[i]),
                markersize=np.random.uniform(0.2, 0.8), zorder=1)

    n_galaxies = 4000
    for i in range(n_galaxies):
        x = np.random.uniform(PAD_L, PAD_L + PW)
        y = np.random.uniform(PAD_B, PAD_B + PH)
        # "Redshift" = distance proxy — mixture for rich color diversity
        # 60% from moderate exponential (fills foreground+mid), 40% uniform (fills all bins)
        if np.random.random() < 0.6:
            z = np.random.exponential(0.5)
        else:
            z = np.random.uniform(0.0, 3.0)
        z = min(z, 3.0)
        size = 0.01 + 0.11 * np.exp(-z * 1.0)
        alpha = 0.15 + 0.75 * np.exp(-z * 0.65)
        # Rich multi-hue palette — random color family for even distribution
        # Each galaxy gets a random hue family, independent of redshift
        hue_roll = np.random.random()
        if hue_roll < 0.25:
            # Warm: orange, gold, amber, peach
            col = np.random.choice([GOLD, AMBER, CORONA, '#C88030', PEACH])
        elif hue_roll < 0.45:
            # Purple, magenta, rose
            col = np.random.choice([NEBULA_P, '#7A3A9A', MAGENTA, '#C06080', ROSE])
        elif hue_roll < 0.65:
            # Teal, cyan, azure
            col = np.random.choice([TEAL, CYAN, '#2A8A8A', AZURE, '#50A0A0'])
        elif hue_roll < 0.80:
            # Cool white, ice, starlight
            col = np.random.choice([STARLIGHT, ICE, '#6A9AB0', SILVER, '#A8B8C8'])
        elif hue_roll < 0.90:
            # Deep red, crimson
            col = np.random.choice([CRIMSON, '#B05030', ROSE, '#8A2A2A', '#A04040'])
        else:
            # Deep violet, ultraviolet
            col = np.random.choice([ULTRAVIOLET, '#4A2A6A', NEBULA_P, '#6A3A8A', INDIGO])
        # Some are spiral (two arms), some elliptical
        if np.random.random() < 0.4 and z < 1.5:
            # Two-arm spiral galaxy
            angle = np.random.uniform(0, 2 * np.pi)
            incl = np.random.uniform(0.3, 1.0)
            for arm_offset in [0, np.pi]:
                theta = np.linspace(0, 3 * np.pi, 80)
                r = size * 0.5 * theta / (3 * np.pi)
                gx = x + r * np.cos(theta + angle + arm_offset)
                gy = y + r * np.sin(theta + angle + arm_offset) * incl
                draw_lc(ax, gx, gy, col, lw=0.5 + size * 10, alpha=alpha * 0.6, zo=3)
            # Luminous core
            ax.add_patch(Circle((x, y), radius=size * 0.3,
                        facecolor=rgba(col, alpha * 0.9), edgecolor='none', zorder=4))
        else:
            # Elliptical
            e = np.random.uniform(0.5, 1.0)
            ax.add_patch(Ellipse((x, y), width=size * 2, height=size * 2 * e,
                        angle=np.random.uniform(0, 180),
                        facecolor=rgba(col, alpha * 0.5), edgecolor='none', zorder=3))
        # Multi-layer glow around brighter galaxies
        if z < 1.5:
            ax.add_patch(Circle((x, y), radius=size * 3.0,
                        facecolor=rgba(col, alpha * 0.05), edgecolor='none', zorder=2))
            ax.add_patch(Circle((x, y), radius=size * 5.0,
                        facecolor=rgba(col, alpha * 0.018), edgecolor='none', zorder=1))
    label(ax, "N(>S)\u223cS^{-3/2}")
    save(fig, "awe_deep_field.pdf")


if __name__ == '__main__':
    render()
