# Review Checklist

Use this checklist before delivering a computational social science `loop.md`,
after user edits, and whenever a residual repeats. Fix LOCAL residuals in
place, re-scope PLANNER residuals, escalate DOMAIN EXPERT residuals for method
or interpretation review, and escalate HUMAN residuals for authorization or
non-delegable judgment.

## Residual Classification

| Residual | Class | Action |
|---|---|---|
| `goal_vague`, `term_missing` | LOCAL | Fix the relevant section. |
| `research_question_missing`, `unit_missing`, `claim_missing` | LOCAL | Add the research question, unit of analysis, and intended claim. |
| `corpus_boundary_missing`, `sampling_logic_missing`, `timeframe_missing` | LOCAL | Define source, cases, timeframe, inclusion, exclusion, and sampling logic. |
| `operationalization_missing` | LOCAL | Map each construct or claim to variables, codes, features, annotations, model outputs, or evidence artifacts. |
| `metadata_missing` | LOCAL | Require the minimum metadata or data dictionary needed to interpret the evidence. |
| `progress_invariant_missing`, `unbounded_path` | LOCAL | Add the bounded quantity or exit. |
| `skipped_grill`, `vague_answer_accepted` | LOCAL | Return to grill or re-ask with a sharper strawman. |
| `subagent_policy_missing` | LOCAL | Add Subagent Using Policy. |
| `subagent_unbounded` | LOCAL | Give the sub-task its own termination. |
| `skipped_capability_survey` | LOCAL | Survey capability before grilling subagent selection. |
| `platform_leak` | LOCAL | Replace platform names with capability semantics; keep examples parenthetical only. |
| `measurement_domain_mismatch`, `claim_measure_mismatch` | PLANNER | Re-scope the measurement domains or narrow the claim. |
| `validity_threat_unaddressed`, `reliability_unaddressed`, `triangulation_missing` | PLANNER | Add validity, reliability, triangulation, sensitivity, negative-case, or error-analysis checks. |
| `evidence_chain_missing`, `provenance_missing`, `replication_artifact_missing` | LOCAL | Add source-to-claim chain, provenance, versions, and replication artifact. |
| `truth_source_missing`, `artifact_mistaken_for_truth`, `claim_without_truth_source` | LOCAL | Name the truth source for each claim and distinguish it from measurement artifacts. |
| `trace_log_missing`, `decision_unlogged`, `failed_attempt_unlogged`, `adjudication_unlogged` | LOCAL | Add full research trace requirements for changes, failures, judgments, disputes, and claim revisions. |
| `decision_record_missing`, `rejected_alternative_missing`, `decision_without_evidence`, `validity_risk_unlogged` | LOCAL | Add decision records with rationale, evidence, rejected alternatives, scope risk, validity risk, tested, and not tested. |
| `paper_mapping_missing` | LOCAL | Map each loop output to method, result, robustness, appendix, ethics, limitations, dataset card, or replication package. |
| `method_branch_unchecked` | LOCAL | Read `references/method-branches.md` and apply the branch-specific checks. |
| `ethics_boundary_missing`, `privacy_boundary_missing`, `restricted_data_ungated` | HUMAN | Ask for authorization, consent/IRB scope, or a safer data boundary. |
| `interpretation_requires_domain_judgment`, `construct_dispute`, `coding_scheme_dispute` | DOMAIN EXPERT | Request domain or methods review before accepting the loop. |
| `subagent_role_unavailable` | HUMAN | Ask whether to change the loop or provide the missing role. |
| `ambiguous_success` | HUMAN | Ask the user for an observable success signal. |

## Hard Rules

- Design only: no loop execution, runtime code, executors, launchers, scraping, data collection, modeling, or tool-dispatch mechanics.
- Do not prescribe execution shape: no `while`, phase machine, state layout, or dispatch pseudocode.
- Do not deliver a loop with an unbounded path.
- Do not draft against an un-grilled goal unless the user explicitly accepts open questions.
- Do not deliver a CSS loop without a research question, unit of analysis, data/corpus boundary, and intended evidence product.
- Do not treat data availability as a sampling strategy.
- Do not let a strong computation substitute for a weak construct definition.
- Do not let a model metric substitute for validity, reliability, or interpretation checks.
- Do not let a generated label, topic, cluster, or embedding substitute for source-grounded evidence.
- Do not make claims that cannot be traced from raw source through processing, measurement, and interpretation.
- Do not accept a claim without a named truth source.
- Do not treat model outputs, LLM labels, embeddings, topic models, clusters, platform API returns, or scraped availability as truth sources unless separately validated.
- Do not deliver a loop without full-process trace requirements for changes, failures, human judgments, disputes, and claim revisions.
- Do not deliver a loop where consequential corpus, measurement, analysis, interpretation, ethics, or publication decisions lack decision records.
- Do not ignore privacy, consent, licensing, platform terms, IRB scope, or de-identification boundaries when sensitive or restricted data is in scope.
- Do not grill subagent selection before surveying available role capabilities.
- Do not use platform subagent names as the contract; use role capability and tool boundary.
- Do not accept reviewer claims or chain-of-thought as validation; require a domain-matched artifact.
- Every dispatched sub-task needs its own termination and no-progress bound.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Success signal is "done", "publishable", "robust", or "good enough". | State an observable check tied to an evidence artifact. |
| One loop contains several research goals. | Split or reduce to one claim and one unit of analysis. |
| `loop.md` describes a while loop, phases, or dispatch code. | Keep only design decisions and contracts. |
| "Use all available data" is treated as a corpus definition. | Add source, population, timeframe, inclusion, exclusion, and sampling logic. |
| A variable, topic, code, or embedding is treated as self-evidently valid. | Add operational definition and validation artifact. |
| Model accuracy is used as the only evidence for a social claim. | Add construct validity, error analysis, sensitivity checks, or triangulation. |
| Qualitative coding has no disagreement or adjudication rule. | Add reliability or adjudication evidence. |
| Network analysis has no node/edge definition. | Add node, edge, boundary, and missingness definitions. |
| Simulation has no calibration or external validity check. | Add calibration target, sensitivity plan, and interpretation boundary. |
| Sensitive data is routed through ordinary iteration. | Add an approval gate or narrow to de-identified/public data. |
| Correlation, co-occurrence, or topic similarity is written as a causal or mechanism claim. | Narrow the claim or add causal design, identification, or mechanism evidence. |
| Platform API returns are treated as the population. | Add platform boundary, missingness, rate-limit/filtering risks, and external validity limits. |
| LLM-generated annotations have no audit sample. | Add human review, adjudication, benchmark, or error-analysis artifact. |
| A paper result has no path to a method appendix or replication artifact. | Add paper/output mapping and reproducibility evidence. |
| A claim points to a classifier score, topic, cluster, or LLM label as if it were the underlying social fact. | Identify the truth source and treat the output as a measurement artifact needing validation. |
| Cleaning, exclusion, prompt, model, codebook, or sampling changes are not logged. | Add full research trace requirements. |
| A methodological decision has no rationale or rejected alternative. | Add a decision record. |
| Failed attempts disappear from the research history. | Log why the path failed and how it affected scope or interpretation. |
| Grill asks fill-in-the-blank questions. | Ship a recommended answer each time. |
| Vague answers are accepted politely. | Name the vagueness and offer a sharper strawman. |
| Subagent policy says "use general-purpose subagent". | Write the role capability, tool boundary, and acceptance check. |
| Subagent task has no termination. | Add max-iterations, budget, or no-progress bound. |
