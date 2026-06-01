# Calibration Suite

## Purpose

The calibration suite provides fixed reference submissions used to test scoring,
verification, evaluator training, and regression behavior when benchmark rules
change.

## Suite Contents

- minimal valid M0 shell
- M1 navigation shell
- M2 network fixture implementation
- partial implementations for each milestone
- intentionally flawed submissions
- hardcoded-fixture examples
- unsafe artifact examples for private scanner tests
- high-quality reference submissions where publication is safe
- expected verification records
- expected evaluator score sheets

## Calibration Uses

The suite runs before scoring formula releases, evaluator onboarding, hidden
checker changes, public checker changes, and major harness releases. Failures
block publication until maintainers decide whether the benchmark or calibration
expectation changed.

## Versioning

Each calibration artifact has stable ID, target milestone, intended flaw or
capability, expected outcomes, benchmark commit, checksum, and allowed public
visibility. Hidden calibration examples remain private.

## Guardrails

Calibration submissions must not become templates that agents can copy to
game the benchmark. Public examples should be deliberately incomplete when full
solutions would contaminate future runs.

## Research Basis

ACM artifact review practice motivates evaluated artifacts with expected
behavior. MLCommons-style benchmark operations motivate reference checks and
known baselines when rules or software change.

## QA Pass

Checked against `milestone-evidence-requirements.md`,
`blended-score-calibration.md`, `evaluator-workflow.md`,
`anti-overfitting-and-anti-gaming.md`, and `official-result-certification.md`.
This spec defines calibration artifacts, not the milestone rubric itself.
