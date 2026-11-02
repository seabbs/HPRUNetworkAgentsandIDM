#!/usr/bin/env -S uv run --with matplotlib --script
"""Schematic of two ways to spend the time agents free up.

Shares its style with scripts/agents-tool-llm.py and scripts/agents-multi.py.

Usage:
    ./scripts/agents-time.py

Writes figures/agents-time.png.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.path import Path as MPath

out = Path(__file__).resolve().parent.parent / "figures" / "agents-time.png"

teal, slate = "#1f6f8b", "#4a5899"
ink, muted, light, grey = "#333333", "#6b7280", "#e8f1f5", "#f3f4f6"
plt.rcParams.update({"font.size": 15, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(11, 5.6), dpi=200)
fig.subplots_adjust(0, 0, 1, 1)
ax.set_xlim(0, 110)
ax.set_ylim(0, 56)
ax.set_aspect("equal")
ax.axis("off")


def box(x0, y0, x1, y1, edge, fill="white", lw=2, ls="-"):
    ax.add_patch(FancyBboxPatch(
        (x0, y0), x1 - x0, y1 - y0,
        boxstyle="round,pad=0,rounding_size=1.6",
        facecolor=fill, edgecolor=edge, linewidth=lw, linestyle=ls,
    ))


def text(x, y, s, color=ink, **kw):
    ax.text(x, y, s, color=color, ha="center", va="center",
            linespacing=1.25, **kw)


def arrow(path, color, lw):
    ax.add_patch(FancyArrowPatch(
        path=path, arrowstyle="-|>", mutation_scale=lw * 6, color=color,
        linewidth=lw,
    ))


def line_path(*points):
    return MPath(points)


# The source: time agents free up.
sx0, sx1, sy0, sy1 = 0.8, 21.2, 39.5, 53.5
box(sx0, sy0, sx1, sy1, teal, teal)
text((sx0 + sx1) / 2, (sy0 + sy1) / 2, "Time agents\nfree up", "white",
     fontsize=17, fontweight="bold")

# Path 1, the default: more of the same, faster.
gx0, gx1, gy0, gy1 = 50, 109.5, 40.5, 52.5
gyc = (gy0 + gy1) / 2
arrow(line_path((sx1, gyc), (gx0, gyc)), muted, 7)
text((sx1 + gx0) / 2, gyc + 3.4, "what we could do", muted)
box(gx0, gy0, gx1, gy1, muted, grey)
text((gx0 + gx1) / 2, gyc, "More of the same, faster", ink)

# Path 2, the choice: work agents make room for.
fx0, fx1, fy0, fy1 = 25, 109.5, 1.2, 36
box(fx0, fy0, fx1, fy1, slate, "#eef0f7")
choices = [
    "Review", "Deep dives", "Big-picture\nthinking",
    "Reducing\ntechnical debt", "Making work\ngeneral and\ninteroperable",
    "Evaluating\nwhat works", "Collaboration", "Talking to\nstakeholders",
]
cols = 4
gap = 1.6
bw = (fx1 - fx0 - (cols + 1) * gap) / cols
bh = (fy1 - fy0 - 3 * gap) / 2
for i, label in enumerate(choices):
    row, col = divmod(i, cols)
    x0 = fx0 + gap + col * (bw + gap)
    y1 = fy1 - gap - row * (bh + gap)
    box(x0, y1 - bh, x0 + bw, y1, teal, light)
    text(x0 + bw / 2, y1 - bh / 2, label, teal, fontweight="bold")
px = (sx0 + sx1) / 2
py = (fy0 + fy1) / 2
arrow(line_path((px, sy0), (px, py), (fx0, py)), slate, 4)
ax.text(px + 1.6, 28, "what we\nshould do", color=slate, va="center")

fig.savefig(out, facecolor="white")
print(out)
