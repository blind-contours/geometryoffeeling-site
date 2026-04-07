"""
Geometry of Feeling — Comprehending: Clarity

The left wing of the Comprehension triptych. Drama-blue palette, paired
piers reaching up from below into a vortex storm above. The thesis: the
moment the field and the ground meet each other halfway. Block quantization
captures the storm — vortices being literally squared.

Mechanism:
  - Recursive feature-driven Mondrian subdivision driven by scalar field
    gradients. Vorticity-rich regions get more cuts.
  - Pier injection: tall vertical strips at chosen x-positions recurse only
    to a shallow depth, becoming monumental piers that pierce up into the
    storm.
  - Soft horizon: gradient depth top→bottom (no clean horizon line).
  - Vertical aspect bias band: cells in the middle prefer vertical splits.
  - Velocity-tinted per-cell quantization.

This script reproduces the exact configuration of "V10 — Full Synthesis"
from scripts/wonder_comprehension_v9.py.
"""
import os
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
PRINT_DIR = os.path.join(SCRIPT_DIR, '..', '..', '..', 'public', 'prints', 'comprehending')
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PRINT_DIR, exist_ok=True)

DPI = 300
FIG_W, FIG_H = 12, 8
MARGIN_COLOR = "#DDD9D2"
ML, MR, MB, MT = 0.07, 0.07, 0.08, 0.08


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


# ─── Field — paired vortices ────────────────────────────────────────

def field_paired(X, Y, complexity=1.0, offset=0.0,
                 v1_pos=(1.4, 3.4), v1_strength=1.55, v1_radius=0.21,
                 v2_pos=(4.0, 3.1), v2_strength=0.85, v2_radius=0.30,
                 v3_pos=(2.7, 2.4), v3_strength=0.30, v3_radius=0.55,
                 bg_amp=0.16):
    c = complexity
    P = np.zeros_like(X)
    r1 = np.sqrt((X - v1_pos[0]) ** 2 + (Y - v1_pos[1]) ** 2) + 0.12
    P += v1_strength * np.exp(-r1 * v1_radius) * np.sin(r1 * 2.7 * c + offset)
    r2 = np.sqrt((X - v2_pos[0]) ** 2 + (Y - v2_pos[1]) ** 2) + 0.13
    P += v2_strength * np.exp(-r2 * v2_radius) * np.sin(r2 * 3.0 * c + offset + 0.5)
    r3 = np.sqrt((X - v3_pos[0]) ** 2 + (Y - v3_pos[1]) ** 2) + 0.15
    P += v3_strength * np.exp(-r3 * v3_radius) * np.sin(r3 * 3.8 * c + offset + 1.3)
    P += bg_amp * np.sin(X * 2.0 * c + offset * 0.3) * np.cos(Y * 1.5 * c)
    P += (bg_amp * 0.4) * np.sin(X * 4.2 * c + 1.3) * np.cos(Y * 3.5 * c + 0.7)
    return P


def compute_velocity(scalar_field):
    dPdy = np.gradient(scalar_field, axis=0)
    dPdx = np.gradient(scalar_field, axis=1)
    vx, vy = dPdy, -dPdx
    vmag = np.sqrt(vx ** 2 + vy ** 2)
    return vx, vy, vmag


def compute_vorticity(scalar_field):
    vx, vy, _ = compute_velocity(scalar_field)
    dvy_dx = np.gradient(vy, axis=1)
    dvx_dy = np.gradient(vx, axis=0)
    return np.abs(dvy_dx - dvx_dy)


def field_to_colors(field, palette_rgb):
    vmin, vmax = field.min(), field.max()
    t = (field - vmin) / (vmax - vmin + 1e-10)
    n = len(palette_rgb) - 1
    idx = t * n
    i = np.floor(idx).astype(int)
    i = np.clip(i, 0, n - 1)
    frac = idx - i
    frac = frac[..., np.newaxis]
    pal = np.array(palette_rgb)
    return pal[i] * (1 - frac) + pal[np.minimum(i + 1, n)] * frac


# ─── Mondrian subdivision with PIER INJECTION + SOFT HORIZON ────────

def subdivide_mondrian(color_field, scalar_field, vmag, vort, cfg):
    H, W, _ = color_field.shape
    grad_y, grad_x = np.gradient(scalar_field)

    max_depth_top = cfg.get('max_depth_top', 10)
    max_depth_bot = cfg.get('max_depth_bot', 4)
    depth_power = cfg.get('depth_power', 1.1)
    min_cell = cfg.get('min_cell', 3)
    edge_margin = cfg.get('edge_margin', 0.22)
    vort_depth_bias = cfg.get('vort_depth_bias', 1.2)
    rng = np.random.RandomState(cfg.get('seed', 77))
    rand_jitter = cfg.get('split_jitter', 0.10)

    vbias_top = cfg.get('vbias_top', 0.35)
    vbias_bot = cfg.get('vbias_bot', 0.78)
    vbias_strength = cfg.get('vbias_strength', 0.65)

    vort_norm = vort / (vort.max() + 1e-10)
    cells = []

    def depth_for_cell(yc_norm, vort_avg, pier=False):
        if pier:
            return cfg.get('pier_depth', 4)
        s = yc_norm ** depth_power
        base = max_depth_top * (1 - s) + max_depth_bot * s
        bonus = vort_depth_bias * vort_avg * (max_depth_top - max_depth_bot)
        return int(round(base + bonus))

    def recurse(x0, y0, x1, y1, depth, pier=False):
        w, h = x1 - x0, y1 - y0
        yc = (y0 + y1) / 2
        yc_norm = yc / H
        cell_vort = vort_norm[y0:y1, x0:x1].mean()
        max_d = depth_for_cell(yc_norm, cell_vort, pier=pier)

        if depth >= max_d or w < min_cell * 2 or h < min_cell * 2:
            cells.append((x0, y0, x1, y1, depth))
            return

        if w >= h * 1.4:
            split_dir = 'v'
        elif h >= w * 1.4:
            split_dir = 'h'
        else:
            if vbias_top <= yc_norm <= vbias_bot and not pier:
                split_dir = 'v' if rng.random() < (0.5 + vbias_strength * 0.5) else 'h'
            else:
                split_dir = 'v' if rng.random() < 0.5 else 'h'

        if split_dir == 'v':
            col_sum = np.abs(grad_x[y0:y1, x0:x1]).sum(axis=0)
            ml = max(1, int(w * edge_margin))
            mr = max(1, int(w * edge_margin))
            valid = col_sum[ml:w - mr]
            if len(valid) > 0:
                k = max(1, len(valid) // 6)
                top_idx = np.argpartition(valid, -k)[-k:]
                jitter = int(rng.uniform(-rand_jitter, rand_jitter) * w)
                idx = top_idx[rng.randint(len(top_idx))]
                split = x0 + ml + idx + jitter
                split = max(x0 + min_cell, min(x1 - min_cell, split))
            else:
                split = x0 + w // 2
            recurse(x0, y0, split, y1, depth + 1, pier=pier)
            recurse(split, y0, x1, y1, depth + 1, pier=pier)
        else:
            row_sum = np.abs(grad_y[y0:y1, x0:x1]).sum(axis=1)
            mt = max(1, int(h * edge_margin))
            mb = max(1, int(h * edge_margin))
            valid = row_sum[mt:h - mb]
            if len(valid) > 0:
                k = max(1, len(valid) // 6)
                top_idx = np.argpartition(valid, -k)[-k:]
                jitter = int(rng.uniform(-rand_jitter, rand_jitter) * h)
                idx = top_idx[rng.randint(len(top_idx))]
                split = y0 + mt + idx + jitter
                split = max(y0 + min_cell, min(y1 - min_cell, split))
            else:
                split = y0 + h // 2
            recurse(x0, y0, x1, split, depth + 1, pier=pier)
            recurse(x0, split, x1, y1, depth + 1, pier=pier)

    # ── PIER INJECTION ──
    pier_xs = cfg.get('pier_xs', [0.32, 0.62])
    pier_widths = cfg.get('pier_widths', [0.13, 0.16])
    pier_y_top = cfg.get('pier_y_top', 0.18)

    pier_bounds = []
    for px, pw in zip(pier_xs, pier_widths):
        cx = int(px * W)
        hw = int(pw * W / 2)
        x0 = max(0, cx - hw)
        x1 = min(W, cx + hw)
        y0 = int(pier_y_top * H)
        y1 = H
        pier_bounds.append((x0, y0, x1, y1))

    pier_bounds.sort(key=lambda b: b[0])

    cur_x = 0
    for (px0, py0, px1, py1) in pier_bounds:
        if cur_x < px0:
            recurse(cur_x, 0, px0, H, 0, pier=False)
        if py0 > 0:
            recurse(px0, 0, px1, py0, 0, pier=False)
        recurse(px0, py0, px1, py1, 0, pier=True)
        cur_x = px1
    if cur_x < W:
        recurse(cur_x, 0, W, H, 0, pier=False)

    # Build quantized image with VELOCITY TINTING per cell
    velocity_tint = cfg.get('velocity_tint', 0.40)
    vmag_norm = vmag / (vmag.max() + 1e-10)
    out = np.copy(color_field)
    for (x0, y0, x1, y1, _d) in cells:
        avg_color = color_field[y0:y1, x0:x1].mean(axis=(0, 1))
        avg_vmag = vmag_norm[y0:y1, x0:x1].mean()
        if velocity_tint > 0:
            v_center = avg_vmag - 0.35
            factor = 1.0 - velocity_tint * v_center
            factor = np.clip(factor, 0.6, 1.15)
            avg_color = np.clip(avg_color * factor, 0, 1)
        out[y0:y1, x0:x1] = avg_color

    return out, cells


# ─── Flow line tracing ──────────────────────────────────────────────

def trace_flow_lines(field, n_lines, steps, step_size, seed=42,
                     focal_pt=None, focal_bias=0.55, secondary_pt=None,
                     secondary_bias=0.25):
    H, W = field.shape
    dPdy = np.gradient(field, axis=0)
    dPdx = np.gradient(field, axis=1)
    vx, vy = dPdy, -dPdx
    mag = np.sqrt(vx ** 2 + vy ** 2) + 1e-10
    vx /= mag
    vy /= mag
    rng = np.random.RandomState(seed)
    paths = []
    for _ in range(n_lines):
        u = rng.random()
        if focal_pt is not None and u < focal_bias:
            fx = np.clip(rng.normal(focal_pt[0] * W, W * 0.16), 0, W - 1)
            fy = np.clip(rng.normal(focal_pt[1] * H, H * 0.14), 0, H - 1)
        elif secondary_pt is not None and u < focal_bias + secondary_bias:
            fx = np.clip(rng.normal(secondary_pt[0] * W, W * 0.13), 0, W - 1)
            fy = np.clip(rng.normal(secondary_pt[1] * H, H * 0.12), 0, H - 1)
        else:
            fx = rng.uniform(0, W - 1)
            fy = rng.uniform(0, H - 1)
        px, py = [fx / W], [fy / H]
        for _ in range(steps):
            ix, iy = int(np.clip(fx, 0, W - 1)), int(np.clip(fy, 0, H - 1))
            fx += vx[iy, ix] * step_size * W
            fy += vy[iy, ix] * step_size * H
            if fx < 1 or fx >= W - 1 or fy < 1 or fy >= H - 1:
                break
            px.append(fx / W)
            py.append(fy / H)
        if len(px) >= 6:
            paths.append((np.array(px), np.array(py)))
    return paths


# ─── Renderer ───────────────────────────────────────────────────────

def render(cfg):
    fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor=MARGIN_COLOR, dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(MARGIN_COLOR)

    cl, cr = ML, 1 - MR
    cb, ct = MB, 1 - MT
    cw, ch = cr - cl, ct - cb

    res_w, res_h = cfg.get('res_w', 1100), cfg.get('res_h', 733)
    fs = cfg.get('field_scale', 5.0)
    fx_arr = np.linspace(0, fs, res_w)
    fy_arr = np.linspace(0, fs * res_h / res_w, res_h)
    FX, FY = np.meshgrid(fx_arr, fy_arr)

    field = field_paired(
        FX, FY,
        complexity=cfg.get('complexity', 0.9),
        offset=cfg.get('offset', 1.5),
        v1_pos=cfg.get('v1_pos', (1.4, 3.4)),
        v1_strength=cfg.get('v1_strength', 1.55),
        v1_radius=cfg.get('v1_radius', 0.21),
        v2_pos=cfg.get('v2_pos', (4.0, 3.1)),
        v2_strength=cfg.get('v2_strength', 0.85),
        v2_radius=cfg.get('v2_radius', 0.30),
        v3_pos=cfg.get('v3_pos', (2.7, 2.4)),
        v3_strength=cfg.get('v3_strength', 0.30),
        v3_radius=cfg.get('v3_radius', 0.55),
        bg_amp=cfg.get('bg_amp', 0.16),
    )

    palette_rgb = [hex_to_rgb(c) for c in cfg['palette']]
    color_field = field_to_colors(field, palette_rgb)

    _, _, vmag = compute_velocity(field)
    vort = compute_vorticity(field)

    color_field_flipped = color_field[::-1]
    field_flipped = field[::-1]
    vmag_flipped = vmag[::-1]
    vort_flipped = vort[::-1]

    quantized, cells = subdivide_mondrian(
        color_field_flipped, field_flipped,
        vmag_flipped, vort_flipped, cfg)
    quantized_disp = quantized[::-1]

    ax.imshow(quantized_disp, extent=[cl, cr, cb, ct], origin='lower',
              aspect='auto', zorder=1, interpolation='nearest')

    # ── Hairline cell boundaries ──
    grid_color_rgb = hex_to_rgb(cfg.get('grid_color', '#0e1218'))
    grid_lw = cfg.get('grid_lw', 0.35)
    grid_alpha_max = cfg.get('grid_alpha_max', 0.32)
    grid_min_area_norm = cfg.get('grid_min_area_norm', 0.0008)

    if grid_alpha_max > 0:
        segs, cols, lws = [], [], []
        max_area = res_w * res_h
        for (x0, y0, x1, y1, _d) in cells:
            cell_area_norm = ((x1 - x0) * (y1 - y0)) / max_area
            if cell_area_norm < grid_min_area_norm:
                continue
            disp_y0 = res_h - y1
            disp_y1 = res_h - y0
            cx0 = cl + (x0 / res_w) * cw
            cy0 = cb + (disp_y0 / res_h) * ch
            cx1 = cl + (x1 / res_w) * cw
            cy1 = cb + (disp_y1 / res_h) * ch
            a_norm = min(1.0, (cell_area_norm / 0.05) ** 0.6)
            alpha = grid_alpha_max * a_norm
            if alpha < 0.015:
                continue
            lw = grid_lw + a_norm * cfg.get('grid_lw_range', 0.6)
            for seg in [[(cx0, cy0), (cx1, cy0)],
                        [(cx1, cy0), (cx1, cy1)],
                        [(cx1, cy1), (cx0, cy1)],
                        [(cx0, cy1), (cx0, cy0)]]:
                segs.append(seg)
                cols.append((*grid_color_rgb, alpha))
                lws.append(lw)
        if segs:
            ax.add_collection(LineCollection(
                segs, colors=cols, linewidths=lws,
                capstyle='butt', zorder=5))

    # ── Flow lines ──
    flow_max_alpha = cfg.get('flow_max_alpha', 0.48)
    flow_max_lw = cfg.get('flow_max_lw', 0.95)
    flow_top_y = cfg.get('flow_top_y', 0.55)
    fc_top = hex_to_rgb(cfg.get('flow_color_top', '#e8eef4'))
    fc_mid = hex_to_rgb(cfg.get('flow_color_mid', '#8898b0'))
    glow_a = cfg.get('glow_alpha_mult', 0.20)
    glow_w = cfg.get('glow_width_mult', 3.8)

    v1_pos = cfg.get('v1_pos', (1.4, 3.4))
    v2_pos = cfg.get('v2_pos', (4.0, 3.1))
    fy_max = fs * res_h / res_w
    focal_pt = (v1_pos[0] / fs, v1_pos[1] / fy_max)
    secondary_pt = (v2_pos[0] / fs, v2_pos[1] / fy_max)

    paths = trace_flow_lines(
        field, cfg.get('n_flow_lines', 1400),
        cfg.get('flow_steps', 250),
        cfg.get('flow_step_size', 0.0035),
        seed=cfg.get('seed', 77),
        focal_pt=focal_pt,
        focal_bias=cfg.get('focal_bias', 0.55),
        secondary_pt=secondary_pt,
        secondary_bias=cfg.get('secondary_bias', 0.25),
    )

    for layer in ('glow', 'core'):
        ss, cc, ww = [], [], []
        for px, py in paths:
            py_disp = 1.0 - py
            ca = cl + px * cw
            cb_arr = cb + py_disp * ch
            pts = np.column_stack([ca, cb_arr]).reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            ns = len(segs)
            pf = np.sin(np.linspace(0, np.pi, ns)) ** 0.5
            for si in range(ns):
                my = (py_disp[si] + py_disp[si + 1]) / 2
                if my > flow_top_y:
                    va = 1.0
                else:
                    t = my / flow_top_y if flow_top_y > 0 else 0
                    va = t ** 2
                bl = np.clip(my, 0, 1)
                r = fc_mid[0] * (1 - bl) + fc_top[0] * bl
                g = fc_mid[1] * (1 - bl) + fc_top[1] * bl
                b = fc_mid[2] * (1 - bl) + fc_top[2] * bl
                f = pf[si] * va
                if layer == 'glow':
                    a, w = flow_max_alpha * glow_a * f, flow_max_lw * glow_w * f
                else:
                    a, w = flow_max_alpha * f, flow_max_lw * f
                if a < 0.003:
                    continue
                ss.append(segs[si])
                cc.append((r, g, b, min(a, 1.0)))
                ww.append(max(w, 0.1))
        if ss:
            ax.add_collection(LineCollection(
                ss, colors=cc, linewidths=ww,
                capstyle='round', joinstyle='round',
                zorder=3 if layer == 'glow' else 4))

    da = cfg.get('diag_alpha', 0.07)
    if da > 0:
        dc = cfg.get('diag_color', '#a0a8b8')
        ax.plot([cl, cr], [ct, cb], color=dc, lw=0.5, alpha=da, zorder=7)
        ax.plot([cl, cr], [cb, ct], color=dc, lw=0.5, alpha=da, zorder=7)

    # Signature in the bottom margin
    add_signature(fig, ax, MARGIN_COLOR, margin_piece=True,
                  margin_bottom=FIG_H * 0.08)

    return fig


# ─── Configuration: V10 — Full Synthesis ────────────────────────────
# Drama palette, two piers, dissolved horizon, max velocity encoding.
# Reproduces comp_v9_10.jpg from scripts/wonder_comprehension_v9.py.

PAL_DRAMA = ['#0a1018', '#1c2838', '#2a4068', '#3870b0', '#6098c8',
             '#9ec0d8', '#d0e0e8', '#f0f4f8']

CONFIG = {
    'palette': PAL_DRAMA,
    'res_w': 1100, 'res_h': 733,
    'field_scale': 5.0,
    'complexity': 0.9, 'offset': 1.5, 'bg_amp': 0.16,
    'v1_pos': (1.4, 3.4), 'v1_strength': 1.65, 'v1_radius': 0.21,
    'v2_pos': (4.0, 3.1), 'v2_strength': 0.85, 'v2_radius': 0.30,
    'v3_pos': (2.7, 2.4), 'v3_strength': 0.30, 'v3_radius': 0.55,
    # Soft horizon (v9 default)
    'max_depth_top': 10, 'max_depth_bot': 5,
    'depth_power': 0.95, 'min_cell': 3,
    'edge_margin': 0.22, 'split_jitter': 0.10,
    'vort_depth_bias': 1.6,
    'velocity_tint': 0.50,
    # Vertical aspect bias band
    'vbias_top': 0.35, 'vbias_bot': 0.78, 'vbias_strength': 0.65,
    # Pier injection — two piers
    'pier_xs': [0.32, 0.62], 'pier_widths': [0.15, 0.13],
    'pier_y_top': 0.13, 'pier_depth': 3,
    # Grid hairlines
    'grid_color': '#0e1218', 'grid_lw': 0.35, 'grid_alpha_max': 0.32,
    'grid_lw_range': 0.65, 'grid_min_area_norm': 0.0008,
    # Flow lines — punchy
    'n_flow_lines': 1700, 'flow_steps': 250, 'flow_step_size': 0.0035,
    'flow_max_alpha': 0.52, 'flow_max_lw': 0.95, 'flow_top_y': 0.50,
    'flow_color_top': '#e8eef4', 'flow_color_mid': '#8898b0',
    'glow_alpha_mult': 0.20, 'glow_width_mult': 3.8,
    'focal_bias': 0.55, 'secondary_bias': 0.25,
    'seed': 99,
    'diag_alpha': 0.07, 'diag_color': '#a0a8b8',
}


if __name__ == '__main__':
    print("═══ Comprehending: Clarity ═══")

    fig = render(CONFIG)
    pdf_path = os.path.join(OUTPUT_DIR, "comprehending_clarity.pdf")
    fig.savefig(pdf_path, format='pdf', facecolor=MARGIN_COLOR, dpi=DPI)
    print(f"  saved {pdf_path}")
    jpg_path = os.path.join(PRINT_DIR, "comprehending_clarity.jpg")
    fig.savefig(jpg_path, facecolor=MARGIN_COLOR, dpi=DPI,
                pil_kwargs={"quality": 96})
    print(f"  saved {jpg_path}")
    plt.close(fig)

    print("═══ Done ═══")
