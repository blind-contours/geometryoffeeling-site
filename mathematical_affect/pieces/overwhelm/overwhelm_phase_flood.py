"""
Geometry of Feeling — Overwhelm: Overwhelm Phase Flood
Standalone render script
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
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"  saved {name}")

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


def render():
    fig, ax = make_fig()
    np.random.seed(314)

    # Driven damped pendulum parameters (chosen for mixed regular/chaotic behavior)
    gamma_damp = 0.2
    F_drive = 1.2       # moderate driving — mix of chaos and periodicity
    omega_d = 0.6667    # driving frequency (2/3 natural)

    n_traj = 80
    n_steps = 8000
    dt_p = 0.015

    # First pass: collect all data to find bounds
    all_theta = []
    all_omega_vals = []
    traj_data = []

    for i in range(n_traj):
        theta = np.random.uniform(-np.pi, np.pi)
        omega_v = np.random.uniform(-3.0, 3.0)
        thetas = []
        omegas = []

        for step in range(n_steps):
            # Driven damped pendulum equations
            alpha_acc = (-gamma_damp * omega_v - np.sin(theta)
                         + F_drive * np.cos(omega_d * step * dt_p))
            omega_v += alpha_acc * dt_p
            theta += omega_v * dt_p
            # Keep theta in [-4pi, 4pi] range for extended phase space
            if theta > 4 * np.pi:
                theta -= 2 * np.pi
            elif theta < -4 * np.pi:
                theta += 2 * np.pi
            thetas.append(theta)
            omegas.append(omega_v)

        thetas = np.array(thetas)
        omegas = np.array(omegas)
        all_theta.extend(thetas)
        all_omega_vals.extend(omegas)
        traj_data.append((thetas, omegas))

    all_theta = np.array(all_theta)
    all_omega_vals = np.array(all_omega_vals)

    # Compute bounds using percentiles to avoid extreme outliers
    th_lo, th_hi = np.percentile(all_theta, 1), np.percentile(all_theta, 99)
    om_lo, om_hi = np.percentile(all_omega_vals, 1), np.percentile(all_omega_vals, 99)
    th_range = th_hi - th_lo if th_hi != th_lo else 1
    om_range = om_hi - om_lo if om_hi != om_lo else 1

    # Draw each trajectory — use chunked gradient (fewer unique colors)
    for i, (thetas, omegas) in enumerate(traj_data):
        # Map to canvas coordinates
        nx = PAD_L + PW * (0.03 + 0.94 * (thetas - th_lo) / th_range)
        ny = PAD_B + PH * (0.03 + 0.94 * (omegas - om_lo) / om_range)

        mask = ((nx > PAD_L) & (nx < PAD_L + PW) &
                (ny > PAD_B) & (ny < PAD_B + PH))

        col = COLS[i % len(COLS)]

        for seg_xs, seg_ys in split_segments(nx, ny, mask):
            if len(seg_xs) < 3:
                continue
            # Draw in chunks with stepped alpha for PDF efficiency
            n_chunks = 6
            chunk_size = max(1, len(seg_xs) // n_chunks)
            for ci in range(n_chunks):
                s = ci * chunk_size
                e = min((ci + 1) * chunk_size + 1, len(seg_xs))
                if e - s < 2:
                    continue
                frac = ci / max(1, n_chunks - 1)
                alpha_c = 0.55 - 0.40 * frac
                lw_c = 1.0 - 0.55 * frac
                draw_lc(ax, seg_xs[s:e], seg_ys[s:e], col,
                        lw=max(0.25, lw_c), alpha=max(0.06, alpha_c),
                        zo=3 + i % 6)

    # Faint separatrix hints: the undriven pendulum's separatrix
    theta_sep = np.linspace(-np.pi * 1.5, np.pi * 1.5, 2000)
    omega_sep_upper = 2 * np.cos(theta_sep / 2)
    omega_sep_lower = -2 * np.cos(theta_sep / 2)
    for omega_sep in [omega_sep_upper, omega_sep_lower]:
        nx_s = PAD_L + PW * (0.03 + 0.94 * (theta_sep - th_lo) / th_range)
        ny_s = PAD_B + PH * (0.03 + 0.94 * (omega_sep - om_lo) / om_range)
        mask_s = ((nx_s > PAD_L) & (nx_s < PAD_L + PW) &
                  (ny_s > PAD_B) & (ny_s < PAD_B + PH))
        for seg_xs, seg_ys in split_segments(nx_s, ny_s, mask_s):
            if len(seg_xs) < 3:
                continue
            draw_lc(ax, seg_xs, seg_ys, "#FFFFFF", lw=0.4, alpha=0.06, zo=2)

    label(ax,
          "\u03b8'' + \u03b3\u03b8' + sin(\u03b8) = F\u00b7cos(\u03c9t)")
    save(fig, "overwhelm_phase_flood.pdf")


if __name__ == '__main__':
    render()
