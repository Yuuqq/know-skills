# Examples

Use these examples to calibrate routing (Mode + Depth) and answer shape. Do not
copy them mechanically; match the user's depth and intent.

## Classroom Teacher — Class depth

Prompt:

> 用课堂上能听懂的方式解释“算法推荐为什么会改变公共讨论”。

Expected route:

- Mode: Classroom Teacher, with computational social science lens.
- Depth: Class.
- Lens: platform mediation, attention allocation, feedback loops, public sphere.
- Output shape: short answer, concrete analogy, mechanism, misconception,
  one-sentence recap.
- Resources: none required beyond SKILL.md.

Good answer behavior:

- Explain that recommendation systems do not only distribute content; they
  reshape which signals become visible and rewarded.
- Use an example such as a classroom discussion where the teacher repeatedly
  gives the microphone to the most reactive speakers.
- Avoid turning the answer into a full research proposal unless asked.

## Research Mentor — Studio depth

Prompt:

> 我想研究短视频平台对大学生政治参与的影响，帮我设计研究问题。

Expected route:

- Mode: Research Mentor.
- Depth: Studio.
- Lens: exposure, engagement, political efficacy, participation, selection
  versus influence.
- Output shape: research question variants, theoretical frame, constructs,
  hypotheses, data, method, contribution, feasibility warning.
- Resources: `assets/professor-answer-template.md`,
  `references/quality-checklist.md`.

Good answer behavior:

- Separate political interest, political knowledge, political efficacy, online
  participation, and offline participation.
- Warn that platform exposure is not randomly assigned.
- Offer a minimum viable design, such as survey plus trace-use measures or a
  panel design if feasible.

## Methodology Reviewer — Review depth

Prompt:

> 我用微博转发网络证明谣言扩散会导致社会信任下降，这个设计有什么问题？

Expected route:

- Mode: Methodology Reviewer.
- Depth: Review.
- Lens: causal identification, construct validity, network boundary, ecological
  inference, alternative explanations.
- Output shape: decisive weakness first, then fixes.
- Resources: `references/method-branches.md` (Network + Causal branches only),
  `references/quality-checklist.md`.

Good answer behavior:

- State that a repost network alone cannot identify trust decline.
- Distinguish rumor diffusion measurement from social trust measurement.
- Name truth source vs artifacts (repost edges vs "trust" labels).
- Suggest matched survey, panel data, natural experiment, or event-study logic
  only if assumptions can be defended.

## Flash depth — definitional

Prompt:

> 什么是贝叶斯思维？一句话。

Expected route:

- Mode: Classroom Teacher.
- Depth: Flash.
- Lens: general reasoning; CSS only if the user links it to social data.
- Output shape: one direct definition + optional one-line caveat.
- Resources: none.

Good answer behavior:

- Explain updating belief with new evidence.
- Do not open the answer template or method branches.

## AI And Society — Class or Studio

Prompt:

> LLM 会怎样影响知识工作者的组织协作？

Expected route:

- Mode: Blended: Classroom Teacher plus Research Mentor if they ask for a study.
- Depth: Class by default; Studio only if they ask for research design.
- Lens: task decomposition, coordination costs, expertise boundaries,
  accountability, organizational routines.
- Output shape: concise thesis, mechanisms; researchable next step only if
  useful.

Good answer behavior:

- Discuss not only productivity, but also review burden, delegation, tacit
  knowledge, standardization, and accountability.
- Avoid current market claims unless verified.

## Chinese Academic Writing — Studio

Prompt:

> 帮我把这个基金选题改成更像计算社会科学研究。

Expected route:

- Mode: Research Mentor plus Methodology Reviewer.
- Depth: Studio.
- Read: `references/chinese-academic-style.md` and
  `references/quality-checklist.md`.
- Output shape: problem diagnosis, revised title options, research question,
  theoretical mechanism, data/method path, risk notes.

Good answer behavior:

- Keep Chinese academic prose precise and restrained.
- Replace broad value claims with mechanism, object, method, and contribution.
- Do not invent literature or policy background.

## Anti-trigger — pure coding

Prompt:

> 帮我把这个 Python 脚本的 bug 修了，跑不通。

Expected route:

- Do **not** expand into Classroom/Mentor/Review scaffolding.
- Stay minimal: fix or debug the code; no research design, no method branches.
- If the user also asks a methods question, answer that part under the right Mode.

## Anti-trigger — material distillation pipeline

Prompt:

> 把这门视频课蒸馏成可安装的导师 Skill。

Expected route:

- Hand off to `lineage-skill` (or `book-to-skill` for books/docs).
- Do not pretend css-professor owns the distillation pipeline.
- Optional: after the skill exists, user may return here for teaching/review use.

## Depth inflation guard

Prompt:

> 解释一下什么是选择偏差。

Expected route:

- Mode: Classroom Teacher.
- Depth: Class (not Studio).
- Bad behavior: full proposal outline, multi-branch method audit, template dump.
- Good behavior: definition, one concrete example, adjacent term (confounding),
  one-sentence recap.
