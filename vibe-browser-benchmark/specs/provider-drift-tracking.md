# Provider Drift Tracking

## Purpose

Provider drift tracking records when mutable model APIs, aliases, or service
conditions may have changed enough to affect benchmark results.

## Drift Signals

- model alias version change
- provider release note or status incident
- changed token accounting
- pricing change
- canary output shift
- latency or error-rate shift
- tool-call behavior change
- safety refusal behavior change
- participant report

## Required Metadata

Each run records provider, model alias, model snapshot if available, API base,
region when relevant, request parameters, provider-reported version fields,
price snapshot, and run timestamp.

## Canary Program

Maintain a small public-safe canary set that runs on a schedule and records
output hashes, token counts, latency, and error class. Canary prompts must not
include hidden tests or private benchmark fixtures.

## Result Labels

If drift is suspected, affected runs may be labeled `mutable-alias`,
`provider-drift-suspected`, `provider-incident`, or `rerun-recommended`.
Labels explain risk without retroactively changing scores by default.

## Research Basis

NIST AI RMF motivates monitoring model behavior and communicating measurement
uncertainty. HELM motivates transparent model and evaluation-condition
reporting.

## QA Pass

Checked against `model-and-tool-identity.md`, `comparison-eligibility-rules.md`,
`reproducibility-contract.md`, `longitudinal-trends-page.md`, and
`ethics-and-disclosure.md`. This spec defines drift monitoring, not provider
contracts.
