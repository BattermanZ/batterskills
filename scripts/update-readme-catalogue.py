#!/usr/bin/env python3
"""Regenerate the catalogue section of README.md from SKILL.md frontmatter.

Run after adding, moving, renaming, or removing a skill. The section between
the catalogue markers is replaced wholesale; everything else is untouched.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
README = REPO / "README.md"
START = "<!-- catalogue:start -->"
END = "<!-- catalogue:end -->"

TREE_TITLES = {
    "battermanz": "battermanz (original work)",
    "mattpocock": "mattpocock",
    "pstack": "pstack",
    "anthropic": "anthropic",
}


def description(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    m = re.search(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return ""
    fm = re.search(r'^description:\s*(?:"((?:[^"\\]|\\.)*)"|(.+))$', m.group(1), re.M)
    if not fm:
        return ""
    desc = (fm.group(1) or fm.group(2)).strip().strip("'")
    desc = desc.replace('\\"', '"')
    # First sentence only; the SKILL.md has the rest.
    first = re.split(r"(?<=[.!?]) ", desc, maxsplit=1)[0]
    return first


def main() -> int:
    lines = []
    trees = sorted(
        (d for d in (REPO / "skills").iterdir() if d.is_dir()),
        key=lambda d: (d.name != "battermanz", d.name),
    )
    for tree in trees:
        lines.append(f"### {TREE_TITLES.get(tree.name, tree.name)}")
        lines.append("")
        for skill_md in sorted(tree.rglob("SKILL.md")):
            rel = skill_md.parent.relative_to(REPO)
            name = skill_md.parent.name
            lines.append(f"- **[{name}](./{rel}/SKILL.md)**: {description(skill_md)}")
        lines.append("")

    readme = README.read_text(encoding="utf-8")
    if START not in readme or END not in readme:
        print("catalogue markers missing from README.md", file=sys.stderr)
        return 1
    block = f"{START}\n" + "\n".join(lines).rstrip() + f"\n{END}"
    readme = re.sub(re.escape(START) + r".*?" + re.escape(END), block, readme, flags=re.S)
    README.write_text(readme, encoding="utf-8")
    print(f"catalogue refreshed: {sum(1 for _ in (REPO / 'skills').rglob('SKILL.md'))} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
