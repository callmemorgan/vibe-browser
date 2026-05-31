# Architecture

This document describes the reference architecture for browser implementations
submitted to the Vibe Browser benchmark. It is not mandatory scaffolding or an
implementation supplied by this repository; it is the baseline shape evaluators
use when assessing whether a submission preserved important browser boundaries.

Participants may choose a simpler prototype architecture, but they should
document deviations and avoid making shortcuts look like finished design.

## Target Shape

The reference target is a multi-process browser:

- Browser process: owns trusted UI, profile state, permissions, navigation
  policy, downloads, and process coordination.
- Renderer process: handles untrusted page content, parsing, DOM, style, layout,
  painting, JavaScript execution, and event dispatch.
- Network service: fetches resources, applies protocol policy, and enforces
  security decisions shared by navigations and subresources.

Early benchmark submissions may be single-process to reduce bootstrapping cost,
but content code must still be treated as untrusted. APIs should avoid assuming
that renderer and browser state share memory unless the submission explicitly
marks that as prototype-only risk.

## Component Map

| Component | Benchmark expectation | Responsibility |
| --- | --- | --- |
| Browser chrome | Expected by M1 | Address bar, navigation controls, page surface, security indicators. |
| Browser process | Expected in design notes | Trusted orchestration, profile state, permissions, process lifecycle. |
| Renderer process | Expected in design notes | Untrusted document parsing, DOM, style, layout, paint, script execution. |
| Network stack | Expected by M2 | URL fetches, HTTP, TLS policy, redirects, cache policy, MIME decisions. |
| URL and origin model | Expected by M2 | URL parsing, origin computation, same-origin checks, site identity. |
| HTML parser | Expected by M3 | Tokenization, tree construction, document mode decisions. |
| DOM | Expected by M3 | Node tree, mutation, events, document lifecycle. |
| CSS parser | Expected by M4 | Stylesheet parsing, declarations, error recovery. |
| Style engine | Expected by M4 | Selector matching, cascade, inheritance, computed values. |
| Layout engine | Expected by M4 | Initial block and inline layout, viewport sizing, scrolling model. |
| Paint and compositing | Expected by M5 | Display list generation, rasterization, invalidation, page surface. |
| JavaScript runtime boundary | Expected by M7 | Runtime choice, bindings, event loop integration, security isolation. |
| Storage | Expected by M8 | Cookies, local/session storage, cache, profile data. |
| Permissions | Expected by M8 | Origin-scoped prompts, persistence, revocation, UI indicators. |
| Downloads | Optional | Safe destination handling, content-type policy, user consent. |
| Accessibility | Advanced scoring | Accessibility tree mapping and platform integration. |
| Extensions | Deferred | No extension API expected in baseline runs. |
| WebRTC/WebGPU/WebXR/device APIs | Deferred | Outside baseline benchmark scope. |

## Navigation Data Flow

Submissions that implement navigation should make the equivalent flow
inspectable, even if the components are not separate OS processes:

1. Browser chrome submits a URL string to the browser process.
2. Browser process parses the URL, computes navigation policy, and creates or
   selects a renderer.
3. Network stack fetches the main resource with redirect, TLS, MIME, and content
   policy checks.
4. Browser process commits a successful navigation to the renderer.
5. Renderer parses HTML, builds the DOM, fetches subresources through mediated
   network APIs, computes style, lays out content, and produces paint output.
6. Browser process presents the rendered surface and owns trusted UI indicators.

## Trust Boundaries

Remote content, all bytes from the network, local files opened as documents, and
page scripts are untrusted in submitted browsers. Trusted state includes browser
chrome, profile data, permission decisions, certificate policy, download
destinations, and process management.

The renderer must not have ambient access to:

- The filesystem.
- Profile databases.
- Raw cookies outside mediated APIs.
- Permission grants outside the current origin.
- Browser UI state.
- OS APIs not explicitly delegated.

## Design Constraints

- Security UI belongs to trusted browser chrome, never page content.
- Certificate errors fail closed until an explicit override flow is designed.
- Permission grants are origin-scoped and revocable.
- Storage APIs must be origin-aware from their first implementation.
- Parser and decoder code should be fuzzable.
- Submissions must identify prototype shortcuts that weaken these constraints.
- Evaluators should prefer explicit unsupported status over hidden boundary
  collapse.
