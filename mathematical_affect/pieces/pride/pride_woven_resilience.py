"""
Geometry of Feeling — Pride: Woven Resilience
Community as fabric: interlocking sinusoidal strands.
Trans palette horizontal, rainbow vertical — woven together.
"""

import os
import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 300
FIG_W = 12
FIG_H = 8
BG_COLOR = '#f3eee7'

PAL_TRANS = ['#f6f2ef', '#f5a9b8', '#5bcffb', '#ffd100', '#7f2dbd']
PAL_RAINBOW = ['#E40303', '#FF8C00', '#FFED00', '#008026', '#004DFF', '#750787']

def smooth_palette(cols, n):
    rgba = np.array([mcolors.to_rgba(c) for c in cols])
    xs = np.linspace(0, 1, len(rgba))
    t = np.linspace(0, 1, n)
    return np.column_stack([np.interp(t, xs, rgba[:, k]) for k in range(4)])

def render():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG_COLOR)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Margins to keep art contained within frame
    mx, my = 0.08, 0.10  # horizontal / vertical margin
    nh, nv = 18, 18
    ch = smooth_palette(PAL_TRANS, nh)
    cv = smooth_palette(PAL_RAINBOW, nv)
    t_h = np.linspace(mx, 1 - mx, 800)   # horizontal lines stay within x margins
    t_v = np.linspace(my, 1 - my, 800)   # vertical lines stay within y margins

    for i in range(nh):
        by = my + (1 - 2 * my) * i / (nh - 1)
        ax.plot(t_h, by + 0.018 * np.sin(2 * np.pi * nv * 0.5 * t_h + i * np.pi),
                color=ch[i], lw=0.8, alpha=0.85)

    for j in range(nv):
        bx = mx + (1 - 2 * mx) * j / (nv - 1)
        ax.plot(bx + 0.018 * np.sin(2 * np.pi * nh * 0.5 * t_v + j * np.pi), t_v,
                color=cv[j], lw=0.8, alpha=0.85)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "pride_woven_resilience.pdf")
    add_signature(fig, ax, BG_COLOR)
    fig.savefig(pdf_path, facecolor=BG_COLOR, dpi=DPI)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    render()
