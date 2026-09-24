This is batterskills, a personal agent-skills collection consumed by symlink and by checkout on other hosts. A push to `main` is what propagates a change beyond this machine.

## Layout rules

Skills live under `skills/<provenance>/`, where the first level says where a skill came from:

- `battermanz/`: original work, organised by domain (`vault/`, `writing/`, `personal/`, `meta/`). A new skill goes in the domain it fits; add a new domain folder only when none fits.
- `mattpocock/`, `pstack/`, `anthropic/`: third-party trees. Each mirrors its author's own repo layout so porting stays a clean diff, and each has a README at its root naming the author, source URL, license, and sync point. Keep that README accurate when porting.

A third-party import goes in its author's tree (create one for a new author), keeps the author's license file, and records the source and copy date (a `SOURCE.md` in the skill dir, as `pstack/unslop` does). Adjusting an imported skill in place is fine; the git history against the import commit is the record of divergence.

Porting upstream changes is manual and per skill: diff the author's repo against their tree here. Never merge an upstream wholesale; the `upstream` git remote exists only as a reference for cherry-picking.

Skill directory names must be unique across the whole tree: `link-skills.sh` links flat by basename.

## After changing skills

- Run `scripts/link-skills.sh` to refresh the harness symlinks (`~/.claude/skills`, `~/.agents/skills`). It skips `misc/` on purpose and never prunes, so after a rename or removal, delete the dangling links it leaves behind.
- Run `scripts/update-readme-catalogue.py` to refresh the README catalogue.
- Keep each bucket README (where the author's layout has them) in step with the bucket's contents.
- `battermanz/meta/ask-me` is the router over the user-reachable skills: when a skill is added, renamed, removed, or changes how it fits the flows, update it, since a router that lies is worse than none.

Every `SKILL.md` is either user-invoked (`disable-model-invocation: true` plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`) or model-invoked.

Every skill under `battermanz/` carries a version, starting at `"1.0.0"` in the commit that adds it; third-party skills carry none, since their author's repo is their history. The version lives in frontmatter as `metadata.version`, a quoted string (`"1.2.0"`), per the Agent Skills spec. Frontmatter never reaches the model when a skill runs, so a skill that stamps its version into what it writes also carries `Version 1.2.0.` under its H1; bump both together. Bump the patch for a correction that changes what a skill does without adding a rule (a stale name, a wrong path), the minor for a new or dropped rule or a new required output, and the major when the flow itself is reshaped. A change to punctuation or wording alone bumps nothing. Git log carries what changed and why, so no skill holds a changelog.

There is no plugin, marketplace, changesets, or release machinery here, deliberately; do not reintroduce any of it.

No em-dashes anywhere in this repo's prose. Where a sentence reaches for one, rewrite it with a comma, colon, period, parentheses, or a conjunction, whichever the sentence actually wants.
