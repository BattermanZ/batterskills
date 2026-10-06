---
name: implement
description: "Claim, implement, validate, and ship one issue or spec."
disable-model-invocation: true
---

Implement exactly one issue or spec through to a pushed commit. For issue work, the issue is the completion ledger.

## 1. Establish the guardrails

Read every applicable `AGENTS.md`, from the repository root down into the directories the work touches. Re-check for nested instructions as the implementation surface becomes known.

Before changing code, identify from those instructions how to start or reach the app's live test environment and how to exercise its public interface. A production environment is not a test environment unless the user explicitly authorizes it. If no usable live-test procedure is documented, stop and report the missing guardrail.

Find which issue tracker the repo uses and how to operate it. The repo's instructions say: `AGENTS.md`, the machine-local `AGENTS.local.md`, or `docs/agents/issue-tracker.md`. This skill names no tracker of its own.

Inspect the worktree and branch before claiming the work. Require a clean worktree, record the starting `HEAD` as the review fixed point, and confirm pushing this branch will not include unrelated unpushed commits. Stop and ask the user to resolve or explicitly include any pre-existing work.

## 2. Resolve and claim the work

- **An issue was supplied:** fetch it from the repo's tracker and confirm its title and repository. If it already has any assignee, require the user's explicit green light for that assigned issue; invoking this skill alone is not that green light.
- **No work was supplied:** list the tracker's open issues carrying the `ready-for-agent` label. Exclude assigned issues and issues with open blockers, then choose the oldest eligible issue (lowest issue number). Stop if none is available.
- **The chosen issue is unassigned:** assign it to yourself, the way the tracker assigns work, before editing code, then fetch it again and verify the assignment succeeded.
- **A spec with no issue was supplied:** continue without issue actions.

**Read the ledger whole**: the body and every comment. The brief specifying the work, and the decisions that reshaped it, are often comments, so an issue read from its body alone can miss the contract entirely.

Issue work requires a tracker the repo's instructions name and working access to it. If the instructions name none, or name several without saying which leads, ask the user. If access fails, stop before claiming or changing anything. Do not substitute a tracker the repo did not name.

## 3. Implement and check

Implement the agreed work without reopening its design. Call the Skill tool with "tdd" where possible at pre-agreed seams. Run typechecking and focused tests regularly, then run every repository-required validation and the full test suite.

All automated checks must pass before review.

## 4. Review and fix

Call the Skill tool with "code-review" against the complete change since the recorded starting `HEAD`, including committed, staged, unstaged, and untracked work. Supply the issue or spec explicitly so the Spec axis does not depend on commit messages.

Resolve every actionable finding: fix it or record why it does not apply. Rerun affected focused checks and every repository-required validation. No hard Standards finding or Spec finding may remain unresolved.

## 5. Run final live acceptance

After review fixes, start or reach the documented live test environment. Exercise the changed behaviour through the app's real public interface and verify every applicable acceptance criterion. Record the commands, paths, URLs, or other evidence used.

If live acceptance exposes a defect, fix it and return to automated checks and review before repeating live acceptance. The final live pass must exercise the reviewed code. A failed or skipped live pass blocks every remaining step.

## 6. Complete and ship

For issue work:

1. Check off each implementation or acceptance checkbox only when the live-pass evidence proves it complete. The checkboxes sit wherever the brief does, a comment as readily as the body; tick them in place there.
2. Fetch the issue again, comments included, and verify every required checkbox is checked. Any unchecked required item blocks the release.

Then inspect the final diff, commit only the intended work to the current branch, push that branch, and verify the remote contains the commit. Follow all repository-specific commit, push, deployment, and post-push validation gates in `AGENTS.md`.

Close the issue, the way the tracker closes work, only after validation, checkbox completion, commit, push, and any required post-push checks have all succeeded. Fetch it once more and verify it is closed. On any failure, leave the issue open and report the exact blocking gate.
