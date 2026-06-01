# Model and Tool Identity

## Purpose

Model and tool identity fields prevent ambiguous claims such as "GLM did X" or
"Codex scored Y" when provider aliases, agent versions, and tool surfaces may
have changed.

## Model Identity

Record:

- provider name
- provider endpoint class, such as first-party API, Ollama cloud, local Ollama,
  proxy, or self-hosted inference
- model display name
- provider model identifier
- model version, build, or snapshot date when available
- alias mutability: fixed, dated, rolling, unknown
- inference parameters visible to the harness
- context window, if known
- provider incident notes during the run window

If a model is only known through a mutable alias, label the result with
`unknown-model-snapshot` unless provider metadata proves a stable version.

## Agent and Harness Identity

Record:

- agent tool name and package version
- harness name and version
- prompt set checksum
- tool capability manifest hash
- Docker image digest
- runtime profile
- CLI command used to launch the run
- repository baseline commit

## Display Rules

Public pages should show a friendly name plus the exact metadata behind it.
Filters may group aliases into model families, but ranked result cards must keep
the original observed identity.

## Alias Corrections

Corrections append alias records rather than rewriting historical names. If two
aliases are merged, preserve old URLs and show the merge reason.

## Research Basis

HELM's transparency goal and MLCommons' fair-comparison framing both require
declaring the evaluated system clearly enough that readers can understand what
changed between runs.

## QA Pass

Checked against comparison eligibility, result cards, provider drift tracking,
and final blind-spot entries for tool capability manifests and external state.
This spec stores identity; it does not decide whether drift occurred.
