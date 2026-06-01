# Accessibility Requirements for the Public Site

## Purpose

Accessibility requirements ensure the public benchmark can be used by readers,
submitters, evaluators, and maintainers with different abilities, devices, and
assistive technologies.

## Baseline Standard

Public pages target WCAG 2.2 AA. Any intentional exception requires documented
reason, affected page, mitigation, owner, and review date.

## Required Capabilities

- keyboard navigation for all interactive controls
- visible focus indicators
- sufficient text and non-text contrast
- screen-reader labels for tables, charts, filters, and badges
- table alternatives for charts
- skip links and landmarks
- accessible artifact browsing
- reduced-motion support
- meaningful link text
- error messages tied to form fields

## Benchmark-Specific Cases

Leaderboards need accessible sorting, filters, and comparison tables. Run pages
need accessible timelines, milestone ladders, screenshots, diffs, and evidence
links. Charts must expose underlying data tables.

## QA

Accessibility checks run before public launch, major UI changes, and chart
library releases. Automated checks are required but do not replace manual
keyboard and screen-reader review.

## Research Basis

WCAG 2.2 provides a stable W3C standard for accessible web content. WAI chart
and text-alternative guidance motivates exposing data behind visual summaries.

## QA Pass

Checked against `chart-library.md`, `public-leaderboard-page.md`,
`public-run-result-page.md`, `artifact-explorer.md`, and
`brand-and-naming-guidelines.md`. This spec defines accessibility requirements,
not final component implementations.
