"""
Geometry of Feeling — Wonder: Transform
Joukowski-like conformal mapping — circles become airfoils.
A pole singularity warps concentric circles into nested lobes,
revealing hidden structure in simple geometry.
"""
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
BG_COLOR = '#4f5d71'


def render():
    blue = '#90a6cf'
    gold = '#d6b876'
    ring = '#efe2bf'

    theta = np.linspace(0, 2 * np.pi, 3200)
    curves = []

    pole = 0.40
    strength = 0.48
    yscale = 0.86

    for R in np.linspace(0.79, 1.74, 38):
        z = R * np.exp(1j * theta)
        w = z + strength / (z - (pole + 0j))
        x = np.real(w)
        y = np.imag(w) * yscale
        curves.append((x, y))

    xmin = min(x.min() for x, y in curves)
    xmax = max(x.max() for x, y in curves)
    ymin = min(y.min() for x, y in curves)
    ymax = max(y.max() for x, y in curves)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    for i, (x, y) in enumerate(curves):
        X = 0.12 + 0.76 * (x - xmin) / (xmax - xmin)
        Y = 0.16 + 0.68 * (y - ymin) / (ymax - ymin)
        col = gold if i % 2 == 0 else blue
        ax.plot(X, Y, color=col,
                lw=0.72 if i % 2 == 0 else 0.68,
                alpha=0.86 if i % 2 == 0 else 0.78,
                solid_capstyle='round')

    t = np.linspace(0, 2 * np.pi, 400)
    for rr, alpha in [(0.007, 0.88), (0.014, 0.22)]:
        ax.plot(0.55 + rr * np.cos(t), 0.50 + rr * np.sin(t),
                color=ring, lw=1.15, alpha=alpha)

    # Equation label
    ax.text(0.06, 0.06, "w=z+a/(z\u2212z\u2080)",
            fontfamily='monospace', fontsize=8,
            color=(0.85, 0.80, 0.75, 0.35), transform=ax.transAxes)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "wonder_transform.pdf")
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
