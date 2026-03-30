"""
Geometry of Feeling -- Envy: Envy Shadow
Reconceived as "Parasitic Resonance" (variant):
Two coupled spiral-orbit bodies in vertical composition.
Top body (the envied): warm gold/chartreuse, dense concentric spirals.
Bottom body (the envier): same curves stretched downward, desaturated grey-olive,
thinner lines -- overextending to match what it covets.
Transfer filaments drip downward like gravitational drainage.
"""
import os
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#DDD9D2'

# --- Palettes ---
# Envied body: warm golds and chartreuse
ENVIED_COLORS = ['#8A9A30', '#A0AA40', '#70882A', '#96A438', '#7E9228']
# Envier body: grey-olive, desaturated
ENVIER_COLORS = ['#7A7A68', '#8A8A78', '#6A6A58', '#757568', '#808070']

def hex_to_rgba(h, a):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return (r, g, b, float(np.clip(a, 0, 1)))

def render():
    np.random.seed(42)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # --- Harmonic definition for coupled oscillator bodies ---
    # Each body is built from a sum of harmonics: r(theta) = sum A_k * cos(n_k * theta + phi_k)
    n_harmonics = 7
    harmonic_n = np.array([1, 2, 3, 5, 7, 11, 13])
    harmonic_A = np.array([0.10, 0.06, 0.045, 0.03, 0.02, 0.012, 0.008])
    harmonic_phi = np.array([0.0, 0.8, 1.6, 2.4, 0.5, 3.1, 1.9])

    n_points = 1200
    theta = np.linspace(0, 2 * np.pi, n_points)

    # --- Envied body (top, warm gold, dense) ---
    envied_cx, envied_cy = 0.50, 0.72
    n_envied_lines = 30

    for i in range(n_envied_lines):
        t_frac = i / (n_envied_lines - 1)
        # Concentric spirals with slight radial growth per orbit
        base_r = 0.04 + 0.14 * t_frac
        # Phase offset per orbit for spiral effect
        phase_shift = i * 0.21

        r = np.ones_like(theta) * base_r
        for k in range(n_harmonics):
            # Amplitude decays slightly for outer orbits to keep density
            amp = harmonic_A[k] * (1.0 - 0.3 * t_frac)
            r += amp * np.cos(harmonic_n[k] * theta + harmonic_phi[k] + phase_shift)

        # Compact: no stretch, keep circular
        x = envied_cx + r * np.cos(theta)
        y = envied_cy + r * np.sin(theta)

        # Line properties: full weight, higher alpha for inner
        lw = 1.2 - 0.4 * t_frac
        alpha = 0.65 - 0.25 * t_frac
        col = ENVIED_COLORS[i % len(ENVIED_COLORS)]

        ax.plot(x, y, color=hex_to_rgba(col, alpha), lw=lw,
                solid_capstyle="round", zorder=5)

    # --- Envier body (bottom, grey-olive, stretched downward) ---
    envier_cx, envier_cy = 0.50, 0.38
    n_envier_lines = 32

    for i in range(n_envier_lines):
        t_frac = i / (n_envier_lines - 1)
        # Same harmonic structure but wider base -- overextending
        base_r = 0.05 + 0.18 * t_frac
        phase_shift = i * 0.21

        r = np.ones_like(theta) * base_r
        for k in range(n_harmonics):
            # Faster radial decay: harmonics die off more at outer orbits
            amp = harmonic_A[k] * (1.0 - 0.55 * t_frac)
            r += amp * np.cos(harmonic_n[k] * theta + harmonic_phi[k] + phase_shift)

        x = envier_cx + r * np.cos(theta)
        # Vertical stretch downward: the bottom of each orbit sags
        # Gravity-like asymmetry: stretches more in -y direction
        stretch_down = 1.0 + 0.35 * t_frac  # grows with orbit number
        y_raw = r * np.sin(theta)
        # Apply asymmetric stretch: only stretch the bottom half
        y_stretched = np.where(y_raw < 0, y_raw * stretch_down, y_raw * 0.85)
        y = envier_cy + y_stretched

        # Thinner lines, lower alpha -- hollower feel
        lw = 0.85 - 0.3 * t_frac
        alpha = 0.50 - 0.22 * t_frac
        col = ENVIER_COLORS[i % len(ENVIER_COLORS)]

        ax.plot(x, y, color=hex_to_rgba(col, alpha), lw=lw,
                solid_capstyle="round", zorder=4)

    # --- Transfer filaments: parabolic arcs dripping downward ---
    n_filaments = 12
    filament_angles = np.linspace(-0.55 * np.pi, 0.55 * np.pi, n_filaments)

    # Source points on the bottom of the envied body
    envied_bottom_r = 0.04 + 0.14 * 0.5  # mid-orbit radius
    # Target points on the top of the envier body
    envier_top_r = 0.05 + 0.18 * 0.5

    for j, fa in enumerate(filament_angles):
        # Source point: bottom edge of envied body
        src_x = envied_cx + envied_bottom_r * 0.9 * np.cos(fa)
        src_y = envied_cy - envied_bottom_r * 0.7

        # Target point: top edge of envier body
        dst_x = envier_cx + envier_top_r * 1.15 * np.cos(fa)
        dst_y = envier_cy + envier_top_r * 0.6

        # Parabolic drip path
        n_fil_pts = 80
        t_fil = np.linspace(0, 1, n_fil_pts)

        # x interpolation with slight lateral drift
        lateral_drift = 0.03 * np.sin(np.pi * t_fil) * np.cos(fa + j * 0.5)
        fx = src_x + (dst_x - src_x) * t_fil + lateral_drift

        # y follows a parabolic (gravitational) arc: faster at the end
        # Dripping effect: slow departure, accelerating fall
        fy = src_y + (dst_y - src_y) * (t_fil ** 1.6)

        # Color gradient: gold at top fading to grey at bottom
        for seg in range(n_fil_pts - 1):
            seg_frac = seg / (n_fil_pts - 1)
            # Interpolate from gold to grey-olive
            r_start, g_start, b_start = 0.54, 0.60, 0.19  # ~#8A9A30
            r_end, g_end, b_end = 0.48, 0.48, 0.41        # ~#7A7A68
            rc = r_start + (r_end - r_start) * seg_frac
            gc = g_start + (g_end - g_start) * seg_frac
            bc = b_start + (b_end - b_start) * seg_frac

            # Alpha: fade at endpoints, stronger in middle
            a_fil = 0.30 * np.sin(np.pi * seg_frac) ** 0.6
            # Thinner filaments near edges
            edge_dist = min(j, n_filaments - 1 - j) / (n_filaments / 2)
            lw_fil = 0.5 + 0.5 * edge_dist

            ax.plot(fx[seg:seg+2], fy[seg:seg+2],
                    color=(rc, gc, bc, a_fil), lw=lw_fil,
                    solid_capstyle="round", zorder=3)

    # --- Save ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "envy_shadow.pdf")
    add_signature(fig, ax, BG_COLOR)
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    render()
