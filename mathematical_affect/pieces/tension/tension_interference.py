"""
Geometry of Feeling — Tension: Tension Interference
Standalone render script
"""

"""
Geometry of Feeling — Tension (Final Series)
Five pieces: Fracture, Opposition, Buckling, Interference, Torsion

CONCEPTUALIZATION — 20 CANDIDATES:
 1. Fracture — Stress-strain curve pushed past yield, microcrack propagation
 2. Opposition — Two mirrored attractors pulling apart, phase space tug-of-war
 3. Buckling — Euler column buckling, sudden lateral deflection under axial load
 4. Interference — Standing wave at max constructive/destructive overlap
 5. Torsion — Twisted coordinate field, shear stress on cross-section
 6. Catenary — Loaded chain sagging past elastic limit
 7. Beat (exists) — Skip, already in original series
 8. Stretch (exists) — Skip, already in original series
 9. Resonance (exists) — Skip, already in original series
10. Spring cascade — Coupled springs at resonance, chaotic amplitude
11. Membrane — Drumhead vibration mode shapes at high excitation
12. Hysteresis — Magnetization loop, irreversible path tension
13. Elastic rebound — Compressed spring releasing, moment of maximum potential
14. Phase lock — Two oscillators fighting synchronization
15. Bifurcation — System at critical parameter, about to split
16. Moiré — Overlapping gratings creating interference stress pattern
17. Whiplash — Damped oscillation with violent initial amplitude
18. Pressure vessel — Hoop stress reaching yield, circumferential tension
19. Cantilever — Beam deflection under increasing point load
20. Vortex pair — Counter-rotating vortices stretching fluid between them

CRITIQUE & SELECTION:
- Fracture (#1): Outstanding. The stress-strain curve is THE canonical tension
  visualization. We can show the elastic region, yield, necking, and the moment
  of fracture with microcrack lines radiating from the break point. Rich,
  narrative, mathematically precise.

- Opposition (#2): Strong. Two Lorenz-like attractors mirrored and pulling apart
  creates visual tension through symmetry violation. The space BETWEEN them is
  where tension lives. We render the gap as a taut void.

- Buckling (#3): Excellent. Euler buckling is dramatic — a straight column
  suddenly bowing under compressive load. We show the family of buckling modes
  (n=1,2,3...) with the critical load curves, the moment of instability.
  Mathematically: y(x) = A*sin(n*pi*x/L). The superposition of modes creates
  visual complexity.

- Interference (#5): Torsion is more visually unique than simple wave
  interference. A twisted coordinate grid shows shear stress beautifully —
  circles becoming ellipses, straight lines becoming spirals. The deformation
  IS the tension.

- Torsion (#5): Selected over Interference (#4) because it offers a completely
  different visual vocabulary — rotational deformation vs. wave patterns.
  Mathematical richness: Prandtl stress function, warping, the twist angle
  gradient.

REJECTED (with reasons):
- #4 Interference: Too similar to Beat (wave superposition)
- #6 Catenary: Visually too simple (just a curve)
- #10 Spring cascade: Hard to make visually distinct from Beat
- #11 Membrane: Requires 3D or complex mode visualization
- #12 Hysteresis: Loop shape is too contained, doesn't fill canvas
- #13 Elastic rebound: Hard to show "moment" without animation
- #14 Phase lock: Too similar to Opposition
- #15 Bifurcation: Better suited for "Confusion" series
- #16 Moiré: Could be stunning but risks being decorative, not tense
- #17 Whiplash: Too similar to damped oscillation (basic)
- #18 Pressure vessel: Hard to show circumferential stress in 2D elegantly
- #19 Cantilever: Visually too similar to Buckling
- #20 Vortex pair: Better suited for "Desire" or fluid dynamics series

FINAL FIVE:
1. Fracture    — Stress-strain with microcrack propagation at yield
2. Opposition  — Mirrored chaotic attractors pulling apart
3. Buckling    — Euler column modes at critical load
4. Interference— Standing waves at maximum constructive/destructive points
5. Torsion     — Twisted coordinate field under shear

Dependencies: matplotlib, numpy
    pip install matplotlib numpy
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Circle
import os


DPI    = 300
FIG_W  = 12
FIG_H  = 8

BG       = "#1A1A1A"
ACID     = "#E8D820"
DIM      = "#888810"
HOT      = "#D04010"
RED      = "#C03010"
ELECTRIC = "#E0E020"
ORANGE   = "#E87020"

PAD_L = 0.65; PAD_R = 0.55; PAD_T = 0.60; PAD_B = 0.85
PW = FIG_W - PAD_L - PAD_R
PH = FIG_H - PAD_T  - PAD_B
cx = PAD_L + PW / 2
cy = PAD_B + PH / 2


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))


def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax  = fig.add_subplot(111)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def label(ax, eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(1,1,1,0.20),transform=ax.transData)
def split_segments(xs, ys, mask):
    """Split arrays into contiguous segments where mask is True."""
    segments = []
    in_seg = False
    start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j
            in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3:
                segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3:
        segments.append((xs[start:], ys[start:]))
    return segments


def draw_lc(ax, xs, ys, col, lw, alpha, zo=4):
    pts  = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc   = mc.LineCollection(segs, linewidths=lw,
                             colors=[rgba(col, alpha)],
                             capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)


def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Ensure name ends with .pdf
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


# =============================================================================
# 4. INTERFERENCE — Standing waves at maximum constructive/destructive overlap
#    y(x,t) = sum_k A_k * sin(k*pi*x/L) * cos(omega_k*t + phi_k)
#    Multiple harmonics frozen at the moment of maximum interference
# =============================================================================
def render():
    fig, ax = make_fig()
    Y_MIN = PAD_B + 0.02
    Y_MAX = PAD_B + PH - 0.02

    N = 5000
    x = np.linspace(0, 1, N)
    xs = PAD_L + PW * x

    acid_rgb = hex_to_rgb(ACID)
    elec_rgb = hex_to_rgb(ELECTRIC)
    hot_rgb  = hex_to_rgb(HOT)
    red_rgb  = hex_to_rgb(RED)
    dim_rgb  = hex_to_rgb(DIM)

    # --- Two wave systems traveling in opposite directions ---
    # Wave 1: rightward packet
    # Wave 2: leftward packet (reflected)
    # Their superposition creates standing wave patterns

    n_harmonics = 7
    freqs = [3, 5, 7, 11, 13, 17, 19]  # prime harmonics for complex pattern
    amps  = [1.0, 0.7, 0.5, 0.35, 0.25, 0.18, 0.12]

    # Total amplitude for normalization
    total_amp = sum(amps)

    # --- Draw individual harmonics as ghost layers ---
    for h_idx, (freq, amp) in enumerate(zip(freqs, amps)):
        y_h = amp * np.sin(2 * np.pi * freq * x)
        y_scaled = cy + (PH * 0.40 / total_amp) * y_h
        y_clipped = np.clip(y_scaled, Y_MIN, Y_MAX)

        t_h = h_idx / max(len(freqs) - 1, 1)
        alpha = 0.08 + 0.06 * (1 - t_h)
        col = DIM
        draw_lc(ax, xs, y_clipped, col, 0.5 + 0.3 * (1 - t_h), alpha, zo=2)

    # --- Constructive interference: all harmonics in phase ---
    y_constructive = np.zeros(N)
    for freq, amp in zip(freqs, amps):
        y_constructive += amp * np.sin(2 * np.pi * freq * x)
    y_c_scaled = cy + (PH * 0.40 / total_amp) * y_constructive
    y_c_scaled = np.clip(y_c_scaled, Y_MIN, Y_MAX)

    # --- Destructive interference: alternating phase offsets ---
    y_destructive = np.zeros(N)
    for i, (freq, amp) in enumerate(zip(freqs, amps)):
        phase = np.pi * (i % 2)  # alternating 0 and pi
        y_destructive += amp * np.sin(2 * np.pi * freq * x + phase)
    y_d_scaled = cy + (PH * 0.40 / total_amp) * y_destructive
    y_d_scaled = np.clip(y_d_scaled, Y_MIN, Y_MAX)

    # --- Fill between constructive and destructive: the tension zone ---
    for i in range(0, N - 1, 3):
        y_top = max(y_c_scaled[i], y_d_scaled[i])
        y_bot = min(y_c_scaled[i], y_d_scaled[i])
        span = y_top - y_bot
        max_span = PH * 0.5
        intensity = np.clip(span / max_span, 0, 1)
        a = 0.03 + 0.15 * intensity
        ax.fill([xs[i], xs[i+1], xs[i+1], xs[i]],
                [y_bot, min(y_c_scaled[i+1], y_d_scaled[i+1]),
                 max(y_c_scaled[i+1], y_d_scaled[i+1]), y_top],
                color=rgba(ACID, a), linewidth=0, zorder=1)

    # --- Draw constructive wave (bright, acid) ---
    pts_c = np.array([xs, y_c_scaled]).T.reshape(-1, 1, 2)
    segs_c = np.concatenate([pts_c[:-1], pts_c[1:]], axis=1)
    colors_c = []
    for i in range(len(segs_c)):
        # Color based on amplitude — peaks are hotter
        amp_norm = abs(y_c_scaled[i] - cy) / (PH * 0.42)
        amp_norm = np.clip(amp_norm, 0, 1)
        r = acid_rgb[0] * (1 - amp_norm*0.4) + elec_rgb[0] * amp_norm * 0.4
        g = acid_rgb[1] * (1 - amp_norm*0.4) + elec_rgb[1] * amp_norm * 0.4
        b = acid_rgb[2] * (1 - amp_norm*0.4) + elec_rgb[2] * amp_norm * 0.4
        colors_c.append((r, g, b, 0.85))
    lc_c = mc.LineCollection(segs_c, linewidths=1.8, colors=colors_c,
                             capstyle='round', zorder=5)
    ax.add_collection(lc_c)

    # --- Draw destructive wave (hot, opposing) ---
    pts_d = np.array([xs, y_d_scaled]).T.reshape(-1, 1, 2)
    segs_d = np.concatenate([pts_d[:-1], pts_d[1:]], axis=1)
    colors_d = []
    for i in range(len(segs_d)):
        amp_norm = abs(y_d_scaled[i] - cy) / (PH * 0.42)
        amp_norm = np.clip(amp_norm, 0, 1)
        r = hot_rgb[0] * (1 - amp_norm*0.3) + red_rgb[0] * amp_norm * 0.3
        g = hot_rgb[1] * (1 - amp_norm*0.3) + red_rgb[1] * amp_norm * 0.3
        b = hot_rgb[2] * (1 - amp_norm*0.3) + red_rgb[2] * amp_norm * 0.3
        colors_d.append((r, g, b, 0.80))
    lc_d = mc.LineCollection(segs_d, linewidths=1.6, colors=colors_d,
                             capstyle='round', zorder=4)
    ax.add_collection(lc_d)

    # --- Nodes: where both curves cross the center line ---
    # Find approximate crossing points of constructive wave
    crossings = []
    for i in range(N - 1):
        if (y_c_scaled[i] - cy) * (y_c_scaled[i+1] - cy) < 0:
            # Linear interpolation for crossing point
            t_cross = (cy - y_c_scaled[i]) / (y_c_scaled[i+1] - y_c_scaled[i])
            x_cross = xs[i] + t_cross * (xs[i+1] - xs[i])
            crossings.append(x_cross)

    for xc in crossings:
        ax.plot(xc, cy, 'o', color=rgba(DIM, 0.35),
                markersize=2.5, markeredgewidth=0, zorder=7)

    # --- Maximum constructive point marker ---
    max_c_idx = np.argmax(np.abs(y_c_scaled - cy))
    ax.plot(xs[max_c_idx], y_c_scaled[max_c_idx], 'o',
            color=rgba(ELECTRIC, 0.80), markersize=5, markeredgewidth=0, zorder=8)

    # Vertical tension line at max point
    ax.plot([xs[max_c_idx], xs[max_c_idx]],
            [y_d_scaled[max_c_idx], y_c_scaled[max_c_idx]],
            color=rgba(RED, 0.50), linewidth=1.5, zorder=7)
    for y_dot in [y_d_scaled[max_c_idx], y_c_scaled[max_c_idx]]:
        ax.plot(xs[max_c_idx], y_dot, 'o', color=rgba(RED, 0.70),
                markersize=3.5, markeredgewidth=0, zorder=8)

    # --- Center equilibrium line ---
    ax.plot([PAD_L, PAD_L + PW], [cy, cy],
            color=rgba(DIM, 0.12), linewidth=0.5, linestyle='-', zorder=1)

    label(ax, "y(x) = \u03a3 A_k\u00b7sin(2\u03c0f_k\u00b7x+\u03c6_k)")
    save(fig, "tension_interference.pdf")


if __name__ == '__main__':
    render()
