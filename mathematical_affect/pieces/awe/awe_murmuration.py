"""
Geometry of Feeling — Awe: Awe Murmuration
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
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


# ============================================================================
# 5. MURMURATION — emergent swarm patterns (flowing swooping form)
#    One smooth swooping function that all trails follow coherently.
#    The spine undulates like a river of birds — all lines move together
#    as one flock with gentle vertical offsets.
# ============================================================================

def _swooping_spine(x):
    """Single smooth swooping function for the murmuration shape.

    Blended from v2/v4/v5 — wide organic swoop with gentle undulation.
    Shallow nadir keeps the flock well within frame.
    Input x in [0, 1], output y offset from center.
    """
    # Gentle cosine arch
    y = 0.15 * np.cos(np.pi * x)
    # Slight linear tilt
    y += 0.12 * x
    # Shallow, wide nadir — stays well above bottom border
    y -= 0.28 * np.exp(-((x - 0.44) ** 2) / (2 * 0.14 ** 2))
    # Secondary undulation for organic double-swoop feel
    y += 0.12 * np.sin(1.8 * np.pi * x + 0.4)
    # Tertiary ripple
    y += 0.05 * np.sin(3.3 * np.pi * x - 0.3)
    # Subtle high-frequency for liveliness
    y += 0.02 * np.sin(6.5 * np.pi * x + 0.8)
    return y

def render():
    fig, ax = make_fig()
    np.random.seed(42)
    rng = np.random.default_rng(42)

    # --- Build the flowing spine ---
    n_spine = 1000
    # X spans the full width with padding
    x_start = PAD_L + PW * 0.02
    x_end = PAD_L + PW * 0.98
    spine_x = np.linspace(x_start, x_end, n_spine)

    # Normalize x to [0, 1] for the swooping function
    x_norm = (spine_x - x_start) / (x_end - x_start)

    # Y from swooping function, centered in upper portion
    y_center = PAD_B + PH * 0.50
    spine_y = y_center + PH * _swooping_spine(x_norm)

    # Smooth the spine
    spine_y = gaussian_filter1d(spine_y, sigma=4.0)

    # --- Nadir position for coloring ---
    nadir_idx = np.argmin(spine_y)
    nadir_y = spine_y[nadir_idx]
    nadir_x = spine_x[nadir_idx]

    # --- Helper to draw one trail ---
    def _draw_trail(trail_x, trail_y, col, alpha, lw):
        mask = ((trail_x > 0.15) & (trail_x < FIG_W - 0.15) &
                (trail_y > 0.15) & (trail_y < FIG_H - 0.15))
        if mask.sum() < 4:
            return
        for seg_xs, seg_ys in split_segments(trail_x, trail_y, mask):
            seg_len = len(seg_xs)
            if seg_len < 3:
                continue
            pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            n_seg = len(segs)
            seg_taper = np.ones(n_seg)
            seg_fade = max(1, int(n_seg * 0.15))
            if seg_fade > 1:
                seg_taper[:seg_fade] = np.linspace(0.15, 1.0, seg_fade)
                seg_taper[-seg_fade:] = np.linspace(1.0, 0.15, seg_fade)
            colors = [rgba(col, float(alpha * seg_taper[j])) for j in range(n_seg)]
            lc = mc.LineCollection(segs, linewidths=lw, colors=colors,
                                   capstyle='round', joinstyle='round', zorder=3)
            ax.add_collection(lc)

    # --- Generate coherent murmuration trails ---
    # All trails follow the SAME spine function with slight vertical offsets.
    # Mix of long trails (for coherence) and shorter trails (for texture).
    n_birds = 1800
    n_trail_pts = 280

    # Nadir t-parameter (normalized position along spine)
    nadir_t = nadir_idx / (n_spine - 1)

    for b in range(n_birds):
        # --- Vertical offset: birds offset from the spine ---
        # Wider normal distribution for more visible individual lines
        y_offset = rng.normal(0, PH * 0.10)
        y_offset = np.clip(y_offset, -PH * 0.35, PH * 0.35)

        # --- Trail span ---
        r = rng.random()
        if r < 0.35:
            trail_frac = rng.uniform(0.55, 1.0)
        elif r < 0.70:
            trail_frac = rng.uniform(0.28, 0.55)
        else:
            trail_frac = rng.uniform(0.12, 0.30)

        max_start = 1.0 - trail_frac
        t_start = rng.uniform(0.0, max_start)
        t_end = t_start + trail_frac

        # Sample spine at this range
        ts = np.linspace(t_start, t_end, n_trail_pts)
        idxs = (ts * (n_spine - 1)).astype(int)
        idxs = np.clip(idxs, 0, n_spine - 1)

        trail_x = spine_x[idxs].copy()
        trail_y = spine_y[idxs].copy() + y_offset

        # --- Per-bird waviness for organic feel ---
        wave_t = np.linspace(0, 1, n_trail_pts)

        # Y waviness
        phase = rng.uniform(0, 2 * np.pi)
        freq = rng.uniform(1.0, 3.5)
        amp = rng.uniform(0.005, 0.020) * PH
        trail_y += amp * np.sin(freq * wave_t * 2 * np.pi + phase)

        # X waviness
        phase_x = rng.uniform(0, 2 * np.pi)
        trail_x += rng.uniform(0.001, 0.006) * PW * np.sin(
            rng.uniform(1.0, 2.5) * wave_t * 2 * np.pi + phase_x)

        # Smooth the trail
        trail_x = gaussian_filter1d(trail_x, sigma=3.0)
        trail_y = gaussian_filter1d(trail_y, sigma=3.0)

        # --- Coloring based on distance from spine center ---
        abs_offset = abs(y_offset) / (PH * 0.10)

        if abs_offset < 0.40:
            col = IVORY
        elif abs_offset < 0.75:
            col = SILVER
        elif abs_offset < 1.2:
            col = ICE
        elif abs_offset < 1.8:
            col = AZURE
        else:
            col = DEEP

        # Base alpha and linewidth — slightly reduced for individual line visibility
        alpha = rng.uniform(0.05, 0.20)
        lw = rng.uniform(0.12, 0.38)

        # Outer birds progressively fainter
        if abs_offset > 1.4:
            alpha *= 0.40
            lw *= 0.50
        elif abs_offset > 1.0:
            alpha *= 0.60
            lw *= 0.65

        _draw_trail(trail_x, trail_y, col, alpha, lw)

    # --- Violet nadir accent trails ---
    # Dedicated short trails concentrated at the nadir for the violet glow
    n_nadir = 300
    for b in range(n_nadir):
        y_offset = rng.normal(0, PH * 0.06)
        y_offset = np.clip(y_offset, -PH * 0.18, PH * 0.18)

        trail_frac = rng.uniform(0.08, 0.22)
        # Center around nadir
        center = nadir_t + rng.normal(0, 0.03)
        t_start = max(0, center - trail_frac / 2)
        t_end = min(1.0, t_start + trail_frac)

        ts = np.linspace(t_start, t_end, n_trail_pts)
        idxs = (ts * (n_spine - 1)).astype(int)
        idxs = np.clip(idxs, 0, n_spine - 1)

        trail_x = spine_x[idxs].copy()
        trail_y = spine_y[idxs].copy() + y_offset

        wave_t = np.linspace(0, 1, n_trail_pts)
        phase = rng.uniform(0, 2 * np.pi)
        trail_y += rng.uniform(0.003, 0.012) * PH * np.sin(
            rng.uniform(1.0, 3.0) * wave_t * 2 * np.pi + phase)

        trail_x = gaussian_filter1d(trail_x, sigma=3.0)
        trail_y = gaussian_filter1d(trail_y, sigma=3.0)

        abs_off = abs(y_offset) / (PH * 0.10)
        if abs_off < 0.3:
            col = ULTRAVIOLET
        elif abs_off < 0.6:
            col = NEBULA_P
        else:
            col = COSMIC

        alpha = rng.uniform(0.05, 0.18)
        lw = rng.uniform(0.12, 0.32)

        _draw_trail(trail_x, trail_y, col, alpha, lw)

    label(ax, "v_i=\u03b1\u00b7align+\u03b2\u00b7cohere+\u03b3\u00b7separate")
    save(fig, "awe_murmuration.pdf")


if __name__ == '__main__':
    render()
