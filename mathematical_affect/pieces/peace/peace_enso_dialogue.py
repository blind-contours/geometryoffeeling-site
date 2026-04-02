"""
Geometry of Feeling — Peace: Enso Dialogue

Two imperfect circles, ocean and sage, overlapping like two people
in conversation. They weave over and under each other at the crossings —
neither one dominates. The brush stroke thickens with confidence,
tapers at the gap. Each circle is its own breath, its own arc,
but they share the space between them.

Parametric enso with pressure-based brush simulation, interleaved z-ordering.
"""

import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W, FIG_H = 12, 8
BG = "#F0EDE8"

# Standard Peace series margins
PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R
PH = FIG_H - PAD_T - PAD_B
CX = PAD_L + PW / 2
CY = PAD_B + PH / 2

OCEAN = "#3A5A6A"
DEEP_SAGE = "#4A6A52"


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))


def generate_circle(circle, rng):
    """Generate circle geometry and brush properties."""
    center_x = CX + circle['cx_off'] * PW
    center_y = CY + circle['cy_off'] * PH
    base_r = min(PW, PH) * circle['r_frac']

    gap_center = circle['gap_pos']
    gap_half = circle['gap_size'] / 2
    theta = np.linspace(gap_center + gap_half, gap_center + 2*np.pi - gap_half, 8000)

    # Low-frequency noise for imperfect circularity
    r_noise = np.zeros_like(theta)
    for freq in [1, 2, 3, 5, 8]:
        amp = 0.025 * base_r / (freq ** 0.7)
        phase = rng.uniform(0, 2*np.pi)
        r_noise += amp * np.sin(freq * theta + phase)
    r = base_r + r_noise

    xs = center_x + r * np.cos(theta)
    ys = center_y + r * np.sin(theta)

    # Brush pressure envelope: attack → sustain → release + tremor
    t = np.linspace(0, 1, len(theta))
    attack = np.clip(t / 0.12, 0, 1) ** 0.6
    sustain = 0.85 + 0.15 * np.sin(4 * np.pi * t + rng.uniform(0, np.pi))
    release = np.clip((1 - t) / 0.18, 0, 1) ** 0.4
    tremor = 1.0 + 0.06 * np.sin(30 * np.pi * t + rng.uniform(0, 10))
    pressure = attack * sustain * release * tremor

    lws = circle['lw_max'] * pressure
    alphas = circle['alpha_max'] * pressure ** 0.35

    # Clip to art area
    mask = ((xs >= PAD_L + 0.05) & (xs <= FIG_W - PAD_R - 0.05) &
            (ys >= PAD_B + 0.05) & (ys <= FIG_H - PAD_T - 0.05))
    return xs[mask], ys[mask], lws[mask], alphas[mask]


def draw_circle_weave(ax, xs, ys, lws, alphas, col, y_threshold, front_above):
    """Draw a circle with interleaved z-ordering at crossings.

    front_above=True: this circle renders in front when y > y_threshold.
    """
    for i in range(len(xs) - 1):
        mid_y = (ys[i] + ys[i+1]) / 2
        above = mid_y > y_threshold

        if (above and front_above) or (not above and not front_above):
            zo_s, zo_m = 5, 6  # front
        else:
            zo_s, zo_m = 2, 3  # back

        seg = np.array([[[xs[i], ys[i]], [xs[i+1], ys[i+1]]]])

        # Shadow
        seg_s = np.array([[[xs[i]+0.025, ys[i]-0.025],
                           [xs[i+1]+0.025, ys[i+1]-0.025]]])
        lc_s = mc.LineCollection(seg_s, linewidths=[lws[i]*1.4],
                                 colors=[rgba(col, alphas[i] * 0.06)],
                                 capstyle='round', joinstyle='round', zorder=zo_s)
        ax.add_collection(lc_s)

        # Main stroke
        lc = mc.LineCollection(seg, linewidths=[lws[i]],
                               colors=[rgba(col, alphas[i])],
                               capstyle='round', joinstyle='round', zorder=zo_m)
        ax.add_collection(lc)


def render():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')

    rng = np.random.default_rng(42)

    # Two circles: ocean (left, larger) and sage (right, smaller)
    circle_blue = dict(cx_off=-0.12, cy_off=0.02, r_frac=0.32, gap_pos=2.3,
                       gap_size=0.5, col=OCEAN, lw_max=7.0, alpha_max=0.65)
    circle_green = dict(cx_off=0.10, cy_off=-0.03, r_frac=0.28, gap_pos=1.0,
                        gap_size=0.45, col=DEEP_SAGE, lw_max=6.0, alpha_max=0.55)

    xs_b, ys_b, lws_b, alphas_b = generate_circle(circle_blue, rng)
    xs_g, ys_g, lws_g, alphas_g = generate_circle(circle_green, rng)

    # Weave threshold: midpoint between circle centers
    blue_cy = CY + circle_blue['cy_off'] * PH
    green_cy = CY + circle_green['cy_off'] * PH
    y_mid = (blue_cy + green_cy) / 2

    # Weave A: blue in front at top, green in front at bottom
    draw_circle_weave(ax, xs_b, ys_b, lws_b, alphas_b, OCEAN,
                      y_threshold=y_mid, front_above=True)
    draw_circle_weave(ax, xs_g, ys_g, lws_g, alphas_g, DEEP_SAGE,
                      y_threshold=y_mid, front_above=False)

    # ── Signature and save ──
    add_signature(fig, ax, BG)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_path = os.path.join(OUTPUT_DIR, 'peace_enso_dialogue.pdf')
    fig.savefig(pdf_path, format='pdf', facecolor=BG)
    print(f"saved {pdf_path}")

    # JPG for website (three levels up from pieces/peace/ to project root)
    jpg_path = os.path.join(SCRIPT_DIR, '..', '..', '..', 'public', 'prints', 'peace',
                            'peace_enso_dialogue.jpg')
    os.makedirs(os.path.dirname(jpg_path), exist_ok=True)
    fig.savefig(jpg_path, format='jpg', facecolor=BG, dpi=150)
    print(f"saved {jpg_path}")

    plt.close(fig)
    return pdf_path


if __name__ == '__main__':
    render()
