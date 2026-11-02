# Drafting rules for the decks

Copied from `seabbs/AIandIDVUB`, with this project's mechanics.
Read in this order before writing a slide: `original-brief.md`,
`steers.md`, `style.md`, `llmisms.md`.

## What a slide is

- `##` heading that says the thing, not the topic. Wry where he would be.
- Two columns, about 40/60. Three or four short bullets on one side, one
  figure, schematic, code block or interactive on the other.
- The figure explains. The bullets say what the figure cannot.
- One `::: {.attribution}` block for sources only: paper, repo, URL, date
  read. No asides, no cross-references, no commentary.
- At most one callout, one sentence, and only when it carries a fact.
- No sub-bullets. No bullet longer than two lines.
- Section dividers are `# Title` slides with nothing else on them.

## Pictures and interactives

He asked for pictures, schematics and interactives, and sparse text.

- Every content slide has a visual unless it is a code slide or a single
  quote.
- Reuse first. The research notes list figures on disk with paths. Copy
  what you use into `figures/` with your deck's prefix, for example
  `keynote-bvd-streams.png`, and record the source path in the
  attribution.
- Draw what does not exist. Timelines, loops, box diagrams, before and
  after pairs. Write a script in `scripts/` (Python with matplotlib via
  `uv run --with matplotlib`, or hand-written SVG) so it can be regenerated.
  Match the site palette: teal `#1f6f8b`, slate `#4a5899`, brick `#b5432f`,
  greys. No mermaid box-and-arrow diagrams; he called them weak.
- Interactives, one to three per deck, only where they earn it. Options
  that work in Quarto revealjs: an `{ojs}` cell with an `Inputs.range`
  slider driving a Plot (for example a renewal process or a delay being
  censored); an `<iframe>` of a live site (the BVDOutbreakSize report at
  https://epiforecasts.io/BVDOutbreakSize/stable/, the COVID dashboard at
  https://epiforecasts.io/covid/); a revealjs `fragment` reveal on a
  before and after figure. Every interactive needs a static fallback
  figure in the same partial in case the room has no network.
- Alt text on every image.

## Words

- Where the research marks a line as **[Sam's words]**, use it verbatim.
- Lines from `how-I-llm` carry his facts in bot phrasing. Restate the fact
  plainly. Do not copy the phrasing.
- Every number and date comes from a research note with a source, and the
  source goes in the attribution. No number without one.
- Gloss on first use, one line each, for a room of statisticians and AI
  researchers: $R_t$, nowcasting, renewal process, pull request, bot
  account, SPI-M-O, SAGE, UKHSA, WIS.
- Run the greps in `llmisms.md` over your partials before you finish and
  fix every hit that is a fault.
- UK English. Under 80 characters a line except link targets and headings.
  No trailing whitespace. `./scripts/lint.sh` must pass.

## Mechanics

- Write into the existing `_partials/*.qmd` files, replacing the HTML
  comment. The six section titles and the 13 slide cap come from the
  brief. Do not add `#` divider slides; they cost slides from the cap.
- Copied figures keep their source deck's name with an `agents-` prefix.
- Render with `task`, which uses Quarto 1.9 from `~/.local/bin` when it is
  there. The `quarto` first on PATH is 1.3 and too old.
- Do not commit or push. The orchestrator does.
- When done, write `notes/draft-<deck>-report.md`: what you built, slide
  count, every number with its source, figures made or copied, what you
  were unsure about, and anything in the spec you could not do.

## Mine his past decks first

His steer, 12 September: "where it makes sense, heavily mine past
presentations of mine for images, complete slides and sections that make
sense".

Before drawing a figure or writing a slide, look for one he has already
given. Lift whole slides and whole sections where they fit, keeping his
wording, and copy the figures with your deck's prefix. Record the source
deck and file in the attribution. Past decks, in rough order of usefulness:

- `/home/seabbs/code/seabbs/JuliaCon2026/{roadmap,delays,composable}/_partials/`
  and `figures/` (August 2026, corrected by him line by line)
- `/home/seabbs/code/seabbs/how-to-serial-interval/_partials/` and
  `figures/` (June 2026, delays, censoring, composition)
- `/home/seabbs/code/EpiAware/ComposableProbabilisticIDModels/presentations/`
  (the 40 minute composable talk and shorter cuts) and `../figures/`
- `/home/seabbs/code/seabbs/BVDOutbreakSize/slides/` (the 10 June 2026
  WHO collaboratory talk on the live outbreak)
- `/home/seabbs/code/seabbs/hpru-ppie-kickoff/` (public involvement,
  ensembles, forecasting for the public)
- `/home/seabbs/code/nfidd/{nfidd,sismid,sismid-forecasting,sismid-nowcasting}/sessions/slides/`
  (teaching: forecasting, nowcasting, delays, Rt, evaluation; check the
  author of each deck, several are Nick Reich's or others')
- `/home/seabbs/code/seabbs/fellowships/decks/` (recent decks on his
  research programme)
- `/home/seabbs/code/archive/composable-grant/slides/`
- `/home/seabbs/code/seabbs/how-I-llm/_partials/` (facts and figures
  only; the phrasing is not his)
- `/home/seabbs/code/epinowcast/GuideToSTLTReportingDelays/meeting/`
