"""Live-model eval harness for the css-professor Agent Skill.

WHAT THIS IS
------------
A MANUAL / nightly evaluation that turns the offline fixtures in
``skills/css-professor/tests/fixtures/golden_prompts.json`` into runnable model
evaluations. The offline suite (``test_eval_fixtures.py``) only pins fixture
*shape*; it never calls a model. This harness closes that gap by building the
same skill context the real Agent host would provide, calling a model, and
scoring whether the model actually routes to the expected Mode + Depth.

This is NOT wired into the push-gate CI by default. It is meant for:
  * local iteration while editing SKILL.md or fixtures, and
  * an opt-in nightly job that sets ``EVAL_API_KEY``.

It is deliberately safe to run without configuration: if ``EVAL_API_KEY`` is
unset it prints a skip message and exits 0, so adding it to a CI matrix can
never turn the build red just because a secret is missing.

HOW TO RUN
----------
    # 1. No key — smoke / CI-safe path (exits 0, calls no model):
    python scripts/eval_css_professor.py --max-fixtures 1

    # 2. Live eval against the default GLM endpoint:
    export EVAL_API_KEY="your-key-here"
    python scripts/eval_css_professor.py

    # 3. Iterate on one fixture:
    export EVAL_API_KEY="..."
    python scripts/eval_css_professor.py --only studio-shortvideo-politics-zh

    # 4. Point at a different OpenAI-compatible endpoint / model:
    export EVAL_API_KEY="..."
    export EVAL_API_BASE="https://api.example.com/v1"
    export EVAL_MODEL="gpt-4o-mini"
    python scripts/eval_css_professor.py

ENVIRONMENT VARIABLES
---------------------
    EVAL_API_BASE  OpenAI-compatible chat-completions base URL.
                   Default: "https://open.bigmodel.cn/api/paas/v4"
    EVAL_API_KEY   Bearer token for the endpoint. REQUIRED for a live run;
                   if unset/empty the harness skips and exits 0.
    EVAL_MODEL     Model name passed in the request body.
                   Default: "glm-4-plus"

DEPENDENCIES
------------
Python standard library only. HTTP is done with ``urllib.request`` so the script
runs anywhere CPython runs — no ``requests``, no ``openai`` SDK.

SCORING RUBRIC
--------------
Each fixture's model response is scored on five fields:

    mode_hit             Does the response state/select the expected_mode?
                         Substring match of the allowed mode label against the
                         response, case-insensitive. (Anti-trigger responses
                         rarely label themselves; see routing_pass below.)
    depth_hit            Same as mode_hit but for expected_depth.
    must_include_hit     Fraction of must_include tokens present in the response
                         (lowercased substring). Empty must_include lists score
                         1.0 (vacuous pass) and are shown as "n/a".
    must_not_violation   Count of must_not strings that DID appear in the
                         response (lowercased substring). Lower is better;
                         0 = pass.
    anti_trigger_handled Only meaningful when expected_mode is "Anti-trigger":
                         True when no must_not scaffolding token appeared (i.e.
                         must_not_violation == 0). Shown as "-" otherwise.

ROUTING GATE
------------
The pass/fail decision per fixture is ``routing_pass``:

    * Anti-trigger fixtures: routing_pass = anti_trigger_handled
      (the correct routing is to NOT act as a professor).
    * All other fixtures:    routing_pass = mode_hit AND depth_hit.

The harness exits non-zero (exit code 1) when the mean routing_pass across the
selected fixtures is below 0.80. This is the threshold future CI can gate on.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "css-professor"
SKILL_MD = SKILL_DIR / "SKILL.md"
FIXTURES_PATH = SKILL_DIR / "tests" / "fixtures" / "golden_prompts.json"

# Basename -> path under the skill dir. Mirrors the KNOWN_RESOURCES map in
# skills/css-professor/tests/test_eval_fixtures.py so the harness resolves
# must_load entries exactly the way the offline contract expects.
KNOWN_RESOURCES: dict[str, Path] = {
    "professor-answer-template.md": SKILL_DIR / "assets" / "professor-answer-template.md",
    "quality-checklist.md": SKILL_DIR / "references" / "quality-checklist.md",
    "method-branches.md": SKILL_DIR / "references" / "method-branches.md",
    "examples.md": SKILL_DIR / "references" / "examples.md",
    "chinese-academic-style.md": SKILL_DIR / "references" / "chinese-academic-style.md",
}

# Routing gate threshold (mean routing_pass). Below this -> exit 1.
ROUTING_PASS_THRESHOLD = 0.80

# Defaults for the OpenAI-compatible endpoint.
DEFAULT_API_BASE = "https://open.bigmodel.cn/api/paas/v4"
DEFAULT_MODEL = "glm-4-plus"
REQUEST_TIMEOUT_S = 60
MAX_TOKENS = 1024  # routing lives in the opening lines; keep it cheap and fast


# ---------------------------------------------------------------------------
# Fixture + skill loading
# ---------------------------------------------------------------------------
def load_bundle(fixtures_path: Path = FIXTURES_PATH) -> dict[str, Any]:
    """Load and basic-validate the golden_prompts bundle."""
    if not fixtures_path.is_file():
        raise FileNotFoundError(f"fixtures file not found: {fixtures_path}")
    data = json.loads(fixtures_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("fixtures"), list):
        raise ValueError(f"malformed fixtures bundle at {fixtures_path}")
    return data


def parse_frontmatter(skill_md_text: str) -> tuple[dict[str, str], str]:
    """Split a SKILL.md into (frontmatter_dict, body).

    Frontmatter is the YAML block between leading ``---`` fences. We only need
    simple ``key: value`` parsing — no external YAML dependency. Quoted values
    have their surrounding quotes stripped.
    """
    fm: dict[str, str] = {}
    body = skill_md_text
    if skill_md_text.lstrip().startswith("---"):
        # First line is the opening fence; find the closing fence.
        lines = skill_md_text.splitlines()
        # Find opening fence index (skip leading blank lines).
        start = next(
            (i for i, ln in enumerate(lines) if ln.strip() == "---"), None
        )
        if start is not None:
            end = next(
                (i for i in range(start + 1, len(lines)) if lines[i].strip() == "---"),
                None,
            )
            if end is not None:
                for ln in lines[start + 1 : end]:
                    if ":" in ln:
                        k, _, v = ln.partition(":")
                        k = k.strip()
                        v = v.strip()
                        # strip matching surrounding quotes
                        if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
                            v = v[1:-1]
                        fm[k] = v
                body = "\n".join(lines[end + 1 :])
    return fm, body


def read_reference(basename: str) -> str:
    """Read a must_load reference file by basename; warn + stub if missing."""
    path = KNOWN_RESOURCES.get(basename)
    if path is None:
        return f"[unknown reference basename: {basename}]"
    if not path.is_file():
        sys.stderr.write(f"WARNING: reference missing on disk: {path}\n")
        return f"[file missing: {path}]"
    return path.read_text(encoding="utf-8")


def build_system_message(fixture: dict[str, Any], skill_md_text: str) -> str:
    """Construct the system message the real Agent host would send.

    Injects: the skill's frontmatter description, the full SKILL.md body, and
    the contents of every must_load reference file (resolved via
    KNOWN_RESOURCES). must_not_load files are intentionally NOT injected —
    the host only loads what the task requires, and the model is expected to
    route correctly without them.
    """
    fm, body = parse_frontmatter(skill_md_text)
    description = fm.get("description", "").strip()

    parts: list[str] = []
    parts.append(
        "You are operating as the css-professor Agent Skill. Follow the skill "
        "contract below precisely."
    )
    if description:
        parts.append("# Skill description\n" + description)
    parts.append("# SKILL.md (full contract)\n" + body.strip())

    must_load = fixture.get("must_load") or []
    if must_load:
        ref_block = ["# Loaded reference materials (per the skill's Hard Load Table for this task)"]
        for basename in must_load:
            ref_block.append(f"## {basename}\n" + read_reference(basename).strip())
        parts.append("\n\n".join(ref_block))

    parts.append(
        "# Your task\n"
        "Apply the skill's Mode + Depth routing to the user's message. As the "
        "skill's Answer Workflow step 1 says (\"Pick Mode + Depth — state "
        "briefly when helpful\"), begin your answer by briefly stating the "
        "chosen Mode and Depth, then deliver the answer at that depth. If this "
        "request is an Anti-trigger (pure coding, ops, or a book/course-to-skill "
        "pipeline), do NOT emit professor scaffolding — hand off or stay minimal."
    )
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Scoring (pure function — unit-testable without a network/key)
# ---------------------------------------------------------------------------
def _lower(text: str) -> str:
    return text.lower()


def score_response(fixture: dict[str, Any], response: str) -> dict[str, Any]:
    """Score a model response against a fixture. Pure: no I/O.

    Returns a dict with: mode_hit, depth_hit, must_include_found,
    must_include_total, must_include_frac, must_not_violation,
    must_not_violators, anti_trigger_handled, routing_pass.
    """
    if response is None:
        response = ""
    lowered = _lower(response)
    expected_mode = fixture["expected_mode"]
    expected_depth = fixture["expected_depth"]

    mode_hit = _lower(expected_mode) in lowered
    depth_hit = _lower(expected_depth) in lowered

    must_include = fixture.get("must_include") or []
    must_include_total = len(must_include)
    must_include_found = sum(
        1 for tok in must_include if _lower(tok) in lowered
    )
    must_include_frac = (
        must_include_found / must_include_total if must_include_total else 1.0
    )

    must_not = fixture.get("must_not") or []
    violators = [tok for tok in must_not if _lower(tok) in lowered]
    must_not_violation = len(violators)

    is_anti = expected_mode == "Anti-trigger"
    anti_trigger_handled = bool(
        is_anti and must_not_violation == 0
    )

    # Per-fixture routing decision feeding the gate.
    if is_anti:
        routing_pass = anti_trigger_handled
    else:
        routing_pass = bool(mode_hit and depth_hit)

    return {
        "mode_hit": mode_hit,
        "depth_hit": depth_hit,
        "must_include_found": must_include_found,
        "must_include_total": must_include_total,
        "must_include_frac": must_include_frac,
        "must_not_violation": must_not_violation,
        "must_not_violators": violators,
        "anti_trigger_handled": anti_trigger_handled if is_anti else None,
        "routing_pass": routing_pass,
    }


# ---------------------------------------------------------------------------
# Model call (stdlib urllib only)
# ---------------------------------------------------------------------------
def call_model(
    system_message: str,
    user_message: str,
    *,
    api_base: str,
    api_key: str,
    model: str,
    timeout: int = REQUEST_TIMEOUT_S,
) -> str:
    """POST to an OpenAI-compatible /chat/completions endpoint. Returns content.

    Raises RuntimeError with a helpful message on any failure so the caller can
    report per-fixture errors without aborting the whole run.
    """
    url = api_base.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.0,   # deterministic routing eval
        "max_tokens": MAX_TOKENS,
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {e.code} from {url}: {detail[:500]}"
        ) from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"network error calling {url}: {e.reason}") from None

    try:
        data = json.loads(raw)
        return data["choices"][0]["message"]["content"] or ""
    except (ValueError, KeyError, IndexError, TypeError) as e:
        raise RuntimeError(
            f"could not parse chat completion response: {e}; raw[:300]={raw[:300]!r}"
        ) from None


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def _fmt_bool(b: bool | None) -> str:
    if b is None:
        return "-"
    return "Y" if b else "n"


def print_table(rows: list[dict[str, Any]]) -> None:
    """Print a per-fixture score table to stdout."""
    header = (
        f"{'id':<40} {'mode':>4} {'depth':>5} {'incl':>6} "
        f"{'viol':>4} {'anti':>4} {'pass':>4}"
    )
    print()
    print(header)
    print("-" * len(header))
    for r in rows:
        incl = (
            "n/a"
            if r["must_include_total"] == 0
            else f"{r['must_include_found']}/{r['must_include_total']}"
        )
        print(
            f"{r['id']:<40} {_fmt_bool(r['mode_hit']):>4} "
            f"{_fmt_bool(r['depth_hit']):>5} {incl:>6} "
            f"{r['must_not_violation']:>4} "
            f"{_fmt_bool(r['anti_trigger_handled']):>4} "
            f"{_fmt_bool(r['routing_pass']):>4}"
        )
        if r["must_not_violators"]:
            print(f"    violators: {r['must_not_violators']}")
    print()


def print_aggregate(rows: list[dict[str, Any]]) -> dict[str, float]:
    n = len(rows)
    mode_rate = sum(1 for r in rows if r["mode_hit"]) / n
    depth_rate = sum(1 for r in rows if r["depth_hit"]) / n
    routing_rate = sum(1 for r in rows if r["routing_pass"]) / n
    incl_frac_avg = sum(r["must_include_frac"] for r in rows) / n
    total_violations = sum(r["must_not_violation"] for r in rows)
    print("Aggregate")
    print(f"  mode_hit rate        : {mode_rate:.1%} ({sum(1 for r in rows if r['mode_hit'])}/{n})")
    print(f"  depth_hit rate       : {depth_rate:.1%} ({sum(1 for r in rows if r['depth_hit'])}/{n})")
    print(f"  routing_pass rate    : {routing_rate:.1%} ({sum(1 for r in rows if r['routing_pass'])}/{n})  [gate threshold: {ROUTING_PASS_THRESHOLD:.0%}]")
    print(f"  avg must_include frac : {incl_frac_avg:.1%}")
    print(f"  total must_not violations: {total_violations}")
    return {
        "mode_rate": mode_rate,
        "depth_rate": depth_rate,
        "routing_rate": routing_rate,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def select_fixtures(
    bundle: dict[str, Any],
    *,
    only_id: str | None,
    max_fixtures: int | None,
) -> list[dict[str, Any]]:
    fixtures: list[dict[str, Any]] = bundle["fixtures"]
    if only_id is not None:
        fixtures = [f for f in fixtures if f["id"] == only_id]
        if not fixtures:
            raise SystemExit(
                f"--only {only_id!r} matched no fixture. "
                f"Known ids: {[f['id'] for f in bundle['fixtures']]}"
            )
    if max_fixtures is not None:
        fixtures = fixtures[:max_fixtures]
    return fixtures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Live-model eval harness for the css-professor skill.",
    )
    parser.add_argument(
        "--max-fixtures",
        type=int,
        default=None,
        help="Only evaluate the first N fixtures (quick iteration).",
    )
    parser.add_argument(
        "--only",
        dest="only_id",
        default=None,
        help="Evaluate only the fixture with this id.",
    )
    args = parser.parse_args(argv)

    api_key = os.environ.get("EVAL_API_KEY", "").strip()
    if not api_key:
        # CI-safe skip path: never fail a build just because a secret is absent.
        print("EVAL_API_KEY not set — live eval skipped (set EVAL_API_KEY to run)")
        return 0

    api_base = os.environ.get("EVAL_API_BASE", DEFAULT_API_BASE)
    model = os.environ.get("EVAL_MODEL", DEFAULT_MODEL)

    bundle = load_bundle()
    skill_md_text = SKILL_MD.read_text(encoding="utf-8")

    fixtures = select_fixtures(
        bundle, only_id=args.only_id, max_fixtures=args.max_fixtures
    )
    if not fixtures:
        print("no fixtures selected; nothing to do.")
        return 0

    print(
        f"css-professor live eval: {len(fixtures)} fixture(s) | "
        f"model={model} | base={api_base}"
    )

    rows: list[dict[str, Any]] = []
    for fx in fixtures:
        sys_msg = build_system_message(fx, skill_md_text)
        user_msg = fx["prompt"]
        print(f"  -> {fx['id']} ...", flush=True)
        t0 = time.time()
        try:
            response = call_model(
                sys_msg, user_msg, api_base=api_base, api_key=api_key, model=model
            )
        except RuntimeError as e:
            print(f"     ERROR: {e}")
            # Score an empty response so the fixture still appears in the table.
            response = ""
        dt = time.time() - t0
        score = score_response(fx, response)
        score["id"] = fx["id"]
        score["elapsed_s"] = dt
        rows.append(score)

    print_table(rows)
    agg = print_aggregate(rows)

    if agg["routing_rate"] < ROUTING_PASS_THRESHOLD:
        print(
            f"\nFAIL: routing_pass rate {agg['routing_rate']:.1%} "
            f"< threshold {ROUTING_PASS_THRESHOLD:.0%}"
        )
        return 1
    print(f"\nPASS: routing_pass rate {agg['routing_rate']:.1%} >= threshold {ROUTING_PASS_THRESHOLD:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
