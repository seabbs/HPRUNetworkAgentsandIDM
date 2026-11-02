#!/usr/bin/env -S uv run --with matplotlib --with pillow --script
"""The agent loop with review agents and new tasks, for the Implementing slide.

Usage:
    ./scripts/agents-loop.py

Adapted from AIandIDVUB scripts/keynote-schematics.py (agent_2), with the
secondary labels removed. Writes figures/agents-agent-2.png.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from PIL import Image, ImageDraw
TEAL = "#1f6f8b"
SLATE = "#4a5899"
BRICK = "#b5432f"
INK = "#2b2b2b"
GREY = "#8a8f98"
LIGHT = "#e4e6ea"
PALE_TEAL = "#e3eef2"
PALE_SLATE = "#e6e8f2"
PALE_BRICK = "#f5e6e3"
PALE = {TEAL: PALE_TEAL, SLATE: PALE_SLATE, BRICK: PALE_BRICK, GREY: "white",
        INK: "white"}

plt.rcParams.update(
    {
        "font.size": 15,
        "font.family": "sans-serif",
        "figure.dpi": 160,
        "text.color": INK,
    }
)


def canvas(w=10, h=5.2, xlim=None, ylim=None):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*(xlim or (0, w)))
    ax.set_ylim(*(ylim or (0, h)))
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, colour=TEAL, fill=None, fs=14, lw=2,
        weight="normal", text_colour=None, ls="-", spacing=1.15):
    patch = FancyBboxPatch((x, y), w, h,
                           boxstyle="round,pad=0.02,rounding_size=0.12",
                           edgecolor=colour, facecolor=fill or PALE[colour],
                           linewidth=lw, zorder=2, linestyle=ls)
    ax.add_patch(patch)
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs, color=text_colour or colour, fontweight=weight,
                zorder=3, linespacing=spacing)


def arrow(ax, p, q, colour=GREY, lw=2, style="-|>", rad=0.0, ls="-",
          scale=18):
    a = FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=scale,
                        color=colour, linewidth=lw, zorder=1,
                        connectionstyle=f"arc3,rad={rad}", linestyle=ls)
    ax.add_patch(a)


def label(ax, x, y, text, colour=GREY, fs=12, ha="center", va="center",
          style="normal", weight="normal", rotation=0):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fs, color=colour,
            style=style, fontweight=weight, linespacing=1.15, zorder=3,
            rotation=rotation)



def save(fig, name):
    fig.savefig(f"figures/{name}", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print("wrote figures/" + name)


def inner_loop(ax, cx, cy, r=1.35, fs=10.5):
    nodes = [("Read the files\nand the docs", 90), ("Write or\nchange code", 0),
             ("Run it.\nTests, render", -90), ("Check passed?", 180)]
    for text, deg in nodes:
        t = np.deg2rad(deg)
        x, y = cx + r * np.cos(t), cy + r * np.sin(t)
        colour = TEAL if deg == 180 else SLATE
        box(ax, x - 0.8, y - 0.36, 1.6, 0.72, text, colour=colour, fs=fs)
    arcs = [((cx + 0.5, cy + r - 0.36), (cx + r - 0.2, cy + 0.36)),
            ((cx + r - 0.2, cy - 0.36), (cx + 0.5, cy - r + 0.36)),
            ((cx - 0.5, cy - r + 0.36), (cx - r + 0.2, cy - 0.36)),
            ((cx - r + 0.2, cy + 0.36), (cx - 0.5, cy + r - 0.36))]
    for p, q in arcs:
        arrow(ax, p, q, colour=SLATE, lw=1.8, rad=-0.35)


def avatar(ax, path, x, y, size=0.8):
    """Draw a round avatar centred on (x, y), size in data units."""
    im = Image.open(path).convert("RGBA").resize((240, 240))
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 239, 239), fill=255)
    im.putalpha(mask)
    ax.imshow(np.asarray(im), extent=(x - size / 2, x + size / 2,
                                      y - size / 2, y + size / 2),
              zorder=5, aspect="auto")


def agent_loop():
    fig, ax = canvas(11, 6.2)
    # Where tasks come from.
    box(ax, 0.1, 4.7, 2.6, 1.1, "A specification\nor a conversation",
        colour=BRICK, fs=12)
    box(ax, 3.4, 4.7, 2.4, 1.1, "Agents write\nthe tasks", colour=SLATE,
        fs=12)
    arrow(ax, (2.7, 5.25), (3.4, 5.25), colour=BRICK, lw=2)
    arrow(ax, (4.6, 4.7), (4.6, 4.16), colour=SLATE, lw=2)
    # The inner loop.
    inner_loop(ax, 4.6, 2.3, r=1.5, fs=10.5)
    box(ax, 7.3, 1.75, 1.35, 1.1, "Proposed\nchange", colour=TEAL, fs=12)
    arrow(ax, (6.7, 2.3), (7.3, 2.3), colour=TEAL, lw=2)
    # Review agents send findings back into the loop.
    box(ax, 7.05, 0.15, 1.85, 0.95, "Review\nagents", colour=SLATE, fs=12)
    arrow(ax, (7.975, 1.75), (7.975, 1.1), colour=SLATE, lw=1.8)
    arrow(ax, (7.05, 0.8), (5.4, 0.8), colour=SLATE, lw=1.8)
    # People review.
    box(ax, 9.3, 1.75, 1.6, 1.1, "We\nreview", colour=BRICK, fs=12)
    arrow(ax, (8.65, 2.3), (9.3, 2.3), colour=BRICK, lw=2)
    # Merging refits the model and raises new tasks.
    box(ax, 9.05, 4.7, 1.9, 1.1, "Merge\nand refit", colour=TEAL, fs=12)
    arrow(ax, (10.1, 2.85), (10.1, 4.7), colour=TEAL, lw=1.8)
    arrow(ax, (9.05, 5.25), (5.8, 5.25), colour=TEAL, lw=1.8, ls="--")
    # Who does the work: our implementation and review agents.
    avatar(ax, "figures/seabbs-bot.jpg", 0.75, 2.45)
    avatar(ax, "figures/sbfnk-bot.jpg", 1.75, 2.45)
    label(ax, 1.25, 1.75, "Implementation\nagents", colour=SLATE, fs=12)
    avatar(ax, "figures/seabbs-review-bot.jpg", 9.6, 0.62)
    avatar(ax, "figures/sbfnk-review-bot.png", 10.55, 0.62)
    # The people: here Sam builds a feature and Seb reviews it.
    avatar(ax, "figures/sam.jpg", 0.55, 4.15, size=0.75)
    label(ax, 1.05, 4.15, "Sam", colour=BRICK, fs=12, ha="left")
    avatar(ax, "figures/seb.jpg", 10.6, 3.75, size=0.75)
    label(ax, 10.6, 3.2, "Seb", colour=BRICK, fs=12)
    # Colour key: people come in at two points only.
    for k, (c, t) in enumerate([(BRICK, "People"), (SLATE, "Agents"),
                                (TEAL, "Code and checks")]):
        box(ax, 0.15, 0.95 - k * 0.42, 0.32, 0.28, "", colour=c, lw=2)
        label(ax, 0.6, 1.09 - k * 0.42, t, colour=INK, fs=12, ha="left")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    save(fig, "agents-agent-2.png")


agent_loop()
