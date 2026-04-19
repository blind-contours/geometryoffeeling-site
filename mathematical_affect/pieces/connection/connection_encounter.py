"""
Geometry of Feeling — Connection: Encounter
Standalone render script

Two coupled Stuart-Landau oscillators that perturb each other at close approach.
The encounter leaves visible kinks — brief impulses where each path bends toward
the other, then settles into a permanently altered orbit. Connection as event:
the meeting changes both trajectories.
"""

import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import FancyBboxPatch, Rectangle
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#090A12"
MARGIN_COLOR = "#E8D8B8"

AMBER = np.array([212, 168, 86]) / 255
EMBER = np.array([192, 128, 64]) / 255
ROSE = np.array([201, 138, 132]) / 255


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    fig.patch.set_facecolor(MARGIN_COLOR)
    ax.set_facecolor(MARGIN_COLOR)
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    ml = FIG_W * 0.07; mr = FIG_W * 0.07
    mb = FIG_H * 0.08; mt = FIG_H * 0.08
    ax.add_patch(FancyBboxPatch((ml, mb), FIG_W - ml - mr, FIG_H - mb - mt,
                                 boxstyle="square,pad=0",
                                 facecolor=BG, edgecolor='none', zorder=0))
    zo = 1000
    ax.add_patch(Rectangle((0, 0), FIG_W, mb,
                            facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, FIG_H - mt), FIG_W, mt,
                            facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, 0), ml, FIG_H,
                            facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((FIG_W - mr, 0), mr, FIG_H,
                            facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    return fig, ax


def glow(ax, p, color, rad=0.14, alpha=0.9, z=8):
    """Gaussian radiance at a point — no circles."""
    res = 120
    yy, xx = np.mgrid[:res, :res]
    c = res // 2
    sig = res / 8.0
    g = np.exp(-((xx - c)**2 + (yy - c)**2) / (2 * sig**2))
    img = np.zeros((res, res, 4))
    img[:, :, :3] = color
    img[:, :, 3] = g * alpha
    ax.imshow(img,
              extent=[p[0] - rad, p[0] + rad, p[1] - rad, p[1] + rad],
              origin='lower', interpolation='bicubic', zorder=z, aspect='auto')


def simulate_seed(seed=0, n=22000, dt=0.007):
    """Stuart-Landau oscillator pair with encounter coupling.

    Two limit-cycle oscillators at slightly different frequencies.
    When close in the central corridor, they exchange brief impulses
    that create visible kinks and lasting phase shifts.
    """
    rng = np.random.default_rng(seed)
    z1 = (1.0 + 0.012 * rng.normal()) * np.exp(
        1j * (0.28 + 0.02 * rng.normal()))
    z2 = (1.0 + 0.012 * rng.normal()) * np.exp(
        1j * (np.pi - 0.20 + 0.02 * rng.normal()))

    m1 = 0 + 0j
    m2 = 0 + 0j
    pulse1 = 0 + 0j
    pulse2 = 0 + 0j

    # Oscillator parameters
    mu = 1.0
    w1, w2 = 1.0, 0.958
    b1, b2 = 0.22, 0.15
    eps = 0.11

    # Coupling parameters
    attract = 0.20
    tang = 0.08
    mem = 0.075
    lam = 0.85
    pulse_str = 0.36
    pulse_decay = 0.92
    tau = 1.02
    cooldown = 10

    # Mapping parameters
    sep = 1.88
    ax1, by1 = 1.88, 1.31
    ax2, by2 = 1.76, 1.22
    warp = 0.48
    corridor_gain = 1.02
    sigma = 1.14
    asym = 0.14
    slip = 0.28

    corridor_wx = 0.32
    corridor_wy = 0.72
    corridor_y = 0.05

    def map_pos(z, side=1):
        x, y = z.real, z.imag
        if side == 1:
            X = -sep + ax1 * x + 0.16 * (x * x - y * y) + warp * x * y
            Y = by1 * y + 0.12 * (x * x) - 0.09 * (y * y)
        else:
            X = sep + ax2 * x - 0.14 * (x * x - y * y) - warp * x * y
            Y = by2 * y - 0.10 * (x * x) + 0.08 * (y * y)
        return np.array([X, Y])

    ps1, ps2, rose, ev = [], [], [], []
    last_ev = -10**9

    for i in range(n):
        p1, p2 = map_pos(z1, 1), map_pos(z2, 2)
        d = p2 - p1
        rho = np.linalg.norm(d) + 1e-9
        q = (d[0] + 1j * d[1]) / rho
        tq = 1j * q
        mid = 0.5 * (p1 + p2)

        corridor = np.exp(
            -(mid[0]**2) / (2 * corridor_wx**2)
            - ((mid[1] - corridor_y)**2) / (2 * corridor_wy**2)
        )
        g = np.exp(-(rho**2) / (2 * sigma**2))

        base1 = (mu + 1j * w1 - (1 + 1j * b1) * abs(z1)**2) * z1 \
                + eps * np.conj(z1)
        base2 = (mu + 1j * w2 - (1 + 1j * b2) * abs(z2)**2) * z2 \
                - 0.8 * eps * np.conj(z2)

        coup = (attract * (g + corridor_gain * corridor)
                + 1j * tang * corridor) * (z2 - z1)
        dz1 = base1 + coup + m1 + pulse1
        dz2 = base2 - coup + m2 + pulse2

        if rho < tau and corridor > 0.18 and (i - last_ev) > cooldown:
            k = pulse_str * (0.38 + 0.62 * corridor)
            pulse1 += (1 - asym) * (k * q + 0.14 * k * tq)
            pulse2 -= (1 + asym) * (k * q - 0.14 * k * tq)
            m1 += (1 - asym) * mem * (q + 0.18 * tq)
            m2 -= (1 + asym) * mem * (q - 0.18 * tq)
            z1 *= np.exp(1j * slip * (1 - asym) * (0.55 + 0.45 * corridor))
            z2 *= np.exp(-1j * slip * (1 + asym) * (0.55 + 0.45 * corridor))
            ev.append(i)
            last_ev = i

        z1 += dt * dz1
        z2 += dt * dz2
        pulse1 *= pulse_decay
        pulse2 *= pulse_decay
        m1 *= np.exp(-lam * dt)
        m2 *= np.exp(-lam * dt)

        ps1.append(map_pos(z1, 1))
        ps2.append(map_pos(z2, 2))
        rose.append(corridor * np.clip(1 - rho / (1.45 * sigma), 0, 1))

    return np.array(ps1), np.array(ps2), np.array(ev), np.array(rose)


PAD_L = 0.78; PAD_R = 0.62; PAD_B = 0.88; PAD_T = 0.66
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_B - PAD_T


def render():
    fig, ax = make_fig()

    # Ensemble of 6 seeds for layered depth
    sims = [simulate_seed(seed=s) for s in range(6)]

    # Global normalization across all seeds
    xs = np.concatenate([np.r_[s[0][:, 0], s[1][:, 0]] for s in sims])
    ys = np.concatenate([np.r_[s[0][:, 1], s[1][:, 1]] for s in sims])

    scale = min(
        PW / (xs.max() - xs.min() + 1e-9),
        PH / (ys.max() - ys.min() + 1e-9),
    ) * 0.94
    cx_data = (xs.min() + xs.max()) / 2
    cy_data = (ys.min() + ys.max()) / 2

    def tx(P):
        return np.c_[
            (P[:, 0] - cx_data) * scale + (PAD_L + PW / 2),
            (P[:, 1] - cy_data) * scale + (PAD_B + PH / 2),
        ]

    # Per-layer alpha and linewidth — back layers faint, front bold
    alpha_levels = [0.014, 0.018, 0.024, 0.036, 0.060, 0.22]
    width_levels = [0.12, 0.13, 0.15, 0.18, 0.24, 0.86]

    for rep, (P1, P2, ev, rose) in enumerate(sims):
        P1, P2 = tx(P1), tx(P2)

        def draw_path(P, color, z):
            nn = len(P) - 1
            seg = np.stack([P[:-1], P[1:]], axis=1)
            mids = 0.5 * (P[:-1] + P[1:])
            ctr = np.array([FIG_W / 2, FIG_H / 2])

            a = np.linspace(0.006, alpha_levels[rep], nn)
            lw = np.linspace(width_levels[rep] * 0.65, width_levels[rep], nn)

            # Spatial fade from center
            dist = np.linalg.norm(mids - ctr, axis=1)
            fade = np.clip(1 - (dist - 1.20) / 2.55, 0.02, 1.0)
            a *= fade

            # Quieter outer loops
            outerness = np.clip((dist - 1.55) / 1.25, 0, 1)
            a *= (1 - 0.36 * outerness)
            lw *= (1 - 0.18 * outerness)

            # Rose tint near encounters
            rose_mix = np.clip(1.05 * rose[:nn], 0, 0.62)

            # Rhythmic break near encounter events
            for idx in ev:
                for rad, amp, sharp in [(8, 0.95, 18), (18, 0.58, 8)]:
                    lo = max(0, idx - rad)
                    hi = min(nn, idx + rad)
                    t = np.linspace(-1, 1, hi - lo)
                    bump = amp * np.exp(-sharp * t * t)
                    rose_mix[lo:hi] = np.maximum(rose_mix[lo:hi], bump)
                    lw[lo:hi] *= (1 + 0.22 * bump)

            cols = []
            for ai, ri in zip(a, rose_mix):
                rgb = color * (1 - ri) + ROSE * ri
                cols.append((*rgb, float(np.clip(ai * (1 + 0.90 * ri), 0, 0.78))))

            ax.add_collection(
                LineCollection(seg, colors=cols, linewidths=lw,
                               capstyle='round', joinstyle='round', zorder=z))

        draw_path(P1, AMBER, 4)
        draw_path(P2, EMBER, 5)

    # Two presences — slightly unequal, placed along the front seed's path
    P1_front, P2_front = tx(sims[-1][0]), tx(sims[-1][1])
    glow(ax, P1_front[int(len(P1_front) * 0.80)], AMBER, 0.145, 0.93, 8)
    glow(ax, P2_front[int(len(P2_front) * 0.72)], EMBER, 0.120, 0.72, 7)

    add_signature(fig, ax, MARGIN_COLOR, margin_piece=True,
                  margin_bottom=FIG_H * 0.08)
    return fig


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
PRINT_DIR = os.path.join(SCRIPT_DIR, '..', '..', '..', 'public', 'prints', 'connection')

if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PRINT_DIR, exist_ok=True)
    print("═══ Connection: Encounter ═══")

    # Print PDF
    fig = render()
    pdf_path = os.path.join(OUTPUT_DIR, "connection_encounter.pdf")
    fig.savefig(pdf_path, format='pdf', facecolor=MARGIN_COLOR)
    print(f"  saved {pdf_path}")
    plt.close(fig)

    # Web thumbnail
    fig = render()
    jpg_path = os.path.join(PRINT_DIR, "connection_encounter.jpg")
    fig.savefig(jpg_path, facecolor=MARGIN_COLOR, dpi=DPI,
                pil_kwargs={"quality": 96})
    print(f"  saved {jpg_path}")
    plt.close(fig)

    print("═══ Done ═══")
