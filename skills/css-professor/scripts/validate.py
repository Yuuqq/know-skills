#!/usr/bin/env python3
"""Minimal structural validator for css-professor (and sibling skills).

Checks:
1. SKILL.md exists and starts with YAML frontmatter delimited by `---`.
2. Frontmatter contains non-empty `name` and `description`.
3. Every resource path mentioned in SKILL.md (lines like
   `references/foo.md` or `assets/bar.md`) resolves relative to the skill root.
4. (css-professor only) The four declared references and one asset exist.

Usage:
    python skills/css-professor/scripts/validate.py                 # default: css-professor
    python skills/css-professor/scripts/validate.py <skill-dir>     # any skill dir

Exits non-zero on any failure. No third-party dependencies.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
RESOURCE_RE = re.compile(r"`((?:references|assets)/[^`]+)`")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fields: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip().strip('"').strip("'").strip()
        fields[key.strip()] = value
    return fields


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_md} does not exist or is not a file"]

    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append(f"{skill_md}: missing YAML frontmatter (--- ... ---)")
        return errors

    for field in ("name", "description"):
        if not fm.get(field):
            errors.append(f"{skill_md}: frontmatter field '{field}' is missing or empty")

    # Check every references/* and assets/* path mentioned in the body.
    for rel in RESOURCE_RE.findall(text):
        target = skill_dir / rel
        if not target.exists():
            errors.append(f"{skill_md}: referenced resource '{rel}' not found at {target}")

    # css-professor owns a fixed set of declared resources; verify them explicitly.
    if skill_dir.name == "css-professor":
        declared = [
            "assets/professor-answer-template.md",
            "references/quality-checklist.md",
            "references/method-branches.md",
            "references/examples.md",
            "references/chinese-academic-style.md",
        ]
        for rel in declared:
            if not (skill_dir / rel).is_file():
                errors.append(f"{skill_dir}: declared resource '{rel}' missing")

    return errors


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parents[3]
    if len(argv) > 1:
        skill_dirs = [Path(argv[1]).resolve()]
    else:
        skill_dirs = [
            (repo_root / "skills" / "css-professor").resolve(),
            (repo_root / "skills" / "agent-loop").resolve(),
        ]

    all_errors: list[str] = []
    for d in skill_dirs:
        errs = validate(d)
        if errs:
            all_errors.extend(f"[{d.name}] {e}" for e in errs)
        else:
            print(f"OK  {d.name}: frontmatter + resources valid")

    if all_errors:
        print("\nFAIL:")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print("\nAll skills valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
