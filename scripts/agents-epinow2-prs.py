#!/usr/bin/env -S uv run --with matplotlib --script
"""Merged EpiNow2 pull requests by month, from people and from agents.

Usage:
    ./scripts/agents-epinow2-prs.py

Needs an authenticated gh. Leaves out automated accounts (dependabot,
GitHub Actions and workflow apps). Writes figures/agents-epinow2-prs.png.
"""

import json
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

out = Path(__file__).resolve().parent.parent / "figures" / "agents-epinow2-prs.png"
prs = json.loads(subprocess.run(
    ["gh", "pr", "list", "-R", "epiforecasts/EpiNow2", "--state", "merged",
     "--limit", "3000", "--search", "merged:>=2025-01-01",
     "--json", "author,mergedAt"],
    capture_output=True, text=True, check=True,
).stdout)

agents = {"seabbs-bot", "sbfnk-bot"}
counts = {"People": Counter(), "Agents": Counter()}
for pr in prs:
    login = pr["author"]["login"]
    if login.startswith("app/"):
        continue
    month = pr["mergedAt"][:7]
    counts["Agents" if login in agents else "People"][month] += 1

months, d = [], date(2025, 1, 1)
today = date.today()
# The current month is incomplete, so it is left out.
while d < date(today.year, today.month, 1):
    months.append(f"{d:%Y-%m}")
    d = date(d.year + d.month // 12, d.month % 12 + 1, 1)
x = [date.fromisoformat(m + "-01") for m in months]

colours = {"People": "#b5432f", "Agents": "#4a5899"}
ink, muted = "#333333", "#6b7280"
plt.rcParams.update({"font.size": 16, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(8, 3.6), dpi=200)
for name, c in counts.items():
    y = [c[m] for m in months]
    ax.plot(x, y, color=colours[name], linewidth=2.5)
    i = max(range(len(y)), key=y.__getitem__)
    ax.annotate(name, (x[i], y[i]), xytext=(10, 4),
                textcoords="offset points", va="bottom",
                color=colours[name], fontweight="bold")
ax.set_ylabel("Merged per month", color=ink)
ax.set_xlim(x[0], x[-1])
ax.set_ylim(0, max(max(c.values()) for c in counts.values()) * 1.2)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(muted)
ax.tick_params(colors=muted)
ax.grid(axis="y", color="#e5e7eb", linewidth=0.8)
ax.set_axisbelow(True)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
fig.tight_layout()
fig.savefig(out)
print(out, {k: sum(v.values()) for k, v in counts.items()})
