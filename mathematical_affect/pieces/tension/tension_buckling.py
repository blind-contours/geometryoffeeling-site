"""
Geometry of Feeling — Tension: Tension Buckling
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

    N = 2000
    # Column runs vertically — x_param goes from bottom to top
    x_param = np.linspace(0, 1, N)
    # Map to vertical canvas position
    y_pos = PAD_B + PH * 0.05 + PH * 0.90 * x_param

    n_modes = 8
    acid_rgb = hex_to_rgb(ACID)
    hot_rgb  = hex_to_rgb(HOT)
    red_rgb  = hex_to_rgb(RED)
    orange_rgb = hex_to_rgb(ORANGE)
    elec_rgb = hex_to_rgb(ELECTRIC)

    # --- Draw the original straight column (ghost) ---
    ax.plot([cx, cx], [y_pos[0], y_pos[-1]],
            color=rgba(DIM, 0.15), linewidth=1.0, linestyle='--', zorder=2)

    # --- Buckling modes ---
    for mode_n in range(1, n_modes + 1):
        # Amplitude increases with mode number (more load = more deflection)
        # But also: higher modes have smaller amplitude per hump
        base_amp = PW * 0.06
        # Supercritical amplitude: grows with sqrt of (P/Pcr - 1)
        # Simulate increasing load fraction
        load_frac = 0.3 + 0.7 * (mode_n / n_modes)  # near critical for all
        amp = base_amp * (1.5 + 0.8 * mode_n**0.5) * load_frac

        # y(x) = A * sin(n * pi * x / L) — buckling deflection
        deflection = amp * np.sin(mode_n * np.pi * x_param)

        # Horizontal position = center + deflection
        x_pos = cx + deflection

        # Color: low modes are acid (stable), high modes are hot/red (critical)
        t_mode = (mode_n - 1) / max(n_modes - 1, 1)

        # Clip to canvas
        mask = ((x_pos >= PAD_L) & (x_pos <= PAD_L + PW) &
                (y_pos >= Y_MIN) & (y_pos <= Y_MAX))
        segments = split_segments(x_pos, y_pos, mask)

        for sx, sy in segments:
            n_s = len(sx)
            if n_s < 3:
                continue
            pts = np.array([sx, sy]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            colors = []
            lws = []
            for i in range(n_s - 1):
                t_local = i / max(n_s - 2, 1)
                # Color from acid to hot to red with mode number
                if t_mode < 0.5:
                    t2 = t_mode * 2
                    r = acid_rgb[0] * (1 - t2) + orange_rgb[0] * t2
                    g = acid_rgb[1] * (1 - t2) + orange_rgb[1] * t2
                    b = acid_rgb[2] * (1 - t2) + orange_rgb[2] * t2
                else:
                    t2 = (t_mode - 0.5) * 2
                    r = orange_rgb[0] * (1 - t2) + red_rgb[0] * t2
                    g = orange_rgb[1] * (1 - t2) + red_rgb[1] * t2
                    b = orange_rgb[2] * (1 - t2) + red_rgb[2] * t2
                # Alpha: stronger at antinodes (max deflection)
                local_defl = abs(np.sin(mode_n * np.pi * x_param[int(t_local * (N-1))]))
                a = 0.35 + 0.55 * local_defl * (0.5 + 0.5 * t_mode)
                colors.append((r, g, b, float(np.clip(a, 0, 1))))
                lws.append(1.0 + 1.5 * t_mode + 0.5 * local_defl)
            lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                   capstyle='round', zorder=3 + mode_n)
            ax.add_collection(lc)

        # --- Stress concentration markers at antinodes ---
        for k in range(1, mode_n + 1):
            # Antinodes at x = (2k-1)/(2n) for mode n
            x_anti = (2 * k - 1) / (2 * mode_n)
            if 0 < x_anti < 1:
                idx = int(x_anti * (N - 1))
                px_anti = cx + deflection[idx]
                py_anti = y_pos[idx]
                if PAD_L <= px_anti <= PAD_L + PW and Y_MIN <= py_anti <= Y_MAX:
                    # Small stress glow
                    circle = Circle((px_anti, py_anti), 0.06 + 0.03 * t_mode,
                                    facecolor=rgba(HOT if t_mode > 0.5 else ACID, 0.15 + 0.15 * t_mode),
                                    edgecolor='none', zorder=2)
                    ax.add_patch(circle)

    # --- Fixed support markers at top and bottom ---
    for y_end in [y_pos[0], y_pos[-1]]:
        ax.plot([cx - PW*0.04, cx + PW*0.04], [y_end, y_end],
                color=rgba(DIM, 0.50), linewidth=2.5, solid_capstyle='butt', zorder=12)
        # Hatching for fixed support
        for dx in np.linspace(-PW*0.04, PW*0.04, 8):
            if y_end < cy:
                ax.plot([cx + dx, cx + dx - 0.05], [y_end, y_end - 0.12],
                        color=rgba(DIM, 0.30), linewidth=0.6, zorder=11)
            else:
                ax.plot([cx + dx, cx + dx - 0.05], [y_end, y_end + 0.12],
                        color=rgba(DIM, 0.30), linewidth=0.6, zorder=11)

    # --- Load arrows at top ---
    arrow_y = y_pos[-1] + 0.02
    for dx_arr in [-0.15, 0, 0.15]:
        ax.annotate('', xy=(cx + dx_arr, y_pos[-1]),
                    xytext=(cx + dx_arr, min(arrow_y + 0.4, Y_MAX)),
                    arrowprops=dict(arrowstyle='->', color=rgba(RED, 0.50),
                                    lw=1.2), zorder=12)

    label(ax, "y(x) = A\u00b7sin(n\u03c0x/L),  P_cr = n\u00b2\u03c0\u00b2EI/L\u00b2")
    save(fig, "tension_buckling.pdf")


if __name__ == '__main__':
    render()
