# Public Smoke Fixtures

These fixtures are small, benchmark-authored pages for smoke-testing early Vibe
Browser milestones. They are public orientation fixtures, not a conformance suite.

Passing these fixtures is not enough to claim broad browser compatibility.
Participants must not hard-code fixture contents, paths, or expected outputs.
Evaluators may use hidden variations of the same behaviors.

## Milestone Mapping

- `m2-network/`: main-resource fetch, redirects, content type, and basic error
  resources.
- `m3-html-dom/`: HTML parsing, document title extraction, comments, doctype, and
  malformed markup recovery.
- `m4-style-layout/`: selectors, cascade, inheritance, and simple block layout.
- `m5-paint/`: colors, borders, text painting, viewport clipping or scrolling,
  and basic image or fallback behavior.

These fixtures intentionally avoid advanced JavaScript, forms, storage, cookies,
workers, device APIs, and browser extensions.
