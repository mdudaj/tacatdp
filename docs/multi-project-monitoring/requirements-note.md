# Multi-Project Monitoring Requirements Note

## Bounded outcome

Define requirements for a Dataverse-first monitoring platform data model that can support TACATDP and future monitoring projects.

This is requirements and architecture planning only. It must not create Dataverse tables, import data, publish apps, or alter environments.

## Problem

The current Dataverse-first plan is still mostly TACATDP-shaped. If future monitoring projects have different forms, repeats, events, entities, choices, and workflows, a project-specific schema will create repeated redesign work and brittle migrations.

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| MP-RQ-01 | The platform must support multiple monitoring projects as first-class records. | P0 |
| MP-RQ-02 | Each project must support multiple instruments/forms and versions. | P0 |
| MP-RQ-03 | Instruments must be composed of sections/groups and fields. | P0 |
| MP-RQ-04 | Groups must support repeatability, nested repeat context, repeat index, and parent repeat instance links. | P0 |
| MP-RQ-05 | Fields must support data types, required rules, relevance rules, constraints, calculations, labels, hints, and display order. | P0 |
| MP-RQ-06 | Multi-select responses must be stored as one row per selected term. | P0 |
| MP-RQ-07 | The runtime model must separate submission headers, group instances, and answer values. | P0 |
| MP-RQ-08 | The model must support long-lived entities/cases and repeated encounters/follow-ups. | P0 |
| MP-RQ-09 | Controlled vocabularies must be reusable across projects and field definitions. | P0 |
| MP-RQ-10 | Controlled vocabulary terms must support stable codes, labels, synonyms, external authority IDs, hierarchy, status, and versioning. | P0 |
| MP-RQ-11 | Project-specific vocabulary subsets must be possible without duplicating global terms. | P1 |
| MP-RQ-12 | Export/reporting shapes may be project-specific projections, but normalized runtime data is source of truth. | P0 |
| MP-RQ-13 | TACATDP must be represented as a project configuration on the platform model. | P0 |
| MP-RQ-14 | Existing TACATDP field mapping must remain traceable to the generic definitions. | P0 |

## Non-goals

- Building a full dynamic form renderer in this slice.
- Creating Dataverse tables in this slice.
- Replacing Canvas screens in this slice.
- Deleting existing TACATDP or Microsoft Lists artifacts.

## Design stance

Use a metadata-driven core model, not one fixed Dataverse table per project section as the long-term source of truth. Project-specific typed/wide tables may still be generated later for analytics or performance, but they should be treated as projections.

