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
WARM_TEAL = "#60C070"
WARM_GREEN = "#70B850"
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


def blend_hex(h1, h2, t):
    """Blend two hex colors. t=0 returns h1, t=1 returns h2."""
    r1, g1, b1 = hex_to_rgb(h1)
    r2, g2, b2 = hex_to_rgb(h2)
    return (np.clip(r1 + (r2 - r1) * t, 0, 1),
            np.clip(g1 + (g2 - g1) * t, 0, 1),
            np.clip(b1 + (b2 - b1) * t, 0, 1))


def lerp(a, b, t):
    return a + (b - a) * t


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


def spawn_clusters(ax, cx, cy, r, depth, rng, _is_root=True,
                   warmth=0.0, warmth_decay=0.6, child_warmths=None):
    """
    Recursive cluster spawning with warmth gradient for visual hierarchy.
    warmth (0.0–1.0) controls glow brightness, color temperature
    (teal → warm green), and gold particle fraction per pool.
    """
    col_hex = PALETTE[min(len(PALETTE) - 1, depth % len(PALETTE))]
    col_rgb = hex_to_rgb(col_hex)

    # ── Pool body layers ──
    for rr_scale, alpha in [(1.6, 0.022), (0.9, 0.038)]:
        rr = r * rr_scale
        wa = 0.035 * (0.4 if rr_scale > 1.2 else 1.0)
        wx, wy = wobble_contour(cx, cy, rr, rng, wobble_amp=wa)
        ax.fill(wx, wy, color=rgba(col_hex, alpha), zorder=1)

    # ── Green/teal glow — warmth shifts brightness and color ──
    glow_alpha_mult = lerp(1.0, 2.5, warmth)
    for glow_hex_cool, glow_hex_warm, glow_r, glow_a in [
        (GREEN_DEEP, WARM_GREEN, r * 0.85, 0.031),
        (TEAL_GLOW,  WARM_TEAL,  r * 0.65, 0.043),
        (TEAL_GLOW,  WARM_TEAL,  r * 0.45, 0.040),
        (GREEN_DEEP, WARM_GREEN, r * 0.30, 0.025),
    ]:
        blended = blend_hex(glow_hex_cool, glow_hex_warm, warmth)
        fc = blended + (float(np.clip(glow_a * glow_alpha_mult, 0, 1)),)
        ax.add_patch(Circle((cx, cy), glow_r,
                            facecolor=fc, edgecolor="none", zorder=2))

    # Extra glow layers at high warmth
    if warmth > 0.15:
        extra_alpha = warmth * 0.04
        for er, ea in [(r * 0.55, extra_alpha), (r * 0.35, extra_alpha * 0.8)]:
            blended = blend_hex(TEAL_GLOW, WARM_TEAL, warmth)
            fc = blended + (float(np.clip(ea, 0, 1)),)
            ax.add_patch(Circle((cx, cy), er, facecolor=fc, edgecolor="none", zorder=2))

    # ── Gold center glow ──
    if _is_root:
        gold_mult = lerp(1.0, 3.5, warmth)
        for glow_r, glow_a in [(r * 0.5, 0.015), (r * 0.3, 0.011)]:
            ax.add_patch(Circle((cx, cy), glow_r,
                                facecolor=rgba(WARM_GOLD, glow_a * gold_mult),
                                edgecolor="none", zorder=2))

    # ── Particles ──
    count = 18 if depth > 2 else 10
    ang = rng.uniform(0, 2 * np.pi, count)
    rad = r * (0.08 + 0.92 * np.sqrt(rng.random(count)))
    x = cx + rad * np.cos(ang)
    y = cy + rad * np.sin(ang)

    raw = rng.power(0.45, count)
    sizes = (0.6 + 12.0 * raw) * (1.0 + depth * 0.2) * 1.2

    gold_frac = lerp(0.12, 0.25, warmth)
    teal_frac = 0.12

    p_colors = []
    for i in range(count):
        alpha_val = (0.14 + 0.28 * rng.random()) * 1.4
        roll = rng.random()
        if roll < gold_frac:
            gc = hex_to_rgb(PALE_GOLD if rng.random() < 0.5 else WARM_GOLD)
            gc = shift_color(gc, rng, 0.015, 0.06)
            p_colors.append(gc + (float(np.clip(alpha_val * 0.8, 0, 1)),))
        elif roll < gold_frac + teal_frac:
            tc = hex_to_rgb(TEAL_GLOW)
            tc = shift_color(tc, rng, 0.03, 0.06)
            p_colors.append(tc + (float(np.clip(alpha_val * 0.7, 0, 1)),))
        else:
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

    # ── Children ──
    if depth == 0:
        return
    child_n = 2 + (1 if depth > 2 else 0)
    for i in range(child_n):
        angle = (2 * np.pi * i / child_n) + rng.uniform(-0.45, 0.45)
        dist = r * (0.46 + 0.16 * rng.random())
        if child_warmths is not None and i < len(child_warmths):
            cw = child_warmths[i]
        else:
            cw = warmth * warmth_decay
        spawn_clusters(
            ax,
            cx + dist * np.cos(angle),
            cy + dist * np.sin(angle),
            r * (0.42 + 0.06 * rng.random()),
            depth - 1, rng,
            _is_root=False,
            warmth=cw,
            warmth_decay=warmth_decay,
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

    # Root pools — Balanced Fill layout with warmth gradient
    spawn_clusters(ax, 0.46, 0.50, 0.25, 3, rng, _is_root=True,
                   warmth=0.12, child_warmths=[0.9, 0.0, 0.0])
    spawn_clusters(ax, 0.25, 0.66, 0.14, 2, rng, _is_root=True, warmth=0.0)
    spawn_clusters(ax, 0.74, 0.35, 0.15, 2, rng, _is_root=True, warmth=0.0)
    spawn_clusters(ax, 0.70, 0.66, 0.08, 1, rng, _is_root=False, warmth=0.0)

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
