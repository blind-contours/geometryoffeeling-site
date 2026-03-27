"""
Geometry of Feeling — Fractured: Catastrophe Fold
Reconceived as "Diffusion Cliff Retreat":
Family of cliff profiles based on the diffusion equation solution.
A sharp cliff face erodes over time — each profile shows the surface
at a different moment, softening from a sharp step into a gentle S-curve.
The error function solution: z(x,t) = z₀ · erfc(x / 2√(Dt))
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.special import erfc
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG = "#F0EBE2"

COBALT = "#2255A4"; FOREST = "#1A6B3A"; CRIMSON = "#C8392B"
OCHRE = "#B87A2A"; NAVY = "#1C3755"; TEAL = "#1A5C8A"
SIENNA = "#A85A2A"; RUST = "#C84A20"

PAD_L = 0.78; PAD_R = 0.65; PAD_T = 0.72; PAD_B = 1.05
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))


def draw_lc(ax, xs, ys, col, lw, alpha, zo=4):
    if len(xs) < 2:
        return
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)


def render():
    np.random.seed(42)

    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')

    x_left = PAD_L + 0.2
    x_right = FIG_W - PAD_R - 0.2
    y_base = PAD_B + 0.3
    y_top = FIG_H - PAD_T - 0.3

    cliff_height = y_top - y_base
    x_span = x_right - x_left

    # Diffusion parameters
    D = 1.0
    z0 = cliff_height
    n_profiles = 28
    t_values = np.geomspace(0.02, 8.0, n_profiles)

    n_x = 500
    x_phys = np.linspace(-3.0, 6.0, n_x)

    def phys_to_fig_x(xp):
        return x_left + (xp - x_phys[0]) / (x_phys[-1] - x_phys[0]) * x_span

    n_strata = 18
    strata_heights_frac = np.linspace(0.04, 0.96, n_strata)

    # Draw profiles from latest (most eroded) to earliest (sharpest)
    for i, t in enumerate(reversed(t_values)):
        idx = n_profiles - 1 - i
        frac = idx / (n_profiles - 1)

        z = z0 * 0.5 * erfc(x_phys / (2 * np.sqrt(D * t)))

        fig_x = phys_to_fig_x(x_phys)
        fig_y = y_base + z

        sienna_rgb = hex_to_rgb(SIENNA)
        ochre_rgb = hex_to_rgb(OCHRE)
        r = sienna_rgb[0] * (1 - frac) + ochre_rgb[0] * frac
        g = sienna_rgb[1] * (1 - frac) + ochre_rgb[1] * frac
        b = sienna_rgb[2] * (1 - frac) + ochre_rgb[2] * frac
        profile_col = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

        alpha_profile = 0.55 * (1 - frac * 0.65)
        lw_profile = 1.0 - frac * 0.45

        # Subtle fill below profile (rock mass)
        fill_alpha = 0.03 + 0.04 * (1 - frac)
        fill_x = np.concatenate([fig_x, [fig_x[-1], fig_x[0]]])
        fill_y = np.concatenate([fig_y, [y_base, y_base]])
        fill_col = rgba(profile_col, fill_alpha)
        poly = plt.Polygon(np.column_stack([fill_x, fill_y]), closed=True,
                           facecolor=fill_col, edgecolor='none', zorder=2)
        ax.add_patch(poly)

        # Profile line
        draw_lc(ax, fig_x, fig_y, profile_col, lw_profile, alpha_profile,
                zo=4 + i * 0.01)

        # Strata lines that bend with profile
        for s_frac in strata_heights_frac:
            strata_z = z * s_frac
            strata_y = y_base + strata_z

            mask = strata_z > 0.03
            if not np.any(mask):
                continue

            sx_all = fig_x[mask]
            sy_all = strata_y[mask]

            if len(sx_all) < 2:
                continue

            strata_alpha = 0.025 * (1 - frac * 0.7)
            draw_lc(ax, sx_all, sy_all, SIENNA, 0.25, strata_alpha, zo=3)

    # Scattered fragments/sediment at base
    np.random.seed(77)
    n_fragments = 800
    for _ in range(n_fragments):
        fx = np.random.beta(3, 1.5) * x_span + x_left
        fy = y_base - np.random.exponential(0.15) - 0.05
        if fy < y_base - 1.2:
            continue

        t_frag = (fx - x_left) / x_span
        if np.random.rand() > t_frag * 0.7 + 0.15:
            continue

        frag_alpha = 0.08 + 0.25 * np.random.rand() * t_frag
        frag_size = 0.5 + np.random.rand() * 2.0 * (1 - t_frag * 0.5)
        col = OCHRE if np.random.rand() < 0.6 else SIENNA
        ax.plot(fx, fy, '.', color=rgba(col, frag_alpha),
                markersize=frag_size, zorder=5)

    # Small fragment blocks near base
    np.random.seed(33)
    for _ in range(80):
        bx = np.random.beta(2.5, 1.2) * x_span + x_left
        by = y_base - np.random.uniform(0.05, 0.6)
        t_b = (bx - x_left) / x_span
        if np.random.rand() > t_b * 0.6 + 0.1:
            continue
        size = np.random.uniform(0.02, 0.10) * (1 - t_b * 0.4)
        angle = np.random.uniform(0, 2 * np.pi)
        corners = []
        for a in [0, np.pi/2, np.pi, 3*np.pi/2]:
            corners.append([bx + size * np.cos(a + angle),
                            by + size * np.sin(a + angle)])
        block = plt.Polygon(corners, closed=True,
                            facecolor=rgba(SIENNA, 0.10 + 0.12 * np.random.rand()),
                            edgecolor=rgba(RUST, 0.08),
                            linewidth=0.3, zorder=5)
        ax.add_patch(block)

    # Water suggestion: very faint teal washes
    np.random.seed(123)
    for i in range(25):
        wx_start = np.random.uniform(x_left + x_span * 0.2, x_right)
        wy_start = np.random.uniform(y_base + cliff_height * 0.3, y_top)
        n_w = 60
        wx = np.zeros(n_w)
        wy = np.zeros(n_w)
        wx[0] = wx_start
        wy[0] = wy_start
        for k in range(1, n_w):
            wx[k] = wx[k-1] + np.random.randn() * 0.03 + 0.02
            wy[k] = wy[k-1] - 0.06 - 0.02 * np.random.rand()
            if wy[k] < y_base - 0.5:
                break
        wx = wx[:k+1]
        wy = wy[:k+1]
        draw_lc(ax, wx, wy, TEAL, 0.4, 0.04, zo=3)

    # Equation label
    ax.text(0.75, 0.75, "\u2202z/\u2202t = D\u00b7\u2207\u00b2z",
            fontfamily='monospace', fontsize=10,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transData)

    # Save
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "fractured_catastrophe_fold.pdf")
    fig.savefig(pdf_path, format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
