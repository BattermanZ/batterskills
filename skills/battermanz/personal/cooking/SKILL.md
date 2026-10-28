---
name: cooking
description: "Work out how to cook something in the user's own kitchen. Use when asked how to cook an ingredient, a cut or a dish, or for a time, heat setting or method at the hob or oven."
metadata:
  version: "1.1.0"
---

# Cooking: advice for this kitchen

Advice for one kitchen, not for kitchens in general. The method names the burner, the setting, the pan and the oven mode the user actually has, starts from what the user has already cooked, and has every number checked against a source before it reaches them. The equipment and the cooking history live in the vault and in Kamosu; this skill says where to look and how to weigh what turns up.

## Steps

1. **Inventory the kit.** Search the vault through Hatchdoor for the equipment the cook could use: the hob, the oven, pans by material, appliances, a probe thermometer. Read the sections that bear on this cook, such as burner layout and outputs, power-level tables and heating modes. For the hob, read its note's **Heat words on this hob** and **As cooked on this hob** sections before the manual's power table, and rank them above it (see Heat below). Done when every piece of kit the method will name comes from a note or from the user. Kit that no note records is unknown, so ask about it, or write a method that works without it. A plan, an artifact or an earlier answer only shows what someone assumed the user owns.

2. **Read the history.** Search Kamosu with `search_recipes` three ways: the dish, the main ingredient or cut, and the technique ("pan-seared steak"), since the closest record is often a different dish cooked the same way. For every hit that shares the cut or the technique, `get_thread` lists its Branches and their Attempt notes, and `get_recipe` on each Branch gives that Branch's method and Version notes. Read all three. Done when the closest recorded cook is named with its burner, settings, timings and how it turned out, or when none is close and the three searches are named.

   Rank the evidence in this order: Attempt notes, the newest as-cooked Branch, older Branches, manuals and outside sources, then plans and artifacts made before a cook. A recorded cook that ran too hot outranks the manual's recommended setting, and a plan nobody updated after the cook is stale.

3. **Draft the method** from the closest recorded cook, adjusted for what differs: thickness, weight, doneness, number of pieces. Every step names its kit and setting.

4. **Verify before answering.** Check every time, temperature, heat level, resting time and safety claim against sources read in this run: the retailer's or producer's own recipe for that product or cut, a technique source that tests its claims (Serious Eats is one), and the national food-safety authority for anything about safety. SEO recipe sites copy each other and settle nothing. Revise the draft wherever a source changes it, and name the source behind each change. Done when every number in the answer traces to the user's history or to a source read in this run. A number that does not is left out, even labelled as an estimate: check it, or write the step to be judged by eye (browned underneath, nothing pink inside).

## The answer

- **The first line names the closest recorded cook**: the dish, its date, the burner and setting, and how it turned out ("Closest cook: pan-seared kogelbiefstuk on 20 October, medium-high (wok burner, 4), came out well"). When no recorded cook is close, the first line says so and names what was searched: the dish, the ingredient and the technique.
- **The last line says where each number came from**: each time, temperature, heat setting and amount with its source, whether a recorded cook, the hob note's heat-word table or a page read in this run.

## Heat

**Every hob setting is written as a word first, then the burner and the knob in brackets**: "Brown the skin side on very high (wok burner, 7) for 6 minutes." The word is what someone reading a shared recipe follows; the brackets are what the user turns. The burner is always named, even when the whole method uses one.

Burners are named by size: small, medium, large and wok. The hob's note maps each name to its burner.

A word becomes a knob number, or a knob number a word, only through the hob note's **Heat words on this hob** table, for that burner. The manual's power table never converts either way: its levels are the same for every burner, and the recorded cooks show them running hot. Where the table gives a range, write the knob the closest recorded cook used if it falls inside, and otherwise the range itself ("high (wok burner, 5 to 6)"). A dash in the table means the burner does not reach that word: say so and ask which burner to use, naming the ones that do. A word or burner the table has nothing for is asked, not guessed. A knob nobody recorded is not filled in: write the word and the burner alone, and say the knob was not recorded.

A burner's spread matters as much as its output. A multi-ring burner turned down heats a wide pan base evenly; a smaller single-ring burner concentrates its heat in the centre, and cast iron moves heat sideways slowly, so the centre scorches while the edges lag. When a recorded cook ran too hot, turn the same burner down before moving to a smaller one. A change of burner or pan the user suggests gets weighed against this before it is adopted, with the reasoning given either way.

## Saving the recipe

When the user asks to save what they cooked, the recipe carries the whole method recommended across the conversation, in cooking order: the prep steps from early answers (taking meat out of the fridge, salting, warming plates) as well as whatever the last artifact or timer covered. Every hob setting in it follows the format in Heat above, an unrecorded knob included. Gather every step first, then load the `kamosu` skill for the save.
