# Milestone Capability Matrix

## Purpose

The milestone capability matrix maps benchmark milestones to browser
capabilities so readers can understand what each score actually represents.

## Capability Areas

- process and shell
- navigation
- networking
- URL parsing
- HTTP and TLS behavior
- HTML parsing
- DOM construction
- CSS parsing
- layout
- rendering
- JavaScript
- storage
- security boundaries
- accessibility
- WPT compatibility
- fuzzing robustness

## Matrix Fields

Each row maps milestone, capability, public checks, hidden checks, evaluator
evidence, artifact type, minimum acceptable proof, and known exclusions.

## Public Use

The matrix appears on methodology, score interpretation, and milestone pages.
It must explain that a milestone is evidence of selected capabilities, not full
browser conformance.

## Maintenance

Matrix changes follow task authoring, oracle, and benchmark difficulty policies.

## Research Basis

WPT subsystem organization motivates capability-oriented mapping for browser
behavior. HELM motivates transparent scenario and metric coverage rather than
opaque aggregate scores.

## QA Pass

Checked against `milestone-evidence-requirements.md`, `methodology-page.md`,
`score-interpretation-guide.md`, `wpt-integration-view.md`, and
`fuzzing-results-view.md`. This spec defines capability mapping, not scoring
weights.
