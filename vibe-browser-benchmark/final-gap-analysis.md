# Final Gap Analysis

This pass asks what would still be missing if Vibe Browser Benchmark were meant
to become a durable public benchmark, not just a leaderboard UI.

## Assessment

The existing specs cover the visible product well: leaderboard pages, run detail
pages, scoring, artifacts, public reports, governance, submissions, access
control, reproducibility, and public communications. The remaining gaps are
mostly about trust at the edges: long-running agent behavior, admissible tool
surfaces, task authorship, oracle design, transcript privacy, service
operations, and abuse handling.

## Final Missing Areas

- **Agent lifecycle**: 10-minute smoke tests and 24-hour frontier tests need
  different restart, pause, timeout, and checkpoint rules.
- **Tool boundaries**: official runs need a machine-readable manifest of tools,
  permissions, filesystem access, network access, and human approvals.
- **External state**: agents may have memories, caches, prior run artifacts, or
  provider-side context. Comparison rules need an explicit state policy.
- **Ground truth**: each milestone needs an oracle strategy, not only a rubric.
  Browser behavior should be checked against fixtures, golden outputs, public
  specs, and eventually WPT metadata.
- **Task authorship**: fixtures, hidden checks, and milestones need a review
  process so benchmark maintainers do not accidentally create brittle or
  contaminated tasks.
- **Transcript policy**: raw agent traces can include secrets, private reasoning,
  provider metadata, and hidden-test clues. Publication needs a clear boundary.
- **LLM-assisted judging**: judges can help summarize evidence, but official
  scores should define when model-generated analysis is advisory only.
- **Public trust operations**: a real benchmark needs SLOs, audit sampling,
  anti-abuse controls, and public claims review, not only data exports.

## Research Anchors

- HELM motivates broad, multi-metric, transparent evaluation rather than a single
  accuracy number: https://arxiv.org/abs/2211.09110
- MLCommons emphasizes fair comparison, reproducibility, useful measurement, and
  affordable participation: https://mlcommons.org/benchmarks/
- ACM artifact badging separates artifact availability, artifact evaluation, and
  validated results: https://www.acm.org/publications/policies/artifact-review-and-badging-current
- SWE-bench Verified shows the value of containerized evaluation harnesses for
  agentic coding tasks: https://openai.com/index/introducing-swe-bench-verified/
- WPT expectation metadata is a useful model for expected failures and flaky
  results: https://web-platform-tests.org/tools/wptrunner/docs/expectation.html
- SLSA provides a vocabulary for provenance and attestations:
  https://slsa.dev/spec/latest/
- WCAG 2.2 should anchor public-site accessibility requirements:
  https://www.w3.org/TR/WCAG22/
- NIST AI RMF is a useful reference for trustworthiness and risk management:
  https://www.nist.gov/itl/ai-risk-management-framework

## Final Backlog Additions

Add the final blind-spot specs to `spec-backlog.md`. They should be written
before launch, but after the core leaderboard, scoring, ingestion, and artifact
explorer specs are stable.
