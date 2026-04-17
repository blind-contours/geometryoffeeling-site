"""
Geometry of Feeling:
Standalone render script (revision 3)

REAL DIAGNOSIS (finally):
The lines DO reach the right margin mathematically � they just stop feeling
alive. By ~70% across: width has collapsed to a uniform COMMON_LW, color has
blended fully to WARM (which is close to the BG cream), and flow_y has very
little amplitude. So the eye reads the right third as "empty" even though
lines are technically there.

Fix: keep the lines feeling active all the way to the right crop. They should
be calmer on the right than the left, but still CARRYING tone, width variation,
and some gentle motion.

Changes from rev 2:
  1. flow_y gets a secondary slower wave so there's still motion at right edge
  2. Width blend capped � lines don't fully collapse to COMMON_LW
  3. Color blend capped at 0.65 � lines keep substantial tonal identity
  4. Alpha baseline raised further so right side has real presence
  5. Removed the width convergence � retain hierarchy all the way across
"""

import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os, glob

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#E8E4DE"

DARK     = "#5A5048"
MED_DARK = "#7A7068"
SOFT     = "#9A9088"
WARM     = "#B0A898"
LIGHT    = "#C8C0B4"
LAVENDER = "#8A7E98"
BLUE_GR  = "#6A7A88"
RUST     = "#987868"
CLAY     = "#8A7060"
MIST     = "#A0A8A0"

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    # Remove default axes padding � otherwise matplotlib shrinks the drawable
    # area by ~10% on each side and margins render incorrectly.
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    return fig, ax

MARGIN = 0.7
PAD_L = PAD_R = PAD_T = PAD_B = MARGIN
PW = FIG_W - PAD_L - PAD_R
PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2
cy = PAD_B + PH / 2

def split_segments(xs, ys, mask):
    segments = []
    in_seg = False; start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j; in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3:
                segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3:
        segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='butt', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def brush_jitter(lw_arr, strength=0.18, grain=25):
    n = len(lw_arr) if hasattr(lw_arr, '__len__') else 1
    if n <= 1:
        return lw_arr
    noise = np.random.randn(n)
    noise = gaussian_filter1d(noise, grain)
    noise = noise / (np.abs(noise).max() + 1e-9) * strength
    return np.clip(lw_arr * (1 + noise), 0.15, None)

def draw_lc_color_blend(ax, xs, ys, col_start, col_end, blend_arr, lw, alpha,
                         zo=4, smooth=0, brush=True):
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    n = len(segs)
    lw_arr = np.full(n, lw) if np.isscalar(lw) else np.asarray(lw[:n], dtype=float)
    if brush and n > 1:
        lw_arr = brush_jitter(lw_arr)
    r1, g1, b1 = hex_to_rgb(col_start)
    r2, g2, b2 = hex_to_rgb(col_end)
    scalar_alpha = np.isscalar(alpha)
    colors = []
    for j in range(n):
        b = float(np.clip(blend_arr[j], 0, 1))
        a = float(np.clip(alpha, 0, 1)) if scalar_alpha else float(np.clip(alpha[j], 0, 1))
        colors.append((r1 + (r2 - r1) * b, g1 + (g2 - g1) * b,
                        b1 + (b2 - b1) * b, a))
    lc = mc.LineCollection(segs, linewidths=lw_arr, colors=colors,
                           capstyle='butt', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name), format='pdf', facecolor=BG)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def render():
    fig, ax = make_fig()
    np.random.seed(33)
    n_curves = 30
    # Overshoot both edges so lines are clipped by the frame, not ending at it
    t = np.linspace(-0.04, 1.04, 1800)
    # Gentle upward lift peaking ~65-70% across, then curves down to exit
    flow_y = (cy
              + PH * 0.06 * np.sin(2 * np.pi * t * 0.7)
              + PH * 0.08 * np.exp(-((t - 0.67) / 0.18) ** 2))  # Gaussian bump at ~67%
    TARGET = WARM       # the color everything surrenders into
    COMMON_LW = 1.4     # the width everything surrenders into

    # Hierarchy: two slightly more present voices, not a featured cast
    dominant = {9, 20}
    late     = {11, 22}     # delayed surrender — trace of independence
    linger   = {25}         # one upper strand holds individuality a beat longer

    for i in range(n_curves):
        frac = i / (n_curves - 1)
        xs_f = PAD_L + PW * t

        # Selective spread: outer strands pushed further, center cluster stays present
        spread_frac = frac + 0.08 * np.sin(np.pi * frac) * (2 * abs(frac - 0.5))
        spread_frac = np.clip(spread_frac, 0.03, 0.88)
        y_start = PAD_B + PH * (0.02 + spread_frac * 0.96)

        merge_rate = 1.4 + np.random.uniform(0, 1.4)

        # Outer strands: both top and bottom join faster so they curve toward center
        edge_dist = abs(frac - 0.5) * 2
        if edge_dist > 0.85:
            merge_rate *= 3.5   # very outermost — pull in hard
        elif edge_dist > 0.6:
            merge_rate *= 1.7

        # Late surrenderers: slightly slower spatial convergence
        if i in late:
            merge_rate *= 0.84

        blend = 1 - np.exp(-merge_rate * t)
        noise = np.cumsum(np.random.randn(len(t)) * PH * 0.003 * (1 - blend))
        noise = gaussian_filter1d(noise, 15)
        ys_f = y_start * (1 - blend) + flow_y * blend + noise

        # Closing funnel: soft proportional pull toward flow_y on the right
        # No hard clamp — just gently reduces deviation so outliers drift in
        funnel_t = np.clip((t - 0.65) / 0.35, 0, 1) ** 3   # very gentle ease-in from 65%
        deviation = ys_f - flow_y
        ys_f = flow_y + deviation * (1 - funnel_t * 0.25)

        mask = (ys_f > PAD_B) & (ys_f < PAD_B + PH)
        if mask.sum() < 3: continue

        cols = [DARK, MED_DARK, SOFT, RUST, CLAY, BLUE_GR, WARM, LAVENDER, MIST]
        col = cols[i % len(cols)]
        alpha = 0.38 + 0.58 * (1 - abs(frac - 0.5) * 1.2)

        # Width hierarchy — two forms carry more weight, integrated into the tonal field
        if i == 9:
            lw_start = 2.5 + np.random.uniform(0, 0.7)
            alpha = min(alpha * 1.12, 0.85)
        elif i in dominant:
            lw_start = 3.0 + np.random.uniform(0, 1.0)
            alpha = min(alpha * 1.15, 0.88)
        else:
            lw_start = 0.7 + 1.4 * (1 - abs(frac - 0.5))

        for seg_xs, seg_ys in split_segments(xs_f, ys_f, mask):
            seg_t = (seg_xs - PAD_L) / PW

            # Color blend timing — still surrendering as lines hit the crop
            if i in late:
                color_t = np.clip((seg_t - 0.50) / 0.50, 0, 1)
            elif i in linger:
                color_t = np.clip((seg_t - 0.46) / 0.56, 0, 1)
            else:
                color_t = np.clip((seg_t - 0.38) / 0.52, 0, 1)
            seg_blend = color_t ** 2  # ease-in for smooth transition

            # Width blend — all lines converge to COMMON_LW
            seg_lw = lw_start + (COMMON_LW - lw_start) * seg_blend

            # Middle-left depth: Gaussian opacity boost centered ~35% across canvas
            depth_boost = np.exp(-((seg_t - 0.35) / 0.15) ** 2) * 0.10
            seg_alpha = np.clip(alpha + depth_boost, 0, 1)

            # Glow — subliminal radiance, strongest in the middle zones
            # Reads as stained air, not an outline aura
            glow_envelope = np.exp(-((seg_t - 0.45) / 0.30) ** 2)  # peaks ~45%, fades at edges
            for glow_mult, glow_base_alpha in [(8.0, 0.03), (4.5, 0.06)]:
                glow_lw = seg_lw * glow_mult
                glow_alpha = np.clip(seg_alpha * glow_base_alpha * glow_envelope, 0, 1)
                draw_lc_color_blend(ax, seg_xs, seg_ys, col, TARGET, seg_blend,
                                    lw=glow_lw, alpha=glow_alpha, zo=2, smooth=5,
                                    brush=False)
            # Core line on top
            draw_lc_color_blend(ax, seg_xs, seg_ys, col, TARGET, seg_blend,
                                lw=seg_lw, alpha=seg_alpha, zo=3, smooth=5)

    #draw_lc(ax, PAD_L + PW * t, flow_y, TARGET, lw=2.1, alpha=0.42, zo=2, smooth=5)
    add_signature(fig, ax, BG)
    save(fig, "surrender_flow")
    plt.show()

if __name__ == '__main__':
    render()
