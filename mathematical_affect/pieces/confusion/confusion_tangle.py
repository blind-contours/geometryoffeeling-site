"""
Geometry of Feeling — Confusion: Phase Slip
Horizontal line field where phase coherence dissolves left-to-right.
Lines begin orderly, then accumulate spatially-varying phase offsets —
the moment understanding slips.
"""
import colorsys
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#DDD9D2'


def make_color_palette():
    """Amber/ochre (warm left) -> slate/grey (cool right).
    Returns a function that maps x in [0,1] to an RGBA tuple."""
    # Anchor colors along x-axis
    # Left:  warm amber  #B8935A
    # Mid-L: burnt ochre #A08060
    # Mid:   warm grey   #8A8078
    # Mid-R: cool grey   #747A82
    # Right: slate       #5E6872
    anchors_x = np.array([0.0,   0.25,  0.50,  0.75,  1.0])
    anchors_rgb = np.array([
        [0xB8, 0x93, 0x5A],  # warm amber
        [0xA0, 0x80, 0x60],  # burnt ochre
        [0x8A, 0x80, 0x78],  # warm grey
        [0x74, 0x7A, 0x82],  # cool grey
        [0x5E, 0x68, 0x72],  # slate
    ], dtype=float) / 255.0

    def color_at(x_frac):
        r = np.interp(x_frac, anchors_x, anchors_rgb[:, 0])
        g = np.interp(x_frac, anchors_x, anchors_rgb[:, 1])
        b = np.interp(x_frac, anchors_x, anchors_rgb[:, 2])
        return r, g, b

    return color_at


def render():
    np.random.seed(42)

    n_lines = 50
    n_pts = 3000

    # --- figure setup (grief_void pattern) ---
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    color_fn = make_color_palette()

    # X spans the full width with small margins
    x = np.linspace(0.03, 0.97, n_pts)
    # Normalized position along line [0, 1]
    t = (x - x[0]) / (x[-1] - x[0])

    # Vertical positions for lines — evenly spaced with slight jitter
    y_centers = np.linspace(0.08, 0.92, n_lines)
    y_jitter = np.random.uniform(-0.002, 0.002, n_lines)

    # --- Phase decoherence parameters ---
    # Amplitude envelope: near-zero on left, grows toward right
    # Using a smooth power curve for gradual onset
    # Max displacement tuned so lines waver but rarely cross
    amp_envelope = 0.007 * t ** 2.0

    # Base angular frequency for undulation
    omega_base = 2 * np.pi * 3.0

    for i in range(n_lines):
        y0 = y_centers[i] + y_jitter[i]

        # Per-line properties
        line_omega = omega_base * (0.85 + 0.3 * np.random.random())
        line_phase_base = np.random.uniform(0, 2 * np.pi)
        line_lw = 0.6 + 0.6 * np.random.random()
        line_alpha = 0.40 + 0.25 * np.random.random()

        # --- Phase accumulation (the key decoherence mechanism) ---
        # phi_i(x) = base_phase + cumulative noise that grows with x
        # The noise increments grow larger toward the right
        noise_increments = np.random.normal(0, 1, n_pts)
        # Weight the noise so it accumulates faster on the right
        noise_weight = t ** 2.0
        weighted_noise = noise_increments * noise_weight * 0.04
        phi = line_phase_base + np.cumsum(weighted_noise)

        # --- Compute y displacement ---
        # y_i(x) = y0 + A(x) * sin(omega * x + phi_i(x))
        # Plus a second harmonic for richness
        displacement = (
            amp_envelope * np.sin(line_omega * t * 6 + phi)
            + amp_envelope * 0.25 * np.sin(line_omega * 1.7 * t * 6 + phi * 1.3 + 0.5)
        )

        # A very subtle global wave even on the left (Agnes Martin register)
        gentle_wave = 0.0012 * np.sin(2 * np.pi * 1.2 * t + line_phase_base)

        y = y0 + displacement + gentle_wave

        # --- Draw line with color varying along x ---
        # We draw the line as short segments with varying color
        seg_len = 60  # points per segment
        n_segs = n_pts // seg_len

        for s in range(n_segs):
            s0 = s * seg_len
            s1 = min(s0 + seg_len + 1, n_pts)  # +1 for overlap
            x_seg = x[s0:s1]
            y_seg = y[s0:s1]

            # Color at segment midpoint
            x_mid = t[(s0 + min(s1, n_pts - 1)) // 2]
            r, g, b = color_fn(x_mid)

            # Alpha decreases very slightly toward right (lines become ghostlier)
            seg_alpha = line_alpha * (1.0 - 0.15 * x_mid)

            ax.plot(x_seg, y_seg,
                    color=(r, g, b, seg_alpha),
                    lw=line_lw,
                    solid_capstyle='round',
                    zorder=2)

    # --- Equation label (bottom-left, matching grief_void style) ---
    eq = "y\u1d62(x) = y\u2080 + A(x)\u00b7sin(\u03c9x + \u03c6\u1d62(x))   \u03c6\u1d62 \u2190 \u2211\u03b5\u2c7c\u00b7x\u1d47"
    ax.text(0.06, 0.04, eq,
            fontfamily='monospace', fontsize=8,
            color=(0.15, 0.15, 0.20, 0.25),
            transform=ax.transAxes)

    # --- Save ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "confusion_tangle.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
