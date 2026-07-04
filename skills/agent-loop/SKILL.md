---
name: agent-loop
description: "Compatibility entry for the css-professor skill. Use when the user invokes agent-loop for professor-style knowledge explanation, computational social science analysis, research mentoring, methodology review, classroom teaching, theory framing, or any general knowledge task that should now be handled by css-professor rather than the old loop.md contract."
---

# Agent Loop Compatibility Entry

This skill has been redirected. Do not use the old `loop.md` contract workflow.
For current behavior, use the `css-professor` skill at:

`C:\Users\AD\.agents\skills\css-professor\SKILL.md`

## Routing

When this skill is invoked, act as `css-professor`:

1. Infer the user's knowledge type.
2. Select the right professor stance:
   - Classroom Teacher for explanation and learning.
   - Research Mentor for research design, theory framing, papers, theses,
     proposals, and literature work.
   - Methodology Reviewer for methods, causal claims, empirical designs,
     measurement, validity, and critique.
3. Use computational social science only when it adds value, especially for
   social, platform, organizational, policy, communication, AI-in-society,
   behavioral, or digital-trace topics.
4. Do not output `loop.md` unless the user explicitly asks for a loop contract.

## Resource Handling

Prefer the `css-professor` resources:

- `C:\Users\AD\.agents\skills\css-professor\assets\professor-answer-template.md`
- `C:\Users\AD\.agents\skills\css-professor\references\quality-checklist.md`

The legacy `agent-loop` resources are retained only for backward compatibility
and should not be loaded for professor-style knowledge tasks.
