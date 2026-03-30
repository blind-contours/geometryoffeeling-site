"""
Geometry of Feeling — Tension: Tension Opposition
Standalone render script
"""

import numpy as np
import matplotlib
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

def label(ax, eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(1,1,1,0.20),transform=ax.transData)
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
    Y_MIN = PAD_B + 0.02
    Y_MAX = PAD_B + PH - 0.02
    X_MIN = PAD_L
    X_MAX = PAD_L + PW

    # Rossler attractor parameters
    a, b, c = 0.2, 0.2, 5.7
    dt = 0.008
    n_steps = 25000

    def integrate_rossler(x0, y0, z0):
        """Integrate Rossler system using RK4."""
        xs, ys, zs = [x0], [y0], [z0]
        x, y, z = x0, y0, z0
        for _ in range(n_steps):
            # RK4
            def f(x, y, z):
                return (-(y + z), x + a * y, b + z * (x - c))
            k1 = f(x, y, z)
            k2 = f(x + dt/2*k1[0], y + dt/2*k1[1], z + dt/2*k1[2])
            k3 = f(x + dt/2*k2[0], y + dt/2*k2[1], z + dt/2*k2[2])
            k4 = f(x + dt*k3[0], y + dt*k3[1], z + dt*k3[2])
            x += dt/6 * (k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
            y += dt/6 * (k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
            z += dt/6 * (k1[2] + 2*k2[2] + 2*k3[2] + k4[2])
            xs.append(x); ys.append(y); zs.append(z)
        return np.array(xs), np.array(ys), np.array(zs)

    # Two trajectories from slightly different initial conditions
    rx1, ry1, rz1 = integrate_rossler(1.0, 1.0, 1.0)
    rx2, ry2, rz2 = integrate_rossler(1.01, 1.0, 1.0)

    # Project to 2D: use (x, y) plane of Rossler
    # Scale and center — attractor 1 on left, attractor 2 mirrored on right
    def scale_to_canvas(rx, ry, center_x, flip_x=False):
        """Map attractor coordinates to canvas region."""
        rx_min, rx_max = rx.min(), rx.max()
        ry_min, ry_max = ry.min(), ry.max()
        # Normalize to [0, 1]
        nx = (rx - rx_min) / (rx_max - rx_min + 1e-12)
        ny = (ry - ry_min) / (ry_max - ry_min + 1e-12)
        if flip_x:
            nx = 1.0 - nx
        # Scale to half canvas
        half_w = PW * 0.42
        half_h = PH * 0.88
        px = center_x + (nx - 0.5) * half_w
        py = cy + (ny - 0.5) * half_h
        return px, py

    # Attractor 1: left side
    px1, py1 = scale_to_canvas(rx1, ry1, cx - PW * 0.25, flip_x=False)
    # Attractor 2: right side, mirrored
    px2, py2 = scale_to_canvas(rx2, ry2, cx + PW * 0.25, flip_x=True)

    # --- Draw attractors with evolving color ---
    acid_rgb = hex_to_rgb(ACID)
    elec_rgb = hex_to_rgb(ELECTRIC)
    hot_rgb  = hex_to_rgb(HOT)
    orange_rgb = hex_to_rgb(ORANGE)

    def draw_attractor(px, py, base_rgb, stress_rgb, zo, alpha_base=0.55):
        """Draw attractor as color-evolving line collection."""
        mask = ((px >= X_MIN) & (px <= X_MAX) &
                (py >= Y_MIN) & (py <= Y_MAX))
        segments = split_segments(px, py, mask)
        for sx, sy in segments:
            n = len(sx)
            if n < 3:
                continue
            pts = np.array([sx, sy]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            colors = []
            lws = []
            for i in range(n - 1):
                t = i / max(n - 2, 1)
                # Pulsing alpha — tension breathing
                pulse = 0.5 + 0.5 * np.sin(t * 12 * np.pi)
                r = base_rgb[0] * (1 - pulse*0.4) + stress_rgb[0] * pulse * 0.4
                g = base_rgb[1] * (1 - pulse*0.4) + stress_rgb[1] * pulse * 0.4
                b_c = base_rgb[2] * (1 - pulse*0.4) + stress_rgb[2] * pulse * 0.4
                a = alpha_base * (0.6 + 0.4 * pulse)
                colors.append((r, g, b_c, float(np.clip(a, 0, 1))))
                lws.append(0.6 + 0.8 * pulse)
            lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                   capstyle='round', zorder=zo)
            ax.add_collection(lc)

    draw_attractor(px1, py1, acid_rgb, hot_rgb, zo=4, alpha_base=0.50)
    draw_attractor(px2, py2, elec_rgb, orange_rgb, zo=5, alpha_base=0.50)

    # --- Tension filaments between the two attractors ---
    # Sample corresponding points and draw taut lines between them
    n_filaments = 60
    np.random.seed(77)
    step = n_steps // n_filaments
    for i in range(n_filaments):
        idx = i * step + np.random.randint(0, step // 2)
        if idx >= len(px1):
            continue
        x1, y1 = px1[idx], py1[idx]
        x2, y2 = px2[idx], py2[idx]
        # Check bounds
        if not (X_MIN <= x1 <= X_MAX and X_MIN <= x2 <= X_MAX and
                Y_MIN <= y1 <= Y_MAX and Y_MIN <= y2 <= Y_MAX):
            continue
        # Draw as slightly curved taut line (catenary sag under tension)
        t_fil = np.linspace(0, 1, 50)
        fx = x1 + (x2 - x1) * t_fil
        # Tiny sag in the middle — barely perceptible, like a taut string
        sag = -0.08 * np.sin(np.pi * t_fil)
        fy = y1 + (y2 - y1) * t_fil + sag

        mask_f = (fy >= Y_MIN) & (fy <= Y_MAX) & (fx >= X_MIN) & (fx <= X_MAX)
        segs_f = split_segments(fx, fy, mask_f)
        # Distance determines tension color
        dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        max_dist = PW * 0.7
        tension = np.clip(dist / max_dist, 0, 1)
        for sx, sy in segs_f:
            n_s = len(sx)
            if n_s < 3:
                continue
            pts_f = np.array([sx, sy]).T.reshape(-1, 1, 2)
            segs_fc = np.concatenate([pts_f[:-1], pts_f[1:]], axis=1)
            # Alpha peaks in middle, fades at ends
            alphas = 0.08 + 0.15 * tension * np.sin(np.pi * np.linspace(0, 1, n_s - 1))
            cols_f = []
            for j in range(n_s - 1):
                t_j = j / max(n_s - 2, 1)
                mid_t = 1.0 - abs(2 * t_j - 1)  # peaks at center
                r = acid_rgb[0] * (1 - tension) + hot_rgb[0] * tension
                g = acid_rgb[1] * (1 - tension) + hot_rgb[1] * tension
                b = acid_rgb[2] * (1 - tension) + hot_rgb[2] * tension
                cols_f.append((r, g, b, float(np.clip(alphas[j], 0, 0.25))))
            lc_f = mc.LineCollection(segs_fc, linewidths=0.4 + 0.3 * tension,
                                     colors=cols_f, capstyle='round', zorder=3)
            ax.add_collection(lc_f)

    # --- Central void emphasis: faint vertical line marking the tension axis ---
    ax.plot([cx, cx], [Y_MIN + 0.3, Y_MAX - 0.3],
            color=rgba(RED, 0.18), linewidth=0.6, linestyle='-', zorder=2)

    label(ax, "dx/dt = \u2212(y+z),  dy/dt = x+ay,  dz/dt = b+z(x\u2212c)")
    save(fig, "tension_opposition.pdf")


if __name__ == '__main__':
    render()
