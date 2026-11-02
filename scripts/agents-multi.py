#!/usr/bin/env -S uv run --with matplotlib --script
"""Schematic of agents working in concert: subagents and a workflow script.

Pairs with scripts/agents-tool-llm.py, so it shares its size and style.

Usage:
    ./scripts/agents-multi.py

Writes figures/agents-multi.png.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

out = Path(__file__).resolve().parent.parent / "figures" / "agents-multi.png"

teal, slate = "#1f6f8b", "#4a5899"
ink, muted, light = "#333333", "#6b7280", "#e8f1f5"
plt.rcParams.update({"font.size": 15, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
fig.subplots_adjust(0, 0, 1, 1)
ax.set_xlim(0, 100)
ax.set_ylim(0, 62)
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


def arrow(a, b, color=ink, lw=2):
    ax.add_patch(FancyArrowPatch(
        a, b, arrowstyle="-|>", mutation_scale=22, color=color,
        linewidth=lw, shrinkA=0, shrinkB=0,
    ))


# Left: a lead agent hands tasks to subagents, which run in parallel.
lx0, lx1, ly0, ly1 = 1, 11.5, 7, 55
box(lx0, ly0, lx1, ly1, teal, teal)
text((lx0 + lx1) / 2, (ly0 + ly1) / 2, "Lead\nagent", "white",
     fontsize=17, fontweight="bold")

sx0, sx1 = 24, 49.5
ax.text(lx0, 58.4, "Subagents", color=teal, fontweight="bold",
        va="center")
ax.text(lx0 + 13.5, 58.4, "in parallel, fresh contexts", color=muted,
        va="center")
for i, role in enumerate(["Implement", "Test", "Review"]):
    y1 = 55 - i * 16
    y0 = y1 - 13
    box(sx0, y0, sx1, y1, teal, light)
    text((sx0 + sx1) / 2, y1 - 3.3, role, teal, fontweight="bold")
    cw = (sx1 - sx0 - 4.5) / 2
    box(sx0 + 1.5, y0 + 1.5, sx0 + 1.5 + cw, y0 + 6.8, teal, "white",
        lw=1.5)
    text(sx0 + 1.5 + cw / 2, y0 + 4.15, "context")
    box(sx1 - 1.5 - cw, y0 + 1.5, sx1 - 1.5, y0 + 6.8, teal, "white",
        lw=1.5)
    text(sx1 - 1.5 - cw / 2, y0 + 4.15, "tools")
    arrow((lx1, y1 - 3.5), (sx0, y1 - 3.5), teal)
    arrow((sx0, y0 + 3.5), (lx1, y0 + 3.5), teal, 4)
text((lx1 + sx0) / 2, 53.6, "task", teal)
text((lx1 + sx0) / 2, 42.9, "summary", teal)

# Right: a workflow script runs the same fan-out, verify, merge each time.
wx0, wx1, wy0, wy1 = 53, 99.5, 1, 61.5
box(wx0, wy0, wx1, wy1, slate, "#eef0f7")
ax.text(wx0 + 2, wy1 - 3.4, "Workflow", color=slate, fontweight="bold",
        va="center")
ax.text(wx0 + 2, wy1 - 7.2, "e.g. a Claude Code workflow script",
        color=muted, va="center")

gap = 1.8
bw = (wx1 - wx0 - 4 - 2 * gap) / 3
merge_y1 = 12
for i, dim in enumerate(["bugs", "tests", "docs"]):
    x0 = wx0 + 2 + i * (bw + gap)
    xc = x0 + bw / 2
    box(x0, 37, x0 + bw, 49, teal, light)
    text(xc, 43, f"Review\n{dim}", teal)
    box(x0, 20, x0 + bw, 28, teal, light)
    text(xc, 24, "Verify", teal)
    arrow((xc, 37), (xc, 28), slate)
    arrow((xc, 20), (xc, merge_y1), slate)
box(wx0 + 2, 4, wx1 - 2, merge_y1, slate, "white")
text((wx0 + wx1) / 2, 8, "Merge results", slate, fontweight="bold")

fig.savefig(out, facecolor="white")
print(out)
