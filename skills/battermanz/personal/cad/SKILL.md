---
name: cad
description: "Design or change a part for the user's 3D printer. Use when the user asks for a part, mount, holder or adapter to be designed, modelled or resized, wants a FreeCAD file they edited by hand checked, or asks how to do something in FreeCAD."
metadata:
  version: "1.1.0"
---

# CAD: parts for the 3D printer

The parts and the toolkit live in the `battercad` repo, checked out at `~/coding/battercad`. Its `AGENTS.md` is the source of truth for how a part is built, checked and delivered, and for which choices are still candidates: FreeCAD as the program, and the way a part is built. Work from that checkout whatever directory the session started in.

## Steps

1. **Read `~/coding/battercad/AGENTS.md`.** When the checkout is missing, `~/.claude/docs/repos.md` names its remote. Its "Candidates" section says whether a trial of the two build routes is still owed: when it is, the part you were asked for is the trial.

2. **Write the brief.** `parts/<name>/brief.md` holds what the part is for, what it must fit, and every measurement, in the user's words. The user measures with a caliper: ask for one measurement at a time, and only for those the part cannot be built without. Done when every dimension the part needs has a number from the user or a default you stated.

3. **Build, check and deliver** as the repo's `AGENTS.md` describes. Done when its check passes, you have looked at the pictures yourself, and the push has landed.

4. **Walk through the steps.** With the delivery, name the steps in the file in the order FreeCAD's side panel lists them, one plain line each: the user is learning FreeCAD and every delivered part doubles as a worked example.

## Tutoring

The user learns FreeCAD on their own parts. A FreeCAD term gets a plain-words definition the first time it appears. Answer how-to questions for the version in `~/coding/battercad/FREECAD_VERSION`, since tutorials for other versions show an interface that has moved. When the user shares a file they are stuck on, read it with the toolkit's read-only check before answering.
