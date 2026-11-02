#!/usr/bin/env python3
"""Export when I sent messages and when commits landed, for the build figures.

Usage:
    ./scripts/build-timeline-data.py SESSION.jsonl

Reads a Claude Code session log and this repository's git history, and
writes notes/build-timeline.csv. Only messages I typed count. Subagent
hand-backs, attached images and skill loads are left out.
"""

import json
import re
import subprocess
import sys

NOT_MINE = ("[Image", "Another Claude session", "Base directory for this skill",
            "This session is being continued")
MID_TURN = re.compile(r"The user sent a new message while you were working:"
                      r"\\n(.*?)\\n\\nThis is how")


def my_messages(path):
    seen = set()
    for line in open(path):
        r = json.loads(line)
        ts = r.get("timestamp")
        if r.get("type") == "assistant" or not ts:
            continue
        texts = []
        c = r.get("message", {}).get("content") if r.get("type") == "user" \
            else None
        if isinstance(c, str) and not c.startswith("<"):
            texts.append(c)
        if isinstance(c, list) and not any(
                b.get("type") == "tool_result" for b in c):
            texts += [b["text"] for b in c if b.get("type") == "text"
                      and not b["text"].startswith("<")]
        for m in MID_TURN.findall(json.dumps(r)):
            if m not in seen:
                seen.add(m)
                texts.append(json.loads('"' + m + '"'))
        for t in texts:
            if not t.startswith(NOT_MINE):
                yield ts[:19]


rows = [(t, "message") for t in my_messages(sys.argv[1])]
log = subprocess.run(["git", "log", "--format=%cI"], capture_output=True,
                     text=True, check=True).stdout.split()
rows += [(t[:19], "commit") for t in log]
rows.sort()
with open("notes/build-timeline.csv", "w") as f:
    f.write("time_utc,event\n")
    f.writelines(f"{t},{k}\n" for t, k in rows)
n = sum(k == "message" for _, k in rows)
print(f"{n} messages, {len(rows) - n} commits")
