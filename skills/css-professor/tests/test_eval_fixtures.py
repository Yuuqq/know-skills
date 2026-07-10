"""Static eval-fixture contract for css-professor.

These tests do NOT call a model. They pin the offline rubric inventory so that:

1. Every golden prompt has complete, typed metadata.
2. Mode × Depth coverage does not silently shrink.
3. Anti-triggers and Review truth-source expectations stay explicit.
4. must_load paths resolve to real resources under the skill root.

Run:

    python -m unittest skills.css-professor.tests.test_eval_fixtures
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_PATH = Path(__file__).resolve().parent / "fixtures" / "golden_prompts.json"

# Minimum coverage the suite promises. Shrinking below these counts is a
# regression even if individual fixtures remain well-formed.
MIN_FIXTURES = 10
REQUIRED_DEPTHS = {"Flash", "Class", "Studio", "Review", "Minimal"}
REQUIRED_MODES = {
    "Classroom Teacher",
    "Research Mentor",
    "Methodology Reviewer",
    "Blended",
    "Anti-trigger",
}
REQUIRED_IDS = {
    "flash-bayes-zh",
    "class-algo-public-sphere-zh",
    "studio-shortvideo-politics-zh",
    "review-weibo-rumor-trust-zh",
    "anti-pure-coding",
    "anti-lineage-pipeline",
    "class-selection-bias-zh",
}


def _load_bundle() -> dict:
    assert FIXTURES_PATH.is_file(), f"missing fixtures file: {FIXTURES_PATH}"
    data = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert "fixtures" in data and isinstance(data["fixtures"], list)
    return data


class FixtureInventory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = _load_bundle()
        cls.fixtures = cls.bundle["fixtures"]
        cls.allowed_modes = set(cls.bundle.get("allowed_modes", []))
        cls.allowed_depths = set(cls.bundle.get("allowed_depths", []))

    def test_minimum_count(self):
        self.assertGreaterEqual(
            len(self.fixtures),
            MIN_FIXTURES,
            f"expected at least {MIN_FIXTURES} fixtures, got {len(self.fixtures)}",
        )

    def test_ids_unique(self):
        ids = [f["id"] for f in self.fixtures]
        self.assertEqual(len(ids), len(set(ids)), f"duplicate fixture ids: {ids}")

    def test_required_ids_present(self):
        have = {f["id"] for f in self.fixtures}
        missing = REQUIRED_IDS - have
        self.assertFalse(missing, f"required fixture ids missing: {missing}")

    def test_mode_coverage(self):
        modes = {f["expected_mode"] for f in self.fixtures}
        missing = REQUIRED_MODES - modes
        self.assertFalse(missing, f"mode coverage gaps: {missing}")

    def test_depth_coverage(self):
        depths = {f["expected_depth"] for f in self.fixtures}
        missing = REQUIRED_DEPTHS - depths
        self.assertFalse(missing, f"depth coverage gaps: {missing}")

    def test_both_languages_present(self):
        langs = {f.get("lang") for f in self.fixtures}
        self.assertIn("zh", langs)
        self.assertIn("en", langs)


class FixtureSchema(unittest.TestCase):
    REQUIRED_FIELDS = {
        "id",
        "lang",
        "prompt",
        "expected_mode",
        "expected_depth",
        "must_load",
        "must_not_load",
        "must_include",
        "must_not",
        "rubric",
    }

    @classmethod
    def setUpClass(cls):
        cls.bundle = _load_bundle()
        cls.fixtures = cls.bundle["fixtures"]
        cls.allowed_modes = set(cls.bundle["allowed_modes"])
        cls.allowed_depths = set(cls.bundle["allowed_depths"])

    def test_each_fixture_has_required_fields(self):
        for fx in self.fixtures:
            missing = self.REQUIRED_FIELDS - set(fx.keys())
            self.assertFalse(
                missing,
                f"fixture {fx.get('id', '<no-id>')} missing fields: {missing}",
            )

    def test_mode_and_depth_are_allowed(self):
        for fx in self.fixtures:
            self.assertIn(
                fx["expected_mode"],
                self.allowed_modes,
                f"{fx['id']}: unexpected mode {fx['expected_mode']}",
            )
            self.assertIn(
                fx["expected_depth"],
                self.allowed_depths,
                f"{fx['id']}: unexpected depth {fx['expected_depth']}",
            )

    def test_prompt_and_rubric_nonempty(self):
        for fx in self.fixtures:
            self.assertTrue(fx["prompt"].strip(), f"{fx['id']}: empty prompt")
            self.assertTrue(fx["rubric"].strip(), f"{fx['id']}: empty rubric")
            self.assertGreaterEqual(
                len(fx["prompt"]),
                6,
                f"{fx['id']}: prompt too short to be a real trigger",
            )

    def test_list_fields_are_lists_of_strings(self):
        for fx in self.fixtures:
            for key in ("must_load", "must_not_load", "must_include", "must_not"):
                val = fx[key]
                self.assertIsInstance(val, list, f"{fx['id']}.{key} must be a list")
                for item in val:
                    self.assertIsInstance(
                        item, str, f"{fx['id']}.{key} items must be strings"
                    )


class FixtureResourcePaths(unittest.TestCase):
    """must_load / must_not_load basenames must refer to shipped resources when
    they name skill files (not abstract tags)."""

    KNOWN_RESOURCES = {
        "professor-answer-template.md": SKILL_ROOT / "assets" / "professor-answer-template.md",
        "quality-checklist.md": SKILL_ROOT / "references" / "quality-checklist.md",
        "method-branches.md": SKILL_ROOT / "references" / "method-branches.md",
        "examples.md": SKILL_ROOT / "references" / "examples.md",
        "chinese-academic-style.md": SKILL_ROOT / "references" / "chinese-academic-style.md",
    }

    @classmethod
    def setUpClass(cls):
        cls.fixtures = _load_bundle()["fixtures"]

    def test_must_load_names_are_known_and_exist(self):
        for fx in self.fixtures:
            for name in fx["must_load"]:
                self.assertIn(
                    name,
                    self.KNOWN_RESOURCES,
                    f"{fx['id']}: unknown must_load resource '{name}'",
                )
                path = self.KNOWN_RESOURCES[name]
                self.assertTrue(
                    path.is_file(),
                    f"{fx['id']}: must_load '{name}' missing at {path}",
                )

    def test_must_not_load_names_are_known(self):
        for fx in self.fixtures:
            for name in fx["must_not_load"]:
                self.assertIn(
                    name,
                    self.KNOWN_RESOURCES,
                    f"{fx['id']}: unknown must_not_load resource '{name}'",
                )


class FixtureRoutingConsistency(unittest.TestCase):
    """Routing rules encoded as static invariants — the skill promises these
    without needing a live model."""

    @classmethod
    def setUpClass(cls):
        cls.fixtures = _load_bundle()["fixtures"]
        cls.by_id = {f["id"]: f for f in cls.fixtures}

    def test_flash_forbids_method_branches(self):
        for fx in self.fixtures:
            if fx["expected_depth"] != "Flash":
                continue
            self.assertIn(
                "method-branches.md",
                fx["must_not_load"],
                f"{fx['id']}: Flash must list method-branches.md in must_not_load",
            )
            self.assertNotIn(
                "method-branches.md",
                fx["must_load"],
                f"{fx['id']}: Flash must not require method-branches.md",
            )

    def test_review_requires_method_branches(self):
        for fx in self.fixtures:
            if fx["expected_mode"] != "Methodology Reviewer":
                continue
            if fx["expected_depth"] != "Review":
                continue
            self.assertIn(
                "method-branches.md",
                fx["must_load"],
                f"{fx['id']}: Review mode must load method-branches.md",
            )

    def test_studio_mentor_loads_template_or_checklist(self):
        for fx in self.fixtures:
            if fx["expected_depth"] != "Studio":
                continue
            if fx["expected_mode"] not in ("Research Mentor", "Blended"):
                continue
            loaded = set(fx["must_load"])
            self.assertTrue(
                loaded & {"professor-answer-template.md", "quality-checklist.md", "chinese-academic-style.md"},
                f"{fx['id']}: Studio mentor/blended should load design/style resources",
            )

    def test_anti_triggers_are_minimal(self):
        for fx in self.fixtures:
            if fx["expected_mode"] != "Anti-trigger":
                continue
            self.assertEqual(
                fx["expected_depth"],
                "Minimal",
                f"{fx['id']}: Anti-trigger depth must be Minimal",
            )
            self.assertEqual(
                fx["must_load"],
                [],
                f"{fx['id']}: Anti-trigger must load no professor resources",
            )
            # Scaffolding markers must be forbidden in answers.
            forbidden_hit = any(
                token in " ".join(fx["must_not"]).lower()
                for token in ("研究问题", "构念", "professor", "课堂科普")
            ) or any(
                "professor-answer-template.md" in x or "method-branches.md" in x
                for x in fx["must_not_load"]
            )
            self.assertTrue(
                forbidden_hit,
                f"{fx['id']}: Anti-trigger should forbid scaffolding tokens or resource loads",
            )

    def test_review_fixtures_require_truth_or_identification_language(self):
        for fx in self.fixtures:
            if fx["expected_depth"] != "Review":
                continue
            markers = " ".join(fx["must_include"]).lower()
            self.assertTrue(
                any(
                    k in markers
                    for k in (
                        "truth source",
                        "artifact",
                        "识别",
                        "无法",
                        "中心",
                        "权力",
                        "外部",
                    )
                ),
                f"{fx['id']}: Review must_include should demand identification/truth-source language",
            )

    def test_depth_inflation_guard_fixture_present(self):
        fx = self.by_id.get("class-selection-bias-zh")
        self.assertIsNotNone(fx)
        self.assertEqual(fx["expected_depth"], "Class")
        self.assertEqual(fx["expected_mode"], "Classroom Teacher")
        self.assertIn("method-branches.md", fx["must_not_load"])


class SkillMdAlignment(unittest.TestCase):
    """Fixtures must not invent Depth/Mode labels that SKILL.md does not define."""

    def test_skill_md_defines_depth_labels_used_by_fixtures(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        bundle = _load_bundle()
        for depth in bundle["allowed_depths"]:
            if depth == "Minimal":
                # Minimal is anti-trigger only; may appear as concept not heading.
                continue
            self.assertIn(depth, skill, f"SKILL.md missing Depth label used by fixtures: {depth}")

    def test_skill_md_defines_core_modes(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for mode in (
            "Classroom Teacher",
            "Research Mentor",
            "Methodology Reviewer",
        ):
            self.assertIn(mode, skill)


if __name__ == "__main__":
    unittest.main(verbosity=2)
