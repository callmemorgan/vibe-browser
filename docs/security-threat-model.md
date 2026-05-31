# Security Threat Model

Vibe Browser benchmark submissions must treat the web as hostile input. This
threat model defines the default security expectations evaluators should apply to
submitted browsers so prototype shortcuts do not become silent architecture
decisions.

## Assets in a Submitted Browser

- User profile data, including cookies, storage, history, permissions, and cache.
- Local filesystem and download destinations.
- Browser chrome and security indicators.
- Network credentials, TLS decisions, and authenticated sessions.
- OS APIs and device access.
- Process integrity and memory safety boundaries.

## Trust Boundaries

| Boundary | Default |
| --- | --- |
| Web content to renderer | Web content is hostile. |
| Renderer to browser process | Renderer is untrusted and must use mediated APIs. |
| Browser process to profile data | Browser process owns trusted profile access. |
| Network to parser/decoder | All bytes are attacker-controlled. |
| Page content to browser chrome | Page content cannot draw trusted UI. |
| Web origin to permission grants | Grants are origin-scoped and revocable. |
| Downloads to filesystem | Writes require user-mediated destination policy. |

## Primary Threats

- Malicious pages exploiting parser, decoder, layout, or script bugs.
- Renderer compromise attempting filesystem, profile, or OS access.
- Origin confusion exposing cookies, storage, or permissions cross-site.
- Certificate or TLS downgrade attacks.
- Download abuse, path confusion, and unsafe file opening.
- Permission spoofing through misleading page UI.
- Mixed content weakening an otherwise secure page.
- Cache, history, or storage leaks between browsing modes.
- Fingerprinting and persistent identifiers created by implementation details.

## Default Decisions

- Remote content, local files loaded as documents, and page scripts are untrusted.
- Renderer/content code must never have ambient filesystem access.
- Certificate errors fail closed unless a future ADR defines an explicit override
  flow.
- Browser chrome owns security indicators and permission UI.
- Permission grants are origin-scoped, visible, and revocable.
- Storage and cookies are origin-aware from their first implementation.
- Downloads must not silently overwrite arbitrary paths.
- Mixed active content is blocked once secure-context policy exists.
- Dangerous APIs require a security and privacy review before implementation.
- Benchmark submissions may defer a feature, but they should not implement it
  with weaker defaults without naming the risk.

## Review Checklist for New Browser Surfaces

Before adding or evaluating a browser-facing feature, answer:

- What untrusted input does it parse or decode?
- Which process owns the trusted decision?
- Which origin can access the data or capability?
- Can page content spoof the UI or state?
- Does failure default to deny, block, or no-op?
- What profile data can it read or write?
- What tests prove cross-origin and private-mode isolation?
- Which standards define the behavior?

## Prototype Rules

Early prototypes may use simplified process boundaries, but they must preserve
the logical boundary in APIs and docs. If a shortcut gives content direct access
to trusted state, it must be marked `blocked` or `researching`, not treated as an
acceptable architecture.

Evaluators should reward submissions that identify their own security shortcuts
and penalize submissions that hide trusted-state exposure behind vague status
claims.
