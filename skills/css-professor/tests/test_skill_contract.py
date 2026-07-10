"""Behavior-level contract tests for the css-professor skill.

These tests pin down the *contract* the skill promises to its host agent and to
the rest of the repository. They are intentionally stdlib-only (no pytest) so
they run anywhere Python runs:

    python -m unittest skills.css-professor.tests.test_skill_contract
    # or, from this file's directory:
    python -m unittest test_skill_contract

What is checked here is deliberately stronger than scripts/validate.py:
validate.py asserts structural presence (files exist, frontmatter parses).
These tests assert *behavioral expectations*: the description leads with
trigger verbs (EN + ZH), every method branch carries the truth-source rule, the
agent-loop alias no longer leaks a hardcoded Windows path, Depth and Hard Load
Table remain wired, etc. If any of these break, the skill's published promises
stop being true.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]            # .../skills/css-professor
SKILLS_DIR = SKILL_ROOT.parent                              # .../skills
REPO_ROOT = SKILL_ROOT.parents[1]                           # .../know-skills

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _frontmatter(text: str) -> dict[str, str]:
    m = FRONTMATTER_RE.match(text)
    assert m is not None, "SKILL.md must start with YAML frontmatter delimited by ---"
    fields: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"').strip("'").strip()
    return fields


def _load(rel: Path) -> str:
    p = SKILL_ROOT / rel
    assert p.is_file(), f"expected file missing: {p}"
    return p.read_text(encoding="utf-8")


# The eight empirical method branches that the original agent-loop methodology
# owned and that css-professor is supposed to have inherited. If a branch name
# drifts, the inheritance contract has broken and a reviewer would silently lose
# coverage for that method.
EXPECTED_METHOD_BRANCHES = [
    "Text / Corpus Analysis",
    "Qualitative Coding / Digital Ethnography",
    "Network Analysis",
    "Causal Inference / Quasi-Experiment",
    "Survey / Experiment",
    "Simulation / Agent-Based Modeling",
    "Platform / Digital Trace Data",
    "Mixed Methods / Triangulation",
]

# English trigger verbs the description promises near the front (matchers often
# truncate long descriptions).
DESCRIPTION_TRIGGER_TERMS_EN = [
    "explain", "teach", "analyze", "critique",
    "design research questions", "review methods", "frame",
]

# Chinese triggers for the same intent surface; required in description head so
# ZH prompts still route after matcher truncation.
DESCRIPTION_TRIGGER_TERMS_ZH = [
    "解释", "讲解", "分析", "审稿", "选题", "研究设计",
]

# Depth ladder labels that must appear in the main contract.
EXPECTED_DEPTHS = ["Flash", "Class", "Studio", "Review"]


class FrontmatterContract(unittest.TestCase):
    def test_name_matches_directory(self):
        fm = _frontmatter(_load(Path("SKILL.md")))
        self.assertEqual(fm.get("name"), "css-professor")
        self.assertEqual(SKILL_ROOT.name, "css-professor")

    def test_description_is_present_and_bounded(self):
        fm = _frontmatter(_load(Path("SKILL.md")))
        desc = fm.get("description", "")
        self.assertTrue(desc, "description must not be empty")
        self.assertLess(len(desc), 1200, f"description too long ({len(desc)} chars)")

    def test_description_leads_with_english_trigger_terms(self):
        fm = _frontmatter(_load(Path("SKILL.md")))
        desc = fm.get("description", "").lower()
        head = desc[:280]
        missing = [t for t in DESCRIPTION_TRIGGER_TERMS_EN if t not in head]
        self.assertFalse(
            missing,
            f"description head does not mention EN trigger terms: {missing}",
        )

    def test_description_leads_with_chinese_trigger_terms(self):
        fm = _frontmatter(_load(Path("SKILL.md")))
        desc = fm.get("description", "")
        # Chinese does not case-fold; take a generous head of the raw string.
        head = desc[:280]
        missing = [t for t in DESCRIPTION_TRIGGER_TERMS_ZH if t not in head]
        self.assertFalse(
            missing,
            f"description head does not mention ZH trigger terms: {missing}",
        )

    def test_description_states_anti_scope(self):
        fm = _frontmatter(_load(Path("SKILL.md")))
        desc = fm.get("description", "").lower()
        # At least one negative scope signal so matchers can avoid pure-code tasks.
        self.assertTrue(
            "not for" in desc or "coding" in desc,
            "description should signal out-of-scope (e.g. not for pure coding)",
        )


class ResourceCrossReference(unittest.TestCase):
    """Every references/* and assets/* path named in SKILL.md must exist, and
    every reference file shipped must actually be referenced from SKILL.md.

    This catches two regressions: orphans (file on disk, never loaded) and
    dangling pointers (path mentioned, file missing)."""

    def test_referenced_resources_exist(self):
        text = _load(Path("SKILL.md"))
        referenced = set(re.findall(r"`((?:references|assets)/[^`]+)`", text))
        self.assertTrue(referenced, "SKILL.md should reference at least one resource")
        for rel in referenced:
            self.assertTrue(
                (SKILL_ROOT / rel).exists(),
                f"SKILL.md references '{rel}' but it does not exist",
            )

    def test_all_reference_files_are_referenced(self):
        text = _load(Path("SKILL.md"))
        referenced = set(re.findall(r"`((?:references|assets)/[^`]+)`", text))
        shipped: list[str] = [
            p.relative_to(SKILL_ROOT).as_posix()
            for sub in ("references", "assets")
            for p in (SKILL_ROOT / sub).rglob("*") if p.is_file()
        ]
        orphans = [s for s in shipped if s not in referenced]
        self.assertFalse(
            orphans,
            f"resource files exist on disk but SKILL.md never loads them: {orphans}",
        )


class MethodBranchesInheritance(unittest.TestCase):
    """The whole point of the css-professor / agent-loop merge was to carry the
    8 method-specific evidence rules forward. These tests guard that."""

    def test_all_eight_branches_present(self):
        text = _load(Path("references/method-branches.md"))
        headers = re.findall(r"^## (.+)$", text, re.MULTILINE)
        for branch in EXPECTED_METHOD_BRANCHES:
            self.assertIn(branch, headers, f"method branch missing: {branch}")

    def test_each_branch_states_truth_source_rule(self):
        text = _load(Path("references/method-branches.md"))
        blocks = re.split(r"^## ", text, flags=re.MULTILINE)[1:]
        self.assertGreaterEqual(len(blocks), 8)
        for block in blocks:
            title = block.splitlines()[0].strip()
            if title.startswith("How To Use"):
                continue
            self.assertIn(
                "truth source",
                block.lower(),
                f"branch '{title}' does not state its truth source",
            )

    def test_branches_define_unacceptable_evidence(self):
        text = _load(Path("references/method-branches.md"))
        blocks = re.split(r"^## ", text, flags=re.MULTILINE)[1:]
        for block in blocks:
            title = block.splitlines()[0].strip()
            if title.startswith("How To Use"):
                continue
            self.assertIn(
                "unacceptable evidence",
                block.lower(),
                f"branch '{title}' does not name unacceptable evidence",
            )

    def test_truth_source_vs_artifact_rule_stated_up_front(self):
        text = _load(Path("references/method-branches.md"))
        first_branch = text.index("## Text / Corpus Analysis")
        preamble = text[:first_branch].lower()
        self.assertIn("truth source", preamble)
        self.assertIn("measurement artifact", preamble)

    def test_branch_only_load_must_rule(self):
        text = _load(Path("references/method-branches.md")).lower()
        self.assertIn("matching branch", text)
        self.assertIn("not this whole file", text)


class SkillBodyContract(unittest.TestCase):
    def test_truth_source_rule_appears_in_main_skill(self):
        text = _load(Path("SKILL.md")).lower()
        self.assertIn("truth source", text)

    def test_method_branches_wired_into_reviewer_mode(self):
        text = _load(Path("SKILL.md"))
        self.assertIn("references/method-branches.md", text)
        self.assertIn("Methodology Reviewer", text)

    def test_quality_bar_distinguishes_artifacts(self):
        text = _load(Path("SKILL.md")).lower()
        self.assertIn("measurement artifact", text)

    def test_depth_ladder_present(self):
        text = _load(Path("SKILL.md"))
        self.assertIn("## Depth", text)
        for depth in EXPECTED_DEPTHS:
            self.assertIn(depth, text, f"Depth ladder missing level: {depth}")

    def test_hard_load_table_present(self):
        text = _load(Path("SKILL.md"))
        self.assertIn("## Hard Load Table", text)
        # Review path must require method-branches; Flash must not force loads.
        self.assertIn("matching branch only", text.lower())
        self.assertRegex(text, r"Flash.*None|None beyond this file", re.I | re.S)

    def test_anti_triggers_section_present(self):
        text = _load(Path("SKILL.md"))
        self.assertIn("## Anti-Triggers", text)
        self.assertIn("book-to-skill", text)
        self.assertIn("lineage-skill", text)


class TemplateDepthContract(unittest.TestCase):
    def test_template_has_depth_gates(self):
        text = _load(Path("assets/professor-answer-template.md"))
        self.assertIn("Depth gates", text)
        for depth in ("Class", "Studio", "Review"):
            self.assertIn(depth, text)
        self.assertIn("Flash never uses this file", text)

    def test_template_requires_truth_source_on_review(self):
        text = _load(Path("assets/professor-answer-template.md")).lower()
        self.assertIn("truth source", text)


class ExamplesContract(unittest.TestCase):
    def test_examples_cover_anti_triggers_and_depth(self):
        text = _load(Path("references/examples.md"))
        self.assertIn("Anti-trigger", text)
        self.assertIn("Depth inflation guard", text)
        self.assertIn("Flash depth", text)
        self.assertIn("lineage-skill", text)

    def test_examples_mention_mode_and_depth(self):
        text = _load(Path("references/examples.md"))
        self.assertIn("Depth: Review", text)
        self.assertIn("Depth: Studio", text)
        self.assertIn("Depth: Class", text)
        self.assertIn("Depth: Flash", text)


class AgentLoopAliasRegression(unittest.TestCase):
    """The agent-loop alias used to ship a hardcoded Windows absolute path
    (C:\\Users\\AD\\...) that broke on any other machine. Don't let it come
    back, and don't let the deleted legacy resources be re-referenced."""

    ALIAS = SKILLS_DIR / "agent-loop" / "SKILL.md"

    def test_alias_exists(self):
        self.assertTrue(self.ALIAS.is_file(), "agent-loop compatibility entry must exist")

    def test_no_hardcoded_absolute_path(self):
        text = self.ALIAS.read_text(encoding="utf-8")
        self.assertNotRegex(
            text,
            r"[A-Za-z]:\\Users\\",
            "agent-loop SKILL.md contains a hardcoded Windows user path",
        )
        self.assertNotRegex(
            text,
            r"/Users/[^/]+/\.agents",
            "agent-loop SKILL.md contains a hardcoded macOS/Linux home path",
        )

    def test_alias_routes_to_css_professor_by_name(self):
        text = self.ALIAS.read_text(encoding="utf-8")
        self.assertIn("css-professor", text)

    def test_alias_does_not_load_retired_resources(self):
        text = self.ALIAS.read_text(encoding="utf-8")
        retired = [
            "loop-template.md",
            "references/review-checklist.md",
            "references/example-loops.md",
            "references/method-branches.md",
        ]
        for path in retired:
            self.assertNotIn(
                f"`{path}`",
                text,
                f"agent-loop marks retired resource '{path}' as loadable",
            )

    def test_alias_legacy_files_actually_gone(self):
        for rel in [
            "assets/loop-template.md",
            "references/review-checklist.md",
            "references/example-loops.md",
            "references/method-branches.md",
        ]:
            self.assertFalse(
                (SKILLS_DIR / "agent-loop" / rel).exists(),
                f"retired legacy file still present: agent-loop/{rel}",
            )


class ValidateScriptContract(unittest.TestCase):
    """The structural validator must agree with reality — if it ships, it must
    pass on the skills it claims to validate."""

    def test_validate_script_runs_clean(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, str(SKILL_ROOT / "scripts" / "validate.py")],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(
            result.returncode, 0,
            f"validate.py failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("css-professor", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
