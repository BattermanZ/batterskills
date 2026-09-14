---
name: effort-store-vault
description: The effort store's vault adapter. Reach it whenever the effort-store contract runs in this environment; it maps roots, find, open, write, update and register onto the BatterNotes vault through Hatchdoor.
---

# Effort store: BatterNotes vault

This environment's adapter for the `effort-store` contract. Load the `hatchdoor` skill first: it owns filing, frontmatter, tags, note shape, linking, British English, this vault's unslop exceptions and the change report. This file maps only the contract.

## Roots and layout

- A consumer root maps to `personal/<root>/`: purchase-advisor's `purchases` lives at `personal/purchases/`. A root folder that does not exist yet is created by the first-run question below.
- **A root's first run needs three things and asks for them once.** The folder, the `type/*` tag, and the hub note are one decision, not three: put them in a single question, before the consumer's own interview begins, and never between the consumer's questions. A user working through a decision should not be interrupted to rule on vault filing. If they decline the hub, the effort still writes; **register** links it wherever they said instead.
- An effort is one folder, `personal/<root>/<Effort>/`, with its notes inside. This is deeper than the vault's usual two levels, and deliberate for the same reason deep-research's efforts are: the notes only make sense together.
- A note's title is `<Effort> - <note name>`: the consumer declares bare note names, and this adapter composes the titles. The separator is ` - `, never an em dash, per the `hatchdoor` skill's documented exception, and it applies to every note of an effort.

## Operations

- **find** — `search_notes` on the subject, and `get_tree` under `personal/<root>/`. A folder that does not exist yet is an error rather than an empty tree: read it as "no effort yet" and carry on to the first-run question. During or just after a write burst, per-note reads are authoritative and `get_tree` is not (Hatchdoor #226).
- **open** — the vault has no empty folders; the effort's folder comes into existence with the first **write**.
- **write** — `create_note` under the effort folder, frontmatter per the hatchdoor skill. For the `type/*` tag, consult the vault's Tags Reference; a new root's tag was settled by the first-run question, so do not re-ask here, and add it to the Tags Reference before using it. Every mutation carries a commit summary of the form `<root>(<effort>): <what happened>`. Wikilink the effort's notes to each other as they are written.
- **update** — `edit_note`, or `replace_section` when the dated sections sit under one heading. Per the contract, a fresh pass inserts its dated section above the older ones, and above `## Related`; `append_to_note` would land it below both.
- **register** — link the effort into the topic hub for `personal/<root>/`, created or declined by the first-run question rather than asked about here. Then one hatchdoor change report covering the whole effort, a clickable link per note. Agents that wrote notes mid-run do not report; the register step reports once, for all of it.

Hatchdoor being unavailable mid-run is a blocker to surface, per the hatchdoor skill: report it and park the effort's notes in the session scratchpad for import, rather than silently falling back to the contract's `~/efforts/` tree.

## Environment facts for consumers

Personal defaults a consumer skill may use, kept here so the consumer stays shareable:

- **Location**: Amsterdam, the Netherlands. A consumer that asks for a location offers this as the recommended answer to confirm, per run, rather than asking cold; a run for someone elsewhere overrides it.
