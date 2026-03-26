"""
Geometry of Feeling — Solitude: Solitude Beacon
Standalone render script
"""

"""
Geometry of Feeling -- Solitude (Final Series v2)

Curated target: One isolated "person" (concentric circles with gold center)
at the top-right, radiating outward in blue/grey. Many small "people"
(concentric circle clusters) gathered at the bottom-left like droplets.
The solitary beacon stands apart, radiating.

Background: cool parchment (#E0DDD6)
Palette: deep grey, dark green, warm gold accent
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
BG="#E0DDD6"

# Palette
DEEP_GREY="#404850"; DARK_GREEN="#2A4A3A"; WARM_ACCENT="#C8963A"
SLATE="#5A6878"; CHARCOAL="#353D45"; MOSS="#3A5A42"
MIST="#8A9AA8"; LONE_GOLD="#D4A840"; IRON="#2A3038"
TEAL="#3A6A68"; SAGE="#5A7A60"; DUSK="#4A5068"
BONE="#C8C4B8"; NIGHT="#1A2028"

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
            color=(0.25,0.28,0.30,0.25),transform=ax.transData)

def draw_lc(ax,xs,ys,col,lw,alpha,zo=4,smooth=0):
    if smooth>0:
        ys=gaussian_filter1d(ys,smooth)
    pts=np.array([xs,ys]).T.reshape(-1,1,2)
    segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
    lc=mc.LineCollection(segs,linewidths=lw,colors=[rgba(col,alpha)],
                         capstyle='round',joinstyle='round',zorder=zo)
    ax.add_collection(lc)

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


def draw_person(ax, px, py, n_rings, max_r, has_gold_center=False,
                ring_alpha_base=0.35, ring_lw_base=0.8, zo_base=4):
    """Draw a 'person' as concentric circles (like a water droplet ripple)."""
    theta = np.linspace(0, 2*np.pi, 500)
    for i in range(n_rings):
        frac = i / max(n_rings - 1, 1)
        r = max_r * (0.04 + frac * 0.96)

        # Slight wobble for organic feel
        wobble = 1 + 0.006 * np.sin(5*theta + i*1.7)
        xs = px + r * wobble * np.cos(theta)
        ys = py + r * wobble * np.sin(theta)

        # Inverse falloff
        intensity = 1.0 / (1 + 2.5 * frac**1.2)
        alpha = ring_alpha_base * intensity
        lw = ring_lw_base * intensity

        if has_gold_center and frac < 0.20:
            col = LONE_GOLD
            alpha = min(alpha * 1.8, 0.75)
            lw = lw * 1.3
        elif has_gold_center and frac < 0.35:
            col = WARM_ACCENT
            alpha = alpha * 1.2
        elif frac < 0.5:
            col = DEEP_GREY
        elif frac < 0.75:
            col = SLATE
        else:
            col = MIST

        draw_lc(ax, xs, ys, col, lw=max(lw, 0.15), alpha=max(alpha, 0.03),
                zo=zo_base + int((1-frac)*3))

    # Center dot
    if has_gold_center:
        for r_g, a_g in [(0.06, 0.55), (0.12, 0.25), (0.20, 0.10)]:
            ax.add_patch(Circle((px, py), radius=r_g * max_r / 1.5,
                        facecolor=rgba(LONE_GOLD, a_g), edgecolor='none',
                        zorder=zo_base+5))
    else:
        # Small dark center dot for crowd members
        ax.add_patch(Circle((px, py), radius=max_r * 0.04,
                    facecolor=rgba(DEEP_GREY, 0.35), edgecolor='none',
                    zorder=zo_base+3))


def render():
    fig,ax=make_fig()
    np.random.seed(42)

    # === THE BEACON: isolated person at top-right ===
    beacon_x = cx + PW * 0.28
    beacon_y = cy + PH * 0.22
    beacon_max_r = min(PW, PH) * 0.32

    draw_person(ax, beacon_x, beacon_y, n_rings=30, max_r=beacon_max_r,
                has_gold_center=True, ring_alpha_base=0.45, ring_lw_base=1.2,
                zo_base=5)

    # === THE CROWD: many small people clustered at bottom-left ===
    # Positions clustered in bottom-left quadrant
    crowd_cx = cx - PW * 0.20
    crowd_cy = cy - PH * 0.15

    n_crowd = 35
    crowd_positions = []

    # Generate clustered positions — more people, bigger
    for i in range(n_crowd):
        angle = np.random.uniform(0, 2*np.pi)
        dist = np.random.exponential(0.30) * min(PW, PH) * 0.20
        px = crowd_cx + dist * np.cos(angle)
        py = crowd_cy + dist * np.sin(angle) * 0.8
        # Keep within bounds
        px = np.clip(px, PAD_L + 0.3, PAD_L + PW * 0.60)
        py = np.clip(py, PAD_B + 0.2, cy + PH * 0.10)
        crowd_positions.append((px, py))

    # Draw crowd members - larger, more visible
    for i, (px, py) in enumerate(crowd_positions):
        size = np.random.uniform(0.35, 0.70) * min(PW, PH) * 0.12
        n_rings = np.random.randint(8, 16)
        draw_person(ax, px, py, n_rings=n_rings, max_r=size,
                    has_gold_center=False, ring_alpha_base=0.35,
                    ring_lw_base=0.7, zo_base=3)

    # === CONCENTRIC RIPPLES FROM CROWD CENTER ===
    # Like droplets of water radiating outward from the crowd cluster
    theta = np.linspace(0, 2*np.pi, 1000)
    n_ripples = 40
    for i in range(n_ripples):
        frac = i / (n_ripples - 1)
        r = min(PW, PH) * (0.08 + frac * 0.65)

        # Slight wobble for organic feel
        wobble = 1 + 0.008 * np.sin(7*theta + i*2.3) + 0.005 * np.cos(11*theta + i*1.1)
        xs = crowd_cx + r * wobble * np.cos(theta)
        ys = crowd_cy + r * wobble * np.sin(theta) * 0.85

        # Clip to canvas
        mask = ((xs > PAD_L - 0.3) & (xs < PAD_L + PW + 0.3) &
                (ys > PAD_B - 0.3) & (ys < PAD_B + PH + 0.3))
        if mask.sum() < 10:
            continue

        # Inverse-distance falloff from center
        intensity = 1.0 / (1 + 3.0 * frac**1.2)
        alpha = 0.25 * intensity
        lw = 0.8 * intensity
        col = [DEEP_GREY, SLATE, MIST][i % 3]

        # Draw only visible segments
        in_seg = False; start = 0; segments = []
        for j in range(len(mask)):
            if mask[j] and not in_seg:
                start = j; in_seg = True
            elif not mask[j] and in_seg:
                if j - start >= 5:
                    segments.append((xs[start:j], ys[start:j]))
                in_seg = False
        if in_seg and len(mask) - start >= 5:
            segments.append((xs[start:], ys[start:]))

        for seg_xs, seg_ys in segments:
            draw_lc(ax, seg_xs, seg_ys, col, lw=max(lw, 0.1), alpha=max(alpha, 0.02), zo=2)

    # === SPRINKLED CLUSTERS above the main crowd ===
    # A few small droplet clusters scattered above and around
    np.random.seed(99)
    sprinkle_centers = [
        (crowd_cx - PW*0.08, crowd_cy + PH*0.25),
        (crowd_cx + PW*0.12, crowd_cy + PH*0.32),
        (crowd_cx - PW*0.18, crowd_cy + PH*0.18),
        (crowd_cx + PW*0.22, crowd_cy + PH*0.15),
        (crowd_cx + PW*0.05, crowd_cy + PH*0.40),
        (crowd_cx - PW*0.12, crowd_cy + PH*0.35),
    ]
    for sp_x, sp_y in sprinkle_centers:
        # 2-4 tiny people per sprinkle
        n_sp = np.random.randint(2, 5)
        for _ in range(n_sp):
            sx = sp_x + np.random.uniform(-0.4, 0.4)
            sy = sp_y + np.random.uniform(-0.3, 0.3)
            if PAD_L + 0.3 < sx < PAD_L + PW - 0.3 and PAD_B + 0.3 < sy < PAD_B + PH - 0.3:
                sz = np.random.uniform(0.20, 0.40) * min(PW, PH) * 0.10
                nr = np.random.randint(4, 10)
                draw_person(ax, sx, sy, n_rings=nr, max_r=sz,
                            has_gold_center=False, ring_alpha_base=0.25,
                            ring_lw_base=0.5, zo_base=3)

    label(ax,"A(r)=A\u2080/r\u00b2")
    save(fig,"solitude_beacon")


if __name__ == '__main__':
    render()
