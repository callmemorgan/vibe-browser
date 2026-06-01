# API Contract

## Purpose

The API contract defines how the leaderboard frontend, evaluator tools, admin
screens, exports, and external integrations read and write benchmark data.

## API Style

Use HTTP JSON APIs described by OpenAPI. Public read endpoints should be stable,
cacheable, and documented. Mutating evaluator/admin endpoints require
authentication, authorization, idempotency keys where relevant, and audit logs.

## Core Resources

- `GET /seasons`
- `GET /leaderboards`
- `GET /runs`
- `GET /runs/{run_id}`
- `GET /runs/{run_id}/result-card`
- `GET /runs/{run_id}/timeline`
- `GET /runs/{run_id}/evidence`
- `GET /runs/{run_id}/artifacts`
- `GET /models`
- `GET /fixtures`
- `POST /imports`
- `POST /runs/{run_id}/evaluations`
- `POST /runs/{run_id}/certification-gates`
- `POST /runs/{run_id}/admin-actions`
- `GET /exports/{season_id}`

## Response Rules

List endpoints use cursor pagination and deterministic sorting. Every response
includes schema version, request ID, generated timestamp, and permissions-aware
redaction status. Error responses include machine-readable code, safe message,
correlation ID, and remediation hint where useful.

## Versioning

Breaking response changes require a new API major version or season-specific
export schema. Additive fields are allowed when clients can ignore unknown
fields. Published data exports remain immutable.

## Research Basis

OpenAPI provides a formal standard for describing HTTP APIs and generating
clients, tests, and design checks. JSON Schema anchors validation of structured
payloads.

## QA Pass

Checked against `ingestion-pipeline.md`, `result-card.md`,
`evidence-model.md`, `access-control.md`, `admin-operations.md`, and
`public-data-export` backlog expectations. This spec defines API surface, not
database schema.
