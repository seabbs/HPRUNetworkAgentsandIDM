# The steers

Follow-up instructions given during the build, in order, with typos corrected.

---

> I am thinking a slide on each title for starters.

> We don't just want pictures/figures etc. from our own work, and anything
> we have needs a short cite.

Use figures from other groups' work as well as ours.
Every figure, ours included, carries a short citation in its attribution.
Short means author, year and venue or link, as in the AIandIDVUB keynote
after Sam asked for shorter references there.

> You can commit to main as we work.

> One of the things they can do is implementation, optimisation (code,
> theory, custom adjoints (but technical, gradients?)), review, rubber duck
> model development. Free up time for review etc.

> BVDOutbreakSize shows dangers. Hard to keep track of, their push for
> very complex nested models and code. Hard to review. Don't write models
> etc. like a human, which makes them hard to parse.

> One thing they also do is make modelling infrastructure, i.e. the workflow
> easier, model checks etc.

> Tool use for agents?

Read as: the agent slide should say what the tools are.

> How to collaborate in an agent-driven environment: add a slide at the end,
> prior to the summary. We are finding it very hard.

> Err, the bot thing sounds a bit specific and weird for this more general
> talk.

Read as: drop the bot-written issues bullet from the collaboration slide.

> I really like this article about the user contract, and science has some
> analogues:
> https://productpicnic.com/archive/thoughtless-changes-overwhelm-our-users-and-its/
> I saw similar ideas about what to do with the time agents free up, i.e. not
> just add more and more incremental science but big-picture thinking, review,
> deep dives etc.?

Read as: the collaboration slide takes the article's point that changes are
cheap to make and as costly as ever to check. The summary says what to do with
the freed time.

> No, we don't want the article in there, just some of the points I like as
> mentioned.

Read as: keep the points, drop the citation and link to the article.

> In general it looks like "checking them costs" should be its own bullet.
> Same for similar statements like this.

Read as: one statement per bullet across the deck. Label-led bullets
("Reading data. Agents read ...") stay as they are.

> Resources on the home page should have our other AI talks from recent
> stuff, I think, and something about our recent science?
> i.e. primarycensored, EpiNow2 etc. maybe?

> The date for this is tomorrow.

Read as: 3 November 2026.

Issue #3, closed by Sam: "I am presenting all of it."

> Challenges, not dangers.

Read as: rename the Dangers section, its slide and the talk-plan entry.

> Remove this slide: "Ebola disease, Democratic Republic of the Congo". We
> need to add scenarios to "used for" with an example, i.e. from Nick Davies'
> work?

Read as: drop the Bundibugyo slide, and add a scenarios panel from Davies
et al. 2020, Lancet Public Health, to the used-for montage.

> For "what is a model" we need to have not the workflow, I think. This is
> kind of fluff, cut: "Fitted to data that arrive late, incomplete and
> changing". Hmm, we need to have a bit more on models in general: a
> parsimonious representation of domain knowledge trying to answer a question
> of interest, or similar?
> You can look at the workflow paper itself. Reminder: we have it in
> code/seabbs.

> For "what is an agent", get rid of that schematic and have one to highlight
> what a tool-using LLM actually is. Get an agent to make it.
> Have skills, context and MCP in the schematic.
> The harness clearly there.
> Some layer on multi-agent models? Maybe a second slide: agents working in
> concert, dispatching agents, Claude Code workflows etc. In the first slide,
> have logos of some common agent harnesses?

> Remove: "Others go further. EpidemIQs runs from a question to a written
> report". I think how much work, and how autonomously, agents should do is an
> open question. Currently a human in the loop at quite an involved level
> seems to be very needed for most tasks.

> What agents do needs a picture of a rubber duck.

Read as: a rubber duck photo on the Where slide, by the rubber duck bullet.

> They won't know what CI is, and that is a bit specific. Model checking
> infrastructure: make it more general?

> Here too specific: "Agents read the French DRC situation reports and
> digitise the onset figure".

> I like the specific examples and the schematic in "Implementing,
> optimising", but the examples need to be a bit more general, i.e. "custom
> ...", not "in primarycensored".

Read as: general wording in the bullets, specific pull requests stay in the
citations.

> The answer to "what can they be used for", the first bullet, should I think
> be something like "many of the tasks that are often assigned to early career
> researchers".

> "BVDOutbreakSize ..." is too specific in Dangers.

Read as: a general first bullet on Challenges, and no #779 label on the chart.

> Rather than code lines, can we show some complex agent code? Odd bugs, but
> not too in the weeds, that sort of thing?

> Collaboration and training are other challenges, and of course all
> currently very heavily subsidised.
> What happens when having to pay true costs?

> Shouldn't this be in "what can agents do", not after dangers: "Google's
> tree ..."

Read as: move the tree-search slide into the Where section, after
Implementing.

> Does that slide have an accurate heading? Can we make the role of the
> domain experts checking their process, i.e. the Funk paper, a little
> clearer and more nuanced?

Read as: retitle the tree-search slide without "Google" or "topped", and
tell it in order. Retrospective claim (Aygün), leakage found by domain
experts (Bracher and Funk), then the prospective result (Martinson).

> Also the building on existing domain expertise a bit clearer?

> We could also have a nicer and better version of our outbreak response
> model as a slide, as an example of what you can do, perhaps?
> After the Google one?

> This is not a good slide: "How to collaborate in an agent-...". It should
> be some reflections in more detail on why it is hard, i.e. the volume of
> changes, understanding what is output from a person and what from an LLM.
> Different levels of access to agents.
> That kind of thing.

> We don't have anything about how to use the time they give us? i.e. a slide
> with a header? Something like: the challenge is the push to do more of the
> same work, but really a different kind of work, i.e. review, deep dives,
> big-picture thinking etc.? How to train for that kind of work? Build tools
> to make agents work better: do they look different from the kinds of tools
> and methods we have built historically?

> Challenge: a rapidly changing field, i.e. a bubble. What is true today may
> not be true in a few months or next year.

> Cut: "We have not solved it".

Read as: the summary says collaborating through agents is hard, and stops there.

> Cut: "They get things wrong, and retrospective scores can leak". New
> bullet: "They get things wrong in ways that humans wouldn't, and these
> errors can be hard to spot."

> Look at the latest BVDOutbreakSize work. Look at the remote and update this
> box's copy, and get some nicer plots, maps etc.

Read as: fast-forward the local BVDOutbreakSize clone, and take the map and
plots from the dev report (data to 25 October).

> Ah, the agent schematic needs to have where it is running, i.e. your
> computer, the cloud, an HPC etc., which changes data access, tools and
> compute. Need to have something on confidential data access in Challenges,
> ideally a local agent etc.?

#5, Sam: "Yeah, we need some kind of domain-specific testing and evaluation,
access, training, yes."

#4, Sam: "Make sure it's one sentence a line, short and concise, not
overblown, and based on what we have in the slides."

> The abstract is a bit too sparse, and not how a human would write: flowing
> text whilst being concise.

Read as: flowing prose, still one sentence per line. Lint no longer wraps
lines inside the abstract block.

> I think how we use the time is part of using agents, not the ending, no?

Read as: the freed-time slide moves to the end of the Where section, out of
the talk plan, and the summary and abstract follow.

> Equity is a challenge.

> Ah, maybe I am wrong. Keep the "how we should use the time" story point
> and slide.

Read as: undo the move. The freed-time slide is its own section again,
before Summary.

> "...what we know about a disease" -> "disease transmission"?

> You cite the workflow paper but don't show it in the first slide. Planning
> to show it? Yes, I think?

Read as: show Fig. 2 of the workflow paper under the Davies model on the first slide.

> Replace "How infections spread ..." with i.e. "nested in a wider modelling
> workflow"?

> "What are infectious disease models used for", not "is"?

> Correct my typos in any copied-in prompts.

> An ending slide before the links and thanks, or add a link to the prompts
> that built these slides, with an image of seabbs-bot?
> And maybe sbfnk-bot?

Read as: a prompts page from these notes, linked from the closing slide
with both bot avatars.

> Cut the agent-based model, i.e. ABM, two bullets. Add a bullet on examples
> of what tools are. Need to, i.e., define context.

> "Building infrastructure ...", not "the" before it.

> How much an agent should do is a challenge point for infectious disease?

Read as: move the autonomy pair from the Where slide to Challenges.

> What can it do is missing, i.e. optimisation, maths, i.e. analytical
> solutions, differentiating code etc., candidate model permutations and
> proposals. Managing complex experimental workflows.

> "Spec": write it out as "specification".

> Here, "Implementing, optimising and reviewing": change to "How we use agents
> to develop EpiNow2", with links? Check that code base. Both have agents,
> i.e. seabbs-bot and sbfnk-bot pictures? Cross-check each other, my review
> bot etc.

> "An agent that writes ..." is a bit informal. It should refer to the Google
> paper or its title, or be a little more formal?
> Same with the title for our outbreak modelling.

Read as: the tree-search slide is titled after the system, Empirical Research
Assistance, and the outbreak slide after the report.

> A bullet on the agent-built dashboard, forecast evaluation allowing for
> real-time evaluation, and the infrastructure built to allow public-domain
> fitting and model checking?

> Challenges: cut the code example. Can we make it a bit more visually
> interesting, groups of challenges, coloured boxes etc.?
> Some kind of meta-challenges with the current bullets in them etc.

> This is good, but the figure is boring. A few more interesting figures for
> "collaborate in an ...".

> A schematic for this slide? Should we use the ... i.e. "use time"? The pull
> in a callout? Training in a callout at the bottom.
> Review, deep dives and technical debt reduction, generalising,
> interoperating? Any other kind of work we could be doing, thinking about
> utility and how to evaluate what works and what doesn't. Collaboration.

> The summary needs some meta-organisation as well.

> The summary needs cutting down, five points at most.

> Put photos of me and Seb in the thank you, and then our agents in a 2 by 2.

> Make sure to cite this somewhere: "How should we use the ...", i.e.
> https://productpicnic.com/archive/thoughtless-changes-overwhelm-our-users-and-its/

Read as: cite the article on the freed-time slide.

> Training in a callout at the bottom.

> In "how we built it", can you summarise somewhere the tools you called,
> how many, how many turns etc.?

> Split this into two slides, models then workflow? ("What is infectious
> disease modelling?")

> "How we use agents to develop EpiNow2" is missing the pictures of our
> review bots.

> Here, "Ebola disease in the DRC ...": it is situational awareness of?

> Here, "One model fitted to all the surveillance streams": extracted from the
> publicly available situation reports.

> "Agents built the dashboard": here also maintain an interactive dashboard,
> with features added as users ask for them.

> Last bullet or callout: this work is an experiment in agent-driven outbreak
> modelling, meant as an external viewpoint or similar? It represents both the
> potential benefits and dangers of agent-driven work.

> It is not "when" here: "when access to agents ..."

> "What should we be training people to do" is better than just "Training" as
> a flat statement.

> "How much to hand over" needs a models-changing-quickly bullet: rapid
> improvement in the last year.

> Here, some kind of firehose picture ("How to collaborate in an
> agent-driven ...") to make it a bit more interesting, in the bottom left?

> "Interoperating" is not a word: making work interoperable?

> Talking to stakeholders as something else we should do?

> Meta-groups on this slide: "Where can agents be used ..."

> EpiNow2 needs a bullet on what it is, i.e. used by public health agencies,
> and a bullet on development being a challenge, as it is hard to get
> traditional research funding.

> Not sure we need: "They fix bugs, simplify code, and add tests and
> benchmarks".

> This is in the schematic? "Review bots read each pull request first", so no
> repeat?

> Can we break this into what, and why it is important? ("Empirical Research
> Assistance ...") The Google model slide has too much text in a wall.
