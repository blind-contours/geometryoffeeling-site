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
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
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

# Palette: euphoric jewel tones
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

def draw_lc(ax, xs, ys, col_rgba, lw, zo=4):
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
    segments = []
    in_seg = False
    start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j; in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 5:
                segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 5:
        segments.append((xs[start:], ys[start:]))
    return segments

def _draw_petal(ax, xs, ys, color_hex, lw_peak, a_peak, zo,
                smooth_sigma=4, fade_power=0.5):
    """Draw a petal-shaped curve with bell-curve alpha envelope."""
    xs = gaussian_filter1d(np.array(xs, dtype=float), smooth_sigma)
    ys = gaussian_filter1d(np.array(ys, dtype=float), smooth_sigma)
    n = len(xs)
    if n < 5:
        return
    mask = ((xs > PAD_L + 0.05) & (xs < PAD_L + PW - 0.05) &
            (ys > PAD_B + 0.05) & (ys < PAD_B + PH - 0.05))
    if mask.sum() < 8:
        return

    segments = _split_masked(xs, ys, mask)
    rgb = hex_to_rgb(color_hex)

    for sx, sy in segments:
        n_s = len(sx)
        if n_s < 3:
            continue
        pts = np.array([sx, sy]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        colors = []
        widths = []
        for i in range(n_s - 1):
            frac = i / max(n_s - 2, 1)
            env = np.sin(np.pi * frac) ** fade_power
            a = a_peak * env
            w = max(lw_peak * (0.1 + 0.9 * env), 0.08)
            colors.append((rgb[0], rgb[1], rgb[2],
                           float(np.clip(a, 0, 1))))
            widths.append(w)
        lc = mc.LineCollection(
            segs, linewidths=widths, colors=colors,
            capstyle='round', joinstyle='round', zorder=zo)
        ax.add_collection(lc)

def _reflect_and_draw(ax, r, theta_base, col, lw, alpha, zo,
                      n_fold, sector, smooth, fade):
    """Reflect a single petal curve across all n_fold symmetry axes."""
    for k in range(n_fold):
        offset = k * sector
        for mirror in [1, -1]:
            theta = mirror * theta_base + offset
            xs = cx + r * np.cos(theta)
            ys = cy + r * np.sin(theta)
            _draw_petal(ax, xs, ys, col, lw, alpha, zo=zo,
                        smooth_sigma=smooth, fade_power=fade)

# ===============================================================================
# KALEIDOSCOPE — broken sine waves of euphoria radiating from center
# 12-fold symmetry mandala: layered petal forms with sine-wave modulation
# R_k(theta) = theta + 2*pi*k/n
# ===============================================================================
def render():
    fig, ax = make_fig()
    np.random.seed(42)

    n_fold = 12
    sector = 2 * np.pi / n_fold
    R_max = min(PW, PH) * 0.47

    t = np.linspace(0, 1, 800)
    envelope = np.sin(np.pi * t)  # petal shape: 0 -> 1 -> 0

    # -------------------------------------------------------------------
    # A) LUMINOUS CENTER GLOW — warm radiance anchoring the composition
    # -------------------------------------------------------------------
    glow = [
        (0.35, 0.008, DEEP_VIOLET),
        (0.28, 0.014, ULTRAVIOLET),
        (0.22, 0.025, MAGENTA_GLOW),
        (0.17, 0.040, ROSE_PINK),
        (0.12, 0.065, HOT_CORAL),
        (0.085, 0.100, SOLAR_ORANGE),
        (0.055, 0.180, GOLDEN),
        (0.035, 0.350, "#FFE8D8"),
        (0.018, 0.800, "#FFFAF6"),
    ]
    for rad_f, a, c in glow:
        ax.add_patch(Circle((cx, cy), radius=R_max * rad_f,
                     facecolor=rgba(c, a), edgecolor='none', zorder=7))

    # -------------------------------------------------------------------
    # B) MAIN PETAL LAYERS — 4 concentric rings of petals
    #
    #    Each petal: r(t) = R * envelope(t) * (1 + amp * sin(bumps*2pi*t))
    #                theta(t) = sector * t
    #
    #    Key: bumps=1 gives a single gentle undulation (one wider, one
    #    narrower lobe). bumps=2 gives a subtle figure-8. Low amplitudes
    #    keep the undulation graceful.
    # -------------------------------------------------------------------

    # Ring 1: INNER — intense, jewel-like
    inner_petals = [
        # (r_scale, bumps, amp, lw, alpha, color_idx, smooth, fade)
        (0.26, 1, 0.04, 2.6, 0.68, 0, 3, 0.5),   # rose pink
        (0.23, 2, 0.03, 2.3, 0.62, 1, 3, 0.5),   # deep violet
        (0.28, 1, 0.05, 2.4, 0.58, 2, 3, 0.5),   # vivid cyan
        (0.20, 1, 0.04, 2.0, 0.55, 4, 3, 0.5),   # magenta
    ]

    # Ring 2: MID-INNER — full-bodied
    mid_inner_petals = [
        (0.44, 1, 0.05, 2.2, 0.52, 6, 4, 0.45),  # ultraviolet
        (0.40, 2, 0.03, 2.0, 0.48, 8, 4, 0.45),  # electric blue
        (0.47, 1, 0.06, 1.8, 0.45, 3, 4, 0.45),  # solar orange
        (0.42, 1, 0.04, 1.9, 0.44, 5, 4, 0.45),  # emerald
    ]

    # Ring 3: MID-OUTER — elegant transition zone
    mid_outer_petals = [
        (0.62, 1, 0.04, 1.7, 0.38, 7, 5, 0.4),   # hot coral
        (0.58, 2, 0.03, 1.5, 0.34, 9, 5, 0.4),   # golden
        (0.65, 1, 0.05, 1.4, 0.32, 1, 5, 0.4),   # deep violet
        (0.60, 1, 0.04, 1.3, 0.30, 2, 5, 0.4),   # vivid cyan
    ]

    # Ring 4: OUTER — gossamer, dissolving into the background
    outer_petals = [
        (0.82, 1, 0.03, 1.2, 0.24, 0, 7, 0.35),  # rose (faint)
        (0.78, 1, 0.04, 1.0, 0.20, 4, 7, 0.35),  # magenta
        (0.86, 1, 0.03, 0.9, 0.18, 2, 8, 0.35),  # cyan
        (0.75, 1, 0.03, 0.8, 0.16, 5, 8, 0.35),  # emerald
    ]

    all_petals = [
        (inner_petals, 7),
        (mid_inner_petals, 6),
        (mid_outer_petals, 5),
        (outer_petals, 4),
    ]

    for petal_group, base_zo in all_petals:
        for (r_scale, bumps, amp, lw, alpha, ci, smooth, fade) in petal_group:
            col = PALETTE[ci % len(PALETTE)]

            r = R_max * r_scale * envelope * \
                (1 + amp * np.sin(bumps * 2 * np.pi * t))
            r = r + R_max * 0.02

            theta_base = sector * t

            _reflect_and_draw(ax, r, theta_base, col, lw, alpha, base_zo,
                              n_fold, sector, smooth, fade)

    # -------------------------------------------------------------------
    # C) SHIMMER THREADS — fine broken sine waves overlaying petals
    #    Creates the "euphoria breaking apart" texture
    # -------------------------------------------------------------------
    for s_idx in range(10):
        freq = 3 + s_idx * 2.5
        r_center = 0.20 + s_idx * 0.07

        r = R_max * r_center * envelope * \
            (1 + 0.01 * np.sin(freq * 2 * np.pi * t))
        r = r + R_max * 0.02

        theta_base = sector * t
        col = PALETTE[(s_idx * 3) % len(PALETTE)]

        _reflect_and_draw(ax, r, theta_base, col, 0.4, 0.12, 3,
                          n_fold, sector, 3, 0.3)

    # -------------------------------------------------------------------
    # D) OUTERMOST HALO — barely visible echoes
    # -------------------------------------------------------------------
    for h_idx in range(3):
        r_h = R_max * (0.92 + h_idx * 0.04) * envelope
        r_h = r_h + R_max * 0.02
        col_h = [ROSE_PINK, DEEP_VIOLET, VIVID_CYAN][h_idx]

        _reflect_and_draw(ax, r_h, sector * t, col_h, 0.7, 0.08, 2,
                          n_fold, sector, 10, 0.3)

    # -------------------------------------------------------------------
    # E) FAINT STRUCTURAL RINGS
    # -------------------------------------------------------------------
    theta_ring = np.linspace(0, 2 * np.pi, 1000)
    for rf, a, c, lw in [
        (0.90, 0.03, DEEP_VIOLET, 0.3),
        (0.68, 0.035, ROSE_PINK, 0.25),
        (0.48, 0.035, VIVID_CYAN, 0.25),
        (0.30, 0.04, GOLDEN, 0.2),
    ]:
        wobble = R_max * 0.003 * np.sin(n_fold * theta_ring)
        r_ring = R_max * rf + wobble
        xs_r = cx + r_ring * np.cos(theta_ring)
        ys_r = cy + r_ring * np.sin(theta_ring)
        mask = ((xs_r > PAD_L + 0.05) & (xs_r < PAD_L + PW - 0.05) &
                (ys_r > PAD_B + 0.05) & (ys_r < PAD_B + PH - 0.05))
        if mask.sum() > 10:
            segments = _split_masked(xs_r, ys_r, mask)
            for sx, sy in segments:
                draw_lc(ax, sx, sy, rgba(c, a), lw=lw, zo=2)

    add_signature(fig, ax, BG)
    save(fig, "euphoria_kaleidoscope.pdf")

if __name__ == '__main__':
    render()
