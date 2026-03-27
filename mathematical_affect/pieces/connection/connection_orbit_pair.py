"""
Geometry of Feeling — Connection: Orbit Pair
Standalone render script
"""

"""
Geometry of Feeling — Connection v3 (revised based on feedback)
Key changes:
- Rose gold + gold as the two-curve palette
- "Orbiting but not merging" as core direction
- Regenerate: Lorenz→orbit-pair, Magnetic→field-focused, Murmuration→coherent
- Enhance: Entanglement, Double Helix, Pendulum with rose gold
- Keep favorites: Coupled, Lissajous, Torus Knot, Rossler, Phase Sync, Weave
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os


DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#0A0A12"
MARGIN_COLOR = "#E8D8B8"

# ROSE GOLD + GOLD palette (user request)
ROSE_GOLD = "#C8887A"
WARM_ROSE = "#D4988A"
SOFT_ROSE = "#B87A70"
GOLD = "#E8C878"
AMBER = "#D4A856"
PALE_GOLD = "#F0D890"
WARM_WHITE = "#F0E8D8"
COPPER = "#C49A3C"
BRONZE = "#B08830"

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(MARGIN_COLOR)
    ax.set_facecolor(BG)
    ax.set_position([0.07, 0.08, 0.86, 0.84])
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    return fig, ax

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW/2; cy = PAD_B + PH/2

def label(ax, eq, note=None):
    ax.text(0.75,0.75,eq,fontfamily='monospace',fontsize=10,
            color=(0.85,0.80,0.75,0.55),transform=ax.transData)
def split_segments(xs, ys, mask):
    segments = []
    in_seg = False; start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j; in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3:
                segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3:
        segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax, xs, ys, col, lw, alpha, zo=4, smooth=0):
    if len(xs) < 2: return
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def draw_lc_gradient(ax, xs, ys, col, lw_s, lw_e, a_s, a_e, zo=4, smooth=0):
    if len(xs) < 2: return
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    n = len(segs)
    alphas = np.linspace(a_s, a_e, n)
    lws = np.linspace(lw_s, lw_e, n)
    colors = [rgba(col, float(a)) for a in alphas]
    lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def head(ax, x, y):
    ax.plot(x, y, 'o', color=rgba(WARM_WHITE, 0.10), markersize=18, markeredgewidth=0, zorder=8)
    ax.plot(x, y, 'o', color=rgba(WARM_WHITE, 0.25), markersize=9, markeredgewidth=0, zorder=9)
    ax.plot(x, y, 'o', color=rgba(WARM_WHITE, 0.55), markersize=4, markeredgewidth=0, zorder=10)

def save(fig, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Ensure name ends with .pdf
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=MARGIN_COLOR)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


# ============================================================================
# 3. ORBIT PAIR — Two curves orbiting each other, not merging.
#    Uses coupled nonlinear oscillators that orbit a shared center.
# ============================================================================
def render():
    fig, ax = make_fig()
    dt = 0.003; n_steps = 15000
    # Two particles orbiting a shared center with mutual perturbation
    # Particle 1: elliptical orbit
    th1, r1 = 0.0, PW*0.28
    th2, r2 = np.pi, PW*0.22
    w1, w2 = 1.0, 1.3  # angular velocities

    trail1_x, trail1_y = [], []
    trail2_x, trail2_y = [], []

    for step in range(n_steps):
        # Slightly elliptical orbits with mutual perturbation
        e1 = 0.2 + 0.05*np.sin(0.1*step*dt)
        e2 = 0.15 + 0.05*np.cos(0.13*step*dt)

        x1 = cx + r1*(1 + e1*np.cos(2*th1))*np.cos(th1)
        y1 = cy + r1*(1 + e1*np.cos(2*th1))*np.sin(th1)*(PH/PW)
        x2 = cx + r2*(1 + e2*np.cos(2*th2))*np.cos(th2)
        y2 = cy + r2*(1 + e2*np.cos(2*th2))*np.sin(th2)*(PH/PW)

        trail1_x.append(x1); trail1_y.append(y1)
        trail2_x.append(x2); trail2_y.append(y2)

        # Mutual perturbation — each slightly pulls the other
        dx, dy = x2-x1, y2-y1
        dist = np.sqrt(dx**2 + dy**2) + 0.5
        perturb = 0.003 / dist

        th1 += w1*dt + perturb*np.sin(th2-th1)*dt
        th2 += w2*dt + perturb*np.sin(th1-th2)*dt

    t1x, t1y = np.array(trail1_x), np.array(trail1_y)
    t2x, t2y = np.array(trail2_x), np.array(trail2_y)

    draw_lc_gradient(ax, t1x, t1y, ROSE_GOLD, 0.3, 1.6, 0.06, 0.48, zo=4)
    draw_lc_gradient(ax, t2x, t2y, GOLD, 0.3, 1.6, 0.06, 0.48, zo=5)
    head(ax, t1x[-1], t1y[-1]); head(ax, t2x[-1], t2y[-1])

    label(ax, "d\u03b8/dt = \u03c9 + \u03b5\u00b7sin(\u03b8\u2082-\u03b8\u2081)/r")
    save(fig, "connection_orbit_pair.pdf")


if __name__ == '__main__':
    render()
