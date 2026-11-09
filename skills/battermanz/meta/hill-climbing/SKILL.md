---
name: hill-climbing
description: Improve one thing in rounds of fix, check and score until it reaches a target, keeping the best version.
disable-model-invocation: true
metadata:
  version: "1.0.0"
---

# Hill climbing

Version 1.0.0.

A **hill climb** improves one thing in **rounds**. Each round fixes, checks, saves and scores, and the run keeps the **best version** so far. The thing can be anything with a score: a web page, a form, a document, a prompt, a script.

The design comes from a run on 2026-11-08, which spent five rounds on a wedding site with a target of 9.0 in seven categories and one grader per round. It never got there. From round 3 on, two graders scoring the same site disagreed by more than a round of fixes changed. Rules also arrived mid-run, and nothing recorded which version was best. Every step below answers one of those failures.

## Words

- **Score**: the number a round is judged by, per category. A **measured** score (tests passing, load time, a count, a price) comes out the same every time. A **graded** score is an agent's 1-to-10 with one decimal, for taste. Prefer a measured score whenever one exists.
- **Improves** means moves the good way for that category: up for a grade or a pass count, down for a load time or a price. **Worsens** is the opposite.
- **Grader**: the fresh agent that produces a graded score. A new one every round, on the same **frozen brief**.
- **Wobble**: how far the score moves with nothing changed. A move inside the wobble is noise, never progress.
- **Reference examples**: things the user points at with a score each ("this site is a 9 to me"). They set what the scale means, and only the user sets them.
- **Best version**: the version the judging rules in step 4 last crowned, with its commit or saved copy.
- **Parked question**: anything that needs the user mid-run. The agent notes it in the log, works around it, and carries on.

## 1. Setup

Read the project first: its `AGENTS.md` and other instruction files, its checks (tests, build, screenshot tools), how to run or view the thing, and what a push sets off (some repos deploy on push). Those are facts to find, never questions.

Then ask the setup in **one message**, each item with your recommended answer, so the user can accept them all at once:

1. **The thing and its edges**: what is improved, and what is out of scope.
2. **The score**: the categories, a line on what each means, and for a measurement how it runs and which way is better.
3. **Reference examples** (graded only): things to point at, each with the user's score. "None" is a valid answer.
4. **Rules**: what must not change (fonts, wording, data), what the grader skips (unwritten content, an admin page), which stand-ins are allowed for missing content, and side effects the grader must avoid (real emails, payments, live data).
5. **Target and cap**: the score to reach, and the most rounds to run. Default cap: 5.
6. **Saving**: commit each round, or commit and push. Say what a push sets off in this project.

Setup is done when every item has an answer or an accepted default, written into the log.

## 2. The frozen brief (graded only)

Write the grader's brief from [`references/grader-brief.md`](references/grader-brief.md) and save it in the log. From then on every round's grader gets it **word for word**, with only the round folder changed.

The user can step in at any time. A rule they add mid-run adds one line to the brief, and the log records the round it joined. The scores before and after that line measure different things, so the next round is not judged: its scores become the new reference, and its version the best version.

## 3. Round 0: measure the wobble

1. Run the project's checks on the untouched thing, and note any that already fail. Those are not this run's to fix, and they never hold a round back.
2. Score the untouched thing **twice**, with two separate graders or two runs of the measurement.
3. The **starting score** is the average of the two. The **wobble** is the largest gap between the two scores in any category. For a graded score, use at least 0.3, because two samples understate the noise. A measurement that gives the same number twice has a wobble of 0.

Round 0 is the first best version.

## 4. Rounds

Each round counts toward the cap, and runs these steps in order:

1. **Fix.** Work from the latest score's findings, and make every fix that fits the rules. A finding that needs the user (content, a choice, a purchase) becomes a parked question; use an allowed stand-in or leave it.
2. **Check.** Run the project's checks. Score the round once every check that passed in round 0 passes again. A change that breaks a check and cannot be fixed this round gets undone, and the rest of the round goes on.
3. **Save** the thing: commit, or save a dated copy outside a repo. Fix history with a new commit; never rewrite one.
4. **Score.** A fresh grader on the frozen brief, writing to this round's folder, with the same model and effort every round. Or run the measurement.
5. **Judge** the round against the best version, category by category, taking the first rule that fits:
   - **Target reached**: every category at the target. A category that reached it in an earlier round still counts while a graded score dips below it by 0.1 or less. This round becomes the best version, and the run stops.
   - **Better**: at least one category improves by more than the wobble, and none worsens by more than the wobble. This round becomes the best version.
   - **Worse**: any category worsens by more than the wobble. If this round's findings name the cause (something the round changed or broke), the next round fixes it first. If they name none, the drop may be one grader's bad draw: score the same version once more with a fresh grader (a measurement needs no second run). If the second score is no longer Worse, judge the round on it instead. If it is still Worse, restore the thing's files to the best version with a new commit, or copy back the best version's dated copy, and try different fixes next round. A restore leaves the log and the grader reports in place.
   - **Level**: anything else. Keep the round; the best version stays where it is.
6. **Record.** Add the round's row and grader report to the log, commit it, and push if setup said so. Give the user one line: round number, scores, verdict, best version.
7. **Stop check** (section 5). If no signal fires, start the next round.

## 5. Stop signals

Stop at the first of these, and name it in the final report:

- **Target reached**, as judged in step 4.
- **Round cap** reached.
- **Plateau**: two rounds in a row where no category improves by more than the wobble against the round before.
- **Only the user's part left**: every finding still holding the score down is a parked question.

## 6. Final report

- The stop signal that fired.
- The score table: round 0 and every round, with each round's verdict.
- The best version and its commit or copy. If the last round is not the best version, say so and offer to restore it; restoring waits for a yes.
- With no reference examples, a plain warning that the scores are only as steady as the wobble, with its number.
- The parked questions, each with what answering it would raise.
- What no grader could check (a real phone, a real mail app, a slow connection).

## The log

One Markdown file per run, the record a later session reads instead of the transcript. In a repo it lives at `hill-climbing/<YYYY-MM-DD>-<topic>/log.md`. Outside a repo it goes in the same folder in the working directory, beside the dated copies.

It holds the skill's version from the top of this file, the setup answers, the frozen brief and each later rule with the round it joined, the round 0 checks and wobble, and one row per round (scores, verdict, commit). It also holds the best version, the parked questions, and the stop signal. Each round's grader report goes beside it as `round-<n>.md`.
