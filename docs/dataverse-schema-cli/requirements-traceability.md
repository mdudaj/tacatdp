# Requirements Traceability: Dataverse Schema CLI Delivery

| Requirement | Story | Acceptance criteria | Artifact / implementation |
| --- | --- | --- | --- |
| DVCLI-RQ-01 | DVCLI-US-01 | AC-01, AC-02 | `scripts/dataverse-deploy-preflight.py` |
| DVCLI-RQ-02 | DVCLI-US-01 | AC-02 | `.env.example`, preflight output |
| DVCLI-RQ-03 | DVCLI-US-02 | AC-03 | `schemas/dataverse/mvp-tables.json` |
| DVCLI-RQ-04 | DVCLI-US-02 | AC-03 | `schemas/dataverse/mvp-schema-definition.json`, `docs/dataverse-schema-cli/schema-definition.md`, `schemas/dataverse/mvp-columns.csv` |
| DVCLI-RQ-05 | DVCLI-US-02 | AC-03 | `scripts/dataverse-schema-plan.py` |
| DVCLI-RQ-06 | DVCLI-US-03 | AC-05 | PAC auth/solution commands |
| DVCLI-RQ-07 | DVCLI-US-03 | AC-05 | Dataverse Web API metadata operations |
| DVCLI-RQ-08 | DVCLI-US-03 | AC-05 | `MSCRM.SolutionUniqueName` header |
| DVCLI-RQ-09 | DVCLI-US-04 | AC-06 | seed data checklist |
| DVCLI-RQ-10 | DVCLI-US-01, DVCLI-US-03 | AC-04 | safety gates |
