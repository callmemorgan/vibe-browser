# Independent Replication

## Purpose

Independent replication defines how outside groups can rerun seasons, verify
public claims, and report replication results without becoming the canonical
source of truth.

## Replication Packet

Provide benchmark commit, public data export, runner instructions, container
digests, fixture checksums, prompt and harness versions, baseline artifacts,
public checker commands, evaluator rubric packet, and known nondeterminism.

## Replication Outcomes

- `replicated`: independent result matches expected public-check and score
  envelope.
- `partially-replicated`: key artifacts replay but some nondeterminism remains.
- `not-replicated`: material mismatch or missing dependency blocks replay.
- `inconclusive`: environment or provider drift prevents interpretation.

## Reporting

Replication reports include operator, environment, date, commands, checksums,
differences, logs, and contact. Maintainers may link accepted replication
reports from public seasons.

## Boundaries

Independent groups should not receive hidden tests unless a separate governance
decision creates a trusted replication program.

## Research Basis

ACM artifact badging motivates explicit artifact availability and repeatability
claims. FAIR principles motivate reusable, documented, and findable research
data.

## QA Pass

Checked against `reproducibility-contract.md`, `public-data-export.md`,
`trusted-execution-environment.md`, `citation-and-doi-policy.md`, and
`hidden-test-policy.md`. This spec defines external replication, not official
certification.
