# Merging Foods

A Food is the ingredient a Reading points at. The import left many spellings of one ingredient ("garlic cloves", "minced garlic", "Garlic"). Merging joins them: every Reading on the absorbed Food moves to the survivor. There is no un-merge.

Neither deleting a recipe nor repairing an ingredient line shrinks the list: old Versions keep their Readings, so a repair adds a clean Food beside the dirty one. A Food no recipe shows any more can be deleted with `delete_food`, or merged away.

## The batch

1. **Find candidates.** `list_foods` is too large to read inline: let it save to a file and work it with Python. Group by name after stripping quantities, units, preparation words (chopped, minced, fresh, to taste, for serving) and plural s; every group of two or more is a candidate. Grouping by staple word (onion, oil, garlic) finds the rest.
2. **Propose about twenty at a time**, grouped by staple, as a table of survivor, absorbed Foods and count, followed by what you are keeping apart and why. Apply only what Aurélien approves.
3. **Pick the survivor with the cleanest name.** Its names stay first and are the ones shown; the absorbed Food's names are kept after them, so a line using either word still finds the survivor (ADR 0043).
4. **Preview, then merge.** `preview_food_merge` returns `ingredient_lines`; `merge_food` must be handed that exact figure back or it refuses. Previews run in parallel; merges into different survivors run in parallel too.
5. **Fix names afterwards** with `set_food_names`, which takes a Language's whole list, the shown name first: `["ginger"]` renames "grated ginger", and `[]` takes a Language off. Read the Food with `get_food` first so the list keeps the names you mean to keep.

## French names

A Food may answer to several names in one language, and a merge keeps them all, the survivor's first. Merge the clean French Food first ("sel") and the clumsy ones after ("pincé de sel"), then drop a clumsy name with `set_food_names` if it should not stay. French Foods merge into their English twins, which gives the staples their French names.

## Keep apart

The Foods a cook tells apart are listed in the conventions note. Merge across them only on Aurélien's word.

Units that became Foods (`cup`, `tablespoon`) hang only off old Versions. Merging their plurals is harmless; there is nothing better to merge them into.
