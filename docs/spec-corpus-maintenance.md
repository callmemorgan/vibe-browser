# Spec Corpus Maintenance

The `specs/` directory contains upstream standards snapshots used as local
benchmark inputs. These files are reference material supplied to LLM agents, not
files we author directly.

## Rules

- Do not hand-edit upstream spec snapshots.
- Keep benchmark decisions in `docs/`, not inside `specs/`.
- Prefer canonical source URLs and revision metadata when adding or refreshing a
  spec.
- Update [Spec Inventory](spec-inventory.md) when a corpus change affects
  priority, category, or benchmark scope.
- Update [Standards Strategy](standards-strategy.md) when a spec moves between
  tiers.
- Avoid duplicate copies of the same spec unless there is a documented reason.
- Avoid changing the corpus during an active benchmark run.
- Record corpus changes that affect comparability across runs.

## Metadata to Capture

When adding or replacing a spec, capture as much of this as practical:

- Spec name.
- Local filename.
- Canonical URL.
- Source organization or standards body.
- Snapshot date.
- Revision, commit, generator metadata, or publication status.
- Reason for inclusion.
- Initial implementation tier.
- Benchmark impact, if the change affects task scope or scoring.

If the metadata is embedded in the generated HTML, do not rewrite the upstream
file. Record benchmark-facing metadata in `docs/spec-inventory.md` or a future
machine-readable manifest.

## Refresh Flow

1. Identify the canonical source and current snapshot.
2. Replace or add the local file under `specs/`.
3. Verify the file opens locally and is not an error page.
4. Update `docs/spec-inventory.md` if the changed spec is represented there.
5. Update `docs/standards-strategy.md` if priority or scope changed.
6. Rebuild `specs.zip` if the compressed archive remains part of the repo.
7. Review the diff for accidental formatting, minification, or duplicate corpus
   churn.
8. Record whether old and new benchmark runs remain comparable.

## Archive Policy

`specs.zip` mirrors the vendored corpus for portability. If the benchmark later
adopts a generated manifest or external fetch step, record that change in an ADR
before removing or replacing the archive.

Because the corpus is large, changes to `specs/` should be intentional and easy
to review. Prefer focused updates over broad refreshes unless the broad refresh
is the explicit purpose of the change.

Benchmark reports should identify the corpus revision used for a run. If two
runs use different corpus revisions, evaluators should avoid treating the scores
as strictly equivalent without reviewing the changed inputs.
