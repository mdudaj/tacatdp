# Multi-Project Monitoring Platform Research

## Purpose

Research ODK Central, OpenClinica/CDISC ODM, REDCap, and InvenioRDM patterns to avoid building a TACATDP-only data model that cannot support future monitoring projects, repeating groups, multiple-select questions, longitudinal follow-up, and controlled vocabularies.

## ODK Central patterns

ODK Central organizes work around Projects, Forms, Submissions, and Entities.

Relevant patterns:

- Project is the top-level boundary for users, permissions, forms, and entity lists.
- A Project can contain many Forms.
- Forms have draft/publish lifecycle and version updates.
- Submissions are filled form instances and can be reviewed, commented on, edited, exported, or accessed through OData.
- Entities are long-lived records for registration/follow-up workflows and live inside Projects.
- Entities can be created/updated by submissions and referenced by later forms.
- Entity lists support longitudinal workflows and reduce manual CSV attachment workflows.
- Repeat groups are arrays of repeated answer groups inside a submission; ODK repeat formulas use repeat names and instance positions.
- ODK `select_multiple` is raw-stored as selected values and often exported as one column per choice, but analytics-friendly platforms should normalize these selections.

Implication for our platform:

- Use Project as an explicit first-class boundary.
- Separate Form/Instrument definitions from Submissions.
- Support Form versions and draft/published states.
- Add a long-lived Entity/Subject/Case layer for registration and follow-up.
- Store repeating groups as repeat instances, not as fixed columns.
- Store multi-select answers as child rows, not delimited text.

Primary references:

- `https://docs.getodk.org/central-intro/`
- `https://docs.getodk.org/central-projects/`
- `https://docs.getodk.org/central-forms/`
- `https://docs.getodk.org/central-submissions/`
- `https://docs.getodk.org/central-entities/`
- `https://docs.getodk.org/form-repeats/`
- `https://docs.getodk.org/form-question-types/`

## OpenClinica / CDISC ODM patterns

OpenClinica and CDISC ODM use a clinical-study hierarchy:

```text
Study
  StudyEvent
    Form
      ItemGroup
        Item
```

Relevant patterns:

- Study is the top-level protocol/project.
- Study Events represent visits, time points, or collection occasions.
- Forms are assigned to events.
- Item Groups organize fields and can repeat.
- Items are individual variables/questions.
- CodeLists define allowed values for coded items.
- Instance data preserves event/form/group/item identity and repeat keys.

Implication for our platform:

- Add explicit Event/Encounter concepts, even if TACATDP initially uses one survey encounter.
- Define Instrument, Section/Group, and Field metadata separately from collected values.
- Make repeatability a property of group definitions.
- Store group instance repeat index / occurrence key.
- Use controlled vocabularies/code lists for enumerated fields.

References:

- `https://www.cdisc.org/standards/data-exchange/odm`
- `https://docs.openclinica.com/`
- `https://docs.openclinica.com/3-1-technical-documents/openclinica-and-cdisc-odm-specifications/openclinica-and-cdisc-odm-specifications-cdisc-odm-representation-openclin-5/`

## REDCap patterns

REDCap is useful for understanding project-level instruments, longitudinal events, and repeating instances:

- Project is the top-level unit.
- Instruments/forms are metadata-defined.
- Longitudinal projects use arms and events.
- Repeating instruments/events add repeat instrument and repeat instance identifiers.
- Checkbox/multi-select exports often create one column per choice, but that is an export shape rather than a normalized source-of-truth model.

Implication for our platform:

- Keep event/repeat identity explicit in collected data.
- Do not confuse export shape with storage shape.
- Support project-specific exports/projections from a normalized source model.

## InvenioRDM controlled vocabulary patterns

InvenioRDM uses controlled vocabularies for resource types, subjects, affiliations, names, languages, licenses, and relation types. Relevant patterns:

- Vocabularies have stable identifiers, schemes, labels, and optional external authority IDs.
- Vocabularies can be loaded from YAML/data fixtures and customized by an institution.
- Subjects can be organized by scheme, such as OECD, MeSH, FAST, or local taxonomies.
- Affiliations can map to external registries such as ROR.
- Resource types map local values to external standards such as DataCite or Schema.org.

Implication for our platform:

- Build a controlled vocabulary feature instead of hard-coded choice lists.
- Represent vocabulary schemes and terms with stable IDs, labels, synonyms, external identifiers, status, and versions.
- Allow project-specific term subsets and field bindings.
- Allow import/export from CSV/YAML/JSON and later external authority synchronization.

References:

- `https://inveniordm.docs.cern.ch/use/operate/vocabularies/`
- `https://invenio-vocabularies.readthedocs.io/`

## Architecture conclusion

The robust path is a reusable monitoring platform model:

1. **Control plane metadata**: projects, instruments, versions, events, groups, fields, constraints, relevance rules, and controlled vocabulary bindings.
2. **Runtime data**: entities/cases, encounters/events, submissions, group instances, answers, multi-select answer rows, attachments, reviews, and audit events.
3. **Controlled vocabulary service**: schemes, terms, labels, aliases, hierarchy, external IDs, project bindings, field bindings, versioning, and import/export.
4. **Project-specific projections**: optional wide exports or Dataverse views/tables for analytics, generated from normalized source data.

TACATDP should become the first configured monitoring project on this platform, not the hard-coded platform schema.

