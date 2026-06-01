# Official Result Certification

## Purpose

Certification is the workflow that turns a run into an official result. It
separates "the harness produced artifacts" from "the benchmark stands behind
this public score."

## Certification Gates

1. **Completeness**: required snapshot files, summary, metrics, diff, version
   info, verification outputs, and evidence objects are present.
2. **Eligibility**: comparison rules produce `ranked` or an explicit official
   unranked label.
3. **Clean-room replay**: public verification commands run from the snapshot in
   an approved runtime profile, or replay limitations are documented.
4. **Redaction**: artifacts pass secret, private metadata, hidden-test, and
   unsafe-file checks.
5. **Evaluator signoff**: required evaluator count and adjudication rules are
   satisfied.
6. **Provenance**: checksums, image digests, benchmark commit, and certification
   timestamp are recorded.
7. **Publication review**: result card, run page, data export, and leaderboard
   placement are checked for consistency.

## Certification Outcomes

- `official-ranked`: appears in the official ranked table.
- `official-unranked`: public and certified, but excluded from ranking.
- `provisional`: visible to allowed users, awaiting a gate.
- `rejected`: cannot become official without a new run.
- `security-hold`: blocked from publication pending review.

## Audit Trail

Every gate records actor, timestamp, evidence links, and decision note.
Corrections require a new certification revision. Historical public results must
remain understandable after reanalysis.

## Research Basis

The workflow follows ACM's separation between artifacts evaluated and results
validated, and uses SLSA-style provenance concepts for checksums, image digests,
and attestable build/run facts.

## QA Pass

Checked against result cards, submission snapshots, verification schema,
comparison eligibility, and the final gap analysis. This spec is intentionally
stricter than local smoke-run sharing.
