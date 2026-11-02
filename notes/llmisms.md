# LLM-isms this author strips out

A corpus of the phrasing Sam Abbott removes from his own slides, mined from
the git history of three previous decks.
Another agent should be able to act on this without asking anyone.

Sources, all verified by reading `git log -p`:

- `SI` = `/home/seabbs/code/seabbs/how-to-serial-interval`
- `LLM` = `/home/seabbs/code/seabbs/how-I-llm`
- `CPIDM` =
  `/home/seabbs/code/EpiAware/ComposableProbabilisticIDModels`
  (`presentations/`)

The two heaviest commits are `SI bdd0a34` ("Revise deck from review", which
rewrote the whole deck) and `LLM eac9c73` ("cut to 18 content slides").
Most of the single-line cuts are the "Drop / Trim / Cut / Shorten / Soften"
commits in `SI`.

## How to use this

1. Run the grep for a pattern over `*.qmd`.
2. For each hit, ask the diagnostic question in that section.
   A hit is not automatically a fault.
3. Apply the rewrite rule.
   The default rewrite is deletion, not rephrasing.
4. Do not touch `::: {.abstract}` blocks, `::: {.prompt}` blocks,
   `notes/original-brief.md`, `notes/steers.md`, or the
   `BANNED_README_WORDS` code fence in
   `roadmap/_partials/02-what-we-have.qmd`.
   That text is quoted source.

The single most common pattern by count of removals is **the bolted-on
clause** (pattern 2), followed by **the moral** (pattern 3).

---

## 1. The point-stamp

**Definition.** A sentence, or a clause, whose only job is to tell the
audience that the sentence before it mattered.

**Grep.**

```
rg -n --glob '*.qmd' -i \
  '\bthe point (is|was|here|of)\b|\b(is|was) the point\b|\bwhich is the point\b|\bthat is (what|why) [a-z]+ matter'
```

**Example A** (`LLM eac9c73`, `_partials/05-scale.qmd`).
Removed with the slide it sat on:

> The point is not attribution etiquette.
> It is that I can *filter* — and so can anyone else reading the history.

Rewrite chosen: nothing replaced it.
The bullet above it already said `git log` tells you who did what.

**Example B** (`LLM eac9c73`, `_partials/03-tooling.qmd`).
Removed:

> - Nothing clever, and that is the point — no bespoke orchestrator to
>   maintain

Rewrite chosen: the claim moved into an attribution line that states the
fact instead of the moral, later settling at
"what I maintain is prompts and config, not services" (`LLM 8c7e834`).

**Example C** (`SI bdd0a34`, `_partials/07-collaboration.qmd`).
Before:

> - The point is to drop the parametric-shape assumption while keeping the
>   censoring and truncation handling honest.

After:

> - It drops the parametric-shape assumption while still handling the
>   censoring and truncation.

**Diagnostic.** Delete the sentence.
If the slide still makes the point, the sentence was the pattern.

**Rewrite rule.** Delete it.
If deleting loses information, move the information into the preceding
sentence as a plain statement, as in Example C.

**Note.** One survivor exists: the `.callout-important` in
`LLM _partials/09-steers.qmd` ("The prompt is not the work. The steering is
the work.").
That is the author's own steer, quoted back.
Assume any *you* wrote is the pattern.

---

## 2. The bolted-on clause

**Definition.** A trailing clause added to a finished sentence after a
comma or a dash, carrying a second idea the sentence did not need.
Usually starts with `which`, `and`, `so`, `— that is`, or a participle.
This is the most frequent removal in the corpus.

**Grep.**

```
rg -n --glob '*.qmd' \
  ',\s+(which|and that|so that|so it|so they|and the|making|giving|leaving|allowing|ensuring|meaning|showing)\b'
rg -n --glob '*.qmd' '\s—\s(that|which|and)\s'
```

**Example A** (`SI 55adbb7`, commit message "Cut redundant
right-censored/meeting-point bullet on contact-interval slide").
Removed:

> - Contact intervals are right-censored, so survival analysis is the
>   natural tool, and the natural meeting point with this room

Rewrite chosen: the whole bullet went.
The slide already carried a precise contact-interval definition added two
commits earlier (`SI a865fe2`).

**Example B** (`SI 746e423`, "Remove SI/GI mean-coincidence bullet").
Removed:

> - They share a mean, but coincide most closely only without
>   presymptomatic transmission — that is what pulls them apart

Rewrite chosen: deleted, nothing added.
It had been added one commit before (`SI 97be5f2`) and did not survive a
re-read.

**Example C** (`SI 4897ba8`, "Trim MNAR bullet to just the term").
Before:

> - Observation is often **missing not at random**: which pairs we see
>   depends on the very timing we are trying to estimate

After:

> - Observation is often **missing not at random**

**Example D** (`LLM eac9c73`, `_partials/02-use-cases.qmd`).
Before:

> - One sentence, one commit, so every change is separately reviewable and
>   separately revertible

After (via `LLM 8c7e834`):

> - One sentence, one commit. Small enough to review on its own, and to
>   revert on its own

**Diagnostic.** Cover everything after the comma.
If the first half is a complete, useful claim, the tail is the pattern.

**Rewrite rule.** Delete the tail.
If it carries a real second claim, break it into its own sentence or its
own bullet, and check the slide can still afford the line.

---

## 3. The moral

**Definition.** A closing line, bullet, or callout whose content is the
significance of the slide rather than any new fact.
Often a `::: {.callout-note}` or a `## Lesson` heading.

**Grep.**

```
rg -n --glob '*.qmd' -i \
  '\bwhy (this|it|that) matters\b|\bmatters? (most|here|because)\b|\b(is|are) (the )?(key|critical|crucial|essential|vital)\b|^## (Lesson|Takeaway|Why)'
rg -n -A3 --glob '*.qmd' 'callout-note\}' | rg -i 'this is (where|exactly|the)'
```

**Example A** (`SI a865fe2`, "drop biases-slide note"),
`_partials/05-practice.qmd`.
Removed callout:

> This is where the survival-analysis and modelling views most need each
> other.

Rewrite chosen: nothing.
The column now holds only the attribution.

**Example B** (`SI bdd0a34`, deleting `_partials/04-practice.qmd`).
Removed callout:

> ## Lesson
> The index cases pin the incubation period, which is what lets the
> sourced cases identify transmission timing at all.
> The serial interval is not estimated directly: it is what the two delays
> imply.

Rewrite chosen: the case study was rebuilt as "the model" and "results"
slides carrying a model DAG and a results figure, with no lesson block.

**Example C** (`SI bdd0a34`, deleting `_partials/08-tte-broadly.qmd`).
Removed:

> None of these is metaphor.
> Each is the same likelihood, so the tools transfer in both directions.

Also removed in the same commit, from the double-censoring slide:

> A double interval censored likelihood is one convolution composed with
> one CDF difference.
> Nothing exotic.

replaced by the concrete
"In the past this was often written as a double integral, which is
typically more complicated to evaluate."

**Rewrite rule.** Delete.
If the slide needs a note, make it carry a fact, a caveat, or a citation,
never an evaluation of the slide.

---

## 4. The slogan callout

**Definition.** A short, balanced, quotable line in a callout that
compresses the slide into marketing.

**Grep.**

```
rg -n -A2 --glob '*.qmd' 'callout-(note|important|tip)\}' | \
  rg -n '^[^:]*:[0-9-]+[:-][A-Z][^.]{10,70}\.$'
```

Then read the hits; this one needs judgement rather than a pattern.

**Example A** (`SI 0431103`), `_partials/03-extending.qmd`.
Removed callout:

> One likelihood, many delays, with the bias adjustments handled for you.

Rewrite chosen: replaced with an actual figure,
`figures/pc-pmf-lognormal-1.png`, captioned
"Empirical (censored) samples vs the analytic PMF".

**Example B** (`LLM eac9c73`), `_partials/08-how-i-made-this.qmd`.
Removed:

> The deck is the demo. Source:
> [github.com/seabbs/how-I-llm](https://github.com/seabbs/how-I-llm)

Rewrite chosen: replaced by "I wrote the argument and none of the words",
itself corrected later to "almost none of the words" (`LLM 8c7e834`).

**Rewrite rule.** Replace the slogan with a figure, a number, or a code
block.
A slide that needed a slogan usually needed evidence.

---

## 5. Rule of three

**Definition.** Three parallel items where the third exists for rhythm, or
a triple of triples.

**Grep.**

```
rg -n --glob '*.qmd' '\b\w+, \w+,? and \w+\b'
rg -n --glob '*.qmd' '(\w+), (\w+),? (or|and) (\w+)( give| are| gives)'
```

**Example A** (`SI 8ee7785`), `_partials/04-paper.qmd`.
Before:

> A separable $V(t)\,g(t)$ recovers the Burr; constant, power-of-time, or
> staged limits give the exponential, Weibull, or gamma.

After:

> other activation functions give other families (a separable
> $V(t)\,g(t)$ gives the Burr)

The triple-mapped-to-a-triple went; the one example that carries the idea
stayed.

**Example B** (`SI 9df6beb`, "Shorten per-event hazards note so it fits on
the slide").
Before:

> - $h_S = \beta_S V(t)$: symptoms have no fixed load threshold — they
>   track replication, host response, and detection — so onset is a
>   stochastic activation that rises with load

After:

> - $h_S = \beta_S V$: no fixed symptom threshold, so a stochastic
>   activation

**Example C** (`CPIDM 9b57979`), the deleted Conclusions slide, which
stacked three abstract benefits and was replaced wholesale by a
"What I want from you" slide of concrete asks.

**Rewrite rule.** Keep the items that are load-bearing.
Two is fine.
One with a real example beats three without.

---

## 6. Negative parallelism

**Definition.** Defining something by what it is not: "not X but Y",
"not just X", "X, not Y", "This is not a pitch. It is ...".

**Grep.**

```
rg -n --glob '*.qmd' -i \
  '\bnot (just|only|merely|simply)\b|\bnot [^.]{1,40}\bbut\b|\bthis is not\b|\brather than (just|merely)\b|, not the other way'
```

**Example A** (`LLM eac9c73`), `_partials/01-where-i-am.qmd`.
Before:

> This is not a pitch. It is a description of a working setup, its costs,
> and the bits that do not work.

After:

> Everything that follows is a description of a working setup, including
> the parts that do not work.

**Example B** (`LLM eac9c73`), `_partials/04-drc.qmd`.
Before:

> I would not have attempted this shape of project on this timescale
> without agents. Not "it went faster" — I would have picked a smaller
> question.

After:

> - I would not have picked a question this size without them

**Example C** (`SI bdd0a34`), `index.qmd`, whole bullet removed:

> - Design the estimand around the data, not the data around a textbook
>   serial interval

and from the same commit, `_partials/03-paper.qmd`:

> - Pick the hazard to match the data and the question, not the other way
>   round

**Also** (`SI de2e7c2`, "Drop 'not iid survival times' from Ask 2"): the
trailing contrast "…, not iid survival times" was cut from an otherwise
unchanged sentence.

**Rewrite rule.** State the positive claim only.
Keep a contrast only where the wrong belief is one the audience actually
holds, and then name it plainly.

---

## 7. Title echo and structure announcement

**Definition.** A line that restates the slide heading, or announces the
shape of what follows, instead of saying something.

**Grep.**

```
rg -n --glob '*.qmd' -B1 '^(The same|Three|Two|Here) .{0,40}:$'
rg -n --glob '*.qmd' -i '^(- )?(as we (will|have) see|first,|in this (talk|section)|we will (now )?(look|turn|cover))'
```

Also compare each `##` heading with the first bullet under it by eye.

**Example A** (`SI 705bb74`, "Drop redundant 'same f, three roles' line on
ecosystem slide").
Removed lead-in above three labelled equations:

> The same $f$, three roles:

The three equations were already labelled `epidist`, `EpiNow2`,
`epinowcast`.

**Example B** (`SI bdd0a34`), `_partials/08-tte-broadly.qmd`, deleted with
its slide:

> ## The same machinery runs through all of this
>
> The serial interval is one censored, truncated, dependent delay.
> The same survival-analysis ideas reappear right across infectious
> disease modelling, often under other names.

**Example C** (`LLM eac9c73`), `index.qmd`: the whole "Talk plan" slide and
the whole "Summary" slide were cut, along with the `# Wrapping up`
section heading.

**Rewrite rule.** Delete the echo.
Do not re-announce the section you are already in.

---

## 8. The colon gloss

**Definition.** A colon in a bullet followed by a restatement or an
enumeration, where a full stop or nothing would do.
The house style already says minimise colons; the history shows how.

**Grep.**

```
rg -n --glob '*.qmd' '^\s*-\s.*[a-z]\*{0,2}:\s'
```

**Example A** (`LLM eac9c73`), `_partials/02-use-cases.qmd`.
Before:

> - Agents are good at the boring half: unused arguments, silent
>   fallbacks, an off-by-one index, a test that asserts nothing

After:

> - Good at the boring half. Unused arguments, silent fallbacks, an
>   off-by-one index, a test that asserts nothing

**Example B** (`LLM 8c7e834`), `_partials/05-scale.qmd`.
Before:

> - Ten of my skills run at org level. Standards, CI health, dependencies,
>   releases

which had itself come from
"- Ten of my skills run at org level: standards, CI health, dependencies,
releases" in `LLM eac9c73`.
The final form drops the colon and states the unit:
"Ten of my skills take a whole org as their unit, not one repo."

**Example C** (`SI b907acc`, "Reframe reference-cohort bullet around which
event reporting conditions on").
Before:

> - The reference cohort matters: forward versus backward intervals

After:

> - The reference cohort matters: which event reporting is conditioned on

Here the colon survived because the right-hand side is the content, not a
gloss.
That is the distinction to apply.

**Rewrite rule.** If the right-hand side restates the left, cut it.
If it is a list, replace the colon with a full stop.
Keep the colon only when the right-hand side is the substance.

---

## 9. Overclaimed identity

**Definition.** "X really is Y", "X is exactly Y", "*is*" in italics for
emphasis, "nothing but", "just".
The author repeatedly softened these to what he can defend.

**Grep.**

```
rg -n --glob '*.qmd' -i \
  '\breally (is|it is|a)\b|\bis exactly\b|\bexactly (a|the)\b|\bis just (a|an|one)\b|\*is\*|\bprecisely (the|a)\b'
```

**Example A** (`SI 328e770`, "soften SI-as-composition wording").
Before:

> - We treated the SI as one event-to-event delay; really it is a
>   **composition** of delays

After:

> - We treated the SI as one event-to-event delay; it can be thought of as
>   a **composition** of delays

The same softening was applied to the "Why?" slide in `SI a7d9c77`:
"many epidemiological delays are themselves **composed**" became
"can be thought of as".

**Example B** (`SI 1891fec`), `_partials/03-extending.qmd`.
Before:

> - A common-source outbreak shares one exposure window — exactly a known
>   primary-censoring interval

After:

> - A common-source outbreak shares one exposure window
> - The distribution of exposure times within the source may itself
>   differ — it need not be uniform

The overclaim was replaced by the caveat that made it false.

**Example C** (`SI bdd0a34`), `_partials/02-censoring.qmd`.
Before:

> - Right truncation here *is* the nowcasting problem of survival
>   analysis: short delays are over-represented early on

After:

> - Short delays are over-represented early in an epidemic

**Rewrite rule.** Drop the intensifier.
If the equivalence is real, state it flatly and once.
If it is an analogy, say "can be thought of as".

---

## 10. Adjectives and verbs doing persuasive work

**Definition.** Evaluative words that add no information: comprehensive,
powerful, seamless, robust, novel, key, highest-value, elegant, natural,
full, complete, and inflated verbs like "validated", "enables",
"unlocks", "expands".

**Grep.**

```
rg -n --glob '*.qmd' -i \
  '\b(comprehensive|practitioner|robust|novel|powerful|seamless|elegant|cutting-edge|state-of-the-art|highest-value|best-in-class|landscape|leverage|utilis|utiliz|facilitate|foster|streamline|pivotal|nuanced|cornerstone|synergy|overarching|current approaches)\b'
rg -n --glob '*.qmd' -i '\b(validated|unlocks|enables|empowers|transforms) '
```

**Example A** (`LLM eac9c73`), `_partials/02-use-cases.qmd`.
Before:

> - Small, verifiable, tedious. The highest-value category, and the least
>   interesting to talk about

After:

> - Small, verifiable, tedious. The most useful category, and the least
>   interesting to talk about

Same commit, `_partials/04-drc.qmd`: "Validated against two independently
published estimates" became "Checked against two independently published
estimates", and "several independent reviewers" became
"several reviewers".

**Example B** (`SI bdd0a34`), `index.qmd`: the slide titled
`## The method landscape` was deleted outright, taking with it
"Standardised, bias-aware methods make results **comparable**".

**Example C** (`SI 28515cc`, "Tidy wording on primarycensored-solves
slide").
"Signed support too (normal, logistic, …)" became
"Signed support (normal, logistic, …)", and the flattering clause
"for when you would rather not pick a family" was cut from the
non-parametric estimator bullet, leaving the blunt
"it needs an eye on it, and is not clearly a good idea".

**Example D** (`CPIDM 9b57979`), deleted Conclusions slide:

> - Likely key for enabling robust LLM assisted model construction with
>   reduced errors

**Rewrite rule.** Delete the adjective.
If the claim collapses without it, the claim was the adjective.

---

## 11. Metadiscourse and stage directions

**Definition.** Text about the talk rather than in it: agendas, summaries,
"honestly", "an honest question", "it is worth noting", promises about
what the speaker will do.

**Grep.**

```
rg -n --glob '*.qmd' -i \
  '\bit is worth (noting|saying)\b|\bnote that\b|\bhonestly\b|\ban honest\b|\bto be clear\b|\bI will (go and|try to|promise)\b|\blet me\b|\bin this section\b'
rg -n --glob '*.qmd' '^## (Talk plan|Agenda|Summary|Outline|Recap)'
```

**Example A** (`SI a9e5d50`, "drop in-both-directions callout"),
`_partials/07-collaboration.qmd`.
Removed:

> I have three asks for the survival-analysis people in the room.
> They run in both directions, but today I am mostly asking.

The section now opens straight on "Ask 1".

**Example B** (`SI bdd0a34`), same file.
Before:

> An honest question. We spend a lot of effort on primary plus secondary
> interval censoring…

After:

> We spend a lot of effort on primary plus secondary interval censoring…

**Example C** (`LLM eac9c73` and `LLM b0dbb7b`).
The `# The tooling, honestly` heading became `# The tooling`.
The closing line "Tell me what you think agents cannot do. I will go and
try it." became "…I will not promise to try it, but I want to know",
with the commit message "Inviting the challenge is honest; promising to
act on it is not."

**Note.** "it is worth noting" itself does not appear in these repos.
It belongs to this family; treat a hit as a fault.

**Rewrite rule.** Delete.
Agendas and summary slides go entirely unless the audience needs the map.

---

## 12. Room flattery

**Definition.** A clause that tells the audience they are the right
audience, or that their field is where the answer lies.

**Grep.**

```
rg -n --glob '*.qmd' -i \
  '\b(this room|in the room|you (already )?know|as you (all )?know|the natural meeting point|this audience|you are the)\b'
```

**Example A** (`SI 55adbb7`).
Removed: "…and the natural meeting point with this room" (see pattern 2).

**Example B** (`SI bdd0a34`), `_partials/07-collaboration.qmd`.
Removed from Ask 1:

> Where would a survival analyst say I have reinvented something, badly?

and from Ask 3:

> - Tell me which of these is real and which is us reinventing your wheels.

Rewrite chosen: one direct question each, e.g. "is the discrete-time hazard
formulation right, and how should we modellers handle a non-parametric
delay estimate for onward use?"

Also cut in the same commit, from the original draft `SI 3e040bb`:
"A special case of the survival-analysis problem this room already knows".

**Rewrite rule.** Ask the question.
Do not tell the room it is qualified to answer it.

---

## 13. Unsupported precision and absolutes

**Definition.** A number, a superlative, or a universal ("every", "all",
"nobody", "always") that no repo, API, or registry backs.
This is the failure the author polices hardest.
`LLM 8c7e834` is titled "fix: correct 41 claims the git record does not
support".

**Grep.**

```
rg -n --glob '*.qmd' '\b(every|all|always|never|none|nobody|no one|the only|the first|the best)\b'
rg -n --glob '*.qmd' '~?\b[0-9][0-9,\.]*\b'
```

**Example A** (`LLM 8c7e834`), `_partials/01-where-i-am.qmd`.
Before:

> - Most code I ship is written by an agent and reviewed by me

After:

> - Most code I ship is written by an agent. About half of it carries a
>   review from me

The commit message gives the check: 712 of 1,371 merged bot pull requests
carry no review.

**Example B** (`LLM 8c7e834`), `_partials/02-use-cases.qmd`.
"Every change is read by something before a human reads it" became
"Most changes are read by something before I read them", because the
review workflow was gated on a login that never matched.

**Example C** (`SI 0676d35`, "Drop specific GT numbers that did not match
the figure").
Before:

> - Shorter mean generation time for Omicron (~3.1 d) than Delta (~4.0 d)

After:

> - Shorter mean generation time for Omicron than Delta

**Also** (`LLM 1fceb9a`): "530 pull requests" was GitHub's latest issue
number, not a count, and became 353; "22 packages" was the org repo count
and became eleven.

**Rewrite rule.** Verify against the repo, the GitHub API, or the
registry, or delete the number.
Replace universals with the measured share.

---

## 14. Decorative hedges

**Definition.** Hedging that softens tone rather than lowering a claim:
"in principle", "arguably", "somewhat", "may potentially", "can help to".

**Grep.**

```
rg -n --glob '*.qmd' -i \
  '\bin principle\b|\barguably\b|\bsomewhat\b|\b(may|might|could) (potentially|well|perhaps)\b|\bcan help( to)?\b|\bto some extent\b|\bfairly\b'
```

**Example A** (`SI a8ff162`), `_partials/06-composed.qmd`.
Before:

> Simulation and `logpdf` for individual data, convolution for counts, or
> a reaction network for a compartmental model — and, in principle,
> multi-state.

After:

> Simulation and `logpdf` for individual data, convolution for counts, or
> — via the **linear-chain trick** — a Catalyst reaction network for a
> compartmental model.

**Example B** (`LLM 8c7e834`), `_partials/03-tooling.qmd`.
Before:

> - Agents get their own warm Julia over MCP, so they talk to a process
>   that is already compiled

After:

> - Julia precompilation dominates the loop, so I keep a warm REPL in a
>   pane. Giving agents their own over MCP is this week's experiment

The vague capability claim became a dated, checkable one.

**Counter-rule, and it matters.** The author *adds* hedges when they lower
a claim to what he can defend: "really it is a composition" became "can be
thought of as a composition" (`SI 328e770`, `SI a7d9c77`), and
"Signed support" kept the blunt caveat "it needs an eye on it, and is not
clearly a good idea" (`SI 28515cc`).
Cut hedges that protect the tone.
Keep hedges that protect the truth.

---

## 15. The benefit tail

**Definition.** A closing clause that explains why a technical fact is
good for the reader: "so it is faster", "so you get X for free", "handled
for you", "at scale".

**Grep.**

```
rg -n --glob '*.qmd' -i \
  '\bso (it|the|you|this) (is|are|get|gets|can)\b|\bfor free\b|\bhandled for you\b|\bat scale\b|\bout of the box\b|\bcomes along\b'
```

**Example A** (`SI bdd0a34`), deleting `_partials/06-pointsource.qmd`.
Removed callout:

> Analytic forms cut a numerical integral to a few CDF calls, so the
> likelihood is faster and more stable for inference at scale.

Removed from the same slide:

> - Onsets are also reported by day, so secondary censoring and
>   right-truncation come along for free
> - Exact solutions matter most here, where the shared window is fixed and
>   reused across thousands of cases

**Example B** (`SI 0431103`), `_partials/03-extending.qmd`.
Removed:

> One likelihood, many delays, with the bias adjustments handled for you.

Rewrite chosen: a figure of the empirical versus analytic PMF.

**Rewrite rule.** State the mechanism.
Let the audience draw the benefit.

---

## 16. The structural metaphor

**Definition.** Labelling a thing with a borrowed noun that dresses up a plain
relationship. "X is the through-line", "the spine of the talk", "the backbone
of the ecosystem", "the thread running through", "at the heart of", "the glue
between", "the north star". The metaphor adds no information and announces
significance instead of showing it.

Caught live, in this project. The author, on a spec sentence written for these
very decks:

> stan is the through line is the kind of classic LLM language that i don't
> use and edit out

**Grep.**

```
rg -ni --glob '*.qmd' \
  'through.?line|the spine|backbone|the thread|at the heart|north star|the glue|the linchpin|the engine (of|behind)|the connective'
```

**Example A.** Written in `notes/spec-delays.md`, flagged by the author,
removed:

> **Stan is the through-line.** `primarycensored` ships Stan functions,
> `epidist` fits through `brms` to Stan, and `epinowcast` is Stan. So rungs 5
> to 7 are all one backend.

Rewrite chosen:

> Rungs 5 to 7 all fit with Stan. `primarycensored` ships Stan functions,
> `epidist` fits through `brms` to Stan, and `epinowcast` is Stan. Each
> package inherits the constraints of the one backend.

The facts are identical. The metaphor and the announcement of importance are
gone, and the sentence now states the relationship directly.

**Example B.** Same file, same pass:

> The Stan pain is no longer the spine of the talk.

Rewrite chosen:

> The Stan work is no longer what the talk is mainly about.

**How to fix.** Say the relationship plainly. "A runs through B" becomes "B
uses A". "At the heart of" becomes "central to", or more often just delete the
phrase and let the sentence assert the thing. If the metaphor is load bearing,
the sentence was not doing its job.

## 17. The promise tail

**Definition.** A title or bullet that finishes with ", and what/why/where it
<verb>", promising significance instead of stating content. "The switch to a
fixed rule, and what it cost". "What we said we would build, and where it got
to". The tail says "there is a lesson here" without saying what it is.

Caught by the author on the delays talk page:

> This from the delays project page is a classic LLMism I would not use in my
> own writing i.e. my seabbs.github.io: "The switch to a fixed rule, and what
> it cost."

**Precedent check, which is what settles it.** Searched every delivered deck
for titles matching `^#{1,2} .*, and `:

- `how-to-serial-interval`: **zero**.
- 40 minute composability deck: one, "The gap: timely, rigorous, and
  collaborative evidence". A rule-of-three list, not a promise tail.
- `how-I-llm`: one, "Why the terminal, and not an IDE". A plain contrast.

So he has never used the promise tail, and the construction is an invention of
this project.

**Grep.**

```
rg -n --glob '*.qmd' ', and (what|why|where|how) (it|that|they|we|this|the)'
```

**Not the same thing, and fine.** A contrast between two named things, where
both halves carry content: "Why the terminal, and not an IDE", or
"What the move fixed, and what it did not" in
`delays/_partials/90-summary.qmd`, where the slide really does cover both
sides. The test is whether the second half names something. "and what it did
not" names the other half of a comparison. "and what it cost" names nothing.

**Examples and rewrites, all from this project.**

`delays/index.qmd`: "The switch to a fixed rule, and what it cost." became
"The switch to a fixed quadrature rule, so gradients trace through every
backend." The cost is now stated rather than advertised.

`roadmap/_partials/01-what-we-wanted.qmd`: the section divider "What we
wanted, and why the obvious route was hard" became "What we wanted". The
following slides make the case.

`roadmap/_partials/90-summary.qmd`: "What we said we would build, and where it
got to" became "What we said we would build". The diagram beneath already
shows where it got to.

## 18. The maxim, and the nominalised cost

Two related flourishes, both cut by the author on sight.

**18a. The maxim.** A short general truth appended to a specific point, as
though the slide had earned an aphorism. He cut:

> In the paper I wrote that NumPyro and JAX are promising, with barriers for
> epidemiological modellers, and that I find them ugly. **Taste is not an
> argument**

His instruction was simply "cut: Taste is not an argument". The specific claim
stays; the maxim goes. Related shapes: "the tool is not the problem", "that is
a choice, not a constraint", "the map is not the territory".

**18b. The nominalised cost.** Turning a plain consequence into an abstract
noun with a dramatic copula. He cut:

> Eleven breaking releases in nineteen months, v0.35.5 to v0.46.0. Our
> migration was one rename. **The cost is the tracking**

Rewritten to just the fact:

> Eleven breaking releases in nineteen months, v0.35.5 to v0.46.0

The family: "the cost is X", "the price is X", "the real work is X", "the
problem is not X, it is Y". Each announces an insight instead of stating one.

**Grep.**

```
rg -n --glob '*.qmd' \
  '\b(the (cost|price|real work|hard part|difficulty) is)\b|is not (an argument|the problem|the point)'
```

**How to fix.** Delete the sentence. Almost always the sentence before it
already carried the content, which is why the flourish felt available.

## What he does not cut

Do not over-correct.
These survive every pass and should be left alone.

- Blunt admissions against interest.
  "it needs an eye on it, and is not clearly a good idea" (`SI 28515cc`);
  "I do not have a defence for this. I am part of the problem"
  (`LLM eac9c73`).
- Short verbless fragments after a full stop.
  "Small, verifiable, tedious."
- First-person opinion when it is flagged as opinion.
  "In my view", "My guesses".
- Concrete numbers with a source, and dated caveats on figures.
- Attribution and citation lines.
  These get longer, not shorter, over the history.
- Plain "as we have seen" back-references to an earlier slide in the same
  deck; the author kept one in `SI 06-composed.qmd`.

## Working checklist for a slide

1. Does any sentence exist to say the previous one mattered? Cut it.
2. Does any sentence end in a clause the sentence did not need? Cut it.
3. Does the first bullet restate the heading? Cut it.
4. Is there a list of three where two would do? Cut one.
5. Is anything defined by what it is not? Say what it is.
6. Is any adjective carrying the claim? Cut it and see.
7. Can every number be traced to a repo, an API, or a registry? If not,
   delete or verify it.
8. Would a figure, an equation, or five lines of code say it better than
   the callout? Replace it.
