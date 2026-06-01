# Task Authoring and Review

## Purpose

Task authoring and review define how new milestones, fixtures, public checks,
and hidden checks are created without ambiguity, leakage, or unmeasurable
oracles.

## Authoring Checklist

- intended capability
- milestone mapping
- public description
- hidden detail boundary
- expected behavior
- oracle source
- fixture license
- difficulty estimate
- contamination risk
- accessibility and security impact
- calibration example
- retirement criteria

## Review Flow

New tasks require independent review for ambiguity, oracle quality, hardcoding
risk, hidden-test leakage, and benchmark-thesis fit. Major tasks require
calibration-suite replay before launch.

## Acceptance Criteria

A task is accepted only when it has clear evidence requirements, reproducible
fixtures, documented failure modes, and public-safe explanation.

## Retirement

Weak, leaked, saturated, or misleading tasks are retired through release notes
and season compatibility decisions.

## Research Basis

WPT contribution practice motivates peer review and clear expected behavior for
web tests. Benchmark-overfitting research motivates contamination checks and
private holdout protection.

## QA Pass

Checked against `ground-truth-oracle-policy.md`, `fixture-registry.md`,
`hidden-test-policy.md`, `calibration-suite.md`, and
`benchmark-difficulty-tuning.md`. This spec defines task governance, not
individual milestone content.
