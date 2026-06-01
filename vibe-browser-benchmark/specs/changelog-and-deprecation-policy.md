# Changelog and Deprecation Policy

## Purpose

Changelog and deprecation policy defines how benchmark, harness, prompt,
schema, scoring, API, and UI changes are announced and retired.

## Changelog Scope

Maintain changelogs for benchmark methodology, harness, prompt sets, public
checker, hidden-check policy, API schemas, scoring formula, website UI, and
data exports.

## Deprecation Record

Each deprecation records affected feature or field, replacement, first notice
date, removal date or season, affected clients, migration guide, and public
contact.

## Breaking Changes

Breaking scoring, API, prompt, or compatibility changes require governance
review, release notes, migration plan, and season compatibility decision.

## Public Display

Deprecated fields and retired seasons remain documented. Public pages should
link from old records to replacements without pretending the old record changed
meaning.

## Research Basis

Keep a Changelog motivates structured public change history. Semantic
Versioning motivates explicit deprecation notices and compatibility signaling.

## QA Pass

Checked against `release-notes-template.md`,
`schema-versioning-and-migrations.md`, `governance-and-versioning.md`,
`api-contract.md`, and `leaderboard-seasons.md`. This spec defines deprecation
policy, not code-level warning mechanisms.
