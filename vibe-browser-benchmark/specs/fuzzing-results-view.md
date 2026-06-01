# Fuzzing Results View

## Purpose

The fuzzing results view summarizes parser, decoder, URL, CSS, and DOM fuzzing
evidence. It highlights stability and security-relevant behavior without making
fuzzing coverage look more complete than it is.

## Data Inputs

Inputs include target name, harness command, fuzzer engine, sanitizer settings,
seed corpus checksum, generated corpus size, runtime, executions per second,
coverage summary, crash count, timeout count, minimized repros, and verification
result IDs.

## Target Types

Initial targets should cover URL parsing, HTML tokenization/tree construction,
CSS parsing, MIME/content-type handling, image decoding if implemented, and
storage/cookie parsing. Later targets may include JS bindings and layout
mutation cases.

## UX

The overview table groups by target and shows status, runtime, corpus size,
coverage, crashes, timeouts, and last clean run. Drill-down shows command,
environment, sanitizer, minimized input, stack summary, reproduction status,
linked source paths, and security visibility.

## Scoring Boundary

Fuzzing is evidence, not a standalone milestone unless the milestone rubric
requires it. A clean short fuzz run can support robustness but does not prove
absence of bugs. Crashes should feed failure classification and security review.

## Research Basis

OSS-Fuzz motivates continuous fuzzing to find stability and security bugs, with
engines such as libFuzzer, AFL++, Honggfuzz, Centipede, sanitizers, distributed
execution, and crash reporting.

## QA Pass

Checked against `verification-result-schema.md`, `failure-classification.md`,
`security-and-redaction.md`, `milestone-evidence-requirements.md`, and future
security review specs. This view reports fuzzing evidence, not security
certification.
