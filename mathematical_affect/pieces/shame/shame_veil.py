"""
Geometry of Feeling — Shame: Shame Veil
Standalone render script
"""

"""
Geometry of Feeling — Shame (Final Series)
Five pieces: Shrink, Contraction, Fold, Crumple, Veil

Mathematical primitives: logarithmic spirals collapsing inward,
contraction mappings, lemniscate self-intersections,
progressive frequency crumpling, semi-transparent layered obscuration

Background: #3A3430 (warm dim — curtains drawn)
Palette: muddy brown, dark grey, washed-out burgundy

Dependencies: matplotlib, numpy, scipy
    pip install matplotlib numpy scipy
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.ndimage import gaussian_filter1d
import os


DPI=300; FIG_W=12; FIG_H=8
BG="#3A3430"

# Palette: muddy brown, dark grey, washed-out burgundy
UMBER="#5A4A38"; SHADOW="#3A3028"; FLUSH="#8A4A40"
HIDE="#4A4038"; SMOKE="#6A6058"; EMBER="#7A5030"
COPPER="#8A6A48"; DUST="#6A5A48"; VEIL_COL="#5A5048"
BURGUNDY="#6A3838"; MUDDY="#5A5040"; ASHEN="#4A4A44"

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
            color=(0.85,0.78,0.68,0.40),transform=ax.transData)
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


# ===============================================================================
# 5. VEIL — multiple translucent layers obscuring what's behind them
#    overlapping semi-transparent curves creating a murky, hidden feeling
#    like gauze layered over gauze — depth without clarity
# ===============================================================================
def render():
    fig,ax=make_fig()
    np.random.seed(21)
    t=np.linspace(0,1,2000); xs=PAD_L+PW*t

    # LAYER 1: the hidden thing — a few clear, warm curves buried beneath
    for i in range(6):
        y_base=cy+PH*(np.random.uniform(-0.15,0.15))
        freq=2+i*0.8
        amp=PH*0.04
        ys=y_base+amp*np.sin(freq*np.pi*t+i*0.9)
        draw_lc(ax,xs,ys,FLUSH,lw=1.12,alpha=0.17,zo=2,smooth=3)

    # LAYER 2: the veiling — many translucent curves in progressively
    # darker/murkier tones, each one hiding a little more
    n_layers=65
    for i in range(n_layers):
        frac=i/(n_layers-1)
        # each layer has slightly different vertical positioning
        # concentrated in center to maximize obscuration
        y_center=PAD_B+PH*(0.15+0.70*np.random.random())
        # distance from absolute center affects density
        dist_from_center=abs(y_center-cy)/PH
        density=np.exp(-(dist_from_center**2)/(2*0.25**2))

        # gentle undulating curves
        freq=0.8+np.random.random()*4
        amp=PH*(0.008+0.025*np.random.random())
        phase=np.random.random()*2*np.pi

        # each veil layer has a slightly different vertical drift
        drift=PH*0.01*np.sin(1.5*np.pi*t+np.random.random()*3)
        ys=y_center+amp*np.sin(freq*np.pi*t+phase)+drift
        ys=np.clip(ys,PAD_B+PH*0.02,PAD_B+PH*0.98)

        # veil colors — progressively darker, murkier
        cols=[VEIL_COL,HIDE,SHADOW,DUST,SMOKE,UMBER,ASHEN,MUDDY]
        col=cols[i%len(cols)]
        # alpha: very low individually, but accumulates
        alpha=0.05+0.17*density+0.07*np.random.random()
        lw=0.35+0.77*density+0.42*np.random.random()
        draw_lc(ax,xs,ys,col,lw=lw,alpha=alpha,zo=3+int(frac*3),smooth=6)

    # LAYER 3: faint horizontal bands — like fabric grain
    for i in range(12):
        y_pos=PAD_B+PH*(0.10+0.80*i/11)
        ys_band=np.full_like(t,y_pos)+PH*0.002*np.sin(20*np.pi*t+i)
        draw_lc(ax,xs,ys_band,SHADOW,lw=0.28,alpha=0.07,zo=5,smooth=0)

    label(ax,"\u03a3\u03b1_k\u00b7sin(\u03c9_k t+\u03c6_k),  \u03b1_k\u22480")
    save(fig,"shame_veil.pdf")


if __name__ == '__main__':
    render()
