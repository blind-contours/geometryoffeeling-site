"""
Geometry of Feeling — Euphoria: Euphoria Kaleidoscope
Standalone render script
"""

"""
Geometry of Feeling — Euphoria (Final Series)
Five pieces: Kaleidoscope, Stained Glass, Prismatic, Crown, Firework

Mathematical primitives: symmetric reflection, Voronoi tessellation,
spectral divergence, epicycloid rotation, radial ballistic burst

Aesthetic: Matisse at maximum saturation, Rothko's brightest works,
stained glass in full sun — oversaturated, almost painful vividness

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle
from scipy.ndimage import gaussian_filter1d
import os

DPI = 300
FIG_W = 12
FIG_H = 8
BG = "#FEFCF8"

# Palette: euphoric jewel tones — vivid, warm-cool alternation
ROSE_PINK    = "#E8308C"
DEEP_VIOLET  = "#8818E8"
VIVID_CYAN   = "#00B8D8"
SOLAR_ORANGE = "#F08020"
MAGENTA_GLOW = "#D020A8"
EMERALD      = "#18C870"
ULTRAVIOLET  = "#6010E0"
HOT_CORAL    = "#F05068"
ELECTRIC_BLUE = "#2888F0"
GOLDEN       = "#E8B010"

PALETTE = [ROSE_PINK, DEEP_VIOLET, VIVID_CYAN, SOLAR_ORANGE, MAGENTA_GLOW,
           EMERALD, ULTRAVIOLET, HOT_CORAL, ELECTRIC_BLUE, GOLDEN]


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))


def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))


def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R
PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2
cy = PAD_B + PH / 2


def label(ax, eq):
    ax.text(0.75, 0.75, eq, fontfamily='monospace', fontsize=10,
            color=(0.35, 0.20, 0.40, 0.22), transform=ax.transData)


def draw_gradient_line(ax, xs, ys, color_hex, lw_start, lw_end,
                       alpha_start, alpha_end, zo=4, smooth=0):
    """Draw a line with gradually changing width and alpha."""
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
        xs = gaussian_filter1d(xs, smooth)
    n = len(xs)
    if n < 3:
        return
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    r, g, b = hex_to_rgb(color_hex)
    colors = []
    widths = []
    for i in range(n - 1):
        frac = i / max(n - 2, 1)
        a = alpha_start + (alpha_end - alpha_start) * frac
        w = lw_start + (lw_end - lw_start) * frac
        colors.append((r, g, b, float(np.clip(a, 0, 1))))
        widths.append(w)
    lc = mc.LineCollection(segs, linewidths=widths, colors=colors,
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)


def draw_lc(ax, xs, ys, col_rgba, lw, zo=4):
    """Simple uniform line collection."""
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[col_rgba],
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


def _split_masked(xs, ys, mask):
    """Split arrays into contiguous segments where mask is True."""
    segments = []
    in_seg = False
    start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j
            in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 5:
                segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 5:
        segments.append((xs[start:], ys[start:]))
    return segments


def _draw_in_frame(ax, xs, ys, color_hex, lw_s, lw_e, a_s, a_e, zo,
                   smooth=0):
    """Clip to frame boundaries and draw gradient line segments."""
    mask = ((xs > PAD_L + 0.05) & (xs < PAD_L + PW - 0.05) &
            (ys > PAD_B + 0.05) & (ys < PAD_B + PH - 0.05))
    if mask.sum() < 8:
        return
    segments = _split_masked(xs, ys, mask)
    for sx, sy in segments:
        draw_gradient_line(ax, sx, sy, color_hex,
                           lw_s, lw_e, a_s, a_e, zo=zo, smooth=smooth)


# ===============================================================================
# KALEIDOSCOPE — broken sine waves of euphoria radiating from center
# 12-fold symmetry mandala: organic petal forms with sine-wave edges
# R_k(theta) = theta + 2*pi*k/n
# ===============================================================================
def render():
    fig, ax = make_fig()
    np.random.seed(42)

    n_fold = 12
    sector = 2 * np.pi / n_fold
    R_max = min(PW, PH) * 0.47

    # -------------------------------------------------------------------
    # A) LUMINOUS CENTER — layered soft glow
    # -------------------------------------------------------------------
    glow_specs = [
        (0.22, 0.025, DEEP_VIOLET),
        (0.17, 0.04,  MAGENTA_GLOW),
        (0.13, 0.06,  ROSE_PINK),
        (0.09, 0.10,  SOLAR_ORANGE),
        (0.06, 0.18,  GOLDEN),
        (0.035, 0.40, HOT_CORAL),
        (0.018, 0.80, "#FFF4EC"),
    ]
    for rad_f, a, c in glow_specs:
        ax.add_patch(Circle((cx, cy), radius=R_max * rad_f,
                     facecolor=rgba(c, a), edgecolor='none', zorder=7))

    # -------------------------------------------------------------------
    # B) PETAL CURVES — the soul of the mandala
    #
    #    Each petal is a parametric curve where:
    #      r(t) = envelope(t) * (1 + sine_modulation(t))
    #      theta(t) = sweep across the sector
    #
    #    The envelope rises from 0, peaks at mid-sector, falls back —
    #    creating a teardrop/petal shape. The sine modulation adds the
    #    broken, joyful wobble that makes it feel alive.
    # -------------------------------------------------------------------

    t = np.linspace(0, 1, 700)

    # Petal envelope: a smooth rise-and-fall
    # Using sin(pi*t) gives a nice teardrop when mapped to r vs theta
    envelope = np.sin(np.pi * t)  # 0 -> 1 -> 0

    petal_defs = [
        # (r_max_f, n_sine_bumps, bump_amp, lw, a_peak, color_idx, r_offset)
        # Large outer petals
        (0.92, 5,  0.08, 2.4, 0.65, 0, 0.05),
        (0.85, 7,  0.06, 2.0, 0.55, 1, 0.06),
        (0.88, 4,  0.10, 2.2, 0.50, 2, 0.04),
        # Mid petals
        (0.65, 6,  0.07, 1.8, 0.55, 3, 0.08),
        (0.60, 8,  0.05, 1.6, 0.50, 4, 0.07),
        (0.70, 3,  0.09, 2.0, 0.45, 5, 0.06),
        # Inner petals — vivid and bold
        (0.42, 5,  0.06, 2.5, 0.70, 6, 0.05),
        (0.38, 7,  0.04, 2.2, 0.65, 7, 0.06),
        (0.45, 4,  0.08, 2.8, 0.60, 8, 0.04),
        # Tiny inner accents
        (0.22, 6,  0.03, 2.0, 0.75, 9, 0.04),
        (0.25, 4,  0.05, 1.8, 0.70, 0, 0.03),
    ]

    for (r_max_f, n_bumps, bump_amp, lw, a_peak, ci, r_off) in petal_defs:

        col = PALETTE[ci % len(PALETTE)]

        # Radius: petal envelope modulated by sine bumps
        r = R_max * (r_off + r_max_f * envelope *
                     (1 + bump_amp * np.sin(n_bumps * 2 * np.pi * t)))

        # Theta: sweeps smoothly across the sector
        # Using a parabolic path so it slows at the edges (more organic)
        theta_base = sector * t

        # Alpha fades at the edges of the petal
        alpha_envelope = envelope ** 0.4  # sharper than pure sine

        for k in range(n_fold):
            offset = k * sector
            for mirror in [1, -1]:
                theta = mirror * theta_base + offset
                xs = cx + r * np.cos(theta)
                ys = cy + r * np.sin(theta)

                # Per-point alpha based on envelope
                mask = ((xs > PAD_L + 0.05) & (xs < PAD_L + PW - 0.05) &
                        (ys > PAD_B + 0.05) & (ys < PAD_B + PH - 0.05))
                if mask.sum() < 8:
                    continue

                segments = _split_masked(xs, ys, mask)
                for sx, sy in segments:
                    n_s = len(sx)
                    pts = np.array([sx, sy]).T.reshape(-1, 1, 2)
                    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
                    rgb = hex_to_rgb(col)
                    colors = []
                    widths = []
                    for i in range(n_s - 1):
                        frac = i / max(n_s - 2, 1)
                        # Map frac back to approximate t position
                        env_val = np.sin(np.pi * frac) ** 0.4
                        a = a_peak * env_val
                        w = lw * (0.3 + 0.7 * env_val)
                        colors.append((rgb[0], rgb[1], rgb[2],
                                       float(np.clip(a, 0, 1))))
                        widths.append(w)
                    lc = mc.LineCollection(
                        segs, linewidths=widths, colors=colors,
                        capstyle='round', joinstyle='round',
                        zorder=4)
                    ax.add_collection(lc)

    # -------------------------------------------------------------------
    # C) RADIAL SPINES — thin lines from center outward along each axis
    #    These give the mandala geometric structure and crispness
    # -------------------------------------------------------------------
    t_spine = np.linspace(0, 1, 400)
    for k in range(n_fold):
        angle = k * sector
        # Subtle sine wobble on the spine
        r_spine = R_max * 0.95 * t_spine
        wobble = R_max * 0.005 * np.sin(8 * np.pi * t_spine)
        xs_s = cx + (r_spine + wobble) * np.cos(angle)
        ys_s = cy + (r_spine + wobble) * np.sin(angle)

        # Alternate colors on spines
        spine_col = PALETTE[(k * 2) % len(PALETTE)]
        _draw_in_frame(ax, xs_s, ys_s, spine_col,
                       1.2, 0.2, 0.30, 0.04, zo=5, smooth=1)

    # -------------------------------------------------------------------
    # D) CONCENTRIC ACCENT RINGS — faint circles with 12-fold wobble
    # -------------------------------------------------------------------
    theta_ring = np.linspace(0, 2 * np.pi, 1000)
    for rf, a, c, lw in [
        (0.95, 0.05, DEEP_VIOLET, 0.5),
        (0.78, 0.06, ROSE_PINK, 0.4),
        (0.60, 0.05, VIVID_CYAN, 0.4),
        (0.42, 0.06, SOLAR_ORANGE, 0.3),
        (0.25, 0.07, MAGENTA_GLOW, 0.3),
    ]:
        wobble = R_max * 0.008 * np.sin(n_fold * theta_ring)
        r_ring = R_max * rf + wobble
        xs_r = cx + r_ring * np.cos(theta_ring)
        ys_r = cy + r_ring * np.sin(theta_ring)
        mask = ((xs_r > PAD_L + 0.05) & (xs_r < PAD_L + PW - 0.05) &
                (ys_r > PAD_B + 0.05) & (ys_r < PAD_B + PH - 0.05))
        if mask.sum() > 10:
            segments = _split_masked(xs_r, ys_r, mask)
            for sx, sy in segments:
                draw_lc(ax, sx, sy, rgba(c, a), lw=lw, zo=2)

    # -------------------------------------------------------------------
    # E) OUTER FILIGREE — very fine high-frequency petals at the edge
    #    Adds ethereal complexity without muddying the core
    # -------------------------------------------------------------------
    for f_idx in range(5):
        freq_f = 10 + f_idx * 3
        r_f = R_max * (0.60 + 0.35 * envelope *
                       (1 + 0.03 * np.sin(freq_f * 2 * np.pi * t)))
        theta_f = sector * t
        col_f = PALETTE[(f_idx * 2 + 3) % len(PALETTE)]

        for k in range(n_fold):
            offset = k * sector
            for mirror in [1, -1]:
                theta = mirror * theta_f + offset
                xs = cx + r_f * np.cos(theta)
                ys = cy + r_f * np.sin(theta)
                _draw_in_frame(ax, xs, ys, col_f,
                               0.4, 0.1, 0.12, 0.03, zo=3)

    label(ax, "R_k(\u03b8)=\u03b8+2\u03c0k/n")
    save(fig, "euphoria_kaleidoscope.pdf")


if __name__ == '__main__':
    render()
