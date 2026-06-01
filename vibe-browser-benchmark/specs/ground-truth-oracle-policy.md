# Ground Truth Oracle Policy

## Purpose

Ground truth oracle policy defines how expected behavior is established for
tests, fixtures, screenshots, human judgments, and evaluator decisions.

## Oracle Sources

- public web specifications
- fixture-local assertions
- golden screenshots
- reference outputs
- WPT metadata
- security policy expectations
- accessibility criteria
- human evaluator judgment
- calibration artifacts

## Oracle Records

Each oracle records source, owner, version, expected behavior, confidence,
affected milestone, public-safe explanation, and change history.

## Change Rules

Changing an oracle can alter scores. Oracle changes require review, release
notes, calibration impact analysis, and reanalysis decision.

## Disagreement

When oracle evidence conflicts, evaluators record disagreement, confidence, and
chosen authority. Human judgment can supplement but should not silently replace
formal specs or fixture assertions.

## Research Basis

Web Platform Tests metadata practice motivates explicit expected outcomes.
ACM artifact review practice motivates connecting claims to evaluated artifacts
and reproducible evidence.

## QA Pass

Checked against `milestone-evidence-requirements.md`, `wpt-integration-view.md`,
`screenshots-and-golden-artifacts.md`, `evaluator-workflow.md`, and
`reanalysis-policy.md`. This spec defines oracle governance, not the full test
suite.
