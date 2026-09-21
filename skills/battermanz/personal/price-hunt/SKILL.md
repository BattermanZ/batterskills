---
name: price-hunt
description: Find the cheapest trustworthy way to buy a product you have already chosen, priced as a full basket landed at your door.
disable-model-invocation: true
metadata:
  version: "1.0.0"
---

# price-hunt

The product is already chosen; the job is the seller. Find the cheapest trustworthy way to get that exact product, plus everything its use requires, delivered to the user, and say how long it takes to arrive. Choosing between products is `/purchase-advisor`'s job, and product evidence stays upstream with it. A price watch is `/loop` run over this skill, not a mode of it.

Three terms carry the run:

- The **pin** is the maker's article number or EAN. Shop titles blur lookalike models and comparators conflate them, so the pin is what makes a price at one shop comparable to a price at another.
- The **basket** is the pinned product plus whatever the user's stated specification requires that the box does not contain. The cheapest seller of the headline item is often not the cheapest seller of the basket.
- The **landed cost** is the basket plus delivery, plus import VAT, customs duty and the carrier's handling fee wherever the goods cross a customs border. Every ranking uses landed cost.

## Hard rules

These bind every step.

- Read pages only. Carts, forms, accounts and orders belong to `/batterdeals` and to the user.
- A price reaches the report only once you have fetched it from the seller's own page in this session. Comparator, tracker and subagent figures are leads.
- Only a seller that passes the trust check in step 5 can be recommended.
- At most one subagent, for second-hand only, and only when step 4's trigger fires.

## Step 1: pin

Accept one product. A category ("a breast pump", "a good TV") goes to `/purchase-advisor` with one line saying why, and so do two or more products the user wants weighed against each other.

Find the pin on the maker's own page. When the user's words match more than one product (a Mini and a full-size model sharing a name, a current and a previous generation), ask one question to settle it. That is the run's only question.

When the vault is reachable, search it through `hatchdoor` for the product. A decision note carries the user's specification and any context bearing on urgency, and it is where step 6 offers to record findings.

State the location in the run's first message rather than asking for it: "hunting for delivery to <location>". The default is the **Location** line of the `effort-store-vault` skill; when that skill is absent, ask.

Done when the pin is recorded, the location is stated, and a decision note is found or known absent.

## Step 2: basket

Read what the box contains, from the maker's page or manual, and set it against the user's specification. Everything the specification requires that the box lacks joins the basket: a size the box omits, a charger the regional version leaves out. The basket holds requirements only, however useful an extra would be.

Consumables the product uses up on a schedule (replacement parts, cartridges, filters) stay out of the basket and are reported as a running cost with their interval.

Search for a bundle or set that covers the whole basket. When one exists it is priced beside the parts, and the cheaper wins.

Done when every basket line has a reason tied to the user's words, and the bundle search has an answer.

## Step 3: hunt

Hunt in this session, so every seller's price for every basket line stays in view. A summary drops the per-line prices that decide close contests.

- **Home market, in full**: every seller that delivers to the location and carries the pin, with every basket line priced at each.
- **EU probe**: one pan-EU comparator (Geizhals, idealo) for a seller in another member state that beats the home leader.
- **International probe**: one pass beyond the EU for the same.

A foreign listing under a different pin still counts when it is the same product sold for another region. List every difference from the home version (charger or plug, box contents, warranty region, language), each taken from the maker's page or the listing, and mark anything you could not establish as **unknown**. A difference that leaves the basket incomplete adds its missing line to that row, exactly as in step 2.

Comparators and price trackers render their price tables in JavaScript, so a plain fetch returns their prose without the numbers. Retailer product pages carry the price in the text. Use comparators to find sellers, then read the price at the seller.

Price history answers one question: is today a good day to buy? Read the current low, the all-time low with its date, and the typical price from a tracker for the location's market (knibble or Tweakers Pricewatch in the Netherlands, Geizhals across the EU, Keepa for Amazon).

Done when every home seller carrying the pin has a price for every basket line or a note of what was missing, both probes have run, and the price history has an answer.

## Step 4: second-hand

Probe the marketplaces local to the location (Marktplaats in the Netherlands, Kleinanzeigen in Germany, leboncoin in France) and price the best listing as a basket: add whatever it lacks against the specification, plus any part touching food, skin or milk, since hygiene means buying those new.

When that priced listing still clearly undercuts the new-market leader, dispatch one subagent with [references/second-hand-brief.md](references/second-hand-brief.md). A few hundred off a television is worth a stranger and no warranty; twenty off a €95 appliance is not. Otherwise report the probe's verdict and move on.

Done when the second-hand verdict is written down, with the subagent's report back if one ran.

## Step 5: verify and price

For each candidate, fetch the seller's own page and record:

- The price of every basket line, and stock.
- Delivery cost and **delivery time**, on every row, home sellers included.
- Import costs wherever the goods cross a customs border: VAT, customs duty and the carrier's handling fee. Establish the current rules for the destination from its customs authority at run time. The EU replaced its duty-free treatment of parcels up to €150 with a flat per-item duty on 1 July 2026, with further changes scheduled, so remembered thresholds are stale.
- The returns policy as it applies to this product (a broken hygiene seal commonly ends the right to return), and who honours the guarantee or warranty, in which region.
- The **seller of record**: who the contract is with and who owes the legal guarantee. On a marketplace that is either the platform or a third party, and the page says which.
- A **trust verdict**. A known retailer, or a platform selling on its own account, passes. An unknown webshop passes on company registration, a recognised trust mark (Thuiswinkel Waarborg in the Netherlands), a real review history, and absence from the national scam register (Fraudehelpdesk in the Netherlands). A non-EU seller passes only as an authorised reseller, since that is where counterfeits sit.

Done when every row has a verified landed cost, a delivery time, a returns line, a guarantee line, a seller of record and a trust verdict, with **unknown** wherever a value could not be established.

## Step 6: report and hand off

One chat message, in this order:

1. **The full table**, every candidate including those that failed the trust check: seller, seller of record, trust verdict, each basket line's price, delivery cost, import costs, landed cost, delivery time, returns, guarantee and its region, and variant differences on foreign rows.
2. **The recommendation**, argued: which seller, at what landed cost, and why, drawn only from sellers that passed.
3. **The split**: the cheapest passing seller and the fastest sensible one, each with landed cost and delivery time, or one line saying they are the same seller. When context gives the urgency (a decision note, the user's own words), lean on it and say where it came from.
4. **Price history**: today's price against the all-time low and the typical price, in one line.
5. **Second-hand**: the verdict, even when every row is new.
6. **Running costs**: consumables and their interval.
7. **Handoff**: the winner's product URL for `/batterdeals`, plus the URL of every passing seller whose landed cost sits close enough that a discount code could reorder them. The user types `/batterdeals`, since it drives a real cart.

The run saves nothing. When a decision note exists and the run found something about the product that stays true for months (a size the box omits, a variant that differs by region), offer in one line to record it there.

Done when the message carries all seven parts.
