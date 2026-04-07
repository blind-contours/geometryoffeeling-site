"""
Geometry of Feeling — Comprehending: Gravity

The right wing of the Comprehension triptych — warm oxblood, the
"dissolution" pole. Vortices orbit the edges; a quiet block-basin holds
the center. The dynamic is radial: shallow at the center, deep at the
edges. The streamlines literally crystallize INTO the block layer
through density-driven cell color blending and depth subdivision —
flow becomes ground rather than sitting on top of it.

Mechanism (triptych grammar — different from left/center pier grammar):
  - Recursive feature-driven Mondrian subdivision driven by scalar field
    gradients, with a configurable depth axis (here: radial — shallow
    at center, deep at the edges).
  - Streamlines are rasterized into a density buffer that feeds back
    into the subdivide step: dense flow regions get a depth bonus, and
    cells inherit a cream tint where flow accumulates. The flow LITERALLY
    becomes the block layer.
  - Velocity-tinted per-cell quantization.
  - Bottom floor: streamlines fade across the bottom band so the block
    layer can hold a horizon line — the ground is being LOST, not absent.
  - Extra accents: explicit dark singularity at the dominant vortex and
    two near-black anchors in the bottom row for tonal range.

This script reproduces the exact configuration of "RIGHT_PANEL" from
scripts/wonder_comprehension_triptych.py.
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
from scipy.ndimage import gaussian_filter

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


def rasterize_paths(paths, W, H, blur_sigma=2.5):
    """Rasterize streamline paths into a density buffer aligned with
    color_field_flipped (row 0 = top of display, row H-1 = bottom)."""
    buf = np.zeros((H, W), dtype=np.float32)
    for px, py in paths:
        if len(px) < 2:
            continue
        xi = np.clip((px * W).astype(np.int32), 0, W - 1)
        yi = np.clip(((1 - py) * H).astype(np.int32), 0, H - 1)
        for k in range(len(xi) - 1):
            x0, y0 = int(xi[k]), int(yi[k])
            x1, y1 = int(xi[k + 1]), int(yi[k + 1])
            n = max(abs(x1 - x0), abs(y1 - y0), 1)
            xs = np.linspace(x0, x1, n + 1).astype(np.int32)
            ys = np.linspace(y0, y1, n + 1).astype(np.int32)
            buf[ys, xs] += 1.0
    if blur_sigma > 0:
        buf = gaussian_filter(buf, sigma=blur_sigma)
    m = buf.max()
    if m > 0:
        buf /= m
    return buf


# ─── Mondrian subdivision with depth_axis + flow crystallization ────

def subdivide_mondrian(color_field, scalar_field, vmag, vort, cfg,
                       flow_density=None):
    H, W, _ = color_field.shape
    grad_y, grad_x = np.gradient(scalar_field)

    max_depth_top = cfg.get('max_depth_top', 10)
    max_depth_bot = cfg.get('max_depth_bot', 4)
    depth_power = cfg.get('depth_power', 1.1)
    depth_axis = cfg.get('depth_axis', 'y')
    radial_cx = cfg.get('radial_cx', 0.5)
    radial_cy = cfg.get('radial_cy', 0.5)
    min_cell = cfg.get('min_cell', 3)
    edge_margin = cfg.get('edge_margin', 0.22)
    vort_depth_bias = cfg.get('vort_depth_bias', 1.2)
    density_depth_bias = cfg.get('density_depth_bias', 0.0)
    rng = np.random.RandomState(cfg.get('seed', 77))
    rand_jitter = cfg.get('split_jitter', 0.10)

    aspect = H / W
    r_max_norm = np.sqrt(1 + aspect * aspect)

    vort_norm = vort / (vort.max() + 1e-10)
    cells = []

    def depth_for_cell(xc_norm, yc_norm, vort_avg, density_avg=0.0):
        if depth_axis == 'y':
            s = yc_norm ** depth_power
        elif depth_axis == 'x_right':
            s = xc_norm ** depth_power
        elif depth_axis == 'radial':
            dx = (xc_norm - radial_cx) * 2
            dy = (yc_norm - radial_cy) * 2 * aspect
            r = np.sqrt(dx * dx + dy * dy) / r_max_norm
            r = min(r, 1.0)
            s = (1 - r) ** depth_power
        else:
            s = yc_norm ** depth_power
        base = max_depth_top * (1 - s) + max_depth_bot * s
        bonus = vort_depth_bias * vort_avg * (max_depth_top - max_depth_bot)
        d_bonus = density_depth_bias * density_avg * (max_depth_top - max_depth_bot)
        return int(round(base + bonus + d_bonus))

    def recurse(x0, y0, x1, y1, depth):
        w, h = x1 - x0, y1 - y0
        xc_norm = (x0 + x1) / 2 / W
        yc_norm = (y0 + y1) / 2 / H
        cell_vort = vort_norm[y0:y1, x0:x1].mean()
        if flow_density is not None:
            cell_density = float(flow_density[y0:y1, x0:x1].mean())
        else:
            cell_density = 0.0
        max_d = depth_for_cell(xc_norm, yc_norm, cell_vort, cell_density)

        if depth >= max_d or w < min_cell * 2 or h < min_cell * 2:
            cells.append((x0, y0, x1, y1, depth))
            return

        if w >= h * 1.4:
            split_dir = 'v'
        elif h >= w * 1.4:
            split_dir = 'h'
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
            recurse(x0, y0, split, y1, depth + 1)
            recurse(split, y0, x1, y1, depth + 1)
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
            recurse(x0, y0, x1, split, depth + 1)
            recurse(x0, split, x1, y1, depth + 1)

    recurse(0, 0, W, H, 0)

    # Velocity-tinted per-cell quantization with flow-density crystallization
    velocity_tint = cfg.get('velocity_tint', 0.40)
    flow_blend_mult = cfg.get('flow_blend_mult', 0.0)
    flow_blend_gamma = cfg.get('flow_blend_gamma', 1.0)
    flow_cream_rgb = np.array(hex_to_rgb(cfg.get('flow_cream_color',
                                                 cfg.get('flow_color_top', '#e8eef4'))))
    vmag_norm = vmag / (vmag.max() + 1e-10)
    out = np.copy(color_field)
    for (x0, y0, x1, y1, _d) in cells:
        avg_color = color_field[y0:y1, x0:x1].mean(axis=(0, 1))
        avg_vmag = vmag_norm[y0:y1, x0:x1].mean()
        if flow_density is not None and flow_blend_mult > 0:
            avg_density = float(flow_density[y0:y1, x0:x1].mean())
            blend = min(1.0, (avg_density ** flow_blend_gamma) * flow_blend_mult)
            avg_color = avg_color * (1 - blend) + flow_cream_rgb * blend
        if velocity_tint > 0:
            v_center = avg_vmag - 0.35
            factor = 1.0 - velocity_tint * v_center
            factor = np.clip(factor, 0.6, 1.15)
            avg_color = np.clip(avg_color * factor, 0, 1)
        out[y0:y1, x0:x1] = avg_color

    # Extra accents — dark singularity + bottom-row anchors
    extra_accents = cfg.get('extra_accents', [])
    for ea in extra_accents:
        ex_pos = ea.get('pos')
        if ex_pos is None:
            continue
        ex_target = ex_pos[0] * W
        ey_target = ex_pos[1] * H
        ex_min_area = ea.get('min_area', 0.002)
        ex_min_area_px = ex_min_area * W * H
        best = None
        best_d2 = float('inf')
        for (x0, y0, x1, y1, _d) in cells:
            area = (x1 - x0) * (y1 - y0)
            if area < ex_min_area_px:
                continue
            cxp = (x0 + x1) / 2
            cyp = (y0 + y1) / 2
            d2 = (cxp - ex_target) ** 2 + (cyp - ey_target) ** 2
            if d2 < best_d2:
                best_d2 = d2
                best = (x0, y0, x1, y1)
        if best is not None:
            ec = np.array(hex_to_rgb(ea.get('color', '#000000')))
            x0, y0, x1, y1 = best
            out[y0:y1, x0:x1] = ec

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
            fx = np.clip(rng.normal(focal_pt[0] * W, W * 0.18), 0, W - 1)
            fy = np.clip(rng.normal(focal_pt[1] * H, H * 0.16), 0, H - 1)
        elif secondary_pt is not None and u < focal_bias + secondary_bias:
            fx = np.clip(rng.normal(secondary_pt[0] * W, W * 0.16), 0, W - 1)
            fy = np.clip(rng.normal(secondary_pt[1] * H, H * 0.14), 0, H - 1)
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

    # Trace streamlines first so we can rasterize them and feed the
    # density into the subdivide step (flow crystallizes into blocks).
    flow_focal_pt = cfg.get('flow_focal_pt')
    flow_secondary_pt = cfg.get('flow_secondary_pt')
    paths = trace_flow_lines(
        field, cfg.get('n_flow_lines', 1500),
        cfg.get('flow_steps', 250),
        cfg.get('flow_step_size', 0.0035),
        seed=cfg.get('seed', 77),
        focal_pt=flow_focal_pt,
        focal_bias=cfg.get('focal_bias', 0.55),
        secondary_pt=flow_secondary_pt,
        secondary_bias=cfg.get('secondary_bias', 0.25),
    )

    flow_density = rasterize_paths(
        paths, res_w, res_h,
        blur_sigma=cfg.get('density_blur_sigma', 2.5))

    quantized, cells = subdivide_mondrian(
        color_field_flipped, field_flipped,
        vmag_flipped, vort_flipped, cfg,
        flow_density=flow_density)
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

    # ── Flow lines overlay ──
    flow_max_alpha = cfg.get('flow_max_alpha', 0.48)
    flow_max_lw = cfg.get('flow_max_lw', 0.95)
    flow_top_y = cfg.get('flow_top_y', 0.55)
    flow_fade_mode = cfg.get('flow_fade_mode', 'top')
    radial_cx = cfg.get('radial_cx', 0.5)
    radial_cy = cfg.get('radial_cy', 0.5)
    fc_top = hex_to_rgb(cfg.get('flow_color_top', '#e8eef4'))
    fc_mid = hex_to_rgb(cfg.get('flow_color_mid', '#8898b0'))
    glow_a = cfg.get('glow_alpha_mult', 0.20)
    glow_w = cfg.get('glow_width_mult', 3.8)

    draw_flow_overlay = cfg.get('draw_flow_overlay', True)
    paths_draw = paths if draw_flow_overlay else []

    for layer in ('glow', 'core'):
        ss, cc, ww = [], [], []
        for px, py in paths_draw:
            py_disp = 1.0 - py
            ca = cl + px * cw
            cb_arr = cb + py_disp * ch
            pts = np.column_stack([ca, cb_arr]).reshape(-1, 1, 2)
            segs_arr = np.concatenate([pts[:-1], pts[1:]], axis=1)
            ns = len(segs_arr)
            pf = np.sin(np.linspace(0, np.pi, ns)) ** 0.5
            for si in range(ns):
                mx = (px[si] + px[si + 1]) / 2
                my_disp = (py_disp[si] + py_disp[si + 1]) / 2
                if flow_fade_mode == 'top':
                    if my_disp > flow_top_y:
                        va = 1.0
                    else:
                        t = my_disp / flow_top_y if flow_top_y > 0 else 0
                        va = t ** 2
                elif flow_fade_mode == 'left':
                    fade_start = flow_top_y
                    fade_exp = cfg.get('flow_fade_exp', 0.9)
                    if mx < fade_start:
                        va = 1.0
                    else:
                        t = (1 - mx) / (1 - fade_start) if fade_start < 1 else 0
                        va = max(t, 0) ** fade_exp
                elif flow_fade_mode == 'radial_edge':
                    dx = (mx - radial_cx) * 2
                    dy = (my_disp - radial_cy) * 2
                    r = np.sqrt(dx * dx + dy * dy)
                    inner = flow_top_y
                    if r > inner:
                        va = 1.0
                    else:
                        t = r / inner if inner > 0 else 0
                        va = t ** 1.6
                else:
                    va = 1.0
                # Bottom floor — protect the bottom band of display
                # from streamlines so a baseline of blocks shows through.
                bottom_floor = cfg.get('flow_bottom_floor', 0.0)
                if bottom_floor > 0 and my_disp < bottom_floor:
                    bf = (my_disp / bottom_floor) ** 1.5
                    va *= bf
                bl = np.clip(my_disp, 0, 1)
                r_c = fc_mid[0] * (1 - bl) + fc_top[0] * bl
                g_c = fc_mid[1] * (1 - bl) + fc_top[1] * bl
                b_c = fc_mid[2] * (1 - bl) + fc_top[2] * bl
                f = pf[si] * va
                if layer == 'glow':
                    a, w = flow_max_alpha * glow_a * f, flow_max_lw * glow_w * f
                else:
                    a, w = flow_max_alpha * f, flow_max_lw * f
                if a < 0.003:
                    continue
                ss.append(segs_arr[si])
                cc.append((r_c, g_c, b_c, min(a, 1.0)))
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


# ─── Configuration: Right Panel — "Proof from the Center" ──────────
# Warm oxblood. Vortices orbit the edges; quiet block-basin in the center.
# Flow crystallizes into the block layer via density-driven blending and
# depth bonus. Reproduces comp_triptych_right.jpg from
# scripts/wonder_comprehension_triptych.py.

PAL_OXBLOOD = [
    '#160806',   # near black with red undertone
    '#2a1410',   # deep oxblood shadow
    '#4a1e1a',   # oxblood
    '#6e2a18',   # burnt umber
    '#9a4524',   # burnt sienna
    '#bd6a42',   # terracotta
    '#d89070',   # soft clay
    '#f0d8b8',   # warm bone
]

CONFIG = {
    'palette': PAL_OXBLOOD,
    'res_w': 1100, 'res_h': 733,
    'field_scale': 5.0,
    'complexity': 0.9, 'offset': 1.5, 'bg_amp': 0.12,
    'depth_axis': 'radial',
    'depth_power': 0.85,
    'max_depth_top': 9, 'max_depth_bot': 4,
    'min_cell': 3,
    'edge_margin': 0.22, 'split_jitter': 0.10,
    'radial_cx': 0.50, 'radial_cy': 0.52,
    # One dominant attractor + two clearly subordinate vortices.
    'v1_pos': (0.55, 2.95), 'v1_strength': 1.95, 'v1_radius': 0.21,
    'v2_pos': (4.45, 2.90), 'v2_strength': 0.78, 'v2_radius': 0.30,
    'v3_pos': (2.50, 0.30), 'v3_strength': 0.55, 'v3_radius': 0.38,
    # Flow concentrates on v1, with right-corner vortex as quiet secondary.
    'flow_focal_pt': (0.12, 0.22),    # upper-left vortex on display
    'flow_secondary_pt': (0.88, 0.25),
    'focal_bias': 0.58, 'secondary_bias': 0.15,
    'flow_fade_mode': 'radial_edge',
    'flow_top_y': 0.42,    # inner radius — inside this, streams fade
    # Baseline protection: streamlines fade across the bottom 22% so
    # the block layer holds a ground line. The ground is being LOST.
    'flow_bottom_floor': 0.22,
    'n_flow_lines': 1400, 'flow_steps': 260, 'flow_step_size': 0.0035,
    'flow_max_alpha': 0.12,
    'flow_max_lw': 0.85,
    'velocity_tint': 0.48, 'vort_depth_bias': 1.4,
    # Flow crystallizes into the block layer.
    'flow_blend_mult': 4.2,
    'flow_blend_gamma': 0.7,
    'flow_cream_color': '#f0d8b8',
    'density_depth_bias': 1.8,
    'density_blur_sigma': 2.2,
    'draw_flow_overlay': True,
    # Streamline colors warm to harmonize with oxblood
    'flow_color_top': '#f0e8dc',
    'flow_color_mid': '#b89880',
    'glow_alpha_mult': 0.20, 'glow_width_mult': 3.8,
    # Dark anchors — singularity at v1 + two near-black bottom-row cells.
    'extra_accents': [
        {'pos': (0.22, 0.22), 'color': '#020203', 'min_area': 0.002},
        {'pos': (0.38, 0.94), 'color': '#080202', 'min_area': 0.004},
        {'pos': (0.66, 0.93), 'color': '#080202', 'min_area': 0.004},
    ],
    'grid_color': '#1a0c08', 'grid_lw': 0.35, 'grid_alpha_max': 0.32,
    'grid_lw_range': 0.65, 'grid_min_area_norm': 0.0008,
    'seed': 61,
    'diag_alpha': 0.07, 'diag_color': '#a0a8b8',
}


if __name__ == '__main__':
    print("═══ Comprehending: Gravity ═══")

    fig = render(CONFIG)
    pdf_path = os.path.join(OUTPUT_DIR, "comprehending_gravity.pdf")
    fig.savefig(pdf_path, format='pdf', facecolor=MARGIN_COLOR, dpi=DPI)
    print(f"  saved {pdf_path}")
    jpg_path = os.path.join(PRINT_DIR, "comprehending_gravity.jpg")
    fig.savefig(jpg_path, facecolor=MARGIN_COLOR, dpi=DPI,
                pil_kwargs={"quality": 96})
    print(f"  saved {jpg_path}")
    plt.close(fig)

    print("═══ Done ═══")
