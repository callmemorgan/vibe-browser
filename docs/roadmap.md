# Roadmap

This roadmap defines benchmark task phases for LLM agents building a browser
from the supplied standards corpus. Each phase should produce a demonstrable
submission capability, supporting tests, and enough design notes for evaluators
to trace behavior back to [Architecture](architecture.md),
[Standards Strategy](standards-strategy.md), and [Testing](testing.md).

Benchmark runs may target a single phase, a cumulative sequence, or an open-ended
attempt. Evaluators should record which phase was attempted before scoring.

## M0: Benchmark Orientation

Goal: understand the corpus, benchmark rules, and expected browser shape before
writing browser code.

Acceptance criteria:

- Submission identifies the attempted milestone and implementation stack.
- Submission explains how it will use the local `specs/` corpus.
- Submission records initial security and privacy assumptions.
- Submission lists first observable acceptance tests.

Exclusions:

- No browser code required.
- No build system required.

## M1: Browser Shell Prototype

Goal: create a minimal executable shell or equivalent local interface with a page
surface and URL entry path.

Acceptance criteria:

- Evaluators can launch the submitted artifact locally.
- The shell can accept a URL string, even if it does not fetch yet.
- Trusted browser chrome is visually distinct from page content.
- Submission records the chosen language, UI toolkit, and process model.

Exclusions:

- No real navigation required.
- No HTML parsing or rendering required.

## M2: URL and Network Fetch

Goal: fetch a text/html resource over HTTP(S).

Acceptance criteria:

- URL parsing follows the Tier 0 subset or documents any narrower subset.
- HTTP(S) fetch can retrieve a main resource.
- Redirect behavior is specified and tested.
- TLS certificate failures fail closed.
- Response MIME type is captured for downstream parsing.

Exclusions:

- No cache required.
- No cookies required.
- No subresource loading required.

## M3: Minimal HTML and DOM

Goal: turn a simple HTML response into a document tree.

Acceptance criteria:

- HTML tokenizer handles basic tags, attributes, text, comments, and doctype.
- Tree builder creates a DOM for simple well-formed and common malformed pages.
- Document title can be extracted and shown in browser chrome or logs.
- Parser errors are recoverable for expected web input.
- Submission cites the HTML and DOM specs for implemented behavior.

Exclusions:

- No scripting required.
- No forms required.
- No custom elements required.

## M4: CSS Parsing, Style, and Layout

Goal: compute enough style and layout to display text and boxes.

Acceptance criteria:

- CSS parser handles rules, declarations, comments, and basic error recovery.
- Selectors support type, class, id, descendant, child, and simple compound
  selectors.
- Cascade handles origin, specificity, inheritance, and initial values for the
  supported property set.
- Layout supports viewport, block flow, inline text, margins, borders, padding,
  width, height, and basic scrolling.
- Submission includes focused tests for selector specificity, inheritance, and
  simple block layout.

Exclusions:

- No flex, grid, floats, transforms, or animations.
- No full font shaping beyond the initial text path.

## M5: Painting

Goal: render the styled layout tree to the page surface.

Acceptance criteria:

- Paints background, border, and text for supported layout boxes.
- Clips to viewport and scroll offset.
- Supports basic image decoding for at least one common image format.
- Has golden tests for simple pages.
- Submission documents the rendering backend and its limitations.

Exclusions:

- No GPU acceleration required.
- No advanced compositing required.

## M6: Navigation, History, and Reload

Goal: make browsing stateful.

Acceptance criteria:

- Address bar navigation loads new pages.
- Back, forward, reload, and stop have defined behavior.
- Same-document and cross-document navigation are distinguished.
- Browser chrome displays current URL and a basic security state.
- Submission tests state transitions and error cases.

Exclusions:

- No session restore required.
- No multi-tab support required unless chosen in M1.

## M7: JavaScript Runtime and Event Loop

Goal: integrate a JavaScript runtime enough for basic scripts and events.

Acceptance criteria:

- Runtime choice is recorded in an ADR.
- Web IDL binding strategy is documented.
- Script execution can read and mutate a supported DOM subset.
- Event loop, tasks, microtasks, timers, and input dispatch have tests.
- Submission states which ECMAScript and DOM bindings are unsupported.

Exclusions:

- No workers required.
- No WebAssembly required.
- No extension APIs required.

## M8: Storage, Cookies, and Hardening

Goal: add persistent state with explicit security and privacy behavior.

Acceptance criteria:

- Cookie storage is origin/site aware and tested.
- Local/session storage behavior is specified before implementation.
- Private browsing storage behavior is tested.
- Permission prompts are origin-scoped and revocable.
- Threat model is updated with implementation-specific boundaries.
- Submission documents state-clearing behavior and third-party storage policy.

Exclusions:

- No IndexedDB completeness required.
- No service worker cache required.

## M9: Compatibility Expansion

Goal: expand from prototype browser to compatibility-driven engine.

Acceptance criteria:

- Web Platform Tests are integrated into CI or an equivalent local harness.
- Subsystems publish conformance labels.
- Tier 1 standards have owners and focused test plans.
- Fuzz targets exist for URL, HTML, CSS, image, and network parsers.
- Submission records expected failures and unsupported APIs explicitly.

Exclusions:

- No promise of full web compatibility.
- Deferred APIs remain out of scope unless reprioritized by ADR.
