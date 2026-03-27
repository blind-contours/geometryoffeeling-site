"""
Round 13: Field-push + straight horizontal lines behind the void at peaks.
The void is a window — behind it you see the original undeflected horizontal
lines. They stay FLAT (not curved), clipped to the void boundary. This creates
3D depth: curved main lines in front, flat lines pushed behind.
Only near the top and bottom peaks. Some break in the middle.
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
                   bg_stubs=True, bg_stub_count=9,
                   bg_full=3, bg_alpha=0.70,
                   bg_lw=1.0, bg_break_gap=0.015,
                   bg_color_boost=1.4, bg_depth=0.22):
    """
    bg_stubs: draw straight horizontal lines behind the void at peaks
    bg_stub_count: how many horizontal lines per peak
    bg_full: first N lines (nearest peak) are full/unbroken
    bg_alpha: opacity
    bg_lw: line width
    bg_break_gap: base center gap for the first broken line; doubles each subsequent
    bg_color_boost: saturation boost for background lines
    bg_depth: how deep into the void the lines extend (fraction of tip height)
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

    # --- Helper: compute deflected y for a given y0 ---
    def deflect(y0):
        d = y0 - cy
        a = abs(d)
        sign = 1 if d >= 0 else -1
        a_target = tip + stretch * np.maximum(a - break_band, 0.0) ** gamma
        morph = np.exp(-((np.abs(x - cx) / sx) ** morph_exp))
        d_curve = (1.0 - morph) * d + morph * sign * a_target
        sa = 0.055 * np.exp(-((a - (break_band + 0.05)) / 0.10) ** 2)
        shoulder = sign * sa * np.exp(-((np.abs(x - cx) / 0.14) ** 4))
        return cy + d_curve + shoulder + wave_amp * np.sin(2 * np.pi * (1.18 * x + 0.8 * y0))

    # --- Compute void boundary from first non-breaking lines ---
    first_above_idx = mid + n_break
    first_below_idx = mid - n_break - 1
    void_top = deflect(ys[first_above_idx]) if first_above_idx < n_lines else np.full_like(x, cy + tip)
    void_bottom = deflect(ys[first_below_idx]) if first_below_idx >= 0 else np.full_like(x, cy - tip)

    # --- Draw straight horizontal background lines at peaks (z=1) ---
    if bg_stubs:
        # Use the MAIN LINE SPACING so they look like continuations of the field
        main_spacing = ys[1] - ys[0]  # spacing between main lines

        for peak_sign in [1, -1]:  # +1 = top, -1 = bottom
            # Start from near the peak tip going inward
            # The peak is at cy + peak_sign * tip
            peak_y = cy + peak_sign * tip

            for si in range(bg_stub_count):
                # y position: start at peak, go toward center at main line spacing
                by = peak_y - peak_sign * main_spacing * (si + 0.5)

                # Don't go too deep into the void
                if peak_sign > 0 and by < cy + tip * (1.0 - bg_depth):
                    continue
                if peak_sign < 0 and by > cy - tip * (1.0 - bg_depth):
                    continue

                # Clip to void boundary: only draw where this y is inside the void
                if peak_sign > 0:
                    inside = by < void_top
                else:
                    inside = by > void_bottom

                if not np.any(inside):
                    continue

                # Color: use navy/center palette colors, boosted
                t_col = (by - ys[0]) / (ys[-1] - ys[0])
                ci = int(np.clip(t_col * (n_lines - 1), 0, n_lines - 1))
                col = np.array(line_colors[ci])
                if bg_color_boost != 1.0:
                    h, s, v = colorsys.rgb_to_hsv(*col)
                    s = min(1.0, s * bg_color_boost)
                    v = min(1.0, v * 1.05)
                    col = np.array(colorsys.hsv_to_rgb(h, s, v))

                # Build the horizontal line at y=by, masked to inside void
                y_line = np.where(inside, by, np.nan)

                if si < bg_full:
                    # Full line — no center break
                    ax.plot(x, y_line, color=col, lw=bg_lw, alpha=bg_alpha,
                            solid_capstyle="round", zorder=1)
                else:
                    # Broken: center gap doubles each line
                    gap_idx = si - bg_full
                    gap_hw = bg_break_gap * (2 ** gap_idx)
                    y_broken = np.where(np.abs(x - cx) > gap_hw, y_line, np.nan)
                    ax.plot(x, y_broken, color=col, lw=bg_lw, alpha=bg_alpha,
                            solid_capstyle="round", zorder=1)

    # --- Draw main deflected lines (z=2) ---
    for i, y0 in enumerate(ys):
        y = deflect(y0)

        if i in break_ids:
            d = y0 - cy
            a = abs(d)
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
        # 1: Baseline — 9 lines, 3 full, matching main spacing
        ('grief_void_r13_01', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_stubs=True, bg_stub_count=9, bg_full=3,
            bg_alpha=0.70, bg_lw=1.0, bg_break_gap=0.015,
            bg_color_boost=1.4, bg_depth=0.22)),

        # 2: Deeper into void (more lines visible)
        ('grief_void_r13_02', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_stubs=True, bg_stub_count=12, bg_full=3,
            bg_alpha=0.70, bg_lw=1.0, bg_break_gap=0.015,
            bg_color_boost=1.4, bg_depth=0.35)),

        # 3: Shallower (lines only very near peak)
        ('grief_void_r13_03', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_stubs=True, bg_stub_count=9, bg_full=3,
            bg_alpha=0.70, bg_lw=1.0, bg_break_gap=0.015,
            bg_color_boost=1.4, bg_depth=0.15)),

        # 4: Bigger break gap (stubs get shorter faster)
        ('grief_void_r13_04', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_stubs=True, bg_stub_count=9, bg_full=3,
            bg_alpha=0.70, bg_lw=1.0, bg_break_gap=0.025,
            bg_color_boost=1.4, bg_depth=0.22)),

        # 5: Smaller break gap (stubs stay intact longer)
        ('grief_void_r13_05', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_stubs=True, bg_stub_count=9, bg_full=3,
            bg_alpha=0.70, bg_lw=1.0, bg_break_gap=0.008,
            bg_color_boost=1.4, bg_depth=0.22)),

        # 6: Bolder + stronger color
        ('grief_void_r13_06', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=2.2,
            bg_stubs=True, bg_stub_count=9, bg_full=3,
            bg_alpha=0.80, bg_lw=1.2, bg_break_gap=0.015,
            bg_color_boost=1.6, bg_depth=0.22)),

        # 7: 2 full lines only
        ('grief_void_r13_07', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_stubs=True, bg_stub_count=9, bg_full=2,
            bg_alpha=0.70, bg_lw=1.0, bg_break_gap=0.012,
            bg_color_boost=1.4, bg_depth=0.22)),

        # 8: Sweet spot shape + bg lines
        ('grief_void_r13_08', dict(
            sx=0.13, tip=0.35, stretch=0.95, gamma=2.00,
            n_break=2, sat_boost=1.8,
            bg_stubs=True, bg_stub_count=9, bg_full=3,
            bg_alpha=0.70, bg_lw=1.0, bg_break_gap=0.015,
            bg_color_boost=1.4, bg_depth=0.22)),

        # 9: No bg lines (clean void)
        ('grief_void_r13_09', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            bg_stubs=False)),

        # 10: Wider + taller + bg lines
        ('grief_void_r13_10', dict(
            sx=0.14, tip=0.36, stretch=1.00, gamma=1.90,
            n_break=2, sat_boost=2.0,
            bg_stubs=True, bg_stub_count=9, bg_full=3,
            bg_alpha=0.70, bg_lw=1.0, bg_break_gap=0.015,
            bg_color_boost=1.4, bg_depth=0.25)),
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
