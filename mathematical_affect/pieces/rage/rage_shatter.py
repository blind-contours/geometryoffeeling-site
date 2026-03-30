"""
Geometry of Feeling — Rage: Rage Shatter
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
from matplotlib.patches import Circle
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#0E0E12"  # very dark — rage lives in darkness

# Palette: violent contrast against near-black
CRIMSON = "#C02020"; BLACK_ACCENT = "#181818"; EXPLOSIVE = "#E06020"
BLOOD = "#8A1818"; HOT_WHITE = "#F0E8E0"
SCAR = "#E04030"; EMBER = "#D05020"; ASH = "#808088"
FURNACE = "#C83818"; WOUND = "#A02028"

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2; cy = PAD_B + PH / 2

EQ_OPACITY = 0.55
SERIES_OPACITY = 0.38

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

def split_segments(xs, ys, mask):
    """Split masked arrays into contiguous segments to avoid straight-line jumps."""
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
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
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
    np.random.seed(303)

    # The break point — where the smooth curve detonates
    break_frac = 0.45
    break_x = PAD_L + PW * break_frac
    break_y = cy

    # Phase 1: smooth coherent curve approaching the break point
    t_pre = np.linspace(0, break_frac, 800)
    xs_pre = PAD_L + PW * t_pre
    # smooth sinusoidal — calm before the explosion
    ys_pre = cy + PH * 0.15 * np.sin(3 * np.pi * t_pre / break_frac)
    # slight upward trend toward break
    ys_pre += PH * 0.06 * (t_pre / break_frac)
    break_y = ys_pre[-1]

    # Draw the smooth curve in crimson — thick, confident
    draw_lc(ax, xs_pre, ys_pre, CRIMSON, lw=3.0, alpha=0.85, zo=6)

    # Phase 2: explosion — fragments radiating from the break point
    n_fragments = 120
    for i in range(n_fragments):
        # Each fragment launches from the break point at a random angle
        # biased rightward (the curve was going right)
        angle = np.random.uniform(-np.pi * 0.85, np.pi * 0.85)
        # some fragments go backward too — violence has no direction
        if np.random.random() < 0.20:
            angle = np.random.uniform(np.pi * 0.5, np.pi * 1.5)

        n_pts = np.random.randint(30, 120)
        t_frag = np.linspace(0, 1, n_pts)

        # speed varies — some shards fly far, some barely escape
        speed = np.random.uniform(0.15, 0.65) * PW
        # deceleration (fragments slow down as they fly)
        r = speed * t_frag * (1 - 0.3 * t_frag)

        # each fragment is a short curve segment — very slight curvature
        # not spiral, just a slight bend like flying debris
        angular_wobble = np.random.uniform(0.0, 0.08) * np.sin(
            np.random.uniform(1, 3) * np.pi * t_frag)

        xs_frag = break_x + r * np.cos(angle + angular_wobble)
        ys_frag = break_y + r * np.sin(angle + angular_wobble)

        mask = ((xs_frag > PAD_L) & (xs_frag < PAD_L + PW) &
                (ys_frag > PAD_B) & (ys_frag < PAD_B + PH))
        if mask.sum() < 3:
            continue

        # Color: closer to break = hotter
        cols = [CRIMSON, EXPLOSIVE, SCAR, FURNACE, EMBER, WOUND, HOT_WHITE, BLOOD]
        col = cols[i % len(cols)]

        for seg_xs, seg_ys in split_segments(xs_frag, ys_frag, mask):
            if len(seg_xs) < 3:
                continue
            pts = np.array([seg_xs, seg_ys]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            n_s = len(segs)
            # bright near the break, fading as they fly
            alphas = np.linspace(0.75, 0.06, n_s)
            lws = np.linspace(2.8, 0.4, n_s)
            colors = [rgba(col, float(a)) for a in alphas]
            lc_obj = mc.LineCollection(segs, linewidths=lws, colors=colors,
                                       capstyle='round', zorder=3 + i % 5)
            ax.add_collection(lc_obj)

    # Jagged shards near the break — sharp angular polylines
    n_big_shards = 20
    for i in range(n_big_shards):
        angle = np.random.uniform(-np.pi, np.pi)
        n_pts = np.random.randint(4, 9)
        # jagged polyline — each vertex is a sharp turn
        shard_xs = [break_x]
        shard_ys = [break_y]
        cur_angle = angle
        for k in range(n_pts):
            step = np.random.uniform(0.06, 0.25) * PW * 0.25
            cur_angle += np.random.uniform(-1.0, 1.0)
            shard_xs.append(shard_xs[-1] + step * np.cos(cur_angle))
            shard_ys.append(shard_ys[-1] + step * np.sin(cur_angle))
        shard_xs = np.array(shard_xs)
        shard_ys = np.array(shard_ys)
        shard_xs = np.clip(shard_xs, PAD_L, PAD_L + PW)
        shard_ys = np.clip(shard_ys, PAD_B, PAD_B + PH)
        col = [CRIMSON, EXPLOSIVE, HOT_WHITE, SCAR, FURNACE][i % 5]
        draw_lc(ax, shard_xs, shard_ys, col,
                lw=np.random.uniform(1.2, 2.8),
                alpha=np.random.uniform(0.45, 0.80), zo=7)

    # Hot-white flash at break point
    for r_c, a in [(0.35, 0.05), (0.18, 0.15), (0.08, 0.40), (0.03, 0.75)]:
        ax.add_patch(Circle((break_x, break_y), radius=r_c,
                    facecolor=rgba(HOT_WHITE, a), edgecolor='none', zorder=9))

    add_signature(fig, ax, BG)
    save(fig, "rage_shatter.pdf")

if __name__ == '__main__':
    render()
