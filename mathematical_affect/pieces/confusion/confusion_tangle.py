"""
Geometry of Feeling — Confusion: Confusion Tangle
Standalone render script
"""

"""
Geometry of Feeling — Confusion (Final Series)

Curated target: A physical string/rope that has knots and tangles in
specific places. Not abstract parametric curves but a continuous string
path that goes relatively straight in some places and gets knotted/tangled
in others. Like a string that someone has tangled.

Background: #E8E4E0 (light, uncertain)
Palette: muted pastels all mixed
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os


DPI=300; FIG_W=12; FIG_H=8
BG="#E8E4E0"

# Palette: muddled, uncertain
MURK="#6A6A68"; TANGLE_COL="#7A6A58"; FOG="#8A8A88"
UNCERTAIN="#5A6A70"; CROSSED="#7A5A68"; KNOT_COL="#6A5A50"
HAZE="#9A9A90"; DRIFT="#5A7070"; STATIC="#7A7A80"
MAUVE="#8A6A7A"; SAGE="#6A7A68"; CLAY="#8A7A60"

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
            color=(0.15,0.15,0.20,0.22),transform=ax.transData)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def make_knot(cx_k, cy_k, radius, n_loops, n_pts=400, phase=0):
    """Create a trefoil-like knot at a given position.
    Returns xs, ys arrays for the knot path."""
    t = np.linspace(0, 2*np.pi*n_loops, n_pts)
    # Trefoil-inspired knot: parametric curve that crosses over itself
    r = radius * (0.6 + 0.4 * np.sin(3*t + phase))
    xs = cx_k + r * np.cos(t + phase * 0.5) + radius * 0.15 * np.sin(5*t + phase)
    ys = cy_k + r * np.sin(t + phase * 0.3) * 0.8 + radius * 0.12 * np.cos(4*t + phase)
    return xs, ys


def make_tangle_region(cx_k, cy_k, radius, n_pts=500, seed=0):
    """Create a tangled region - string that loops around chaotically
    in a localized area, like a knot in a rope."""
    rng = np.random.RandomState(seed)
    t = np.linspace(0, 2*np.pi*3, n_pts)

    # Multiple overlapping loops of different sizes and orientations
    xs = cx_k + np.zeros_like(t)
    ys = cy_k + np.zeros_like(t)

    n_harmonics = 6
    for h in range(n_harmonics):
        freq = 1 + h * 0.7 + rng.uniform(-0.3, 0.3)
        amp_x = radius * rng.uniform(0.2, 0.8) / (1 + h * 0.3)
        amp_y = radius * rng.uniform(0.2, 0.7) / (1 + h * 0.3)
        phase_x = rng.uniform(0, 2*np.pi)
        phase_y = rng.uniform(0, 2*np.pi)
        xs += amp_x * np.sin(freq * t + phase_x)
        ys += amp_y * np.cos(freq * t + phase_y)

    return xs, ys


def render():
    fig,ax=make_fig()
    np.random.seed(42)

    # Create multiple strings that traverse the canvas with knots
    n_strings = 8

    cols = [MURK, TANGLE_COL, FOG, UNCERTAIN, CROSSED, KNOT_COL,
            HAZE, DRIFT, STATIC, MAUVE, SAGE, CLAY]

    for s in range(n_strings):
        col = cols[s % len(cols)]
        base_alpha = 0.25 + 0.25 * np.random.random()
        base_lw = 0.6 + 1.2 * np.random.random()

        # String path: goes from left to right with gentle undulation
        # and has 2-4 knot/tangle regions along the way
        n_total_pts = 4000
        t = np.linspace(0, 1, n_total_pts)

        # Base path: smooth left-to-right trajectory with gentle wave
        y_offset = PH * np.random.uniform(-0.05, 0.40)
        base_freq = np.random.uniform(0.5, 2.0)
        base_amp = PH * np.random.uniform(0.05, 0.18)

        xs = PAD_L + PW * t
        ys = cy + y_offset + base_amp * np.sin(2*np.pi*base_freq*t +
                                                np.random.uniform(0, 2*np.pi))
        ys += PH * 0.03 * np.sin(2*np.pi*2.3*t + np.random.uniform(0, 2*np.pi))

        # Add knot/tangle regions - localized chaotic loops
        n_knots = np.random.randint(2, 5)
        knot_centers = np.sort(np.random.uniform(0.1, 0.9, n_knots))

        for k_center in knot_centers:
            knot_width = np.random.uniform(0.04, 0.10)  # how wide the knot region is
            knot_amplitude = PH * np.random.uniform(0.08, 0.22)

            # Gaussian envelope for the knot - only affects nearby region
            envelope = np.exp(-((t - k_center) / knot_width)**2)

            # Chaotic loops within the knot
            n_harmonics = np.random.randint(3, 7)
            for h in range(n_harmonics):
                freq_h = np.random.uniform(8, 35)
                phase_h = np.random.uniform(0, 2*np.pi)
                amp_x = knot_amplitude * np.random.uniform(0.3, 1.0) / (1 + h * 0.2)
                amp_y = knot_amplitude * np.random.uniform(0.3, 1.0) / (1 + h * 0.2)
                xs += amp_x * np.sin(2*np.pi*freq_h*t + phase_h) * envelope
                ys += amp_y * np.cos(2*np.pi*freq_h*0.8*t + phase_h*1.3) * envelope

        # Smooth the path slightly for rope-like feel
        xs = gaussian_filter1d(xs, 3)
        ys = gaussian_filter1d(ys, 3)

        # Clip to canvas
        mask = ((xs > PAD_L - 0.3) & (xs < PAD_L + PW + 0.3) &
                (ys > PAD_B - 0.3) & (ys < PAD_B + PH + 0.3))

        if mask.sum() < 10:
            continue

        # Draw the string with varying width - thicker in knot regions
        pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        n_s = len(segs)

        # Compute local "tanglement" - how much the path deviates locally
        # More tangled = thicker line, higher alpha
        dx = np.diff(xs)
        dy = np.diff(ys)
        curvature = np.sqrt(dx**2 + dy**2)
        curvature = gaussian_filter1d(curvature, 20)
        curvature_norm = curvature / (curvature.max() + 1e-10)

        lws = base_lw * (0.5 + 1.5 * curvature_norm)
        alphas = base_alpha * (0.6 + 0.6 * curvature_norm)
        alphas = np.clip(alphas, 0.05, 0.7)

        colors = [rgba(col, float(a)) for a in alphas]

        lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                               capstyle='round', joinstyle='round',
                               zorder=3 + s % 3)
        ax.add_collection(lc)

    label(ax,"T(s) = \u222Bk(s)ds   \u2014   tangle:  a string knotted in places")
    save(fig,"confusion_tangle.pdf")


if __name__ == '__main__':
    render()
