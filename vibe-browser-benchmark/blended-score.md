# Blended Score

## Purpose

The blended score turns milestone progress and engineering quality into one
leaderboard number while preserving drill-down evidence. It must reward reaching
later browser milestones more than endlessly polishing early prototypes.

## Recommended Formula

Use a quadratic milestone value curve:

```text
milestone_value(Mn) = (n + 1)^2
```

For `M0` through `M9`, values are:

| Milestone | Value |
| --- | ---: |
| M0 | 1 |
| M1 | 4 |
| M2 | 9 |
| M3 | 16 |
| M4 | 25 |
| M5 | 36 |
| M6 | 49 |
| M7 | 64 |
| M8 | 81 |
| M9 | 100 |

Quadratic weighting is intentionally superlinear but not explosive. It makes
`M5` much more valuable than `M2`, while still giving early foundations enough
weight to matter.

## Score Components

For each milestone:

```text
milestone_points = milestone_value * milestone_rubric_score
```

Overall normalized score:

```text
blended_score = 100 * sum(milestone_points) / sum(all_milestone_values)
```

With `M0` through `M9`, the denominator is `385`.

## Quality Modifier

Apply the repository-wide rubric as a multiplier, not as separate additive
points:

```text
final_score = blended_score * (0.70 + 0.30 * repository_rubric_score)
```

Where `repository_rubric_score` is normalized from `0.0` to `1.0`.

This means milestone progress drives rank, but poor test quality, weak security,
or dishonest scope claims can reduce the final score by up to 30%.

## Public vs Evaluator Scores

Store three blended scores:

- `claimed_score`: based on self-reported milestone status.
- `public_check_score`: based on deterministic public checks.
- `evaluator_score`: official leaderboard score.

Only `evaluator_score` should determine official rank. Public-check scores can
power previews and debugging views.

## Partial Milestones

A partial milestone should contribute fractional value through its milestone
rubric score. Example:

```text
M0 = 1.00
M1 = 1.00
M2 = 0.80
M3 = 0.35
M4+ = 0.00
```

This rewards meaningful progress into the next milestone without pretending the
milestone is complete.

## Alternative Curves

Keep the curve configurable by batch:

- Linear: `n + 1`; useful for debugging small harness runs.
- Quadratic: `(n + 1)^2`; recommended default.
- Cubic: `(n + 1)^3`; use only if the benchmark wants to heavily reward deep
  compatibility over early robustness.

Do not mix runs scored with different curves in the same official leaderboard.
