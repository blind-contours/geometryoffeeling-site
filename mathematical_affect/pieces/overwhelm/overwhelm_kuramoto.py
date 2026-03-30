"""
Geometry of Feeling — Overwhelm: Overwhelm Kuramoto
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
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
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
# 3. KURAMOTO — Coupled oscillators at the edge of synchronization
#    d(theta_i)/dt = omega_i + (K/N) * sum_j sin(theta_j - theta_i)
#    Each oscillator drawn as a time-series curve. At critical coupling K_c,
#    some oscillators lock while others drift — maximum complexity.
#    60 oscillators, each a vivid trace across the canvas.
# =============================================================================
def render():
    fig, ax = make_fig()
    np.random.seed(271)

    N_osc = 60
    # Natural frequencies: drawn from a Lorentzian (Cauchy) distribution
    # centered at 0 with spread gamma_dist
    gamma_dist = 1.0
    omega = gamma_dist * np.tan(np.pi * (np.random.uniform(0, 1, N_osc) - 0.5))
    omega = np.clip(omega, -5, 5)  # prevent extreme outliers

    # Critical coupling for Lorentzian: K_c = 2 * gamma_dist
    # Set K slightly above K_c for partial synchronization (maximum overwhelm)
    K = 2.2 * gamma_dist

    # Initial phases: random
    theta = np.random.uniform(0, 2 * np.pi, N_osc)

    # Time integration
    dt_k = 0.02
    n_steps = 2000
    time_arr = np.arange(n_steps) * dt_k
    theta_history = np.zeros((N_osc, n_steps))

    for step in range(n_steps):
        theta_history[:, step] = theta
        # Kuramoto coupling
        sin_diff = np.sin(theta[np.newaxis, :] - theta[:, np.newaxis])
        coupling = (K / N_osc) * np.sum(sin_diff, axis=1)
        dtheta = (omega + coupling) * dt_k
        theta = theta + dtheta

    # Draw each oscillator as a curve: x = time, y = theta (mod 2pi) mapped
    # to vertical position, with vertical offset per oscillator for layering
    xs_base = PAD_L + PW * np.linspace(0, 1, n_steps)

    for i in range(N_osc):
        # Unwrap phase and normalize to canvas height
        phase = theta_history[i, :]
        # Use sin(phase) to create an oscillating curve, offset vertically
        base_y = PAD_B + PH * (0.02 + 0.96 * i / (N_osc - 1))
        amp = PH * 0.012  # small amplitude per oscillator
        ys_curve = base_y + amp * np.sin(phase)

        # Also add a faint wider version showing the raw phase drift
        phase_unwrap = np.unwrap(phase)
        phase_norm = (phase_unwrap - phase_unwrap.min())
        if phase_norm.max() > 0:
            phase_norm = phase_norm / phase_norm.max()
        # subtle lateral wobble from the phase
        xs_curve = xs_base + PW * 0.008 * np.sin(phase * 3)

        col = COLS[i % len(COLS)]

        # Primary curve: the oscillating trace
        mask = ((xs_curve > PAD_L) & (xs_curve < PAD_L + PW) &
                (ys_curve > PAD_B) & (ys_curve < PAD_B + PH))
        for seg_xs, seg_ys in split_segments(xs_curve, ys_curve, mask):
            if len(seg_xs) < 3:
                continue
            pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            n_s = len(segs)
            # Faster oscillators get brighter (more demanding)
            base_alpha = 0.34 + 0.60 * min(1.0, abs(omega[i]) / 3.0)
            alphas = np.full(n_s, base_alpha)
            lc = mc.LineCollection(segs, linewidths=1.12,
                                   colors=[rgba(col, float(a)) for a in alphas],
                                   capstyle='round', zorder=3 + i % 5)
            ax.add_collection(lc)

        # Secondary: a ghost trace of the running phase for texture
        # map phase modulo to a vertical oscillation around base
        ys_ghost = base_y + amp * 2.5 * np.sin(phase * 0.5)
        mask2 = ((xs_base > PAD_L) & (xs_base < PAD_L + PW) &
                 (ys_ghost > PAD_B) & (ys_ghost < PAD_B + PH))
        for seg_xs, seg_ys in split_segments(xs_base, ys_ghost, mask2):
            if len(seg_xs) < 3:
                continue
            draw_lc(ax, seg_xs, seg_ys, col, lw=0.42, alpha=0.14, zo=2)

    add_signature(fig, ax, BG)
    save(fig, "overwhelm_kuramoto.pdf")

if __name__ == '__main__':
    render()
