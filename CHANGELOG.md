# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-13

First tracked release of the Agent Skill workbench. Captures the current,
publicly-releasable state of the repository.

### Added

- **css-professor**: Mode + Depth routing. Mode selection (Classroom Teacher /
  Research Mentor / Methodology Reviewer) is now orthogonal to a Depth ladder
  (Flash / Class / Studio / Review), with a Hard Load Table that loads only the
  reference a task requires instead of preloading everything.
- **css-professor**: Offline eval fixtures for behavioral contract testing,
  runnable with stdlib-only `unittest` (no pytest dependency).
- **agent-loop**: Compatibility shim that redirects to `css-professor`, retiring
  the legacy `loop.md` contract and its hardcoded Windows path. Versioned at
  `1.0.0` as a compatibility entry.
- Version field (`version: "1.0.0"`) in the YAML frontmatter of both skills.
- Compliance scaffolding for public release: root `LICENSE` (MIT, Yuuqq),
  `NOTICES.md` summarizing per-component licensing, and `UPSTREAM.sha`
  recording the vendored upstream snapshot provenance.
- Continuous Integration runs the skill contract and eval-fixture suites.

### Changed

- Inherited the 8 method-specific evidence rules (Text/Corpus, Qualitative
  Coding, Network, Causal Inference, Survey/Experiment, Simulation,
  Platform/Trace, Mixed Methods) from the retired agent-loop methodology into
  `css-professor/references/method-branches.md`, each pinned to a truth-source
  vs. measurement-artifact distinction.

### Removed

- Legacy agent-loop resources (`loop-template.md`, `review-checklist.md`,
  `example-loops.md`, and the old `references/method-branches.md`) are retired
  and no longer referenced.

[1.0.0]: https://github.com/Yuuqq/know-skills/releases/tag/v1.0.0
