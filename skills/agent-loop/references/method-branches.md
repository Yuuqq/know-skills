# Method Branches

Read the relevant branch before drafting or reviewing `loop.md`. Use these as
branch checks, not as execution steps.

## Text / Corpus Analysis

- Define corpus source, population, timeframe, language, deduplication, sampling,
  and inclusion/exclusion rules.
- Operationalize constructs as dictionaries, codes, annotations, embeddings,
  topics, classifiers, or close-reading evidence.
- Require validation: gold labels, human audit, intercoder agreement, dictionary
  face validity, model error analysis, or negative-case review.
- Unacceptable evidence: word clouds, topics, embeddings, or LLM labels alone as
  proof of a social construct.
- Data as Truth: raw text units, human-validated annotations, and analytic memos
  can be truth sources; topics, embeddings, classifiers, and LLM labels are
  measurement artifacts until validated.

## Qualitative Coding / Digital Ethnography

- Define cases, field boundary, observation units, codebook version, memo rules,
  and adjudication policy.
- Require evidence: codebook, coded excerpts, disagreement log, analytic memos,
  negative cases, and saturation or stopping rationale.
- Unacceptable evidence: unlogged interpretive judgments or unsupported quotes
  detached from context.
- Data as Truth: coded excerpts, field notes, memos, and adjudicated labels can
  be truth sources; summaries or generated interpretations require traceable
  supporting excerpts.

## Network Analysis

- Define nodes, edges, edge direction, weight, timeframe, boundary, missingness,
  and multiplex layers if any.
- Require evidence: construction log, summary diagnostics, robustness to boundary
  choices, and interpretation limits for centrality or community measures.
- Unacceptable evidence: centrality or cluster membership treated as motivation,
  influence, or power without external validation.
- Data as Truth: source records and explicit node/edge construction rules are
  truth sources; graph measures are derived artifacts.

## Causal Inference / Quasi-Experiment

- Define treatment, outcome, assignment process, comparison group, estimand, and
  identification assumption.
- Require evidence: DAG or assumption table, balance/placebo/pre-trend checks,
  sensitivity analysis, and scope conditions.
- Unacceptable evidence: correlation, prediction, or before/after difference
  stated as a causal claim without identification.
- Data as Truth: observed assignment, treatment, outcome, and covariate records
  are truth sources; estimates are derived artifacts constrained by assumptions.

## Simulation / Agent-Based Modeling

- Define agents, rules, environment, parameters, calibration target, and output
  behavior to explain.
- Require evidence: parameter table, seed policy, sensitivity analysis,
  calibration/validation target, and limits on external validity.
- Unacceptable evidence: one simulation run or visually plausible dynamics as
  proof of a social mechanism.
- Data as Truth: theory, empirical calibration targets, and observed benchmark
  patterns can ground the simulation; simulated outputs are artifacts, not
  empirical truth.

## Survey / Experiment

- Define sample frame, recruitment, instrument, treatment or vignette, outcome,
  exclusion rules, and power or precision target.
- Require evidence: instrument appendix, randomization or sampling record,
  manipulation/attention checks where appropriate, and attrition/missingness log.
- Unacceptable evidence: convenience sample generalized without scope limits.
- Data as Truth: response records, assignment logs, instruments, and sampling
  records are truth sources; scales and indices require reliability/validity
  evidence.

## Mixed Methods / Triangulation

- Define what each method contributes: discovery, measurement, explanation,
  validation, or contradiction handling.
- Require evidence: integration matrix linking findings across methods, conflict
  resolution rule, and claim-specific evidence strength.
- Unacceptable evidence: multiple weak signals treated as convergence without
  checking whether they measure the same construct.
- Data as Truth: each method keeps its own truth source; integration records
  must distinguish convergence, complementarity, and contradiction.

## Platform / Digital Trace Data

- Define platform boundary, API/search/filter behavior, collection date,
  deletion/editing risks, bot/spam handling, and terms/licensing constraints.
- Require evidence: collection manifest, query log, missingness assessment,
  de-identification rule, and external validity limits.
- Unacceptable evidence: treating returned data as the whole population or
  publishing sensitive derived data without an approval gate.
- Data as Truth: collected records and platform documentation are bounded truth
  sources for returned data only; API/search outputs are not evidence of the
  unseen population without missingness and boundary analysis.
