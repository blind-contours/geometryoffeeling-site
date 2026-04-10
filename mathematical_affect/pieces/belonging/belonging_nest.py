"""
Geometry of Feeling — Belonging: Nest
Organic warm stone with domain-warped concentric rings and a deeper core.
The nest is where shape meets comfort — a form that holds without grasping.

Source: nest_v1b from R3b.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '..'))
from signature_utils import add_signature

ROOT_DIR = os.path.join(SCRIPT_DIR, '..', '..', '..')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
PRINT_DIR = os.path.join(ROOT_DIR, 'public', 'prints', 'belonging')

# ─── Figure constants ───
DPI = 300
FIG_W = 12
FIG_H = 8

# Margins
ML = FIG_W * 0.07
MR = FIG_W * 0.07
MB = FIG_H * 0.08
MT = FIG_H * 0.08
ART_L = ML
ART_R = FIG_W - MR
ART_B = MB
ART_T = FIG_H - MT
ART_W = ART_R - ART_L
ART_H = ART_T - ART_B
ART_CX = (ART_L + ART_R) / 2
ART_CY = (ART_B + ART_T) / 2

# ─── Palette ───
BG           = "#E8DFD0"
CREAM_WARM   = "#F0E0C8"
BLUSH        = "#E8C0B0"
APRICOT      = "#E8B898"
ROSE_DUST    = "#C89080"
HONEY        = "#D4A860"
SAND         = "#DCC290"
TERRACOTTA   = "#B87A60"
EMBER        = "#B8543C"
SAGE         = "#8BA092"
SAGE_LIGHT   = "#A8B8A0"
DUSTY_BLUE   = "#7892A5"
MEMBRANE_BLUE     = "#5A7A98"
MEMBRANE_BLUE_LT  = "#7A9AB0"
DEEP_WARM    = "#7A4A35"
DEEP_CRIMSON = "#5A1A0A"
DEEP_BURNT   = "#7A3020"
DEEP_SIENNA  = "#8A4028"


# ─── Utilities ───

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def _smooth_noise_fft(shape, rng, sigma):
    noise = rng.standard_normal(shape)
    ny, nx = shape
    ky = np.fft.fftfreq(ny).reshape(-1, 1)
    kx = np.fft.fftfreq(nx).reshape(1, -1)
    k_mag = np.sqrt(ky ** 2 + kx ** 2)
    H = np.exp(-((sigma * k_mag * 2 * np.pi) ** 2) / 2)
    return np.real(np.fft.ifft2(np.fft.fft2(noise) * H))


def fbm_noise(shape, rng, n_octaves=5, base_sigma=48.0, amp_decay=0.55):
    field = np.zeros(shape)
    amp = 1.0
    sigma = base_sigma
    for _ in range(n_octaves):
        field += amp * _smooth_noise_fft(shape, rng, sigma)
        amp *= amp_decay
        sigma /= 2.0
    m = np.abs(field).max()
    if m > 1e-9:
        field /= m
    return field


def make_fig():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.add_patch(Rectangle((0, 0), FIG_W, FIG_H, facecolor=BG,
                            edgecolor='none', zorder=-10))
    ax.add_patch(FancyBboxPatch((ML, MB), FIG_W - ML - MR, FIG_H - MB - MT,
                                boxstyle="square,pad=0",
                                facecolor=BG, edgecolor='none', zorder=0))
    zo = 1000
    for args in [((0, 0), FIG_W, MB), ((0, FIG_H - MT), FIG_W, MT),
                 ((0, 0), ML, FIG_H), ((FIG_W - MR, 0), MR, FIG_H)]:
        ax.add_patch(Rectangle(args[0], args[1], args[2],
                                facecolor=BG, edgecolor='none', zorder=zo))
    return fig, ax


def make_mesh(nx=900, ny=600):
    xs = np.linspace(ART_L - 0.1, ART_R + 0.1, nx)
    ys = np.linspace(ART_B - 0.1, ART_T + 0.1, ny)
    X, Y = np.meshgrid(xs, ys)
    ext = (xs[0], xs[-1], ys[0], ys[-1])
    return X, Y, ext


def boundary_mask(X, Y, power=6, fade=0.95):
    nx = (X - ART_CX) / (ART_W * 0.5 * fade)
    ny = (Y - ART_CY) / (ART_H * 0.5 * fade)
    return np.exp(-(nx ** power + ny ** power))


def _gauss(X, Y, cx, cy, sig):
    return np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * sig ** 2))


def _gauss_xy(X, Y, cx, cy, sx, sy):
    return np.exp(-((X - cx) ** 2 / (2 * sx ** 2)
                    + (Y - cy) ** 2 / (2 * sy ** 2)))


def render_mass(ax, field, extent, colors, alpha_gamma=0.5, alpha_max=1.0,
                zorder=3):
    f = np.clip(field, 0, 1)
    rgb_stops = np.array([hex_to_rgb(c) for c in colors])
    n = len(colors)
    scaled = f * (n - 1)
    idx = np.clip(scaled.astype(int), 0, n - 2)
    t = (scaled - idx)[..., None]
    col_a = rgb_stops[idx]
    col_b = rgb_stops[idx + 1]
    rgb = col_a * (1 - t) + col_b * t
    alpha = alpha_max * np.power(f, alpha_gamma)
    img = np.concatenate([rgb, alpha[..., None]], axis=-1)
    ax.imshow(img, extent=extent, origin='lower', aspect='auto',
              interpolation='bilinear', zorder=zorder)


def render_fbm_layer(ax, X, Y, ext, mask, color_hex, alpha_scale,
                     seed, n_octaves=5, base_sigma=50, zorder=5,
                     focal_mask=None):
    rng = np.random.default_rng(seed)
    noise = fbm_noise(X.shape, rng, n_octaves=n_octaves,
                      base_sigma=base_sigma, amp_decay=0.56)
    noise_pos = np.clip((noise + 0.15) * 0.75, 0, 1)
    rgba_img = np.zeros((*X.shape, 4))
    c = hex_to_rgb(color_hex)
    rgba_img[..., :3] = c
    effective_mask = mask * focal_mask if focal_mask is not None else mask
    rgba_img[..., 3] = noise_pos * effective_mask * alpha_scale
    ax.imshow(rgba_img, extent=ext, origin='lower', aspect='auto',
              interpolation='bilinear', zorder=zorder)


def render_blue_membrane(ax, X, Y, ext, outer_field, inner_field,
                         blue_colors, alpha_max=0.75, gamma=0.55,
                         fbm_seed=None, zorder=2):
    membrane = outer_field * np.power(1 - np.clip(inner_field, 0, 1), 1.5)
    membrane = np.clip(membrane, 0, 1)
    render_mass(ax, membrane, ext, colors=blue_colors,
                alpha_gamma=gamma, alpha_max=alpha_max, zorder=zorder)
    if fbm_seed is not None:
        render_fbm_layer(ax, X, Y, ext, membrane,
                         blue_colors[-1], 0.18,
                         seed=fbm_seed, base_sigma=55, zorder=zorder + 0.1)


def _domain_warp(X, Y, amp, seed):
    rng = np.random.default_rng(seed)
    X_w = X.copy()
    Y_w = Y.copy()
    for freq in [0.7, 1.3, 2.1]:
        px, py, ax_, ay_ = rng.uniform(0, 2 * np.pi, 4)
        X_w += (amp / freq) * np.sin(X * freq + px) * np.cos(Y * freq * 0.8 + py)
        Y_w += (amp / freq) * np.cos(X * freq * 0.7 + ax_) * np.sin(Y * freq + ay_)
    return X_w, Y_w


# ─── Nest field helper ───

def _nest_field(X, Y, cx, cy, a, b, ring_freq, ring_depth,
                falloff=2.2, warp_amp=0.35, warp_seed=0):
    X_w, Y_w = _domain_warp(X, Y, amp=warp_amp, seed=warp_seed)
    dx = (X_w - cx) / a
    dy = (Y_w - cy) / b
    r = np.sqrt(dx ** 2 + dy ** 2)
    glow = np.exp(-r ** 2 / falloff)
    rings = 0.5 + 0.5 * np.cos(r * ring_freq)
    rings = np.power(rings, ring_depth)
    return glow * (0.6 + 0.4 * rings), glow


# ─── Render ───

def render():
    fig, ax = make_fig()
    X, Y, ext = make_mesh()
    mask = boundary_mask(X, Y)

    f, glow = _nest_field(X, Y, ART_CX, ART_CY,
                          a=3.2, b=2.4, ring_freq=7, ring_depth=1.3,
                          falloff=2.0, warp_amp=0.32, warp_seed=1)
    f = f * mask
    glow = glow * mask

    X_w, Y_w = _domain_warp(X, Y, amp=0.32, seed=1)
    outer = _gauss_xy(X_w, Y_w, ART_CX, ART_CY, sx=4.5, sy=3.3) * mask

    render_blue_membrane(ax, X, Y, ext,
        outer_field=outer, inner_field=glow ** 0.7,
        blue_colors=[BG, MEMBRANE_BLUE_LT, MEMBRANE_BLUE, DUSTY_BLUE],
        alpha_max=0.65, gamma=0.52, fbm_seed=301, zorder=2)

    render_mass(ax, f, ext,
                colors=[BG, SAGE, ROSE_DUST, HONEY, TERRACOTTA,
                        DEEP_SIENNA, DEEP_CRIMSON],
                alpha_gamma=0.42, alpha_max=0.98, zorder=3)

    focal = _gauss(X, Y, ART_CX, ART_CY, sig=2.5)
    render_fbm_layer(ax, X, Y, ext, glow, "#F0D8A8", 0.40,
                     seed=303, base_sigma=55, zorder=5, focal_mask=focal)
    render_fbm_layer(ax, X, Y, ext, glow, DEEP_WARM, 0.28,
                     seed=305, base_sigma=42, zorder=5.1, focal_mask=focal)

    add_signature(fig, ax, BG, margin_piece=True, margin_bottom=FIG_H * 0.08)
    return fig


if __name__ == '__main__':
    fig = render()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "belonging_nest.pdf")
    fig.savefig(pdf_path, format='pdf', facecolor=BG)

    os.makedirs(PRINT_DIR, exist_ok=True)
    jpg_path = os.path.join(PRINT_DIR, "belonging_nest.jpg")
    fig.savefig(jpg_path, facecolor=BG, dpi=DPI, format='jpg',
                pil_kwargs={"quality": 96})

    plt.close(fig)
    print(f"saved {pdf_path}")
    print(f"saved {jpg_path}")
