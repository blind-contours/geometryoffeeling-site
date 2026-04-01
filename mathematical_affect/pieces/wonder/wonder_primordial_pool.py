"""
Geometry of Feeling — Wonder: Primordial Pool
Recursive cluster spawning — primordial pools of scattered particles
nested in circles within circles. Built from the original spawn_clusters
with organic edges, green/teal at density, gold-tinted particles, and
subtle per-particle color variation.
"""
import os
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 320
FIG_W = 12
FIG_H = 8
MARGIN = "#DDD9D2"
BG = "#263B59"
PALETTE = ["#2060A0", "#4080C0", "#60A0E0", "#80C0FF", "#A0D0FF"]
TEAL_GLOW = "#50B898"
GREEN_DEEP = "#3A9878"
WARM_GOLD = "#D8B840"
PALE_GOLD = "#C8A848"
ML, MR, MB, MT = 0.07, 0.07, 0.08, 0.08


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgba(h, a):
    r, g, b = hex_to_rgb(h)
    return (r, g, b, float(np.clip(a, 0.0, 1.0)))


def shift_color(base_rgb, rng, hue_var=0.03, lum_var=0.06):
    """Slightly shift a color's RGB values for natural variation."""
    r, g, b = base_rgb
    r = np.clip(r + rng.uniform(-hue_var, hue_var), 0, 1)
    g = np.clip(g + rng.uniform(-hue_var, hue_var), 0, 1)
    b = np.clip(b + rng.uniform(-hue_var, hue_var), 0, 1)
    lum = rng.uniform(-lum_var, lum_var)
    r = np.clip(r + lum, 0, 1)
    g = np.clip(g + lum, 0, 1)
    b = np.clip(b + lum, 0, 1)
    return (r, g, b)


def wobble_contour(cx, cy, r, rng, wobble_amp=0.035, n_points=180):
    """Wobbly circle — subtle organic edges."""
    theta = np.linspace(0, 2 * np.pi, n_points)
    n_freqs = rng.integers(3, 5)
    freqs = rng.choice([2, 3, 4, 5, 6], size=n_freqs, replace=False)
    phases = rng.uniform(0, 2 * np.pi, n_freqs)
    amps = rng.uniform(0.3, 1.0, n_freqs) * wobble_amp
    wobble = sum(a * np.sin(f * theta + p) for f, p, a in zip(freqs, phases, amps))
    x = cx + r * (1.0 + wobble) * np.cos(theta)
    y = cy + r * (1.0 + wobble) * np.sin(theta)
    return x, y


def spawn_clusters(ax, cx, cy, r, depth, rng, _is_root=True):
    """
    Recursive cluster spawning with targeted beauty enhancements.
    Based on the original spawn_clusters with:
    - Organic wobble on circle edges
    - Green/teal glow at density zones
    - Gold-tinted particles mixed in
    - Per-particle hue/luminosity variation
    - Power-law particle size distribution
    """
    col_hex = PALETTE[min(len(PALETTE) - 1, depth % len(PALETTE))]
    col_rgb = hex_to_rgb(col_hex)

    # ── Pool body layers (original structure: r*1.6 halo, r*0.9 body) ──
    # Balanced pop: pool alpha x1.2
    for rr_scale, alpha in [(1.6, 0.022), (0.9, 0.038)]:
        rr = r * rr_scale
        wa = 0.035 * (0.4 if rr_scale > 1.2 else 1.0)
        wx, wy = wobble_contour(cx, cy, rr, rng, wobble_amp=wa)
        ax.fill(wx, wy, color=rgba(col_hex, alpha), zorder=1)

    # ── Green/teal glow at overlap zones (green x1.8) ──
    for glow_hex, glow_r, glow_a in [
        (GREEN_DEEP, r * 0.85, 0.031),
        (TEAL_GLOW,  r * 0.65, 0.043),
        (TEAL_GLOW,  r * 0.45, 0.040),
        (GREEN_DEEP, r * 0.30, 0.025),
    ]:
        ax.add_patch(Circle((cx, cy), glow_r,
                            facecolor=rgba(glow_hex, glow_a),
                            edgecolor="none", zorder=2))

    # ── Warm gold whisper at root pool center (gold x1.5) ──
    if _is_root:
        for glow_r, glow_a in [(r * 0.5, 0.015), (r * 0.3, 0.011)]:
            ax.add_patch(Circle((cx, cy), glow_r,
                                facecolor=rgba(WARM_GOLD, glow_a),
                                edgecolor="none", zorder=2))

    # ── Particles ──
    count = 18 if depth > 2 else 10
    ang = rng.uniform(0, 2 * np.pi, count)
    rad = r * (0.08 + 0.92 * np.sqrt(rng.random(count)))
    x = cx + rad * np.cos(ang)
    y = cy + rad * np.sin(ang)

    # Power-law sizes (size x1.2)
    raw = rng.power(0.45, count)
    sizes = (0.6 + 12.0 * raw) * (1.0 + depth * 0.2) * 1.2

    # Per-particle color: blue base + gold fraction + teal fraction
    p_colors = []
    for i in range(count):
        alpha_val = (0.14 + 0.28 * rng.random()) * 1.4  # particle alpha x1.4
        roll = rng.random()
        if roll < 0.12:
            # Gold-tinted
            gc = hex_to_rgb(PALE_GOLD if rng.random() < 0.5 else WARM_GOLD)
            gc = shift_color(gc, rng, 0.015, 0.06)
            p_colors.append(gc + (float(np.clip(alpha_val * 0.8, 0, 1)),))
        elif roll < 0.24:
            # Teal-tinted
            tc = hex_to_rgb(TEAL_GLOW)
            tc = shift_color(tc, rng, 0.03, 0.06)
            p_colors.append(tc + (float(np.clip(alpha_val * 0.7, 0, 1)),))
        else:
            # Base blue with variation
            bc = shift_color(col_rgb, rng, 0.03, 0.06)
            p_colors.append(bc + (float(np.clip(alpha_val, 0, 1)),))

    ax.scatter(x, y, s=sizes, c=p_colors, linewidths=0, zorder=3)

    # ── Strays ──
    n_strays = int(count * 0.42)
    s_ang = rng.uniform(0, 2 * np.pi, n_strays)
    s_rad = r * (1.05 + 0.6 * rng.random(n_strays))
    sx = cx + s_rad * np.cos(s_ang)
    sy = cy + s_rad * np.sin(s_ang)
    s_sizes = (0.3 + 3.0 * rng.power(0.4, n_strays)) * (0.8 + depth * 0.15) * 1.2
    s_colors = []
    for _ in range(n_strays):
        sc = shift_color(col_rgb, rng, 0.03, 0.06)
        s_colors.append(sc + (float(np.clip((0.06 + 0.10 * rng.random()) * 1.4, 0, 1)),))
    ax.scatter(sx, sy, s=s_sizes, c=s_colors, linewidths=0, zorder=3)

    # ── Children (same recursion as original) ──
    if depth == 0:
        return
    child_n = 2 + (1 if depth > 2 else 0)
    for i in range(child_n):
        angle = (2 * np.pi * i / child_n) + rng.uniform(-0.45, 0.45)
        dist = r * (0.46 + 0.16 * rng.random())
        spawn_clusters(
            ax,
            cx + dist * np.cos(angle),
            cy + dist * np.sin(angle),
            r * (0.42 + 0.06 * rng.random()),
            depth - 1, rng,
            _is_root=False,
        )


def render():
    rng = np.random.default_rng(31)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=MARGIN)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=MARGIN, edgecolor="none", zorder=-20))
    ax.add_patch(
        FancyBboxPatch(
            (ML, MB), 1 - ML - MR, 1 - MB - MT,
            boxstyle="square,pad=0", facecolor=BG, edgecolor="none", zorder=-10,
        )
    )

    # Root pools — R7 V10 layout
    spawn_clusters(ax, 0.47, 0.50, 0.19, 3, rng, _is_root=True)
    spawn_clusters(ax, 0.28, 0.64, 0.11, 2, rng, _is_root=True)
    spawn_clusters(ax, 0.71, 0.37, 0.12, 2, rng, _is_root=True)
    spawn_clusters(ax, 0.68, 0.63, 0.06, 1, rng, _is_root=False)

    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "wonder_primordial_pool.pdf")
    add_signature(fig, ax, MARGIN, margin_piece=True, margin_bottom=FIG_H * 0.08)
    fig.savefig(pdf_path, facecolor=MARGIN, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
