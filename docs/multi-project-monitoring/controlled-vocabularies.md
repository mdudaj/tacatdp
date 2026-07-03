# Controlled Vocabularies Feature

## Goal

Implement an InvenioRDM-inspired controlled vocabulary feature for monitoring projects. This replaces ad-hoc choice lists and makes controlled variables reusable across projects.

## Core concepts

| Concept | Meaning |
| --- | --- |
| Vocabulary scheme | A named vocabulary namespace, such as crop, village, organization, intervention type, or resource type. |
| Term | One controlled value inside a scheme. |
| Label | Human-readable term text, with language and label type. |
| External identifier | Link to an external authority such as ROR or a government code. |
| Term relation | Parent/child, broader/narrower, exact match, replacement, or deprecation relation. |
| Project binding | Which terms from a scheme are allowed in a project. |
| Field binding | Which scheme/terms a field may use. |

## Required behavior

1. Terms must have stable codes independent of display labels.
2. Labels must support language codes and alternate labels.
3. Terms must support active, deprecated, draft, and retired statuses.
4. Terms may have parent/child hierarchy.
5. Terms may map to external authorities.
6. Project managers may bind a scheme or subset of terms to a project.
7. Field definitions may bind to one scheme and specify single or multiple selection.
8. Data collection stores selected term references, not only copied labels.
9. Exports may include both term code and label snapshot.

## Import formats

Support CSV first, later YAML/JSON:

```csv
scheme_code,term_code,preferred_label_en,preferred_label_sw,parent_term_code,sort_order,status,external_authority,external_id
crop,maize,Maize,Mahindi,,10,active,,
```

## Governance rules

- Do not delete terms that have been used in submitted data.
- Deprecate and replace terms instead.
- Track vocabulary version used by an instrument version.
- Allow project-specific term subsets.
- Keep imported TACATDP XLSForm choice values traceable to original `list_name` and `name`.

## TACATDP first vocabularies

- Regions
- Districts
- Wards
- Villages
- CRDB branches
- Gender
- Education level
- Crop
- Technology
- Cost item
- Unit
- Safeguards/climate choices
- Insurance/guarantee choices

