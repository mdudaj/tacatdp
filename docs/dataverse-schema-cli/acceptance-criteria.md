# Acceptance Criteria: Dataverse Schema CLI Delivery

## AC-01 Preflight passes for example configuration

Given `.env.example`, when preflight runs with placeholder allowance, then required keys and MVP schema artifacts are validated without requiring real secrets.

## AC-02 Preflight passes for local dev configuration

Given `.env` with dev target values, when preflight runs, then it reports no missing required values and does not print secret values.

## AC-03 Operation plan is MVP-only

Given `mvp-schema-definition.json`, `schema-definition.md`, `mvp-tables.json`, and `mvp-columns.csv`, when the plan command runs, then it lists only the ten MVP tables, columns, and lookup relationships.

## AC-04 Write command is gated

Given environment writes are not explicitly enabled, when a deployment command is requested, then it refuses to write and points to the dry-run plan.

## AC-05 Approved dev write path is explicit

Given explicit approval and dev-only flags, when schema creation is implemented, then each metadata request includes the target solution unique name and environment URL.

## AC-06 Seed data is limited

Given schema creation succeeds, when seed data is prepared, then it includes only one form/version, a small set of sections/questions/choices/rules, and one assignment.
