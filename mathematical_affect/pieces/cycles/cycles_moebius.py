"""
Geometry of Feeling — Cycles: Cycles Moebius
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

# Palette: seasonal color rotation
SPRING="#5A9A50"; SUMMER="#C8A030"; AUTUMN="#B85A30"; WINTER="#4A6A90"
BLOSSOM="#C87898"; HARVEST="#9A7020"; FROST="#7A90A8"; EARTH="#6A5A40"
RENEWAL="#70B060"; DUSK="#8A6A50"; SAGE="#7A9A70"; AMBER="#D0A020"
DEEP_WINTER="#2A4A6A"; MOSS="#4A6A3A"

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
            color=(0.15,0.15,0.20,0.25),transform=ax.transData)
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


# ===================================================================
# MOEBIUS — Polished Ribbon
# A true 3D Mobius strip projected onto 2D, rendered as cross-section
# lines that reveal the half-twist. Deep teal to warm amber gradient
# with z-based depth for an organic, flowing feel.
# ===================================================================
def render():
    fig, ax = make_fig()

    # --- Mobius strip parametric surface ---
    # x(u,v) = (R + v*cos(u/2)) * cos(u)
    # y(u,v) = (R + v*cos(u/2)) * sin(u)
    # z(u,v) = v * sin(u/2)
    # u in [0, 2pi], v in [-w, w]

    R_strip = 2.6          # major radius of the strip
    w_strip = 1.15         # half-width of the ribbon (wider for more presence)
    n_u = 300              # number of cross-section lines around the loop
    n_v = 48               # points per cross-section line

    # Viewing angle — tilt the strip for a pleasing 3D perspective
    tilt_x = 0.62          # rotation around x-axis (radians) — look slightly more "down"
    tilt_y = 0.03          # minimal y-rotation to keep centered

    # Color endpoints: deep teal -> warm amber
    color_a = np.array([0.14, 0.46, 0.50])   # deep teal
    color_b = np.array([0.82, 0.58, 0.20])   # warm amber

    u_vals = np.linspace(0, 2 * np.pi, n_u, endpoint=False)
    v_vals = np.linspace(-w_strip, w_strip, n_v)

    # Projection scale — fill ~70% of canvas
    scale_x = PW * 0.33 / R_strip
    scale_y = PH * 0.47 / R_strip

    # Nudge center slightly left to compensate for perspective spread on back side
    cx_adj = cx - 0.25
    cy_adj = cy + 0.05

    # Precompute the full surface for z-ordering
    # Each cross-section is a line at fixed u, varying v
    cross_sections = []

    for i, u in enumerate(u_vals):
        cos_u2 = np.cos(u / 2)
        sin_u2 = np.sin(u / 2)
        cos_u = np.cos(u)
        sin_u = np.sin(u)

        # 3D coordinates for this cross-section
        x3d = (R_strip + v_vals * cos_u2) * cos_u
        y3d = (R_strip + v_vals * cos_u2) * sin_u
        z3d = v_vals * sin_u2

        # Apply rotation around x-axis (tilt forward)
        y_rot = y3d * np.cos(tilt_x) - z3d * np.sin(tilt_x)
        z_rot = y3d * np.sin(tilt_x) + z3d * np.cos(tilt_x)

        # Apply slight rotation around y-axis
        x_rot = x3d * np.cos(tilt_y) + z_rot * np.sin(tilt_y)
        z_final = -x3d * np.sin(tilt_y) + z_rot * np.cos(tilt_y)

        # Project to 2D (orthographic)
        xs_2d = cx_adj + x_rot * scale_x
        ys_2d = cy_adj + y_rot * scale_y

        # Average z for depth sorting and shading
        z_avg = np.mean(z_final)
        z_center = z_final[n_v // 2]  # z at the center of the cross-section

        cross_sections.append({
            'u': u,
            'u_frac': u / (2 * np.pi),
            'xs': xs_2d,
            'ys': ys_2d,
            'z_avg': z_avg,
            'z_center': z_center,
            'z_vals': z_final.copy(),
        })

    # Sort cross-sections by z_center so back lines are drawn first
    cross_sections.sort(key=lambda c: c['z_center'])

    # Compute global z range for normalization
    all_z = [c['z_center'] for c in cross_sections]
    z_min, z_max = min(all_z), max(all_z)
    z_range = z_max - z_min if z_max > z_min else 1.0

    # --- Draw cross-section lines ---
    for cs in cross_sections:
        xs = cs['xs']
        ys = cs['ys']
        u_frac = cs['u_frac']
        z_norm = (cs['z_center'] - z_min) / z_range  # 0 = back, 1 = front

        # Color: smooth gradient teal -> amber based on u position
        # Use a sine-based blend for smoother transition
        blend = 0.5 + 0.5 * np.sin(u_frac * 2 * np.pi - np.pi / 2)
        line_rgb = color_a * (1 - blend) + color_b * blend

        # Alpha: back parts fainter, front parts bolder
        # Gentle curve: even the back has presence
        alpha_base = 0.22 + 0.50 * (z_norm ** 0.75)

        # Line width: thicker in front, thinner in back
        lw_base = 0.55 + 1.7 * (z_norm ** 0.7)

        # Slight warm highlight on front-facing parts
        if z_norm > 0.65:
            highlight = (z_norm - 0.65) / 0.35
            line_rgb = line_rgb * (1 - highlight * 0.18) + np.array([1.0, 0.93, 0.82]) * (highlight * 0.18)

        line_rgb = np.clip(line_rgb, 0, 1)

        # Clip to canvas bounds
        mask = ((xs > PAD_L - 0.1) & (xs < PAD_L + PW + 0.1) &
                (ys > PAD_B - 0.1) & (ys < PAD_B + PH + 0.1))

        if np.sum(mask) < 3:
            continue

        # Build segments for this cross-section line
        pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)

        # Per-segment colors with alpha varying along the cross-section
        # for a soft, rounded edge feel
        n_segs = len(segs)
        colors = []
        lws = []
        for j in range(n_segs):
            if not (mask[j] and mask[min(j + 1, len(mask) - 1)]):
                colors.append((0, 0, 0, 0))
                lws.append(0)
                continue
            # Fade alpha toward the edges of the ribbon
            v_frac = abs(j - n_segs / 2) / (n_segs / 2)
            edge_fade = 1.0 - 0.45 * (v_frac ** 1.5)
            seg_alpha = alpha_base * edge_fade
            # Soften linewidth at edges too
            seg_lw = lw_base * (0.6 + 0.4 * edge_fade)
            colors.append((line_rgb[0], line_rgb[1], line_rgb[2], float(np.clip(seg_alpha, 0, 1))))
            lws.append(seg_lw)

        zo = int(z_norm * 100) + 2  # z-order based on depth
        lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                               capstyle='round', joinstyle='round', zorder=zo)
        ax.add_collection(lc)

    # --- Draw longitudinal "flow" lines along the strip ---
    # These trace the surface at fixed v positions, giving a sense of
    # continuous flow and making the twist more legible.
    # Only draw edges + center + a few intermediates for organic feel.
    n_pts_long = 1800
    u_smooth = np.linspace(0, 2 * np.pi, n_pts_long)

    # Specific v positions: edges, center, and a few intermediates
    v_positions = []
    # Two edges
    v_positions.append((-w_strip, 1.0))       # outer edge
    v_positions.append((w_strip, 1.0))        # other outer edge
    # Near-edges for thickness
    v_positions.append((-w_strip * 0.85, 0.5))
    v_positions.append((w_strip * 0.85, 0.5))
    # Center line
    v_positions.append((0.0, 0.7))
    # A few intermediates for texture
    for frac in [0.35, -0.35, 0.6, -0.6]:
        v_positions.append((w_strip * frac, 0.30))

    for v_pos, prominence in v_positions:

        cos_u2 = np.cos(u_smooth / 2)
        sin_u2 = np.sin(u_smooth / 2)
        cos_u = np.cos(u_smooth)
        sin_u = np.sin(u_smooth)

        x3d = (R_strip + v_pos * cos_u2) * cos_u
        y3d = (R_strip + v_pos * cos_u2) * sin_u
        z3d = v_pos * sin_u2

        y_rot = y3d * np.cos(tilt_x) - z3d * np.sin(tilt_x)
        z_rot = y3d * np.sin(tilt_x) + z3d * np.cos(tilt_x)
        x_rot = x3d * np.cos(tilt_y) + z_rot * np.sin(tilt_y)
        z_final = -x3d * np.sin(tilt_y) + z_rot * np.cos(tilt_y)

        xs_2d = cx_adj + x_rot * scale_x
        ys_2d = cy_adj + y_rot * scale_y

        # Per-segment coloring for the longitudinal lines
        pts = np.array([xs_2d, ys_2d]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)

        mask = ((xs_2d > PAD_L - 0.1) & (xs_2d < PAD_L + PW + 0.1) &
                (ys_2d > PAD_B - 0.1) & (ys_2d < PAD_B + PH + 0.1))

        n_segs = len(segs)
        colors = []
        lws = []
        for j in range(n_segs):
            if not (mask[j] and mask[min(j + 1, len(mask) - 1)]):
                colors.append((0, 0, 0, 0))
                lws.append(0)
                continue
            uf = u_smooth[j] / (2 * np.pi)
            z_here = z_final[j]
            z_n = np.clip((z_here - z_min) / z_range, 0, 1)

            blend = 0.5 + 0.5 * np.sin(uf * 2 * np.pi - np.pi / 2)
            rgb = color_a * (1 - blend) + color_b * blend
            rgb = np.clip(rgb, 0, 1)

            a = 0.08 + 0.40 * (z_n ** 0.9) * prominence
            lw_val = 0.3 + 1.0 * (z_n ** 0.85) * prominence

            # Edge lines: bolder
            is_edge = abs(abs(v_pos) - w_strip) < w_strip * 0.18
            if is_edge:
                a = 0.15 + 0.55 * (z_n ** 0.8) * prominence
                lw_val = 0.5 + 1.4 * (z_n ** 0.8) * prominence

            colors.append((rgb[0], rgb[1], rgb[2], float(np.clip(a, 0, 1))))
            lws.append(lw_val)

        zo_long = int(np.clip((np.mean(z_final) - z_min) / z_range, 0, 1) * 100) + 102
        lc = mc.LineCollection(segs, linewidths=lws, colors=colors,
                               capstyle='round', joinstyle='round', zorder=zo_long)
        ax.add_collection(lc)

    label(ax, "M\u00f6bius: (R+v\u00b7cos\u00bd u)\u00b7e^{iu}")
    save(fig, "cycles_moebius")


if __name__ == '__main__':
    render()
