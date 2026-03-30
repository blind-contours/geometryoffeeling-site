"""
Geometry of Feeling — Growth: Growth Lissajous Bloom
Standalone render script
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import os

DPI=300; FIG_W=12; FIG_H=8
BG="#F5F0E6"

# Palette
MOSS="#4A7A3A"; LEAF="#6A9A4A"; GOLD="#C8920A"; AMBER="#D4A832"
CORAL="#C8603A"; SAGE="#7A9A6A"; SPRING="#8AB84A"; DARK_G="#2A4A1A"; TEAL="#3A8A6A"

def hex_to_rgb(h):
    h=h.lstrip('#')
    return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))

def rgba(h,a):
    c=hex_to_rgb(h)
    return (c[0],c[1],c[2],float(np.clip(a,0,1)))

def make_fig():
    fig=plt.figure(figsize=(FIG_W,FIG_H),dpi=DPI)
    ax=fig.add_subplot(111)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0,FIG_W); ax.set_ylim(0,FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    return fig,ax

PAD_L=0.72; PAD_R=0.60; PAD_T=0.65; PAD_B=0.88
PW=FIG_W-PAD_L-PAD_R; PH=FIG_H-PAD_T-PAD_B
cx=PAD_L+PW/2; cy=PAD_B+PH/2

def label(ax,eq):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.12,0.18,0.08,0.31),transform=ax.transData)
def split_segments(xs, ys):
    """Convert x,y arrays into line segments for LineCollection."""
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    return segs

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4):
    segs = split_segments(xs, ys)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def render():
    fig, ax = make_fig()

    # Multiple Lissajous figures at increasing amplitudes
    # Different frequency ratios create different "petal" patterns
    # As amplitude grows, the figures bloom outward

    configs = [
        # (a, b, delta_frac, label)  — frequency ratios and phase
        (1, 2, 0.0),    # figure-8 pattern
        (2, 3, 0.25),   # trefoil-like
        (3, 4, 0.0),    # more complex
        (3, 5, 0.5),    # intricate weave
        (5, 7, 0.25),   # highly detailed
        (4, 5, 0.1),    # four-fold
        (5, 6, 0.3),    # five-fold
        (7, 8, 0.15),   # seven-fold
    ]

    colors_cycle = [DARK_G, MOSS, LEAF, SPRING, TEAL, SAGE, GOLD, AMBER, CORAL]

    for ci, (a, b, delta_frac) in enumerate(configs):
        config_frac = ci / (len(configs) - 1)

        # Multiple amplitude rings for each frequency ratio
        n_rings = 8
        for ri in range(n_rings):
            ring_frac = (ri + 1) / n_rings

            # Amplitude grows for each ring
            amp_x = PW * 0.04 + PW * 0.40 * ring_frac * (0.5 + 0.5 * config_frac)
            amp_y = PH * 0.04 + PH * 0.40 * ring_frac * (0.5 + 0.5 * config_frac)

            # Phase shift creates rotation between rings
            delta = delta_frac * np.pi + ri * 0.12

            # Parametric curve
            n_pts = 2000
            t = np.linspace(0, 2 * np.pi, n_pts)

            xs = cx + amp_x * np.sin(a * t + delta)
            ys = cy + amp_y * np.sin(b * t)

            # Clip to canvas
            in_bounds = ((xs >= PAD_L + 0.02) & (xs <= PAD_L + PW - 0.02) &
                         (ys >= PAD_B + 0.02) & (ys <= PAD_B + PH - 0.02))

            # Find contiguous segments
            segments_list = []
            seg_start = None
            for j in range(len(in_bounds)):
                if in_bounds[j]:
                    if seg_start is None:
                        seg_start = j
                else:
                    if seg_start is not None:
                        if j - seg_start > 5:
                            segments_list.append((seg_start, j))
                        seg_start = None
            if seg_start is not None and len(in_bounds) - seg_start > 5:
                segments_list.append((seg_start, len(in_bounds)))

            col_idx = (ci + ri) % len(colors_cycle)
            col = colors_cycle[col_idx]

            # Outer rings more transparent
            alpha = 0.06 + 0.35 * (1 - ring_frac * 0.5) * (1 - config_frac * 0.3)
            lw = 0.2 + 1.2 * (1 - ring_frac * 0.4) * (1 - config_frac * 0.2)

            for s_start, s_end in segments_list:
                draw_lc(ax, xs[s_start:s_end], ys[s_start:s_end],
                        col, lw=lw, alpha=alpha, zo=3)

    # Add a faint center mark
    center_theta = np.linspace(0, 2 * np.pi, 100)
    for r in [0.05, 0.10, 0.15]:
        ccx = cx + r * np.cos(center_theta)
        ccy = cy + r * np.sin(center_theta)
        draw_lc(ax, ccx, ccy, GOLD, lw=0.3, alpha=0.08, zo=2)

    label(ax,
          "x = A\u00b7sin(a\u00b7t+\u03b4),  y = B\u00b7sin(b\u00b7t),  "
          "(a:b) \u2208 {1:2, 2:3, 3:4, 3:5, ...}")
    save(fig, "growth_lissajous_bloom.pdf")


if __name__ == '__main__':
    render()
