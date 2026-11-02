#!/usr/bin/env -S uv run --with matplotlib --with pillow --script
"""Title slide banner: our agents fitting an epidemic curve while we watch.

Usage:
    ./scripts/agents-title.py

Writes figures/agents-title.png.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

TEAL = "#1f6f8b"
SLATE = "#4a5899"
BRICK = "#b5432f"
GREY = "#8a8f98"


def avatar(ax, path, x, y, size, ring):
    """Draw a round avatar with a coloured ring centred on (x, y)."""
    im = Image.open(path).convert("RGBA").resize((300, 300))
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 299, 299), fill=255)
    im.putalpha(mask)
    ax.add_patch(plt.Circle((x, y), size / 2 * 1.08, color=ring, zorder=4))
    ax.imshow(np.asarray(im), extent=(x - size / 2, x + size / 2,
                                      y - size / 2, y + size / 2),
              zorder=5, aspect="auto")


def curve(t):
    return 2.6 * np.exp(-((t - 8.2) ** 2) / 6.5) + 0.25


fig, ax = plt.subplots(figsize=(16, 3.6))
ax.set_xlim(0, 16)
ax.set_ylim(0, 3.6)
ax.set_aspect("equal")
ax.axis("off")

# The fitted model: a credible band, the median, and the observed data.
t = np.linspace(2.4, 13.6, 300)
mid = curve(t)
ax.fill_between(t, mid * 0.82, mid * 1.18, color=TEAL, alpha=0.15, lw=0)
ax.plot(t, mid, color=TEAL, lw=3)
rng = np.random.default_rng(3)
td = np.arange(2.8, 13.4, 0.45)
ax.scatter(td, curve(td) * rng.normal(1, 0.1, td.size), s=26, color=GREY,
           zorder=3)
ax.plot([2.2, 13.8], [0.08, 0.08], color=GREY, lw=1.5)

# Our agents at work along the curve.
bots = [("seabbs-bot.jpg", 5.0), ("sbfnk-bot.jpg", 6.9),
        ("seabbs-review-bot.jpg", 9.5), ("sbfnk-review-bot.png", 11.4)]
for path, x in bots:
    avatar(ax, f"figures/{path}", x, curve(x) + 0.62, 0.95, SLATE)

# The people, keeping an eye on things from either side.
avatar(ax, "figures/sam.jpg", 1.0, 0.75, 1.3, BRICK)
avatar(ax, "figures/seb.jpg", 15.0, 0.75, 1.3, BRICK)

fig.savefig("figures/agents-title.png", bbox_inches="tight",
            pad_inches=0.05, dpi=160, transparent=True)
print("wrote figures/agents-title.png")
