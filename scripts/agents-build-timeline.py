#!/usr/bin/env -S uv run --with matplotlib --script
"""When the deck was built: commits over the day, with my messages beneath.

Usage:
    ./scripts/agents-build-timeline.py

Reads notes/build-timeline.csv (times from the session log and git) and
writes figures/agents-build-timeline.png.
"""

import csv
from datetime import datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

TEAL = "#1f6f8b"
BRICK = "#b5432f"
GREY = "#6b7280"

events = {"commit": [], "message": []}
with open("notes/build-timeline.csv") as f:
    for row in csv.DictReader(f):
        events[row["event"]].append(datetime.fromisoformat(row["time_utc"]))
commits = sorted(events["commit"])
messages = sorted(events["message"])

plt.rcParams.update({"font.size": 15, "font.family": "sans-serif"})
fig, ax = plt.subplots(figsize=(11, 4.6))
ax.step(commits, range(1, len(commits) + 1), where="post", color=TEAL, lw=2.5)
ax.text(commits[-1], len(commits) + 3, f"{len(commits)} commits",
        color=TEAL, ha="right", va="bottom", fontsize=15, fontweight="bold")
ax.vlines(messages, -11, -3, color=BRICK, lw=1.2, alpha=0.7)
ax.text(messages[0], -14, f"{len(messages)} messages from me", color=BRICK,
        ha="left", va="top", fontsize=14, fontweight="bold")
ax.set_ylim(-24, len(commits) + 12)
ax.set_yticks([0, 25, 50, 75])
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.xaxis.set_major_locator(mdates.HourLocator())
ax.set_xlabel("2 November 2026, UTC", color=GREY)
ax.grid(axis="y", color="#e5e7eb")
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(GREY)
ax.tick_params(colors=GREY, length=0)
fig.savefig("figures/agents-build-timeline.png", dpi=160,
            bbox_inches="tight", pad_inches=0.1)
print("wrote figures/agents-build-timeline.png")
