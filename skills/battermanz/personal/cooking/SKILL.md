---
name: cooking
description: "Work out how to cook something in the user's own kitchen. Use when asked how to cook an ingredient, a cut or a dish, or for a time, heat setting or method at the hob or oven."
metadata:
  version: "1.0.1"
---

# Cooking: advice for this kitchen

Advice for one kitchen, not for kitchens in general. The method names the burner, the setting, the pan and the oven mode the user actually has, starts from what the user has already cooked, and has every number checked against a source before it reaches them. The equipment and the cooking history live in the vault and in Kamosu; this skill says where to look and how to weigh what turns up.

## Steps

1. **Inventory the kit.** Search the vault through Hatchdoor for the equipment the cook could use: the hob, the oven, pans by material, appliances, a probe thermometer. Read the sections that bear on this cook, such as burner layout and outputs, power-level tables and heating modes. Done when every piece of kit the method will name comes from a note or from the user. Kit that no note records is unknown, so ask about it, or write a method that works without it. A plan, an artifact or an earlier answer only shows what someone assumed the user owns.

2. **Read the history.** Search Kamosu with `search_recipes` three ways: the dish, the main ingredient or cut, and the technique ("pan-seared steak"), since the closest record is often a different dish cooked the same way. For every hit that shares the cut or the technique, `get_thread` lists its Branches and their Attempt notes, and `get_recipe` on each Branch gives that Branch's method and Version notes. Read all three. Done when the closest recorded cook is named with its burner, settings, timings and how it turned out.

   Rank the evidence in this order: Attempt notes, the newest as-cooked Branch, older Branches, manuals and outside sources, then plans and artifacts made before a cook. A recorded cook that ran too hot outranks the manual's recommended setting, and a plan nobody updated after the cook is stale.

3. **Draft the method** from the closest recorded cook, adjusted for what differs: thickness, weight, doneness, number of pieces. Every step names its kit and setting.

4. **Verify before answering.** Check every time, temperature, heat level, resting time and safety claim against sources read in this run: the retailer's or producer's own recipe for that product or cut, a technique source that tests its claims (Serious Eats is one), and the national food-safety authority for anything about safety. SEO recipe sites copy each other and settle nothing. Revise the draft wherever a source changes it, and name the source behind each change. Done when every number in the answer traces to the user's history or to a source read in this run.

## Heat

A burner's spread matters as much as its output. A multi-ring burner turned down heats a wide pan base evenly; a smaller single-ring burner concentrates its heat in the centre, and cast iron moves heat sideways slowly, so the centre scorches while the edges lag. When a recorded cook ran too hot, turn the same burner down before moving to a smaller one. A change of burner or pan the user suggests gets weighed against this before it is adopted, with the reasoning given either way.

## Saving the recipe

When the user asks to save what they cooked, the recipe carries the whole method recommended across the conversation, in cooking order: the prep steps from early answers (taking meat out of the fridge, salting, warming plates) as well as whatever the last artifact or timer covered. Gather every step first, then load the `kamosu` skill for the save.
