"""
Round 9: Field-push approach (from user's reference code).
Clean morph-based deflection, no elliptical void mask.
Vary: sx (field width), tip (peak height), break_band, stretch, gamma.
"""
import colorsys
import os
import subprocess

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pathlib import Path


CURATED_IMAGE = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'prints', 'grief', 'grief_void.jpg')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = (0.870, 0.850, 0.827)  # #DDD9D2 approx


def make_fallback_palette(n_lines=60):
    anchors_t = np.array([0.00, 0.08, 0.18, 0.28, 0.38, 0.46, 0.50,
                          0.54, 0.62, 0.72, 0.82, 0.92, 1.00])
    anchors_rgb = np.array([
        [0x9b, 0x84, 0x8b],
        [0xa1, 0x8a, 0x91],
        [0x85, 0x80, 0x92],
        [0x61, 0x6f, 0x88],
        [0x50, 0x61, 0x79],
        [0x41, 0x53, 0x6c],
        [0x35, 0x48, 0x62],
        [0x41, 0x53, 0x6c],
        [0x50, 0x61, 0x79],
        [0x61, 0x6f, 0x88],
        [0x85, 0x80, 0x92],
        [0xa1, 0x8a, 0x91],
        [0x9b, 0x84, 0x8b],
    ], dtype=float) / 255.0
    t = np.linspace(0.0, 1.0, n_lines)
    return np.column_stack([
        np.interp(t, anchors_t, anchors_rgb[:, 0]),
        np.interp(t, anchors_t, anchors_rgb[:, 1]),
        np.interp(t, anchors_t, anchors_rgb[:, 2]),
    ])


def boost_outer_saturation(colors, outer_sat_boost=2.6, sigma=10.0, outer_value_scale=1.0):
    n = len(colors)
    idx = np.arange(n)
    mid = (n - 1) / 2.0
    center_weight = np.exp(-((idx - mid) / sigma) ** 2)
    outer_weight = 1.0 - center_weight
    boosted = []
    for i, rgb in enumerate(colors):
        h, s, v = colorsys.rgb_to_hsv(*rgb)
        s = min(1.0, s * (1.0 + (outer_sat_boost - 1.0) * outer_weight[i]))
        v = min(1.0, v * (1.0 + (outer_value_scale - 1.0) * outer_weight[i]))
        boosted.append(colorsys.hsv_to_rgb(h, s, v))
    return np.clip(np.array(boosted), 0.0, 1.0)


def sample_visible_line_palette(reference_path, n_lines=60, x0=40, x1=240):
    arr = np.asarray(Image.open(reference_path).convert("RGB"), dtype=float) / 255.0
    h, w, _ = arr.shape
    bg = arr[int(h*0.45):int(h*0.55), int(w*0.45):int(w*0.55)].mean(axis=(0, 1))
    diff = np.linalg.norm(arr - bg, axis=2)
    row_score = diff[:, x0:x1].max(axis=1)
    row_score = np.convolve(row_score, np.ones(3)/3.0, mode="same")
    peaks = []
    for y in range(1, h-1):
        if row_score[y] > 0.14 and row_score[y] >= row_score[y-1] and row_score[y] > row_score[y+1]:
            if not peaks or y - peaks[-1] > 8:
                peaks.append(y)
            elif row_score[y] > row_score[peaks[-1]]:
                peaks[-1] = y
    if len(peaks) != n_lines:
        return make_fallback_palette(n_lines), bg
    colors = []
    for y in peaks:
        patch = arr[max(0,y-1):min(h,y+2), x0:x1]
        patch_diff = diff[max(0,y-1):min(h,y+2), x0:x1]
        mask = patch_diff > 0.22
        if np.count_nonzero(mask) < 5:
            idx_max = np.unravel_index(np.argmax(patch_diff), patch_diff.shape)
            color = patch[idx_max]
        else:
            color = patch[mask].mean(axis=0)
        colors.append(color)
    colors = np.array(colors)
    colors = 0.5 * (colors + colors[::-1])
    return colors, bg


def get_palette(n_lines=60):
    ref = os.path.abspath(CURATED_IMAGE)
    if Path(ref).exists():
        visible_colors, bg = sample_visible_line_palette(ref, n_lines=n_lines)
        palette = boost_outer_saturation(visible_colors, outer_sat_boost=2.6, sigma=10.0)
        return palette, tuple(bg)
    return make_fallback_palette(n_lines), BG_COLOR


def render_variant(name, sx=0.12, tip=0.34, break_band=0.048, stretch=0.90,
                   gamma=1.90, shoulder_amp_scale=1.0, n_break=3,
                   morph_exp=2.1, lw_center=1.9, lw_base=0.85,
                   n_lines=60, wave_amp=0.0008):
    line_colors, bg = get_palette(n_lines)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=bg)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(bg)
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

        sa = 0.055 * shoulder_amp_scale * np.exp(-((a - (break_band + 0.05)) / 0.10) ** 2)
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

    # Equation label
    ax.text(0.06, 0.06, "(x\u2212cx)\u00b2/a\u00b2+(y\u2212cy)\u00b2/b\u00b2=1",
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25), transform=ax.transAxes)

    out_dir = os.path.join(os.path.dirname(__file__), 'renders')
    os.makedirs(out_dir, exist_ok=True)
    png_path = os.path.join(out_dir, f'{name}.png')
    fig.savefig(png_path, facecolor=bg, dpi=DPI)
    plt.close(fig)
    print(f"saved {name}")
    return png_path


if __name__ == '__main__':
    renders_dir = os.path.join(os.path.dirname(__file__), 'renders')

    variants = [
        # 1: Baseline (exact params from user's code)
        ('grief_void_r9_01', dict(
            sx=0.12, tip=0.34, break_band=0.048, stretch=0.90, gamma=1.90,
            n_break=3)),

        # 2: Wider field (more lines pulled at sides)
        ('grief_void_r9_02', dict(
            sx=0.15, tip=0.34, break_band=0.048, stretch=0.90, gamma=1.90,
            n_break=3)),

        # 3: Taller tip (sharper diamond)
        ('grief_void_r9_03', dict(
            sx=0.12, tip=0.38, break_band=0.048, stretch=0.90, gamma=1.90,
            n_break=3)),

        # 4: Shorter tip + wider field
        ('grief_void_r9_04', dict(
            sx=0.14, tip=0.30, break_band=0.048, stretch=0.90, gamma=1.90,
            n_break=3)),

        # 5: More stretch (lines further from center pulled more)
        ('grief_void_r9_05', dict(
            sx=0.12, tip=0.34, break_band=0.048, stretch=1.10, gamma=1.90,
            n_break=3)),

        # 6: Less gamma (more linear pull — changes diamond curvature)
        ('grief_void_r9_06', dict(
            sx=0.12, tip=0.34, break_band=0.048, stretch=0.90, gamma=1.50,
            n_break=3)),

        # 7: Higher gamma (more nonlinear — sharper transition)
        ('grief_void_r9_07', dict(
            sx=0.12, tip=0.34, break_band=0.048, stretch=0.90, gamma=2.40,
            n_break=3)),

        # 8: Fewer breaks (only 2 each side)
        ('grief_void_r9_08', dict(
            sx=0.12, tip=0.34, break_band=0.048, stretch=0.90, gamma=1.90,
            n_break=2)),

        # 9: Wider field + narrower break band + more stretch
        ('grief_void_r9_09', dict(
            sx=0.14, tip=0.36, break_band=0.040, stretch=1.00, gamma=1.90,
            n_break=2)),

        # 10: Sweet spot attempt
        ('grief_void_r9_10', dict(
            sx=0.13, tip=0.35, break_band=0.045, stretch=0.95, gamma=2.00,
            n_break=2)),
    ]

    for name, params in variants:
        png = render_variant(name, **params)

    # Convert PNGs to JPGs for review page
    for name, _ in variants:
        png = os.path.join(renders_dir, f'{name}.png')
        jpg = os.path.join(renders_dir, f'{name}.jpg')
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '92',
                        '--resampleWidth', '1800', png, '--out', jpg],
                       capture_output=True)
        print(f"converted {name}.jpg")
