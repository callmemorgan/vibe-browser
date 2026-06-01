# Scoring and Ranking

## Ranking Modes

### Comparable Batch Ranking

Default ranking. Only includes runs with matching:

- benchmark commit
- benchmark input digest
- prompt set and checksum
- profile
- target or target mode
- human intervention policy

Sort by:

1. Highest evaluator-confirmed milestone
2. Weighted rubric score
3. Highest public-check milestone
4. Verification status
5. Lower elapsed time, if all above tie

### Open-Ended Ranking

Used for "get as far as you can" runs. Sort by:

1. Highest evaluator-confirmed milestone
2. Progress within next milestone
3. Weighted rubric score
4. Scope honesty score
5. Lower budget usage, if all above tie

Open-ended ranks must not be mixed with targeted milestone ranks.

### Public-Check Preview

Used before evaluator scoring exists. This is explicitly provisional and should
not be displayed as the official leaderboard rank.

Sort by:

1. Highest public-check milestone
2. Latest verification result
3. Highest claimed milestone
4. Material progress count

## Rubric

Use the repository rubric:

- Runnable artifact: 15%
- Browser capability: 20%
- Standards traceability: 15%
- Test quality: 15%
- Architecture quality: 10%
- Security posture: 10%
- Privacy posture: 5%
- Scope honesty: 10%

Each rubric score must have evaluator notes and evidence links. The UI should
show both raw category scores and weighted total.

## Eligibility Rules

Exclude from ranked comparable tables when:

- Human intervention policy is `guided`.
- Benchmark commit or input digest differs from the batch.
- Prompt set or prompt checksum differs.
- Target or profile differs.
- Specs were modified during the run.
- Required artifacts are missing.
- The run was marked invalid by the harness or evaluator.

Still display excluded runs in an "All Runs" view with the exclusion reason.

## Milestone Status Vocabulary

- `not_started`: no evidence.
- `partial`: implementation evidence exists but criteria are incomplete.
- `candidate`: public checks pass but evaluator has not confirmed.
- `confirmed`: evaluator accepted the milestone.
- `failed`: evidence contradicts the milestone claim.

## Anti-Gaming Rules

- Hidden evaluator tests must not be exposed through public-check results.
- Public checks can report missing evidence, not prescribe implementation.
- Self-reported claims never outrank evaluator-confirmed evidence.
- Runs that hard-code public fixtures should be marked non-comparable or scored
  down under scope honesty and test quality.
