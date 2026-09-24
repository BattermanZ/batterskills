---
name: ask-me
description: Ask which skill or flow fits your situation. A router over the batterskills catalogue.
disable-model-invocation: true
metadata:
  version: "1.3.0"
---

# Ask me

You don't remember every skill, so ask.

A **flow** is a path through the skills. Most paths run along one **main flow**, and three **on-ramps** merge onto it. Everything else is standalone, or a vocabulary layer that runs underneath. Past engineering, buying something has a short flow of its own, and the vault, writing and UI skills are picked by situation (see Beyond engineering).

## The main flow: idea → ship

The route most work travels. You have an idea and want it built.

1. **`/grill-with-docs`**: sharpen the idea by interview. Start here whenever you are **working in a working directory**: it's stateful, retaining what it learns in `CONTEXT.md` and ADRs. (No working directory? Use `/grill-me`, covered under Standalone. Both run the same `/grilling` primitive; `grill-with-docs` is the one that leaves a paper trail, which makes it the better of the two whenever a repo is there to leave it in.)
2. **Branch: can you settle every question in conversation?** If a question needs a runnable answer (state, business logic, a UI you have to see), detour through a prototype, bridged by **`/handoff`** in both directions (a prototype lives in its own directory, which is exactly what `/handoff` is for; see Phase boundaries):
   - **`/handoff`** out, then open a fresh session against that file,
   - **`/prototype`** to answer the question with throwaway code,
   - **`/handoff`** back what you learned, and reference it from the original idea thread.
3. **Branch: is this a multi-session build?**
   - **Yes** → **`/to-spec`** (turn the thread into a spec), then **`/to-tickets`** to split it into tracer-bullet tickets, each declaring its **blocking edges**. On a local tracker that's one file per ticket under `.scratch/<feature>/issues/`, worked blockers-first by hand; on a real tracker the edges become native blocking links, so any ticket whose blockers are done can be grabbed. Kick off **`/implement`** per ticket, **`/clear`ing context between each one**. Each ticket is self-contained, so the last one's context is disposable.
   - **No** → **`/implement`** right here, in the same context window.

   Either way, **`/implement`** claims one GitHub issue through `gh`, drives **`/tdd`** internally (one red-green slice at a time), runs **`/code-review`** over the complete change, and fixes the findings. It then proves the reviewed code against the live test environment documented in `AGENTS.md`, completes the GitHub issue checklist, commits, pushes, and closes the issue. With no argument it takes the oldest unassigned, unblocked `ready-for-agent` GitHub issue. Reach for **`/tdd`** on its own when you just want to build a concrete behaviour test-first without a full spec, and **`/code-review`** on its own whenever you want to review a branch, PR, or working tree against a fixed point.

### Context hygiene

Keep steps 1–3 in **one unbroken context window**, with no compact or clear until after `/to-tickets`, so the grilling, spec, and tickets all build on the same thinking. Each `/implement` then starts fresh, working from the ticket.

The limit on this is the **[smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**: the window (~150k tokens on state-of-the-art models) within which the model still reasons sharply. If a session approaches it before `/to-tickets`, don't push on degraded: `/compact` at the nearest phase boundary and carry on (see Phase boundaries).

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Bugs and requests piling up** → **`/triage`**. It moves issues through triage roles and produces agent-ready issues, which **`/implement`** later picks up.

  Triage is only for issues **you didn't create**: bug reports, incoming feature requests, anything that arrives raw. Tickets that `/to-tickets` produced are already agent-ready, so **don't triage them**.

- **Something's broken** → **`/diagnosing-bugs`**. For the hard ones: the bug that resists a first glance, the intermittent flake, the regression that crept in between two known-good states. It refuses to theorise until it has a **tight feedback loop** (one command that already goes red on *this* bug), then fixes with a regression test. Its post-mortem hands off to **`/improve-codebase-architecture`** when the real finding is that there's no good seam to lock the bug down.

- **A huge, foggy effort (a greenfield project or a huge feature build, too big for one session)** → **`/wayfinder`**, the most cognitively demanding flow here. When the way from here to the destination isn't visible yet, it charts a **shared map** of **decision tickets** on the issue tracker and resolves them one at a time, producing **decisions, not deliverables**, until the fog is pushed back and the way is clear. Where **`/grill-with-docs`** sharpens an idea you can hold in one session, wayfinder is for the idea you can't. It's slower and denser, so save it for exactly that, never a well-scoped feature.

  When the map clears, **it hands off, it doesn't build**: merge onto the main flow at **`/to-spec`**, which collapses the map's linked decisions into a buildable plan, then `/to-tickets` and `/implement` as usual. Looping the map straight into `/implement` skips that collapse and throws the linked detail away. Go straight to `/implement` only when the effort turned out genuinely small.

## Codebase health

Not feature work: upkeep.

- **`/improve-codebase-architecture`**: run whenever you have a spare moment to keep the codebase good for agents to operate in. It surfaces **deepening opportunities**; picking one _generates an idea_ you can take into the main flow at `/grill-with-docs`. It's the survey that finds the candidates; **`/codebase-design`** (below) is the bench you design the chosen one on.

## Vocabulary underneath

Two model-invoked references that run *beneath* the other skills, each the single source of truth for its vocabulary. Reach for them directly when the **words**, not the process, are the problem; or let the skills above pull them in.

- **`/domain-modeling`**: sharpen the project's *domain* language: challenge a fuzzy term, resolve an overloaded word ("account" doing three jobs), record a hard-to-reverse decision as an ADR. It's the active discipline `/grill-with-docs` drives to keep `CONTEXT.md` a clean glossary.
- **`/codebase-design`**: the deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality) for designing a module's *shape*: a lot of behaviour behind a small interface at a clean seam. `/tdd` and `/improve-codebase-architecture` both speak it.

## Phase boundaries

A **phase** is a chunk of work inside a session: the grilling, the implementation, the QA. At the **boundary** between two of them you have five options, and picking between them is the fuzziest decision in this whole map:

- **Continue**: stay put. Costs nothing, loses nothing.
- **`/clear`**: empty the window, when nothing here matters to what's next.
- **`/handoff`**: write a portable markdown file. Narrow: only for a **new harness**, a **new directory**, a **colleague**, or forking a side task **mid-phase**. What it buys is portability.
- **Subagent**: send a tightly-scoped task to its own window and get a report back.
- **`/compact`**: compress this context and seed a fresh session with it. The **default**, at the bottom of the tree rather than the first reach.

Read [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) for the ordered tree: the five questions, the reasoning behind each branch, and why the primary-source cost makes **Continue** the one to rule out first. Make the decision **at** a boundary; mid-phase, continue or split the rest into subagents.

## Standalone

Off the main flow entirely.

- **`/grill-me`**: the same relentless interview as `/grill-with-docs`, but **stateless**: it saves nothing locally and builds no `CONTEXT.md`. Reach for it when you are **not working in a working directory**: sharpening a plan, a design, a piece of writing, anything with no repo under it. If you are in a working directory, use `/grill-with-docs` instead: it runs the same interview and leaves a paper trail, so it is strictly the better one.
- **`/grilling`**: the interview primitive itself: one question at a time along the frontier, facts are the agent's job and decisions are yours. `/grill-me` and `/grill-with-docs` are the two named ways in, and `/triage`, `/wayfinder` and `/improve-codebase-architecture` all run it internally. Reach for it directly only when you want the interview with no wrapper around it.
- **`/resolving-merge-conflicts`**: work an in-progress merge or rebase conflict hunk by hunk, resolving by **intent** traced to each side's primary source rather than by picking lines, then finish the operation. It never runs `--abort`. Standalone and off every flow: reach for it when you are already mid-conflict.
- **`/prototype`**: a small, throwaway program that answers one design question: does this state model feel right, or what should this UI look like. Throwaway is a constraint on how the code is written, not a promise to destroy it: the answer folds into the real code, and the prototype itself is kept as a **primary source** on a `prototype/<name>` branch out of main, pointed at from the implementation issue. It's the detour in step 2 of the main flow, but reach for it any time a design question is hard to settle on paper.
- **`/research`**: delegate reading legwork to a **background agent**: it investigates a question against **primary sources**, then leaves a cited Markdown file in the repo. Keep working while it reads. The file it produces is something to take *into* the main flow at `/grill-with-docs`; research feeds the thinking, it doesn't replace it.
- **`/to-questionnaire`**: when the thing blocking you isn't in your head or the codebase but in **someone else's**, this writes them a questionnaire to fill in. It's the inverse of `/grill-me`: instead of interviewing you about the subject, it interviews you about the **send** (who it's going to, what you need back) and aims the questions at the gap. What comes back is material for `/grill-with-docs` or `/to-spec`.
- **`/wizard`**: for the steps only a **human** can take: provisioning infrastructure, setting up credentials or CI secrets, clicking through an unfamiliar third-party dashboard, running a one-off migration or cutover. It generates an interactive bash script that opens each URL, captures each value, and writes it into `.env` and GitHub secrets, so the procedure stops being something you re-explain to an agent every time. Model-invoked, so the agent reaches for it the moment it hits a wall only you can pass. If the agent could just do it itself, it should; this is for where a human is genuinely in the loop.
- **`/wait-what`**: the corrective for a message that didn't land. Use it mid-conversation, inside any other skill, and the agent re-pitches what it just said with the context you were missing, in plain English, using the `CONTEXT.md` vocabulary. It works after the fact; `/grill-with-docs` is the upfront cure, because a shared language agreed early is what stops the jargon arriving at all.
- **`/teach`**: learn a concept over multiple sessions, using the current directory as a stateful workspace.
- **`/writing-for-agents`**: reference for writing documents agents consume: skills, AGENTS.md, pointed-at docs.

## Precondition

The engineering flows assume the target repo declares its issue tracker and triage labels in `docs/agents/issue-tracker.md`. When that file is missing, ask which tracker to use before publishing tickets. The personalized `/implement` workflow uses GitHub through `gh`.

## Beyond engineering

The catalogue reaches past the main flow into four more trees: buying, the vault, writing, and UI. None of them runs through `/grill-with-docs` or `/implement`. Buying has a flow of its own; the rest are single skills you pick by situation.

Most of these are **model-invoked**: the agent reaches for them the moment the request fits, so describing the job is enough. The four marked **user-invoked** below never fire on their own, and you type them.

### Buying something: decide → seller → discount

A three-step chain, all user-invoked. Join at whichever step you are already at.

1. **`/purchase-advisor`**: you know the kind of product (a TV, a stand mixer) but not which one. It scans the category before asking anything, so the interview asks this category's questions: around six, one at a time, each with a recommended answer. It won't hunt while use, budget, dealbreakers or location is still a guess. Before hunting it checks the **constraint cost**, whether one of your requirements pushes the search into a corner of the market nobody has reviewed, and if so offers you the trade. One subagent hunts (two when the used market can pay for itself), every shortlisted listing is re-fetched live, and the run ends with **one recommendation**, a few "pick this instead if..." alternatives, and a verdict on buying second-hand. It saves the run as an effort (in the vault here, under `personal/purchases/<Product>/`), so a second-hand hunt that takes weeks resumes where it stopped instead of re-interviewing you.
2. **`/price-hunt`**: the product is chosen and the job is the seller. It pins the exact article number or EAN, builds the **basket** (the product plus whatever your spec needs that the box doesn't contain), and ranks sellers by **landed cost**: basket, delivery, and import VAT, duty and handling wherever the parcel crosses a customs border. It covers the home market in full, probes once across the EU, once beyond it, and once second-hand, and runs a trust check on every seller before any can be recommended. It asks at most one question and saves nothing. Give it a category, or two products to weigh, and it sends you back to `/purchase-advisor`.
3. **`/batterdeals`**: finds published discount codes for that shop and tests them in a real guest cart in front of you, then leaves the best code applied and the cart open for you. It never enters payment details, never guesses codes, and stops at 15 attempts. A bare shop domain gets recon only, since testing needs a product URL. "No code works, but the sale already saves you X" is a normal result, not a failure.

A price watch is `/loop` over `/price-hunt`, not a mode of it. A second-hand pick skips steps 2 and 3: haggling stays with you.

### The vault

Every vault skill reads and writes BatterNotes through the Hatchdoor MCP tools, never the filesystem, and every one of them loads **`/hatchdoor`** first.

- **`/hatchdoor`**: any read or write in the vault. Before a change it reads the vault's "Operating Rules" note (filing, tags, links), picks the note's shape from the Markdown showcase, and searches before creating so it updates a note rather than duplicating it. A quick capture holds what you said and nothing inferred. It never moves, renames, archives or deletes unless you ask.
- **`/clip-web-article`**: archive an article with its images stored in the vault rather than hotlinked, each in its original position with its own photo credit. It checks the extracted text against the page, because the extractor has silently dropped whole sections. Not for general note-taking; that's `/hatchdoor`.
- **`/deep-research`** (user-invoked): a question big enough for three or more lines of enquiry that don't overlap. The coordinator interviews you (four questions at most), shows a plan of clusters and source tiers and waits for your yes, then runs one agent per cluster, one at a time, verifying each while it is still warm. It all lands in the vault as one effort folder: a Brief, an Evidence note, an optional Practical checklist, and a ranked Sources to obtain list. A question with one line of enquiry gets answered directly and spawns nothing. It is slow and expensive by design. A technical question about code, APIs or specs goes to `/research` instead, which writes one cited file into the repo.
- **`/sci-hub`**: the follow-up to a "Sources to obtain" or "could not fetch" list. It works a ladder (open-access copy, supplementary files, Sci-Hub mirrors, the publisher's site in a real browser) and finishes only when every source is a verified file on disk or has a written reason it can't be had. Guidelines are a website problem rather than a paywall one and get their own branch. Files land raw in a scratchpad; take them back to `/deep-research` as a source-upgrade pass on the same effort.
- **`/wayfinder-vault-tracker`**: where a `/wayfinder` effort lives when its subject isn't code (household, hardware, life, fleet decisions). The map, tickets and research notes go under `wayfinder/<effort>/` in the vault; an effort about code keeps its repo tracker. Run these sessions from `~/coding/wayfinding`. It loads itself once `/wayfinder` starts on a non-coding subject.

`effort-store` and `effort-store-vault` are plumbing, not entry points: `/purchase-advisor` loads them to find and save its efforts.

### Writing

The `unslop` rules cover all prose, always. Hooks inject them, so don't invoke the skill by hand.

- **`/documentation-writer`**: software docs, split the Diátaxis way into tutorial, how-to, reference or explanation. It pins down the type, audience, goal and scope first, proposes an outline, and writes only once you approve it.
- **`/writing-project-readmes`**: write, tighten or audit a README for an app, CLI, service or library. It treats the README as the front page: a pitch that names the differentiator, who it's for and who it isn't, a quick start matching the defaults, and troubleshooting written from the symptom. It also answers "is this README any good" against its rubric.

For skills and `AGENTS.md`, use `/writing-for-agents` (under Standalone).

### Building UI

- **`/frontend-design`**: visual direction for a new UI or a reshaped one. It plans a small token system first (palette, type, layout, one signature element), checks that plan against the three looks AI-made design keeps landing on, and builds only once the plan is specific to your brief. A throwaway UI that answers a design question is `/prototype` instead.
