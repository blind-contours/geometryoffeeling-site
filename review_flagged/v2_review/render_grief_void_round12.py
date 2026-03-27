"""
Round 12 (v3): Field-push with natural stub lines at void peaks.
The stubs are actual deflected lines — continuations of the horizontal
line field pushed by the morph. They follow the same curvature as the
main lines but break/gap in the center. 9 lines at each peak:
first 3 are full connecting, then each successive one has a center gap
that doubles (visible stubs halve).
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
                   peak_stubs=True, stub_count=9,
                   stub_full=3, stub_alpha=0.70,
                   stub_lw=1.0, stub_y0_start=0.005,
                   stub_y0_end=0.10, stub_base_gap=0.008,
                   stub_color_boost=1.4):
    """
    peak_stubs: enable graduated stub lines at peaks
    stub_count: lines per peak (9)
    stub_full: first N lines (at tip) are full/unbroken (3)
    stub_y0_start: y0 offset from cy for the first stub (closest to equator, pushed to tip)
    stub_y0_end: y0 offset from cy for the last stub (furthest, pushed least)
    stub_base_gap: center gap half-width for the first broken stub (4th line)
    stub_color_boost: saturation multiplier for stub line colors
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

    # --- Compute void boundary ---
    first_above_idx = mid + n_break
    first_below_idx = mid - n_break - 1
    void_top = deflect(ys[first_above_idx]) if first_above_idx < n_lines else np.full_like(x, cy + tip)
    void_bottom = deflect(ys[first_below_idx]) if first_below_idx >= 0 else np.full_like(x, cy - tip)

    # --- Draw stub lines FIRST (z=1, behind main lines) ---
    if peak_stubs:
        # Stub y0 values: distributed from near-equator to further out
        # si=0 → y0 closest to equator → pushed nearest peak tip
        # si=stub_count-1 → y0 furthest → pushed least (deepest into void)
        stub_y0_offsets = np.linspace(stub_y0_start, stub_y0_end, stub_count)

        for peak_sign in [1, -1]:  # top and bottom peaks
            for si in range(stub_count):
                y0 = cy + peak_sign * stub_y0_offsets[si]

                # Deflect this line using same physics
                y_path = deflect(y0)

                # Clip to void interior only
                if peak_sign > 0:
                    inside = y_path < void_top
                else:
                    inside = y_path > void_bottom
                y_clipped = np.where(inside, y_path, np.nan)

                # Color: use the palette, boosted
                t_col = (y0 - ys[0]) / (ys[-1] - ys[0])
                ci = int(np.clip(t_col * (n_lines - 1), 0, n_lines - 1))
                col = np.array(line_colors[ci])
                if stub_color_boost != 1.0:
                    h, s, v = colorsys.rgb_to_hsv(*col)
                    s = min(1.0, s * stub_color_boost)
                    v = min(1.0, v * 1.05)
                    col = np.array(colorsys.hsv_to_rgb(h, s, v))

                # Stub ordering: si=0 is at tip (shortest visible)
                # si=stub_count-1 is deepest (longest visible)
                # Reverse so si=0 → tip, stub_full lines at tip are full
                # The "full" lines are the first `stub_full` at the tip
                stub_idx_from_tip = si  # 0 = at tip

                if stub_idx_from_tip < stub_full:
                    # Full connecting line — no center gap
                    ax.plot(x, y_clipped, color=col, lw=stub_lw, alpha=stub_alpha,
                            solid_capstyle="round", zorder=1)
                else:
                    # Broken: center gap doubles with each line from the full zone
                    gap_idx = stub_idx_from_tip - stub_full  # 0, 1, 2, 3, 4, 5
                    gap_hw = stub_base_gap * (2 ** gap_idx)

                    y_gapped = np.where(np.abs(x - cx) > gap_hw, y_clipped, np.nan)
                    ax.plot(x, y_gapped, color=col, lw=stub_lw, alpha=stub_alpha,
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
        # 1: Baseline
        ('grief_void_r12_01', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            peak_stubs=True, stub_count=9, stub_full=3,
            stub_alpha=0.70, stub_lw=1.0,
            stub_y0_start=0.005, stub_y0_end=0.10,
            stub_base_gap=0.008, stub_color_boost=1.4)),

        # 2: Wider y0 range (stubs more spread vertically)
        ('grief_void_r12_02', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            peak_stubs=True, stub_count=9, stub_full=3,
            stub_alpha=0.70, stub_lw=1.0,
            stub_y0_start=0.005, stub_y0_end=0.14,
            stub_base_gap=0.008, stub_color_boost=1.4)),

        # 3: Tighter y0 range (stubs clustered near tip)
        ('grief_void_r12_03', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            peak_stubs=True, stub_count=9, stub_full=3,
            stub_alpha=0.70, stub_lw=1.0,
            stub_y0_start=0.003, stub_y0_end=0.07,
            stub_base_gap=0.006, stub_color_boost=1.4)),

        # 4: Bigger base gap (stubs break more aggressively)
        ('grief_void_r12_04', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            peak_stubs=True, stub_count=9, stub_full=3,
            stub_alpha=0.70, stub_lw=1.0,
            stub_y0_start=0.005, stub_y0_end=0.10,
            stub_base_gap=0.014, stub_color_boost=1.4)),

        # 5: Smaller base gap (stubs break less)
        ('grief_void_r12_05', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            peak_stubs=True, stub_count=9, stub_full=3,
            stub_alpha=0.70, stub_lw=1.0,
            stub_y0_start=0.005, stub_y0_end=0.10,
            stub_base_gap=0.005, stub_color_boost=1.4)),

        # 6: Bolder + stronger color
        ('grief_void_r12_06', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=2.2,
            peak_stubs=True, stub_count=9, stub_full=3,
            stub_alpha=0.80, stub_lw=1.2,
            stub_y0_start=0.005, stub_y0_end=0.10,
            stub_base_gap=0.008, stub_color_boost=1.6)),

        # 7: Sweet spot shape + stubs
        ('grief_void_r12_07', dict(
            sx=0.13, tip=0.35, stretch=0.95, gamma=2.00,
            n_break=2, sat_boost=1.8,
            peak_stubs=True, stub_count=9, stub_full=3,
            stub_alpha=0.70, stub_lw=1.0,
            stub_y0_start=0.005, stub_y0_end=0.10,
            stub_base_gap=0.008, stub_color_boost=1.4)),

        # 8: 2 full + different y0 range
        ('grief_void_r12_08', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            peak_stubs=True, stub_count=9, stub_full=2,
            stub_alpha=0.70, stub_lw=1.0,
            stub_y0_start=0.005, stub_y0_end=0.10,
            stub_base_gap=0.010, stub_color_boost=1.4)),

        # 9: No stubs (clean void)
        ('grief_void_r12_09', dict(
            sx=0.12, tip=0.34, n_break=3, sat_boost=1.8,
            peak_stubs=False)),

        # 10: Wider field + taller + stubs
        ('grief_void_r12_10', dict(
            sx=0.14, tip=0.36, stretch=1.00, gamma=1.90,
            n_break=2, sat_boost=2.0,
            peak_stubs=True, stub_count=9, stub_full=3,
            stub_alpha=0.70, stub_lw=1.0,
            stub_y0_start=0.005, stub_y0_end=0.12,
            stub_base_gap=0.008, stub_color_boost=1.4)),
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
