# Contributing

Thanks for helping make `css-professor` better. Issues and PRs are welcome in
English or Chinese (中英文皆可).

## What fits well here

- **New golden prompts** — add a fixture to
  `skills/css-professor/tests/fixtures/golden_prompts.json` that pins an
  expected Mode + Depth for a prompt the skill currently mis-routes.
- **Method branches** — extend
  `skills/css-professor/references/method-branches.md` with a method's
  truth-source vs. measurement-artifact rules (e.g. panel data, diff-in-diff,
  agent-based models).
- **English fixture variants** — most fixtures are Chinese-first; English
  twins are wanted.
- **Docs** — sharper before/after demos, fixes to either README.

Out of scope: turning this repo into a multi-skill collection, adding runtime
dependencies (everything is stdlib-only by design), or vendoring third-party
code (see `NOTICES.md` for why we stopped).

## Before you open a PR

All checks are offline and take under five seconds:

```bash
# structure: frontmatter + resource paths
python skills/css-professor/scripts/validate.py

# behavior: contract + golden-prompt fixtures
python -m unittest skills.css-professor.tests.test_skill_contract skills.css-professor.tests.test_eval_fixtures

# eval harness smoke tests
python -m unittest discover -s scripts -p "test_*.py"
```

If you changed routing behavior in `SKILL.md`, update the golden fixtures in
the same PR — CI pins them to each other on Ubuntu and Windows.

Optionally, replay the golden prompts against a live model:

```bash
EVAL_API_KEY=... python scripts/eval_css_professor.py
```

## Commit style

Conventional commits (`feat:`, `fix:`, `test:`, `docs:`, `chore:`), scoped to
the skill when relevant, e.g. `feat(css-professor): add panel-data method
branch`. Explain the why in the body when it is not obvious.
