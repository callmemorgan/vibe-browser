# Spec Backlog

This file lists additional specs worth writing for the Vibe Browser leaderboard
and benchmark product. Each entry names the spec and the decision area it should
settle.

## Ingestion Pipeline

Defines how raw run artifacts become leaderboard records. Covers artifact
discovery, schema validation, malformed run handling, idempotent re-imports, and
where evaluator score sheets enter the system.

## Public Milestone Checker

Specifies the agent-visible `check-progress` or `check-milestone` tool. Covers
deterministic checks, allowed feedback, hidden-test boundaries, output JSON, and
how public-check status differs from evaluator confirmation.

## Evaluator Workflow

Describes the human review flow for scoring a run. Covers queue states,
assignment, rubric entry, evidence links, review comments, disagreement handling,
and final score publication.

## Evidence Model

Defines first-class evidence objects. Covers command output, verification logs,
screenshots, golden outputs, source references, design notes, evaluator notes,
and how evidence attaches to criteria and rubric categories.

## Open-Ended Run Semantics

Defines "get as far as you can" mode. Covers highest claimed milestone, highest
public-check milestone, highest evaluator-confirmed milestone, partial progress,
frontier blockers, and how open-ended runs are ranked separately from targeted
runs.

## Comparison Eligibility Rules

Turns comparison eligibility into a formal rule set. Covers prompt checksum,
benchmark commit, profile, tool versions, intervention policy, dirty baselines,
provider drift, reruns, and guided/debugged runs.

## Run State Taxonomy

Standardizes run lifecycle states. Covers queued, running, artifact-exported,
public-checked, awaiting-evaluation, evaluated, invalid, non-comparable, and
archived.

## Artifact Retention Policy

Defines what artifacts are stored, redacted, compressed, or discarded. Covers raw
transcripts, provider logs, secrets, generated submissions, diffs, screenshots,
Docker images, and long-term reproducibility.

## Security and Redaction

Specifies how the UI and ingestion layer prevent leaking secrets or hidden tests.
Covers environment redaction, log scanning, artifact download permissions,
dangerous file types, and evaluator-only notes.

## Submission Snapshot Format

Defines a portable archive format for submitted artifacts. Covers `submission/`,
manifest, version info, run summary, checksums, diffs, and commands needed to
replay verification from a clean environment.

## Verification Result Schema

Standardizes build, test, smoke, public-check, GUI, WPT, fuzz, and hidden-test
results. Covers statuses, duration, stdout/stderr links, flaky reruns, and
failure classification.

## Milestone Evidence Requirements

Lists minimum evidence required for each milestone. This is stricter than the
rubric: for example, `M2` requires fetch fixtures and TLS failure evidence, while
`M5` requires render/golden evidence.

## Blended Score Calibration

Defines how to tune milestone weighting curves. Covers linear/quadratic/cubic
comparisons, sensitivity analysis, expected score distributions, and rules for
changing score formulas between leaderboard seasons.

## Leaderboard Seasons

Defines immutable leaderboard batches. Covers season names, benchmark commits,
allowed profiles, model snapshot cutoffs, rerun policy, archival, and how old
seasons remain visible after scoring rules change.

## Model and Tool Identity

Specifies how model, provider, agent tool, harness, and runtime versions are
identified. Covers aliases, model snapshots, cloud model drift, Ollama/PI/Codex
versions, Docker image IDs, and unknown-version handling.

## Cost and Efficiency Metrics

Defines optional efficiency leaderboards. Covers wall time, tokens, cost, tool
calls, turns, milestone-per-dollar, score-per-token, and why efficiency metrics
should not override primary quality ranking.

## Failure Classification

Creates categories for failures. Covers model gave up, invalid submission,
verification failure, harness crash, provider outage, dependency outage, timeout,
tool permission failure, and suspected benchmark bug.

## Diff and Code Browser UX

Specifies how reviewers inspect generated code. Covers changed-file tree,
participant diff, syntax highlighting, file search, large-file handling, and
links from scores directly to code evidence.

## Timeline and Telemetry UX

Defines the per-turn timeline view. Covers tokens, elapsed time, tool calls,
changed paths, verification status, idle/failure counts, and event filtering
without exposing raw private reasoning.

## Screenshots and Golden Artifacts

Defines how visual evidence is captured and displayed. Covers GUI screenshots,
rendering golden tests, image diffs, viewport metadata, accessibility notes, and
artifact storage paths.

## WPT Integration View

Specifies how Web Platform Test progress appears once `M9` work begins. Covers
test directory mapping, pass/fail/expected-fail counts, flaky tests, conformance
labels, and subsystem ownership.

## Fuzzing Results View

Defines how parser/decoder fuzzing evidence is summarized. Covers target names,
corpus size, runtime, crashes, minimized repros, sanitizers, and whether fuzzing
is required for a milestone or only bonus evidence.

## API Contract

Defines HTTP or file-based APIs for the leaderboard frontend. Covers list runs,
get run detail, get artifacts, get scores, submit evaluator score, and export
batch data.

## Access Control

Defines who can view, evaluate, edit, or publish runs. Covers public viewers,
maintainers, evaluators, participants, draft scores, hidden notes, and artifact
download permissions.

## Admin Operations

Specifies maintenance screens and commands. Covers re-ingesting artifacts,
invalidating runs, merging duplicate model aliases, assigning evaluators,
locking seasons, and regenerating summaries.

## Fixture Registry

Defines public fixtures used by benchmark checks. Covers fixture names, served
URLs, checksums, expected behavior, hidden variants, and anti-hardcoding
guidelines.

## Prompt and Harness Registry

Defines how prompt sets and harness versions are displayed and compared. Covers
checksums, release notes, compatibility, deprecation, and links to exact prompt
text where public.

## Public Homepage

Defines the public landing page for the benchmark. Covers the benchmark thesis,
why browser-building is hard, what is measured, latest top results, how to run a
submission, and links to methodology, data, and artifacts.

## Public Leaderboard Page

Specifies the main public leaderboard. Covers official ranking tables,
season/batch selectors, comparable-run grouping, filters, model cards, score
breakdowns, caveats, and public download links.

## Public Run Result Page

Defines the shareable page for a single run. Covers model/tool metadata,
timeline, milestones, public-check status, evaluator scores, artifacts,
verification commands, limitations, and a stable citation URL.

## Test Run Result Sharing

Specifies how smoke tests, dry runs, failed harness trials, and non-official runs
can be shared without polluting the official leaderboard. Covers visibility
labels, expiration, artifact redaction, and "not ranked" banners.

## Result Embeds and Badges

Defines embeddable scorecards for README files, blog posts, and vendor pages.
Covers SVG/PNG badges, iframe cards, signed result snapshots, and anti-stale
version labels.

## Submission Guide

Defines public instructions for running the benchmark. Covers hardware/software
requirements, Docker setup, provider configuration, supported harnesses, artifact
upload, common failure modes, and comparison-eligibility requirements.

## Methodology Page

Explains the benchmark design publicly. Covers roadmap milestones, scoring,
rubrics, public vs hidden checks, intervention policy, profile definitions,
statistical caveats, and why browser implementation is a useful agent benchmark.

## Score Interpretation Guide

Helps readers understand what scores mean. Covers milestone depth, blended score,
rubric score, confidence, non-comparable runs, partial progress, and why a lower
score may still show an interesting capability.

## Blog Post Template

Defines the house format for result announcements. Covers title patterns,
headline result, methodology recap, key charts, surprising failure modes,
artifact links, caveats, and reproducibility notes.

## Release Notes Template

Defines how benchmark changes are announced. Covers new prompt sets, harness
changes, scoring formula updates, fixture changes, bug fixes, and whether a new
season is required.

## White Paper Outline

Defines the structure for a formal benchmark paper. Covers motivation, related
work, task design, corpus, harnesses, scoring, experiments, threats to validity,
limitations, reproducibility, and future work.

## Technical Report Generator

Specifies automated generation of per-batch analysis reports. Covers summary
tables, score distributions, milestone histograms, failure taxonomy, cost curves,
and links to representative runs.

## Run Analysis Notebook

Defines a reproducible analysis environment for benchmark data. Covers loading
`summary.json`, joining evaluator scores, plotting milestone progress, comparing
profiles, and exporting charts for posts or papers.

## Qualitative Run Analysis

Specifies how evaluators write narrative analysis of runs. Covers planning
quality, debugging behavior, code organization, testing habits, self-awareness,
scope control, and notable failure patterns.

## Failure Mode Report

Defines recurring benchmark failure categories and publication format. Covers
tool failures, model loops, overclaiming, fragile tests, missing security
boundaries, hardcoded fixtures, and under-scoped submissions.

## Model Comparison Report

Specifies a report comparing models across a fixed season. Covers aggregate
score, milestone reach, cost/time efficiency, variance, qualitative strengths,
common weaknesses, and confidence caveats.

## Harness Comparison Report

Specifies reports comparing agent tools or harnesses while holding models fixed.
Covers tool reliability, patch quality, restart behavior, context retention,
permission overhead, and artifact completeness.

## Longitudinal Trends Page

Defines charts showing benchmark progress over time. Covers best score by date,
milestone frontier, cost-to-score trends, model family trends, and benchmark
version annotations.

## Public Data Export

Specifies downloadable datasets. Covers JSONL/CSV exports, schemas, checksums,
license, redaction, artifact URLs, evaluator notes visibility, and versioned
snapshots for papers.

## Citation and DOI Policy

Defines how benchmark versions, seasons, and reports should be cited. Covers
stable URLs, semantic benchmark versions, dataset checksums, optional DOI
publication, and citation text.

## Governance and Versioning

Defines how the benchmark evolves. Covers maintainers, proposal process,
breaking scoring changes, season resets, deprecated runs, public changelog, and
appeal/review policy.

## External Submission Review

Defines how third parties submit results for inclusion. Covers required
artifacts, reproducibility checks, evaluator assignment, rejection reasons,
private embargo windows, and public disclosure.

## Result Verification Service

Specifies a hosted or CI-backed service that replays submitted artifacts. Covers
clean-room execution, resource limits, network policy, deterministic fixtures,
cache handling, and signed verification records.

## Artifact Explorer

Defines public browsing of submitted artifacts. Covers file tree, diff view,
manifest, logs, screenshots, downloads, redaction banners, and direct evidence
links from leaderboard score cells.

## Chart Library

Defines reusable visualizations for public pages and reports. Covers score
breakdowns, milestone ladders, run timelines, token/cost curves, failure
taxonomies, and comparison scatterplots.

## News and Updates Page

Defines a public feed for benchmark releases and analysis posts. Covers tags,
authors, linked seasons, linked runs, RSS/Atom support, and archive pages.

## FAQ

Defines answers for common public questions. Covers why browsers, why local
specs, how scoring works, whether hidden tests exist, how to submit, how to
compare runs, and what the benchmark does not measure.

## Ethics and Disclosure

Specifies public transparency obligations. Covers limitations of agent
benchmarks, reproducibility concerns, vendor-submitted results, conflicts of
interest, model/provider drift, and responsible interpretation.

## Brand and Naming Guidelines

Defines how the benchmark should present itself publicly. Covers official name,
logo usage, color/typography guidance, chart style, terminology, and rules for
claims like "state of the art" or "frontier result."

## Public Roadmap

Defines a public-facing roadmap for benchmark development. Covers upcoming
milestone checkers, harness support, scoring changes, WPT integration, public
data releases, and governance milestones.

## Statistical Validity

Defines how benchmark claims become statistically defensible. Covers repeated
runs, confidence intervals, variance by model and harness, tie handling,
significance thresholds, minimum sample sizes, and when a leaderboard position
should be marked "too close to call."

## Calibration Suite

Defines fixed baseline submissions used to calibrate scoring. Covers hand-written
reference artifacts for each milestone, intentionally flawed submissions,
expected rubric scores, evaluator training examples, and regression checks when
the scoring formula changes.

## Evaluator Calibration

Specifies how human evaluators stay consistent. Covers double-scoring, reviewer
agreement metrics, adjudication, rubric examples, blind review options, score
drift detection, and evaluator notes quality.

## Hidden Test Policy

Defines what hidden tests are allowed to measure and how they are protected.
Covers public/hidden split, fixture rotation, leak response, embargoes,
challenge windows, and why hidden tests must not become agent-visible feedback.

## Benchmark Contamination Policy

Specifies how to handle models trained on benchmark docs, prompts, prior
submissions, or hidden tests. Covers disclosure fields, contamination risk
labels, synthetic holdouts, periodically refreshed fixtures, and public claims
about contaminated vs clean comparisons.

## Anti-Overfitting and Anti-Gaming

Defines protections against submissions that optimize leaderboard mechanics
instead of browser behavior. Covers fixture hardcoding, fake tests, fake
milestone claims, no-op shells, overbroad dependency use, copied browser engines,
and suspiciously narrow implementations.

## Allowed Dependency Policy

Specifies which libraries are allowed, discouraged, or disqualifying. Covers UI
toolkits, parsers, networking libraries, JS runtimes, layout/rendering libraries,
browser engines, automation frameworks, and required dependency disclosure.

## Reproducibility Contract

Defines the minimum standard for reproducing a result. Covers pinned container
images, provider snapshots, package versions, artifact checksums, replay
commands, hardware assumptions, network policy, and expected nondeterminism.

## Trusted Execution Environment

Specifies the infrastructure used for official reruns. Covers container runtime,
resource isolation, privileged operations, outbound network rules, filesystem
mounts, timeout enforcement, log capture, and how to prove the run environment
matches the published condition.

## Resource Accounting

Defines how time, tokens, tool calls, cost, CPU, memory, disk, and network usage
are measured. Covers missing data, provider-reported vs harness-measured tokens,
currency conversion, retries, and whether failed infrastructure time counts.

## Provider Drift Tracking

Specifies how cloud model changes are detected. Covers model snapshot fields,
daily canary prompts, output drift alerts, provider status incidents, rerun
requirements, and labels for results from mutable model aliases.

## Baseline Agents and Reference Runs

Defines canonical baselines. Covers manual baseline, scripted baseline, simple
LLM baseline, existing agent/tool baselines, expected scores, and how baselines
are rerun each season.

## Benchmark Difficulty Tuning

Defines how to change task difficulty without destroying comparability. Covers
milestone revisions, fixture additions, scoring curve changes, profile changes,
season resets, and migration notes for historical runs.

## Threats to Validity

Specifies the public limitations section for papers and methodology pages.
Covers model contamination, tool mismatch, scoring subjectivity, browser-task
representativeness, hidden test brittleness, environment drift, and language or
dependency bias.

## Appeals and Corrections

Defines how participants challenge a score or metadata error. Covers appeal
windows, required evidence, maintainer response SLAs, correction notices,
preserving old records, and whether rank changes trigger announcements.

## Independent Replication

Specifies how outside groups can reproduce seasons. Covers downloadable
artifacts, runner instructions, checksums, expected output hashes, evaluator
rubric packets, and how to report independent replication results.

## Legal and Licensing

Defines licensing for benchmark docs, generated submissions, public datasets,
screenshots, reports, and third-party specs. Covers contributor license
agreements, model-output ownership, artifact redistribution, and takedown policy.

## Privacy Review

Specifies privacy guarantees for published runs. Covers personal paths in logs,
API keys, provider account identifiers, local usernames, machine names, network
endpoints, and redaction verification before publication.

## Security Review for Published Artifacts

Defines checks before making artifacts public. Covers malware scanning,
dangerous scripts, symlinks, large binaries, exfiltration attempts, dependency
lockfiles, and safe artifact browsing/download behavior.

## Incident Response

Specifies what happens when a secret leaks, hidden test leaks, result is
fraudulent, scoring bug is found, or official infrastructure is compromised.
Covers severity levels, takedown, notification, audit trail, and season repair.

## Provenance and Signing

Defines cryptographic provenance for official runs. Covers signed summaries,
artifact checksums, image digests, evaluator signatures, timestamping, and
verifying that a public result matches the original run.

## Determinism and Flake Policy

Defines how flaky submissions or flaky harness checks are handled. Covers rerun
counts, pass thresholds, quarantined tests, nondeterministic visual diffs,
network instability, and labels for unstable results.

## Language and Stack Breakdown

Specifies analysis by implementation stack. Covers language, UI toolkit, parser
libraries, JS runtime, renderer backend, dependency count, and whether certain
stacks systematically score better or fail differently.

## Human Baseline

Defines a calibrated human or team baseline. Covers time budget, allowed
references, tool access, skill level disclosure, artifact expectations, and how
human scores should be presented without turning the benchmark into a hiring
test.

## Economic Model

Specifies whether the benchmark has sponsorship, paid submissions, hosted runs,
or grant support. Covers vendor conflicts, disclosure, pricing, queue priority,
and firewalling financial relationships from scoring decisions.

## Community Program

Defines how external contributors participate. Covers issue labels, roadmap
proposals, fixture contributions, evaluator onboarding, discussion forums,
office hours, and recognition without compromising hidden tests.

## Reference Implementation Policy

Specifies whether benchmark maintainers provide any reference browser
implementation. Covers public examples, deliberately incomplete samples, risk of
training contamination, and how reference code is excluded from scored
submissions.

## Multi-Agent and Team Runs

Defines whether a run may use multiple agents. Covers orchestration disclosure,
role separation, shared memory, sub-agent logs, comparison grouping, and whether
multi-agent runs rank separately from single-agent runs.

## Interactive Intervention Audit

Specifies detailed logging for human approvals and interventions. Covers
permission approvals, restarts, substantive guidance, timing, actor identity,
model-visible changes, and automatic eligibility effects.

## Benchmark Meta-Evaluation

Defines how to evaluate whether Vibe Browser itself is a good benchmark. Covers
correlation with real engineering tasks, sensitivity to model improvements,
failure diversity, evaluator workload, reproducibility rate, and community
trust.

# Final Missing Spec Candidates

These are the last major gaps before the backlog feels like a genuine benchmark
program rather than a leaderboard product.

## Benchmark Charter

Defines the benchmark's constitution: what it measures, what it refuses to
measure, who it serves, what changes require a new season, and which principles
win when leaderboard excitement conflicts with scientific caution.

## Benchmark Card

Creates a public, model-card-style summary of the benchmark. Covers intended use,
out-of-scope use, task design, scoring, known biases, failure modes, data
sources, hidden tests, maintenance policy, and citation guidance.

## Result Card

Defines a standardized public card for each official result. Covers model/tool
identity, benchmark version, score, confidence, cost, artifacts, limitations,
eligibility, replication status, and caveats in a compact shareable format.

## Schema Versioning and Migrations

Specifies JSON schemas for runs, scores, artifacts, milestones, and reports.
Covers schema versions, migrations, backwards compatibility, validation errors,
and how old seasons remain readable after the product evolves.

## Data Quality Checks

Defines automated checks over imported leaderboard data. Covers impossible
values, missing artifacts, inconsistent milestone states, duplicate run IDs,
clock skew, broken links, corrupted archives, and score/category mismatches.

## Official Result Certification

Defines what turns a run into an official result. Covers artifact completeness,
clean-room rerun, evaluator signoff, redaction, provenance signature, public data
export, and publication approval.

## Draft, Private, Embargoed, and Public Results

Specifies visibility states before publication. Covers vendor embargoes,
internal dry runs, private artifact review, public release timing, who can view
what, and how embargoed results are prevented from affecting public rankings.

## Submission Identity and Organizations

Defines accounts, teams, vendors, independent researchers, and aliases. Covers
organization profiles, verified submitters, contact fields, result ownership,
transfer of ownership, and duplicate vendor/model naming.

## Tracks and Divisions

Defines separate competition tracks. Examples: cloud models, local models,
open-weights, cost-capped, time-capped, single-agent, multi-agent, guided,
unguided, targeted milestone, and open-ended frontier.

## Queueing and Run Scheduling

Specifies how official runs are scheduled. Covers fair queueing, priority,
retries, provider outages, concurrency limits, cancellation, reservations for
baseline reruns, and preventing one submitter from monopolizing infrastructure.

## Hardware and Runtime Profiles

Defines official machine classes and runtime limits. Covers CPU, memory, disk,
GPU availability, OS, architecture, container runtime, network bandwidth, and
which profile each leaderboard track uses.

## Network and Fixture Serving

Specifies the official network environment. Covers offline vs online modes,
local fixture servers, TLS fixtures, DNS behavior, blocked domains, dependency
downloads, caching, and how network policy affects comparability.

## Dependency Mirror and Supply Chain

Defines how dependencies are fetched reproducibly. Covers package mirrors,
lockfiles, allowed registries, checksum verification, yanked packages, malicious
packages, and dependency availability years later.

## Sandbox Escape and Host Safety

Specifies protections against untrusted generated code. Covers container escape
risk, syscall restrictions, root vs non-root execution, network exfiltration,
artifact scanning, resource exhaustion, and emergency kill switches.

## Accessibility Requirements for the Public Site

Defines accessibility standards for the benchmark website. Covers keyboard
navigation, screen-reader labels, color contrast, table navigation, chart
alternatives, reduced motion, and accessible artifact browsing.

## Internationalization and Time Handling

Specifies language, locale, and time presentation. Covers UTC vs local time,
date formats, number formats, translated public docs, Unicode model names, and
stable citation timestamps.

## Search, Discovery, and Compare UX

Defines how users find and compare runs. Covers global search, saved filters,
side-by-side comparisons, diffing two runs, model family pages, tag pages, and
per-season navigation.

## Model Family Pages

Defines public pages for model families and providers. Covers all runs for a
family, trend charts, best result per season, drift notes, cost/performance
summary, and links to provider disclosures.

## Benchmark Data License and Terms of Use

Separates legal use of the public dataset from source licensing. Covers
commercial use, redistribution, attribution, prohibited misrepresentation,
artifact download terms, and warranty disclaimers.

## Vendor Disclosure and Conflict Policy

Specifies how vendor involvement is disclosed. Covers sponsored runs, self-run
submissions, maintainer affiliations, paid infrastructure, report sponsorship,
and conflict labels on public pages.

## Communications and Launch Plan

Defines how benchmark launches and major updates are announced. Covers release
checklists, press/blog coordination, social snippets, embargo handling, FAQ
readiness, and rollback if a launch-blocking issue appears.

## Changelog and Deprecation Policy

Specifies public changelogs for benchmark, harness, prompt, scoring, and UI
changes. Covers severity, migration notes, deprecating old fields, retired
seasons, and linking changes to affected results.

## Reanalysis Policy

Defines when old results are recomputed. Covers scoring bug fixes, formula
changes, evaluator corrections, newly discovered contamination, model/tool
metadata corrections, and whether ranks change retroactively.

## Negative Results and Failed Runs

Specifies how to publish failures usefully. Covers failed official attempts,
invalid submissions, harness failures, model refusal/loops, non-runnable code,
and how negative evidence feeds analysis without shaming participants.

## Benchmark Issue Taxonomy

Defines labels for benchmark bugs and improvement requests. Covers harness bug,
scoring ambiguity, fixture bug, doc ambiguity, hidden-test issue, UI bug,
infra-outage, security report, and appeal.

## Maintainer Operations Handbook

Defines day-to-day operations. Covers running seasons, reviewing queues,
assigning evaluators, rotating hidden fixtures, publishing reports, responding
to appeals, and disaster recovery.

## Onboarding for Evaluators

Specifies evaluator training. Covers sample runs, calibration exercises, rubric
walkthroughs, evidence standards, common scoring mistakes, and required signoff
before scoring official runs.

## Onboarding for Submitters

Specifies participant onboarding. Covers quickstart, eligibility checklist,
artifact expectations, local dry run, common pitfalls, support channels, and
what happens after submission.

## Benchmark-to-Research Pipeline

Defines how raw leaderboard activity becomes research output. Covers hypotheses,
cohort selection, preregistered analyses, chart generation, statistical review,
paper appendices, and reproducibility bundles.

## External Integrations

Specifies integrations with eval frameworks, GitHub Actions, Hugging Face,
Weights and Biases, Papers With Code, arXiv artifacts, and package registries.
Covers sync direction, authentication, and canonical source of truth.

## Archival and Preservation

Defines long-term storage. Covers immutable season snapshots, object storage,
checksums, mirror strategy, old Docker images, dead dependency mitigation, and
how someone reruns a 2026 result in 2030.

## Deceptive or Unsafe Submission Handling

Specifies how to respond to submissions that are intentionally misleading or
dangerous. Covers fake browser engines, benchmark sabotage, crypto miners,
credential theft attempts, license laundering, and public disclosure policy.

## Public Trust Dashboard

Defines a meta-dashboard for benchmark health. Covers replication rate,
evaluation backlog, open appeals, recent corrections, hidden-test rotations,
infrastructure incidents, and maintainer disclosures.

## Benchmark Sunset or Succession Plan

Defines what happens if the benchmark becomes obsolete. Covers archival, final
season, successor benchmark, stale hidden tests, domain transfer, and preserving
historical citations.

# Final Blind-Spot Specs

These are the final program-level gaps identified after reviewing the backlog as
if Vibe Browser Benchmark were launching as a public benchmark.

## Endurance Run Protocol

Defines long-running test modes such as 24-hour frontier runs. Covers checkpoint
cadence, restart eligibility, timeout grace periods, partial artifacts,
provider outages, cost caps, and how endurance runs are compared separately from
10-minute smoke or targeted milestone runs.

## Agent Stop and Restart Policy

Specifies what happens when an agent exits before the wall clock expires. Covers
automatic continuation prompts, maximum restart count, preserving context,
detecting repeated no-op exits, labeling restarted runs, and when a stopped
agent should be considered done.

## Tool Capability Manifest

Defines a machine-readable description of the tools available to an agent.
Covers shell access, filesystem scope, Docker access, browser/UI tools, network
access, admin privileges, approval prompts, and how tool differences affect
comparison eligibility.

## Agent Memory and External State Policy

Specifies what persistent context agents may use. Covers local memory files,
provider-side memory, cached dependencies, prior benchmark runs, retrieved
public docs, hidden-test leakage risk, and disclosure labels for stateful runs.

## Reasoning Trace and Transcript Policy

Defines what portions of an agent transcript are stored, redacted, summarized,
or published. Covers private reasoning, tool calls, tool outputs, secrets,
hidden-test clues, provider metadata, and public timeline derivations.

## Prompt Injection and Malicious Content Fixtures

Specifies how benchmark fixtures may include adversarial web content. Covers
prompt-injection pages, malicious HTML/JS, deceptive instructions to the agent,
exfiltration attempts, safe rendering, and whether such fixtures are scored,
hidden, or security-only.

## Task Authoring and Review

Defines how new milestones, fixtures, and hidden tests are created. Covers
author checklists, independent review, contamination scans, ambiguity review,
oracle availability, difficulty estimates, and retirement of weak tasks.

## Ground Truth Oracle Policy

Specifies how expected behavior is established. Covers public web specs,
fixture-local assertions, golden screenshots, reference outputs, WPT metadata,
human judgment, disagreement handling, and rules for changing an oracle.

## Milestone Capability Matrix

Maps milestones to browser capabilities. Covers networking, parsing, DOM, CSS,
layout, rendering, navigation, JavaScript, storage, security, accessibility, and
which public or hidden checks provide evidence for each capability.

## LLM-Assisted Judging Policy

Defines whether model judges may help evaluate runs. Covers summarization,
rubric prefill, hallucination controls, judge model disclosure, human override,
audit sampling, and a rule that official scores remain human- or test-grounded.

## Manual Audit Sampling

Specifies periodic audits of official results. Covers random sampling, targeted
audits for top results, rerunning verification, evaluator consistency checks,
artifact redaction checks, and public correction triggers.

## Official Runner Observability

Defines internal telemetry for the hosted runner. Covers queue health, container
startup, provider latency, tool-call failures, disk pressure, token accounting,
artifact export errors, and dashboards used by maintainers.

## Hosted Service SLOs

Specifies reliability targets for public and official infrastructure. Covers
submission availability, artifact download uptime, evaluator queue latency,
rerun turnaround, incident windows, public status pages, and what is excluded
from SLO calculations.

## Submission Abuse and Rate Limits

Defines controls for spam and resource abuse. Covers per-organization quotas,
duplicate submissions, enormous artifacts, repeated failed runs, scraping, API
limits, denial-of-service protections, and manual override.

## Self-Hosted Benchmark Distribution

Specifies how others can run a local mirror. Covers Docker Compose setup,
sample data, fixture servers, local-only leaderboards, seed runs, offline mode,
and warnings that self-hosted results are not automatically official.

## Dataset and Fixture Generation Pipeline

Defines how new public and hidden fixtures are generated. Covers synthetic pages,
captured web cases, minimization, license review, expected-output generation,
metadata, randomization, and reproducible fixture builds.

## Secret and Hidden Fixture Key Management

Specifies how hidden tests and secrets are protected. Covers access controls,
rotation, storage, evaluator visibility, runner injection, leak detection,
revocation, and rebuilding seasons after compromise.

## Score Uncertainty Display

Defines how uncertainty appears in the UI. Covers confidence intervals, repeated
run variance, evaluator disagreement, too-close-to-call labels, unstable-run
warnings, and avoiding false precision in rankings.

## Benchmark Saturation Detection

Specifies when the benchmark is becoming too easy. Covers ceiling effects,
frontier clustering, reduced failure diversity, hidden-test pass rates,
milestone compression, trigger thresholds, and successor-season planning.

## Public Claims Review

Defines review for public claims made from benchmark results. Covers "SOTA"
claims, vendor marketing quotes, badges, press releases, caveats, conflict
labels, citation requirements, and takedown or correction for misleading use.
