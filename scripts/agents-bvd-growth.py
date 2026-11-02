#!/usr/bin/env -S uv run --with matplotlib --script
"""Lines of Julia in BVDOutbreakSize src/ by week, from its git history.

Usage:
    ./scripts/agents-bvd-growth.py PATH_TO_BVDOutbreakSize_CLONE

Reads origin/main, so fetch first. Writes figures/agents-bvd-growth.png.
"""

import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import matplotlib.pyplot as plt

repo = sys.argv[1]
out = Path(__file__).resolve().parent.parent / "figures" / "agents-bvd-growth.png"


def git(*args):
    return subprocess.run(
        ["git", "-C", repo, *args], capture_output=True, text=True, check=True
    ).stdout


def src_lines(rev):
    files = [
        f for f in git("ls-tree", "-r", "--name-only", rev, "--", "src").split()
        if f.endswith(".jl")
    ]
    return sum(git("show", f"{rev}:{f}").count("\n") for f in files)


start = date(2026, 5, 19)
end = date.fromisoformat(
    git("log", "-1", "--format=%cs", "origin/main").strip()
)
days, lines = [], []
d = start + timedelta(days=7)
while d <= end + timedelta(days=6):
    rev = git("rev-list", "-1", f"--before={d.isoformat()}", "origin/main")
    days.append(min(d, end))
    lines.append(src_lines(rev.strip()))
    d += timedelta(days=7)

teal, ink, muted = "#1f6f8b", "#333333", "#6b7280"
plt.rcParams.update({"font.size": 15, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=200)
ax.plot(days, lines, color=teal, linewidth=2.5)
ax.scatter(days[-1:], lines[-1:], color=teal, s=60, zorder=3)
ax.annotate(
    f"{lines[-1]:,} lines",
    (days[-1], lines[-1]),
    xytext=(-10, 12),
    textcoords="offset points",
    ha="right",
    color=ink,
)
# The health-zone model, one pull request, merged 28 September 2026.
zone = date(2026, 9, 28)
zone_y = lines[min(range(len(days)), key=lambda i: abs(days[i] - zone))]
ax.annotate(
    "One pull request (#779)\nnests a health-zone model\nin the joint model",
    (zone, zone_y),
    xytext=(-235, -10),
    textcoords="offset points",
    color=ink,
    arrowprops={"arrowstyle": "-", "color": muted},
)
ax.set_ylabel("Lines of Julia in src/", color=ink)
ax.set_ylim(0, max(lines) * 1.15)
ax.yaxis.set_major_formatter(lambda v, _: f"{v:,.0f}")
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(muted)
ax.tick_params(colors=muted)
ax.grid(axis="y", color="#e5e7eb", linewidth=0.8)
ax.set_axisbelow(True)
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(out)
print(out, list(zip(days, lines))[-3:])
