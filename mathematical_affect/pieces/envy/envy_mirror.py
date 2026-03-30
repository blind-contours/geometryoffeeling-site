"""
Geometry of Feeling — Envy: Parasitic Resonance
Two spiral bodies where one steals saturation from the other.
LEFT body (source): vivid greens/gold-greens, full weight and alpha.
RIGHT body (shadow): same curves but desaturated, thinner, hollower.
Coupling filaments carry color from source to shadow.
"""
import os
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#DDD9D2'

np.random.seed(42)

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
# Source body: vivid greens and gold-greens
SOURCE_GREENS = [
    '#4A8A30', '#3A7A28', '#5A9A38', '#4E8E34', '#3E7E2C',
    '#48862E', '#528E36', '#447C2A', '#569240', '#3C7826',
]
# Shadow body: desaturated grey-greens
SHADOW_GREYS = [
    '#7A8A78', '#6A7A6A', '#8A9A88', '#748A72', '#7E8E7C',
    '#708870', '#849684', '#6E7E6E', '#889888', '#768876',
]
# Core glow colours
SOURCE_CORE = '#5CA040'
SHADOW_CORE = '#7A8A78'

def hex_to_rgba(h, a):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return (r, g, b, float(np.clip(a, 0, 1)))

def render():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Centres — source left-of-centre, shadow right-of-centre
    src_cx, src_cy = 0.33, 0.50
    shd_cx, shd_cy = 0.68, 0.50

    # ------------------------------------------------------------------
    # Rose-curve orbital parameters
    # ------------------------------------------------------------------
    n_orbits = 36  # 30-40 range
    k_values = [2, 3, 5, 7]  # petal counts for rose curves

    theta = np.linspace(0, 2 * np.pi * 3, 4000)  # 3 full wraps

    # ------------------------------------------------------------------
    # SOURCE BODY — vivid, full weight
    # ------------------------------------------------------------------
    for i in range(n_orbits):
        frac = i / (n_orbits - 1)

        # Pick k and phase to create varied petal structure
        k = k_values[i % len(k_values)]
        phi = frac * 1.6 + 0.3 * np.sin(i * 0.7)

        # Radius envelope — concentric orbits growing outward
        r_base = 0.03 + frac * 0.17
        # Rose modulation
        r_mod = r_base * (1.0 + 0.35 * np.cos(k * theta + phi))
        # Add subtle spiral drift
        spiral = 0.005 * theta / (2 * np.pi)
        r = r_mod + spiral * (0.3 + 0.7 * frac)

        xs = src_cx + r * np.cos(theta)
        ys = src_cy + r * np.sin(theta)

        # Colour, weight, alpha
        col = SOURCE_GREENS[i % len(SOURCE_GREENS)]
        lw = 0.6 + 0.6 * frac  # 0.6 to 1.2
        alpha = 0.4 + 0.4 * (1.0 - frac)  # inner brighter, outer slightly less

        pts = np.column_stack([xs, ys]).reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        lc = mc.LineCollection(segs, linewidths=lw,
                               colors=[hex_to_rgba(col, alpha)],
                               capstyle='round', joinstyle='round', zorder=5)
        ax.add_collection(lc)

    # ------------------------------------------------------------------
    # SHADOW BODY — same maths, diminished
    # ------------------------------------------------------------------
    for i in range(n_orbits):
        frac = i / (n_orbits - 1)

        k = k_values[i % len(k_values)]
        phi = frac * 1.6 + 0.3 * np.sin(i * 0.7)

        # Same base but slightly LARGER extent (1+epsilon) yet compressed amp
        r_base = 0.03 + frac * 0.19  # 0.19 > 0.17 — larger envelope
        # Rose modulation — amplitude compressed (the "drain")
        r_mod = r_base * (1.0 + 0.20 * np.cos(k * theta + phi))  # 0.20 < 0.35
        spiral = 0.005 * theta / (2 * np.pi)
        r = r_mod + spiral * (0.3 + 0.7 * frac)

        # Exponential decay factor — the delta in the equation
        decay = np.exp(-0.08 * frac * 10)  # diminishes outer orbits more
        r = r * (0.85 + 0.15 * decay)

        xs = shd_cx + r * np.cos(theta)
        ys = shd_cy + r * np.sin(theta)

        # Desaturated colours, thinner, lower alpha
        col = SHADOW_GREYS[i % len(SHADOW_GREYS)]
        lw = 0.3 + 0.35 * frac  # thinner: 0.3 to 0.65
        alpha = 0.18 + 0.22 * (1.0 - frac)  # much lower: 0.18 to 0.40

        pts = np.column_stack([xs, ys]).reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        lc = mc.LineCollection(segs, linewidths=lw,
                               colors=[hex_to_rgba(col, alpha)],
                               capstyle='round', joinstyle='round', zorder=3)
        ax.add_collection(lc)

    # ------------------------------------------------------------------
    # GLOWING CORES
    # ------------------------------------------------------------------
    # Source core — layered circles fading outward
    for j in range(8):
        radius = 0.008 + j * 0.006
        alpha_c = 0.50 - j * 0.055
        circle = plt.Circle((src_cx, src_cy), radius,
                             color=hex_to_rgba(SOURCE_CORE, max(alpha_c, 0.04)),
                             fill=True, zorder=10)
        ax.add_patch(circle)

    # Shadow core — dimmer version
    for j in range(6):
        radius = 0.006 + j * 0.005
        alpha_c = 0.22 - j * 0.030
        circle = plt.Circle((shd_cx, shd_cy), radius,
                             color=hex_to_rgba(SHADOW_CORE, max(alpha_c, 0.02)),
                             fill=True, zorder=8)
        ax.add_patch(circle)

    # ------------------------------------------------------------------
    # COUPLING FILAMENTS — 14 arcs carrying colour from source to shadow
    # ------------------------------------------------------------------
    n_arcs = 14
    for i in range(n_arcs):
        frac = i / (n_arcs - 1)
        # Departure angle on source body
        angle_src = 2 * np.pi * frac + 0.15 * np.sin(i * 1.3)
        # Arrival angle on shadow body (slightly offset)
        angle_shd = 2 * np.pi * frac + 0.4 * np.sin(i * 0.9 + 0.7)

        # Radii at the edge of each body
        r_src = 0.03 + 0.17 * (0.5 + 0.5 * np.cos(3 * angle_src))
        r_shd = 0.03 + 0.19 * (0.5 + 0.5 * np.cos(3 * angle_shd))

        # Start/end points
        p_src = np.array([src_cx + r_src * np.cos(angle_src),
                          src_cy + r_src * np.sin(angle_src)])
        p_shd = np.array([shd_cx + r_shd * np.cos(angle_shd),
                          shd_cy + r_shd * np.sin(angle_shd)])

        # Control point for a gentle arc (slight vertical offset)
        mid = 0.5 * (p_src + p_shd)
        perp_offset = 0.04 * np.sin(frac * np.pi * 2 + 0.5) + 0.02
        ctrl = mid + np.array([0.0, perp_offset])

        # Quadratic Bezier arc: C(s) = (1-s)^2 * P0 + 2s(1-s) * ctrl + s^2 * P1
        s = np.linspace(0, 1, 200)
        arc_x = (1 - s)**2 * p_src[0] + 2 * s * (1 - s) * ctrl[0] + s**2 * p_shd[0]
        arc_y = (1 - s)**2 * p_src[1] + 2 * s * (1 - s) * ctrl[1] + s**2 * p_shd[1]

        pts = np.column_stack([arc_x, arc_y]).reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        n_seg = len(segs)

        # Gradient: vivid green near source -> grey-green near shadow
        colors = []
        lws = []
        for j in range(n_seg):
            t = j / (n_seg - 1)
            # Interpolate from source green to shadow grey
            c_src = hex_to_rgba(SOURCE_GREENS[i % len(SOURCE_GREENS)], 1.0)
            c_shd = hex_to_rgba(SHADOW_GREYS[i % len(SHADOW_GREYS)], 1.0)
            r = c_src[0] * (1 - t) + c_shd[0] * t
            g = c_src[1] * (1 - t) + c_shd[1] * t
            b = c_src[2] * (1 - t) + c_shd[2] * t
            a = (0.38 * (1 - t) + 0.12 * t) * (0.7 + 0.3 * np.sin(frac * np.pi))
            colors.append((r, g, b, a))
            lws.append(0.5 * (1 - t) + 0.3 * t)  # thins toward shadow

        lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                               capstyle='round', joinstyle='round', zorder=4)
        ax.add_collection(lc)

    # ------------------------------------------------------------------
    # Equation label
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, 'envy_mirror.pdf')
    add_signature(fig, ax, BG_COLOR)
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    render()
