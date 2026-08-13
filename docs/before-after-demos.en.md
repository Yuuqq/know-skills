# CSS Professor — Before / After Demos

> 中文原版：[before-after-demos.md](./before-after-demos.md)

> Why install this skill? The three comparisons below answer the same question
> two ways: **bare prompt (asking the model directly) vs. the output with
> css-professor installed.**
>
> The "Before" side shows the encyclopedia-style / overconfident failures the
> model produces by default; the "After" side shows the output shape once the
> skill enforces routing + depth gating + truth-source discipline. These are
> **calibrated exemplars** (target output shapes) that show what the skill
> changes; for real model outputs, see the live eval
> (`scripts/eval_css_professor.py`).

Each demo is annotated with the three things the skill did internally:

- **Mode**: which professor stance was chosen (classroom / mentor / reviewer)
- **Depth**: the answer ceiling (Flash / Class / Studio / Review)
- **Discipline**: which hard rule blocked the default bad habit

Prompts below are translated from the Chinese originals; the golden fixtures
pin the Chinese versions (English fixture twins are tracked in
[issue #1](https://github.com/Yuuqq/know-skills/issues/1)).

---

## Demo 1 — Classroom explanation: algorithmic recommendation and public discourse

> Matches fixture `class-algo-public-sphere-zh`. Mode = Classroom Teacher, Depth = Class.

### The same prompt

```text
Explain it the way a classroom could follow: why does algorithmic recommendation change public discourse?
```

### Before (bare prompt) — the classic encyclopedia failure

> Algorithmic recommendation is a technology that uses user data for
> personalized content distribution... It is mainly implemented through
> collaborative filtering, content-based filtering, and hybrid models. Its
> impact on public discourse mainly manifests as filter bubbles, echo chambers,
> and polarization. Research shows that algorithmic recommendation
> significantly affects users' information exposure... (continues for another
> 800 words of survey padding — no judgment, no example, no mechanism layering)

**What's wrong**: no one-sentence judgment; jumps straight into term-stacking;
treats "impact" as a conclusion without separating mechanisms; no common
misconception named.

### After (css-professor, Class depth)

**Mode: Classroom Teacher · Depth: Class**

**One-sentence judgment**: Algorithmic recommendation changes public discourse
not mainly by "pushing certain opinions" but by deciding **who gets seen and
who gets grouped together**.

**Intuitive example**: Imagine a public square. You used to hear whatever you
walked past; now a guide steers you toward people similar to you, based on
where you linger. The problem is not that the guide has opinions — it is that
**the guide decides who meets whom**.

**Mechanisms (CSS lens)**:

- **Selective exposure**: recommendation makes content matching your existing
  preferences easier to see.
- **Visibility allocation**: extreme or emotional content is more likely to be
  pushed to the top, because it drives dwell time.
- **Alignment and clustering**: people with similar views get grouped together;
  internal consensus strengthens, external differences amplify.

**One common misconception**: treating the "filter bubble" as the only
mechanism. Recommendation produces both **isolation** and **incidental
exposure** — which one dominates depends on the platform's objective function.

**One-sentence recap**: What algorithmic recommendation changes is not the
opinions themselves, but **who gets seen and who gets grouped together**.

---

## Demo 2 — Research design: short video and political participation

> Matches fixture `studio-shortvideo-politics-zh`. Mode = Research Mentor, Depth = Studio.

### The same prompt

```text
I want to study how short-video platforms affect college students' political participation. Help me design the research questions and a methods roadmap.
```

### Before (bare prompt) — the classic overconfidence failure

> This is a great research question. Suggested hypothesis: the more time spent
> on short video, the higher the political participation. You could use a
> questionnaire survey, distribute 500 questionnaires, and run regression
> analysis... The contribution is filling the empirical gap between short video
> and political participation...

**What's wrong**: treats "affect" as a single causal claim; constructs not
decomposed; no selection-vs-influence distinction; proposes an unidentifiable
design; boilerplate contribution claim.

### After (css-professor, Studio depth)

**Mode: Research Mentor · Depth: Studio**

**Professor's Take**: Do not assume "an effect" yet. The biggest trap in this
topic is **mistaking selection effects for influence effects** — people who
already care about politics may be exactly the ones who watch political short
videos.

**Research questions (decomposed into workable layers)**:

- RQ1 (exposure surface): What is the correlational structure between
  short-video use and different types of political participation (online
  expression / offline action)?
- RQ2 (mechanism): After exposure to political short videos, does users'
  political efficacy change?
- RQ3 (identification): Can the effects of "self-selected content" and
  "algorithmically pushed content" be separated?

**Key constructs (measure separately)**:

- Political interest, political knowledge, political efficacy (internal /
  external)
- Online participation (reposting, commenting, remixing) vs. offline
  participation (rallies, donations, voting intention)
- Exposure type: active search vs. algorithmic push

**Minimum viable design**: cross-sectional survey + propensity score matching
(partially mitigates selection bias).

**Stronger alternatives**:

- Event study: traffic shocks during a policy or news window as exogenous
  variation.
- Panel design: track the same students over time; individual fixed effects
  absorb stable preferences.
- Natural experiment: a discontinuity around a platform algorithm update.

**Risks and next steps**:

- Causal identification: cross-sections cannot identify causality; the claim
  must be downgraded to "correlational structure".
- Measurement: self-reported usage time is heavily biased; prefer screen-time
  APIs or logs.
- External validity: a single-campus sample does not generalize to college
  students nationwide.

**Researchable Next Step**: Run a small pilot (n≈300) panel or event study
first to verify that "algorithmic push exposure" is measurable at all, then
decide the full-sample design.

---

## Demo 3 — Methods review: Weibo retweet networks and rumor diffusion

> Matches fixture `review-weibo-rumor-trust-zh`. Mode = Methodology Reviewer, Depth = Review.

### The same prompt

```text
I use a Weibo retweet network to prove that rumor diffusion causes a decline in social trust. What's wrong with this design?
```

### Before (bare prompt) — the classic polite review

> This research is interesting and the design is overall reasonable. Consider
> adding control variables such as user demographics and rumor type. You could
> use more regression models to strengthen robustness...

**What's wrong**: no decisive flaw identified; treats the retweet network as
evidence about trust; the suggestions are decoration, not an identification
strategy.

### After (css-professor, Review depth)

**Mode: Methodology Reviewer · Depth: Review**

**Professor's Take (decisive flaw first)**: A retweet network identifies only
the **diffusion structure of information**; it **cannot by itself identify a
change in social trust**. You are treating "visible traces of rumor diffusion"
as "evidence of declining trust" — a confusion of truth source and measurement
artifact.

**Truth source vs. measurement artifact**:

- **Truth source**: social trust itself — it must be measured directly through
  surveys, behavioral experiments, or longitudinal tracking ("do you trust
  strangers / institutions").
- **Measurement artifacts**: retweet counts, network topology, diffusion
  speed — these are **traces of information propagation**, not direct readings
  of trust.

**Evidentiary branches (loads the Network / Trace branches of
`references/method-branches.md`)**:

- Network analysis: centrality and diffusion paths are **structural
  artifacts**; they describe how the rumor flows, not how trust changes.
- Platform digital traces: a retweet is **platform-mediated behavior**,
  modulated by visibility algorithms, moderation deletions, and bot accounts —
  it only counts once mediation and missingness are modeled.

**Identification problem**: even if trust really is declining, the retweet
network cannot separate that from **alternative explanations** (panic,
attention shifts, platform governance changes, offline events).

**Repair paths**:

1. **Measurement patch**: add an independent measure of social trust (panel
   survey / trust experiment) alongside the retweet network.
2. **Identification patch**: an event study (difference in measured trust
   before and after a high-diffusion rumor) or a natural experiment (a
   comparison group not exposed to the rumor).
3. **Downgrade the claim**: if neither patch is possible, downgrade "rumor
   diffusion **causes** trust decline" to "traces of rumor diffusion are
   **associated with** trust-related correlational structure".

**Next Step (only given when a redesign is needed)**: Pick an event with a
measurable trust indicator and run the difference; otherwise this can only be
published as a correlational study.

---

## What the three demos show together: the skill's three cuts

| Default bad habit | How the skill blocks it |
|---|---|
| Encyclopedia padding, no judgment | **Mode routing** picks a stance first; the answer opens with a **one-sentence judgment** |
| Flash/Class silently inflated into Studio | **Depth gating** — simple asks stop early |
| Causal overconfidence, traces treated as truth | **Truth source vs. measurement artifact** discipline + **decisive-flaw-first** reviewing |

> Want to verify these hold against a real model? See
> `scripts/eval_css_professor.py` (requires `EVAL_API_KEY`).
