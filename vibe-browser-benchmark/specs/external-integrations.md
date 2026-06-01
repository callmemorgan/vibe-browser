# External Integrations

## Purpose

External integrations define how benchmark data can connect to evaluation
frameworks, CI systems, model hubs, artifact repositories, and research indexes
without creating competing sources of truth.

## Integration Targets

- GitHub Actions
- Hugging Face datasets, model cards, or spaces
- Weights and Biases artifacts or reports
- Zenodo and DOI repositories
- Papers With Code-style indexes
- package registries
- local self-hosted mirrors
- external evaluator frameworks

## Source Of Truth

Vibe Browser remains canonical for official scores, certification state,
comparison eligibility, and artifact redaction state. External systems may
mirror public data with exact export IDs and timestamps.

## Integration Requirements

Each integration defines sync direction, authentication, data scope, status
mapping, rate limits, failure behavior, privacy boundary, and rollback path.

## Public Labels

External pages and badges must preserve official/provisional/non-comparable
labels and link to canonical run pages.

## Research Basis

Hugging Face model and leaderboard data documentation motivates structured
metadata for model evaluation sharing. Zenodo GitHub integration motivates
archived releases and citable integration points.

## QA Pass

Checked against `public-data-export.md`, `citation-and-doi-policy.md`,
`result-embeds-and-badges.md`, `provenance-and-signing.md`, and
`benchmark-data-license-and-terms-of-use.md`. This spec defines integration
contracts, not implementation credentials.
