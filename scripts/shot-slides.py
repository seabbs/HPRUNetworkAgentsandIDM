#!/usr/bin/env -S uv run --with playwright --script
"""Screenshot every slide of the rendered deck for layout review.

Usage:
    ./scripts/shot-slides.py [OUTDIR]

Writes one PNG per slide, slide-01.png and on, at 1920 by 1080, from
_site/slides.html. Requires "uvx --from playwright playwright install
chromium" once.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent.parent
deck = root / "_site" / "slides.html"
outdir = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "_shots"
outdir.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(deck.as_uri())
    page.wait_for_function("window.Reveal && Reveal.isReady()")
    n = page.evaluate("Reveal.getTotalSlides()")
    for i in range(n):
        page.evaluate(f"Reveal.slide({i})")
        page.wait_for_timeout(400)
        page.screenshot(path=str(outdir / f"slide-{i + 1:02d}.png"))
    browser.close()

print(f"{n} slides to {outdir}")
