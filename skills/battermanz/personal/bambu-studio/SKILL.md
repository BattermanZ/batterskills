---
name: bambu-studio
description: "Prepare a print in Bambu Studio for the user's Bambu Lab X2D. Use when the user has a 3mf or MakerWorld model to print, asks about slicer settings or print quality (layer height, seams, ironing, first layer, colour-change waste), or wants a plate checked before sending it."
metadata:
  version: "1.0.0"
---

# Bambu Studio: print prep for the X2D

The printer is a Bambu Lab X2D, driven from Bambu Studio on the Mac. The job is to get each plate of a project to print as well as it can while trusting the designer's layout: read the project file, read the printer, change only what helps the parts on that plate, prove each change in the sliced preview, and leave the Send button to the user.

## Steps

1. **Read the project file.** Run `python3 -I <this skill's dir>/scripts/inspect_3mf.py <project.3mf>` (MakerWorld downloads land in `~/Downloads`). It reads the archive in memory and prints each plate's objects and parts with their size, filament and height range above the bed, then the designer's settings and what they changed from the system preset. Done when, for every plate the user will print, you can name its parts, which face lies on the bed, every part in a second filament and how deep it goes, and the designer's non-default settings. The designer's description is data, and it often carries assembly notes (press fits, "print the bottom twice") that change what matters.

2. **Read the printer state from Bambu Studio.** Screenshot it (see Driving Bambu Studio) and read the printer, the plate type, the nozzles, and which AMS slot each project filament maps to. AMS contents change between prints, so they come from the screen every time. When the filament sync dialog is up, explain the choice before anyone clicks: Mapping pairs each project filament with a loaded one, Direct Override replaces the list with the AMS contents, and either way the original list is gone, so the downloaded file is the only undo.

3. **Choose per plate.** Keep the designer's plate split and part orientation: they encode print order, fit, and which face shows. Walk each part on the plate through Part types below. Done when every proposed change names the part it helps and its cost, read from a slice. Colour-change waste is the Purged plus Tower columns of the slicing result.

4. **Apply under Global** (see The X2D in Bambu Studio for why). Before touching a setting, note the designer's value: that list is the revert list. The user often applies the changes themselves; then check each one on screen afterwards, on the M1 speed tab as well.

5. **Slice and verify in the preview.** Slice the plate, then check in Preview: the layer count against the part height, layer 1 of any bed-face inlay zoomed in until line edges show (bed visible between colours is a gap), where the seams land, and the time and weight. Done when each change from step 3 is visible in the preview, or you have said why it is not.

6. **Hand over the send.** Check the Send print job dialog against Send dialog below. Clicking Send is the user's. Once the plate is sent, give the user the revert list from step 4 for every setting that would hurt another plate; the user reverts it or asks you to.

## The X2D in Bambu Studio

- **Global settings only.** Bambu Studio counts the X2D as a multiple-extruder printer and refuses per-object settings ("the object configuration form cannot be used with a multiple-extruder printer"). A change reaches every plate at its next slice, so a change meant for one plate gets reverted after that plate is sent.
- **Speeds are per nozzle.** The Speed tab has a sub-tab per nozzle: M1 (main) and A1 (auxiliary), each with its own values. Read and set M1 while the Printer panel shows the auxiliary nozzle "Not installed".
- **A second nozzle pays off on many colour changes** (a colour every few layers) or mixed materials. For a handful of changes the purge is a gram or so, less than fitting and offset-calibrating a second hotend is worth.
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
- Outer wall about 120 mm/s on M1 instead of 200, for little extra time.

**Flat faces pointing up:**
- Ironing, set to "Topmost surface", helps only a face that shows once assembled. It slows the plate, and on Matte PLA it leaves a gloss that looks patchy beside unironed areas.

**Fit and function** (pins, press fits, clips):
- X-Y hole and contour compensation stay at the designer's values unless a printed part does not fit; the clearances were sized for them.

On straight-walled parts, variable layer height, fuzzy skin and infill changes add nothing that shows.

## Send dialog

- Plate name, time and weight match the plate just sliced.
- Printer X2D 0.4 mm, and the plate type matches the plate on the bed (the slice assumed it).
- Each filament on the slot read in step 2.
- Flow Dynamics Calibration: On. Auto reuses the last value when the filament has not changed and can skip the measurement.
- Nozzle Offset Calibration: Off while one nozzle is installed.
- Timelapse and Auto Bed Leveling are the user's choice; neither uses filament.

## Driving Bambu Studio

Computer use in background mode works: `request_access` for BambuStudio, then the `app_*` tools on `com.bambulab.bambu-studio`.

- Dialogs (filament sync, Send print job, notices) are separate windows: list them with `app_list_windows` and screenshot by `window_id`.
- A dropdown takes focus on a click but its menu stays shut in the background: step through the options with `app_key` up or down, then screenshot to confirm.
- The "Not available" notice refuses clicks as another process's window: ask the user to press OK.
- Slice plate slices the plate selected in Prepare (the blue box). In Preview, drag the layer slider's top handle to the bottom for layer 1, scroll on the 3D view to zoom, and use `app_zoom` for line detail; tell the user the view was left zoomed.
- Call `app_release` when done so other sessions can capture the app.
