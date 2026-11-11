---
name: implement-spec
description: "Implement the result of /to-spec and /to-tickets in code."
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

Read the target repo's `AGENTS.md` and `AGENTS.local.md` if present for its issue-tracker instructions and coding-standards pointers. Follow the references they name, at the phases the repo assigns them. Ask the user for a needed pointer only when neither instruction file supplies it. An explicit statement that there is no separate standards document is sufficient.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Gates

These are the same gates `/implement` holds for one ticket, held here for the whole spec. A failed gate blocks every step after it.

- **Guardrails first.** Read every applicable `AGENTS.md`, from the repository root down into the directories the tickets touch. Identify from them how to start or reach the app's live test environment and how to exercise its public interface. A production environment is not a test environment unless the user explicitly authorizes it. If no usable live-test procedure is documented, settle one before any subagent starts, by the rule in [`/implement` step 1](../implement/SKILL.md), judged against every ticket read whole. In short: a fully disposable test runs without asking, any other test waits for the user's approval of the proposed procedure, that one approval covers the whole run, and a procedure that later changes is checked against the rule again. Where that rule says step 4, read step 7 here; where it says step 5, read step 8; where it says the ledger, read the final report. When every ticket looks docs-only, the procedure can wait until step 7 picks the path, as that rule allows: subagents may start without one. If step 7 picks the full-run path instead, settle the procedure by the rule as soon as the path is picked, before the full run.
- **Clean start.** Require a clean worktree and record the starting `HEAD` as the review fixed point. Stop and ask the user to resolve or explicitly include any pre-existing work.
- **Claim before building.** Read each ticket whole, the body and every comment, since the brief and the decisions that reshaped it are often comments. A ticket already assigned to someone needs the user's explicit green light; invoking this skill is not that green light. Assign each ticket to yourself, the way the issue tracker assigns work, when its implementer subagent starts, and verify the assignment took.
- **Live acceptance decides done.** A ticket is resolved, and its checkboxes ticked, only on evidence from the live pass in step 8, or, on the docs-only path, from the text checks and the diff. Passing tests and a clean review are not that evidence.

## Steps

1. Read the spec and every ticket whole, the body and every comment, to understand the task graph. Establish the guardrails and the clean start above.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create the integration branch. If the issue tracker closes work through PRs, or the user asks for one, open a draft PR after the first merge in step 5 (a branch with no commits ahead of main can't open one), marked as closing the spec and tickets.

4. Claim each ticket as it leaves the frontier, then use **implementer subagents** to implement it, each in its own worktree on its own branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - calls the Skill tool with `tdd` to build the ticket;
   - runs the quick checks as it goes, and has them passing before reporting done: typechecking, the formatter and linter where they are fast, and the focused tests around its ticket. It does not run the full suite or any repository-required validation: both wait for step 7;
   - merges the integration branch tip into its own branch before reporting done

5. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**.

6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

7. Once all tickets are complete, call the Skill tool with `code-review` on the integration branch, against the recorded starting `HEAD`, supplying the spec and tickets explicitly. Resolve every actionable finding in a single **implementer subagent**: fix it or record why it does not apply, with the quick checks passing on the fixes. No hard Standards finding, Spec finding, or blocker or major Defects finding may remain unresolved.

   Then decide which path the checks take, the **docs-only path** or the **full-run path**, as [`/implement` step 4](../implement/SKILL.md) defines them, judged on the whole change since the starting `HEAD`. Record the path in the final report.

   **The docs-only path** is for a spec whose change is documentation and nothing else, by the repo's rule or that step's fallback (a skill or a prompt is not documentation under the fallback). Run the repo's fast text checks and every repository-required validation that is not a build or a test suite. Skip the full suite, the dev server and live acceptance, and go on to step 8, which records the skip.

   **The full-run path** is for every other change. Run the full test suite and every repository-required validation once, on the reviewed and fixed integration branch. This run is the gate for live acceptance:
   - The tree holds still while it runs: no merge or edit lands during it. Record `git status --porcelain` and `git diff HEAD | sha256sum` before it starts and compare them when it ends. A run the tree changed under proves nothing: discard its result and run it again.
   - A failure gets a fix through an implementer subagent, and the fix decides what reruns. A fix that only changes formatting, answers a lint finding without changing behaviour, or corrects a test's own mistake reruns only what failed: the failing test, the lint or the format step, not the whole suite. A fix that changes behaviour, a lint fix included, goes back through `code-review` first, so nothing reaches live acceptance unreviewed, and that path ends in a new full run.
   - A failure that passes on an unchanged rerun is a flaky test. Name the test in the final report and take the passing run.
   - The full run is a command of its own. Never chain it with `git commit`, a merge or a push: that only repeats a run that just passed. The repo's own commit-time checks, such as a pre-commit hook, are not chaining: they run as the repo set them, and this skill never bypasses them.

   A repo rule that asks for more wins over both the docs-only path and the rerun of the failed part only: a full suite or a live pass that its `AGENTS.md` requires before every merge still runs.

   The step ends when one full run has passed on a tree that did not change during it, or every failure in it had a fix that changed no behaviour and each failed part has since passed on its rerun. On the docs-only path, it ends when the text checks and those validations pass; a failure there is fixed through an implementer subagent and only the failed check reruns.

8. On the docs-only path, skip this step: record in the final report that the live pass was skipped because the change is docs-only, and go to step 9.

   Otherwise, run final live acceptance yourself, not through a subagent. Start or reach the live test environment the guardrails settled, on the integration branch: the documented one, the disposable one you designed, or the one the user approved. Exercise the changed behaviour through the app's real public interface and verify every acceptance criterion of every ticket. Record the commands, paths, URLs, or other evidence used. When the pass ends, pass or fail, remove any disposable space this run created for it, stop its fixture processes by their saved PIDs, and record that in the final report. If the live pass exposes a defect, fix it through an implementer subagent and return to step 7 before repeating it: the final live pass must exercise the reviewed code. On the full-run path, a failed or skipped live pass blocks every remaining step.

9. Tick each ticket's implementation and acceptance checkboxes, wherever the brief sits, only where the live-pass evidence proves them, or, on the docs-only path, the text checks and the diff. Fetch each ticket again and verify every required checkbox is checked; any unchecked required item blocks the release.

10. Push the integration branch and verify the remote contains it. If a draft PR exists, mark it ready for review. Otherwise, resolve each ticket the way the issue tracker closes work, verify each is closed, and report the integration branch. Follow every repository-specific commit, push and deployment gate in `AGENTS.md`. On any failure, leave the tickets open and report the exact blocking gate.

11. Clean up all **implementer subagent** worktrees.
