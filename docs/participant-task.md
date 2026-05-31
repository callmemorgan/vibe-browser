# Vibe Browser Participant Task

You are being evaluated on your ability to build software in an unfamiliar
repository. Your task is to implement a small browser from scratch using this
repository's local standards corpus and benchmark guidance.

This document is the participant-visible task template for milestone-targeted
runs. A meta-harness or evaluator should fill in the run-specific fields before
starting a run.

## Target for This Run

Target: `{{TARGET_MILESTONE}}`

For this run, implement cumulative milestones through `{{TARGET_MILESTONE}}` as
defined in [Roadmap](roadmap.md). Do not attempt unrelated later milestones
unless they are necessary to verify the target milestone.

The target milestone must also be recorded in the root `benchmark-run.md`
manifest for the run.

## Required Submission Artifacts

At minimum, your submission must include:

- Source code for a runnable browser or browser-shaped prototype.
- Build, run, and smoke-test instructions that work from a fresh checkout.
- Automated tests for implemented behavior.
- Design notes or ADRs citing relevant local files under `specs/`.
- A status summary using the repository status vocabulary from `README.md`.
- Known limitations, unsupported behavior, and security or privacy shortcuts.

## Constraints

- Do not use Chromium, WebKit, Gecko, Electron WebView, system WebView,
  Playwright, Puppeteer, Selenium, or an equivalent browser engine or browser
  automation tool as the implementation.
- Do not hard-code public fixtures, evaluator fixtures, or hidden tests.
- Do not edit files under `specs/`.
- Keep benchmark-authored docs separate from generated implementation artifacts.
- Treat all remote content and all bytes loaded as documents as hostile input.
- Preserve a clean build, test, and smoke-test path from a fresh checkout.

General-purpose libraries are allowed for UI, networking, parsing utilities,
graphics primitives, and language runtimes. Dependencies that effectively supply
a complete browser engine must be disclosed and may affect scoring or comparison
eligibility.

## Suggested Workflow

1. Read `README.md`, [Roadmap](roadmap.md),
   [Standards Strategy](standards-strategy.md), [Testing](testing.md),
   [Security Threat Model](security-threat-model.md), and
   [Privacy Model](privacy-model.md).
2. Create or update the root `benchmark-run.md` manifest.
3. Choose an implementation stack and record it in the submission notes.
4. Build the smallest runnable browser or browser-shaped prototype that satisfies
   the target milestone.
5. Add tests for implemented behavior.
6. Record design decisions and cite relevant local spec files.
7. Run build, test, and smoke-test verification.
8. End with a concise status summary.

## Public Fixtures

The repository may include public smoke fixtures under `fixtures/`. These
fixtures are not exhaustive and are not a conformance suite. Passing them does
not prove broad compatibility. Evaluators may use hidden variations of the same
behaviors, so implementations must not hard-code fixture contents or paths.

## Final Response

When finished, summarize:

- What you implemented.
- Which milestone criteria you believe are satisfied.
- Which build, test, and smoke-test commands you ran.
- Which tests pass or fail.
- Known limitations and deferred work.
