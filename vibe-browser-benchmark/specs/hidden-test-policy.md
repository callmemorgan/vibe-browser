# Hidden Test Policy

## Purpose

The hidden test policy defines what private checks can measure, how they are
protected, and how their results influence official scoring without becoming
agent-visible instructions.

## Allowed Hidden Checks

Hidden checks may cover variant fixtures, edge cases, security boundaries,
regression cases, parser robustness, rendering comparisons, network failures,
and anti-hardcoding probes. They must test benchmark-relevant behavior already
described at a category level in public methodology.

## Protection Rules

Hidden inputs, exact assertions, expected outputs, fixture names, and failure
logs stay private. Public output may show category, pass/fail state, affected
milestone, and redacted summary.

## Agent Feedback Boundary

Agents may use public checkers during runs. Hidden-check results are evaluator
and certification evidence only and must not be streamed back into the active
agent loop.

## Leak Response

Suspected leaks trigger security hold, affected-result review, fixture rotation,
public incident note when needed, and season compatibility decision.

## Research Basis

Web Platform Tests expectation metadata motivates separating expected outcomes
from raw test execution details. Benchmark-overfitting research motivates
private holdouts and cautious public feedback.

## QA Pass

Checked against `public-milestone-checker.md`, `security-and-redaction.md`,
`official-result-certification.md`, `artifact-explorer.md`, and
`benchmark-contamination-policy.md`. This spec defines hidden-test policy, not
the exact private test corpus.
