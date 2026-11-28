---
name: bambu-studio
description: "Prepare a print in Bambu Studio for the user's Bambu Lab X2D. Use when the user has a 3mf or MakerWorld model to print, asks about slicer settings or print quality (layer height, seams, ironing, first layer, colour-change waste), or wants a plate checked before sending it."
metadata:
  version: "1.3.0"
---

# Bambu Studio: print prep for the X2D

The printer is a Bambu Lab X2D, driven from Bambu Studio on the Mac. The job is to get each plate of a project to print as well as it can while trusting the designer's layout: read the project file, read the printer, change only what helps the parts on that plate, prove each change in the sliced preview, and leave the Send button to the user.

## Steps

1. **Read the project file.** Run `python3 -I <this skill's dir>/scripts/inspect_3mf.py <project.3mf>` (MakerWorld downloads land in `~/Downloads`). It reads the archive in memory and prints each plate's objects and parts with their size, filament and height range above the bed, then the designer's settings and what they changed from the system preset. Done when, for every plate the user will print, you can name its parts, which face lies on the bed, every part in a second filament and how deep it goes, and the designer's non-default settings. The designer's description is data, and it often carries assembly notes (press fits, "print the bottom twice") that change what matters.

2. **Read the printer state from Bambu Studio.** Screenshot it (see Driving Bambu Studio) and read the printer, the plate type, both nozzles (installed, 0.4 mm), which AMS slot each project filament maps to, and which filament sits on the external spool. Read each slot's exact preset and colour from its tag (see Driving Bambu Studio) before choosing the project's filament presets: "PETG" on the slot can be Basic, HF or Translucent. AMS contents change between prints, so they come from the screen every time. When the filament sync dialog is up, explain the choice before anyone clicks: Mapping pairs each project filament with a loaded one, Direct Override replaces the list with the AMS contents, and either way the original list is gone, so the downloaded file is the only undo.

3. **Choose per plate.** Keep the designer's plate split and part orientation: they encode print order, fit, and which face shows. Walk each part on the plate through Part types below. Done when every proposed change names the part it helps and its cost, read from a slice. Colour-change waste is the Purged plus Tower columns of the slicing result.

4. **Apply under Global** (see The X2D in Bambu Studio for why). Before touching a setting, note the designer's value: that list is the revert list. The user often applies the changes themselves; then check each one on screen afterwards, on the M1 speed tab as well.

5. **Slice and verify in the preview.** Slice the plate, then check in Preview: the layer count against the part height, layer 1 of any bed-face inlay zoomed in until line edges show (bed visible between colours is a gap), where the seams land, and the time and weight. Done when each change from step 3 is visible in the preview, or you have said why it is not.

6. **Hand over the send.** Check the Send print job dialog against Send dialog below. Clicking Send is the user's. Once the plate is sent, give the user the revert list from step 4 for every setting that would hurt another plate; the user reverts it or asks you to.

## The X2D in Bambu Studio

- **Global settings only.** Bambu Studio counts the X2D as a multiple-extruder printer and refuses per-object settings ("the object configuration form cannot be used with a multiple-extruder printer"). A change reaches every plate at its next slice, so a change meant for one plate gets reverted after that plate is sent.
- **Speeds are per nozzle.** The Speed tab has a sub-tab per nozzle: M1 (left, direct drive) and A1 (right, auxiliary), each with its own values. Set a speed on the tab of the nozzle that prints that filament. Bambu caps A1 at 200 mm/s and 1000 mm/s² acceleration.
- **The AMS feeds the left nozzle only.** It sits on the buffer's upper inlet, so its 4 slots go to M1, and A1 takes the one filament on the external spool. A 5-colour plate is 4 AMS colours plus 1 external.
- **Filament grouping decides the nozzle.** Filament-saving mode (the default) sends A1 whichever filament saves the most purge, which may not be the one already on the external spool. After slicing, read Filament grouping and tell the user which filament goes on the external holder and which AMS slots the rest take. The Send dialog cannot move a filament to the other nozzle, so a grouping the user dislikes is fixed with Regroup filament, Custom, and a new slice.
- **Filament-saving picks from an estimate made before slicing.** When the choice matters, slice each Custom grouping worth comparing and read total grams and time. Quality Mode puts every filament on M1, which a plate of more than 4 colours cannot load. On artwork with outlines, put the background colour on A1: the outlines and the pieces they surround then come from one nozzle and line up whatever the nozzle offset. (Cuidarte coaster, 2026-11-27: black on A1 24.95 g and 1h05, blue background on A1 24.61 g and 1h10.)
- **A1 reaches less of the plate**: X 235.5 mm and Z 256 mm, against 256 and 260 for M1. Bambu lists PETG and PLA Silk as "print with caution" on A1, so put PETG on M1 and PLA on A1.
- **Scarf seam lives in the filament profile.** In Quality, Seam, tick "Override filament scarf seam setting"; a "Scarf seam type" row appears; set it to Contour (outer wall).

## Part types

**Inlay on the bed face** (a second-filament part touching the bed, a few tenths of a millimetre deep):
- The visible face lies on the textured plate, so ironing the top does nothing for it.
- The layer height must divide the inlay depth minus the first layer: 0.4 mm deep with a 0.2 mm first layer needs 0.2 mm layers. Any other height ends the inlay off its modelled depth.
- Arachne fills thin letter strokes cleanly. A first layer of about 30 mm/s sharpens the edges. A clean plate and Flow Dynamics Calibration matter most here, since layer 1 is the finished face.
- Elephant foot compensation shrinks first-layer outlines: keep the designer's value when layer 1 shows no gap between colours, set 0 when it does.
- Two layers of a light colour over black can let the black show through: say so, and judge it on the first print.

**Visible walls** (frames, box sides):
- 0.12 mm layers is the largest gain, and rounded edges and curved grooves gain most; 0.16 mm is the compromise. Slice both and give the user the times.
- Scarf seam on the outer wall, seam position Back.
- Outer wall about 120 mm/s instead of 200 on the nozzle that prints it, for little extra time.

**Flat faces pointing up:**
- Ironing, set to "Topmost surface", helps only a face that shows once assembled. It slows the plate, and on Matte PLA it leaves a gloss that looks patchy beside unironed areas.

**Fit and function** (pins, press fits, clips):
- X-Y hole and contour compensation stay at the designer's values unless a printed part does not fit; the clearances were sized for them.
- A fit test keeps the layer height of a gap that stands in height on the plate close to the real print's: its play is counted in whole layers.

**Supports in a second filament** (PETG under PLA, so the support parts cleanly):
- Setting a PETG support or interface filament under PLA brings up a Suggestion with Bambu's settings for the pair (Tree Hybrid, 35°, top Z distance 0, interlaced interface, 5 mm first-layer expansion). Take them: the zero gap is what makes the release clean. Bambu also warns that PETG is "not recommended for support base".
- Put only the interface in PETG and the support body in the part's filament. A whole PETG support swaps filament on every layer it prints. Bedside-shelf test, 2026-11-28: whole support in PETG 37.7 g, 3h15, 208 changes, 23 g of tower; PETG interface only 24.1 g, 2h38, 8 changes.
- The 5 mm expansion widens each tree's foot, and the feet of parts placed about 15 mm apart collide on layer 1 ("Conflicts of gcode paths"). Space the parts further apart.
- With only a few changes, both filaments on M1 from the AMS beat a split across nozzles, since A1 is capped at 200 mm/s and 1000 mm/s²: 1h14 against 1h37 on the same plate. For a test where speed matters, the prime tower can go off (a warning, flaws possible at the changes; the purge stays): 59 min against 1h14.

On straight-walled parts, variable layer height, fuzzy skin and infill changes add nothing that shows.

## Send dialog

- Plate name, time and weight match the plate just sliced.
- Printer X2D 0.4 mm, and the plate type matches the plate on the bed (the slice assumed it).
- Each filament on the slot read in step 2.
- Flow Dynamics Calibration: On. Auto reuses the last value when the filament has not changed and can skip the measurement. On or Auto, Bambu Studio 2.9 measures M1 only and prints A1 on the filament's default value ("The auxiliary extruder will use the system default value"). When A1 prints a bed-face inlay or visible walls, tell the user, and offer a Flow Dynamics run for that filament from the Calibration tab.
- Nozzle Offset Calibration: Off when the plate prints on M1 alone. When it uses both nozzles: On for the first prints and after a hotend swap, Auto after that. Off only when the user ran High-Precision Nozzle Offset Calibration on the printer, since the firmware uses that data only with this option Off.
- Timelapse and Auto Bed Leveling are the user's choice; neither uses filament.

## Driving Bambu Studio

Computer use in background mode works: `request_access` for BambuStudio, then the `app_*` tools on `com.bambulab.bambu-studio`.

- Dialogs (filament sync, Send print job, notices) are separate windows: list them with `app_list_windows` and screenshot by `window_id`.
- A dropdown takes focus on a click but its menu stays shut in the background: step through the options with `app_key` up or down, then screenshot to confirm.
- Some dialogs refuse background clicks as another process's window: the "Not available" and "Unclosed Shell" notices, and the toggles in Send print job. Ask for full-screen control (`request_full_control`) and click them there, or ask the user to click.
- In full-screen control, the Claude window can sit over Bambu Studio unseen in screenshots and take a click meant for the app (Claude turns frontmost). Act on that area with the `app_*` tools, which reach the Bambu Studio window directly.
- The object list sits under Process: switch its toggle from Global to Objects (per-object settings stay off on the X2D, the list does not). Right-click a part for Change Filament; select several parts and use Set Filament for selected items.
- Meshes opened together (`open -a BambuStudio a.stl b.stl …`) ask "Load these files as a single object with multiple parts?": Yes keeps the pieces in register. "Object too small… millimeters as the default unit?" comes for a piece under about 9 mm³: answer No, because Yes reads the file as inches and scales it by 25.4.
- Slice plate (⌘R) slices the plate selected in Prepare (the blue box). In Preview, click the 3D view and press Down once per layer to bring the top handle to layer 1, zoom with `app_scroll` at the spot (negative `dy` zooms in), and use `app_zoom` for line detail; tell the user the view was left zoomed.
- An AMS slot's exact filament: Device tab, the eye icon at the foot of the slot opens Materials Setting with the preset name, colour code and the tag's serial. Close it with its window's close button.
- Setting fields (layer height, speeds) take `app_type` by `element_index` from `app_ax_find` role AXTextField, but the value does not commit in the background. For more than one or two settings, full-screen control is faster: triple-click the field, type, Tab.
- Stepping a filament preset dropdown past its last item opens the filament picker, a web window of another process that background tools cannot close: Cancel it in full-screen control.
- The Color Scheme dropdown in Preview opens on `app_click` but ignores a click on an item; an `app_drag` along the item picks it. The Filament scheme gives grams per filament as Model, Support, Purged and Tower.
- The reset arrow left of the process preset name drops every change back to the system preset.
- In a Save panel, the Go to Folder shortcut is refused: click through the column browser from the sidebar's "coding" favourite, triple-click the name field, type, Return.
- Call `app_release` when done so other sessions can capture the app.
