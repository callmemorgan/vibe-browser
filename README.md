# Vibe Browser Benchmark

Vibe Browser is a benchmark for evaluating LLM agents on a deliberately hard
software engineering task: build a web browser from scratch using a local web
standards corpus.

The benchmark input is `specs/`, a large local archive of browser-relevant web,
network, media, security, accessibility, JavaScript, Unicode, graphics, and
protocol specifications. `specs.zip` is the compressed copy of that corpus. The
benchmark output is a submitted browser implementation, its tests, and the design
notes that explain how the implementation maps back to the provided specs.

This repository is not itself the browser implementation. It is the task packet,
reference corpus, evaluation rubric, and maintainer documentation for running the
benchmark.

## Start Here

- [Vision](docs/vision.md): benchmark purpose, audience, goals, and non-goals.
- [Architecture](docs/architecture.md): reference browser architecture and trust
  boundaries participants should consider.
- [Standards Strategy](docs/standards-strategy.md): benchmark scope tiers and how
  submissions should cite standards.
- [Roadmap](docs/roadmap.md): task milestones and expected submission
  capabilities.
- [Participant Task](docs/participant-task.md): milestone-targeted task template
  for benchmark participants.
- [Testing](docs/testing.md): evaluation rubric, required artifacts, tests, and
  conformance labels.
- [Evaluator Procedure](docs/evaluator-procedure.md): operational score sheet and
  evidence requirements for reviewing runs.
- [Run Organization](docs/run-organization.md): branch naming and metadata rules
  for model, tool, and harness runs.
- [Meta-Harnesses](docs/meta-harnesses.md): controller profiles for time, token,
  turn, and stop-condition limits.
- [Prompt Sets](docs/prompt-sets/browser-build-v0.md): initial stable prompt bundle
  for comparable browser-building runs.
- [Security Threat Model](docs/security-threat-model.md): security expectations
  used to evaluate submitted browsers.
- [Privacy Model](docs/privacy-model.md): privacy expectations used to evaluate
  submitted browsers.
- [Spec Inventory](docs/spec-inventory.md): curated index of representative files
  in the local standards corpus.
- [Spec Corpus Maintenance](docs/spec-corpus-maintenance.md): maintainer rules for
  updating benchmark inputs.
- [Contributing](docs/contributing.md): benchmark contribution and review
  expectations.

## Current State

The benchmark currently provides:

- A local `specs/` directory with roughly 1,015 browser-adjacent specifications.
- A compressed `specs.zip` copy of that corpus.
- Benchmark documentation in `README.md` and `docs/`.

The benchmark does not provide:

- Browser executable or UI.
- HTML, CSS, DOM, JavaScript, networking, storage, or rendering code.
- Build system or test harness.
- Web Platform Tests integration.

Those are intentionally left to benchmark participants or future harness work.

## Benchmark Objective

Given the supplied specs and documentation, an LLM agent should produce a
minimal, runnable browser implementation with:

- A browser shell or equivalent local executable.
- URL parsing and HTTP(S) main-resource fetching.
- HTML parsing into a document tree.
- Enough CSS, layout, and painting to display simple pages.
- Navigation state such as address entry, reload, and history once the shell
  exists.
- Tests and design notes that cite local spec files for claimed behavior.

Participants may implement the browser in any language or stack unless a
specific benchmark run constrains those choices. Deviations from the reference
architecture are allowed when documented and justified.

## Participant Deliverables

A benchmark submission should include:

- Source code for the browser implementation.
- Instructions to build, run, and smoke-test it locally.
- Automated tests for implemented behavior.
- Design notes or ADRs that cite relevant files from `specs/`.
- A status summary that distinguishes implemented, partial, deferred, and
  unsupported behavior.
- Any known security, privacy, or compatibility limitations.

## Evaluator Deliverables

An evaluation should record:

- The Run ID, run branch, and `benchmark-run.md` manifest.
- The model, prompt, budget limits, tool access, and environment constraints.
- The meta-harness profile, human intervention policy, and observed budget usage.
- Which target milestone or open-ended objective was attempted.
- The submitted artifacts and commands used for verification.
- Rubric scores and qualitative notes from [Testing](docs/testing.md).
- Whether the run is eligible for comparison with other runs.
- Any benchmark-input changes made before the run.

## Repository Layout

```text
.
|-- README.md
|-- docs/
|   |-- adr/
|   |-- architecture.md
|   |-- contributing.md
|   |-- evaluator-procedure.md
|   |-- meta-harnesses.md
|   |-- participant-task.md
|   |-- prompt-sets/
|   |-- privacy-model.md
|   |-- run-organization.md
|   |-- roadmap.md
|   |-- security-threat-model.md
|   |-- spec-corpus-maintenance.md
|   |-- spec-inventory.md
|   |-- standards-strategy.md
|   `-- testing.md
|-- fixtures/
|-- specs/
`-- specs.zip
```

## Project Defaults

- Treat `specs/` and `specs.zip` as benchmark inputs, not authored benchmark
  docs.
- Treat remote web content as hostile in every submitted browser.
- Require browser behavior claims to cite normative specs or documented
  deviations.
- Prefer explicit submission scope over accidental compatibility promises.
- Score the smallest demonstrable browser honestly before rewarding broader
  compatibility.
- Keep privacy and security decisions visible in the submission.

## Status Vocabulary

- `planned`: intended but not implemented.
- `researching`: requires design investigation before implementation.
- `partial`: implemented incompletely once code exists.
- `deferred`: intentionally out of near-term scope.
- `blocked`: cannot proceed without a named dependency or decision.

## Working With Specs

The files in `specs/` are upstream standards snapshots and should not be
hand-edited. Benchmark decisions belong in `docs/`, and submitted code or design
notes should cite the local spec files or canonical source specs that define the
claimed behavior.

Start with [Standards Strategy](docs/standards-strategy.md) before scoping a
benchmark run or evaluating a submitted browser subsystem.
