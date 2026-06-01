# WPT Integration View

## Purpose

The WPT integration view shows how a submitted browser behaves against selected
Web Platform Tests once the benchmark reaches compatibility-focused milestones.
It must be honest about subsets, expected failures, flakes, and unsupported
areas.

## Data Inputs

Inputs include WPT manifest version, selected test paths, metadata files,
`wptreport.json`, expectation files, runtime profile, product adapter, and
verification result IDs.

## Summary Metrics

Show:

- tests discovered, scheduled, skipped, and run
- pass, fail, error, timeout, crash, and expected-fail counts
- unexpected pass/fail counts
- flaky/intermittent statuses
- subsystem and directory breakdown
- implementation-status labels
- run duration and browser restart count

## UX

The default view is a subsystem matrix: HTML, DOM, CSS, URL, fetch, navigation,
storage, JS, rendering, and security. Drill-down shows test path, variant,
expected status, actual status, logs, screenshot/reftest artifacts, owner, and
linked milestone.

## Scope Rules

WPT results are not a global browser-conformance claim unless the selected
subset, expectation metadata, and run profile justify it. Expected failures show
known gaps but do not count as capability wins.

## Research Basis

WPT documentation defines metadata layout, expected/intermittent statuses,
`wptreport.json`, implementation-status labels, and wptrunner architecture for
test loading, expectations, browser management, and restarts.

## QA Pass

Checked against `verification-result-schema.md`,
`milestone-evidence-requirements.md`, `screenshots-and-golden-artifacts.md`,
and `comparison-eligibility-rules.md`. This spec defines the view and data
contract, not which WPT subset is official.
