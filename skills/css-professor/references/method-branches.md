# Method Branches

Use this reference whenever the Methodology Reviewer mode (or a research design
that involves a specific method) is active. Each branch tells you, in professor
voice, what counts as evidence, what does not, and what to check before you
accept a claim.

**MUST: read only the matching branch section(s), not this whole file.** This is
a **branch check, not an execution manual**. If a study mixes methods, open every
matching branch and then the Mixed Methods rule. Do not preload unrelated
branches into context.

A single idea runs through all branches:

> **Every empirical claim must point to a named truth source.** A truth source
> is the record that the construct or fact is grounded in — raw observations,
> original records, validated annotations, an audited sample, an observed
> treatment assignment. Derived quantities — centrality scores, topic
> proportions, classifier labels, LLM annotations, regression estimates,
> simulated outputs — are *measurement artifacts*. They are not truth until they
> are validated against a truth source. When you review, name both: which part is
> truth, which part is artifact, and what links them.

---

## Text / Corpus Analysis

When the user frames, counts, classifies, or models text from documents, posts,
news, archives, or any corpus.

- **Define**: corpus source, population, timeframe, language, deduplication,
  sampling, and inclusion/exclusion rules.
- **Operationalize**: constructs as dictionaries, codes, human annotations,
  embeddings, topics, classifiers, or close-reading evidence — each with its own
  validation.
- **Require**: gold labels, human audit, inter-coder agreement, dictionary face
  validity, model error analysis, or negative-case review.
- **Unacceptable evidence**: word clouds, topics, embeddings, or LLM labels
  alone as proof of a social construct.
- **Truth source**: raw text units and human-validated annotations. Topics,
  embeddings, classifiers, and LLM labels are measurement artifacts until
  validated.

## Qualitative Coding / Digital Ethnography

When the user codes, interprets, or builds theory from interviews, field notes,
archival close reading, or ethnographic observation.

- **Define**: cases, field boundary, observation units, codebook version, memo
  rules, and adjudication policy.
- **Require**: codebook, coded excerpts, disagreement log, analytic memos,
  negative cases, and saturation or stopping rationale.
- **Unacceptable evidence**: unlogged interpretive judgments or quotes detached
  from context.
- **Truth source**: coded excerpts, field notes, memos, and adjudicated labels.
  Summaries or generated interpretations need traceable supporting excerpts.

## Network Analysis

When the user builds and interprets a graph of relationships — collaboration,
communication, citation, follow, transfer, co-occurrence.

- **Define**: nodes, edges, edge direction, weight, timeframe, boundary,
  missingness, and any multiplex layers.
- **Require**: construction log, summary diagnostics, robustness to boundary
  choices, and explicit interpretation limits for centrality or community
  measures.
- **Unacceptable evidence**: centrality or cluster membership treated as
  motivation, influence, or power without external validation.
- **Truth source**: source records and explicit node/edge construction rules.
  Graph measures are derived artifacts.

## Causal Inference / Quasi-Experiment

When the user wants to claim that X causes Y, or that some intervention had an
effect.

- **Define**: treatment, outcome, assignment process, comparison group,
  estimand, and identification assumption.
- **Require**: DAG or assumption table, balance/placebo/pre-trend checks where
  relevant, sensitivity analysis, and stated scope conditions.
- **Unacceptable evidence**: correlation, prediction, or before/after difference
  stated as a causal claim without identification.
- **Truth source**: observed assignment, treatment, outcome, and covariate
  records. Estimates are derived artifacts constrained by assumptions.

## Survey / Experiment

When the user fields a questionnaire, vignette, conjoint, or randomized
experiment.

- **Define**: sample frame, recruitment, instrument, treatment or vignette,
  outcome, exclusion rules, and power or precision target.
- **Require**: instrument appendix, randomization or sampling record,
  manipulation/attention checks where appropriate, and attrition/missingness log.
- **Unacceptable evidence**: convenience sample generalized without scope
  limits.
- **Truth source**: response records, assignment logs, instruments, and sampling
  records. Scales and indices require reliability/validity evidence.

## Simulation / Agent-Based Modeling

When the user builds a simulation, agent-based model, or generative model to
explain a social or system mechanism.

- **Define**: agents, rules, environment, parameters, calibration target, and
  the output behavior to be explained.
- **Require**: parameter table, seed policy, sensitivity analysis,
  calibration/validation target, and limits on external validity.
- **Unacceptable evidence**: one simulation run or visually plausible dynamics
  as proof of a social mechanism.
- **Truth source**: theory, empirical calibration targets, and observed
  benchmark patterns ground the simulation. Simulated outputs are artifacts, not
  empirical truth.

## Platform / Digital Trace Data

When the user works with data pulled from a platform API, search interface, log
export, or scraped stream.

- **Define**: platform boundary, API/search/filter behavior, collection date,
  deletion/editing risks, bot/spam handling, and terms/licensing constraints.
- **Require**: collection manifest, query log, missingness assessment,
  de-identification rule, and external validity limits.
- **Unacceptable evidence**: treating returned data as the whole population, or
  publishing sensitive derived data without an approval gate.
- **Truth source**: collected records and platform documentation are bounded
  truth sources for returned data only. API/search outputs are not evidence of
  the unseen population without missingness and boundary analysis. Always model
  how interfaces, algorithms, and incentives mediate what was captured.

## Mixed Methods / Triangulation

When the user combines two or more methods and wants to claim convergence,
complementarity, or robustness.

- **Define**: what each method contributes — discovery, measurement,
  explanation, validation, or contradiction handling.
- **Require**: an integration matrix linking findings across methods, a conflict
  resolution rule, and claim-specific evidence strength.
- **Unacceptable evidence**: multiple weak signals treated as convergence
  without checking whether they measure the same construct.
- **Truth source**: each method keeps its own truth source. Integration records
  must distinguish convergence, complementarity, and contradiction — do not blur
  them into a single "robust" claim.

---

## How To Use this file during a review

1. Identify the primary method branch(es) of the design under review.
2. Open **only** those branch headings (plus Mixed Methods if needed).
3. For each branch, name the truth source and the measurement artifacts
   separately.
4. List the unacceptable-evidence patterns and check whether the draft avoids
   each.
5. Pair every fatal weakness you name with a concrete fix or downgrade path
   (correlational claim → association language; weak construct → operationalize
   before modeling; missing identification → narrow the claim or add a design).
6. If methods are combined, apply the Mixed Methods rule last — most
   triangulation failures are actually construct-mismatch failures dressed up as
   convergence.
