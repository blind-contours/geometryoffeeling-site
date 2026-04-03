"""
Geometry of Feeling — Growth: Strata
Thirty-five parabolic arcs radiating from a molten core — yellow
radiance at the center decaying through earth tones (amber, bronze,
olive) into greens and teal. Asymmetric frequency-ramped ripples
on both sides; left: fewer bold waves, right: more frequent.
  height(n) = 0.1 + H·(n/N)^1.3,  color(n) = palette[(n/N)^0.65]
"""

import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon, Rectangle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
PRINT_DIR = os.path.join(SCRIPT_DIR, '..', '..', '..', 'public', 'prints', 'growth')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#F5F0E6'

# Full journey: hot yellow → amber → earth brown → olive → green → forest → teal
PALETTE = [
    '#F5E060',  # bright yellow (molten core)
    '#F0D050',  # warm yellow
    '#EABC38',  # yellow-gold
    '#E0A830',  # deep gold
    '#D49428',  # rich amber
    '#C48428',  # dark amber
    '#AA7828',  # bronze earth
    '#8E7430',  # warm brown-olive
    '#748234',  # olive
    '#5A8A3A',  # olive-green
    '#3E8B44',  # green
    '#2E8B4A',  # forest green (growth palette)
    '#1A6A4A',  # deep green
    '#1A5A5A',  # green-teal
    '#1A4D6E',  # teal-blue (growth palette end)
]

# Art region defined by equal margins
MARGIN = 0.65
ART_L = MARGIN
ART_R = FIG_W - MARGIN
ART_B = MARGIN
ART_T = FIG_H - MARGIN
ART_W = ART_R - ART_L
ART_H = ART_T - ART_B
ART_CX = (ART_L + ART_R) / 2


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def interp_color(pal, u):
    rgbs = [np.array(hex_to_rgb(c)) for c in pal]
    u = np.clip(u, 0.0, 1.0)
    if u >= 1.0: return tuple(rgbs[-1])
    if u <= 0.0: return tuple(rgbs[0])
    pos = u * (len(rgbs) - 1)
    i = int(pos)
    f = pos - i
    return tuple((1 - f) * rgbs[i] + f * rgbs[min(i + 1, len(rgbs) - 1)])

BG_RGB = np.array(hex_to_rgb(BG_COLOR))

def interp_rgba(pal, u, a):
    """Return color with real alpha (for fill bands that need transparency)."""
    r, g, b = interp_color(pal, u)
    return (r, g, b, float(np.clip(a, 0, 1)))

def interp_opaque(pal, u, a):
    """Blend color with background — fully opaque, no compositing dots."""
    r, g, b = interp_color(pal, u)
    col = np.array([r, g, b])
    a = float(np.clip(a, 0, 1))
    blended = a * col + (1 - a) * BG_RGB
    return (blended[0], blended[1], blended[2], 1.0)

def lc_from_xy(xs, ys, colors, widths, zo=4):
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    return LineCollection(segs, colors=colors, linewidths=widths,
                          capstyle='round', joinstyle='round', zorder=zo)

def add_mat(ax):
    """Draw margin-colored rectangles ON TOP of the art like a physical mat."""
    zo = 50
    ax.add_patch(Rectangle((0, 0), FIG_W, ART_B,
                           facecolor=BG_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, ART_T), FIG_W, MARGIN,
                           facecolor=BG_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, 0), ART_L, FIG_H,
                           facecolor=BG_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((ART_R, 0), MARGIN, FIG_H,
                           facecolor=BG_COLOR, edgecolor='none', zorder=zo))


def asym_freq_ramp(t, frac, height):
    """Deep sharp ripples on both sides. Left: fewer, bold. Right: more frequent.
    Left side taper reduced so ripples stay sharp to the edge."""
    t_norm = (t + 1) / 2
    wave_amp = 0.105 * (frac ** 2.1) * height
    freq_local = 8.0 + 4 * t_norm
    phase = np.cumsum(freq_local * np.pi / len(t) * 2)
    wave = wave_amp * np.sin(phase)
    taper_left = 1 - np.clip(-t, 0, 1) ** 4.5
    taper_right = 1 - np.clip(t, 0, 1) ** 3
    taper = np.where(t < 0, taper_left, taper_right)
    return wave, taper


def draw_piece(ax, n, ox, oy, n_pts=700):
    """Draw all arcs with molten core → earth → green → blue."""
    arc_curves = []

    zoom = 1.15
    max_span = (ART_W / 2) * zoom
    max_height = ART_H * zoom
    for i in range(n):
        frac = i / (n - 1)
        span = 0.15 + (max_span - 0.15) * (frac ** 1.3)
        height = 0.1 + (max_height - 0.1) * (frac ** 1.3)
        # Extend t range so parabola naturally curves down to mat line
        drop = oy - ART_B + frac * 0.08
        if drop > 0 and height > 0:
            t_max = np.sqrt(1 + drop / height)
        else:
            t_max = 1.0
        t = np.linspace(-t_max, t_max, n_pts)
        xs = ox + span * t
        base_ys = oy + height * (1 - t ** 2) + frac * 0.08

        wave, taper = asym_freq_ramp(t, frac, height)
        ys = base_ys + wave * taper

        arc_curves.append((xs, ys, frac))

        inv = 1.0 - frac

        base_lw = 0.7 + 2.5 * (inv ** 1.0)
        base_alpha = 0.60 + 0.35 * (inv ** 0.4)

        apex = (1 - np.abs(t[:-1] / t_max)) ** 0.5

        seg_colors = []
        seg_widths = []
        for j in range(n_pts - 1):
            cu = frac ** 0.65
            al = base_alpha * (0.55 + 0.45 * apex[j])
            seg_colors.append(interp_opaque(PALETTE, cu, al))
            seg_widths.append(base_lw * (0.40 + 0.60 * apex[j]))

        lc = lc_from_xy(xs, ys, seg_colors, seg_widths)
        ax.add_collection(lc)

    # ── Molten core glow ──
    nx_g, ny_g = 500, 350
    gxs = np.linspace(0, FIG_W, nx_g)
    gys = np.linspace(0, FIG_H, ny_g)
    gxg, gyg = np.meshgrid(gxs, gys)
    core = np.exp(-0.5 * ((gxg - ox) / 0.4) ** 2
                  -0.5 * ((gyg - (oy + 0.3)) / 0.5) ** 2)
    wash = np.exp(-0.5 * ((gxg - ox) / 1.2) ** 2
                  -0.5 * ((gyg - (oy + 0.6)) / 1.5) ** 2)
    rgba_img = np.zeros((ny_g, nx_g, 4))
    cr, cg, cb = hex_to_rgb('#F5E880')
    rgba_img[:, :, 0] = cr
    rgba_img[:, :, 1] = cg
    rgba_img[:, :, 2] = cb
    rgba_img[:, :, 3] = 0.35 * core + 0.06 * wash
    ax.imshow(rgba_img, extent=[0, FIG_W, 0, FIG_H], origin='lower',
              interpolation='bicubic', zorder=0, aspect='auto')

    # ── Filled bands between arcs ──
    n_fill = n - 1
    for k in range(n_fill):
        xs_inner, ys_inner, frac_inner = arc_curves[k]
        xs_outer, ys_outer, frac_outer = arc_curves[k + 1]
        frac_mid = (frac_inner + frac_outer) / 2
        band_alpha = 0.22 * np.exp(-3.5 * frac_mid)
        if band_alpha < 0.003:
            continue
        fill_color = interp_rgba(PALETTE, (frac_mid ** 0.65) * 0.7, band_alpha)
        poly_x = np.concatenate([xs_outer, xs_inner[::-1]])
        poly_y = np.concatenate([ys_outer, ys_inner[::-1]])
        verts = list(zip(poly_x, poly_y))
        poly = Polygon(verts, closed=True, facecolor=fill_color,
                       edgecolor='none', zorder=1)
        ax.add_patch(poly)


def render():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')

    draw_piece(ax, 35, ART_CX, ART_B + 0.25)
    add_mat(ax)
    add_signature(fig, ax, BG_COLOR, margin_piece=True, margin_bottom=ART_B)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "growth_strata.pdf")
    fig.savefig(pdf_path, format='pdf', facecolor=BG_COLOR)

    os.makedirs(PRINT_DIR, exist_ok=True)
    jpg_path = os.path.join(PRINT_DIR, "growth_strata.jpg")
    fig.savefig(jpg_path, facecolor=BG_COLOR, dpi=DPI, format='jpg')

    plt.close(fig)
    print(f"saved {pdf_path}")
    print(f"saved {jpg_path}")
    return pdf_path


if __name__ == '__main__':
    render()
