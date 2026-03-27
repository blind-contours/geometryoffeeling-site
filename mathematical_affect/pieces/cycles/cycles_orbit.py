"""
Geometry of Feeling — Cycles: Cycles Orbit
Standalone render script
"""

"""
Geometry of Feeling — Cycles v2 (20 candidates)
Return, repetition, the loop that never quite closes the same way.

Dependencies: matplotlib, numpy, scipy
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
from matplotlib.patches import Circle
import os


DPI=300; FIG_W=12; FIG_H=8
BG="#F0E8DA"

# Warm palette for light background
SUN_CORE   = "#D4A020"
SUN_GLOW   = "#C88A18"
WARM_GOLD  = "#B8860B"
WARM_AMBER = "#A07020"
TEAL       = "#2A7A70"
CYAN       = "#3A6A80"
COOL_BLUE  = "#3A5A8A"
VIOLET     = "#5A4A7A"
PALE_BLUE  = "#6A7A9A"

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
            color=(0.3,0.3,0.35,0.25),transform=ax.transData)
def split_segments(xs, ys, mask):
    segments = []
    in_seg = False; start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg: start = j; in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3: segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3:
        segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax,xs,ys,col,lw,alpha,zo=4,smooth=0):
    if smooth>0: ys=gaussian_filter1d(ys,smooth)
    mask = (xs>PAD_L-0.1)&(xs<PAD_L+PW+0.1)&(ys>PAD_B-0.1)&(ys<PAD_B+PH+0.1)
    segs = split_segments(xs, ys, mask)
    for sx, sy in segs:
        if len(sx)<3: continue
        pts=np.array([sx,sy]).T.reshape(-1,1,2)
        s=np.concatenate([pts[:-1],pts[1:]],axis=1)
        lc=mc.LineCollection(s,linewidths=lw,colors=[rgba(col,alpha)],
                             capstyle='round',joinstyle='round',zorder=zo)
        ax.add_collection(lc)

def draw_lc_xy(ax,xs,ys,col,lw,alpha,zo=4):
    """Draw with clipping on both axes."""
    mask = (xs>PAD_L-0.1)&(xs<PAD_L+PW+0.1)&(ys>PAD_B-0.1)&(ys<PAD_B+PH+0.1)
    segs = split_segments(xs, ys, mask)
    for sx, sy in segs:
        if len(sx)<3: continue
        pts=np.array([sx,sy]).T.reshape(-1,1,2)
        s=np.concatenate([pts[:-1],pts[1:]],axis=1)
        lc=mc.LineCollection(s,linewidths=lw,colors=[rgba(col,alpha)],
                             capstyle='round',joinstyle='round',zorder=zo)
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


# ═══════════════════════════════════════════════════════════════
# 2. ORBIT — Perihelion: Keplerian orbits with beauty
# ═══════════════════════════════════════════════════════════════
def render():
    fig,ax=make_fig()
    rng = np.random.default_rng(42)

    # Sun position — slightly off-center (at one focus of ellipses)
    sun_x = cx - 0.6
    sun_y = cy + 0.15

    # --- Draw sun glow ---
    # Layered concentric circles for a warm glow effect
    glow_layers = [
        (1.8,  SUN_GLOW, 0.02),
        (1.3,  SUN_GLOW, 0.04),
        (0.9,  SUN_GLOW, 0.06),
        (0.60, SUN_GLOW, 0.10),
        (0.40, SUN_CORE, 0.15),
        (0.25, SUN_CORE, 0.25),
        (0.16, SUN_CORE, 0.40),
        (0.10, SUN_CORE, 0.60),
        (0.06, "#D4A840", 0.80),
        (0.035,"#E8C060", 0.95),
    ]
    for r, col, a in glow_layers:
        ax.add_patch(Circle((sun_x, sun_y), radius=r,
                    facecolor=rgba(col, a), edgecolor='none', zorder=6))

    # --- Define orbits ---
    # Each orbit: (semi_major, eccentricity, tilt_angle_deg, phase_offset)
    # Orbits increase in size; eccentricities vary for visual interest
    orbits = [
        # (a_scale, eccentricity, tilt_deg, body_phase, color)
        (0.32, 0.35, -12,  0.7,  WARM_GOLD),
        (0.48, 0.50,  25,  2.1,  WARM_AMBER),
        (0.62, 0.30, -35,  4.3,  WARM_AMBER),
        (0.80, 0.55,   8,  1.0,  TEAL),
        (1.00, 0.40, -20,  3.5,  TEAL),
        (1.18, 0.45,  40,  5.2,  CYAN),
        (1.40, 0.50, -15,  0.4,  COOL_BLUE),
        (1.65, 0.38,  30,  2.8,  VIOLET),
    ]

    n_pts = 1200  # points per orbit for smoothness
    theta = np.linspace(0, 2*np.pi, n_pts, endpoint=False)

    for idx, (a_scale, ecc, tilt_deg, body_phase, color) in enumerate(orbits):
        tilt = np.radians(tilt_deg)

        # Semi-major axis scaled to fill ~80% of canvas
        a = a_scale * PW * 0.36
        b = a * np.sqrt(1 - ecc**2)  # semi-minor from eccentricity

        # Ellipse in local frame (focus at origin)
        # r(theta) = a(1-e^2)/(1+e*cos(theta))  — polar form
        # But for drawing, parametric is smoother:
        # Center of ellipse is offset from focus by (a*e, 0)
        ex = a * np.cos(theta)  # center-based parametric
        ey = b * np.sin(theta)

        # Shift so that the sun is at one focus (focus offset = a*e along major axis)
        ex = ex - a * ecc  # shift so focus is at origin

        # Rotate by tilt angle
        rx = ex * np.cos(tilt) - ey * np.sin(tilt)
        ry = ex * np.sin(tilt) + ey * np.cos(tilt)

        # Translate to sun position
        rx += sun_x
        ry += sun_y

        # --- Compute distance from sun for each point (for thickness/alpha variation) ---
        dx = rx - sun_x
        dy = ry - sun_y
        dist = np.sqrt(dx**2 + dy**2)
        min_dist = dist.min()
        max_dist = dist.max()
        # Normalized: 0 at perihelion, 1 at aphelion
        dist_norm = (dist - min_dist) / (max_dist - min_dist + 1e-9)

        # --- Draw orbit with variable thickness and alpha ---
        # Thicker and brighter at perihelion (close), thinner and dimmer at aphelion
        base_lw = 0.4 + 0.7 * (1.0 - idx / len(orbits))  # outer orbits slightly thinner
        lw_arr = base_lw + 1.6 * (1.0 - dist_norm)  # thick at perihelion

        base_alpha = 0.15 + 0.35 * (1.0 - idx / len(orbits))
        alpha_arr = base_alpha + 0.35 * (1.0 - dist_norm)  # brighter at perihelion

        # Build segments with per-segment color/width
        pts = np.array([rx, ry]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        # Close the loop
        closing = np.array([[pts[-1, 0], pts[0, 0]]])
        segs = np.concatenate([segs, closing], axis=0)

        # Per-segment linewidths and colors
        lw_segs = np.append(lw_arr[:-1], lw_arr[-1])
        alpha_segs = np.append(alpha_arr[:-1], alpha_arr[-1])

        rgb = hex_to_rgb(color)
        colors = [(rgb[0], rgb[1], rgb[2], float(np.clip(al, 0, 1))) for al in alpha_segs]

        lc = mc.LineCollection(segs, linewidths=lw_segs, colors=colors,
                               capstyle='round', joinstyle='round', zorder=3)
        ax.add_collection(lc)

        # --- Draw a faint inner glow line for the brighter portions ---
        glow_alpha = alpha_arr * 0.3
        glow_colors = [(rgb[0], rgb[1], rgb[2], float(np.clip(ga, 0, 1))) for ga in glow_alpha]
        glow_lw = lw_segs * 2.5
        lc_glow = mc.LineCollection(segs, linewidths=glow_lw, colors=glow_colors,
                                    capstyle='round', joinstyle='round', zorder=2)
        ax.add_collection(lc_glow)

        # --- Draw orbital body (small bright dot) ---
        # Find position on orbit at the given phase
        body_idx = int((body_phase / (2*np.pi)) * n_pts) % n_pts
        bx, by = rx[body_idx], ry[body_idx]

        # Only draw if within canvas bounds
        if PAD_L < bx < PAD_L+PW and PAD_B < by < PAD_B+PH:
            # Body glow
            body_glow_layers = [
                (0.14, color, 0.06),
                (0.09, color, 0.12),
                (0.05, color, 0.25),
                (0.025, "#FFFFFF", 0.65),
                (0.012, "#FFFFFF", 0.95),
            ]
            for r, col, a in body_glow_layers:
                ax.add_patch(Circle((bx, by), radius=r,
                            facecolor=rgba(col, a), edgecolor='none', zorder=8))

            # --- Trailing tail showing motion direction ---
            tail_len = 60  # number of points for tail
            tail_indices = [(body_idx - j) % n_pts for j in range(tail_len)]
            tail_x = rx[tail_indices]
            tail_y = ry[tail_indices]

            # Tail segments
            tail_pts = np.array([tail_x, tail_y]).T.reshape(-1, 1, 2)
            tail_segs = np.concatenate([tail_pts[:-1], tail_pts[1:]], axis=1)

            # Fade out along tail
            tail_alphas = np.linspace(0.55, 0.0, len(tail_segs))
            tail_lws = np.linspace(1.8, 0.2, len(tail_segs))
            tail_colors = [(rgb[0], rgb[1], rgb[2], float(np.clip(ta, 0, 1)))
                          for ta in tail_alphas]

            lc_tail = mc.LineCollection(tail_segs, linewidths=tail_lws, colors=tail_colors,
                                        capstyle='round', joinstyle='round', zorder=7)
            ax.add_collection(lc_tail)

    # (Star field removed for light background)

    label(ax,"r(\u03b8)=a(1\u2212e\u00b2)/(1+e\u00b7cos\u03b8)")
    save(fig,"cycles_orbit")


if __name__ == '__main__':
    render()
