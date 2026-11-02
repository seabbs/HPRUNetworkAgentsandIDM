# Style for this project

Read this, then `llmisms.md`, before touching any slide.

## The brief, on style

His words:

> Note in recent talks look at the git to see how I have pruned and refined
> language and style to make it my own and follow. Be wary of overly dense
> text on slides. We like schematics, pictures and sparse clean slides.

## Reference decks, in order

1. `/home/seabbs/code/seabbs/how-to-serial-interval/_partials/`, especially
   `02-censoring.qmd`. The closest thing to what these decks should look
   like.
2. `/home/seabbs/code/seabbs/JuliaCon2026/{roadmap,delays,composable}/`
   in their **final** state, after about 200 commits of his corrections.
   Read `git log -p` there to see what he cut.
3. `/home/seabbs/code/EpiAware/ComposableProbabilisticIDModels/presentations/40min/index.qmd`.

Do **not** use `/home/seabbs/code/seabbs/how-I-llm` as a style reference.
It was written by agents and he has said so.
Its facts and claims are fine to reuse.

## What the good slides do

- A 40% column of three or four short bullets, a 60% column holding one
  purpose-built figure or schematic.
- One `::: {.attribution}` line for sources only. No editorial asides.
- At most one callout, one sentence.
- Section dividers as `# Title`, wry where he wrote them wry.
- About 1.5 slides a minute. The roadmap deck was 23 slides for 15 minutes,
  the serial interval deck about 40 for 30.

## What he cuts

`llmisms.md` is the full catalogue, mined from three decks.
The two most common: the bolted-on clause after a comma, and the moral at the
end of a slide.
Also: point-stamps, slogans in callouts, rule of three, negative parallelism,
title echoes, colon glosses, structural metaphors ("the through line"),
promise tails (", and what it cost"), unsupported numbers.

## What he keeps

Blunt admissions against interest, short verbless fragments, first-person
opinion flagged as opinion, numbers with a source, his jokes.

## This audience

The Health Analytics and Modelling HPRU network launch.
Mostly modellers and analysts, many of whom will hear "agent" and think of
agent-based models first.
Say what an agent is in one line before using the word.
See `original-brief.md`.

## Pages

A talk page carries the organisers' brief as the abstract, the links, and
the resources.
It does not carry errata or arguments with the brief.

`style-juliacon.md` is the fuller version of this, written for the JuliaCon
decks. Its specifics are that project's; its rules carry over.
