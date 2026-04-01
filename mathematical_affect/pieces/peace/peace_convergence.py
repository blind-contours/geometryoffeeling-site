"""
Geometry of Feeling — Peace: Convergence

Newton's method for z⁵−1=0. Every point in the complex plane
has a destination, and that destination is rest. The basin
boundaries show where the journey is most uncertain — but
every path still arrives. All conflict resolves.

Five-fold symmetry, off-center bloom with cascading fractal
chain. Warm copper palette with gold luminosity at the
petal junction.
"""

import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

DPI = 320
FIG_W, FIG_H = 12, 8
BG = '#F0EDE8'

# Peace series margins
PAD_L = 0.72; PAD_R = 0.60; PAD_T = 0.65; PAD_B = 0.88
PW = FIG_W - PAD_L - PAD_R
PH = FIG_H - PAD_T - PAD_B
ART_ASPECT = PW / PH

# Newton fractal parameters
N_ROOTS = 5
MAX_ITER = 160
COMP_RES = 2400  # computation grid height

# Composition: off-center bloom with chain trailing upper-right
BOUNDS_RAW = [-0.5, 1.7, -0.9, 0.55]
BLOOM_CENTER = (0, 0)

# Rendering
GLOW_RADIUS = 0.17
GLOW_STRENGTH = 0.44
GLOW_COLOR = np.array([0.96, 0.89, 0.72])
CONTRAST_STRENGTH = 0.80
BOUNDARY_WIDTH = 2
SHADE_RANGE = (0.42, 1.0)


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def soften(hex_color, amount):
    c = np.array(hex_to_rgb(hex_color))
    bg = np.array(hex_to_rgb(BG))
    return c + (bg - c) * amount


# Copper palette — soft but with warmth
PALETTE = [
    soften('#3A5848', 0.40),   # sage
    soften('#5A8878', 0.36),   # ocean
    soften('#8A7A58', 0.32),   # warm lichen/copper
    soften('#7A5A40', 0.30),   # deeper copper
    soften('#A0B8B0', 0.26),   # mineral
]


def adjust_bounds(bounds):
    """Widen bounds to match art area aspect ratio."""
    cx = (bounds[0] + bounds[1]) / 2
    cy = (bounds[2] + bounds[3]) / 2
    w = bounds[1] - bounds[0]
    h = bounds[3] - bounds[2]
    if w / h < ART_ASPECT:
        new_w = h * ART_ASPECT
        return [cx - new_w/2, cx + new_w/2, bounds[2], bounds[3]]
    else:
        new_h = w / ART_ASPECT
        return [bounds[0], bounds[1], cy - new_h/2, cy + new_h/2]


def compute_basins(bounds):
    """Newton's method for z^5 - 1 = 0."""
    res_y = COMP_RES
    res_x = int(res_y * (bounds[1] - bounds[0]) / (bounds[3] - bounds[2]))

    x = np.linspace(bounds[0], bounds[1], res_x)
    y = np.linspace(bounds[2], bounds[3], res_y)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    roots = np.exp(2j * np.pi * np.arange(N_ROOTS) / N_ROOTS)

    converged = np.zeros(Z.shape, dtype=bool)
    basin = np.full(Z.shape, -1, dtype=int)
    speed = np.full(Z.shape, float(MAX_ITER))

    for iteration in range(MAX_ITER):
        safe = (~converged) & (np.abs(Z) > 1e-12)
        if not safe.any():
            break
        Zn_1 = Z[safe] ** (N_ROOTS - 1)
        Zn = Z[safe] * Zn_1
        denom = N_ROOTS * Zn_1
        Z[safe] = Z[safe] - (Zn - 1) / (denom + 1e-30)

        for ri, root in enumerate(roots):
            newly = (~converged) & (np.abs(Z - root) < 1e-6)
            basin[newly] = ri
            speed[newly] = iteration
            converged[newly] = True

    remaining = ~converged
    if remaining.any():
        Z_rem = Z[remaining]
        dists = np.abs(Z_rem[:, np.newaxis] - roots[np.newaxis, :])
        basin[remaining] = np.argmin(dists, axis=1)

    return basin, speed, res_x, res_y


def detect_boundaries(basin):
    h, w = basin.shape
    boundary = np.zeros((h, w), dtype=float)
    for dy in range(-BOUNDARY_WIDTH, BOUNDARY_WIDTH + 1):
        for dx in range(-BOUNDARY_WIDTH, BOUNDARY_WIDTH + 1):
            if dy == 0 and dx == 0:
                continue
            shifted = np.roll(np.roll(basin, dy, axis=0), dx, axis=1)
            boundary += (basin != shifted).astype(float)
    return np.clip(boundary / (boundary.max() + 1e-10), 0, 1)


def render():
    bounds = adjust_bounds(BOUNDS_RAW)
    print(f"Computing basins ({COMP_RES}px, {MAX_ITER} iterations)...")
    basin, speed, res_x, res_y = compute_basins(bounds)

    bg_rgb = np.array(hex_to_rgb(BG))

    # ── Base color from basin + speed ──
    img = np.full((res_y, res_x, 3), bg_rgb)
    lo, hi = SHADE_RANGE

    for ri in range(N_ROOTS):
        color = np.array(PALETTE[ri])
        mask_ri = basin == ri
        s = speed[mask_ri] / MAX_ITER
        brightness = lo + (hi - lo) * (1.0 - s)
        for ch in range(3):
            img[mask_ri, ch] = (color[ch] * brightness
                                + bg_rgb[ch] * (1 - brightness))

    # ── Boundary contrast: crisp near bloom, fading outward ──
    print("Detecting boundaries...")
    boundary = detect_boundaries(basin)

    bx, by = BLOOM_CENTER
    x = np.linspace(bounds[0], bounds[1], res_x)
    y = np.linspace(bounds[2], bounds[3], res_y)
    X, Y = np.meshgrid(x, y)
    dist_data = np.sqrt((X - bx)**2 + (Y - by)**2)

    frame_diag = np.sqrt((bounds[1]-bounds[0])**2 + (bounds[3]-bounds[2])**2)
    falloff = np.clip(1.0 - (dist_data / (frame_diag * 0.45)) ** 1.8, 0.08, 1.0)

    darkness = boundary * falloff * CONTRAST_STRENGTH
    for ch in range(3):
        img[:, :, ch] *= (1.0 - darkness)

    # ── Luminosity event: gold glow at bloom center ──
    inner_glow = np.exp(-0.5 * (dist_data / GLOW_RADIUS)**2) * GLOW_STRENGTH
    outer_lift = np.exp(-0.5 * (dist_data / (GLOW_RADIUS * 2.5))**2) * (GLOW_STRENGTH * 0.4)

    for ch in range(3):
        img[:, :, ch] += inner_glow * (GLOW_COLOR[ch] - img[:, :, ch])
        img[:, :, ch] += outer_lift * (GLOW_COLOR[ch] * 0.95 - img[:, :, ch]) * 0.5

    img = np.clip(img, 0, 1)

    # ── Figure with margins ──
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')

    extent = [PAD_L, FIG_W - PAD_R, PAD_B, FIG_H - PAD_T]
    ax.imshow(img, extent=extent, origin='lower',
              interpolation='bilinear', aspect='auto', zorder=2)

    add_signature(fig, ax, BG)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, 'peace_convergence.pdf')
    fig.savefig(pdf_path, format='pdf', facecolor=BG)
    plt.close(fig)
    print(f"saved {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    render()
