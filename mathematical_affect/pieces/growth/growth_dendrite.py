"""
Geometry of Feeling — Growth: Growth Dendrite
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

    # Build a dendritic crystal with 6-fold symmetry
    # Each primary arm has secondary and tertiary branches at 60 deg offsets

    def draw_branch(ax, x0, y0, angle, length, depth, max_depth,
                    branch_scale, seg_list):
        """Recursively draw dendritic branch, collecting segments."""
        if depth > max_depth or length < 0.02:
            return

        # Main arm
        n_pts = max(20, int(length * 80))
        t = np.linspace(0, 1, n_pts)
        rad = np.radians(angle)

        # Slight taper along the arm
        taper = 1 - 0.1 * t  # arms get slightly thinner

        xs = x0 + length * t * np.cos(rad)
        ys = y0 + length * t * np.sin(rad)

        # Add crystalline texture — tiny regular oscillation perpendicular to arm
        perp_rad = rad + np.pi / 2
        texture = length * 0.008 * np.sin(t * np.pi * 12 * (1 + depth * 0.5))
        xs += texture * np.cos(perp_rad)
        ys += texture * np.sin(perp_rad)

        seg_list.append((xs, ys, depth, length))

        # Side branches at regular intervals along the arm
        n_side = max(2, int(6 - depth * 0.8))
        for si in range(n_side):
            branch_frac = (si + 1) / (n_side + 1)
            if branch_frac < 0.15 or branch_frac > 0.92:
                continue

            bx = x0 + length * branch_frac * np.cos(rad)
            by = y0 + length * branch_frac * np.sin(rad)

            # Branch at +60 and -60 degrees from parent
            for sign in [1, -1]:
                sub_angle = angle + sign * 60
                sub_length = length * branch_scale * (1 - branch_frac * 0.3)
                draw_branch(ax, bx, by, sub_angle, sub_length,
                            depth + 1, max_depth, branch_scale * 0.85, seg_list)

    # Six primary arms at 60-degree intervals
    n_arms = 6
    max_arm_length = min(PW, PH) * 0.42
    seg_list = []

    for arm in range(n_arms):
        base_angle = arm * 60 + 90  # start pointing up
        draw_branch(ax, cx, cy, base_angle, max_arm_length,
                    0, 4, 0.45, seg_list)

    # Now render all collected segments with proper coloring
    colors_by_depth = [DARK_G, MOSS, LEAF, TEAL, SAGE]

    for (xs, ys, depth, length) in seg_list:
        # Clip to canvas
        in_b = ((xs >= PAD_L + 0.02) & (xs <= PAD_L + PW - 0.02) &
                (ys >= PAD_B + 0.02) & (ys <= PAD_B + PH - 0.02))

        # Find contiguous segments
        segments_list = []
        seg_start = None
        for j in range(len(in_b)):
            if in_b[j]:
                if seg_start is None:
                    seg_start = j
            else:
                if seg_start is not None:
                    if j - seg_start > 2:
                        segments_list.append((seg_start, j))
                    seg_start = None
        if seg_start is not None and len(in_b) - seg_start > 2:
            segments_list.append((seg_start, len(in_b)))

        col = colors_by_depth[min(depth, len(colors_by_depth) - 1)]
        depth_frac = depth / 4.0
        alpha = 0.18 + 0.62 * (1 - depth_frac * 0.7)
        lw = 0.3 + 2.5 * (1 - depth_frac * 0.6) * min(1.0, length / max_arm_length * 2)

        for s_start, s_end in segments_list:
            draw_lc(ax, xs[s_start:s_end], ys[s_start:s_end],
                    col, lw=lw, alpha=alpha, zo=3 + depth)

    # Draw a faint hexagonal grid overlay to emphasize crystal structure
    for ring in range(1, 6):
        r = ring * min(PW, PH) * 0.08
        hex_theta = np.linspace(0, 2 * np.pi, 7)
        hx = cx + r * np.cos(hex_theta + np.pi / 6)
        hy = cy + r * np.sin(hex_theta + np.pi / 6)
        in_b = ((hx >= PAD_L) & (hx <= PAD_L + PW) &
                (hy >= PAD_B) & (hy <= PAD_B + PH))
        if in_b.all():
            draw_lc(ax, hx, hy, SAGE, lw=0.2, alpha=0.05, zo=2)

    label(ax,
          "r(\u03b8) = R\u00b7\u03a3 cos(6k\u03b8),  branch at \u00b160\u00b0")
    save(fig, "growth_dendrite.pdf")


if __name__ == '__main__':
    render()
