# Merging Foods

A Food is the ingredient a Reading points at. The import left many spellings of one ingredient ("garlic cloves", "minced garlic", "Garlic"). Merging joins them: every Reading on the absorbed Food moves to the survivor. There is no un-merge.

Neither deleting a recipe nor repairing an ingredient line shrinks the list: old Versions keep their Readings, so a repair adds a clean Food beside the dirty one. A Food left behind by a deleted recipe cannot be deleted (#162), but it can be merged away.

## The batch

1. **Find candidates.** `list_foods` is too large to read inline: let it save to a file and work it with Python. Group by name after stripping quantities, units, preparation words (chopped, minced, fresh, to taste, for serving) and plural s; every group of two or more is a candidate. Grouping by staple word (onion, oil, garlic) finds the rest.
2. **Propose about twenty at a time**, grouped by staple, as a table of survivor, absorbed Foods and count, followed by what you are keeping apart and why. Apply only what Aurélien approves.
3. **Pick the survivor with the cleanest name.** It keeps its name; the absorbed English names are dropped.
4. **Preview, then merge.** `preview_food_merge` returns `ingredient_lines`; `merge_food` must be handed that exact figure back or it refuses. Previews run in parallel; merges into different survivors run in parallel too.
5. **Fix names afterwards** with `set_food_name`: a survivor can be renamed in any language ("grated ginger" to "ginger").

## French names

A Food keeps one name per language, and a merge keeps the **first** French name to arrive. Merge the clean French Food first ("sel") and the clumsy ones after ("pincé de sel"), or correct it afterwards with `set_food_name`. French Foods merge into their English twins, which gives the staples their French names.

## Keep apart

A cook cares about these differences, or the name is ambiguous. Merge across them only on Aurélien's word:

- Onion colours (onion, white, yellow, red); spring onion versus onion.
- Olive versus extra-virgin olive oil; sesame versus toasted sesame oil; each neutral oil.
- Kosher, fine sea and plain salt (they measure differently by the spoon).
- "pepper" versus black pepper.
- Salted versus unsalted butter.
- Fresh versus shredded mozzarella.
- "sugar" versus granulated; caster, light brown, soft brown, muscovado.
- Light, dark and sweet soy sauce.
- Chicken broth versus stock; semi-skimmed milk versus milk.
- Each vinegar; rice wine versus rice vinegar.
- Chicken cuts (thighs, boneless thighs, drumsticks, breast).
- Unwaxed lemon versus lemons; curly versus flat-leaf parsley.
- "Tomato puree" (British paste or American passata).
- Any "X or Y" Food: it names a choice, not an ingredient.

Units that became Foods (`cup`, `tablespoon`) hang only off old Versions. Merging their plurals is harmless; there is nothing better to merge them into.
