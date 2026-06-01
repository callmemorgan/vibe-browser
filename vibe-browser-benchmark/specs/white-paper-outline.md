# White Paper Outline

## Purpose

The white paper is the stable, citation-friendly explanation of Vibe Browser
Benchmark. It should make the benchmark credible to external readers without
turning product pages or blog posts into research papers.

## Required Outline

1. **Abstract**: task, benchmark thesis, and primary contribution.
2. **Motivation**: why long-running browser-building agents expose useful
   capabilities and failure modes.
3. **Related work**: model evaluations, coding-agent benchmarks, browser
   conformance suites, and leaderboard governance.
4. **Task definition**: repository state, target browser, agent permissions,
   time budgets, and open-ended progression.
5. **Milestone ladder**: M0-M9 intent, evidence, and scoring weight.
6. **Harness design**: runner, container profile, providers, restarts, prompts,
   artifact capture, and public checker boundary.
7. **Scoring**: evaluator workflow, blended score, eligibility, uncertainty,
   and calibration.
8. **Experiments**: season setup, model cohorts, harness cohorts, baselines,
   and ablations.
9. **Results**: milestone frontier, pass rates, cost, time, and qualitative
   behavior.
10. **Threats to validity**: provider drift, agent variance, hidden-test
   leakage, benchmark overfitting, and evaluator subjectivity.
11. **Ethics and disclosure**: publication safety, redaction, participant
   consent, and dual-use considerations.
12. **Reproducibility appendix**: data exports, code, prompts, seeds,
   environment, and artifact policy.

## Claim Rules

The paper may claim that the benchmark measures progress on this task under
defined profiles. It must not claim broad model intelligence, full browser
quality, or production security from leaderboard rank alone.

## Research Basis

HELM motivates broad transparency across prompts, metrics, scenarios, and
limitations. Model Cards, Datasheets for Datasets, and ACM artifact badging
motivate structured disclosures and reproducibility appendices.

## QA Pass

Checked against `methodology-page.md`, `benchmark-charter.md`,
`milestone-evidence-requirements.md`, `blended-score-calibration.md`, and
`security-and-redaction.md`. This spec defines the paper outline, not the
specific season results.
