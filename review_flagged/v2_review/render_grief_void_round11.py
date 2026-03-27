"""
Round 11: Field-push + background lines running behind the void.
The void acts like a window — behind it you can see the original
undeflected horizontal lines continuing, some broken.
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
BG_COLOR = '#DDD9D2'


def make_palette(n_lines=60, sat_boost=1.0):
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


def render_variant(name, sx=0.12, tip=0.34, break_band=0.048, stretch=0.90,
                   gamma=1.90, n_break=3, morph_exp=2.1,
                   lw_center=1.9, lw_base=0.85, n_lines=60,
                   wave_amp=0.0008, sat_boost=1.8,
                   bg_lines=True, bg_line_count=12, bg_alpha=0.35,
                   bg_break_count=4, bg_lw=0.7):
    """
    bg_lines: draw horizontal background lines behind the void
    bg_line_count: how many background lines visible inside the void
    bg_alpha: opacity of background lines
    bg_break_count: how many of them are broken
    bg_lw: line width of background lines
    """
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

    # --- Compute the void boundary (where the deflected lines define the opening) ---
    # For each x position, find the y-extent of the void (where no lines pass)
    # The innermost non-breaking lines define the boundary
    # We compute the deflected path for the lines closest to the equator that DON'T break
    # to find the void boundary shape

    def compute_y_path(y0):
        d = y0 - cy
        a = abs(d)
        sign = 1 if d >= 0 else -1
        a_target = tip + stretch * np.maximum(a - break_band, 0.0) ** gamma
        morph = np.exp(-((np.abs(x - cx) / sx) ** morph_exp))
        d_curve = (1.0 - morph) * d + morph * sign * a_target
        sa = 0.055 * np.exp(-((a - (break_band + 0.05)) / 0.10) ** 2)
        shoulder = sign * sa * np.exp(-((np.abs(x - cx) / 0.14) ** 4))
        return cy + d_curve + shoulder

    # Find the void boundary: first non-breaking line above and below equator
    first_above_idx = mid + n_break
    first_below_idx = mid - n_break - 1
    if first_above_idx < n_lines:
        void_top = compute_y_path(ys[first_above_idx])
    else:
        void_top = np.full_like(x, cy + tip)
    if first_below_idx >= 0:
        void_bottom = compute_y_path(ys[first_below_idx])
    else:
        void_bottom = np.full_like(x, cy - tip)

    # --- Draw background lines (behind the void, at z=1) ---
    if bg_lines:
        # Background lines are straight horizontals at original y positions
        # Only visible inside the void (between void_top and void_bottom)
        bg_y_min = cy - tip * 0.85
        bg_y_max = cy + tip * 0.85
        bg_ys = np.linspace(bg_y_min, bg_y_max, bg_line_count + 2)[1:-1]

        # Which background lines are broken?
        bg_mid = len(bg_ys) // 2
        bg_break_set = set(range(bg_mid - bg_break_count // 2,
                                  bg_mid + bg_break_count // 2 + bg_break_count % 2))

        for bi, by in enumerate(bg_ys):
            # Only draw where this y-level is inside the void
            inside = (by < void_top) & (by > void_bottom)

            if not np.any(inside):
                continue

            # Find contiguous inside regions
            bg_x_masked = np.where(inside, x, np.nan)

            # Map bg line to nearest palette color
            t_frac = (by - ys[0]) / (ys[-1] - ys[0])
            ci = int(np.clip(t_frac * (n_lines - 1), 0, n_lines - 1))
            col = line_colors[ci]

            # Distance from center affects alpha
            dist_from_center = abs(by - cy) / tip
            line_alpha = bg_alpha * (0.5 + 0.5 * (1.0 - dist_from_center))

            if bi in bg_break_set:
                # Broken: gap near center
                gap_w = 0.02 + 0.04 * (1.0 - dist_from_center)
                bg_y_line = np.where(np.abs(bg_x_masked - cx) > gap_w,
                                      by, np.nan)
            else:
                bg_y_line = np.full_like(bg_x_masked, by)
                bg_y_line[np.isnan(bg_x_masked)] = np.nan

            # Add subtle wave
            bg_y_line = bg_y_line + 0.001 * np.sin(2 * np.pi * (1.18 * x + 0.8 * by))

            ax.plot(x, bg_y_line, color=col, lw=bg_lw, alpha=line_alpha,
                    solid_capstyle="round", zorder=1)

    # --- Draw main deflected lines (at z=2) ---
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
        ax.plot(x, y, color=line_colors[i], lw=lw, alpha=1.0,
                solid_capstyle="round", zorder=2)

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
        # 1: Baseline + background lines (subtle)
        ('grief_void_r11_01', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_lines=True, bg_line_count=10, bg_alpha=0.30,
            bg_break_count=4, bg_lw=0.7)),

        # 2: More background lines, slightly bolder
        ('grief_void_r11_02', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_lines=True, bg_line_count=14, bg_alpha=0.40,
            bg_break_count=4, bg_lw=0.8)),

        # 3: Dense background, more broken
        ('grief_void_r11_03', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_lines=True, bg_line_count=16, bg_alpha=0.35,
            bg_break_count=6, bg_lw=0.7)),

        # 4: Fewer background lines, bolder
        ('grief_void_r11_04', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_lines=True, bg_line_count=8, bg_alpha=0.45,
            bg_break_count=3, bg_lw=0.9)),

        # 5: Sweet spot shape + bg lines
        ('grief_void_r11_05', dict(
            sx=0.13, tip=0.35, stretch=0.95, gamma=2.00,
            n_break=2, sat_boost=1.8,
            bg_lines=True, bg_line_count=12, bg_alpha=0.35,
            bg_break_count=4, bg_lw=0.7)),

        # 6: Taller diamond + bg lines
        ('grief_void_r11_06', dict(
            sx=0.12, tip=0.38, n_break=3, sat_boost=2.0,
            bg_lines=True, bg_line_count=14, bg_alpha=0.35,
            bg_break_count=5, bg_lw=0.7)),

        # 7: Extra rich color + bg lines
        ('grief_void_r11_07', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=2.4,
            bg_lines=True, bg_line_count=12, bg_alpha=0.35,
            bg_break_count=4, bg_lw=0.7)),

        # 8: Background lines very faint (like a ghost)
        ('grief_void_r11_08', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_lines=True, bg_line_count=12, bg_alpha=0.20,
            bg_break_count=4, bg_lw=0.6)),

        # 9: No background (clean void for comparison)
        ('grief_void_r11_09', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_lines=False)),

        # 10: bg lines + wider field for comparison
        ('grief_void_r11_10', dict(
            sx=0.14, tip=0.36, stretch=1.00, gamma=1.90,
            n_break=2, sat_boost=2.0,
            bg_lines=True, bg_line_count=14, bg_alpha=0.38,
            bg_break_count=5, bg_lw=0.75)),
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
