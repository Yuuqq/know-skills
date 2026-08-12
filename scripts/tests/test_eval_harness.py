"""Smoke tests for the css-professor live eval harness.

These run WITHOUT a network and WITHOUT EVAL_API_KEY. They verify the parts of
the harness that are pure logic:

  * fixtures load and have the expected shape,
  * the skill-context system message is non-empty and mentions the skill,
  * main() exits 0 when EVAL_API_KEY is unset (the CI-safe path),
  * score_response correctly counts must_include hits on a canned string.

Run:

    python -m unittest discover -s scripts -p 'test_*.py' -v
"""
from __future__ import annotations

import importlib.util
import os
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
HARNESS_PATH = SCRIPTS_DIR / "eval_css_professor.py"

# Import the harness module by path so the test does not depend on a package.
_spec = importlib.util.spec_from_file_location("eval_css_professor", HARNESS_PATH)
assert _spec is not None and _spec.loader is not None
eval_css_professor = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eval_css_professor)


class FixtureLoading(unittest.TestCase):
    """(a) fixtures load correctly."""

    def test_bundle_loads_with_expected_fixture_count(self):
        bundle = eval_css_professor.load_bundle()
        self.assertIn("fixtures", bundle)
        self.assertGreaterEqual(len(bundle["fixtures"]), 10)
        # The known golden set is 12; pin a floor so shrinkage is caught.
        self.assertEqual(len(bundle["fixtures"]), 12)

    def test_each_fixture_has_scoring_fields(self):
        fixtures = eval_css_professor.load_bundle()["fixtures"]
        for fx in fixtures:
            for key in (
                "id",
                "prompt",
                "expected_mode",
                "expected_depth",
                "must_include",
                "must_not",
            ):
                self.assertIn(key, fx, f"{fx.get('id')} missing {key}")


class SystemMessageBuilding(unittest.TestCase):
    """(b) builds a non-empty skill-context prompt for a sample fixture."""

    def setUp(self):
        self.bundle = eval_css_professor.load_bundle()
        self.skill_md_text = eval_css_professor.SKILL_MD.read_text(
            encoding="utf-8"
        )

    def _fixture(self, fid: str) -> dict:
        for fx in self.bundle["fixtures"]:
            if fx["id"] == fid:
                return fx
        raise AssertionError(f"fixture {fid} not found")

    def test_system_message_for_studio_fixture_includes_skill_and_loaded_refs(self):
        fx = self._fixture("studio-shortvideo-politics-zh")
        msg = eval_css_professor.build_system_message(fx, self.skill_md_text)
        self.assertIsInstance(msg, str)
        self.assertGreater(len(msg), 500)  # non-trivial context block
        # The contract body is injected.
        self.assertIn("css-professor", msg)
        self.assertIn("Mode Selection", msg)  # SKILL.md section heading
        # must_load references are injected.
        self.assertIn("quality-checklist.md", msg)
        self.assertIn("Research Mentor", msg)  # from the skill contract

    def test_system_message_for_anti_trigger_fixture_is_non_empty(self):
        fx = self._fixture("anti-pure-coding")
        msg = eval_css_professor.build_system_message(fx, self.skill_md_text)
        self.assertGreater(len(msg), 200)
        # Anti-trigger has empty must_load -> no reference block, but contract
        # body is still present.
        self.assertIn("Anti-Triggers", msg)

    def test_frontmatter_description_is_extracted(self):
        fm, body = eval_css_professor.parse_frontmatter(self.skill_md_text)
        self.assertIn("description", fm)
        # The description names the skill's role (teacher / mentor / reviewer).
        desc = fm["description"].lower()
        self.assertTrue(
            "teacher" in desc or "mentor" in desc or "reviewer" in desc,
            f"description should name a role: {fm['description']!r}",
        )
        # Body should NOT contain the leading --- fences anymore.
        self.assertFalse(body.lstrip().startswith("---"))


class NoKeySkipPath(unittest.TestCase):
    """(c) exits 0 when EVAL_API_KEY is unset."""

    def setUp(self):
        # Snapshot env so we can restore exactly what was there.
        self._prev = os.environ.get("EVAL_API_KEY")

    def tearDown(self):
        if self._prev is None:
            os.environ.pop("EVAL_API_KEY", None)
        else:
            os.environ["EVAL_API_KEY"] = self._prev

    def test_main_exits_zero_and_skips_when_key_unset(self):
        os.environ.pop("EVAL_API_KEY", None)
        rc = eval_css_professor.main(["--max-fixtures", "1"])
        self.assertEqual(rc, 0)

    def test_main_exits_zero_and_skips_when_key_empty(self):
        os.environ["EVAL_API_KEY"] = "   "
        rc = eval_css_professor.main(["--max-fixtures", "1"])
        self.assertEqual(rc, 0)


class ScoringLogic(unittest.TestCase):
    """(d) score_response counts must_include hits correctly on canned strings."""

    def _fx(self, **overrides) -> dict:
        base = {
            "id": "synthetic",
            "prompt": "n/a",
            "expected_mode": "Classroom Teacher",
            "expected_depth": "Flash",
            "must_load": [],
            "must_not_load": [],
            "must_include": ["证据", "更新"],
            "must_not": ["研究问题"],
        }
        base.update(overrides)
        return base

    def test_all_must_include_present_scores_full_fraction(self):
        fx = self._fx()
        resp = "贝叶斯思维是用证据更新信念的方法。"  # contains 证据 + 更新
        s = eval_css_professor.score_response(fx, resp)
        self.assertEqual(s["must_include_found"], 2)
        self.assertEqual(s["must_include_total"], 2)
        self.assertEqual(s["must_include_frac"], 1.0)

    def test_partial_must_include_present_counts_correctly(self):
        fx = self._fx(must_include=["证据", "更新", "先验", "似然"])
        resp = "证据是关键；先验也很重要。"  # 证据 + 先验 only
        s = eval_css_professor.score_response(fx, resp)
        self.assertEqual(s["must_include_found"], 2)
        self.assertEqual(s["must_include_total"], 4)
        self.assertAlmostEqual(s["must_include_frac"], 0.5)

    def test_empty_must_include_is_vacuously_passing(self):
        fx = self._fx(must_include=[])
        s = eval_css_professor.score_response(fx, "anything")
        self.assertEqual(s["must_include_total"], 0)
        self.assertEqual(s["must_include_frac"], 1.0)

    def test_case_insensitive_mode_and_depth_hit(self):
        fx = self._fx()
        resp = "Mode: CLASSROOM TEACHER | Depth: flash. A one-line answer."
        s = eval_css_professor.score_response(fx, resp)
        self.assertTrue(s["mode_hit"])
        self.assertTrue(s["depth_hit"])
        self.assertTrue(s["routing_pass"])

    def test_must_not_violations_counted_and_routing_fails_when_mode_missed(self):
        fx = self._fx()
        # Response names no mode/depth label AND emits the forbidden 研究问题 token.
        resp = "Here is the 研究问题 and 假设."
        s = eval_css_professor.score_response(fx, resp)
        self.assertEqual(s["must_not_violation"], 1)
        self.assertIn("研究问题", s["must_not_violators"])
        # mode label absent -> routing fails even though must_not is the only flag
        self.assertFalse(s["routing_pass"])

    def test_anti_trigger_routing_passes_when_no_scaffolding(self):
        fx = self._fx(
            expected_mode="Anti-trigger",
            expected_depth="Minimal",
            must_include=[],
            must_not=["研究问题", "Professor's Take"],
        )
        resp = "This looks like a coding task; I'll just fix the bug in main()."
        s = eval_css_professor.score_response(fx, resp)
        self.assertTrue(s["anti_trigger_handled"])
        self.assertTrue(s["routing_pass"])  # anti -> handled == pass

    def test_anti_trigger_routing_fails_when_scaffolding_emitted(self):
        fx = self._fx(
            expected_mode="Anti-trigger",
            expected_depth="Minimal",
            must_include=[],
            must_not=["研究问题", "Professor's Take"],
        )
        resp = "Professor's Take: let me frame the 研究问题 for this code."
        s = eval_css_professor.score_response(fx, resp)
        self.assertFalse(s["anti_trigger_handled"])
        self.assertFalse(s["routing_pass"])
        self.assertEqual(s["must_not_violation"], 2)

    def test_none_response_does_not_crash(self):
        fx = self._fx()
        s = eval_css_professor.score_response(fx, "")  # type: ignore[arg-type]
        self.assertFalse(s["mode_hit"])
        self.assertFalse(s["routing_pass"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
