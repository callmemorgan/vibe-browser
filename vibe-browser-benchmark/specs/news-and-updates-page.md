# News and Updates Page

## Purpose

The news and updates page collects benchmark announcements, releases, analysis,
corrections, and operational notices in one public feed. It keeps the homepage
focused while preserving a durable public history.

## Content Types

- benchmark release
- harness release
- season launch or archive
- result announcement
- analysis post
- technical report
- correction or withdrawal
- incident notice
- roadmap update
- governance decision

## Entry Metadata

Each entry includes title, summary, author, publication date, updated date,
status, tags, affected season, affected runs, related release note, related data
export, and canonical URL.

## Feed Requirements

Provide RSS or Atom feed support for all public entries and filtered feeds for
release notes, reports, and incidents. Feed entries should include stable links,
update timestamps, and concise summaries without private artifact content.

## Archive UX

Readers can filter by season, tag, content type, model, harness, and status.
Correction and incident entries remain visible and link to superseded public
claims.

## Research Basis

Atom syndication practice motivates stable IDs, timestamps, authorship, and
updated entries for feeds. Keep a Changelog motivates visible release history
and correction-oriented communication.

## QA Pass

Checked against `blog-post-template.md`, `release-notes-template.md`,
`public-homepage.md`, `longitudinal-trends-page.md`, and
`citation-and-doi-policy.md`. This spec defines the public feed, not individual
post content.
