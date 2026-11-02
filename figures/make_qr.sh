#!/usr/bin/env bash
# Regenerate the QR code on the talk plan and closing slides.
# It points at the talk page, not at the slides.
set -euo pipefail

cd "$(dirname "$0")"

uvx --from segno segno \
  --output "qr-talk.png" \
  --scale 10 --border 2 --error H \
  --dark "#333333" --light "#ffffff" \
  "https://samabbott.co.uk/HPRUNetworkAgentsandIDM/"
