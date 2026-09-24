---
name: effort-store
description: Durable cross-session storage for a skill's effort notes. Reach it when a consumer skill says to load the effort store, or to find, open, write, update or register an effort.
metadata:
  version: "1.0.0"
---

# effort-store

An **effort** is a named set of notes produced by one run of a consumer skill: a purchase hunt's requirements and shortlist, a research question's dossier. The notes only make sense together, so they live together, and a later session must be able to find them and pick the work back up. This skill is the contract between consumer skills and wherever the notes physically live.

## What a consumer declares

A consumer skill's own document declares two things, once:

- Its **root**: one word naming where its efforts live (`purchases`). The backend decides what the root maps to.
- Its **note set**: the notes an effort of this kind contains, by name.

An effort's name is the subject in a few words, no date: `Stand mixer`, not `2026-09-12 - Stand mixer`. Only a dated sibling of a superseded effort carries a date.

## Operations

- **find**: search the consumer's root for an effort on this subject. Return its notes, or nothing. Consumers call this before planning, so a re-run is recognised instead of restarted.
- **open**: create the effort's container.
- **write**: create a note inside the effort. Every note records the date, the producing skill and its version, so the effort stays legible a year later.
- **update**: every change to an existing note. Earlier runs stay readable in place: a fresh pass adds a dated section rather than replacing what an old one wrote.
- **register**: after the last write: link the effort into whatever index the backend keeps, and report every note written, each one clickable.

Two rules bind every backend:

- An existing effort is continued or given a dated sibling, never silently replaced. Decide which case applies and say so before writing, so the user can overrule.
- Write early. Open the effort and store the settled inputs before any expensive phase, so a killed session recovers by reading notes instead of re-asking the user.

## Backends

**Adapter first.** If this environment has an effort-store adapter skill (a skill whose description names the effort store), load it: it owns the mapping of roots and all five operations. Everything above still binds; the adapter only decides where and how.

**Markdown fallback** otherwise. Efforts live under `~/efforts/<root>/<Effort>/`, one plain `.md` file per note, unless the user names a different base directory. **find** is a listing and grep of that tree; **register** is a closing message listing each file's path.
