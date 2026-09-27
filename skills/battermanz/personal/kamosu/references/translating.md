# Translating a recipe into French

The recipe keeps its source Language, and the French text is a Kamosu Translation: `start_translation` makes a French Branch of the same Lineage that records which Version of the source it renders. The source stays the recipe of record; the Translation follows it.

## Making the Translation

How the French reads (units, title, "vous", what is translated and what is copied) is in the conventions note. Show Aurélien the pair when a title is a judgement call. Kamosu converts a °F temperature inside a step on screen; check it does before relying on it.

**Photos, tags and related recipes are copied by hand.** `main_photo` and every `steps[].photo` go into the `start_translation` payload with the same ids. Then copy every tag with `set_recipe_tag` and every related recipe with `set_related_recipe`. Nothing carries them over.

## Every ingredient line lands on an existing Food

The reader finds a Food by its name in the line's Language: exact match, case-folded, accents kept, no plurals, and `'` and `’` are different characters. A line that matches no French name mints a new French-only Food, which splits the shopping list from its English twin.

- **Name the Food first.** Before writing the lines, map each source line to its Food with `shopping_basis` on the source (it names the Food behind every line, read-only). A Food with no French name gets one with `set_food_names` before the translation is saved. Give a counted Food both numbers, `["œufs", "œuf"]`, so "1 œuf" and "3 œufs" both find it (ADR 0043).
- **Name it by the conventions note's rules** for French Food names, and keep its keep-apart pairs apart in French too.
- **A clean French-only Food answering to the same ingredient** ("crème fraîche", "piment doux") is merged into the English Food, on Aurélien's word, instead of giving the English Food a second copy of the name.
- **Write each line with the Food's French name as its food words**: "2 gousses d'ail", "200 g de farine", "3 œufs".
- **Read back with `shopping_basis` on the Translation.** Every ingredient line points at the same Food as its source line. Fix a miss ("1 carotte" read as a new Food "carotte") by merging the stray into the Food: the merge keeps "carotte" as a second French name, so the next "1 carotte" finds it.
- **Report every French name you set** in the run's summary, so Aurélien can flag one.

## Keeping a Translation current

`get_thread` on any Branch lists its Lineage's Branches, each with its `language` and, for a Translation, `translation.versions_behind`. Above 0, the source has moved on since the Translation was made.

Bring it up to date with `save_recipe_version` on the French Branch: the whole French recipe, with `translates_version_id` set to the source's head Version. `edit_recipe` cannot move `translates_version_id`, so an edit alone leaves the Translation claiming the old Version.

## The sweep

At the start of every Kamosu session, before the task Aurélien named: for each recipe on the shelf that is his (`writes: true`) and not in French, `get_thread` it. List the ones with no French Branch and the ones whose Translation has `versions_behind` above 0, and offer to handle them. Reading 90 recipes through MCP floods the context; a short script calling the MCP endpoint does it outside (Kamosu speaks MCP `2026-07-28`, stateless: no `initialize`, each `tools/call` carries `Mcp-Method` and `Mcp-Name` headers and `params._meta` with `io.modelcontextprotocol/protocolVersion` and `io.modelcontextprotocol/clientCapabilities`; the `Authorization` header comes from `~/.claude.json` as for photos, never printed).
