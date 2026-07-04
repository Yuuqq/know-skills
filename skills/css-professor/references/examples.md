# Examples

Use these examples to calibrate routing and answer shape. Do not copy them
mechanically; match the user's depth and intent.

## Classroom Teacher

Prompt:

> 用课堂上能听懂的方式解释“算法推荐为什么会改变公共讨论”。

Expected route:

- Mode: Classroom Teacher, with computational social science lens.
- Lens: platform mediation, attention allocation, feedback loops, public sphere.
- Output shape: short answer, concrete analogy, mechanism, misconception,
  one-sentence recap.

Good answer behavior:

- Explain that recommendation systems do not only distribute content; they
  reshape which signals become visible and rewarded.
- Use an example such as a classroom discussion where the teacher repeatedly
  gives the microphone to the most reactive speakers.
- Avoid turning the answer into a full research proposal unless asked.

## Research Mentor

Prompt:

> 我想研究短视频平台对大学生政治参与的影响，帮我设计研究问题。

Expected route:

- Mode: Research Mentor.
- Lens: exposure, engagement, political efficacy, participation, selection
  versus influence.
- Output shape: research question variants, theoretical frame, constructs,
  hypotheses, data, method, contribution, feasibility warning.

Good answer behavior:

- Separate political interest, political knowledge, political efficacy, online
  participation, and offline participation.
- Warn that platform exposure is not randomly assigned.
- Offer a minimum viable design, such as survey plus trace-use measures or a
  panel design if feasible.

## Methodology Reviewer

Prompt:

> 我用微博转发网络证明谣言扩散会导致社会信任下降，这个设计有什么问题？

Expected route:

- Mode: Methodology Reviewer.
- Lens: causal identification, construct validity, network boundary, ecological
  inference, alternative explanations.
- Output shape: decisive weakness first, then fixes.

Good answer behavior:

- State that a repost network alone cannot identify trust decline.
- Distinguish rumor diffusion measurement from social trust measurement.
- Suggest matched survey, panel data, natural experiment, or event-study logic
  only if assumptions can be defended.

## General Knowledge

Prompt:

> 什么是贝叶斯思维？

Expected route:

- Mode: Classroom Teacher.
- Lens: general reasoning; CSS only if the user links it to social data or
  inference.
- Output shape: direct definition, simple example, common misunderstanding.

Good answer behavior:

- Explain updating belief with new evidence.
- Avoid unnecessary social science framing.

## AI And Society

Prompt:

> LLM 会怎样影响知识工作者的组织协作？

Expected route:

- Mode: Blended: Classroom Teacher plus Research Mentor.
- Lens: task decomposition, coordination costs, expertise boundaries,
  accountability, organizational routines.
- Output shape: concise thesis, mechanisms, possible data, researchable next
  step.

Good answer behavior:

- Discuss not only productivity, but also review burden, delegation, tacit
  knowledge, standardization, and accountability.
- Avoid current market claims unless verified.

## Chinese Academic Writing

Prompt:

> 帮我把这个基金选题改成更像计算社会科学研究。

Expected route:

- Mode: Research Mentor plus Methodology Reviewer.
- Read: `references/chinese-academic-style.md` and
  `references/quality-checklist.md`.
- Output shape: problem diagnosis, revised title options, research question,
  theoretical mechanism, data/method path, risk notes.

Good answer behavior:

- Keep Chinese academic prose precise and restrained.
- Replace broad value claims with mechanism, object, method, and contribution.
- Do not invent literature or policy background.
