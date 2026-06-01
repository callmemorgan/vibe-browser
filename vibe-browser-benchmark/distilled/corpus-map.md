# Corpus Map

This distilled map is for keeping context small as the benchmark spec corpus
grows.

## Current Spine

- `README.md`: entry point and design principles.
- `spec-backlog.md`: authoritative list of specs to expand.
- `spec-status.md`: progress tracker and next batch ordering.
- `final-gap-analysis.md`: final blind spots that widened the backlog.
- `specs/`: completed standalone backlog specs.

## Completed Foundation Specs

- Charter: what the benchmark is and is not.
- Benchmark card: public disclosure for a benchmark version or season.
- Result card: compact public disclosure for a single run.
- Run states: lifecycle states shared by runner, ingestion, UI, and evaluators.
- Evidence model: score-to-artifact linking.
- Comparison eligibility: rules for ranked grouping.
- Submission snapshot: portable artifact bundle.
- Verification schema: automated check result shape.
- Model/tool identity: provider, model, harness, and tool metadata.
- Certification: gates for official publication.

## Completed Run Data And Evaluation Specs

- Ingestion: how snapshots become internal records.
- Public checker: agent-visible deterministic feedback boundary.
- Evaluator workflow: human scoring, disagreement, and adjudication.
- Open-ended semantics: claimed/public/evaluator milestone progression.
- Retention: artifact classes, durations, and deletion expectations.
- Redaction: sensitive classes, scan pipeline, and publication gates.
- Milestone evidence: minimum proof per M0-M9.
- Score calibration: how formulas change safely across seasons.
- Seasons: immutable comparison batches and lifecycle states.
- Cost metrics: time, tokens, tool calls, dollars, and resource usage.

## Completed Inspection And Operations Specs

- Failure classification: canonical failure classes and analytics fields.
- Diff/code browser: safe source and diff inspection UX.
- Timeline/telemetry: run event model and filtered timeline behavior.
- Screenshots/goldens: visual evidence, metadata, and comparison display.
- WPT view: selected Web Platform Test results and expectation handling.
- Fuzzing view: fuzz target, crash, coverage, and repro summaries.
- API contract: HTTP JSON resources and response/versioning rules.
- Access control: roles, resource classes, and deny-by-default policy.
- Admin operations: maintainer actions, safeguards, and audit trails.
- Fixture registry: versioned public/hidden fixture records and serving rules.

## Completed Public Surface Specs

- Prompt/harness registry: exact prompt, harness, checker, and tool metadata.
- Homepage: public entry point and trust-first positioning.
- Leaderboard page: official ranked table and filter/export behavior.
- Run result page: canonical shareable page for one run.
- Test sharing: unofficial, provisional, failed, and dry-run sharing states.
- Embeds/badges: scoped public score badges and stale-result handling.
- Submission guide: participant workflow, prerequisites, and checklists.
- Methodology page: public explanation of task, scoring, and caveats.
- Score interpretation: reader education for scores and comparability.
- Blog template: careful public announcement structure.

## Completed Reporting And Analysis Specs

- Release notes: scoped changelog format for benchmark, harness, API, and site
  changes.
- White paper outline: citation-friendly research structure and claim
  boundaries.
- Technical report generator: repeatable report outputs from certified data.
- Run notebooks: executable analysis workbooks for seasons, runs, comparisons,
  failures, and export validation.
- Qualitative analysis: structured narrative dimensions for observed agent
  behavior.
- Failure reports: recurring negative-result summaries with public-safe
  evidence.
- Model comparisons: fixed-group model analysis with uncertainty and cost.
- Harness comparisons: agent-wrapper analysis with model/profile controls.
- Longitudinal trends: cross-season charts with compatibility annotations.
- Public data export: immutable, redacted, schema-backed export packages.

## Completed Governance And Trust Specs

- Citation/DOI: stable citation metadata for versions, seasons, reports, runs,
  and exports.
- Governance/versioning: proposal flow, roles, change classes, and season
  compatibility rules.
- External submissions: third-party intake, review, embargo, and rejection
  handling.
- Verification service: clean-room replay, resource policy, and signed records.
- Artifact explorer: safe public artifact browsing and evidence deep links.
- Chart library: reusable accessible charts with data-export backing.
- News page: public feed for releases, reports, incidents, and governance.
- FAQ: short public answers tied to source specs.
- Ethics/disclosure: conflicts, limitations, vendor submissions, and claim
  boundaries.
- Brand/naming: official names, terminology, chart tone, and third-party use.

## Completed Validity And Reproducibility Specs

- Public roadmap: non-leaking roadmap lanes, statuses, and compatibility
  signals.
- Statistical validity: sample counts, uncertainty, close-call, and repeated
  run rules.
- Calibration suite: reference submissions for scoring, verification, and
  evaluator training.
- Evaluator calibration: practice scoring, agreement checks, adjudication, and
  drift review.
- Hidden tests: private check scope, feedback boundary, and leak response.
- Contamination: exposure classes, disclosure fields, labels, and ranking
  effects.
- Anti-gaming: suspicious patterns, detection signals, and neutral outcomes.
- Dependency policy: allowed/disclose/restricted/disallowed dependency classes.
- Reproducibility: replay levels and required materials.
- Trusted execution: pinned official replay environment and drift controls.

## Completed Operational Risk And Replication Specs

- Resource accounting: consistent time, token, cost, CPU, memory, disk, and
  network metrics.
- Provider drift: mutable model alias metadata, canaries, incidents, and labels.
- Baselines: canonical simple, scripted, manual, and previous-season references.
- Difficulty tuning: controlled benchmark changes and compatibility decisions.
- Threats to validity: standard limitation categories for public claims.
- Appeals/corrections: challenge workflow and append-only correction records.
- Independent replication: external replay packets and outcome labels.
- Legal/licensing: license areas, submission rights, takedown, and notices.
- Privacy review: private data classes and publication gates.
- Artifact security review: safe preview/download decisions for submitted
  artifacts.

## Completed Program Operations Specs

- Incident response: severity, containment, repair, public notes, and reviews.
- Provenance/signing: signed official records, verification bundles, and signer
  identity policy.
- Determinism/flake: reruns, labels, quarantine, and unstable-result display.
- Language/stack: implementation metadata and cautious subgroup analysis.
- Human baseline: contextual human attempts with consent and separate display.
- Economic model: funding, paid runs, conflict disclosure, and scoring firewall.
- Community program: contribution channels without hidden-test exposure.
- Reference implementation: safe examples and contamination controls.
- Multi-agent/team runs: orchestration classes, disclosures, and separate
  comparison groups.
- Intervention audit: structured logging for approvals, guidance, restarts, and
  eligibility effects.
- Meta-evaluation: benchmark health metrics and season-close self-review.

## Completed Infrastructure And Execution Specs

- Schema versioning: versioned persisted objects, deterministic migrations, and
  archived-season compatibility.
- Data quality: automated consistency checks across ingestion, certification,
  export, and reports.
- Visibility states: draft, private, embargoed, provisional, public-ranked,
  public-unranked, and withdrawn results.
- Submission identity: people, organizations, vendors, aliases, ownership, and
  conflict labels.
- Tracks/divisions: separate comparable groups for model, agent, guidance,
  budget, and run-mode constraints.
- Queueing/scheduling: fair hosted-run queues, retries, cancellations, and
  capacity reservations.
- Hardware/runtime profiles: machine, container, OS, resource, network, and
  verifier profile identity.
- Network/fixtures: official network modes, fixture hosts, DNS/TLS behavior, and
  allowlist controls.
- Dependency mirror: reproducible package fetches, checksums, yanked package
  handling, and supply-chain checks.
- Sandbox safety: host containment, no credential leakage, network controls,
  and escape incident triggers.

## Completed Public Site And Policy Specs

- Accessibility: WCAG 2.2 AA target, keyboard access, chart alternatives, and
  artifact browsing requirements.
- Internationalization/time: RFC 3339 machine times, UTC defaults, locale-safe
  display, and canonical translations.
- Search/compare: searchable runs, filters, shareable compare views, and
  comparability-first UX.
- Model family pages: provider/family summaries with alias, drift, cost, and
  status caveats.
- Data terms: public data reuse, attribution, misrepresentation, and trademark
  limits.
- Vendor conflicts: sponsor, submitter, evaluator, and maintainer disclosures.
- Communications: launch checklists, rollback, embargo coordination, and public
  caveats.
- Changelog/deprecation: scoped changelogs, retirement dates, migration notes,
  and compatibility decisions.
- Reanalysis: metadata, scoring, replay, export, and season repair triggers.
- Negative results: failed-run publication, neutral language, and analysis use.

## Completed Program Support Specs

- Issue taxonomy: labels for areas, types, severity, priority, and escalation.
- Maintainer handbook: recurring runbooks, cadence, handoff, and safety
  principles.
- Evaluator onboarding: training modules, calibration, signoff, and review
  quality.
- Submitter onboarding: quickstart, preflight, disclosure, and support
  boundaries.
- Research pipeline: hypotheses, cohorts, data exports, notebooks, reports, and
  reproducibility bundles.
- External integrations: canonical-source rules for CI, model hubs, DOI
  repositories, and registries.
- Archival: immutable snapshots, checksums, fixity checks, and tombstones.
- Deceptive/unsafe submissions: abuse classes, quarantine, incidents, and public
  disclosure.
- Trust dashboard: public process-health metrics and health states.
- Sunset/succession: retirement triggers, final season, archival, and successor
  migration.

## Completed Final Blind-Spot Specs

- Endurance protocol: long-running frontier runs, checkpoints, cost caps, and
  separate comparison.
- Stop/restart: early exits, no-op stops, continuation policy, and public labels.
- Tool manifest: agent capabilities as comparison inputs.
- Agent memory/state: persistent context disclosure and eligibility effects.
- Transcript policy: storage, redaction, retention, and public timeline
  derivation.
- Malicious fixtures: prompt-injection and hostile-content fixture safety.
- Task authoring: new milestone, fixture, and hidden-check review flow.
- Oracles: expected behavior sources, oracle versioning, and disagreement.
- Capability matrix: milestone-to-browser-capability mapping.
- LLM judging: advisory model-judge use with human review and audit.
- Manual audits: sampled official-result checks and correction triggers.
- Runner observability: queue, verifier, provider, artifact, and scanner
  telemetry.
- Hosted SLOs: public and official infrastructure reliability targets.
- Abuse limits: submission quotas, artifact limits, and hidden-test probing
  controls.
- Self-hosting: local mirrors and officialness boundary.
- Fixture generation: deterministic fixture pipeline and metadata.
- Secret/key management: hidden fixture, signing, provider, and storage secrets.
- Score uncertainty: intervals, sample counts, close-call labels, and caveats.
- Saturation: ceiling-effect detection and successor-season planning.
- Claims review: evidence-bound review for public and third-party claims.

## Design Invariants

- Every public score must link to evidence.
- Ranked comparisons require compatible benchmark, prompt, runtime, model,
  agent, tool, and intervention profiles.
- Raw artifacts are private until redaction completes.
- Certification is stricter than local smoke-run sharing.
- Corrections append audit history instead of silently mutating old results.
- Public checker feedback never exposes hidden-test inputs or official scores.
- Efficiency views are secondary to evaluator-confirmed quality ranking.
- UI inspection surfaces must not execute submitted artifacts.
- Public WPT and fuzz results are scoped evidence, not blanket conformance or
  security claims.
- Public pages must scope every rank to season, track, profile, and
  comparability group.
- Shared badges must carry official/provisional/non-ranked state.
- Analysis outputs must distinguish certified data, provisional data, and
  exploratory interpretation.
- Public reports and charts must link to exact immutable exports.
- Cross-season trends are contextual unless the benchmark card says scores are
  compatible.
- Citable objects must identify immutable versions, exports, or result
  revisions.
- Third-party claims need conflict labels, status labels, and stable links.
- Public artifact views must render submitted content inertly.
- Charts must expose accessible text/table alternatives and comparability
  caveats.
- Benchmark branding must preserve status, season, track, and evidence scope.
- Statistical claims must show sample count, uncertainty, and comparison scope.
- Hidden-check details must never flow back to active agents.
- Reproducibility labels must say what can and cannot be replayed.
- Official verification depends on immutable runtime identity.
- Public corrections append history instead of silently changing citations.
- Provider drift and infrastructure failures must be visible in interpretation.
- Published artifacts need both privacy and security gates.
- Difficulty changes require calibration and season compatibility decisions.
- Incident repair must preserve audit history and affected-result links.
- Signed records must bind result claims to artifact digests and verifier facts.
- Flaky checks must be labeled instead of quietly retried into confidence.
- Human, multi-agent, and guided runs need separate comparison treatment.
- Funding and community participation must not affect scoring gates.
- Persisted records must declare schema versions and migration history.
- Embargoed and private runs must not affect public rank.
- Network, runtime, dependency, and sandbox profiles are comparability inputs.
- Untrusted submissions must run away from maintainer host state and secrets.
- Public UI must preserve benchmark meaning for keyboard, screen-reader, and
  chart-table users.
- Reanalysis and deprecations must link old and new records instead of changing
  history in place.
- Vendor and sponsor involvement must be visible anywhere it could affect
  interpretation.
- Community, integration, and research outputs must preserve canonical result
  status and links.
- Archived records must remain understandable after active operations end.
- Unsafe submissions are evidence-managed privately and summarized safely.
- Benchmark health metrics are public context, not score modifiers.
- Endurance, self-hosted, guided, stateful, and multi-agent runs are separate
  comparison contexts unless a season explicitly merges them.
- Agent-visible feedback must never include hidden-test or malicious-fixture
  secrets.
- Official scores remain human- or test-grounded even when LLMs assist review.
- Public claims must carry evidence, citation, uncertainty, and conflict labels.

## Next Context To Load

For ingestion or publication work, load:

- `specs/submission-snapshot-format.md`
- `specs/verification-result-schema.md`
- `specs/evidence-model.md`
- `specs/official-result-certification.md`
- `specs/ingestion-pipeline.md`
- `specs/security-and-redaction.md`

For leaderboard and scoring work, load:

- `specs/comparison-eligibility-rules.md`
- `specs/result-card.md`
- `scoring-and-ranking.md`
- `blended-score.md`
- `specs/blended-score-calibration.md`
- `specs/leaderboard-seasons.md`

For governance work, load:

- `specs/benchmark-charter.md`
- `specs/benchmark-card.md`
- `specs/model-and-tool-identity.md`
- `final-gap-analysis.md`

For evaluator work, load:

- `specs/evaluator-workflow.md`
- `specs/milestone-evidence-requirements.md`
- `milestone-rubrics.md`
- `specs/public-milestone-checker.md`

For inspection and operations work, load:

- `specs/failure-classification.md`
- `specs/diff-and-code-browser-ux.md`
- `specs/timeline-and-telemetry-ux.md`
- `specs/api-contract.md`
- `specs/access-control.md`
- `specs/admin-operations.md`

For compatibility evidence work, load:

- `specs/screenshots-and-golden-artifacts.md`
- `specs/wpt-integration-view.md`
- `specs/fuzzing-results-view.md`
- `specs/fixture-registry.md`

For public surface work, load:

- `specs/public-homepage.md`
- `specs/public-leaderboard-page.md`
- `specs/public-run-result-page.md`
- `specs/score-interpretation-guide.md`
- `specs/methodology-page.md`
- `specs/result-embeds-and-badges.md`
- `specs/submission-guide.md`

For reporting and public data work, load:

- `specs/public-data-export.md`
- `specs/technical-report-generator.md`
- `specs/run-analysis-notebook.md`
- `specs/model-comparison-report.md`
- `specs/harness-comparison-report.md`
- `specs/failure-mode-report.md`
- `specs/qualitative-run-analysis.md`

For governance and trust work, load:

- `specs/governance-and-versioning.md`
- `specs/citation-and-doi-policy.md`
- `specs/external-submission-review.md`
- `specs/result-verification-service.md`
- `specs/ethics-and-disclosure.md`
- `specs/brand-and-naming-guidelines.md`
- `specs/chart-library.md`

For validity and reproducibility work, load:

- `specs/statistical-validity.md`
- `specs/calibration-suite.md`
- `specs/evaluator-calibration.md`
- `specs/hidden-test-policy.md`
- `specs/benchmark-contamination-policy.md`
- `specs/anti-overfitting-and-anti-gaming.md`
- `specs/allowed-dependency-policy.md`
- `specs/reproducibility-contract.md`
- `specs/trusted-execution-environment.md`

For operational risk and replication work, load:

- `specs/resource-accounting.md`
- `specs/provider-drift-tracking.md`
- `specs/baseline-agents-and-reference-runs.md`
- `specs/benchmark-difficulty-tuning.md`
- `specs/threats-to-validity.md`
- `specs/appeals-and-corrections.md`
- `specs/independent-replication.md`
- `specs/legal-and-licensing.md`
- `specs/privacy-review.md`
- `specs/security-review-for-published-artifacts.md`

For program operations work, load:

- `specs/incident-response.md`
- `specs/provenance-and-signing.md`
- `specs/determinism-and-flake-policy.md`
- `specs/human-baseline.md`
- `specs/economic-model.md`
- `specs/community-program.md`
- `specs/reference-implementation-policy.md`
- `specs/multi-agent-and-team-runs.md`
- `specs/interactive-intervention-audit.md`
- `specs/benchmark-meta-evaluation.md`

For infrastructure and execution work, load:

- `specs/schema-versioning-and-migrations.md`
- `specs/data-quality-checks.md`
- `specs/draft-private-embargoed-and-public-results.md`
- `specs/submission-identity-and-organizations.md`
- `specs/tracks-and-divisions.md`
- `specs/queueing-and-run-scheduling.md`
- `specs/hardware-and-runtime-profiles.md`
- `specs/network-and-fixture-serving.md`
- `specs/dependency-mirror-and-supply-chain.md`
- `specs/sandbox-escape-and-host-safety.md`

For public site and policy work, load:

- `specs/accessibility-requirements-for-the-public-site.md`
- `specs/internationalization-and-time-handling.md`
- `specs/search-discovery-and-compare-ux.md`
- `specs/model-family-pages.md`
- `specs/benchmark-data-license-and-terms-of-use.md`
- `specs/vendor-disclosure-and-conflict-policy.md`
- `specs/communications-and-launch-plan.md`
- `specs/changelog-and-deprecation-policy.md`
- `specs/reanalysis-policy.md`
- `specs/negative-results-and-failed-runs.md`

For program support work, load:

- `specs/benchmark-issue-taxonomy.md`
- `specs/maintainer-operations-handbook.md`
- `specs/onboarding-for-evaluators.md`
- `specs/onboarding-for-submitters.md`
- `specs/benchmark-to-research-pipeline.md`
- `specs/external-integrations.md`
- `specs/archival-and-preservation.md`
- `specs/deceptive-or-unsafe-submission-handling.md`
- `specs/public-trust-dashboard.md`
- `specs/benchmark-sunset-or-succession-plan.md`

For final blind-spot work, load:

- `specs/endurance-run-protocol.md`
- `specs/agent-stop-and-restart-policy.md`
- `specs/tool-capability-manifest.md`
- `specs/agent-memory-and-external-state-policy.md`
- `specs/reasoning-trace-and-transcript-policy.md`
- `specs/prompt-injection-and-malicious-content-fixtures.md`
- `specs/task-authoring-and-review.md`
- `specs/ground-truth-oracle-policy.md`
- `specs/milestone-capability-matrix.md`
- `specs/llm-assisted-judging-policy.md`
- `specs/manual-audit-sampling.md`
- `specs/official-runner-observability.md`
- `specs/hosted-service-slos.md`
- `specs/submission-abuse-and-rate-limits.md`
- `specs/self-hosted-benchmark-distribution.md`
- `specs/dataset-and-fixture-generation-pipeline.md`
- `specs/secret-and-hidden-fixture-key-management.md`
- `specs/score-uncertainty-display.md`
- `specs/benchmark-saturation-detection.md`
- `specs/public-claims-review.md`
