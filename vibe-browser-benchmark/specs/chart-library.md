# Chart Library

## Purpose

The chart library defines reusable, accessible visualizations for leaderboard
pages, run pages, reports, blog posts, and notebooks. Charts should make
benchmark evidence clearer without hiding comparability caveats.

## Required Charts

- milestone ladder and frontier
- blended score breakdown
- evaluator confidence and uncertainty interval
- run timeline
- token, cost, and wall-clock curves
- failure taxonomy counts
- model comparison scatterplot
- harness comparison table chart
- longitudinal season trend
- WPT and fuzzing summary
- artifact completeness matrix

## Chart Contract

Every chart receives structured data, title, season, track, filters,
comparability group, sample count, score definition, data-export ID, and caveat
text. The chart output includes rendered view, table fallback, alt text, and
machine-readable chart data.

## Accessibility

Charts must not rely on color alone. They need text alternatives, keyboard
access for interactive controls, visible focus, sufficient contrast, and table
or CSV access to the underlying values.

## Usage Rules

No chart may mix official and provisional results without an explicit visual
distinction. Cross-season charts must show methodology-change annotations.

## Research Basis

W3C WAI and WCAG guidance motivate non-color-only communication, text
alternatives, keyboard access, and contrast. FAIR principles motivate charts
backed by reusable data exports.

## QA Pass

Checked against `public-leaderboard-page.md`, `public-run-result-page.md`,
`longitudinal-trends-page.md`, `technical-report-generator.md`, and
`score-interpretation-guide.md`. This spec defines reusable charts, not the
site-wide visual brand.
