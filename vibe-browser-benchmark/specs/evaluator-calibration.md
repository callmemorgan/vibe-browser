# Evaluator Calibration

## Purpose

Evaluator calibration keeps human scoring consistent across reviewers, seasons,
and model cohorts. It turns the rubric into practiced judgment rather than
private intuition.

## Calibration Activities

- onboarding packet with rubric examples
- practice scoring on calibration-suite runs
- double scoring for a sampled share of official submissions
- disagreement review and adjudication
- periodic score-drift checks
- evaluator note quality review
- retraining after rubric or milestone changes

## Metrics

Track reviewer agreement, adjudication rate, score deltas by milestone,
time-to-review, returned-for-evidence rate, and missed-redaction escalation.
Agreement metrics should be used to improve the rubric, not to punish honest
reviewer disagreement.

## Blind Review

Where practical, evaluator views hide submitter identity, vendor relationship,
and leaderboard rank during first-pass scoring. Model and harness metadata may
remain visible when required to interpret evidence.

## Review Artifacts

Calibration records include scored examples, decision notes, adjudication
outcomes, rubric version, evaluator IDs, and training completion status.

## Research Basis

Inter-rater reliability practice motivates repeated scoring, agreement
measurement, and adjudication. ACM artifact review practice motivates
structured evaluation notes tied to evidence.

## QA Pass

Checked against `evaluator-workflow.md`, `milestone-evidence-requirements.md`,
`calibration-suite.md`, `official-result-certification.md`, and
`statistical-validity.md`. This spec defines evaluator consistency practices,
not individual evaluator performance management.
