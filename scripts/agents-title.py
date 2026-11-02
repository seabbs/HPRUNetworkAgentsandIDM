#!/usr/bin/env -S uv run --with matplotlib --with pillow --script
"""Title slide banner: people talk to their agents, and the agents to each other.

Usage:
    ./scripts/agents-title.py

Sam talks to seabbs-bot and Seb to sbfnk-bot. The two bots hand work to a
crowd of agents that talk to each other and build and fit an SEIR model.
Writes figures/agents-title.png.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon
from PIL import Image, ImageDraw

TEAL = "#1f6f8b"
SLATE = "#4a5899"
BRICK = "#b5432f"
GREY = "#8a8f98"
BOTS = ["seabbs-bot.jpg", "sbfnk-bot.jpg", "seabbs-review-bot.jpg",
        "sbfnk-review-bot.png"]


def avatar(ax, path, x, y, size, ring, alpha=1.0):
    """Draw a round avatar with a coloured ring centred on (x, y)."""
    im = Image.open(f"figures/{path}").convert("RGBA").resize((300, 300))
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 299, 299), fill=int(255 * alpha))
    im.putalpha(mask)
    ax.add_patch(plt.Circle((x, y), size / 2 * 1.09, color=ring, zorder=4,
                            alpha=alpha))
    ax.imshow(np.asarray(im), extent=(x - size / 2, x + size / 2,
                                      y - size / 2, y + size / 2),
              zorder=5, aspect="auto")


def bubble(ax, x, y, colour, tail, w=0.85, h=0.42):
    """A chat bubble with three dots, its tail pointing to (tail)."""
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.18",
                                facecolor="white", edgecolor=colour, lw=2.2,
                                zorder=6))
    tx = x + np.sign(tail[0] - x) * 0.12
    ax.add_patch(Polygon([(tx - 0.09, y - h / 2 + 0.01),
                          (tx + 0.09, y - h / 2 + 0.01), tail],
                         closed=True, facecolor="white", edgecolor=colour,
                         lw=2.2, zorder=5))
    for dx in (-0.2, 0, 0.2):
        ax.add_patch(plt.Circle((x + dx, y), 0.055, color=colour, zorder=7))


def curve(t):
    return 0.85 * np.exp(-((t - 8) ** 2) / 2.6) + 0.32


fig, ax = plt.subplots(figsize=(16, 3.8))
ax.set_xlim(0, 16)
ax.set_ylim(0, 3.8)
ax.set_aspect("equal")
ax.axis("off")

# The shared work: the model's fitted epidemic curve with its band and the data.
t = np.linspace(5.0, 11.0, 300)
mid = curve(t)
ax.fill_between(t, mid * 0.82, mid * 1.18, color=TEAL, alpha=0.15, lw=0)
ax.plot(t, mid, color=TEAL, lw=3)
rng = np.random.default_rng(3)
td = np.arange(5.2, 10.9, 0.38)
ax.scatter(td, curve(td) * rng.normal(1, 0.1, td.size), s=22, color=GREY,
           zorder=3)
ax.plot([4.9, 11.1], [0.2, 0.2], color=GREY, lw=1.5)

# The model they fit: susceptible, exposed, infectious, recovered.
for k, name in enumerate("SEIR"):
    x = 6.35 + k * 1.1
    ax.add_patch(FancyBboxPatch((x - 0.3, 1.5), 0.6, 0.42,
                                boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor="white", edgecolor=TEAL, lw=2.2,
                                zorder=3))
    ax.text(x, 1.71, name, ha="center", va="center", fontsize=17,
            color=TEAL, fontweight="bold", zorder=4)
    if k < 3:
        ax.add_patch(FancyArrowPatch((x + 0.34, 1.71), (x + 0.76, 1.71),
                                     arrowstyle="-|>", mutation_scale=14,
                                     color=TEAL, lw=2, zorder=3))
ax.add_patch(FancyArrowPatch((8, 1.46), (8, 1.22), arrowstyle="-|>",
                             mutation_scale=14, color=TEAL, lw=2, zorder=3))

# A crowd of agents talking to each other above the work.
pts = []
for i, x in enumerate(np.linspace(4.4, 11.6, 11)):
    y = 3.05 if i % 2 else 2.45
    pts.append((x + rng.uniform(-0.12, 0.12), y + rng.uniform(-0.1, 0.1)))
pts = np.array(pts)
for i in range(len(pts)):
    for j in range(i + 1, min(i + 3, len(pts))):
        ax.plot(*pts[[i, j]].T, color=SLATE, lw=1.2, alpha=0.45, zorder=1)
for i, (x, y) in enumerate(pts):
    avatar(ax, BOTS[i % 4], x, y, 0.5, SLATE, alpha=0.9)
for i in (2, 6, 9):
    mx, my = pts[i:i + 2].mean(axis=0)
    ax.add_patch(FancyBboxPatch((mx - 0.17, my - 0.08), 0.34, 0.16,
                                boxstyle="round,pad=0.01,rounding_size=0.08",
                                facecolor="white", edgecolor=SLATE, lw=1.2,
                                zorder=6))
    for dx in (-0.08, 0, 0.08):
        ax.add_patch(plt.Circle((mx + dx, my), 0.022, color=SLATE, zorder=7))

# Sam and seabbs-bot, Seb and sbfnk-bot.
avatar(ax, "sam.jpg", 0.9, 0.9, 1.3, BRICK)
avatar(ax, "seabbs-bot.jpg", 3.3, 1.0, 1.1, SLATE)
bubble(ax, 1.9, 2.05, BRICK, (1.4, 1.55))
bubble(ax, 3.1, 2.2, SLATE, (3.3, 1.65))
avatar(ax, "seb.jpg", 15.1, 0.9, 1.3, BRICK)
avatar(ax, "sbfnk-bot.jpg", 12.7, 1.0, 1.1, SLATE)
bubble(ax, 14.1, 2.05, BRICK, (14.6, 1.55))
bubble(ax, 12.9, 2.2, SLATE, (12.7, 1.65))

# Our two bots hand work to the crowd, and the crowd builds the model.
for p, q, rad in [((3.75, 1.45), pts[0] - (0.12, 0.25), -0.2),
                  ((12.25, 1.45), pts[-1] - (-0.12, 0.25), 0.2)]:
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16,
                                 color=SLATE, lw=2, zorder=2,
                                 connectionstyle=f"arc3,rad={rad}"))
for k, i in enumerate((2, 4, 6, 8)):
    x0, y0 = pts[i]
    ax.add_patch(FancyArrowPatch((x0, y0 - 0.3), (6.35 + k * 1.1, 1.97),
                                 arrowstyle="-|>", mutation_scale=14,
                                 color=TEAL, lw=2, zorder=2))

fig.savefig("figures/agents-title.png", bbox_inches="tight",
            pad_inches=0.05, dpi=160, transparent=True)
print("wrote figures/agents-title.png")
