# Requirements Traceability: Multi-Project Monitoring Model

| Requirement | Evidence | Design surface | Verification |
| --- | --- | --- | --- |
| MP-RQ-01 Multiple projects | ODK Project pattern | `mp_Project` | Schema review |
| MP-RQ-02 Instruments and versions | ODK Form drafts/versions, CDISC FormDef | `mp_Instrument`, `mp_InstrumentVersion` | Metadata import test |
| MP-RQ-03 Groups and fields | CDISC ItemGroup/Item | `mp_GroupDefinition`, `mp_FieldDefinition` | TACATDP coverage check |
| MP-RQ-04 Repeating groups | ODK repeats, CDISC repeating ItemGroup | `mp_GroupInstance` | Repeat scenario test |
| MP-RQ-05 Field rules | XLSForm logic, current TACATDP mapping | `mp_FieldRule` | Rule inventory coverage |
| MP-RQ-06 Multi-select rows | ODK/REDCap export caveats, analytics need | `mp_MultiSelectAnswer` | Multi-select save test |
| MP-RQ-07 Runtime separation | ODK submissions, CDISC clinical data | `mp_Submission`, `mp_GroupInstance`, `mp_AnswerValue` | Submission shape review |
| MP-RQ-08 Entities/encounters | ODK Entities, OpenClinica events | `mp_TrackedEntity`, `mp_Encounter` | Longitudinal scenario |
| MP-RQ-09 Controlled vocabularies | InvenioRDM vocabularies | `mp_VocabularyScheme`, `mp_VocabularyTerm` | Vocabulary import test |
| MP-RQ-10 Term metadata | Invenio labels/schemes/external IDs | labels, relations, external IDs | Vocabulary governance review |
| MP-RQ-12 Projections | REDCap/ODK exports | export profiles/views | Wide export fixture |
| MP-RQ-13 TACATDP as project | Current TACATDP artifacts | TACATDP metadata migration | 292-field coverage |

