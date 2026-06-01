# Milestone Rubrics

## Purpose

Each milestone needs its own rubric because `M1` success is about a runnable
shell, while `M5` success is about rendering evidence, and `M8` success is about
state, privacy, and hardening. The leaderboard should store milestone-specific
scores separately, then combine them through the blended score.

## Status Scale

Use the same status scale for every milestone criterion:

- `0.00`: no evidence
- `0.25`: design only or placeholder
- `0.50`: partial implementation
- `0.75`: focused tests pass
- `1.00`: evaluator-confirmed for claimed scope

## Common Dimensions

Every milestone is scored across these dimensions:

- Capability: the feature works for the claimed subset.
- Verification: tests or smoke checks prove the behavior.
- Traceability: implementation cites relevant specs or benchmark docs.
- Integration: the feature connects to prior milestones.
- Honesty: limitations and deferred behavior are explicit.

Suggested weights:

| Dimension | Weight |
| --- | ---: |
| Capability | 40% |
| Verification | 25% |
| Traceability | 15% |
| Integration | 10% |
| Honesty | 10% |

## Milestone-Specific Focus

### M0: Orientation

Score understanding of target, stack, spec corpus usage, security/privacy
assumptions, and planned tests.

### M1: Shell

Score local launch, URL entry, browser chrome/content distinction, documented UI
toolkit, and process model.

### M2: Fetch

Score URL parsing subset, main-resource HTTP(S) fetch, redirect behavior, TLS
failure policy, and MIME capture.

### M3: HTML and DOM

Score tokenizer coverage, tree construction, malformed input recovery, document
title extraction, and HTML/DOM spec citations.

### M4: CSS and Layout

Score CSS parser, selector matching, cascade, inheritance, block/inline layout,
scrolling, and layout-focused tests.

### M5: Painting

Score background/border/text paint, viewport clipping, image decoding, golden
tests, and rendering backend documentation.

### M6: Navigation State

Score address navigation, back/forward/reload/stop semantics, same-document vs
cross-document handling, URL/security chrome state, and transition tests.

### M7: JavaScript

Score runtime integration, Web IDL strategy, DOM mutation, event loop behavior,
timers, microtasks, and unsupported binding disclosure.

### M8: Storage and Hardening

Score origin-aware cookies, storage semantics, private browsing behavior,
permissions, state clearing, third-party policy, and threat model updates.

### M9: Compatibility Expansion

Score WPT or equivalent integration, conformance labels, Tier 1 ownership, fuzz
targets, expected failures, and unsupported API disclosure.

## Output Shape

```json
{
  "milestone": "m4",
  "score": 0.62,
  "dimensions": {
    "capability": 0.65,
    "verification": 0.55,
    "traceability": 0.75,
    "integration": 0.60,
    "honesty": 0.80
  },
  "notes": "Block layout works for simple fixtures; inline layout incomplete."
}
```
