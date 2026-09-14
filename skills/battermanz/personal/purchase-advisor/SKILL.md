---
name: purchase-advisor
description: Decide what to buy: research the category, interview you, hunt new and second-hand, recommend one.
disable-model-invocation: true
---

# purchase-advisor

Version 1.1.0.

Someone wants to buy a specific kind of product (a TV, a stand mixer, a computer) and does not yet know which one. The run moves through scan, interview, constraint cost, hunt, verify, recommend, and ends with one recommendation they can act on today. Choosing is the job: a run that hands back a neutral pile of candidates has pushed the hardest part onto the user.

Storage goes through the `effort-store` skill. Load it before writing anything. Declares: root `purchases`; notes `Requirements`, `Buying guide`, `Shortlist`. The effort name is the product in a few words: `Stand mixer`.

## 0. Resume or start

**find** the product in the effort store before anything else. If an effort exists, offer to resume: the requirements and buying guide stand. Ask what has changed since; a moved budget or requirement reopens the interview for that field only, and **update** writes the new answer into Requirements as a dated section before the hunt launches. Location is re-asked on every resume regardless of what else changed; it is never carried forward from the saved note. The run then re-enters at the hunt with the criteria as updated, and **update** adds the new results to the Shortlist note as a dated section above the old ones. Second-hand hunts especially span weeks; the saved effort is what makes waiting cheap.

## 1. Scan

Cheap and in-session: a few searches and reads to learn the category before asking the user anything, so the interview asks the questions this category deserves rather than generic ones. No subagent; the expensive search comes later, once it can be fully constrained.

Come out holding four findings:

- The dimensions that genuinely separate products in this category, and the ones that are marketing.
- The price tiers: what more money actually buys, and where the returns go flat. These are the scan's estimate from a handful of pages, not the market's real floor, and the hunt reports the real one.
- The **second-hand verdict**: whether second-hand is a smart way to buy this category, and why. A mixer built to last decades points one way; a used OLED TV with burn-in risk and no warranty points the other. The verdict reaches the final report whichever way it points; the user decides with it, not under it.
- The **spec mapping**: how the user's stated requirement probably translates into something searchable, plus the words the market itself uses for it in the language of their country. Write it down as a hypothesis. It reaches the hunt as a lead and never as a filter, because a scan that guesses the mapping wrong aims the whole hunt at the wrong corner of the market and no later step catches it. The hunt's job is to test the mapping, not to inherit it.

Done when you can write the buying guide and name the interview questions that would change the hunt.

## 2. Interview

One question at a time. Ask, wait for the answer, then ask the next, with a recommended answer attached to each question. Around six questions is the target, scaled to the purchase: a TV earns six, a kettle earns two. Ask only what changes the hunt.

The target paces, it does not truncate. Four fields are load-bearing and the hunt never launches while one is a guess:

- **Use**: what this thing will actually do, day to day.
- **Budget**: a number or a range, asked plainly.
- **Dealbreakers**: hard vetoes, including "new only" if second-hand is out for reasons of their own.
- **Location**: city and country, asked every run, plus whether pickup radius or delivery bounds the search. When the effort store's adapter supplies a default location, offer it as the recommended answer to confirm rather than asking cold.

Each load-bearing field is either answered by the user or stated as an assumption they explicitly confirmed. Everything else may be assumed and stated.

Then **open** the effort and **write** Requirements (the answers, the confirmed assumptions, date, skill version) and Buying guide (the scan's findings, the spec mapping marked as a hypothesis) before the hunt starts. They are the recovery anchor, and the hunt brief quotes them.

## 3. The constraint cost

Cross the answers with the scan and ask yourself one question before dispatching anything: does a stated requirement, alone or crossed with another, shrink the field to a corner where the good products are not?

If it does, say so in a few sentences and offer the trade as a question with a recommended answer: keep the requirement and accept a thin, under-reviewed field, or relax it and open the part of the market that is actually reviewed. Name what relaxing costs them in daily use, in concrete terms, and name what keeping it costs them in evidence. A requirement the user reaffirms is hunted exactly as given, and the hunt brief says the market is expected to be thin.

Also check that the requirement buys what the user wanted it to buy. A cleaning-effort requirement that lands on a material which needs scrubbing has inverted itself, and the scan is where that becomes visible.

Most runs pass this step in one sentence. Do not manufacture a trade where the requirements are comfortable. This step exists because a run that notices a doomed box, mentions it in passing, and hunts it anyway spends its whole budget reaching a product nobody has ever reviewed, and leaves the user to ask the question the skill should have asked.

Done when either no requirement collides, or the user has answered the trade.

## 4. Hunt

ONE subagent does the whole hunt and returns a vetted candidate list, so the listing-site noise stays out of this session.

Split into two agents, new retail and second-hand, only when the used market can pay for itself: the scan's verdict says the category rewards buying used **and** the likely saving is big enough in absolute money to be worth a stranger, a possibly missing accessory and no warranty. A few hundred off a television earns the second agent. Twenty euro off a €95 appliance does not, whatever the second-hand verdict says on its own; report the verdict to the user and hunt new retail alone. Never more than two agents.

Pin the subagent's model explicitly in the dispatch, to the model this session's `CLAUDE.md` / `AGENTS.md` rules name; an omitted model silently inherits the session's. Each brief carries, in so many words:

- The Requirements and Buying guide, quoted verbatim.
- The spec mapping, labelled as the scan's hypothesis, plus the instruction to test it rather than search only inside it. The hunt searches the user's requirement in the market's own words and language, against the spec sheets of the brands that lead the category, as well as searching the corner the scan predicted. A mainstream product whose maker states the requirement in writing is the single most likely thing for a hypothesis-driven hunt to walk straight past.
- **Evidence is a deliverable, not a bonus.** For each candidate: what independent evidence exists that the thing works, with the number attached. Search the consumer organisation of the user's country and its neighbours by name (Consumentenbond, Stiftung Warentest, Which?, UFC-Que Choisir, CHOICE), since a category's only real test is often published one border away. Aggregated user ratings count with their sample size. What does not count, and must be named as not counting: retailer copy that reproduces the maker's own sentences, "best of 2026" listicles, affiliate pages carrying shop boxes, and any page borrowing a consumer organisation's name without being it. "No evidence found" is a finding and must be reported as one.
- **A rejection carries its source.** Any candidate ruled out on a spec claim needs the quote and the URL that rules it out, exactly as a recommendation does. A brand dismissed without its own page being read is reported as unchecked, never as failed.
- Where to search: shops that deliver to the location, plus the second-hand marketplaces local to it. The agent works out which those are for this country.
- "Work alone with your own web search and fetch tools; spawning agents or subagents is forbidden."
- Any web-tool guidance this session's `CLAUDE.md` / `AGENTS.md` carry: search them for the web search and fetch rules and paste the section into the brief verbatim, or state in the brief that there is none. A subagent inherits none of it.
- What to return: up to ten candidates ranked best fit first, each with name, asking price, source link, condition (new or second-hand), its evidence, and the one reason it fits these requirements; plus which shops and marketplaces were searched and came up empty, so a thin list reads as a thin market rather than a thin search.

The second-hand brief carries one more instruction, because listings lie by omission: **read the photographs**. Download a listing's images to the scratchpad, resize them, and look at them. They show coating wear and bare metal a seller calls "good condition", whether the accessories in the box are really in the box, and often the model and rating plate. Voltage is the one that ruins a purchase silently, so when no plate is photographed, say so and make "ask the seller for a photo of the rating plate" the action rather than assuming the local model.

Done when every hunt agent's report is back with each candidate carrying its price, link, condition, evidence and reason.

## 5. Verify

The **shortlist** is the five or six candidates you would actually put in front of the user. Before they see anything, fetch each shortlisted candidate's own page and confirm three things: the listing is alive, the price, and availability at the location. A dead listing is dropped and noted; a drifted price is reported at the live number. Delivery cost and stock depth are part of the price. The hunt agent's report is claims; only what you fetched yourself is measured. Second-hand listings die within days, and recommending a vanished one is the classic failure this step exists to catch.

Verify the load-bearing spec claims at the maker's own document too, not at the shop's bullet list, and treat a clean negative with suspicion: a keyword probe that finds nothing on a page you have not confirmed is the real document proves nothing. Manual-aggregator sites serve plausible "manual not found" templates that answer questions about other products entirely. Confirm you are holding the document before you trust its silence.

Done when every shortlisted candidate has a fetched verdict (alive, price, availability) or is dropped and noted.

## 6. Recommend

**write** the Shortlist note and say the same in chat:

- One recommendation, argued against the requirements: why this one, at this price, from this seller.
- Two to four alternatives, each tagged "pick this instead if ...", new and second-hand mixed in one ranking, each with its live-checked price and link.
- The evidence behind the recommendation, including its absence. A pick that meets every requirement and has never been reviewed is offered as reasoned rather than proven, and says so in those terms.
- The second-hand verdict, even when every pick is new.
- What was searched and not found, and anything that could not be verified.

If the recommendation changes later in the same run, rewrite that pass's section whole, ranking table included, rather than swapping the winning claim and leaving the rest. **update**'s dated-section rule protects a previous run's reasoning, not a paragraph you wrote twenty minutes ago. Re-read the section after the edit: a note that recommends one product and ranks another first is worse than no note. Record the reason the pick moved, especially when the cause was your own criterion rather than the user's.

**register** the effort. Then, when the winner is a new-retail buy, tell the user that `/batterdeals` on the product URL hunts the discount before checkout; it is user-invoked, so they type it. A second-hand listing gets no code hunt; the equivalent move there is negotiating, which stays with the human.

Done when the Shortlist note is written and internally consistent, the effort registered, and the chat carries the same recommendation.
