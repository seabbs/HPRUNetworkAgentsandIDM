#!/usr/bin/env -S uv run --with matplotlib --script
"""Schematic of a tool-using language model (a coding agent).

Usage:
    ./scripts/agents-tool-llm.py

Writes figures/agents-tool-llm.png.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

out = Path(__file__).resolve().parent.parent / "figures" / "agents-tool-llm.png"

teal, slate, brick = "#1f6f8b", "#4a5899", "#b5432f"
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


def arrow(a, b, color=ink, lw=2, rad=0.0):
    ax.add_patch(FancyArrowPatch(
        a, b, arrowstyle="-|>", mutation_scale=22, color=color,
        linewidth=lw, connectionstyle=f"arc3,rad={rad}",
        shrinkA=0, shrinkB=0,
    ))


# Where the harness and tools run sets data access, tools and compute.
bx0, bx1, by0, by1 = 22.5, 99.7, 0.3, 61.7
box(bx0, by0, bx1, by1, muted, "#f6f6f7", lw=1.5, ls=(0, (5, 3)))

# The harness, e.g. Claude Code, sits between the model and the tools.
hx0, hx1, hy0, hy1 = 25, 67.5, 2, 60
box(hx0, hy0, hx1, hy1, slate, "#eef0f7")
ax.text(hx0 + 2, hy1 - 3.2, "Harness", color=slate, fontweight="bold",
        va="center")
ax.text(hx0 + 13, hy1 - 3.2, "e.g. Claude Code", color=muted,
        va="center")

# It assembles the context window: everything the model sees.
cx0, cx1, cy0, cy1 = hx0 + 2, hx1 - 2, 27.5, 53.5
box(cx0, cy0, cx1, cy1, teal, light)
ax.text(cx0 + 1.8, cy1 - 3, "Context window", color=teal,
        fontweight="bold", va="center")
cw = (cx1 - cx0 - 4.5) / 2
c1, c2 = cx0 + 1.5, cx0 + 3 + cw
chips = [
    (c1, 38.5, 47.5, "Instructions\nAGENTS.md"),
    (c2, 38.5, 47.5, "Skills, e.g.\nJulia package\ndevelopment"),
    (c1, 29.5, 37, "Conversation"),
    (c2, 29.5, 37, "Tool results"),
]
for x0, y0, y1, label in chips:
    box(x0, y0, x0 + cw, y1, teal, "white", lw=1.5)
    text(x0 + cw / 2, (y0 + y1) / 2, label)

# It runs the tool calls the model writes.
rx0, rx1, ry0, ry1 = hx0 + 2, hx1 - 2, 4, 16.5
box(rx0, ry0, rx1, ry1, teal, "white")
text((rx0 + rx1) / 2, 12.4, "Runs tool calls", teal, fontweight="bold")
text((rx0 + rx1) / 2, 8, "connects MCP servers", muted)

# The language model only writes text or tool calls. It usually runs at
# a provider, outside the box where the harness runs.
mx0, mx1, my0, my1 = 1, 14.5, 9, 40
box(mx0, my0, mx1, my1, teal, teal)
text((mx0 + mx1) / 2, 31, "Language\nmodel", "white", fontsize=16,
     fontweight="bold")
text((mx0 + mx1) / 2, 19.5, "writes\ntext or\ntool calls", "white")
text((mx0 + mx1) / 2, 4.6, "at a provider,\nor local", muted)

# Tools, with extra ones plugged in by MCP servers.
tx0, tx1, ty0, ty1 = 76, 98.2, 4, 38
box(tx0, ty0, tx1, ty1, teal, "white")
tc = (tx0 + tx1) / 2
text(tc, ty1 - 3.2, "Tools", teal, fontweight="bold")
text(tc, 26.6, "Shell\nRead and edit files\nGitHub\nWeb search")
box(tx0 + 1.5, 6, tx1 - 1.5, 17.5, slate, "white", lw=1.5,
    ls=(0, (4, 2)))
text(tc, 14.4, "MCP servers", slate, fontweight="bold")
text(tc, 9.4, "Julia session\nGoogle Drive")

# Where it runs, in the space above the tools.
wx = (hx1 + bx1) / 2 + 0.5
text(wx, 57.2, "Where it runs", ink, fontweight="bold")
text(wx, 50.4, "your computer\nthe cloud\nan HPC cluster")
text(wx, 42.6, "sets data access,\ntools and compute", muted)

# The agent loop: context in, tool call out, run, result back in.
loop_lw = 4
arrow((cx0, 36), (mx1, 36), teal, loop_lw)
arrow((mx1, 11.5), (rx0, 11.5), teal, loop_lw)
arrow((rx1, 10.5), (tx0, 10.5), teal, loop_lw)
text((hx1 + tx0) / 2, 13.1, "runs", teal)
arrow((tx0, 33.25), (c2 + cw, 33.25), teal, loop_lw)
text((hx1 + tx0) / 2, 35.8, "result", teal)
lx = (cx0 + cx1) / 2
text(lx - 11, 22.4, "\u21ba", teal, fontsize=30)
text(lx + 2.5, 22, "repeat until done", teal, fontweight="bold")

# The person gives the prompt and reads the answer.
box(1, 49, 12, 60, brick, brick)
text(6.5, 54.5, "You", "white", fontsize=17, fontweight="bold")
arrow((12, 54.5), (hx0, 54.5), brick)
text((12 + bx0) / 2, 56.8, "prompt", brick)
arrow((6.5, my1), (6.5, 49), brick)
ax.text(7.7, 44.5, "answer", color=brick, va="center")

fig.savefig(out, facecolor="white")
print(out)
