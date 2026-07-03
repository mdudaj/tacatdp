# Acceptance Criteria: Multi-Project Monitoring Model

1. Given a new monitoring project is added, when the platform is configured, then no TACATDP-specific core table must be required.
2. Given a project has multiple forms, when metadata is stored, then each form has instrument and version records.
3. Given a form has repeating groups, when data is submitted, then each repeat occurrence is a `GroupInstance` with repeat identity.
4. Given a form has nested repeats, when data is submitted, then child repeat instances link to parent group instances.
5. Given a field is `select_multiple`, when values are saved, then each selected term is a `MultiSelectAnswer` row.
6. Given a project has longitudinal follow-up, when a new visit occurs, then submissions can link to a long-lived tracked entity and encounter.
7. Given a field uses a controlled vocabulary, when a value is selected, then the stored answer references a vocabulary term and can export code and label.
8. Given a vocabulary term is renamed, when historical submissions are exported, then previous submissions remain traceable to the original term/code and label snapshot.
9. Given TACATDP is migrated into the platform model, when mapping coverage is checked, then all 292 mapped XLSForm fields have matching field definitions or normalized child-row definitions.
10. Given analytics requires wide data, when export runs, then the platform can generate project-specific projections from normalized runtime data.

