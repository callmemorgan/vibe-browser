# Benchmark Issue Taxonomy

## Purpose

Benchmark issue taxonomy defines labels for bugs, proposals, appeals, incidents,
and improvement requests so maintainers can triage public work consistently.

## Label Families

- `area:harness`
- `area:scoring`
- `area:fixtures`
- `area:hidden-tests`
- `area:docs`
- `area:ui`
- `area:data-export`
- `area:security`
- `area:infrastructure`
- `type:bug`
- `type:proposal`
- `type:appeal`
- `type:incident`
- `type:question`
- `type:research`

## Severity And Priority

Separate severity from priority. Severity describes benchmark impact; priority
describes maintainer scheduling. Security, hidden-test leakage, incorrect public
rank, and privacy exposure have dedicated escalation labels.

## Required Metadata

Issue templates collect affected season, run ID, artifact ID, public URL,
expected behavior, observed behavior, reproduction steps, and disclosure needs.

## Triage Rules

Every issue receives area, type, state, and owner labels before work begins.
Appeals and security reports follow their specialized workflows.

## Research Basis

GitHub label management motivates reusable labels across issues, pull requests,
and discussions. Open-source triage practice motivates separating area, type,
severity, and status labels.

## QA Pass

Checked against `incident-response.md`, `appeals-and-corrections.md`,
`public-roadmap.md`, `admin-operations.md`, and
`community-program.md`. This spec defines taxonomy, not issue tracker
automation.
