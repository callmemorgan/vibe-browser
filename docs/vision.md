# Vision

Vibe Browser is a benchmark for evaluating how well LLM agents can build a web
browser from scratch when given a broad local standards corpus and benchmark
guidance. The task is intentionally large, ambiguous in the way real systems are,
and grounded in standards rather than toy requirements.

## Benchmark Intent

The benchmark should measure whether an LLM can turn web-platform specifications
into an executable browser-shaped system with traceable decisions, tests, and
honest scope boundaries.

The submitted browser does not need to become a production browser. It should
demonstrate meaningful progress on loading, parsing, rendering, and interacting
with web content while making every claimed behavior easy to connect to a spec,
test, or documented deviation.

Primary audiences are:

- Benchmark evaluators comparing model capability across runs.
- LLM-agent participants receiving the repository as a task packet.
- Browser, standards, security, and privacy reviewers assessing the quality of a
  submitted implementation.
- Benchmark maintainers keeping the corpus and rubric stable over time.

## Goals

- Evaluate from-scratch system design, not only code generation.
- Reward standards traceability, security reasoning, privacy reasoning, and
  test-backed claims.
- Make partial progress measurable across small browser-building milestones.
- Distinguish working behavior from plausible but unimplemented plans.
- Encourage clear architecture and inspectable data flow over opaque shortcuts.
- Preserve a stable corpus so runs can be compared over time.

## Non-Goals

- Requiring full Chrome, Safari, or Firefox compatibility.
- Shipping this repository as the browser implementation.
- Forcing one language, runtime, UI toolkit, or rendering backend by default.
- Requiring mobile browser support.
- Requiring extension ecosystem support.
- Requiring DRM, advanced media playback, WebGPU, WebXR, WebRTC, payments, or
  device APIs in baseline runs.
- Rewarding silent telemetry or behavior tracking.
- Treating unsupported behavior as failure when the submission scopes it
  honestly.

## Principles

- Corpus first: `specs/` is the supplied benchmark input and should stay stable
  within a benchmark run.
- Standards first: browser behavior claims should cite a local or canonical spec.
- Security first: remote content is hostile input in every serious submission.
- Privacy by default: persistent identifiers require explicit justification.
- Testability over ambition: untested compatibility claims do not count.
- Small milestones: each task phase should produce a demonstrable capability.
- Honest status: submissions must distinguish implemented, partial, deferred,
  unsupported, and researched behavior.
