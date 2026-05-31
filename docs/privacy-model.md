# Privacy Model

Vibe Browser benchmark submissions should minimize persistent identifiers, make
state visible and controllable, and avoid telemetry unless the submission has a
documented opt-in design. Privacy behavior is part of browser correctness and is
included in benchmark scoring.

## Privacy Defaults

- No telemetry is collected or transmitted until an explicit opt-in telemetry ADR
  or design note exists.
- Private browsing leaves no persistent history, cookies, cache, storage, or
  permission grants after the private session closes.
- Storage and cookie behavior must be origin-aware from the first
  implementation.
- Third-party storage and cookies require an explicit policy before shipping.
- New APIs that reveal device, network, user, or environment entropy require a
  privacy review.
- Browser UI should expose site identity and permission state clearly once those
  systems exist.
- Submissions that do not implement a privacy-sensitive feature should say so
  directly rather than implying support.

## State Surfaces

| Surface | Default Policy |
| --- | --- |
| History | Persist only in normal browsing mode. |
| Cookies | Origin/site aware; third-party behavior must be specified before use. |
| Local storage | Origin-scoped; private mode must be ephemeral. |
| Session storage | Origin and browsing-context scoped. |
| Cache | Partitioning policy required before persistent cache ships. |
| Permissions | Origin-scoped, visible, revocable, and private-mode ephemeral. |
| Downloads | User-visible filesystem writes only. |
| Telemetry | Disabled unless future opt-in design exists. |
| Crash reports | Local-only until a documented submission flow exists. |

## Fingerprinting

Fingerprinting risk comes from any stable or high-entropy signal exposed to web
content. Examples include user agent strings, client hints, canvas and graphics
output, installed fonts, device APIs, timing precision, screen geometry, locale,
media capabilities, and hardware concurrency.

Initial decisions:

- Keep user agent and client hints simple until compatibility requires more.
- Avoid exposing device APIs in early milestones.
- Do not add high-resolution timers beyond what the JavaScript/event-loop design
  requires.
- Treat graphics, fonts, media capabilities, and local device APIs as privacy
  review triggers.
- Use `specs/fingerprinting-guidance.html`,
  `specs/privacy-principles.html`, and `specs/nav-tracking-mitigations.html` as
  reference material for future reviews.

## Private Browsing Semantics

Private browsing should eventually provide:

- Separate in-memory cookie jar.
- Separate in-memory storage.
- No persistent history writes.
- No persistent cache writes.
- No persistent permission grants.
- No reuse of normal-mode session state unless explicitly designed.

Until implemented, docs and UI must not claim private browsing exists.

## Privacy Review Checklist

Before adding, changing, or evaluating a web-exposed capability, answer:

- Can this identify a user, device, installation, or network?
- Does it persist across sessions?
- Is it visible to third-party content?
- Does private browsing change the behavior?
- Can the user inspect, clear, or revoke the state?
- Which origin owns the state?
- Which specs define the behavior?
- What regression tests prove isolation?

Evaluators should score explicit, tested privacy limitations higher than broad
claims that leave state ownership or persistence unclear.
