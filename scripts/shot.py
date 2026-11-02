#!/usr/bin/env -S uv run --with playwright --script
"""Screenshot rendered pages so layout can be reviewed rather than guessed at.

Usage:
    ./scripts/shot.py OUTDIR [width] [page.html ...]

Defaults to the home page at desktop width. Pages are paths relative to
_site/. Requires "uvx --from playwright playwright install chromium" once.

Pages are served over http rather than opened as file:// URLs. Chromium
refuses cross origin module requests from file://, which kills quarto.js and
leaves the table of contents collapsed in every shot.
"""

import functools
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent.parent
site = root / "_site"

outdir = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "_shots"
width = int(sys.argv[2]) if len(sys.argv) > 2 else 1440
pages = sys.argv[3:] or ["index.html"]

outdir.mkdir(parents=True, exist_ok=True)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


handler = functools.partial(QuietHandler, directory=str(site))
server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()

try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": 1000})
        for rel in pages:
            if not (site / rel).exists():
                print(f"missing {site / rel}")
                continue
            page.goto(f"http://127.0.0.1:{port}/{rel}")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(400)
            name = rel.replace("/", "-").replace(".html", "")
            out = outdir / f"{name}-{width}.png"
            page.screenshot(path=str(out), full_page=True)
            print(out)
        browser.close()
finally:
    server.shutdown()
    server.server_close()
