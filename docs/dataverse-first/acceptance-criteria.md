# Acceptance Criteria: Dataverse-First Pivot

1. Given the Dataverse environment is available, when the next backend implementation slice starts, then Dataverse is treated as the primary backend and Microsoft Lists as fallback.
2. Given the XLSForm inventory has 292 mapped inputs, when the Dataverse schema is generated, then every mapped field has a target Dataverse table/column or child-row representation.
3. Given a new submission is started, when data is saved, then one Submission parent row exists and section/child rows relate to it.
4. Given an external import/upsert needs stable identifiers, when Dataverse keys are defined, then `SubmissionKey` and reference codes are represented as alternate keys where appropriate.
5. Given a multi-select field is saved, when values are persisted, then each selected choice is stored as one `MultiSelectAnswer` row.
6. Given production cost detail is saved, when values are persisted, then each stage/item entry is stored as one `ProductionCostLine` row.
7. Given a large reference table such as villages is used in the app, when a maker writes filter formulas, then the formulas must be delegation-safe or the exception must be documented.
8. Given the app moves between environments, when solution export/import is planned, then environment-specific values are represented as environment variables or deployment settings rather than hard-coded values.
9. Given Microsoft Lists artifacts remain in the repo, when docs are read, then they clearly indicate Lists is fallback unless production later requires it.
10. Given no explicit production approval exists, when this artifact slice completes, then no Dataverse production write, app publish, permission change, or destructive operation has occurred.

