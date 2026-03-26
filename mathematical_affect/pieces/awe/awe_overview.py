"""
Geometry of Feeling — Awe: Awe Overview
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
# 15. OVERVIEW EFFECT — Earth's atmosphere as a thin luminous line
#     The view from orbit: thin blue arc against black
# ============================================================================
def render():
    fig, ax = make_fig()
    rng = np.random.RandomState(42)
    # Large arc representing Earth's limb near bottom of canvas
    earth_r = PW * 1.6  # smaller radius — more visible curvature
    earth_cx = cx
    earth_cy = PAD_B - earth_r + PH * 0.30

    theta_range = np.linspace(-0.38, 0.38, 1000)

    # --- 1. Primary atmosphere layers: distinct arcs with clear separation ---
    #     Inner: teal/green tones
    #     Core:  bright cyan/azure — brightest
    #     Upper: deeper cosmic/blue — fading out
    primary_layers = [
        # offset_frac,  color,   alpha, lw
        # Inner layers — TEAL greens, well separated
        (0.002, TEAL,   0.45, 1.2),
        (0.008, TEAL,   0.50, 1.4),
        (0.015, TEAL,   0.55, 1.6),
        (0.022, TEAL,   0.50, 1.4),
        # Core layers — bright CYAN / AZURE, prominent
        (0.030, CYAN,   0.65, 2.2),
        (0.038, AZURE,  0.75, 2.8),
        (0.044, CYAN,   0.80, 3.0),
        (0.050, AZURE,  0.75, 2.8),
        (0.056, CYAN,   0.65, 2.2),
        # Upper layers — deeper COSMIC / DEEP blue
        (0.064, COSMIC, 0.35, 1.4),
        (0.074, DEEP,   0.25, 1.0),
        (0.086, COSMIC, 0.15, 0.8),
        (0.100, DEEP,   0.08, 0.5),
    ]
    for off, col, alpha, lw in primary_layers:
        r_ = earth_r + PW * off
        xs = earth_cx + r_ * np.sin(theta_range)
        ys = earth_cy + r_ * np.cos(theta_range)
        mask = ((xs > PAD_L) & (xs < PAD_L + PW) &
                (ys > PAD_B) & (ys < PAD_B + PH))
        if mask.sum() < 3:
            continue
        for seg_xs, seg_ys in split_segments(xs, ys, mask):
            draw_lc(ax, seg_xs, seg_ys, col, lw=lw, alpha=alpha, zo=4)

    # --- 2. Subtle atmospheric glow lines (dimmed for line visibility) ---
    n_atm = 15
    glow_colors = [TEAL, CYAN, AZURE, COSMIC]
    for i in range(n_atm):
        r_atm = earth_r + PW * (0.001 + i / n_atm * 0.06)
        xs = earth_cx + r_atm * np.sin(theta_range)
        ys = earth_cy + r_atm * np.cos(theta_range)
        mask = ((xs > PAD_L) & (xs < PAD_L + PW) &
                (ys > PAD_B) & (ys < PAD_B + PH))
        if mask.sum() < 3:
            continue
        frac = i / n_atm
        alpha = 0.05 * (1 - frac * 0.8)
        # Color by position band
        if frac < 0.25:
            col = TEAL
        elif frac < 0.50:
            col = CYAN
        elif frac < 0.75:
            col = AZURE
        else:
            col = COSMIC
        for seg_xs, seg_ys in split_segments(xs, ys, mask):
            draw_lc(ax, seg_xs, seg_ys, col, lw=0.6, alpha=alpha, zo=3)

    # Earth surface (dark with subtle terrain)
    for theta in theta_range[::5]:
        sx = earth_cx + earth_r * np.sin(theta)
        sy = earth_cy + earth_r * np.cos(theta)
        if PAD_L < sx < PAD_L + PW and PAD_B < sy < PAD_B + PH:
            h = rng.uniform(0.002, 0.01)
            ax.plot([sx, sx], [sy - h, sy + h],
                    color=rgba(TEAL, 0.05), lw=0.3, zorder=2)

    # --- 3. Stars — ONLY above the earth arch ---
    # Helper: check if a point is above the earth's limb arc
    def is_above_arch(sx, sy, margin=0.15):
        """Return True if (sx,sy) is above the earth arc + margin."""
        # Distance from earth center
        dx = sx - earth_cx
        dy = sy - earth_cy
        dist = np.sqrt(dx**2 + dy**2)
        # The outermost atmosphere layer is at earth_r + PW*0.044
        # Add a margin so stars don't sit right on the arc
        return dist > earth_r + PW * 0.05 + margin

    # Tier 1: 500 background pinpoints (tiny dim stars)
    placed = 0
    attempts = 0
    while placed < 500 and attempts < 3000:
        attempts += 1
        sx = rng.uniform(PAD_L, PAD_L + PW)
        sy = rng.uniform(PAD_B, PAD_B + PH)
        if not is_above_arch(sx, sy, margin=0.1):
            continue
        sr = rng.uniform(0.004, 0.014)
        sa = rng.uniform(0.12, 0.45)
        ax.add_patch(Circle((sx, sy), radius=sr,
                    facecolor=rgba(STARLIGHT, sa),
                    edgecolor='none', zorder=5))
        placed += 1

    # Tier 2: 80 medium stars with varied colors
    tier2_colors = [STARLIGHT, IVORY, ICE, SILVER]
    placed = 0
    attempts = 0
    while placed < 80 and attempts < 1000:
        attempts += 1
        sx = rng.uniform(PAD_L, PAD_L + PW)
        sy = rng.uniform(PAD_B, PAD_B + PH)
        if not is_above_arch(sx, sy, margin=0.15):
            continue
        sr = rng.uniform(0.012, 0.030)
        sa = rng.uniform(0.30, 0.65)
        col = tier2_colors[rng.randint(len(tier2_colors))]
        ax.add_patch(Circle((sx, sy), radius=sr,
                    facecolor=rgba(col, sa),
                    edgecolor='none', zorder=6))
        placed += 1

    # Tier 3: 30 bright stars with colored glow halos
    tier3_colors = [GOLD, AMBER, CORONA, IVORY, ICE, CYAN, STARLIGHT]
    placed = 0
    attempts = 0
    while placed < 30 and attempts < 500:
        attempts += 1
        sx = rng.uniform(PAD_L, PAD_L + PW)
        sy = rng.uniform(PAD_B, PAD_B + PH)
        if not is_above_arch(sx, sy, margin=0.25):
            continue
        sr = rng.uniform(0.018, 0.040)
        col = tier3_colors[rng.randint(len(tier3_colors))]
        # Outer glow ring (2.5x) — subtle
        ax.add_patch(Circle((sx, sy), radius=sr * 2.5,
                    facecolor=rgba(col, 0.04),
                    edgecolor='none', zorder=5))
        # Inner glow ring (1.5x)
        ax.add_patch(Circle((sx, sy), radius=sr * 1.5,
                    facecolor=rgba(col, 0.10),
                    edgecolor='none', zorder=5))
        # Core
        ax.add_patch(Circle((sx, sy), radius=sr,
                    facecolor=rgba(col, 0.65),
                    edgecolor='none', zorder=7))
        placed += 1

    label(ax, "h/R\u2248\u2080.\u2080\u2031\u2036")
    save(fig, "awe_overview.pdf")


if __name__ == '__main__':
    render()
