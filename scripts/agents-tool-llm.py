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


# The harness, e.g. Claude Code, sits between the model and the tools.
hx0, hx1, hy0, hy1 = 27, 69, 1, 61.5
box(hx0, hy0, hx1, hy1, slate, "#eef0f7")
ax.text(hx0 + 2, hy1 - 3.4, "Harness", color=slate, fontweight="bold",
        va="center")
ax.text(hx0 + 13, hy1 - 3.4, "e.g. Claude Code", color=muted,
        va="center")

# It assembles the context window: everything the model sees.
cx0, cx1, cy0, cy1 = hx0 + 2, hx1 - 2, 27.5, 54
box(cx0, cy0, cx1, cy1, teal, light)
ax.text(cx0 + 1.8, cy1 - 3, "Context window", color=teal,
        fontweight="bold", va="center")
cw = (cx1 - cx0 - 4.5) / 2
c1, c2 = cx0 + 1.5, cx0 + 3 + cw
chips = [
    (c1, 38.5, 48, "Instructions\nCLAUDE.md", {}),
    (c2, 38.5, 48, "Skills, e.g.\nJulia package\ndevelopment", {}),
    (c1, 29.5, 37, "Conversation", {}),
    (c2, 29.5, 37, "Tool results", {}),
]
for x0, y0, y1, label, kw in chips:
    box(x0, y0, x0 + cw, y1, teal, "white", lw=1.5)
    text(x0 + cw / 2, (y0 + y1) / 2, label, **kw)

# It runs the tool calls the model writes.
rx0, rx1, ry0, ry1 = hx0 + 2, hx1 - 2, 3.5, 16.5
box(rx0, ry0, rx1, ry1, teal, "white")
text((rx0 + rx1) / 2, 12.2, "Runs tool calls", teal, fontweight="bold")
text((rx0 + rx1) / 2, 7.8, "connects MCP servers", muted)

# The language model only writes text or tool calls.
mx0, mx1, my0, my1 = 1, 16, 7, 40
box(mx0, my0, mx1, my1, teal, teal)
text((mx0 + mx1) / 2, 30, "Language\nmodel", "white", fontsize=17,
     fontweight="bold")
text((mx0 + mx1) / 2, 18, "writes\ntext or\ntool calls", "white")

# Tools, with extra ones plugged in by MCP servers.
tx0, tx1, ty0, ty1 = 77.5, 99.5, 3.5, 40.5
box(tx0, ty0, tx1, ty1, teal, "white")
tc = (tx0 + tx1) / 2
text(tc, ty1 - 3.2, "Tools", teal, fontweight="bold")
text(tc, 28.4, "Shell\nRead and edit files\nGitHub\nWeb search")
box(tx0 + 1.5, 5.5, tx1 - 1.5, 17.5, slate, "white", lw=1.5,
    ls=(0, (4, 2)))
text(tc, 14.4, "MCP servers", slate, fontweight="bold")
text(tc, 9.2, "Julia session\nGoogle Drive")

# The agent loop: context in, tool call out, run, result back in.
loop_lw = 4
arrow((cx0, 36), (mx1, 36), teal, loop_lw)
text((mx1 + hx0) / 2, 38.4, "context", teal)
arrow((mx1, 11), (rx0, 11), teal, loop_lw)
text((mx1 + hx0) / 2, 13.4, "tool call", teal)
arrow((rx1, 10), (tx0, 10), teal, loop_lw)
text((hx1 + tx0) / 2, 12.6, "runs", teal)
arrow((tx0, 33.25), (c2 + cw, 33.25), teal, loop_lw)
text((hx1 + tx0) / 2, 36, "result", teal)
lx = (cx0 + cx1) / 2
text(lx - 11, 22.4, "\u21ba", teal, fontsize=30)
text(lx + 2.5, 22, "repeat until done", teal, fontweight="bold")

# The person gives the prompt and reads the answer.
box(1, 49, 16, 60, brick, brick)
text(8.5, 54.5, "You", "white", fontsize=17, fontweight="bold")
arrow((16, 54.5), (hx0, 54.5), brick)
text((16 + hx0) / 2, 56.8, "prompt", brick)
arrow((8.5, my1), (8.5, 49), brick)
ax.text(9.6, 44.5, "answer", color=brick, va="center")

fig.savefig(out, facecolor="white")
print(out)
