# Standards Strategy

The `specs/` directory is the local standards reference archive supplied to
benchmark participants. It is not an implementation plan by itself. This document
defines which parts of the web platform matter first for benchmark scoring and
how submitted code should stay traceable to normative sources.

## Benchmark Scope Tiers

| Tier | Meaning |
| --- | --- |
| Tier 0 | Highest-priority scope for the first visible page load. |
| Tier 1 | Follow-on scope for basic modern web compatibility. |
| Tier 2 | Advanced capability scope, useful after core browsing works. |
| Deferred | Explicitly outside baseline benchmark expectations. |

Every evaluated subsystem should name its tier, cite the relevant spec files, and
document any intentionally narrower subset. Benchmark maintainers should update
this document when scoring priority changes.

## Tier 0: First Visible Page Load

Tier 0 exists to evaluate whether a submission can make one simple HTTP(S) HTML
page load, parse, style, lay out, and paint.

- URL parsing and origin basics: `specs/url.html`
- Web platform primitives: `specs/infra.html`
- Encoding: `specs/encoding.html`
- HTML parsing and document lifecycle subset: `specs/html.html`
- DOM tree basics: `specs/dom.html`
- Web IDL bindings model: `specs/webidl.html`
- Fetch model subset: `specs/fetch.html`
- MIME sniffing: `specs/mimesniff.html`
- HTTP semantics: `specs/rfc9110.html`
- HTTP caching research baseline: `specs/rfc9111.html`
- CSS syntax: `specs/css-syntax-3.html`
- CSS object model subset: `specs/cssom-1.html`
- Selectors subset: `specs/selectors-4.html`
- CSS cascade: `specs/css-cascade-5.html`
- CSS values and units: `specs/css-values-4.html`
- CSS display and box model: `specs/css-display-3.html`, `specs/css-box-3.html`
- Text basics: `specs/css-text-3.html`, `specs/unicode-segmentation.html`
- ECMAScript baseline: `specs/ecma262.html`

Tier 0 benchmark runs should deliberately exclude forms, script-heavy apps,
advanced layout, media playback, workers, persistent storage, and device APIs
unless a participant needs a tiny, well-documented subset to keep a demo page
working.

## Tier 1: Basic Modern Compatibility

Tier 1 expands the benchmark beyond first paint toward simple modern pages.

- Cookies and state: `specs/rfc6265bis.html`, `specs/cookiestore.html`
- Storage: `specs/storage.html`, `specs/IndexedDB-3.html` as research only
- Forms and inputs: `specs/html.html`, `specs/input-events-2.html`
- Referrer and secure contexts: `specs/referrer-policy.html`,
  `specs/secure-contexts.html`
- Content security policy basics: `specs/CSP3.html`
- Mixed content and upgrade policy: `specs/mixed-content.html`,
  `specs/upgrade-insecure-requests.html`
- Flex and grid basics: `specs/css-flexbox-1.html`, `specs/css-grid-1.html`
- Media queries: `specs/mediaqueries-5.html`
- Pointer, keyboard, and UI events: `specs/pointerevents4.html`,
  `specs/uievents.html`, `specs/uievents-key.html`
- Image formats required for the modern web: `specs/png-3.html`,
  `specs/GIF.html`, `specs/jpeg-t81.pdf`, `specs/webp-container.html`,
  `specs/av1-avif.html`
- Accessibility research: `specs/html-aam-1.0.html`, `specs/wai-aria-1.3.html`,
  `specs/accname-1.2.html`
- Service workers: `specs/service-workers.html` as research only until storage,
  cache, process, and security policy are ready.

## Tier 2: Capability Expansion

Tier 2 should be evaluated only once navigation, rendering, scripting, storage,
and WPT integration are stable enough for the added scope to be meaningful.

- Advanced CSS layout and animation.
- Advanced media and codecs.
- WebAssembly.
- Web Workers and Worklets.
- WebSockets and WebTransport.
- Full accessibility tree integration.
- Printing, PDF, and page media.
- Internationalization completeness.

## Deferred Areas

These APIs are intentionally outside near-term scope:

- WebGPU, WebGL completeness, and XR.
- WebRTC and real-time media.
- Payments and digital goods.
- Bluetooth, USB, HID, NFC, Serial, Smart Card, and raw local device APIs.
- FedCM, Topics, Protected Audience, attribution, and ads APIs.
- Encrypted Media Extensions and DRM.
- Browser extensions.
- Installed-app integrations and OS-level app manifests.

Deferred does not mean unimportant. It means submissions should not be penalized
for omitting the area in baseline runs, and they should not receive much credit
for implementing it before the core browser works.

## Rules for Submissions

- Cite normative specs in design notes, module docs, or implementation comments.
- Mark each implemented subsystem with a conformance label from
  [Testing](testing.md).
- Add local regression tests before claiming behavior.
- Use Web Platform Tests as the compatibility source of truth once a test harness
  exists.
- Document unsupported spec areas explicitly instead of implying broad
  compatibility.

## Rules for Maintainers

- Keep scoring tiers stable within a benchmark run.
- Update [Spec Inventory](spec-inventory.md) when adding, removing, or
  reprioritizing spec areas.
- Record tier changes in review notes or an ADR when they affect comparability.
