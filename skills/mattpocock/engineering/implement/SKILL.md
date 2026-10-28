---
name: implement
description: "Claim, implement, validate, and ship one issue or spec."
disable-model-invocation: true
---

Implement exactly one issue or spec through to a pushed commit. For issue work, the issue is the completion ledger.

## Work found outside the ticket

Anything the work turns up that needs doing but lies outside the issue or spec is a follow-up: a defect, or work the change made due, such as instructions, docs, a release step or a caller that depends on what changed. File each follow-up yourself as soon as it is clear, at any step; the final report names what you filed.

1. **Reproduce a defect once and keep the reproduction**: the command or steps, what they showed, the files whose code they exercise, and the commit they ran at, noting any uncommitted change the worktree held then. A follow-up with nothing to reproduce skips this.
2. **File it in the repo's tracker**, following the repo's own rules for tickets an agent writes, a public tracker's included. It carries the reproduction, an agent brief in the form [triage's AGENT-BRIEF.md](../triage/AGENT-BRIEF.md) sets out (naming the cause when you know it), and the repo's label for awaiting the maintainer's approval (`needs-triage` by default). Fetch it back to confirm it exists with that label, and record its number in this issue's ledger, or in the final report for spec work. When the repo names no tracker, list the follow-up in the final report instead.
3. **Carry on with this ticket without fixing it**, unless the user says to fold it into the same change.

## 1. Establish the guardrails

Read every applicable `AGENTS.md`, from the repository root down into the directories the work touches. Re-check for nested instructions as the implementation surface becomes known.

Before changing code, identify from those instructions how to start or reach the app's live test environment and how to exercise its public interface. A production environment is not a test environment unless the user explicitly authorizes it. If no usable live-test procedure is documented, stop and report the missing guardrail.

Find which issue tracker the repo uses and how to operate it. The repo's instructions say: `AGENTS.md`, the machine-local `AGENTS.local.md`, or `docs/agents/issue-tracker.md`. This skill names no tracker of its own.

Inspect the worktree and branch before claiming the work. On a clean worktree, record the starting `HEAD` as the review fixed point and confirm pushing this branch will not include unrelated unpushed commits. If the current branch is not the repo's default branch, record the default branch too: step 6 merges the work into it, so the branch must carry nothing but this work on top of the default branch.

A dirty worktree is a **handover** or a stop. It is a handover when all three hold:

- every uncommitted file belongs to one issue, and that issue is assigned to you;
- that issue's ledger records the automated checks, the review and the live pass as done;
- no uncommitted file was modified after that record was written.

On a handover, resume that issue at step 6. Its ledger is the evidence: the checks, the review and the live pass stand as recorded. Ask the user only for what the ledger still shows outstanding, such as a check on their own device. Once it has shipped, start any further work from step 1 on the clean worktree.

Anything else is a stop: ask the user to resolve or explicitly include the pre-existing work.

## 2. Resolve and claim the work

- **An issue was supplied:** fetch it from the repo's tracker and confirm its title and repository. If it already has any assignee, require the user's explicit green light for that assigned issue; invoking this skill alone is not that green light.
- **No work was supplied:** list the tracker's open issues carrying the `ready-for-agent` label. Exclude assigned issues and issues with open blockers, then choose the oldest eligible issue (lowest issue number). Stop if none is available.
- **The chosen issue is unassigned:** assign it to yourself, the way the tracker assigns work, before editing code, then fetch it again and verify the assignment succeeded.
- **A spec with no issue was supplied:** continue without issue actions.

**Read the ledger whole**: the body and every comment. The brief specifying the work, and the decisions that reshaped it, are often comments, so an issue read from its body alone can miss the contract entirely.

Issue work requires a tracker the repo's instructions name and working access to it. If the instructions name none, or name several without saying which leads, ask the user. If access fails, stop before claiming or changing anything. Do not substitute a tracker the repo did not name.

## 3. Implement and check

Implement the agreed work without reopening its design. Call the Skill tool with "tdd" where possible at pre-agreed seams. A bug whose ledger records a reproduction starts its fix from that reproduction, with no fresh one first; the failing test the fix begins from is part of the fix. As you go, run the quick checks: typechecking, the formatter and linter where they are fast, and the focused tests around the change.

This step ends when the quick checks pass. The full test suite and every repository-required validation wait for step 4, after the review fixes.

## 4. Review, fix and run the full checks

Call the Skill tool with "code-review" against the complete change since the recorded starting `HEAD`, including committed, staged, unstaged, and untracked work. Supply the issue or spec explicitly so the Spec axis does not depend on commit messages.

Resolve every actionable finding: fix it or record why it does not apply, and rerun the quick checks the fixes touch. No hard Standards finding, Spec finding, or blocker or major Defects finding may remain unresolved.

Then run the full test suite and every repository-required validation on the reviewed and fixed code. This run is the gate for live acceptance:

- **The tree holds still while it runs.** Land no edit during the run. Record `git status --porcelain` and `git diff HEAD | sha256sum` before it starts and compare them when it ends. A run the tree changed under proves nothing: discard its result and run it again.
- **A failure is fixed and the full run repeated.** A fix that only changes formatting, answers a lint finding, or corrects a test's own mistake goes straight back to the full run. A fix that changes behaviour goes back through "code-review" first, so nothing reaches live acceptance unreviewed.
- **A failure that passes on an unchanged rerun is a flaky test.** Name the test in the ledger, or in the final report for spec work, and take the passing run.

The step ends when one full run passes on a tree that did not change during it.

## 5. Run final live acceptance

Once step 4's full run has passed, start or reach the documented live test environment. Exercise the changed behaviour through the app's real public interface and verify every applicable acceptance criterion. Record the commands, paths, URLs, or other evidence used.

If live acceptance exposes a defect, fix it with the quick checks and return to step 4 before repeating live acceptance. The final live pass must exercise the reviewed code. A failed or skipped live pass blocks every remaining step.

## 6. Complete and ship

For issue work:

1. Check off each implementation or acceptance checkbox only when the live-pass evidence proves it complete. The checkboxes sit wherever the brief does, a comment as readily as the body; tick them in place there.
2. Fetch the issue again, comments included, and verify every required checkbox is checked. Any unchecked required item blocks the release.

Then inspect the final diff, commit only the intended work to the current branch, push that branch, and verify the remote contains the commit. Follow all repository-specific commit, push, deployment, and post-push validation gates in `AGENTS.md`.

If the work sits on a branch other than the default branch, merge it in and delete it:

1. Fetch the remote. Merge the work branch into the default branch, fast-forward when the default branch has not moved, a merge commit when it has. A conflict is a stop: abort the merge, leave both branches as they are, and report it.
2. When the merge was not a fast-forward, rerun every repository-required validation on the merged result before pushing it.
3. Push the default branch and verify the remote contains the merge.
4. Delete the work branch on the remote and locally. If it is checked out in a worktree you created for this work, remove that worktree first. A branch with an open pull request gets that pull request closed as merged by the tracker, or closed by you with a comment pointing at the merge commit.

Where the repo's instructions require a different landing path, such as merging only through a reviewed pull request, follow them instead and report what is left for a human.

Close the issue, the way the tracker closes work, only after validation, checkbox completion, commit, push, the merge and branch deletion, and any required post-push checks have all succeeded. Fetch it once more and verify it is closed. On any failure, leave the issue open and report the exact blocking gate.

## 7. Offer the follow-ups

Once the work has shipped, ask one question per follow-up filed during this run, one per turn: start #N now, fold it into later work, or leave it.

- **Start**: replace its awaiting-approval label with the repo's `ready-for-agent` label, and hand it to `ticket-queue 1 <N>` so it runs in a fresh session, never in this one's context. From a Herdr pane (`HERDR_ENV=1`), call the Skill tool with "herdr", split a new pane in the checkout, and run `ticket-queue 1 <N>` there once the checkout is back on its integration branch with a clean tree. The step ends when that pane shows the queue's line for the ticket, `[queue <time>] #<N> (pile named): <title>`. Outside Herdr, the report gives the user `ticket-queue 1 <N>` to run from a Herdr pane in the checkout.
- **Fold it in later** or **leave it**: the ticket stays as filed. Report which.

Inside a ticket-queue run (its prompt names a status file), ask before writing the `shipped` line, because the queue closes the pane once it reads it, and start no second queue on the same checkout: the label is the hand-off, and a queue choosing its own tickets takes #N in its turn. The report says so, and gives `ticket-queue 1 <N>` for after the queue ends, since a queue given named issues never chooses. Where ticket-queue does not serve the repo (it needs a GitHub checkout with a `dev` or `development` branch, as Kamosu and Hatchdoor have), the label is still set, and the report gives the user `/implement <N>` to run in a fresh session.
