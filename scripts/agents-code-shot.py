#!/usr/bin/env -S uv run --with pygments --with pillow --script
"""A hand-written gradient rule from BVDOutbreakSize, as an image.

Usage:
    ./scripts/agents-code-shot.py PATH_TO_BVDOutbreakSize_CLONE

Reads src/mooncake_rules.jl at origin/main, lines 1372 to 1401, and writes
figures/agents-complex-code.png.
"""

import subprocess
import sys
import textwrap
from pathlib import Path

from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import JuliaLexer

repo = sys.argv[1]
out = Path(__file__).resolve().parent.parent / "figures" / "agents-complex-code.png"
src = subprocess.run(
    ["git", "-C", repo, "show", "origin/main:src/mooncake_rules.jl"],
    capture_output=True, text=True, check=True,
).stdout.splitlines()
first, last = 1372, 1401
code = textwrap.dedent("\n".join(src[first - 1:last]))
png = highlight(
    code, JuliaLexer(),
    ImageFormatter(
        style="friendly", font_name="DejaVu Sans Mono", font_size=30,
        line_numbers=True, line_number_start=first, line_number_fg="#9ca3af",
        line_number_bg="#f3f4f6", line_number_chars=4, line_number_pad=14,
        line_pad=6, image_pad=24,
    ),
)
out.write_bytes(png)
print(out)
