---
name: implement-spec
description: "Implement the result of /to-spec and /to-tickets in code."
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The issue tracker should have been provided to you. If not, read the target repo's instructions (`AGENTS.md`, `AGENTS.local.md`, `docs/agents/issue-tracker.md`); when none names a tracker, ask the user which to use.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Gates

These are the same gates `/implement` holds for one ticket, held here for the whole spec. A failed gate blocks every step after it.

- **Guardrails first.** Read every applicable `AGENTS.md`, from the repository root down into the directories the tickets touch. Identify from them how to start or reach the app's live test environment and how to exercise its public interface. A production environment is not a test environment unless the user explicitly authorizes it. If no usable live-test procedure is documented, stop and report the missing guardrail before any subagent starts.
- **Clean start.** Require a clean worktree and record the starting `HEAD` as the review fixed point. Stop and ask the user to resolve or explicitly include any pre-existing work.
- **Claim before building.** Read each ticket whole, the body and every comment, since the brief and the decisions that reshaped it are often comments. A ticket already assigned to someone needs the user's explicit green light; invoking this skill is not that green light. Assign each ticket to yourself, the way the issue tracker assigns work, when its implementer subagent starts, and verify the assignment took.
- **Live acceptance decides done.** A ticket is resolved, and its checkboxes ticked, only on evidence from the live pass in step 8. Passing tests and a clean review are not that evidence.

## Steps

1. Read the spec and tickets to understand the task graph. Establish the guardrails and the clean start above.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create the integration branch. If the issue tracker closes work through PRs, or the user asks for one, open a draft PR after the first merge in step 5 (a branch with no commits ahead of main can't open one), marked as closing the spec and tickets.

4. Claim each ticket as it leaves the frontier, then use **implementer subagents** to implement it, each in its own worktree on its own branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - calls the Skill tool with `tdd` to build the ticket;
   - runs the quick checks as it goes, and has them passing before reporting done: typechecking, the formatter and linter where they are fast, and the focused tests around its ticket. The full suite and every repository-required validation wait for step 7;
   - merges the integration branch tip into its own branch before reporting done

5. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**.

6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

7. Once all tickets are complete, call the Skill tool with `code-review` on the integration branch, against the recorded starting `HEAD`, supplying the spec and tickets explicitly. Resolve every actionable finding in a single **implementer subagent**: fix it or record why it does not apply, with the quick checks passing on the fixes. No hard Standards finding, Spec finding, or blocker or major Defects finding may remain unresolved.

   Then run the full test suite and every repository-required validation on the reviewed and fixed integration branch. This run is the gate for live acceptance:
   - The tree holds still while it runs: no merge or edit lands during it. Record `git status --porcelain` and `git diff HEAD | sha256sum` before it starts and compare them when it ends. A run the tree changed under proves nothing: discard its result and run it again.
   - A failure is fixed through an implementer subagent and the full run repeated. A fix that only changes formatting, answers a lint finding, or corrects a test's own mistake goes straight back to the full run. A fix that changes behaviour goes back through `code-review` first, so nothing reaches live acceptance unreviewed.
   - A failure that passes on an unchanged rerun is a flaky test. Name the test in the final report and take the passing run.

   The step ends when one full run passes on a tree that did not change during it.

8. Run final live acceptance yourself, not through a subagent. Start or reach the documented live test environment on the integration branch, exercise the changed behaviour through the app's real public interface, and verify every acceptance criterion of every ticket. Record the commands, paths, URLs, or other evidence used. If the live pass exposes a defect, fix it through an implementer subagent and return to step 7 before repeating it: the final live pass must exercise the reviewed code.

9. Tick each ticket's implementation and acceptance checkboxes, wherever the brief sits, only where the live-pass evidence proves them. Fetch each ticket again and verify every required checkbox is checked; any unchecked required item blocks the release.

10. Push the integration branch and verify the remote contains it. If a draft PR exists, mark it ready for review. Otherwise, resolve each ticket the way the issue tracker closes work, verify each is closed, and report the integration branch. Follow every repository-specific commit, push and deployment gate in `AGENTS.md`. On any failure, leave the tickets open and report the exact blocking gate.

11. Clean up all **implementer subagent** worktrees.
