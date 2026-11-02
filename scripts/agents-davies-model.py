#!/usr/bin/env -S uv run --with matplotlib --script
"""Redraw of the model diagram in Davies et al. 2020 (Fig. 1).

The published figure is low resolution, so this redraws its structure in
the talk's house style.

Usage:
    ./scripts/agents-davies-model.py

Writes figures/agents-davies2020-model-redrawn.png.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.path import Path as MPath

out = (
    Path(__file__).resolve().parent.parent / "figures"
    / "agents-davies2020-model-redrawn.png"
)

teal, slate = "#1f6f8b", "#4a5899"
ink, band_full, band_half = "#333333", "#c4dbe5", "#e8f1f5"
plt.rcParams.update({
    "font.size": 15, "font.family": "DejaVu Sans",
    "mathtext.fontset": "dejavusans",
})
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
fig.subplots_adjust(0, 0, 1, 1)
ax.set_xlim(0, 100)
ax.set_ylim(0, 42)
ax.set_aspect("equal")
ax.axis("off")


def box(x0, y0, x1, y1, label, edge=ink, fill="white"):
    ax.add_patch(FancyBboxPatch(
        (x0, y0), x1 - x0, y1 - y0,
        boxstyle="round,pad=0,rounding_size=1",
        facecolor=fill, edgecolor=edge, linewidth=1.8,
    ))
    text((x0 + x1) / 2, (y0 + y1) / 2, label)


def text(x, y, s, color=ink, **kw):
    kw.setdefault("ha", "center")
    ax.text(x, y, s, color=color, va="center", linespacing=1.3, **kw)


def path_arrow(*points, head=True):
    ax.add_patch(FancyArrowPatch(
        path=MPath(points), arrowstyle="-|>" if head else "-",
        mutation_scale=18, color=ink, linewidth=1.8,
        joinstyle="miter",
    ))


# Infectious bands: fully infectious (top) and half infectious (bottom).
bx0, bx1 = 43, 79
ax.add_patch(Rectangle((bx0, 24), bx1 - bx0, 17.6, color=band_full, lw=0))
ax.add_patch(Rectangle((bx0, 0.4), bx1 - bx0, 16.6, color=band_half, lw=0))
text(bx0 + 1.2, 39.6, "100% infectious", teal, ha="left", fontweight="bold")
text(bx0 + 1.2, 2.8, "50% infectious", slate, ha="left", fontweight="bold")
text((bx0 + bx1) / 2, 20.5, "Infectious stage")

# Compartments.
mid, top, bot = 21, 33, 11
box(0.5, 17, 15.5, 25, "Susceptible\n$S$")
box(23, 17, 35, 25, "Exposed\n$E$")
box(45.5, 29, 60, 37, r"Preclinical" "\n" r"$I_\mathrm{P}$")
box(66, 29, 77.5, 37, r"Clinical" "\n" r"$I_\mathrm{C}$")
box(53.5, 7, 68.5, 15, r"Subclinical" "\n" r"$I_\mathrm{S}$")
box(86, 17, 99.5, 25, "Removed\n$R$")

# Flows.
split, merge = 40, 82
path_arrow((15.5, mid), (23, mid))
text(19.25, 12.6, "Successful\ninfection")
path_arrow((35, mid), (split, mid), head=False)
path_arrow((split, mid), (split, top), (45.5, top))
path_arrow((split, mid), (split, bot), (53.5, bot))
text(split - 1, 29.4, "Latent\nperiod", ha="right")
text(split - 1, 12.6, "Latent\nperiod", ha="right")
path_arrow((60, top), (66, top))
text(63, 26.6, "Case onset")
path_arrow((77.5, top), (merge, top), (merge, mid), head=False)
path_arrow((68.5, bot), (merge, bot), (merge, mid), head=False)
path_arrow((merge, mid), (86, mid))
text(91, 33, "Recovery,\nisolation")
text(91, 11, "Recovery")

fig.savefig(out, facecolor="white")
print(out)
