# Spec Inventory

The repository includes a large local standards corpus under `specs/` and a
compressed copy in `specs.zip`. At the time this document was created, the corpus
was roughly 1,015 files, about 521 MB expanded and 87 MB compressed.

This inventory is curated. It is not a complete list of every file in `specs/`.
Its purpose is to orient benchmark participants and evaluators toward
representative local references. The presence of a spec in the corpus does not
mean baseline submissions must implement it.

## Core Platform

| Area | Representative files | Priority |
| --- | --- | --- |
| Platform primitives | `specs/infra.html`, `specs/webidl.html` | Tier 0 |
| URL and origins | `specs/url.html`, `specs/rfc6454.html` | Tier 0 |
| Encoding and Unicode | `specs/encoding.html`, `specs/unicode-segmentation.html`, `specs/unicode-normalization.html` | Tier 0 |
| HTML and DOM | `specs/html.html`, `specs/dom.html` | Tier 0 |
| Events | `specs/uievents.html`, `specs/input-events-2.html`, `specs/pointerevents4.html` | Tier 1 |

## Networking

| Area | Representative files | Priority |
| --- | --- | --- |
| Fetch | `specs/fetch.html`, `specs/fetch-metadata.html` | Tier 0 |
| HTTP | `specs/rfc9110.html`, `specs/rfc9111.html`, `specs/rfc9112.html`, `specs/rfc9113.html`, `specs/rfc9114.html` | Tier 0/Tier 1 |
| MIME | `specs/mimesniff.html`, `specs/rfc2045.html`, `specs/rfc2046.html` | Tier 0 |
| TLS and certificates | `specs/rfc8446.html`, `specs/rfc5280.html`, `specs/cabf-baseline.pdf` | Tier 1 |
| QUIC and HTTP/3 | `specs/rfc9000.html`, `specs/rfc9001.html`, `specs/rfc9002.html`, `specs/rfc9114.html` | Tier 2 |
| WebSocket and transport | `specs/websockets.html`, `specs/webtransport.html` | Tier 2 |

## JavaScript and WebAssembly

| Area | Representative files | Priority |
| --- | --- | --- |
| ECMAScript | `specs/ecma262.html` | Tier 0/Tier 1 |
| Intl | `specs/ecma-402.html`, `specs/ecma402.html` | Tier 2 |
| TC39 proposals | `specs/tc39-*.html` | Deferred until runtime baseline exists |
| WebAssembly | `specs/wasm-core-2.html`, `specs/wasm-js-api-2.html`, `specs/wasm-web-api-2.html` | Tier 2 |

## CSS, Layout, and Rendering

| Area | Representative files | Priority |
| --- | --- | --- |
| CSS parsing | `specs/css-syntax-3.html`, `specs/cssom-1.html` | Tier 0 |
| Cascade and values | `specs/css-cascade-5.html`, `specs/css-values-4.html` | Tier 0 |
| Selectors | `specs/selectors-4.html`, `specs/selectors-5.html` | Tier 0/Tier 2 |
| Box and display | `specs/css-display-3.html`, `specs/css-box-3.html` | Tier 0 |
| Text | `specs/css-text-3.html`, `specs/css-writing-modes-3.html` | Tier 0/Tier 1 |
| Flex and grid | `specs/css-flexbox-1.html`, `specs/css-grid-1.html` | Tier 1 |
| Animation and transforms | `specs/css-animations-1.html`, `specs/css-transforms-1.html`, `specs/web-animations-1.html` | Tier 2 |

## Storage and State

| Area | Representative files | Priority |
| --- | --- | --- |
| Cookies | `specs/rfc6265bis.html`, `specs/rfc6265.html`, `specs/cookiestore.html` | Tier 1 |
| Storage | `specs/storage.html`, `specs/storage-access.html`, `specs/storage-buckets.html` | Tier 1/Tier 2 |
| IndexedDB | `specs/IndexedDB-3.html` | Tier 2 |
| Cache/service workers | `specs/service-workers.html` | Tier 2 |

## Security and Privacy

| Area | Representative files | Priority |
| --- | --- | --- |
| Secure contexts | `specs/secure-contexts.html` | Tier 1 |
| CSP | `specs/CSP3.html`, `specs/csp-next.html` | Tier 1/Tier 2 |
| Mixed content | `specs/mixed-content.html`, `specs/upgrade-insecure-requests.html` | Tier 1 |
| Referrer and permissions policy | `specs/referrer-policy.html`, `specs/permissions-policy-1.html` | Tier 1 |
| Privacy guidance | `specs/privacy-principles.html`, `specs/fingerprinting-guidance.html`, `specs/nav-tracking-mitigations.html` | Tier 1 reference |
| Reporting | `specs/reporting-1.html`, `specs/network-error-logging.html`, `specs/crash-reporting.html` | Tier 2 |

## Media, Images, and Codecs

| Area | Representative files | Priority |
| --- | --- | --- |
| Images | `specs/png-3.html`, `specs/GIF.html`, `specs/jpeg-t81.pdf`, `specs/webp-container.html`, `specs/av1-avif.html` | Tier 1 |
| Media element | `specs/html.html`, `specs/media-capabilities.html`, `specs/media-source-2.html` | Tier 2 |
| Codecs | `specs/webcodecs.html`, `specs/av1-spec.html`, `specs/vp9-bitstream.html`, `specs/flac-format.html` | Tier 2/Deferred |
| DRM | `specs/encrypted-media-2.html` | Deferred |

## Accessibility

| Area | Representative files | Priority |
| --- | --- | --- |
| ARIA | `specs/wai-aria-1.3.html`, `specs/html-aria.html` | Tier 1/Tier 2 |
| Accessible names | `specs/accname-1.2.html` | Tier 1 |
| Accessibility mappings | `specs/html-aam-1.0.html`, `specs/core-aam-1.2.html`, `specs/svg-aam-1.0.html` | Tier 2 |
| WCAG reference | `specs/WCAG22.html`, `specs/wcag-3.0.html` | Reference |

## Graphics and GPU

| Area | Representative files | Priority |
| --- | --- | --- |
| SVG | `specs/SVG2.html`, `specs/svg-paths.html`, `specs/svg-strokes.html` | Tier 2 |
| Canvas/WebGL | `specs/webgl1.html`, `specs/webgl2.html`, `specs/WEBGL_*.html` | Tier 2/Deferred |
| WebGPU | `specs/webgpu.html`, `specs/WGSL.html` | Deferred |
| Native graphics references | `specs/vulkan-spec.html`, `specs/metal-sl.pdf`, `specs/gles2-spec.pdf`, `specs/gles3-spec.pdf` | Reference |

## Device, Identity, and Experimental APIs

| Area | Representative files | Priority |
| --- | --- | --- |
| Device APIs | `specs/webusb.html`, `specs/webhid.html`, `specs/serial.html`, `specs/web-bluetooth.html`, `specs/web-nfc.html` | Deferred |
| WebRTC | `specs/webrtc.html`, `specs/webrtc-stats.html`, `specs/webrtc-ice.html` | Deferred |
| Payments | `specs/payment-request.html`, `specs/secure-payment-confirmation.html` | Deferred |
| Identity and credentials | `specs/webauthn-3.html`, `specs/credential-management-1.html`, `specs/fedcm-1.html` | Tier 2/Deferred |
| Ads and attribution | `specs/topics.html`, `specs/attribution-reporting-api.html`, `specs/turtledove.html` | Deferred |

## Maintenance Rule

When adding, removing, or replacing vendored specs:

- Update this inventory if the change affects a category or priority.
- Record source URL and snapshot information when available.
- Do not hand-edit upstream spec snapshots.
- Keep [Standards Strategy](standards-strategy.md) in sync with priority changes.
- Record whether the change affects benchmark comparability for previous runs.
