"""
Geometry of Feeling — Wonder: Strata (Deep Time)
Geological strata with irregular fault displacement, non-uniform layer spacing,
event layers, and depth-dependent erosion. The impossible scale of Earth's history.
"""

import os
import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import FancyBboxPatch, Rectangle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
CONTENT_BG = "#0A0A18"
MARGIN_COLOR = "#CCC2AA"

# Strata line palette: vivid cosmic teal -> violet -> earth -> gold
PALETTE = [
    "#50A0D0", "#7868D0", "#C06060", "#D09040",
    "#E0B830", "#F0D040", "#F8E070"
]

# Event layers — singular geological events
EVENT_LAYERS = [
    {"index": 10, "color": "#F0D060", "alpha": 0.75, "width": 1.4},
    {"index": 35, "color": "#8090B0", "alpha": 0.55, "width": 0.9},
    {"index": 55, "color": "#FFE070", "alpha": 0.7, "width": 1.3},
    {"index": 75, "color": "#F0D060", "alpha": 0.65, "width": 1.3},
    {"index": 90, "color": "#C08040", "alpha": 0.5, "width": 1.0},
]

NUM_LAYERS = 100
FAULT_SEED = 120
NUM_FAULTS = 5
WAVE_AMP = 1.3
BREAK_DENSITY = 0.015

# Extra manual fault: dramatic right-side drop
EXTRA_FAULTS = [{"x": 0.75, "drop": 50, "sharpness": 4}]

# Margin fractions (matching other wonder pieces)
ML, MR, MB, MT = 0.07, 0.07, 0.08, 0.08


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def lerp_color(c1, c2, t):
    r1 = hex_to_rgb(c1)
    r2 = hex_to_rgb(c2)
    return tuple(r1[i] + (r2[i] - r1[i]) * t for i in range(3))


def get_grad_color(colors, t):
    t = max(0.0, min(1.0, t))
    n = len(colors) - 1
    i = min(int(t * n), n - 1)
    local_t = t * n - i
    return lerp_color(colors[i], colors[i + 1], local_t)


class SeededRandom:
    def __init__(self, seed=42):
        self.seed = seed

    def rand(self):
        self.seed = (self.seed * 16807) % 2147483647
        return self.seed / 2147483647


def render():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=MARGIN_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(MARGIN_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Full-canvas margin background
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=MARGIN_COLOR,
                            edgecolor='none', zorder=-10))

    # Content rectangle
    content_rect = FancyBboxPatch(
        (ML, MB), 1 - ML - MR, 1 - MB - MT,
        boxstyle="square,pad=0",
        facecolor=CONTENT_BG, edgecolor='none', zorder=0)
    ax.add_patch(content_rect)

    rng = SeededRandom(FAULT_SEED)

    # ── Generate random faults ──
    faults = []
    for _ in range(NUM_FAULTS):
        faults.append({
            "x": 0.08 + rng.rand() * 0.84,
            "baseDrop": 8 + rng.rand() * 22,
            "sharpness": 3 + rng.rand() * 8,
            "direction": 1 if rng.rand() > 0.25 else -1,
            "layerVar": 0.15 + rng.rand() * 0.35,
            "depthStart": rng.rand() * 0.3,
            "depthEnd": 0.7 + rng.rand() * 0.3,
        })

    # Add extra manual faults
    for ef in EXTRA_FAULTS:
        faults.append({
            "x": ef["x"],
            "baseDrop": ef["drop"],
            "sharpness": ef.get("sharpness", 4),
            "direction": 1,
            "layerVar": ef.get("layerVar", 0.2),
            "depthStart": ef.get("depthStart", 0),
            "depthEnd": ef.get("depthEnd", 1),
        })

    faults.sort(key=lambda f: f["x"])

    # ── Non-uniform layer spacing ──
    rng2 = SeededRandom(FAULT_SEED + 1000)
    rates = []
    accum = 0
    for i in range(NUM_LAYERS):
        era = (np.sin(i * 0.08) * 0.5 + np.sin(i * 0.23) * 0.3
               + np.sin(i * 0.51) * 0.2)
        rate = 0.5 + (era + 1) * 0.75
        rates.append(rate)
        accum += rate

    # Content area bounds (in figure-fraction coords)
    content_top = 1 - MT
    content_bottom = MB
    content_h = content_top - content_bottom
    pad_y = content_h * 0.08
    draw_top = content_top - pad_y
    draw_bottom = content_bottom + pad_y
    draw_range = draw_top - draw_bottom

    positions = []
    pos = 0
    for i in range(NUM_LAYERS):
        positions.append(draw_top - (pos / accum) * draw_range)
        pos += rates[i]

    # ── Per-layer random values ──
    rng3 = SeededRandom(FAULT_SEED + 2000)
    layer_fault_offsets = []
    layer_break_seeds = []
    for i in range(NUM_LAYERS):
        offsets = []
        for _ in range(len(faults)):
            offsets.append((rng3.rand() - 0.5) * 2)
        layer_fault_offsets.append(offsets)
        layer_break_seeds.append(rng3.rand() * 10000)

    # ── Draw strata ──
    # Use normalized coords: x in [0, 1], y in [0, 1]
    # Content area: x in [ML, 1-MR], y in [MB, 1-MT]
    x_arr = np.linspace(0, 1, 2000)

    for i in range(NUM_LAYERS):
        t = i / NUM_LAYERS  # depth: 0=top (youngest), 1=bottom (oldest)
        base_y = positions[i]
        depth_factor = t

        # Check for event layer
        event = None
        for ev in EVENT_LAYERS:
            if ev["index"] == i:
                event = ev
                break

        if event:
            rgb = hex_to_rgb(event["color"])
            alpha = event.get("alpha", 0.65)
            line_width = event.get("width", 1.3)
        else:
            rgb = get_grad_color(PALETTE, t)
            alpha = 0.35 + (1 - depth_factor) * 0.55
            wv = np.sin(i * 1.7) * 0.25 + np.sin(i * 4.3) * 0.1
            line_width = max(0.5, min(1.6,
                                       0.7 + (1 - depth_factor) * 0.5 + wv * 0.4))

        # Compute y positions
        sd = i * 137.5
        jagged = 0.4 + depth_factor * 0.8
        amp = WAVE_AMP

        y_arr = np.full_like(x_arr, base_y)

        # Fault shifts
        for fi, f in enumerate(faults):
            fx = f["x"]
            if t < f["depthStart"] or t > f["depthEnd"]:
                continue
            depth_mid = (f["depthStart"] + f["depthEnd"]) / 2
            depth_range = (f["depthEnd"] - f["depthStart"]) / 2
            if depth_range == 0:
                depth_env = 1.0
            else:
                depth_env = 1 - ((t - depth_mid) / depth_range) ** 2
            layer_off = layer_fault_offsets[i][fi] if fi < len(layer_fault_offsets[i]) else 0
            layer_drop = f["baseDrop"] * (1 + layer_off * f["layerVar"])
            drop = layer_drop * f["direction"] * depth_env
            # Convert pixel-scale drop to figure-fraction
            # At 480px canvas height, 50px drop ≈ 0.104. Scale similarly.
            drop_frac = drop / 480 * content_h
            y_arr -= drop_frac * (0.5 + 0.5 * np.tanh((x_arr - fx) / (f["sharpness"] / 700)))

        # Wave displacement (scaled to figure coords)
        wave_scale = content_h / 480 * 4
        y_arr += (4 * amp * wave_scale) * np.sin(0.005 * x_arr * 700 + sd)
        y_arr += (2.2 * amp * wave_scale) * np.sin(0.015 * x_arr * 700 + sd * 1.3)
        y_arr += (0.9 * amp * jagged * wave_scale) * np.sin(0.04 * x_arr * 700 + sd * 2.0)
        y_arr += (0.35 * amp * jagged * wave_scale) * np.sin(0.1 * x_arr * 700 + sd * 3.7)

        # Create segments with breaks
        break_seed = layer_break_seeds[i]
        break_thresh = 1 - BREAK_DENSITY * (1 + depth_factor * 2)

        # Compute break mask
        break_vals = np.sin(x_arr * 700 * 0.13 + break_seed) * 43758.5453
        break_frac = break_vals - np.floor(break_vals)
        mask = break_frac <= break_thresh

        # Also clip to content area
        mask &= (x_arr >= ML) & (x_arr <= 1 - MR)
        mask &= (y_arr >= MB) & (y_arr <= 1 - MT)

        # Split into continuous segments
        segments = []
        in_seg = False
        start = 0
        for j in range(len(mask)):
            if mask[j] and not in_seg:
                start = j
                in_seg = True
            elif not mask[j] and in_seg:
                if j - start >= 2:
                    segments.append((x_arr[start:j], y_arr[start:j]))
                in_seg = False
        if in_seg and len(x_arr) - start >= 2:
            segments.append((x_arr[start:], y_arr[start:]))

        # Draw segments using LineCollection
        for xs, ys in segments:
            pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            color_with_alpha = (rgb[0], rgb[1], rgb[2], alpha)
            lc = mc.LineCollection(segs, linewidths=line_width,
                                   colors=[color_with_alpha],
                                   capstyle='round', joinstyle='round',
                                   zorder=1 + i * 0.01)
            ax.add_collection(lc)

    # ── Save ──
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "wonder_strata.pdf")
    add_signature(fig, ax, MARGIN_COLOR, margin_piece=True, margin_bottom=FIG_H * 0.08)
    fig.savefig(pdf_path, facecolor=MARGIN_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
