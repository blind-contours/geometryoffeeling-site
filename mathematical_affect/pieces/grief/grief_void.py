"""
Geometry of Feeling — Grief: Grief Void
Field-push morph approach: horizontal lines deflected around a central void.
Clean diamond shape with smooth arcs, broken equatorial lines.
"""
import colorsys
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#DDD9D2'


def make_palette(n_lines=60, sat_boost=1.8):
    anchors_t = np.array([0.00, 0.06, 0.14, 0.22, 0.30, 0.38, 0.46, 0.50,
                          0.54, 0.62, 0.70, 0.78, 0.86, 0.94, 1.00])
    anchors_rgb = np.array([
        [0x9E, 0x7E, 0x88], [0x9A, 0x80, 0x8C], [0x90, 0x7C, 0x8E],
        [0x80, 0x78, 0x90], [0x6A, 0x70, 0x88], [0x55, 0x64, 0x7E],
        [0x42, 0x54, 0x70], [0x2E, 0x42, 0x5E], [0x42, 0x54, 0x70],
        [0x55, 0x64, 0x7E], [0x6A, 0x70, 0x88], [0x80, 0x78, 0x90],
        [0x90, 0x7C, 0x8E], [0x9A, 0x80, 0x8C], [0x9E, 0x7E, 0x88],
    ], dtype=float) / 255.0
    t = np.linspace(0.0, 1.0, n_lines)
    colors = np.column_stack([
        np.interp(t, anchors_t, anchors_rgb[:, 0]),
        np.interp(t, anchors_t, anchors_rgb[:, 1]),
        np.interp(t, anchors_t, anchors_rgb[:, 2]),
    ])
    if sat_boost != 1.0:
        n = len(colors)
        mid = (n - 1) / 2.0
        idx = np.arange(n)
        outer_weight = 1.0 - np.exp(-((idx - mid) / 12.0) ** 2)
        boosted = []
        for i, rgb in enumerate(colors):
            h, s, v = colorsys.rgb_to_hsv(*rgb)
            s = min(1.0, s * (1.0 + (sat_boost - 1.0) * (0.4 + 0.6 * outer_weight[i])))
            boosted.append(colorsys.hsv_to_rgb(h, s, v))
        colors = np.clip(np.array(boosted), 0.0, 1.0)
    return colors


def render():
    sx = 0.12
    tip = 0.34
    break_band = 0.048
    stretch = 0.90
    gamma_exp = 1.90
    n_break = 3
    morph_exp = 2.1
    lw_center = 1.9
    lw_base = 0.85
    n_lines = 60
    wave_amp = 0.0008
    sat_boost = 1.8

    line_colors = make_palette(n_lines, sat_boost=sat_boost)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    x = np.linspace(0.02, 0.98, 2600)
    ys = np.linspace(0.05, 0.95, n_lines)
    cx, cy = 0.5, 0.5

    mid = n_lines // 2
    break_ids = set(range(mid - n_break, mid + n_break))

    for i, y0 in enumerate(ys):
        d = y0 - cy
        a = abs(d)
        sign = 1 if d >= 0 else -1

        a_target = tip + stretch * np.maximum(a - break_band, 0.0) ** gamma_exp

        morph = np.exp(-((np.abs(x - cx) / sx) ** morph_exp))
        d_curve = (1.0 - morph) * d + morph * sign * a_target

        sa = 0.055 * np.exp(-((a - (break_band + 0.05)) / 0.10) ** 2)
        shoulder = sign * sa * np.exp(-((np.abs(x - cx) / 0.14) ** 4))

        y = cy + d_curve + shoulder
        y += wave_amp * np.sin(2 * np.pi * (1.18 * x + 0.8 * y0))

        if i in break_ids:
            t_frac = a / break_band if break_band > 0 else 1.0
            gap_scale = 1.0 - 0.55 * np.clip(t_frac, 0, 1)
            gap_half_width = (0.125 + 0.035 * (1 - t_frac ** 1.5)) * gap_scale
            y = np.ma.masked_where(np.abs(x - cx) < gap_half_width, y)

        lw = lw_base + lw_center * np.exp(-((y0 - cy) / 0.22) ** 2)
        ax.plot(x, y, color=line_colors[i], lw=lw, alpha=1.0,
                solid_capstyle="round")

    # Equation label
    ax.text(0.06, 0.06, "(x\u2212cx)\u00b2/a\u00b2+(y\u2212cy)\u00b2/b\u00b2=1",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "grief_void.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
