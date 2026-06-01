# Screenshots and Golden Artifacts

## Purpose

Screenshots and golden artifacts provide visual evidence for shell, layout,
painting, and compatibility milestones. They help reviewers inspect rendered
behavior without relying only on text logs.

## Artifact Types

- GUI shell screenshots
- headless rendering screenshots
- golden reference images
- image diff outputs
- viewport metadata
- font/platform metadata
- accessibility annotations
- video or frame sequence for interaction-only evidence

## Metadata

Each visual artifact records viewport size, device scale factor, OS, renderer,
font set, color scheme, timestamp, command, fixture URL, expected reference,
diff algorithm, fuzz tolerance, and checksum. Golden files must include the
benchmark commit and fixture version that produced them.

## Capture Rules

Screenshots must be produced by repeatable commands. Golden comparisons should
prefer deterministic fixtures and stable fonts. If rendering depends on
platform-specific behavior, the artifact must state the runtime profile and
whether the result is comparable across profiles.

## Display Rules

The UI should show actual, expected, and diff images side by side with zoom,
pixel inspection, viewport metadata, and evidence links. For public pages,
unsafe or unredacted rendered content must stay private.

## Research Basis

WPT reftest documentation anchors reference rendering and fuzzy comparison
concepts. WPT visual-test guidance distinguishes automated testharness/reftest
preferences from screenshot-based visual checks where many conforming renderings
exist.

## QA Pass

Checked against `milestone-evidence-requirements.md`, `evidence-model.md`,
`verification-result-schema.md`, `security-and-redaction.md`, and future WPT
integration. This spec defines visual evidence, not rendering algorithms.
