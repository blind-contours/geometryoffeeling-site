"""
Geometry of Feeling — Wonder: Wonder Apollonian Gasket
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
from scipy.ndimage import gaussian_filter1d
from matplotlib.patches import Circle
import os

DPI = 300; FIG_W = 12; FIG_H = 8
BG = "#0A0A14"
MARGIN_COLOR = "#4d476d"

# Palette: cosmic -- deep indigo, gold, pale violet, white accent
INDIGO = "#2838A0"; DEEP_BLUE = "#182868"; GOLD = "#C8A030"
PALE_VIOLET = "#8878C0"; COSMIC_TEAL = "#2888A0"; NEBULA = "#4838A0"
STAR_WHITE = "#E8E4E0"; DIM_BLUE = "#384888"; AURORA = "#38A888"
DEEP_VIOLET = "#3828A0"; WARM_GOLD = "#D8B840"; ICE = "#88A8D0"
BRIGHT_GOLD = "#F0D060"; BRIGHT_VIOLET = "#A090E0"

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0, 1)))

def make_fig():
    from matplotlib.patches import FancyBboxPatch, Rectangle
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(MARGIN_COLOR)
    ax.set_facecolor(MARGIN_COLOR)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), FIG_W, FIG_H, facecolor=MARGIN_COLOR,
                            edgecolor='none', zorder=-10))
    ml = FIG_W * 0.07; mr = FIG_W * 0.07
    mb = FIG_H * 0.08; mt = FIG_H * 0.08
    ax.add_patch(FancyBboxPatch((ml, mb), FIG_W - ml - mr, FIG_H - mb - mt,
                                 boxstyle="square,pad=0",
                                 facecolor=BG, edgecolor='none', zorder=0))
    zo = 1000
    ax.add_patch(Rectangle((0, 0), FIG_W, mb, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, FIG_H - mt), FIG_W, mt, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((0, 0), ml, FIG_H, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    ax.add_patch(Rectangle((FIG_W - mr, 0), mr, FIG_H, facecolor=MARGIN_COLOR, edgecolor='none', zorder=zo))
    return fig, ax

PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R; PH = FIG_H - PAD_T - PAD_B
cx = PAD_L + PW / 2; cy = PAD_B + PH / 2

def split_segments(xs, ys, mask):
    segments = []
    in_seg = False
    start = 0
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
    if smooth > 0:
        ys = gaussian_filter1d(ys, smooth)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = mc.LineCollection(segs, linewidths=lw, colors=[rgba(col, alpha)],
                           capstyle='round', joinstyle='round', zorder=zo)
    ax.add_collection(lc)

def save(fig, name):
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR, name),
                format='pdf', facecolor=MARGIN_COLOR)
    plt.close(fig); print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

def render():
    fig, ax = make_fig()

    # Descartes Circle Theorem: given three mutually tangent circles with
    # curvatures k1, k2, k3, the fourth tangent circle has curvature:
    # k4 = k1 + k2 + k3 + 2*sqrt(k1*k2 + k2*k3 + k1*k3)
    # (or the minus variant for the outer circle)

    # A circle is represented as (curvature, center_x, center_y)
    # Curvature k = 1/r, negative for the outer bounding circle

    # Use complex numbers for Descartes with positions (Soddy)
    # k4*z4 = k1*z1 + k2*z2 + k3*z3 + 2*sqrt(k1*k2*z1*z2 + k2*k3*z2*z3 + k1*k3*z1*z3)

    # We'll work in a local coordinate system centered at (cx, cy)
    # with the outer circle having radius R

    R = min(PW, PH) * 0.46  # large outer circle to fill the frame

    # The outer bounding circle: curvature = -1/R (negative = bounding)
    k_outer = -1.0 / R

    # Start with the standard Apollonian configuration:
    # Three mutually tangent circles inside a bounding circle.
    # For a symmetric start: three equal circles of radius r = R/(1+2/sqrt(3))
    # tangent to each other and to the outer circle.

    # For three equal inner circles tangent to outer circle of radius R:
    # r = R * (2*sqrt(3) - 3) / 3  (approximate, let's compute properly)
    # Actually, for three equal circles packed inside a circle:
    # r = R / (1 + 2/sqrt(3))
    r_inner = R / (1 + 2.0 / np.sqrt(3))
    k_inner = 1.0 / r_inner

    # Centers of the three inner circles (120 degrees apart)
    # Distance from center to inner circle center = R - r_inner
    d = R - r_inner
    centers = []
    for i in range(3):
        angle = np.pi / 2 + i * 2 * np.pi / 3  # start from top
        centers.append(complex(d * np.cos(angle), d * np.sin(angle)))

    # Store all circles to draw: list of (center_x, center_y, radius, depth)
    circles_to_draw = []

    # The outer bounding circle
    circles_to_draw.append((0, 0, R, 0))

    # The three initial inner circles
    for c in centers:
        circles_to_draw.append((c.real, c.imag, r_inner, 1))

    # Recursive fill using Descartes theorem
    # For each triple of mutually tangent circles, find the two Soddy circles
    # We track (k, k*z) for the complex Descartes theorem

    def descartes_k(k1, k2, k3):
        """Return the two possible fourth curvatures."""
        s = k1 + k2 + k3
        d = 2 * np.sqrt(abs(k1 * k2 + k2 * k3 + k1 * k3))
        return s + d, s - d

    def descartes_center(k1, z1, k2, z2, k3, z3, k4):
        """Return center of fourth circle given curvatures and centers."""
        # k4*z4 = k1*z1 + k2*z2 + k3*z3 + 2*sqrt(k1*k2*z1*z2 + k2*k3*z2*z3 + k1*k3*z1*z3)
        w1 = k1 * z1; w2 = k2 * z2; w3 = k3 * z3
        s = w1 + w2 + w3
        disc = k1 * k2 * z1 * z2 + k2 * k3 * z2 * z3 + k1 * k3 * z1 * z3
        # Take the sqrt carefully
        sqrt_disc = np.sqrt(disc) if disc.real >= 0 else 1j * np.sqrt(-disc)
        z4_plus = (s + 2 * sqrt_disc) / k4 if abs(k4) > 1e-12 else 0
        z4_minus = (s - 2 * sqrt_disc) / k4 if abs(k4) > 1e-12 else 0
        return z4_plus, z4_minus

    # Build the gasket recursively
    # A "triple" is (k1, z1, k2, z2, k3, z3)
    # For each triple, we find the new circle, then create 3 new triples

    min_radius = 0.012  # stop recursion when circles get too small
    max_depth = 8

    # Initial triples: each pair of inner circles + the outer circle
    # We need to carefully set up the initial configuration
    k0 = k_outer; z0 = complex(0, 0)
    k1 = k_inner; z1 = centers[0]
    k2 = k_inner; z2 = centers[1]
    k3 = k_inner; z3 = centers[2]

    def find_fourth(ka, za, kb, zb, kc, zc, existing_k=None):
        """Find the fourth Soddy circle not matching existing_k."""
        k_plus, k_minus = descartes_k(ka, kb, kc)
        z_plus_a, z_plus_b = descartes_center(ka, za, kb, zb, kc, zc, k_plus)
        z_minus_a, z_minus_b = descartes_center(ka, za, kb, zb, kc, zc, k_minus)

        results = []
        for k_try, z_options in [(k_plus, [z_plus_a, z_plus_b]),
                                  (k_minus, [z_minus_a, z_minus_b])]:
            if existing_k is not None and abs(k_try - existing_k) < 1e-6:
                continue
            if k_try < 0:
                continue  # skip outer/bounding solutions
            r_try = 1.0 / k_try if abs(k_try) > 1e-12 else 1e12
            if r_try < min_radius:
                continue
            # Pick the center that is geometrically valid
            for z_try in z_options:
                # Check tangency with all three circles
                valid = True
                for kx, zx in [(ka, za), (kb, zb), (kc, zc)]:
                    expected_dist = abs(1.0 / k_try) + (1.0 / kx if kx > 0 else -1.0 / abs(kx))
                    if kx < 0:
                        expected_dist = abs(1.0 / abs(kx)) - abs(1.0 / k_try)
                    actual_dist = abs(z_try - zx)
                    if abs(actual_dist - abs(expected_dist)) > r_try * 0.3:
                        valid = False
                        break
                if valid:
                    results.append((k_try, z_try))
                    break
        return results

    # Use a queue-based approach
    queue = []

    # First, find the Soddy circle for each curvilinear triangle
    # Triangle 1: outer, c1, c2
    # Triangle 2: outer, c2, c3
    # Triangle 3: outer, c3, c1
    # Triangle 4: c1, c2, c3

    initial_triples = [
        (k0, z0, k1, z1, k2, z2),
        (k0, z0, k2, z2, k3, z3),
        (k0, z0, k3, z3, k1, z1),
        (k1, z1, k2, z2, k3, z3),
    ]

    for triple in initial_triples:
        ka, za, kb, zb, kc, zc = triple
        results = find_fourth(ka, za, kb, zb, kc, zc)
        for k_new, z_new in results:
            r_new = 1.0 / k_new
            if r_new >= min_radius:
                circles_to_draw.append((z_new.real, z_new.imag, r_new, 2))
                # Create three new triples
                if r_new > min_radius * 2:
                    queue.append((ka, za, kb, zb, k_new, z_new, 3))
                    queue.append((ka, za, kc, zc, k_new, z_new, 3))
                    queue.append((kb, zb, kc, zc, k_new, z_new, 3))

    # Process queue
    visited = set()
    while queue:
        ka, za, kb, zb, kc, zc, depth = queue.pop(0)
        if depth > max_depth:
            continue

        # Create a key for deduplication
        key = tuple(sorted([(round(ka, 4), round(za.real, 4), round(za.imag, 4)),
                            (round(kb, 4), round(zb.real, 4), round(zb.imag, 4)),
                            (round(kc, 4), round(zc.real, 4), round(zc.imag, 4))]))
        if key in visited:
            continue
        visited.add(key)

        results = find_fourth(ka, za, kb, zb, kc, zc)
        for k_new, z_new in results:
            r_new = 1.0 / k_new
            if r_new < min_radius:
                continue
            # Check it's inside the outer circle
            if abs(z_new) + r_new > R * 1.05:
                continue
            circles_to_draw.append((z_new.real, z_new.imag, r_new, depth))
            if r_new > min_radius * 1.5 and depth < max_depth:
                queue.append((ka, za, kb, zb, k_new, z_new, depth + 1))
                queue.append((ka, za, kc, zc, k_new, z_new, depth + 1))
                queue.append((kb, zb, kc, zc, k_new, z_new, depth + 1))

    print(f"  Apollonian gasket: {len(circles_to_draw)} circles generated")

    # Draw all circles
    # Color by depth: outer = deep indigo, inner = bright gold
    max_d = max(c[3] for c in circles_to_draw) if circles_to_draw else 1

    for (ccx, ccy, r, d) in circles_to_draw:
        # Map to canvas coordinates
        draw_x = cx + ccx
        draw_y = cy + ccy

        depth_frac = d / max(max_d, 1)

        # Color interpolation: deep indigo (d=0) -> pale violet (mid) -> bright gold (deep)
        if depth_frac < 0.3:
            col = DEEP_BLUE
        elif depth_frac < 0.5:
            col = INDIGO
        elif depth_frac < 0.7:
            col = PALE_VIOLET
        elif depth_frac < 0.85:
            col = WARM_GOLD
        else:
            col = BRIGHT_GOLD

        # Opacity: larger circles more opaque, but all boosted +35%
        if d == 0:
            # Outer bounding circle
            alpha = 0.50
            lw = 1.8
        else:
            base_alpha = 0.30 + 0.45 * (1 - depth_frac)
            alpha = min(base_alpha, 0.85)
            lw = max(0.3, 2.0 * (1 - depth_frac * 0.7))

        # Draw circle outline
        theta = np.linspace(0, 2 * np.pi, max(60, int(200 * r / R)))
        xs_c = draw_x + r * np.cos(theta)
        ys_c = draw_y + r * np.sin(theta)

        # Check bounds
        if draw_x - r > PAD_L + PW or draw_x + r < PAD_L:
            continue
        if draw_y - r > PAD_B + PH or draw_y + r < PAD_B:
            continue

        ax.plot(xs_c, ys_c, color=rgba(col, alpha), linewidth=lw,
                solid_capstyle='round', zorder=3 + d)

        # Add subtle fill for smaller circles
        if d >= 3 and r < R * 0.15:
            fill_alpha = 0.04 + 0.08 * depth_frac
            circle_patch = Circle((draw_x, draw_y), radius=r,
                                  facecolor=rgba(col, fill_alpha),
                                  edgecolor='none', zorder=2 + d)
            ax.add_patch(circle_patch)

    add_signature(fig, ax, MARGIN_COLOR, margin_piece=True, margin_bottom=FIG_H * 0.08)
    save(fig, "wonder_apollonian_gasket.pdf")

if __name__ == '__main__':
    render()
