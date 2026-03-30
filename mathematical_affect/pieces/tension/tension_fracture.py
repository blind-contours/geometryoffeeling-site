"""
Geometry of Feeling — Tension: Tension Fracture
Standalone render script
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
import os

DPI    = 300
FIG_W  = 12
FIG_H  = 8

BG       = "#1A1A1A"
ACID     = "#E8D820"
DIM      = "#888810"
HOT      = "#D04010"
RED      = "#C03010"
ELECTRIC = "#E0E020"
ORANGE   = "#E87020"

PAD_L = 0.65; PAD_R = 0.55; PAD_T = 0.60; PAD_B = 0.85
PW = FIG_W - PAD_L - PAD_R
PH = FIG_H - PAD_T  - PAD_B
cx = PAD_L + PW / 2
cy = PAD_B + PH / 2

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax  = fig.add_subplot(111)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax

def split_segments(xs, ys, mask):
    """Split arrays into contiguous segments where mask is True."""
    segments = []
    in_seg = False
    start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j
            in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3:
                segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3:
        segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4):
    pts  = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc   = mc.LineCollection(segs, linewidths=lw,
                             colors=[rgba(col, alpha)],
                             capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def render():
    fig, ax = make_fig()
    N = 4000
    Y_MIN = PAD_B + 0.02
    Y_MAX = PAD_B + PH - 0.02

    # --- Main stress-strain curve ---
    # Elastic region: linear (Hooke's law)
    # Yield + hardening: power law
    # Necking: decreasing engineering stress
    # Fracture: sudden drop
    eps = np.linspace(0, 1.0, N)
    xs  = PAD_L + PW * eps

    # Material parameters
    E = 6.0           # Young's modulus (slope of elastic region)
    eps_yield = 0.12  # yield strain
    sigma_yield = E * eps_yield  # yield stress
    n_hard = 0.35     # hardening exponent
    eps_uts = 0.55    # ultimate tensile strength strain
    eps_neck = 0.75   # necking completes
    eps_frac = 0.82   # fracture point

    sigma = np.zeros_like(eps)
    for i, e in enumerate(eps):
        if e <= eps_yield:
            # Elastic: sigma = E * epsilon
            sigma[i] = E * e
        elif e <= eps_uts:
            # Power-law hardening: sigma = sigma_y * (e/e_y)^n
            sigma[i] = sigma_yield * (e / eps_yield) ** n_hard
        elif e <= eps_frac:
            # Necking: gradual decrease
            sigma_uts = sigma_yield * (eps_uts / eps_yield) ** n_hard
            t_neck = (e - eps_uts) / (eps_frac - eps_uts)
            sigma[i] = sigma_uts * (1.0 - 0.55 * t_neck**1.8)
        else:
            # Post-fracture: rapid drop to near zero
            sigma_at_frac = sigma_yield * (eps_uts / eps_yield) ** n_hard * (1.0 - 0.55 * 1.0)
            t_post = (e - eps_frac) / (1.0 - eps_frac)
            sigma[i] = sigma_at_frac * np.exp(-12.0 * t_post)

    # Scale to canvas
    sigma_max = np.max(sigma)
    ys = PAD_B + PH * 0.08 + (PH * 0.82) * sigma / sigma_max
    ys = np.clip(ys, Y_MIN, Y_MAX)

    # --- Yield point marker region: subtle shading ---
    yield_idx = int(eps_yield * N)
    uts_idx = int(eps_uts * N)
    frac_idx = int(eps_frac * N)

    # Fill area under curve with gradient tension glow
    for i in range(0, N - 1, 2):
        if eps[i] < eps_yield:
            a = 0.04
            col = ACID
        elif eps[i] < eps_uts:
            t = (eps[i] - eps_yield) / (eps_uts - eps_yield)
            a = 0.04 + 0.14 * t
            col = ACID if t < 0.5 else ORANGE
        elif eps[i] < eps_frac:
            a = 0.18 + 0.10 * ((eps[i] - eps_uts) / (eps_frac - eps_uts))
            col = HOT
        else:
            a = 0.08
            col = RED
        y_base = PAD_B + PH * 0.08
        ax.fill([xs[i], xs[i+1], xs[i+1], xs[i]],
                [y_base, y_base, ys[i+1], ys[i]],
                color=rgba(col, a), linewidth=0, zorder=2)

    # --- Main curve with color gradient ---
    acid_rgb = hex_to_rgb(ACID)
    hot_rgb  = hex_to_rgb(HOT)
    red_rgb  = hex_to_rgb(RED)
    pts  = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    colors = []
    for i in range(len(segs)):
        if eps[i] < eps_yield:
            c = acid_rgb
            alpha = 0.85
            lw = 2.0
        elif eps[i] < eps_uts:
            t = (eps[i] - eps_yield) / (eps_uts - eps_yield)
            c = tuple(acid_rgb[k] * (1 - t) + hot_rgb[k] * t for k in range(3))
            alpha = 0.88
            lw = 2.2
        elif eps[i] < eps_frac:
            t = (eps[i] - eps_uts) / (eps_frac - eps_uts)
            c = tuple(hot_rgb[k] * (1 - t) + red_rgb[k] * t for k in range(3))
            alpha = 0.90
            lw = 2.4
        else:
            c = red_rgb
            alpha = 0.6 * np.exp(-5.0 * (eps[i] - eps_frac))
            lw = 1.5
        colors.append((*c, float(np.clip(alpha, 0, 1))))
    lws = np.array([2.0 if eps[i] < eps_yield else
                     2.0 + 0.5 * ((eps[i] - eps_yield) / max(eps_frac - eps_yield, 0.01))
                     if eps[i] < eps_frac else 1.2
                     for i in range(len(segs))])
    lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                           capstyle='round', zorder=5)
    ax.add_collection(lc)

    # --- Yield point vertical dashed line ---
    x_yield = xs[yield_idx]
    ax.plot([x_yield, x_yield], [Y_MIN, ys[yield_idx]],
            color=rgba(DIM, 0.35), linewidth=0.8, linestyle='--', zorder=3)
    ax.plot(x_yield, ys[yield_idx], 'o', color=rgba(ACID, 0.7),
            markersize=4, markeredgewidth=0, zorder=7)

    # --- UTS marker ---
    x_uts = xs[uts_idx]
    ax.plot([x_uts, x_uts], [Y_MIN, ys[uts_idx]],
            color=rgba(DIM, 0.30), linewidth=0.8, linestyle='--', zorder=3)
    ax.plot(x_uts, ys[uts_idx], 'o', color=rgba(HOT, 0.8),
            markersize=4.5, markeredgewidth=0, zorder=7)

    # --- FRACTURE POINT: microcracks radiating outward ---
    x_frac = xs[frac_idx]
    y_frac = ys[frac_idx]
    ax.plot(x_frac, y_frac, 'o', color=rgba(RED, 0.95),
            markersize=6, markeredgewidth=0, zorder=8)

    # Microcrack propagation — branching stochastic lines
    np.random.seed(42)
    n_cracks = 28
    for _ in range(n_cracks):
        angle = np.random.uniform(0, 2 * np.pi)
        length = np.random.uniform(0.3, 1.8)
        n_pts = 40
        t_crack = np.linspace(0, length, n_pts)
        # Random walk perpendicular to main direction
        dx = np.cos(angle)
        dy = np.sin(angle)
        wander = np.cumsum(np.random.normal(0, 0.015, n_pts))
        crack_x = x_frac + t_crack * dx - wander * dy
        crack_y = y_frac + t_crack * dy + wander * dx
        # Clip to canvas
        mask = ((crack_x >= PAD_L) & (crack_x <= PAD_L + PW) &
                (crack_y >= Y_MIN) & (crack_y <= Y_MAX))
        segments = split_segments(crack_x, crack_y, mask)
        for sx, sy in segments:
            n_s = len(sx)
            pts_c = np.array([sx, sy]).T.reshape(-1, 1, 2)
            segs_c = np.concatenate([pts_c[:-1], pts_c[1:]], axis=1)
            # Fade alpha along crack length
            alphas = np.linspace(0.55, 0.05, n_s - 1)
            lws_c  = np.linspace(1.3, 0.3, n_s - 1)
            cols_c = []
            for j in range(n_s - 1):
                t_j = j / max(n_s - 2, 1)
                r = red_rgb[0] * (1 - t_j) + hot_rgb[0] * t_j
                g = red_rgb[1] * (1 - t_j) + hot_rgb[1] * t_j
                b = red_rgb[2] * (1 - t_j) + hot_rgb[2] * t_j
                cols_c.append((r, g, b, float(alphas[j])))
            lc_c = mc.LineCollection(segs_c, linewidths=lws_c, colors=cols_c,
                                     capstyle='round', zorder=6)
            ax.add_collection(lc_c)

    # --- Ghost curves: repeated stress-strain at lower opacity (material memory) ---
    for offset_y, a_mult in [(-0.25, 0.12), (-0.50, 0.07), (0.20, 0.10)]:
        ys_ghost = ys + offset_y
        ys_ghost = np.clip(ys_ghost, Y_MIN, Y_MAX)
        # Only draw up to fracture
        mask = (eps <= eps_frac) & (ys_ghost >= Y_MIN) & (ys_ghost <= Y_MAX)
        segs_g = split_segments(xs, ys_ghost, mask)
        for sx, sy in segs_g:
            draw_lc(ax, sx, sy, DIM, 0.8, a_mult, zo=2)

    add_signature(fig, ax, BG)
    save(fig, "tension_fracture.pdf")

if __name__ == '__main__':
    render()
