# Prompt and Harness Registry

## Purpose

The prompt and harness registry records the exact benchmark instructions,
runner behavior, tool surface, and checker versions used by each season. It
prevents vague claims like "same benchmark" when prompts or harness behavior
changed.

## Registry Records

Each registry item includes:

- `registry_id`
- type: prompt set, harness, meta-harness, checker, Docker profile, tool
  manifest, or provider adapter
- semantic version
- immutable checksum
- public display name
- release date
- compatibility range
- linked seasons
- changelog URL
- source path or package reference
- deprecation status
- known limitations

## Prompt Set Record

Prompt sets include system/developer/user task text where public, hidden or
private sections redacted by category, target milestone, intervention policy,
run mode, and checksum. If the prompt contains hidden evaluation content, publish
only the stable public digest and a redaction explanation.

## Harness Record

Harness records include launch command, package version, Docker image digest,
restart policy, turn limit, wall-clock behavior, available tools, artifact
export behavior, checker versions, and known incompatibilities.

## Display Rules

Run pages link every prompt and harness field to its registry record. Public
leaderboards expose display name and checksum; detail pages expose full metadata
allowed by visibility.

## Research Basis

HELM motivates publishing raw prompts and completions where safe, standardized
conditions, and living benchmark updates. Semantic Versioning motivates explicit
version increments around public API and compatibility changes.

## QA Pass

Checked against `model-and-tool-identity.md`, `comparison-eligibility-rules.md`,
`leaderboard-seasons.md`, `result-card.md`, and hidden-test redaction rules.
This spec owns registry metadata, not package release mechanics.
