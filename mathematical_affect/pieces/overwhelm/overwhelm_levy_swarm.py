"""
Geometry of Feeling — Overwhelm: Overwhelm Levy Swarm
Standalone render script
"""

"""
Geometry of Feeling — Overwhelm (Final Series)
Five pieces: Attractors, Turbulence, Kuramoto, PhaseFlood, LevySwarm

Mathematical primitives: overlaid strange attractors (Lorenz/Rossler/Chen/Halvorsen),
Navier-Stokes-inspired turbulent streamlines, Kuramoto coupled oscillators at critical
coupling, pendulum phase-space trajectories, Levy flight swarms with heavy tails

Aesthetic: claustrophobic density, competing vivid signals on near-black,
every curve demands attention simultaneously — the visual cortex cannot parse it all

Background: #0A0A12 (very dark — overwhelm is claustrophobic)
Palette: 10+ vivid colors competing for attention

Dependencies: matplotlib, numpy
    pip install matplotlib numpy
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle
import os


DPI = 300
FIG_W = 12
FIG_H = 8
BG = "#0A0A12"

# Palette: 10+ vivid colors competing for attention
ACID = "#E8D820"
FIRE = "#E05010"
COBALT = "#2255C8"
CRIMSON = "#C82050"
EMERALD = "#20B870"
VIOLET = "#A020C8"
AMBER = "#E8A020"
CYAN = "#20C8C8"
MAGENTA = "#C82888"
LIME = "#88C820"
COLS = [ACID, FIRE, COBALT, CRIMSON, EMERALD,
        VIOLET, AMBER, CYAN, MAGENTA, LIME]

PAD_L = 0.72
PAD_R = 0.60
PAD_T = 0.65
PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R
PH = FIG_H - PAD_T - PAD_B
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
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def label(ax, eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(1,1,1,0.18),transform=ax.transData)
def split_segments(xs, ys, mask):
    """Split masked arrays into contiguous segments to avoid straight-line jumps."""
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
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)


def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Ensure name ends with .pdf
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")
# =============================================================================
# 1. ATTRACTORS — Four strange attractors overlaid in the same visual space
#    Lorenz, Rossler, Chen, and Halvorsen systems — each with its own topology,
#    all fighting for the same canvas. Multiple trajectories per system.
#
#    Lorenz:    dx=sigma(y-x), dy=x(rho-z)-y, dz=xy-beta*z
#    Rossler:   dx=-y-z, dy=x+a*y, dz=b+z(x-c)
#    Chen:      dx=a(y-x), dy=(c-a)x-xz+cy, dz=xy-bz
#    Halvorsen: dx=-a*x-4y-4z-y^2, dy=-a*y-4z-4x-z^2, dz=-a*z-4x-4y-x^2
# =============================================================================
def _integrate_lorenz(x0, y0, z0, dt, n, sigma=10, rho=28, beta=8/3):
    xs, ys, zs = [x0], [y0], [z0]
    x, y, z = x0, y0, z0
    for _ in range(n):
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        x += dx; y += dy; z += dz
        xs.append(x); ys.append(y); zs.append(z)
    return np.array(xs), np.array(ys), np.array(zs)


def _integrate_rossler(x0, y0, z0, dt, n, a=0.2, b=0.2, c=5.7):
    xs, ys, zs = [x0], [y0], [z0]
    x, y, z = x0, y0, z0
    for _ in range(n):
        dx = (-y - z) * dt
        dy = (x + a * y) * dt
        dz = (b + z * (x - c)) * dt
        x += dx; y += dy; z += dz
        xs.append(x); ys.append(y); zs.append(z)
    return np.array(xs), np.array(ys), np.array(zs)


def _integrate_chen(x0, y0, z0, dt, n, a=35, b=3, c=28):
    xs, ys, zs = [x0], [y0], [z0]
    x, y, z = x0, y0, z0
    for _ in range(n):
        dx = (a * (y - x)) * dt
        dy = ((c - a) * x - x * z + c * y) * dt
        dz = (x * y - b * z) * dt
        x += dx; y += dy; z += dz
        xs.append(x); ys.append(y); zs.append(z)
    return np.array(xs), np.array(ys), np.array(zs)


def _integrate_halvorsen(x0, y0, z0, dt, n, a=1.89):
    xs, ys, zs = [x0], [y0], [z0]
    x, y, z = x0, y0, z0
    for _ in range(n):
        dx = (-a * x - 4 * y - 4 * z - y**2) * dt
        dy = (-a * y - 4 * z - 4 * x - z**2) * dt
        dz = (-a * z - 4 * x - 4 * y - x**2) * dt
        x += dx; y += dy; z += dz
        xs.append(x); ys.append(y); zs.append(z)
    return np.array(xs), np.array(ys), np.array(zs)


def _normalize_to_canvas(raw_x, raw_y, pad_frac=0.08):
    """Map arbitrary-range data to canvas drawing area."""
    xmin, xmax = raw_x.min(), raw_x.max()
    ymin, ymax = raw_y.min(), raw_y.max()
    xr = xmax - xmin if xmax != xmin else 1
    yr = ymax - ymin if ymax != ymin else 1
    nx = PAD_L + PW * (pad_frac + (1 - 2*pad_frac) * (raw_x - xmin) / xr)
    ny = PAD_B + PH * (pad_frac + (1 - 2*pad_frac) * (raw_y - ymin) / yr)
    return nx, ny

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


# =============================================================================
# 5. LEVY SWARM — 40 Levy flights from a central region
#    X_{n+1} = X_n + L_n * (cos(theta_n), sin(theta_n))
#    where L_n ~ Pareto(alpha) — heavy-tailed step lengths
#    Occasional massive jumps amid small diffusion. The flights scatter outward,
#    each leaving a filament trail of small steps punctuated by violent leaps.
# =============================================================================
def render():
    fig, ax = make_fig()
    np.random.seed(42)

    alpha_levy = 1.5  # Levy exponent (1 < alpha < 2 for heavy tails)

    # --- Multiple epicenters scattered across canvas ---
    # Each epicenter spawns flights that explore outward
    epicenters = [
        (cx,                cy),                 # center
        (PAD_L + PW * 0.18, PAD_B + PH * 0.75), # top-left
        (PAD_L + PW * 0.82, PAD_B + PH * 0.80), # top-right
        (PAD_L + PW * 0.25, PAD_B + PH * 0.25), # bottom-left
        (PAD_L + PW * 0.78, PAD_B + PH * 0.30), # bottom-right
        (PAD_L + PW * 0.50, PAD_B + PH * 0.85), # top-center
        (PAD_L + PW * 0.50, PAD_B + PH * 0.15), # bottom-center
        (PAD_L + PW * 0.12, PAD_B + PH * 0.50), # left
        (PAD_L + PW * 0.88, PAD_B + PH * 0.50), # right
    ]

    flights_per_epicenter = 8
    n_steps = 800

    for ei, (ex, ey) in enumerate(epicenters):
        for fi in range(flights_per_epicenter):
            # Start near this epicenter
            x_f = ex + np.random.uniform(-PW * 0.06, PW * 0.06)
            y_f = ey + np.random.uniform(-PH * 0.06, PH * 0.06)

            xs_path = [x_f]
            ys_path = [y_f]

            for step in range(n_steps):
                # Levy-distributed step length via inverse CDF of Pareto
                u = np.random.uniform(0.01, 1.0)
                step_len = 0.012 / (u ** (1.0 / alpha_levy))
                step_len = min(step_len, PW * 0.18)  # cap extreme jumps

                # Pure random direction — no radial bias so they explore freely
                angle = np.random.uniform(0, 2 * np.pi)

                x_f += step_len * np.cos(angle)
                y_f += step_len * np.sin(angle)
                xs_path.append(x_f)
                ys_path.append(y_f)

            xs_arr = np.array(xs_path)
            ys_arr = np.array(ys_path)

            mask = ((xs_arr > PAD_L) & (xs_arr < PAD_L + PW) &
                    (ys_arr > PAD_B) & (ys_arr < PAD_B + PH))

            gfi = ei * flights_per_epicenter + fi
            col = COLS[gfi % len(COLS)]

            for seg_xs, seg_ys in split_segments(xs_arr, ys_arr, mask):
                if len(seg_xs) < 3:
                    continue
                pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
                segs = np.concatenate([pts[:-1], pts[1:]], axis=1)

                # Compute step lengths for alpha/linewidth variation
                seg_dx = np.diff(seg_xs)
                seg_dy = np.diff(seg_ys)
                seg_lens = np.sqrt(seg_dx**2 + seg_dy**2)
                max_len = seg_lens.max() if seg_lens.max() > 0 else 1

                # Longer jumps = brighter and thicker
                alphas = 0.18 + 0.55 * (seg_lens / max_len)
                lws = 0.5 + 2.5 * (seg_lens / max_len)

                colors = [rgba(col, float(a)) for a in alphas]
                lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                       capstyle='round', zorder=3 + gfi % 6)
                ax.add_collection(lc)

    # --- Brownian micro-walks scattered across FULL canvas for texture ---
    np.random.seed(123)
    for mi in range(200):
        mx = PAD_L + np.random.uniform(0.02, 0.98) * PW
        my = PAD_B + np.random.uniform(0.02, 0.98) * PH
        micro_n = 100
        micro_xs = [mx]
        micro_ys = [my]
        for _ in range(micro_n):
            mx += np.random.randn() * 0.025
            my += np.random.randn() * 0.025
            micro_xs.append(mx)
            micro_ys.append(my)
        micro_xs = np.array(micro_xs)
        micro_ys = np.array(micro_ys)
        mask_m = ((micro_xs > PAD_L) & (micro_xs < PAD_L + PW) &
                  (micro_ys > PAD_B) & (micro_ys < PAD_B + PH))
        if mask_m.sum() < 3:
            continue
        col_m = COLS[mi % len(COLS)]
        for seg_xs, seg_ys in split_segments(micro_xs, micro_ys, mask_m):
            if len(seg_xs) < 3:
                continue
            draw_lc(ax, seg_xs, seg_ys, col_m, lw=0.25, alpha=0.12, zo=2)

    # --- Glow points at each epicenter ---
    for ex, ey in epicenters:
        for r_c, a in [(0.15, 0.03), (0.07, 0.08), (0.03, 0.20)]:
            ax.add_patch(Circle((ex, ey), radius=r_c,
                        facecolor=rgba("#FFFFFF", a), edgecolor='none', zorder=8))

    # Brighter center glow
    for r_c, a in [(0.30, 0.04), (0.15, 0.10), (0.06, 0.25), (0.025, 0.55)]:
        ax.add_patch(Circle((cx, cy), radius=r_c,
                    facecolor=rgba("#FFFFFF", a), edgecolor='none', zorder=9))

    label(ax,
          "L ~ x\u207b\u1d45 (Pareto),  X\u2099\u208a\u2081=X\u2099+L\u2099\u00b7e^{i\u03b8}")
    save(fig, "overwhelm_levy_swarm.pdf")


# =============================================================================
# Main
# =============================================================================


if __name__ == '__main__':
    render()
