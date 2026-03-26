"""
Geometry of Feeling — Solitude: Solitude Signal
Standalone render script
"""

"""
Geometry of Feeling -- Solitude (Final Series v2)

Curated target: ~40 overlapping sine waves of various frequencies and
amplitudes spanning the canvas horizontally. One distinct yellow/gold
signal in the center stands out from all the noise. A lone voice in
a crowded frequency spectrum.

Background: cool parchment (#E0DDD6)
Palette: deep grey, dark green, warm gold accent

Approach: Render each wave as a series of vertical amplitude lines
(waveform/oscilloscope style) rather than continuous curves. This creates
a spectrogram-like texture with natural breathing room between strokes.
The gold signal uses clean, tall verticals to pierce through the noise.
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


# =============================================================================
# SIGNAL -- ~40 overlapping sine waves rendered as vertical amplitude bars,
# one distinct yellow/gold signal piercing through the center
# =============================================================================
def render():
    fig,ax=make_fig()
    np.random.seed(77)

    # --- Sampling grid for vertical bars ---
    # Each wave will be sampled at these x-positions and drawn as a
    # vertical line from the center axis to the wave's amplitude.
    n_bars = 280  # number of x-sample positions across the canvas
    t_positions = np.linspace(0, 1, n_bars)
    x_positions = PAD_L + PW * t_positions

    # Horizontal center line -- subtle, grounding
    ax.plot([PAD_L - 0.15, PAD_L + PW + 0.15], [cy, cy],
            color=rgba(CHARCOAL, 0.18), linewidth=0.5, zorder=2,
            solid_capstyle='round')

    # Wave color families -- grouped so adjacent waves share hue families
    # This creates visual coherence rather than random noise
    color_groups = [
        # Group 1: cool teals and greens (left side tendency)
        [TEAL, SAGE, DARK_GREEN, MOSS],
        # Group 2: neutral greys and slates (throughout)
        [SLATE, DEEP_GREY, MIST, DUSK],
        # Group 3: cool darks (right side tendency)
        [CHARCOAL, IRON, DEEP_GREY, SLATE],
    ]

    n_waves = 42

    # Pre-generate all wave data so we can composite them
    # Each wave: frequency, amplitude, phase, color, alpha, x_offset
    wave_data = []
    for i in range(n_waves):
        frac = i / (n_waves - 1)

        # Frequency: mix of low and high, biased toward variety
        freq = np.random.choice([
            np.random.uniform(2.5, 6.0),    # low frequency (broad gestures)
            np.random.uniform(6.0, 16.0),   # mid frequency
            np.random.uniform(16.0, 38.0),  # high frequency (texture)
        ], p=[0.25, 0.45, 0.30])

        # Amplitude: varied, with some very small and some moderate
        amplitude = PH * np.random.uniform(0.04, 0.32)

        # Phase: random
        phase = np.random.uniform(0, 2 * np.pi)

        # Slight x-offset so waves don't all start at exactly the same place
        x_shift = np.random.uniform(-0.08, 0.08)

        # Color: pick from grouped families with spatial bias
        group_idx = int(frac * 2.99)
        group_idx = min(group_idx, 2)
        col = np.random.choice(color_groups[group_idx])

        # Alpha and line weight: varied for depth
        alpha = np.random.uniform(0.15, 0.45)
        lw = np.random.uniform(0.4, 1.1)

        # Frequency modulation for organic variety
        fm_freq = np.random.uniform(0.3, 2.5)
        fm_depth = np.random.uniform(0, 0.25)

        wave_data.append({
            'freq': freq, 'amplitude': amplitude, 'phase': phase,
            'x_shift': x_shift, 'col': col, 'alpha': alpha, 'lw': lw,
            'fm_freq': fm_freq, 'fm_depth': fm_depth,
        })

    # --- Draw crowd waves as vertical amplitude bars ---
    for wi, wd in enumerate(wave_data):
        t_shifted = t_positions + wd['x_shift']

        # Base wave
        wave = np.sin(2 * np.pi * wd['freq'] * t_shifted + wd['phase'])
        # Add frequency modulation
        wave += wd['fm_depth'] * np.sin(
            2 * np.pi * wd['fm_freq'] * t_shifted + wd['phase'] * 0.7)
        # Normalize to [-1, 1] range then scale by amplitude
        wave = wave / (1 + wd['fm_depth'])
        wave = wave * wd['amplitude']

        # Per-wave spatial envelope: each wave has its own extent,
        # some span the full canvas, others are more localized
        env_center = np.random.uniform(0.20, 0.80)
        env_width = np.random.uniform(0.25, 0.65)
        envelope = np.exp(-((t_positions - env_center) / env_width) ** 2)
        # Stronger baseline presence so waves reach the edges
        envelope = np.clip(envelope + np.random.uniform(0.10, 0.30), 0, 1)

        wave = wave * envelope

        # Draw as vertical line segments from center axis
        segments = []
        colors = []
        linewidths = []

        for j in range(n_bars):
            amp_val = wave[j]
            if abs(amp_val) < 0.015:
                continue  # skip near-zero for breathing room

            x = x_positions[j]
            y_top = cy + amp_val
            y_bot = cy  # from center line

            # Dotted/stippled effect: break each vertical bar into
            # small dashes for texture
            bar_height = abs(amp_val)
            if bar_height < 0.05:
                # Very small: single short segment
                segments.append([(x, cy), (x, y_top)])
                local_alpha = wd['alpha'] * envelope[j] * 0.6
                colors.append(rgba(wd['col'], local_alpha))
                linewidths.append(wd['lw'] * 0.6)
            else:
                # Break into dotted segments
                n_dots = max(2, int(bar_height / 0.06))
                dot_spacing = bar_height / (n_dots + 0.5)
                direction = 1.0 if amp_val > 0 else -1.0

                for d in range(n_dots):
                    y_start = cy + direction * d * dot_spacing
                    y_end = cy + direction * (d * dot_spacing + dot_spacing * 0.55)

                    # Fade alpha toward the tip
                    tip_fade = 1.0 - (d / (n_dots + 1)) * 0.4
                    local_alpha = wd['alpha'] * envelope[j] * tip_fade

                    segments.append([(x, y_start), (x, y_end)])
                    colors.append(rgba(wd['col'], local_alpha))
                    linewidths.append(wd['lw'] * tip_fade)

        if len(segments) > 0:
            lc = mc.LineCollection(segments, colors=colors,
                                   linewidths=linewidths,
                                   capstyle='round', zorder=3)
            ax.add_collection(lc)

    # --- Also draw some crowd waves as thin continuous curves ---
    # A few ghostly continuous sine waves at very low alpha for depth
    t_fine = np.linspace(0, 1, 3000)
    xs_fine = PAD_L + PW * t_fine
    for i in range(8):
        freq = np.random.uniform(4, 25)
        amp = PH * np.random.uniform(0.05, 0.22)
        phase = np.random.uniform(0, 2 * np.pi)
        wave = amp * np.sin(2 * np.pi * freq * t_fine + phase)
        env = np.exp(-((t_fine - np.random.uniform(0.3, 0.7)) /
                       np.random.uniform(0.25, 0.45)) ** 2)
        ys = cy + wave * env
        col = np.random.choice([MIST, SLATE, BONE])
        draw_lc(ax, xs_fine, ys, col, lw=np.random.uniform(0.2, 0.5),
                alpha=np.random.uniform(0.06, 0.14), zo=2, smooth=2)

    # === THE SIGNAL: one distinct gold wave, rendered as clean vertical bars ===
    # Positioned slightly right of center (like the curated image)
    signal_center_t = 0.55
    signal_freq = 14.0
    signal_amplitude = PH * 0.42  # taller than any crowd wave
    signal_phase = 0.0

    signal_wave = signal_amplitude * np.sin(
        2 * np.pi * signal_freq * t_positions + signal_phase)

    # Tight envelope: the signal is localized, a piercing moment
    signal_env = np.exp(-((t_positions - signal_center_t) / 0.065) ** 2)
    # Gentle wider aura
    signal_env_wide = np.exp(-((t_positions - signal_center_t) / 0.14) ** 2)
    signal_env = np.maximum(signal_env, signal_env_wide * 0.30)

    signal_wave = signal_wave * signal_env

    # Draw the gold signal as clean vertical bars (no stippling -- solid, clear)
    signal_segments = []
    signal_colors = []
    signal_lws = []

    for j in range(n_bars):
        amp_val = signal_wave[j]
        if abs(amp_val) < 0.02:
            continue

        x = x_positions[j]

        # Draw from center line in both directions for symmetry emphasis
        # The signal is drawn as a single clean vertical stroke
        bar_height = abs(amp_val)
        local_env = signal_env[j]

        # Main signal bar -- extends both above and below center line
        # mirroring downward at reduced scale for visual weight
        y_below = cy - abs(amp_val) * 0.55
        y_above = cy + amp_val
        signal_segments.append([(x, y_below), (x, y_above)])
        alpha_sig = 0.25 + 0.65 * local_env
        lw_sig = 0.6 + 1.6 * local_env
        signal_colors.append(rgba(LONE_GOLD, alpha_sig))
        signal_lws.append(lw_sig)

    if len(signal_segments) > 0:
        lc_sig = mc.LineCollection(signal_segments, colors=signal_colors,
                                   linewidths=signal_lws,
                                   capstyle='round', zorder=6)
        ax.add_collection(lc_sig)

    # Gold harmonic echoes: a few companion waves near the signal
    for harm_i in range(4):
        harm_freq = signal_freq * (1 + (harm_i + 1) * 0.12)
        harm_phase = signal_phase + (harm_i + 1) * 0.5
        harm_amp = signal_amplitude * (0.45 - harm_i * 0.08)
        harm_wave = harm_amp * np.sin(
            2 * np.pi * harm_freq * t_positions + harm_phase)
        harm_env = np.exp(-((t_positions - signal_center_t) /
                            (0.08 + harm_i * 0.025)) ** 2)
        harm_wave = harm_wave * harm_env

        harm_segments = []
        harm_colors = []
        harm_lws = []

        for j in range(n_bars):
            amp_val = harm_wave[j]
            if abs(amp_val) < 0.025:
                continue
            x = x_positions[j]
            local_env = harm_env[j]
            harm_segments.append([(x, cy), (x, cy + amp_val)])
            alpha_h = 0.12 + 0.35 * local_env
            lw_h = 0.4 + 0.9 * local_env
            harm_colors.append(rgba(WARM_ACCENT, alpha_h))
            harm_lws.append(lw_h)

        if len(harm_segments) > 0:
            lc_h = mc.LineCollection(harm_segments, colors=harm_colors,
                                     linewidths=harm_lws,
                                     capstyle='round', zorder=5)
            ax.add_collection(lc_h)

    # Warm glow: a soft continuous gold wave behind the signal for luminosity
    for spread, glow_alpha in [(1.2, 0.12), (2.0, 0.06), (3.5, 0.03)]:
        glow_env = np.exp(-((t_fine - signal_center_t) /
                            (0.065 * spread)) ** 2)
        ys_glow = cy + signal_amplitude * np.sin(
            2 * np.pi * signal_freq * t_fine + signal_phase) * glow_env * 0.7
        draw_lc(ax, xs_fine, ys_glow, WARM_ACCENT,
                lw=0.4, alpha=glow_alpha, zo=4, smooth=3)

    label(ax, "S(f)=A\u00b7\u03b4(f\u2212f\u2080)+\u03b7")
    save(fig, "solitude_signal")


if __name__ == '__main__':
    render()
