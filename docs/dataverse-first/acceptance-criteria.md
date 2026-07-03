# Acceptance Criteria: Dataverse-First Pivot

1. Given the Dataverse environment is available, when the next backend implementation slice starts, then Dataverse is treated as the primary backend and Microsoft Lists as fallback.
2. Given the XLSForm inventory has 292 mapped inputs, when the Dataverse schema is generated, then every mapped field has a generic field definition and a scalar answer, multi-select answer, attachment, or controlled-vocabulary representation.
3. Given a new submission is started, when data is saved, then one Submission row exists and group instances/answer rows relate to the correct project, instrument version, entity, and encounter context.
4. Given an external import/upsert needs stable identifiers, when Dataverse keys are defined, then project codes, instrument/version codes, `SubmissionKey`, field codes, entity keys, and vocabulary term codes are represented as alternate keys where appropriate.
5. Given a multi-select field is saved, when values are persisted, then each selected choice is stored as one `MultiSelectAnswer` row linked to a field definition and vocabulary term.
6. Given production cost detail is saved, when values are persisted, then each stage/item entry is represented through repeat/group instances and answer rows, with optional line-item projections generated later if justified.
7. Given a large reference vocabulary such as villages is used in the app, when a maker writes filter formulas, then the formulas must be delegation-safe or the exception must be documented.
8. Given the app moves between environments, when solution export/import is planned, then environment-specific values are represented as environment variables or deployment settings rather than hard-coded values.
9. Given Microsoft Lists or older TACATDP-specific table artifacts remain in the repo, when docs are read, then they clearly indicate those artifacts are fallback/source-decomposition evidence or projections, not the core source-of-truth model.
10. Given no explicit production approval exists, when this artifact slice completes, then no Dataverse production write, app publish, permission change, or destructive operation has occurred.
