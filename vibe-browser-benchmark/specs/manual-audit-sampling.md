# Manual Audit Sampling

## Purpose

Manual audit sampling defines periodic human checks of official results,
artifacts, scores, redaction, and public claims.

## Sample Types

- random official results
- top-ranked results
- newly certified results
- vendor-submitted results
- high-disagreement evaluations
- unusual cost or runtime outliers
- security-sensitive artifacts
- failed or negative results selected for publication

## Audit Checks

Auditors review evidence links, score consistency, redaction, artifact safety,
comparison eligibility, public labels, and export records. Audits may trigger
correction, incident, evaluator retraining, or reanalysis.

## Cadence

Run audits at season close, before major reports, after incidents, and on a
scheduled sample of current results.

## Public Reporting

Publish aggregate audit counts and significant corrections. Do not publish
private reviewer notes or hidden-test details.

## Research Basis

ACM artifact review practice motivates independent validation of artifacts and
results. Statistical sampling practice motivates random and targeted samples
for quality assurance.

## QA Pass

Checked against `official-result-certification.md`,
`evaluator-calibration.md`, `privacy-review.md`,
`security-review-for-published-artifacts.md`, and `public-trust-dashboard.md`.
This spec defines sampling policy, not audit staffing.
