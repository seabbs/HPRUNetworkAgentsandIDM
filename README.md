# AI agents in infectious disease modelling

A talk for the Health Analytics and Modelling HPRU network.
Sam Abbott and Sebastian Funk, London School of Hygiene & Tropical Medicine.
15 minutes plus 5 for questions.

Rendered: [samabbott.co.uk/HPRUNetworkAgentsandIDM](https://samabbott.co.uk/HPRUNetworkAgentsandIDM)

## Building

Requires [Quarto](https://quarto.org/) 1.9 and, optionally,
[Task](https://taskfile.dev/) and [uv](https://docs.astral.sh/uv/) for the
QR code and screenshots.

```sh
task          # render the talk page and the deck to _site/
task preview  # live-reloading preview
task qr       # regenerate the QR code
task lint     # line length and trailing whitespace
```

## Layout

- `index.qmd`. The talk page, with the abstract and resources
- `slides.qmd`. The deck, with one partial per section in `_partials/`
- `notes/`. The brief, the steers and the style rules for the agents that
  draft the deck. Read `notes/original-brief.md` and `notes/style.md` first
- `figures/`. Figures and the QR code, which points at the talk page

The page and slides are drafted by coding agents and steered by the
authors.
