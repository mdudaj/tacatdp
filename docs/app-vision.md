# App Vision and TACATDP Prototype Strategy

## Decision

The long-term vision is a reusable project platform, not only a monitoring-project app. The platform may eventually support monitoring, evaluation, field operations, case workflows, inspections, audits, research instruments, and other structured data-collection projects.

The near-term implementation should not attempt the full multi-project platform. TACATDP should be implemented first as a single-project prototype that validates the core data-entry, validation, reference-data, repeat, save, review, and export patterns.

## Why prototype first

Multi-project support is a significant product and engineering effort. It requires deeper research and decisions across:

- project lifecycle and governance;
- instrument authoring and versioning;
- form renderer architecture for web and Power Apps mobile;
- offline and sync behavior;
- expression/rule evaluation;
- repeat group UX;
- controlled vocabularies and high-volume reference lookup;
- security and project-scoped permissions;
- export/projection/codebook generation;
- migration from a project-specific prototype into reusable platform services.

Trying to implement all of this before proving TACATDP would slow delivery and increase risk. A single-project TACATDP prototype gives us a concrete app to validate the patterns while preserving the larger architecture vision.

## Terminology

Use **Project** as the general top-level concept. Avoid locking future documents to **MonitoringProject** unless the context is specifically monitoring and evaluation.

TACATDP is the first configured project/prototype.

## Prototype boundary

The TACATDP prototype may use project-specific shortcuts when they accelerate learning, provided they do not contradict the future platform direction:

1. Dataverse remains the preferred backend.
2. TACATDP may use project-specific screens or generated screens for the prototype.
3. Runtime data should still preserve the normalized answer/repeat principles where practical.
4. High-volume references such as villages should use delegated reference tables.
5. Requiredness must remain visible/relevance-aware rather than unsafe backend-required columns.
6. Project-specific tables, screens, and exports are prototypes/projections, not the final platform contract.

## Vision boundary

The multi-project form renderer remains the app vision and research track:

- forms load from project/instrument metadata, similar to how ODK Collect loads a form definition;
- a published instrument version defines groups, fields, rules, choices, references, and repeats;
- generic renderers can target Power Apps web/mobile first and possibly a custom web renderer later;
- submissions store answers in normalized runtime structures.

This vision should guide naming and schema choices, but it should not block the TACATDP prototype.

## Next implementation direction

1. Implement a TACATDP prototype slice for one project.
2. Use the renderer contract and multi-project artifacts as guardrails, not blockers.
3. Validate one normal section, one high-volume village lookup cascade, one multi-select pattern, and one repeat/line-item pattern.
4. Record every project-specific shortcut as either acceptable prototype debt or a blocker for platform generalization.
5. Resume broader multi-project research after the TACATDP prototype proves the first end-to-end flow.

The first bounded slice is specified in `docs/tacatdp-prototype-slice-1/`.
