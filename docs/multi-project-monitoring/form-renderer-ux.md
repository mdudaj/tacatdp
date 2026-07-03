# Metadata-Driven Form Renderer UX

## Decision

The multi-project platform should not hard-code one Canvas screen per TACATDP section as the long-term app design. The fixed 33-screen TACATDP source can remain a transitional prototype, import recovery artifact, or generated project-specific projection, but the reusable platform should render forms from `InstrumentVersion`, `GroupDefinition`, `FieldDefinition`, `FieldRule`, vocabulary/reference bindings, and repeat metadata.

## Research basis

ODK/XLSForm separates the form definition from the form filling UI:

- XLSForm uses a `survey` worksheet to define form structure and question behavior, and a `choices` worksheet to define reusable choice lists. The XLSForm definition is converted to an ODK XForm that can run across mobile and web data collection tools. Reference: `https://xlsform.org/en/`.
- The `survey` rows include question type, variable name, label, hints, appearance, constraints, relevance, calculations, groups, and repeats. This means one renderer can present many different forms without manually building a screen per project. Reference: `https://xlsform.org/en/`.
- ODK form logic treats groups and repeats like nested paths. Questions are files; groups and repeats are folders; repeat instances are multiple occurrences of the same path. This supports metadata-driven grouping, nested repeats, calculations, and summaries. Reference: `https://docs.getodk.org/form-logic/#groups-and-repeats`.
- XPath predicates are used for repeat filtering and cascading select filters, which maps well to `FieldRule`, `choice_filter`, and indexed reference-data tables in Dataverse. Reference: `https://docs.getodk.org/form-logic/#groups-and-repeats`.
- XLSForm appearances such as `field-list` and page-style navigation influence how a renderer lays out questions without changing the source data model. Reference: `https://xlsform.org/en/#field-list`.

## Implication for TACATDP

The current 33-screen design is not wrong as a TACATDP-specific scaffold, but it is wrong as the reusable platform architecture. A multi-project platform needs a small set of generic screens/components:

| Surface | Purpose |
| --- | --- |
| Project/instrument picker | Select monitoring project, instrument, version, and optional event/encounter. |
| Form runner shell | Renders the current group/page from metadata and manages navigation, save state, validation, and progress. |
| Field renderer | Selects the correct control for each `FieldDefinition` data type and appearance. |
| Choice/reference provider | Loads small vocabularies from vocabulary terms and high-volume lookups from dedicated reference tables such as `mp_VillageReference`. |
| Repeat manager | Adds, edits, lists, and removes `GroupInstance` rows for repeatable groups. |
| Review/summary screen | Shows completion, required visible errors, repeat summaries, and submit/review actions. |

## Renderer requirements

1. Load a published `InstrumentVersion` and its ordered `GroupDefinition` tree.
2. Render only fields whose `relevance` evaluates true for the current submission context.
3. Validate required-visible fields, constraints, and field rules before navigating away from a group/page.
4. Support one-field-per-row as the default layout within a rendered page/group.
5. Support page/group layout metadata so some groups can render as one question per step and others as a `field-list` page.
6. Store scalar answers as `mp_AnswerValue`, multi-select choices as `mp_MultiSelectAnswer`, and repeat occurrences as `mp_GroupInstance`.
7. Treat high-volume references, such as villages, as delegated lookup providers rather than local collections or generic dropdowns.
8. Preserve stable field codes, labels, hints, required markers, helper text, inline errors, and accessible focus order.
9. Keep TACATDP-specific wide screens/tables as optional projections, not the source-of-truth UI model.

## Recommended next design slice

Before editing Canvas screens again, create a review-only renderer contract:

- `schemas/dataverse/form-renderer-contract.json`
- group/page layout metadata columns for `mp_GroupDefinition`
- field appearance/control metadata columns for `mp_FieldDefinition`
- rule-expression subset supported in Power Fx for the first implementation
- pilot renderer flow for one TACATDP section and one repeat group

No Power Platform environment writes should happen until this renderer contract is reviewed.

## Contract status

`schemas/dataverse/form-renderer-contract.json` now defines the first review-only renderer contract. It adds proposed metadata extensions for group render mode, navigation mode, field control kind, lookup provider type/source, choice filters, constraints, calculations, control mapping, and pilot flows for demographics and production-cost repeat entry.
