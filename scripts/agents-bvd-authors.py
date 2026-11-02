#!/usr/bin/env -S uv run --with matplotlib --script
"""Merged BVDOutbreakSize pull requests by author, from the GitHub API.

Usage:
    ./scripts/agents-bvd-authors.py

Needs an authenticated gh. Writes figures/agents-bvd-authors.png.
"""

import json
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt

out = Path(__file__).resolve().parent.parent / "figures" / "agents-bvd-authors.png"

prs = json.loads(
    subprocess.run(
        [
            "gh", "pr", "list", "-R", "epiforecasts/BVDOutbreakSize",
            "--state", "merged", "--limit", "5000", "--json", "author",
        ],
        capture_output=True, text=True, check=True,
    ).stdout
)
counts = Counter(pr["author"]["login"] for pr in prs)

labels = {
    "seabbs-bot": "seabbs-bot, Sam's agents",
    "sbfnk-bot": "sbfnk-bot, Seb's agents",
    "app/dependabot": "dependabot, package updates",
    "seabbs": "Sam",
    "sbfnk": "Seb",
    "SamuelBrand1": "Samuel Brand",
}
rows = sorted(counts.items(), key=lambda kv: kv[1])
names = [labels.get(k, k) for k, _ in rows]
values = [v for _, v in rows]

teal, ink, muted = "#1f6f8b", "#333333", "#6b7280"
plt.rcParams.update({"font.size": 15, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=200)
bars = ax.barh(names, values, color=teal, height=0.6)
for bar, v in zip(bars, values):
    ax.text(
        bar.get_width() + 6, bar.get_y() + bar.get_height() / 2, str(v),
        va="center", color=ink,
    )
ax.set_xlabel(
    f"Merged pull requests, to {date.today():%-d %B %Y}", color=ink
)
ax.set_xlim(0, max(values) * 1.12)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(muted)
ax.tick_params(colors=muted)
ax.tick_params(axis="y", colors=ink)
fig.tight_layout()
fig.savefig(out)
print(out, sum(values), rows)
