"""
Geometry of Feeling — Humility: Plumb
Converging field lines narrow into a single point of light, then continue as a
plumb line below it. A visual of proportion restored: one small point inside a
much larger field.
"""

import os
import numpy as np
import matplotlib
import sys as _sys; import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from signature_utils import add_signature
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "output")
PUBLIC_DIR = os.path.join(SCRIPT_DIR, "..", "..", "..", "public", "prints", "humility")

DPI = 320
FIG_W = 12
FIG_H = 8
MARGIN = "#CCC2AA"
BG = "#0A0A18"
PALETTE = ["#50A0D0", "#7868D0", "#C06060", "#D09040", "#E0B830", "#F0D040", "#F8E070"]


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def rgba(h, a):
    c = hex_to_rgb(h)
    return (c[0], c[1], c[2], float(np.clip(a, 0.0, 1.0)))


def make_fig():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=MARGIN)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=MARGIN, edgecolor="none", zorder=-20))
    x0, x1 = 0.07, 0.93
    y0, y1 = 0.08, 0.92
    ax.add_patch(
        FancyBboxPatch(
            (x0, y0),
            x1 - x0,
            y1 - y0,
            boxstyle="square,pad=0",
            facecolor=BG,
            edgecolor="none",
            zorder=-10,
        )
    )
    return fig, ax, (x0, x1, y0, y1)


def render():
    fig, ax, bounds = make_fig()
    x0, x1, y0, y1 = bounds
    center = (x0 + x1) / 2

    fan_width = 0.37
    top_y = 0.01
    point_y = 0.205
    line_bottom_y = 0.152
    n_lines = 40
    curve_power = 2.15
    point_glow = 1.25
    body_alpha = 0.25
    glow_alpha = 0.22

    rng = np.random.default_rng(1427)
    xs0 = np.linspace(center - fan_width, center + fan_width, n_lines)

    for i, start_x in enumerate(xs0):
        t = i / max(1, n_lines - 1)
        center_bias = 1 - abs(t - 0.5) * 2
        y = np.linspace(y1 - top_y, point_y, 620)
        p = (y - point_y) / ((y1 - top_y) - point_y + 1e-9)
        p = np.clip(p, 0, 1)

        x = center + (start_x - center) * (p ** curve_power)
        x += 0.006 * np.sin((1 - p) * 4.2 * np.pi + i * 0.33) * (0.35 + 0.65 * p)
        x += rng.normal(0.0, 0.0003, len(x))

        palette_idx = int(np.clip(center_bias, 0.0, 0.999) * len(PALETTE))
        color = PALETTE[min(palette_idx, len(PALETTE) - 1)]
        alpha = body_alpha * (0.42 + 0.9 * center_bias)
        lw = 0.32 + 1.02 * (0.35 + 0.65 * center_bias)

        ax.plot(
            x,
            y,
            color=rgba(color, alpha * glow_alpha),
            lw=lw * 2.1,
            solid_capstyle="round",
            zorder=2,
        )
        ax.plot(x, y, color=rgba(color, alpha), lw=lw, solid_capstyle="round", zorder=3)

    ax.plot([center, center], [point_y, line_bottom_y], color=rgba("#F0D060", 0.12), lw=2.0, zorder=5)
    ax.plot([center, center], [point_y, line_bottom_y], color=rgba("#F6E28A", 0.45), lw=0.85, zorder=6)

    for rr, alpha, color in [
        (0.040, 0.035 * point_glow, "#7868D0"),
        (0.025, 0.07 * point_glow, "#C06060"),
        (0.014, 0.14 * point_glow, "#F0D040"),
        (0.007, 0.28 * point_glow, "#F8E070"),
    ]:
        ax.add_patch(Circle((center, point_y), rr, facecolor=rgba(color, alpha), edgecolor="none", zorder=7))

    scar_x = np.linspace(x0 + 0.06, x1 - 0.06, 700)
    scar_y = np.full_like(scar_x, line_bottom_y) + 0.002 * np.sin(np.linspace(0, 9 * np.pi, len(scar_x)))
    ax.plot(scar_x, scar_y, color=rgba("#D09040", 0.08), lw=1.1, zorder=1)

    add_signature(fig, ax, MARGIN, margin_piece=True, margin_bottom=FIG_H * 0.08)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PUBLIC_DIR, exist_ok=True)

    pdf_path = os.path.join(OUTPUT_DIR, "humility_plumb.pdf")
    public_pdf_path = os.path.join(PUBLIC_DIR, "humility_plumb.pdf")
    jpg_path = os.path.join(PUBLIC_DIR, "humility_plumb.jpg")
    fig.savefig(pdf_path, facecolor=MARGIN, dpi=DPI)
    fig.savefig(public_pdf_path, facecolor=MARGIN, dpi=DPI)
    fig.savefig(jpg_path, facecolor=MARGIN, dpi=DPI, pil_kwargs={"quality": 96})
    plt.close(fig)
    print(f"saved {pdf_path}")
    print(f"saved {public_pdf_path}")
    print(f"saved {jpg_path}")
    return pdf_path, public_pdf_path, jpg_path


if __name__ == "__main__":
    render()
