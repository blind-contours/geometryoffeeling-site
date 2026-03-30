"""
Geometry of Feeling — Growth: Growth Reaction Diffusion
Standalone render script
"""

import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
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

    # Multiple ring sources creating expanding wavefronts
    # Each ring is a parametric circle with growing radius and angular instabilities
    np.random.seed(137)

    # Three source points offset from center to create asymmetry
    sources = [
        (cx - PW * 0.05, cy + PH * 0.03),
        (cx + PW * 0.12, cy - PH * 0.08),
        (cx - PW * 0.10, cy - PH * 0.05),
    ]

    colors_cycle = [DARK_G, MOSS, LEAF, TEAL, SAGE, SPRING, GOLD, AMBER, CORAL]

    for si, (sx, sy) in enumerate(sources):
        n_rings = 22
        for ri in range(n_rings):
            frac = ri / (n_rings - 1)
            base_radius = 0.08 + frac * max(PW, PH) * 0.38

            # Angular resolution
            n_pts = 800
            theta = np.linspace(0, 2 * np.pi, n_pts)

            # Turing-like angular instabilities: higher modes grow with radius
            # This creates the "buckling" of the wavefront
            perturbation = np.zeros_like(theta)
            n_modes = 6 + ri  # more modes as ring expands
            for m in range(2, n_modes + 2):
                amp = base_radius * 0.015 * (frac ** 1.2) * (m ** -0.5)
                phase = si * 1.7 + m * 0.83 + ri * 0.31
                perturbation += amp * np.sin(m * theta + phase)

            # Additional organic wobble
            perturbation += base_radius * 0.008 * np.sin(3 * theta + si * 2.1 + ri * 0.5)

            r = base_radius + perturbation

            xs = sx + r * np.cos(theta)
            ys = sy + r * np.sin(theta)

            # Clip to canvas region
            in_bounds = ((xs >= PAD_L + 0.02) & (xs <= PAD_L + PW - 0.02) &
                         (ys >= PAD_B + 0.02) & (ys <= PAD_B + PH - 0.02))

            # Find contiguous segments within bounds
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

            # Color shifts with radius — inner rings dark, outer rings warm
            ci = int(frac * (len(colors_cycle) - 1))
            col = colors_cycle[ci]

            # Outer rings more transparent, inner rings bolder
            alpha = 0.10 + 0.55 * (1 - frac * 0.7)
            lw = 0.25 + 1.8 * (1 - frac * 0.6)

            # Source-specific alpha modulation
            source_alpha = [1.0, 0.75, 0.65][si]
            alpha *= source_alpha

            for s_start, s_end in segments_list:
                seg_xs = xs[s_start:s_end]
                seg_ys = ys[s_start:s_end]
                draw_lc(ax, seg_xs, seg_ys, col, lw=lw, alpha=alpha, zo=3 + si)

    # Draw faint radial lines from primary source to suggest diffusion direction
    for angle_deg in range(0, 360, 30):
        angle_rad = np.radians(angle_deg)
        line_r = np.linspace(0.05, max(PW, PH) * 0.4, 100)
        lx = sources[0][0] + line_r * np.cos(angle_rad)
        ly = sources[0][1] + line_r * np.sin(angle_rad)
        in_b = ((lx >= PAD_L + 0.05) & (lx <= PAD_L + PW - 0.05) &
                (ly >= PAD_B + 0.05) & (ly <= PAD_B + PH - 0.05))
        if in_b.sum() > 5:
            draw_lc(ax, lx[in_b], ly[in_b], SAGE, lw=0.25, alpha=0.05, zo=2)

    add_signature(fig, ax, BG)
    save(fig, "growth_reaction_diffusion.pdf")

if __name__ == '__main__':
    render()
