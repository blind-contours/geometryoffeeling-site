"""
Geometry of Feeling — Peace: Peace Harmonic v5
Same restrained vocabulary as v4, but with a nonlinear settling curve.
The calm zone now occupies the lower ~60% of the image and the activity
concentrates in the top quarter. The image arrives at peace sooner, so
the read is "rest with a memory of motion above" rather than "ordered
variation top to bottom."
"""
import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#F0EDE8"

# Palette: bottom-to-top, blue → green → earth → rust → plum → grey
PALETTE = [
    "#3A5A6A",  # 0  steel blue (bottom — deepest peace)
    "#3A5A6A",  # 1  steel blue (held)
    "#4A6A78",  # 2  ocean
    "#4A6A70",  # 3  blue-slate
    "#4A6A60",  # 4  blue-green
    "#4A6A52",  # 5  deep sage
    "#5A7A5A",  # 6  lichen
    "#5A6A48",  # 7  olive
    "#6A5A48",  # 8  earth
    "#6A5A40",  # 9  warm earth
    "#7A5A48",  # 10 cedar-rust
    "#8A6A4A",  # 11 rust
    "#8A5A50",  # 12 muted terracotta
    "#7A4A55",  # 13 plum-rust
    "#6A4A5A",  # 14 plum
    "#6A5A6A",  # 15 muted plum-grey
    "#6A5A72",  # 16 dusk
    "#7A6A80",  # 17 violet-grey
    "#7A7A82",  # 18 cool grey
    "#82828A",  # 19 soft grey (top)
]

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
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    return fig, ax

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if len(xs) < 2:
        return
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, '..', '..', '..')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
PRINT_DIR = os.path.join(ROOT_DIR, 'public', 'prints', 'peace')

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith('.pdf'):
        name = name + '.pdf'
    pdf_path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(pdf_path, format='pdf', facecolor=BG)
    print(f'saved {pdf_path}')
    os.makedirs(PRINT_DIR, exist_ok=True)
    jpg_name = name.replace('.pdf', '.jpg')
    jpg_path = os.path.join(PRINT_DIR, jpg_name)
    fig.savefig(jpg_path, facecolor=BG, dpi=DPI, format='jpg',
                pil_kwargs={"quality": 96})
    print(f'saved {jpg_path}')
    plt.close(fig)


def render():
    fig, ax = make_fig()

    n = 20
    t = np.linspace(0, 1, 3000)
    xs = PAD_L + PW * t

    for i in range(n):
        # frac: 0 = bottom (deepest peace), 1 = top
        frac = i / (n - 1)
        y_base = PAD_B + PH * (0.06 + frac * 0.88)

        # -----------------------------------------------------------
        # NONLINEAR SETTLING CURVE
        # Use frac^2.2 so most of the image is calm and energy
        # only emerges in the upper quarter. This is the key change
        # — the curator's complaint was that the top half was "all
        # fairly similarly wavy." Now the upper-mid is calm and
        # only the top ~5 lines carry visible motion.
        # -----------------------------------------------------------
        energy = frac ** 2.2

        # FREQUENCY: gentle base, climbs steeply only at top
        mode = 0.4 + energy * 9.0  # 0.4 → ~9.4

        # AMPLITUDE: same nonlinear shape
        amp = PH * (0.008 + energy * 0.030)  # ~0.008 → ~0.038

        # Bottom 4 lines settle further into stillness — anchor
        if frac < 0.18:
            amp *= 0.4

        # -----------------------------------------------------------
        # PHASE: deterministic offsets, but only meaningful at top
        # where amplitude is large enough to see them. Bottom lines
        # are too flat for phase to matter.
        # -----------------------------------------------------------
        phase = 0.7 * np.pi * np.sin(2.1 * np.pi * frac + 0.5)

        # -----------------------------------------------------------
        # SUBTLE PER-LINE VARIATION at the top
        # The curator noted the top lines look too similar. Give the
        # upper lines small individual mode offsets so they read as
        # a varied family rather than parallel copies — but tiny
        # enough that the field stays cohesive.
        # -----------------------------------------------------------
        if frac > 0.65:
            # Small deterministic mode jitter for upper lines
            mode_jitter = 0.6 * np.sin(5.7 * i + 1.3)
            mode += mode_jitter

        ys = y_base + amp * np.sin(mode * np.pi * t + phase)

        # -----------------------------------------------------------
        # COLOR
        # -----------------------------------------------------------
        col = PALETTE[i]

        # -----------------------------------------------------------
        # LINE WEIGHT: bottom slightly heavier (grounded), top
        # slightly thinner (atmospheric). Subtle.
        # -----------------------------------------------------------
        lw = 2.10 - frac * 1.6

        # -----------------------------------------------------------
        # ALPHA: bottom more present, top more atmospheric.
        # The bottom anchor needs to read clearly as the resolved
        # state, so we give it more weight.
        # -----------------------------------------------------------
        if frac < 0.30:
            alpha = 0.66
        else:
            alpha = 0.66 - (frac - 0.30) * 0.32  # 0.66 → 0.44

        draw_lc(ax, xs, ys, col, lw=lw, alpha=alpha, zo=3, smooth=2)

    add_signature(fig, ax, BG)
    save(fig, "peace_harmonic.pdf")


if __name__ == '__main__':
    render()
