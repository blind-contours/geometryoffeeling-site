"""
Geometry of Feeling — Melancholy: Melancholy Elegy
Standalone render script
"""

"""
Geometry of Feeling -- Melancholy (Final Series)
Five pieces: Elegy, Lethe, Dissolve, Drift, Entropy

Melancholy is heavy, slow, quiet -- but not boring. These five pieces
achieve stillness through complexity: many layers all barely moving,
structure that is present but dimming, the weight of things slowly sinking.

Palette: slate blue, grey-mauve, faded green. Cool mid-grey background.
Mathematical primitives: slowly decaying curves, random walk with
downward drift, order dissolving into noise, forgetting, echoes fading.

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os


DPI=300; FIG_W=12; FIG_H=8
BG="#DDD9D2"  # warm parchment

# Palette: muted melancholic blues and greys on warm parchment
DUSTY_BLUE="#4A5A7A"
SLATE="#6A7A8A"
MAUVE="#7A6A8A"
DEEP_BLUE="#3A4A6A"
PALE_SLATE="#8A96A4"
MIST="#A0AABA"
DUSTY_ROSE="#8A6A72"
FADED_INK="#5A5A6A"
WARM_GREY="#7A7A78"

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
cx=PAD_L+PW/2; cy=FIG_H/2  # true vertical center; two-pass centering in render()

def label(ax,eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.15,0.15,0.20,0.28),transform=ax.transData)

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
# 1. ELEGY -- "Last Note Held"
#    y(t) = A * e^(-lambda*t) * sin(omega*t + phi)
#    A series of damped sinusoids: rich harmonics on the left, fading
#    into silence on the right. Like a single sustained note dissolving.
# =============================================================================
def _generate_curves(rng, t, convergence, center_y):
    """Generate all curve data (harmonics + voices) relative to center_y.
    Returns list of (ys_array, col, alpha_start, lw_start, lam, tail_fade_start, zorder) tuples."""
    curves = []
    n_points = len(t)

    n_harmonics = 26
    color_pool = [
        DUSTY_BLUE, DEEP_BLUE, SLATE, MAUVE,
        DUSTY_BLUE, SLATE, PALE_SLATE,
        DEEP_BLUE, FADED_INK, MAUVE,
        MIST, SLATE, WARM_GREY,
        DUSTY_ROSE, PALE_SLATE, FADED_INK,
        DUSTY_BLUE, DEEP_BLUE,
    ]

    for i in range(n_harmonics):
        harmonic_rank = i / (n_harmonics - 1)
        base_freq = 1.2 + harmonic_rank * 12.8
        freq = base_freq * (1.0 + rng.uniform(-0.10, 0.10))
        omega = 2 * np.pi * freq
        phi = rng.uniform(0, 2 * np.pi)
        max_spread = PH * 0.38
        amp_base = max_spread * (1.0 - 0.65 * harmonic_rank)
        amp_base *= rng.uniform(0.55, 1.0)
        y_offset = PH * 0.02 * rng.uniform(-1, 1)
        lam = 1.8 + harmonic_rank * 5.0
        lam *= rng.uniform(0.80, 1.20)

        envelope = amp_base * np.exp(-lam * t) * convergence
        ys_clean = center_y + y_offset * convergence + envelope * np.sin(omega * t + phi)
        wobble_amp = 0.02 * amp_base * np.exp(-lam * t * 0.4) * convergence
        wobble = wobble_amp * gaussian_filter1d(rng.randn(n_points), sigma=50)
        ys = ys_clean + wobble

        alpha_start = 0.12 + 0.48 * (1.0 - harmonic_rank)
        lw_start = 0.35 + 1.9 * (1.0 - harmonic_rank)
        col = color_pool[i % len(color_pool)]
        curves.append((ys, col, alpha_start, lw_start, lam, 0.70, 3 + i))

    # Primary voice lines
    for voice_i, (v_freq, v_phi, v_col, v_amp_mult, v_lam, v_alpha) in enumerate([
        (2.0, 0.4, DUSTY_BLUE, 1.0, 1.0, 0.55),
        (3.1, 1.9, DEEP_BLUE, 0.72, 1.4, 0.42),
        (1.3, 4.0, DUSTY_ROSE, 0.48, 1.7, 0.32),
    ]):
        omega_v = 2 * np.pi * v_freq
        amp_v = PH * 0.30 * v_amp_mult
        envelope_v = amp_v * np.exp(-v_lam * t) * convergence
        ys_v = center_y + envelope_v * np.sin(omega_v * t + v_phi)
        wobble_v = 0.006 * amp_v * np.exp(-v_lam * t * 0.4) * convergence
        wobble_v = wobble_v * gaussian_filter1d(rng.randn(n_points), sigma=70)
        ys_v = ys_v + wobble_v

        lw_start_v = 1.6 + 1.2 * v_amp_mult
        curves.append((ys_v, v_col, v_alpha, lw_start_v, v_lam, 0.72, 40 + voice_i))

    return curves


def render():
    fig, ax = make_fig()
    rng = np.random.RandomState(42)

    n_points = 5000
    t = np.linspace(0, 1, n_points)
    # x spans left ~85% of printable area, leaving intentional silence on right
    x_start = PAD_L + PW * 0.03
    x_end = PAD_L + PW * 0.88
    xs = x_start + (x_end - x_start) * t

    # Vertical convergence: lines spread wide on the left, converge to cy on right
    convergence = np.exp(-2.5 * t)

    # --- Two-pass centering ---
    # Pass 1: generate curves at cy=0 to find vertical bounding box
    rng_copy = np.random.RandomState(42)
    curves_probe = _generate_curves(rng_copy, t, convergence, center_y=0.0)
    # Find the vertical midpoint of the bounding box (weighted toward the left
    # where visual mass is greatest -- use first 30% of points)
    left_slice = slice(0, n_points // 3)
    all_ys_left = np.concatenate([c[0][left_slice] for c in curves_probe])
    y_mid_bbox = (all_ys_left.max() + all_ys_left.min()) / 2.0
    # The actual center_y should place this midpoint at canvas center
    center_y = cy - y_mid_bbox

    # Pass 2: generate final curves with corrected center
    curves = _generate_curves(rng, t, convergence, center_y=center_y)

    # --- Draw all curves ---
    for curve_data in curves:
        ys, col, alpha_start, lw_start, lam, tail_fade_start, zo = curve_data

        # Determine chunk size based on whether this is a voice or harmonic
        is_voice = zo >= 40
        chunk_size = 28 if is_voice else 35
        lw_decay_rate = 0.45 if is_voice else 0.55

        n_chunks = n_points // chunk_size
        for c_idx in range(n_chunks):
            s = c_idx * chunk_size
            e = min(s + chunk_size + 1, n_points)
            if e - s < 3:
                continue

            t_mid = t[s + (e - s) // 2]
            a_val = alpha_start * np.exp(-lam * t_mid)
            if t_mid > tail_fade_start:
                a_val *= max(0, 1.0 - (t_mid - tail_fade_start) / (1.0 - tail_fade_start))

            if a_val < 0.006:
                break

            lw_val = lw_start * np.exp(-lam * t_mid * lw_decay_rate)
            lw_val = max(lw_val, 0.08 if not is_voice else 0.12)

            xs_chunk = xs[s:e]
            ys_chunk = ys[s:e]

            pts = np.array([xs_chunk, ys_chunk]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            lc = mc.LineCollection(
                segs, linewidths=lw_val,
                colors=[rgba(col, a_val)],
                capstyle='round', joinstyle='round', zorder=zo
            )
            ax.add_collection(lc)

    label(ax, "y(t)=Ae^(\u2212\u03bbt)\u00b7sin(\u03c9t+\u03c6)")
    save(fig, "melancholy_elegy")


if __name__ == '__main__':
    render()
