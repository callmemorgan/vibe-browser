# Dependency Mirror and Supply Chain

## Purpose

Dependency mirror and supply chain define how dependencies are fetched,
cached, verified, and preserved so results remain reproducible and safe.

## Mirror Responsibilities

- serve approved registries and package versions
- preserve package checksums
- record source registry and retrieval time
- handle yanked or unavailable packages
- block known malicious packages
- support lockfile-based fetches
- expose audit metadata for verification

## Submission Requirements

Submissions include lockfiles, package manager version, install command,
dependency source list, checksums where available, and restricted dependency
disclosures.

## Supply-Chain Checks

Official verification checks package provenance where available, known
vulnerabilities, install scripts, unexpected binaries, typosquatting risk, and
dependency policy class.

## Long-Term Preservation

Season archives preserve dependency metadata and mirror manifests even when the
actual package bytes cannot be redistributed publicly.

## Research Basis

SLSA dependency and provenance concepts motivate recording resolved
dependencies and supply-chain integrity facts. OpenSSF Scorecard practice
motivates dependency risk assessment as part of software trust.

## QA Pass

Checked against `allowed-dependency-policy.md`,
`reproducibility-contract.md`, `security-review-for-published-artifacts.md`,
`trusted-execution-environment.md`, and `legal-and-licensing.md`. This spec
defines dependency infrastructure, not package-manager-specific commands.
