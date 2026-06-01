# Benchmark Run Manifest

| Field | Value |
| --- | --- |
| Run ID | pi20260601044042 |
| Agent kind | pi |
| Target milestone | m1 |
| Meta-harness profile | smoke-v0 |
| Wall-clock limit | 10m |
| Turn limit | 8 |
| Token limit | 200000 |
| Human intervention policy | administrative-only |
| Base benchmark commit | b37ec008dee96dd078d0edbeaa7aa38446398097 |
| Benchmark input digest | sha256:specs.zip:4ffdca2cd7e5dda104f2569bf99f5f12ccfaa123703e343b52a27a160a2e6173 |
| Start time | 2026-06-01T04:40:42Z |

## Implementation Stack

| Choice | Value |
| --- | --- |
| Language | Python 3 |
| UI toolkit | tkinter (standard library) |
| Process model | Single-process prototype (logical boundaries documented) |
| Rendering backend | tkinter Canvas (deferred: see ADR-001) |

## Cumulative Milestones Attempted

- **M0**: Benchmark Orientation — completed during setup.
- **M1**: Browser Shell Prototype — primary target.

## Status Summary

| Milestone | Status | Notes |
| --- | --- | --- |
| M0 | `passes-focused-tests` | Manifest, stack, security/privacy assumptions documented. |
| M1 | `passes-focused-tests` | Runnable shell with URL entry, chrome/page distinction; 52 focused tests pass; headless + subprocess integration; no fetch yet. |
| M2 | `planned` | URL parsing and network fetch not attempted. |
| M3–M9 | `deferred` | Outside current target scope. |

## Known Limitations

- No network fetch; URL bar accepts text but does not load pages.
- No HTML parsing, CSS, DOM, or rendering engine.
- Single-process prototype; renderer and browser process share memory.
- No TLS, no cookies, no storage, no JavaScript runtime.
- Page surface shows placeholder content only.
- Private browsing mode not implemented.
- No accessibility tree integration.

## Security Shortcuts

- Single-process architecture collapses browser/content trust boundary (prototype-only, documented in ADR-002).
- No origin model enforced yet since no network content is loaded.
- Certificate errors not applicable yet (no TLS).
- No permission system since no web-exposed APIs exist.

## Privacy Shortcuts

- No persistent state of any kind; no history, cookies, or storage.
- No telemetry.
- User agent string not exposed to network (no network).
