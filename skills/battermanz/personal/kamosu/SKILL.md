---
name: kamosu
description: "Work on the household recipe library in Kamosu through its MCP tools: add, fix, rebuild or translate a recipe, retitle, tag, merge Foods, record an Attempt, or file a Kamosu bug found along the way."
metadata:
  version: "1.4.0"
---

# Kamosu: the recipe library

Kamosu is Aurélien's self-hosted recipe app, and its one instance is the household's only copy of the library. `get_public_address` gives its address, called `<public address>` below. There is no staging: every write lands in the recipes he cooks from. Treat each save as **production**.

Two vault notes in `personal/projects/kamosu/`, reached through the `hatchdoor` skill, hold what this skill does not:

- **Kamosu - Library conventions**: how Aurélien wants the library to look (titles, Source, ingredient lines, photos, French translations, tags and their tests, Food names and the Foods kept apart). Every rule in it is his; this skill is how to carry them out. Read it before the first write.
- **Kamosu - Recipe library cleanup**: the running record of work done, what is still open, and the bugs filed. Read its "Still to do" and its bug list before starting, and update it before finishing.

## Before the first write

- The `kamosu` MCP server is registered per project, in `~/coding/wayfinding`, `~/coding/kamosu` and `~/coding/batterlab`. Anywhere else the tools are absent: say so rather than working around it.
- `instance_status` answers when the server is reachable.
- Check the open issues on `BattermanZ/Kamosu` that this skill names (#161, #165, #166, #167, #178, #179). A fixed one retires the workaround written for it.
- Run the translation sweep in [references/translating.md](references/translating.md) and offer what it finds.

## Hard rules

- **Read back every save** with `get_recipe`: ingredient count, step count, photos, and the fields you meant to leave alone. Move on only when they match. Also read `cooking.steps[].uses`, Kamosu's own guess at which ingredients each step uses, and report any step it links wrongly.
- **One recipe at a time**, every write verified before the next.
- **The source decides every quantity, time, temperature and method.** Where the source is silent, leave the field empty and say so. A gap is honest; a plausible guess in a recipe he cooks from is not. What a video shows is the source as much as what it says.
- **Build the fullest recipe the source supports**, in the shape the conventions note sets. Missing amounts leave those fields empty and nothing else: the recipe still gets its steps and photos wherever the source has them.
- **Search the shelf before adding a recipe**, for its main ingredients and its dish type. Link anything close with `set_related_recipe`, and bring a likely duplicate to Aurélien before writing.
- **Deleting a recipe is Aurélien's call**, asked recipe by recipe.
- **Choices are his.** Bring options with a recommendation, one question at a time, and wait.
- **Link every recipe you create or edit** in your reply, with the recipe's title as the link text: `[Gochujang chicken orzo](<public address>/recipes/b_c54e61034c7d5ad8)`, never a bare URL. The web app's recipe page is `/recipes/[branchId]`. No tool returns this link itself, so build it.
- **Show a change before making it** whenever it touches more than the one recipe he named: old and new side by side, applied only on his word.

## Editing mechanics

Kamosu's server states most of these in its MCP instructions since #168, but Claude Code does not show them to the model (seen 2026-09-27), so they stay here until it does.

- **`edit_recipe` for every change.** It takes only the fields that change. `ingredients` and `steps` are each replaced whole, so changing one line means sending that whole list and leaving the other out. `save_recipe_version` replaces the entire recipe: a field left out is erased.
- **Every edit carries a `change_note`.** Edits within roughly an hour of the last save on the same recipe collapse into that Version, and a collapsed edit without a note erases the one already there (#165). A note-only edit saves nothing, so a lost note stays lost.
- **One recipe, one edit.** Gather everything a recipe needs, then send it once: a second pass inside the hour folds into the first and rewrites its note.
- **Photos go up out of band.** `POST <public address>/api/photographs` takes the raw image as the body with the kamosu MCP server's own `Authorization` header, read from `~/.claude.json` (`projects["<cwd>"].mcpServers.kamosu.headers`) inside the script, never printed. Set a plain `User-Agent` (`curl/8.5`); Python's default draws a 403. The answer's `result.photograph_id` goes in `steps[].photo` or `main_photo`. `upload_photograph` takes base64 through the conversation, about 100 KB of context a photo: keep it for a single picture.
- **Newlines in a note are real line breaks** in the parameter, never a typed `\n`.
- **Tags, Readings and Related Recipes are cheap**: `set_recipe_tag`, `set_reading` and `set_related_recipe` touch no content and mint no Version.
- **`read_ingredient_lines` runs only on Aurélien's word.** It takes no input and walks the whole library, and until #178 is fixed it mints an orphan Food for every already-read line whose word matches no Food name.
- **A misread ingredient line is fixed with `set_reading`.** An unchanged line keeps its old Reading on every new Version, so a re-save never corrects it (#166). Ranges ("2-3 basil leaves") read as all Food until #167 is fixed.

## Notes and Attempts

The note holds what is true of the recipe: tips, FAQs, where a method came from when it is not the cited source. What happened on one cooking is an **Attempt** (`start_attempt`, `finish_attempt`), made on the day it happened, never backdated.

## French translations

Which recipes get a French Translation, and how the French reads, is in the conventions note. A Translation is verified like any save. How to make one, how its lines land on existing Foods, and how to catch one up: [references/translating.md](references/translating.md). Read it before the first `start_translation`.

## Tags

The tags, which ones imply another, and the test for each are in the conventions note. Tag a new or rebuilt recipe by those tests, and its Translation the same.

Before changing tags across more than one recipe, snapshot every recipe's current tags to a file: tag changes have no undo.

## Recovering a recipe from its source

A recipe that is an empty bookmark, a caption dumped into one step, or a method filed as ingredients is rebuilt from its own source, never from memory. Web pages, Instagram and a caption with no method: [references/recovering-recipes.md](references/recovering-recipes.md). YouTube and Shorts (description, captions, reading the method and the photos off the frames): [references/youtube.md](references/youtube.md).

## Foods

Merging Foods is the only thing that shrinks the list, and it cannot be undone. The batch workflow and how French names behave are in [references/foods.md](references/foods.md); the Foods to keep apart are in the conventions note. Read it before the first merge.

## A fault in Kamosu itself

File it on `BattermanZ/Kamosu` with `gh issue create --repo BattermanZ/Kamosu` and the label `needs-triage` alone. Use the house shape: a `## Agent Brief` with **Summary**, **Seen** (live evidence with branch ids and a does/should table), **Why** ("Not investigated" unless you read the code), **Desired state**, and a "Keep existing behaviour" line. Search the issues first; a duplicate costs more than a comment.

## Finishing

Update the cleanup note: move finished work into its done record, add what you left and why, name any issue filed. Report per task what changed, what you verified, and what you left, with each recipe's link and every French Food name you set. A new rule Aurélien settles along the way goes into the conventions note, not the cleanup note.
