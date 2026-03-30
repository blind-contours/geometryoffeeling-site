"""
Geometry of Feeling — Melancholy: Melancholy Entropy
"Sagging Lattice" — an Agnes Martin-like grid dissolving under gravity.

A pristine grid at the top of the canvas progressively sags downward:
horizontal lines droop into catenary curves, vertical lines buckle and lean,
intersections dissolve. Ghost echoes mark where the original grid would have been.
The beauty of order yielding to entropy.

Catenary deformation: y_deformed(x) = y_original - a·cosh((x - x_center)/a) + a
Dissolution probability: P(break) = 1 - exp(-k · depth)
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

def render():
    rng = np.random.RandomState(42)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Grid parameters (normalized 0-1 coordinates)
    margin_l, margin_r = 0.06, 0.06
    margin_b, margin_t = 0.08, 0.06

    n_hlines = 28       # horizontal lines
    n_vlines = 38        # vertical lines (more for 3:2 aspect)

    x_positions = np.linspace(margin_l, 1 - margin_r, n_vlines)
    y_positions = np.linspace(margin_b, 1 - margin_t, n_hlines)

    x_center = 0.5      # center of catenary sag

    # Resolution for drawing curves
    n_pts = 800

    # --- Color palette by depth ---
    # depth = 0 (top) -> 1 (bottom)
    # Top: cool grey-blue; Middle: grey-mauve; Bottom: dusty rose/mauve
    def color_for_depth(depth):
        """Return (r, g, b) based on depth 0=top, 1=bottom."""
        # Anchor colors
        c_top = np.array([0x6A, 0x70, 0x88], dtype=float) / 255.0     # #6A7088
        c_mid = np.array([0x90, 0x7C, 0x8E], dtype=float) / 255.0     # #907C8E
        c_bot = np.array([0x9E, 0x7E, 0x88], dtype=float) / 255.0     # #9E7E88
        c_fade = np.array([0xB0, 0x98, 0x98], dtype=float) / 255.0    # #B09898

        if depth < 0.5:
            t = depth / 0.5
            return (1 - t) * c_top + t * c_mid
        else:
            t = (depth - 0.5) / 0.5
            rgb = (1 - t) * c_mid + t * c_bot
            # blend toward fade at very bottom
            fade_t = max(0, (depth - 0.75) / 0.25)
            rgb = (1 - fade_t) * rgb + fade_t * c_fade
            return rgb

    def color_for_depth_v(depth):
        """Slightly cooler variant for vertical lines."""
        c_top = np.array([0x80, 0x80, 0x90], dtype=float) / 255.0     # #808090
        c_mid = np.array([0x85, 0x78, 0x8A], dtype=float) / 255.0
        c_bot = np.array([0x9A, 0x88, 0x90], dtype=float) / 255.0
        if depth < 0.5:
            t = depth / 0.5
            return (1 - t) * c_top + t * c_mid
        else:
            t = (depth - 0.5) / 0.5
            return (1 - t) * c_mid + t * c_bot

    # --- Draw horizontal lines with catenary sag ---
    for i, y0 in enumerate(y_positions):
        # depth: 0 at top, 1 at bottom
        depth = 1.0 - (y0 - margin_b) / (1 - margin_t - margin_b)
        depth = np.clip(depth, 0, 1)

        x = np.linspace(margin_l, 1 - margin_r, n_pts)

        # Catenary sag: a cable hung between two endpoints sags most at the CENTER.
        # Shape: sag(x) = S * [cosh(L/a) - cosh(dx/a)] / [cosh(L/a) - 1]
        # where S = max sag at center, L = half-span, dx = x - x_center
        # This equals S at center (dx=0) and 0 at endpoints (dx=+/-L).

        max_sag = 0.0005 + 0.12 * depth ** 2.5  # nearly zero at top, ~0.12 at bottom
        half_span = (1 - margin_l - margin_r) / 2.0  # ~0.44

        # Catenary parameter a controls the curvature shape
        # Smaller a = more pointed/peaked sag; larger a = more parabolic
        # Use a that decreases with depth for sharper catenary at bottom
        a = 1.2 - 0.9 * depth ** 1.5
        a = max(a, 0.15)

        dx = x - x_center
        cosh_L = np.cosh(half_span / a)
        cosh_dx = np.cosh(dx / a)
        # Normalized so it equals 1 at center and 0 at endpoints
        sag_shape = (cosh_L - cosh_dx) / (cosh_L - 1.0)
        sag_shape = np.clip(sag_shape, 0, 1)  # numerical safety

        y_deformed = y0 - max_sag * sag_shape

        # Add slight wobble that grows with depth
        wobble_amp = 0.0003 + 0.0025 * depth ** 1.5
        wobble = wobble_amp * np.sin(2 * np.pi * (3.5 * x + 0.7 * i))
        y_deformed += wobble

        # --- Dissolution: break segments at random points ---
        k_dissolve = 4.0
        p_break = 1.0 - np.exp(-k_dissolve * depth)
        break_mask = np.ones(n_pts, dtype=bool)

        if depth > 0.18:
            # Breaks at grid intersection neighborhoods
            for xv in x_positions:
                if rng.random() < p_break * 0.45:
                    gap_half = 0.006 + 0.014 * depth * rng.random()
                    break_mask &= ~((x > xv - gap_half) & (x < xv + gap_half))

            # Additional random segment drops at heavy depth
            if depth > 0.55:
                n_extra_breaks = rng.randint(0, int(5 * depth))
                for _ in range(n_extra_breaks):
                    bx = margin_l + rng.random() * (1 - margin_l - margin_r)
                    bw = 0.012 + 0.03 * rng.random()
                    break_mask &= ~((x > bx - bw) & (x < bx + bw))

        # Color and style
        rgb = color_for_depth(depth)
        alpha = 0.75 - 0.35 * depth  # fades toward bottom
        alpha = np.clip(alpha, 0.30, 0.78)
        lw = 0.8 - 0.3 * depth       # thinner toward bottom
        lw = np.clip(lw, 0.45, 0.85)

        # --- Ghost echo: faint line at original pristine position ---
        if depth > 0.12:
            ghost_alpha = 0.08 + 0.14 * depth
            ghost_alpha = np.clip(ghost_alpha, 0.08, 0.20)
            ghost_rgb = np.clip(rgb * 1.18 + 0.06, 0, 1)
            ax.plot(x, np.full_like(x, y0),
                    color=(*ghost_rgb, ghost_alpha),
                    lw=0.35, solid_capstyle="round", zorder=1)

        # --- Draw the sagged line in segments (respecting breaks) ---
        _draw_masked_line(ax, x, y_deformed, break_mask, rgb, alpha, lw, zorder=3)

    # --- Draw vertical lines with buckling ---
    for j, x0 in enumerate(x_positions):
        y = np.linspace(margin_b, 1 - margin_t, n_pts)
        # depth increases as y decreases
        depth_arr = 1.0 - (y - margin_b) / (1 - margin_t - margin_b)
        depth_arr = np.clip(depth_arr, 0, 1)

        # Sinusoidal buckle that grows with depth -- gentle and organic
        buckle_freq = 0.8 + 0.5 * np.sin(0.6 * j)
        buckle_phase = rng.random() * 2 * np.pi
        buckle_amp = 0.008 * depth_arr ** 2.2
        # Add a lean component (cumulative drift, like gravity pulling)
        lean_dir = rng.choice([-1, 1]) * (0.3 + 0.7 * rng.random())
        lean = lean_dir * 0.018 * depth_arr ** 2.0

        x_deformed = x0 + buckle_amp * np.sin(2 * np.pi * buckle_freq * y + buckle_phase) + lean

        # Dissolution for vertical lines
        break_mask_v = np.ones(n_pts, dtype=bool)
        for yh in y_positions:
            local_depth = 1.0 - (yh - margin_b) / (1 - margin_t - margin_b)
            local_depth = np.clip(local_depth, 0, 1)
            if local_depth > 0.2 and rng.random() < (1.0 - np.exp(-3.8 * local_depth)) * 0.5:
                gap_half = 0.006 + 0.010 * local_depth * rng.random()
                break_mask_v &= ~((y > yh - gap_half) & (y < yh + gap_half))

        # Additional breaks at heavy depth region (bottom quarter)
        if True:
            heavy_region = depth_arr > 0.7
            n_heavy_breaks = rng.randint(0, 3)
            for _ in range(n_heavy_breaks):
                by = margin_b + rng.random() * 0.25 * (1 - margin_t - margin_b)
                bw = 0.01 + 0.02 * rng.random()
                break_mask_v &= ~((y > by - bw) & (y < by + bw))

        # Per-point depth for color: use average depth
        avg_depth = np.mean(depth_arr)
        rgb_v = color_for_depth_v(avg_depth)
        alpha_v = 0.55 - 0.15 * avg_depth
        alpha_v = np.clip(alpha_v, 0.30, 0.60)
        lw_v = 0.55 - 0.10 * avg_depth
        lw_v = np.clip(lw_v, 0.40, 0.60)

        # Ghost echo for vertical lines
        ghost_alpha_v = 0.10
        ghost_rgb_v = np.clip(rgb_v * 1.12 + 0.06, 0, 1)
        # Only ghost the bottom portion where buckling is visible
        y_ghost_start = 1 - margin_t - 0.5 * (1 - margin_t - margin_b)
        ghost_mask = y < y_ghost_start
        if np.any(ghost_mask):
            y_g = y[ghost_mask]
            ax.plot(np.full_like(y_g, x0), y_g,
                    color=(*ghost_rgb_v, ghost_alpha_v),
                    lw=0.30, solid_capstyle="round", zorder=1)

        # Draw buckled vertical line
        _draw_masked_line(ax, x_deformed, y, break_mask_v, rgb_v, alpha_v, lw_v, zorder=2)

    # --- Save ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "melancholy_entropy.pdf")
    add_signature(fig, ax, BG_COLOR)
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path

def _draw_masked_line(ax, x, y, mask, rgb, alpha, lw, zorder=3):
    """Draw a line with gaps where mask is False, as separate segments."""
    segments = []
    in_seg = False
    start = 0
    for k in range(len(mask)):
        if mask[k] and not in_seg:
            start = k
            in_seg = True
        elif not mask[k] and in_seg:
            if k - start >= 2:
                segments.append((x[start:k], y[start:k]))
            in_seg = False
    if in_seg and len(x) - start >= 2:
        segments.append((x[start:], y[start:]))

    for sx, sy in segments:
        ax.plot(sx, sy, color=(*rgb, alpha), lw=lw,
                solid_capstyle="round", zorder=zorder)

if __name__ == '__main__':
    render()
