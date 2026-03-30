"""
Geometry of Feeling — Confusion: Confusion Aliased
Standalone render script
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

# Palette: muddled, uncertain — no color dominates
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
def split_segments(xs, ys, mask):
    segments = []
    in_seg = False
    start = 0
    for j in range(len(mask)):
        if mask[j] and not in_seg:
            start = j
            in_seg = True
        elif not mask[j] and in_seg:
            if j - start >= 3:
                segments.append((xs[start:j], ys[start:j]))
            in_seg = False
    if in_seg and len(mask) - start >= 3:
        segments.append((xs[start:], ys[start:]))
    return segments

def draw_lc(ax,xs,ys,col,lw,alpha,zo=4,smooth=0):
    if smooth>0:
        ys=gaussian_filter1d(ys,smooth)
    pts=np.array([xs,ys]).T.reshape(-1,1,2)
    segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
    lc=mc.LineCollection(segs,linewidths=lw,colors=[rgba(col,alpha)],
                         capstyle='round',joinstyle='round',zorder=zo)
    ax.add_collection(lc)

def draw_lc_gradient(ax,xs,ys,col,lw_start,lw_end,a_start,a_end,zo=4,smooth=0):
    if smooth>0:
        ys=gaussian_filter1d(ys,smooth)
    pts=np.array([xs,ys]).T.reshape(-1,1,2)
    segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
    n=len(segs)
    alphas=np.linspace(a_start,a_end,n)
    lws=np.linspace(lw_start,lw_end,n)
    colors=[rgba(col,float(a)) for a in alphas]
    lc=mc.LineCollection(segs,linewidths=lws,colors=colors,
                         capstyle='round',joinstyle='round',zorder=zo)
    ax.add_collection(lc)

def save(fig,name):
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
    fig.savefig(os.path.join(OUTPUT_DIR,name),
                format='pdf',facecolor=BG)
    plt.close(fig); print(f"saved {name}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')


def render():
    fig,ax=make_fig()
    np.random.seed(77)
    t_fine=np.linspace(0,1,8000)  # the "true" signal
    xs_fine=PAD_L+PW*t_fine

    # Multiple high-frequency sine systems
    n_systems=16
    for s in range(n_systems):
        frac=s/(n_systems-1)
        y_base=PAD_B+PH*(0.06+frac*0.85)

        # TRUE signal: very high frequency
        true_freq=40+s*8  # high frequency
        amp=PH*0.025*(0.6+frac*0.4)
        true_signal=amp*np.sin(true_freq*np.pi*t_fine+s*1.3)

        # Draw the true signal very faintly (what's actually there)
        ys_true=y_base+true_signal
        cols=[MURK,TANGLE_COL,FOG,UNCERTAIN,CROSSED,KNOT_COL,
              HAZE,DRIFT,STATIC,MAUVE,SAGE,CLAY,
              MURK,TANGLE_COL,FOG,UNCERTAIN]
        col_true=cols[s%len(cols)]
        draw_lc(ax,xs_fine,ys_true,col_true,lw=0.15,alpha=0.06,zo=2,smooth=0)

        # ALIASED signal: sample at much lower rate, creating phantom frequency
        for alias_pass in range(3):
            # different sample rates create different phantom patterns
            n_samples=int(80+alias_pass*25+s*5)
            t_sampled=np.linspace(0,1,n_samples)
            xs_sampled=PAD_L+PW*t_sampled
            # sample the high-frequency signal at low rate
            sampled_values=amp*np.sin(true_freq*np.pi*t_sampled+s*1.3)
            ys_sampled=y_base+sampled_values

            # interpolate back to smooth curve — this shows the phantom
            from scipy.interpolate import CubicSpline
            if len(t_sampled)>3:
                cs=CubicSpline(t_sampled,ys_sampled)
                t_interp=np.linspace(0,1,2000)
                xs_interp=PAD_L+PW*t_interp
                ys_interp=cs(t_interp)
                ys_interp=np.clip(ys_interp,PAD_B,PAD_B+PH)

                col_alias=cols[(s+alias_pass+4)%len(cols)]
                alpha=0.08+0.22*(1-abs(frac-0.5)*1.3)
                lw=0.3+0.65*(1-abs(frac-0.5))
                draw_lc(ax,xs_interp,ys_interp,col_alias,
                        lw=lw,alpha=alpha,zo=3+alias_pass,smooth=3)

    # faint Moire-like overlay: two dense line grids at slightly different angles
    for g in range(2):
        angle=0.02+g*0.04  # very slight angles
        n_lines=35
        for i in range(n_lines):
            gfrac=i/(n_lines-1)
            y_g=PAD_B+PH*(0.02+gfrac*0.96)
            t_g=np.linspace(0,1,500)
            xs_g=PAD_L+PW*t_g
            ys_g=y_g+PH*0.008*np.sin(angle*80*np.pi*t_g+g*1.5)
            draw_lc(ax,xs_g,ys_g,FOG if g==0 else STATIC,
                    lw=0.15,alpha=0.03,zo=6,smooth=0)

    label(ax,"f_alias=sin(2\u03c0(f\u2212nf_s)t),  f_s<2f")
    save(fig,"confusion_aliased.pdf")


if __name__ == '__main__':
    render()
