"""
Geometry of Feeling — Desire: Desire Magnetism
Standalone render script
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
from matplotlib.patches import Circle
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#E8D8D0"

CRIMSON   = "#9A2030"; HEATED  = "#C88030"; BURGUNDY = "#6A2038"
DARKROSE  = "#8A3848"; FLAME   = "#D06020"; WINE     = "#5A1828"
PULSE_COL = "#B83040"; SMOLDER = "#7A4028"; GILT     = "#C4A040"
EMBER     = "#C05030"; SCARLET = "#D02838"

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2; cy = PAD_B + PH / 2

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    return fig, ax

def label(ax, eq):
    ax.text(0.75, 0.75, eq, fontfamily='monospace', fontsize=10,
            color=(0.55, 0.40, 0.35, 0.40), transform=ax.transData)

def split_segments(xs, ys, mask):
    segments = []; in_seg = False; start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg: start = j; in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3: segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3: segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if smooth > 0: ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def glow(ax, x, y, col, r_max=0.20):
    for r, a in [(r_max, 0.06), (r_max*0.6, 0.12), (r_max*0.3, 0.25), (r_max*0.12, 0.45)]:
        ax.add_patch(Circle((x, y), radius=r, facecolor=rgba(col, a),
                     edgecolor='none', zorder=6))

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def render():
    """The Sealed Chamber — all field lines trapped inside an elliptical boundary.
    Desire contained by skin, by social surface. Lines crowd and intensify
    near the wall. Beautiful from across a room, claustrophobic up close."""
    fig, ax = make_fig()
    np.random.seed(33)

    # Elliptical boundary — the seal
    a_ell = PW * 0.38   # horizontal semi-axis
    b_ell = PH * 0.42   # vertical semi-axis

    # Draw the boundary — fine, precise, burgundy
    theta_b = np.linspace(0, 2 * np.pi, 1000)
    bx = cx + a_ell * np.cos(theta_b)
    by = cy + b_ell * np.sin(theta_b)
    ax.plot(bx, by, color=rgba(BURGUNDY, 0.55), lw=1.5, zorder=8)
    # Faint outer glow of the boundary
    for dr, da in [(0.06, 0.08), (0.12, 0.04), (0.20, 0.02)]:
        bx_g = cx + (a_ell + dr) * np.cos(theta_b)
        by_g = cy + (b_ell + dr) * np.sin(theta_b)
        ax.plot(bx_g, by_g, color=rgba(DARKROSE, da), lw=0.6, zorder=7)

    # Two poles inside the ellipse
    pole_sep = a_ell * 0.55
    p1x, p1y = cx - pole_sep, cy
    p2x, p2y = cx + pole_sep, cy

    # Trace field lines from pole 1 — stop at ellipse boundary
    def inside_ellipse(x, y):
        return ((x - cx) / a_ell)**2 + ((y - cy) / b_ell)**2 < 1.0

    def dist_to_boundary(x, y):
        """Approximate distance to ellipse boundary."""
        r_ell = np.sqrt(((x - cx) / a_ell)**2 + ((y - cy) / b_ell)**2)
        if r_ell < 0.001: return min(a_ell, b_ell)
        angle = np.arctan2((y - cy) / b_ell, (x - cx) / a_ell)
        bnd_x = cx + a_ell * np.cos(angle)
        bnd_y = cy + b_ell * np.sin(angle)
        return np.sqrt((x - bnd_x)**2 + (y - bnd_y)**2) * (1 - r_ell) / max(0.001, 1 - r_ell)

    def trace_field(x0, y0, sink_px, sink_py, step=0.015, max_steps=1500, direction=1):
        """Trace dipole field line, stop at ellipse boundary or sink pole."""
        xs_f, ys_f = [x0], [y0]
        x, y = x0, y0
        for _ in range(max_steps):
            # Dipole field from two monopoles
            bx_f, by_f = 0.0, 0.0
            for px, py, charge in [(p1x, p1y, 1.0), (p2x, p2y, -1.0)]:
                ddx, ddy = x - px, y - py
                r = np.sqrt(ddx**2 + ddy**2) + 0.08
                bx_f += charge * ddx / r**3
                by_f += charge * ddy / r**3
            bmag = np.sqrt(bx_f**2 + by_f**2) + 1e-12
            x += direction * step * bx_f / bmag
            y += direction * step * by_f / bmag
            if not inside_ellipse(x, y):
                break
            xs_f.append(x); ys_f.append(y)
            # Stop at sink pole
            if np.sqrt((x - sink_px)**2 + (y - sink_py)**2) < 0.12:
                break
        return np.array(xs_f), np.array(ys_f)

    def draw_field_lines(ax, source_px, source_py, sink_px, sink_py, direction=1):
        """Fan field lines from a source pole toward the sink pole."""
        n_lines = 36
        cols = [CRIMSON, SCARLET, EMBER, FLAME, HEATED, DARKROSE,
                BURGUNDY, WINE, CRIMSON, SCARLET]
        for i in range(n_lines):
            angle = -np.pi * 0.95 + i * (2 * np.pi * 0.95) / (n_lines - 1)
            start_r = 0.12
            x0 = source_px + start_r * np.cos(angle)
            y0 = source_py + start_r * np.sin(angle)
            if not inside_ellipse(x0, y0):
                continue

            xs_f, ys_f = trace_field(x0, y0, sink_px, sink_py, direction=direction)
            if len(xs_f) < 10:
                continue

            # Calculate distance to boundary for each point — intensity increases near wall
            n_pts = len(xs_f)
            boundary_prox = np.zeros(n_pts)
            for j in range(n_pts):
                r_ell = np.sqrt(((xs_f[j] - cx) / a_ell)**2 + ((ys_f[j] - cy) / b_ell)**2)
                boundary_prox[j] = r_ell  # 0 at center, ~1 at boundary

            col = cols[i % len(cols)]
            # Lines get thicker and brighter near the boundary (pressure building)
            alpha_base = 0.20
            lw_base = 0.5
            alphas = alpha_base + 0.55 * boundary_prox**2
            lws = lw_base + 1.8 * boundary_prox**2
            alphas = np.clip(alphas, 0, 0.85)

            pts = np.array([xs_f, ys_f]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            colors_seg = [rgba(col, float(a)) for a in alphas[:-1]]
            lc = mc.LineCollection(segs, linewidths=lws[:-1], colors=colors_seg,
                                   capstyle='round', joinstyle='round', zorder=4)
            ax.add_collection(lc)

    # Fan field lines from both poles — symmetric
    draw_field_lines(ax, p1x, p1y, p2x, p2y, direction=1)   # left pole → right
    draw_field_lines(ax, p2x, p2y, p1x, p1y, direction=-1)   # right pole → left

    # Pole glows inside the chamber
    glow(ax, p1x, p1y, CRIMSON, 0.18)
    glow(ax, p2x, p2y, DARKROSE, 0.14)

    label(ax, "\u2207\u00b7B=0, \u222eB\u00b7dl=\u03bc\u2080I")
    save(fig, "desire_magnetism")


if __name__ == '__main__':
    render()
