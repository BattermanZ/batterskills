# Second-hand brief

The brief for step 4's subagent. Pin its model explicitly in the dispatch, to the model this session's `CLAUDE.md` / `AGENTS.md` names for subagents; an omitted model silently inherits the session's.

Before dispatching, search this session's `CLAUDE.md` / `AGENTS.md` for web search and fetch rules and paste that section into the brief where marked, or write in the brief that there is none. A subagent inherits none of it.

Fill the placeholders:

> Find second-hand listings for PRODUCT (pin: PIN) that beat a new landed cost of LEADER_COST, for pickup near or delivery to LOCATION. Work alone with your own web search and fetch tools; spawning agents or subagents is forbidden. Read pages only: no messages to sellers, no offers, no accounts.
>
> The buyer needs this basket: BASKET. Price every listing as that basket: add the cost of anything it lacks, and of any part touching food, skin or milk, since hygiene means buying those new.
>
> Search the marketplaces local to LOCATION. A listing for the same product sold in another region counts; list how it differs from the home version, and write **unknown** for anything the listing does not establish.
>
> Read the photographs. Download each shortlisted listing's images to your scratchpad, resize them, and look at them. They show wear a seller calls "good condition", whether the accessories are really in the box, and often the model and rating plate. When no rating plate is photographed, say so, and make "ask the seller for a photo of the rating plate" the action rather than assuming the local model.
>
> WEB_TOOL_RULES
>
> Return up to eight listings, cheapest basket-priced total first, each with: link, asking price, basket-priced total, condition as the photographs show it, what is missing, pickup or delivery and its cost, and the listing date. Then name the marketplaces you searched that came up empty, so a thin list reads as a thin market rather than a thin search.
