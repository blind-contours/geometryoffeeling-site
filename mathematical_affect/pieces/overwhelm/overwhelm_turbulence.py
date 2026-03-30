"""
Geometry of Feeling — Overwhelm: Overwhelm Turbulence
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
    np.random.seed(137)

    # Generate random vortex field
    n_vortices = 60
    vort_x = PAD_L + PW * np.random.uniform(0.0, 1.0, n_vortices)
    vort_y = PAD_B + PH * np.random.uniform(0.0, 1.0, n_vortices)
    # circulation strengths: mix of positive and negative
    gamma = np.random.uniform(-1.5, 1.5, n_vortices)
    # regularization radius to avoid singularity
    eps = 0.15

    def velocity(px, py):
        """Compute velocity at point (px, py) from vortex superposition + shear."""
        u = 0.08  # base shear flow (rightward)
        v = 0.0
        for k in range(n_vortices):
            dx = px - vort_x[k]
            dy = py - vort_y[k]
            r2 = dx**2 + dy**2 + eps**2
            u += gamma[k] / (2 * np.pi) * dy / r2
            v -= gamma[k] / (2 * np.pi) * dx / r2
        return u, v

    # Trace many streamlines
    n_streams = 200
    stream_starts_x = PAD_L + PW * np.random.uniform(-0.1, 1.1, n_streams)
    stream_starts_y = PAD_B + PH * np.random.uniform(-0.1, 1.1, n_streams)

    for si in range(n_streams):
        x_s, y_s = stream_starts_x[si], stream_starts_y[si]
        n_steps = 600
        dt_s = 0.04
        xs_path = [x_s]
        ys_path = [y_s]
        for _ in range(n_steps):
            u, v = velocity(x_s, y_s)
            speed = np.sqrt(u**2 + v**2)
            if speed > 0:
                # normalize to constant step length for visual consistency
                u_n = u / speed * dt_s
                v_n = v / speed * dt_s
            else:
                break
            x_s += u_n
            y_s += v_n
            xs_path.append(x_s)
            ys_path.append(y_s)
            # stop if far outside canvas
            if (x_s < PAD_L - 1 or x_s > PAD_L + PW + 1 or
                    y_s < PAD_B - 1 or y_s > PAD_B + PH + 1):
                break

        xs_arr = np.array(xs_path)
        ys_arr = np.array(ys_path)
        if len(xs_arr) < 5:
            continue

        mask = ((xs_arr > PAD_L) & (xs_arr < PAD_L + PW) &
                (ys_arr > PAD_B) & (ys_arr < PAD_B + PH))

        col = COLS[si % len(COLS)]
        for seg_xs, seg_ys in split_segments(xs_arr, ys_arr, mask):
            if len(seg_xs) < 3:
                continue
            pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            n_s = len(segs)
            alphas = np.linspace(0.55, 0.08, n_s)
            lws = np.linspace(1.4, 0.3, n_s)
            colors = [rgba(col, float(a)) for a in alphas]
            lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                   capstyle='round', zorder=3 + si % 5)
            ax.add_collection(lc)

    # Faint vortex center markers (barely visible)
    for k in range(n_vortices):
        if (PAD_L < vort_x[k] < PAD_L + PW and
                PAD_B < vort_y[k] < PAD_B + PH):
            r_dot = 0.03 + 0.02 * abs(gamma[k])
            ax.add_patch(Circle((vort_x[k], vort_y[k]), radius=r_dot,
                        facecolor=rgba("#FFFFFF", 0.04), edgecolor='none',
                        zorder=2))

    label(ax,
          "u=U+\u03a3 \u0393\u2096(y\u2212y\u2096)/r\u00b2,  "
          "v=\u2212\u03a3 \u0393\u2096(x\u2212x\u2096)/r\u00b2")
    save(fig, "overwhelm_turbulence.pdf")


if __name__ == '__main__':
    render()
