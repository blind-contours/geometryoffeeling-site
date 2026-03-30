"""
Shared signature overlay utility for all piece scripts.

Places the artist's handwritten signature in the bottom-right of each piece.
Automatically inverts to white for dark backgrounds.

Uses figure-level coordinates so placement is independent of axes data limits.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Signature image path (relative to this file -> project root)
_SIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         '..', '..', 'signature.png')

# Cache the loaded image
_sig_cache = {}


def _load_signature():
    """Load and cache the signature image."""
    if 'img' not in _sig_cache:
        _sig_cache['img'] = plt.imread(_SIG_PATH)
    return _sig_cache['img'].copy()


def _hex_to_rgb01(h):
    """Convert hex color to (r, g, b) in [0, 1]."""
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def _perceived_luminance(r, g, b):
    """ITU-R BT.601 perceived luminance."""
    return 0.299 * r + 0.587 * g + 0.114 * b


def add_signature(fig, ax, bg_color, fig_w=12, fig_h=8, margin_piece=False,
                  margin_bottom=None):
    """Add handwritten signature to bottom-right of figure.

    Uses figure-fraction coordinates so placement works regardless of
    the data coordinate system used by each piece script.

    Parameters
    ----------
    fig : matplotlib Figure
    ax : matplotlib Axes (unused, kept for API compatibility)
    bg_color : str
        Hex color of the background (used for luminance detection).
    fig_w, fig_h : float
        Figure dimensions in inches (default 12x8). Only used for
        margin_bottom ratio calculation.
    margin_piece : bool
        If True, place signature in the margin area below artwork.
    margin_bottom : float or None
        Bottom margin height in data units (e.g., FIG_H * 0.08).
        Only used when margin_piece=True.
    """
    sig_img = _load_signature()

    # Determine signature color based on background luminance
    r, g, b = _hex_to_rgb01(bg_color)
    luminance = _perceived_luminance(r, g, b)
    if luminance < 0.4:
        # Invert RGB to white, keep alpha channel
        sig_img[:, :, :3] = 1.0 - sig_img[:, :, :3]

    # Signature size as fraction of figure: ~8% width
    sig_w_frac = 0.08
    sig_aspect = sig_img.shape[0] / sig_img.shape[1]  # height/width of image
    sig_h_frac = sig_w_frac * (fig_w / fig_h) * sig_aspect

    # Position in figure-fraction coordinates (0-1)
    x_frac = 1.0 - sig_w_frac - 0.02  # 2% from right edge
    if margin_piece and margin_bottom is not None:
        # Place in margin: center vertically in bottom margin
        margin_frac = margin_bottom / fig_h
        y_frac = (margin_frac - sig_h_frac) / 2
        if y_frac < 0.005:
            y_frac = 0.005
    else:
        y_frac = 0.02  # 2% from bottom edge

    # Create a small axes in figure-fraction coordinates for the signature
    # This is independent of the main axes' data coordinates
    sig_ax = fig.add_axes([x_frac, y_frac, sig_w_frac, sig_h_frac])
    sig_ax.imshow(sig_img, aspect='auto', alpha=0.85,
                  interpolation='antialiased')
    sig_ax.axis('off')
    sig_ax.set_zorder(1001 if margin_piece else 999)
