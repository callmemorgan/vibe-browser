# Internationalization and Time Handling

## Purpose

Internationalization and time handling define how the benchmark displays dates,
times, numbers, languages, and identifiers without confusing readers or
breaking citations.

## Timestamp Rules

Machine-readable timestamps use RFC 3339 with timezone offset or `Z`. Public
pages show UTC by default and may offer local-time display when the timezone is
clear.

## Required Fields

Run, certification, export, report, appeal, incident, and release records store
created, updated, and effective timestamps. Public pages show the timestamp
meaning, not only the value.

## Locale Handling

Numbers, dates, and currencies may be localized in UI, but exported data uses
stable machine formats. Model names, organization names, and run IDs preserve
Unicode safely.

## Translation Policy

English is canonical for methodology and scoring. Translations can be published
when they link to the canonical version, translation date, and known gaps.

## Research Basis

RFC 3339 motivates unambiguous Internet timestamps. W3C timezone guidance and
Unicode CLDR motivate explicit timezone handling and locale-aware display.

## QA Pass

Checked against `citation-and-doi-policy.md`, `public-data-export.md`,
`release-notes-template.md`, `news-and-updates-page.md`, and `api-contract.md`.
This spec defines representation rules, not a translation program.
