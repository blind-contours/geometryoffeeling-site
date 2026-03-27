"""
Round 10: Field-push approach with:
1. Richer color palette (more mauve in outer, deeper navy in center)
2. Optional interior fringe lines at top/bottom void peaks
"""
import colorsys
import os
import subprocess

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

DPI = 300
FIG_W = 12
FIG_H = 8


def make_palette(n_lines=60, sat_boost=1.0, value_boost=1.0):
    """
    Richer palette matching the curated reference more closely.
    More saturated mauve/rose outer, deeper navy center.
    """
    anchors_t = np.array([0.00, 0.06, 0.14, 0.22, 0.30, 0.38, 0.46, 0.50,
                          0.54, 0.62, 0.70, 0.78, 0.86, 0.94, 1.00])
    anchors_rgb = np.array([
        [0x9E, 0x7E, 0x88],  # warm mauve (outermost)
        [0x9A, 0x80, 0x8C],  # dusty rose
        [0x90, 0x7C, 0x8E],  # rose-purple
        [0x80, 0x78, 0x90],  # dusty purple
        [0x6A, 0x70, 0x88],  # slate-purple
        [0x55, 0x64, 0x7E],  # blue-slate
        [0x42, 0x54, 0x70],  # muted blue
        [0x2E, 0x42, 0x5E],  # deep navy (center)
        [0x42, 0x54, 0x70],  # muted blue
        [0x55, 0x64, 0x7E],  # blue-slate
        [0x6A, 0x70, 0x88],  # slate-purple
        [0x80, 0x78, 0x90],  # dusty purple
        [0x90, 0x7C, 0x8E],  # rose-purple
        [0x9A, 0x80, 0x8C],  # dusty rose
        [0x9E, 0x7E, 0x88],  # warm mauve (outermost)
    ], dtype=float) / 255.0

    t = np.linspace(0.0, 1.0, n_lines)
    colors = np.column_stack([
        np.interp(t, anchors_t, anchors_rgb[:, 0]),
        np.interp(t, anchors_t, anchors_rgb[:, 1]),
        np.interp(t, anchors_t, anchors_rgb[:, 2]),
    ])

    # Apply saturation and value boost
    if sat_boost != 1.0 or value_boost != 1.0:
        n = len(colors)
        mid = (n - 1) / 2.0
        idx = np.arange(n)
        # Boost outer bands more (where the mauve lives)
        outer_weight = 1.0 - np.exp(-((idx - mid) / 12.0) ** 2)
        boosted = []
        for i, rgb in enumerate(colors):
            h, s, v = colorsys.rgb_to_hsv(*rgb)
            s = min(1.0, s * (1.0 + (sat_boost - 1.0) * (0.4 + 0.6 * outer_weight[i])))
            v = min(1.0, v * value_boost)
            boosted.append(colorsys.hsv_to_rgb(h, s, v))
        colors = np.clip(np.array(boosted), 0.0, 1.0)

    return colors


BG_COLOR = '#DDD9D2'


def render_variant(name, sx=0.12, tip=0.34, break_band=0.048, stretch=0.90,
                   gamma=1.90, n_break=3, morph_exp=2.1,
                   lw_center=1.9, lw_base=0.85, n_lines=60,
                   wave_amp=0.0008, sat_boost=1.8, value_boost=1.0,
                   interior_fringe=False, fringe_count=5, fringe_max_len=0.08):
    """
    interior_fringe: if True, draw short line stubs inside the void at the peaks
    fringe_count: how many fringe lines at each peak
    fringe_max_len: max horizontal extent of longest fringe line
    """
    line_colors = make_palette(n_lines, sat_boost=sat_boost, value_boost=value_boost)

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

        a_target = tip + stretch * np.maximum(a - break_band, 0.0) ** gamma

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
        ax.plot(x, y, color=line_colors[i], lw=lw, alpha=1.0, solid_capstyle="round")

    # Interior fringe lines at top and bottom peaks
    if interior_fringe:
        # These are short horizontal stubs inside the void near the peaks
        for sign in [1, -1]:  # top (+1) and bottom (-1)
            peak_y = cy + sign * tip
            for fi in range(fringe_count):
                # Each fringe line is at a slightly different y level
                frac = (fi + 1) / (fringe_count + 1)
                fy = peak_y - sign * frac * tip * 0.3  # spread into the void
                # Length decreases as we go deeper into the void
                flen = fringe_max_len * (1.0 - frac * 0.7)
                # Draw from left side and right side
                fx_left = np.linspace(cx - flen, cx - 0.005, 200)
                fx_right = np.linspace(cx + 0.005, cx + flen, 200)

                # Slight curve toward the peak
                curve_l = sign * 0.015 * frac * np.exp(-((fx_left - (cx - flen)) / (flen * 0.3)) ** 2)
                curve_r = sign * 0.015 * frac * np.exp(-((fx_right - (cx + flen)) / (flen * 0.3)) ** 2)

                fy_l = fy + curve_l
                fy_r = fy + curve_r

                # Color: navy, getting lighter further in
                col_idx = int(mid - sign * (fi + 1))
                col_idx = max(0, min(n_lines - 1, col_idx))
                col = line_colors[col_idx]
                flw = 0.8 + 1.2 * (1.0 - frac)
                falpha = 0.6 + 0.3 * (1.0 - frac)

                ax.plot(fx_left, fy_l, color=col, lw=flw, alpha=falpha,
                        solid_capstyle="round")
                ax.plot(fx_right, fy_r, color=col, lw=flw, alpha=falpha,
                        solid_capstyle="round")

    # Equation label
    ax.text(0.06, 0.06, "(x\u2212cx)\u00b2/a\u00b2+(y\u2212cy)\u00b2/b\u00b2=1",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    out_dir = os.path.join(os.path.dirname(__file__), 'renders')
    os.makedirs(out_dir, exist_ok=True)
    png_path = os.path.join(out_dir, f'{name}.png')
    fig.savefig(png_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {name}")
    return png_path


if __name__ == '__main__':
    renders_dir = os.path.join(os.path.dirname(__file__), 'renders')

    variants = [
        # 1: Baseline with richer color
        ('grief_void_r10_01', dict(
            sx=0.12, tip=0.34, break_band=0.048, stretch=0.90, gamma=1.90,
            n_break=3, sat_boost=1.8)),

        # 2: Even richer color (more sat)
        ('grief_void_r10_02', dict(
            sx=0.12, tip=0.34, break_band=0.048, stretch=0.90, gamma=1.90,
            n_break=3, sat_boost=2.4)),

        # 3: Richer color + interior fringe
        ('grief_void_r10_03', dict(
            sx=0.12, tip=0.34, break_band=0.048, stretch=0.90, gamma=1.90,
            n_break=3, sat_boost=1.8,
            interior_fringe=True, fringe_count=5, fringe_max_len=0.08)),

        # 4: Richer color + interior fringe (more fringe lines)
        ('grief_void_r10_04', dict(
            sx=0.12, tip=0.34, break_band=0.048, stretch=0.90, gamma=1.90,
            n_break=3, sat_boost=1.8,
            interior_fringe=True, fringe_count=8, fringe_max_len=0.10)),

        # 5: Sweet spot params from r9 + richer color
        ('grief_void_r10_05', dict(
            sx=0.13, tip=0.35, break_band=0.045, stretch=0.95, gamma=2.00,
            n_break=2, sat_boost=1.8)),

        # 6: Sweet spot + fringe
        ('grief_void_r10_06', dict(
            sx=0.13, tip=0.35, break_band=0.045, stretch=0.95, gamma=2.00,
            n_break=2, sat_boost=1.8,
            interior_fringe=True, fringe_count=5, fringe_max_len=0.08)),

        # 7: Wider field + richer color + fringe
        ('grief_void_r10_07', dict(
            sx=0.14, tip=0.36, break_band=0.040, stretch=1.00, gamma=1.90,
            n_break=2, sat_boost=2.0,
            interior_fringe=True, fringe_count=6, fringe_max_len=0.09)),

        # 8: Baseline + richer + subtle fringe (fewer, shorter)
        ('grief_void_r10_08', dict(
            sx=0.12, tip=0.34, break_band=0.048, stretch=0.90, gamma=1.90,
            n_break=3, sat_boost=1.8,
            interior_fringe=True, fringe_count=3, fringe_max_len=0.06)),

        # 9: Maximum color richness, no fringe
        ('grief_void_r10_09', dict(
            sx=0.12, tip=0.34, break_band=0.048, stretch=0.90, gamma=1.90,
            n_break=3, sat_boost=2.8, value_boost=0.95)),

        # 10: Richer + taller diamond + fringe
        ('grief_void_r10_10', dict(
            sx=0.12, tip=0.38, break_band=0.048, stretch=0.90, gamma=1.90,
            n_break=3, sat_boost=2.0,
            interior_fringe=True, fringe_count=5, fringe_max_len=0.08)),
    ]

    for name, params in variants:
        render_variant(name, **params)

    for name, _ in variants:
        png = os.path.join(renders_dir, f'{name}.png')
        jpg = os.path.join(renders_dir, f'{name}.jpg')
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '92',
                        '--resampleWidth', '1800', png, '--out', jpg],
                       capture_output=True)
        print(f"converted {name}.jpg")
