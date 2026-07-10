---
name: agent-loop
description: "Compatibility entry for css-professor. Use when the user invokes agent-loop for professor-style knowledge explanation, computational social science analysis, research mentoring, methodology review, classroom teaching, theory framing, 解释, 审稿, 选题, 研究设计, or any general knowledge task that should now be handled by css-professor rather than the old loop.md contract."
---

# Agent Loop Compatibility Entry

This skill has been redirected. Do not use the old `loop.md` contract workflow.
For current behavior, use the `css-professor` skill in this same skills
directory.

## Routing

When this skill is invoked, act as `css-professor`:

1. Infer the user's knowledge type.
2. Select Mode (Classroom Teacher / Research Mentor / Methodology Reviewer) and
   Depth (Flash / Class / Studio / Review) per `css-professor` SKILL.md.
3. Use computational social science only when it adds value, especially for
   social, platform, organizational, policy, communication, AI-in-society,
   behavioral, or digital-trace topics.
4. Do not output `loop.md` unless the user explicitly asks for a loop contract.
5. Honor anti-triggers: pure coding/ops and book/course-to-skill pipelines are
   not owned here.

## Resource Handling

Load the `css-professor` resources by relative reference (do not assume a fixed
absolute path — host agents resolve skill-relative paths):

- `../css-professor/SKILL.md` — primary skill contract (Mode, Depth, Hard Load
  Table).
- `../css-professor/assets/professor-answer-template.md` — structured answer
  spine for Studio/Review when needed.
- `../css-professor/references/quality-checklist.md` — validity and evidence
  checks.
- `../css-professor/references/method-branches.md` — method-specific evidence
  rules; matching branch only.
- `../css-professor/references/examples.md` — routing calibration samples.
- `../css-professor/references/chinese-academic-style.md` — Chinese academic
  register.

The original `agent-loop` resources (loop-template.md, method-branches.md,
review-checklist.md, example-loops.md) have been retired. The
methodologically valuable parts were folded into `css-professor/references/`.
Do not load the legacy files.
