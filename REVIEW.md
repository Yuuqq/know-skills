# Code Review: css-professor (know-skills)

This document provides a thorough code review of the `Yuuqq/know-skills` repository, focusing on architecture, security, reliability, test coverage, maintainability, and documentation.

## 1. Architecture and Code Organization Quality
- **INFO (Solid):** The repository embraces an interesting and effective approach of treating prompts ("Agent Skills") as software, complete with CI/CD, unit tests, and structural validation. The offline and online eval split is well-executed.
- **INFO (Solid):** `KNOWN_RESOURCES` mapping in the eval harness and fixtures test correctly insulates the harness from arbitrary path injection.
- **MEDIUM:** Frontmatter parsing duplication.
  - **File:** `scripts/eval_css_professor.py` (lines ~86-107), `skills/css-professor/scripts/validate.py` (lines ~21-30), `skills/css-professor/tests/test_skill_contract.py` (lines ~34-43)
  - **Impact:** The custom YAML frontmatter parser is implemented independently in three different files. The current regex `r"\A---\s*\n(.*?)\n---\s*\n"` and parsing logic strips quotes but fails if a frontmatter line has an inline comment (e.g. `version: "1.0.0" # comment`, which currently exists in `skills/agent-loop/SKILL.md`).
  - **Fix Suggestion:** Extract `parse_frontmatter` to a shared utility module under a common Python package (e.g., in `scripts/utils.py`) to keep the codebase DRY and fix the inline comment bug once.

## 2. Security Issues
- **INFO (Solid):** Good security hygiene in the CI/CD setup and API key handling. `EVAL_API_KEY` is checked and the script gracefully exits without erroring out CI if missing. The script only uses the stdlib `urllib.request`.
- **LOW:** Remote API URL scheme enforcement.
  - **File:** `scripts/eval_css_professor.py` (line 220 `url = api_base.rstrip("/") + "/chat/completions"`)
  - **Impact:** Since `EVAL_API_BASE` comes from the environment, it could potentially be set to `http://` or `file://`, though the risk is mostly limited to local user execution since this isn't a web service taking arbitrary user input.
  - **Fix Suggestion:** Explicitly assert that `api_base.startswith("https://")` for production endpoints, or at least validate it.

## 3. Reliability / Error Handling / Edge Cases
- **HIGH:** Missing handling for `urllib` Timeout and Socket Errors.
  - **File:** `scripts/eval_css_professor.py` (lines ~236-243)
  - **Impact:** The `call_model` function catches `urllib.error.HTTPError` and `urllib.error.URLError`, but does not explicitly catch `TimeoutError` or socket-level errors (like `ConnectionResetError`) that can bubble up from `urlopen(..., timeout=timeout)`. This causes the script to crash entirely on a network timeout, failing the whole batch instead of failing/reporting a single fixture and continuing.
  - **Fix Suggestion:** Add an `except (TimeoutError, ConnectionError) as e:` block inside `call_model` to raise a wrapped `RuntimeError`.
- **LOW:** JSON parsing error handling in `urllib.error.HTTPError` block.
  - **File:** `scripts/eval_css_professor.py` (line 238)
  - **Impact:** `e.read().decode()` can fail if the server returns non-UTF8 binary data on error. The `errors="replace"` mitigates decode errors, but it is better to wrap the decode in a safe manner. The script also handles happy-path JSON decode gracefully.

## 4. Test Coverage Gaps and High-Risk Untested Paths
- **MEDIUM:** No mock testing for `call_model` error paths in the eval harness.
  - **File:** `scripts/tests/test_eval_harness.py`
  - **Impact:** The `eval_css_professor.py` contains `call_model` which handles HTTP interactions. The smoke tests (`test_eval_harness.py`) explicitly avoid hitting the network, which is good, but they do not mock `urllib.request.urlopen` to verify that `call_model` correctly parses standard responses, handles missing keys in the response JSON, or catches HTTP 400/500 errors.
  - **Fix Suggestion:** Add tests using `unittest.mock.patch("urllib.request.urlopen")` to simulate successful LLM responses and HTTP errors to ensure `call_model` handles them correctly.

## 5. Performance or Maintainability Concerns
- **INFO (Solid):** Code is highly maintainable, type-hinted (`from __future__ import annotations`, static typing syntax used extensively), and adheres to standard library-only constraints for maximum portability.
- **LOW:** Sync script cross-platform drift.
  - **File:** `scripts/sync-skills.sh` and `scripts/sync-skills.ps1`
  - **Impact:** The bash and powershell scripts duplicate logic for syncing skills. While acceptable for a small tool, keeping them in sync if new features are added (like skipping certain patterns) can be tedious.
  - **Fix Suggestion:** If the project adds more complex installation logic, consider writing a single `install.py` script, leveraging Python's cross-platform nature, instead of maintaining separate shell scripts. Since the repo already heavily relies on Python 3 for validation and evaluation, requiring Python 3 for installation is reasonable.

## 6. Documentation and Developer-Experience Gaps
- **INFO (Solid):** Documentation (`README.md`, `CONTRIBUTING.md`) is excellent. The instructions are clear, the purpose of the skill is well-defined, and the "tested, not vibes" section is a strong differentiator. The use of offline unit tests for the agent prompt is highly commendable.
- **LOW:** Missing `requirements.txt` for development.
  - **File:** Repository Root
  - **Impact:** Even though the project uses only the Python standard library, it lacks a formal `requirements.txt` or `pyproject.toml` (even if empty or just stating standard library is used). Standard tooling (e.g. `pip install -e .` or linters like `flake8`/`black`/`mypy`) often looks for standard packaging metadata.
  - **Fix Suggestion:** Add a minimal `pyproject.toml` to define the project structure and configure tools like `mypy` or `black` if they are to be used in the future.
