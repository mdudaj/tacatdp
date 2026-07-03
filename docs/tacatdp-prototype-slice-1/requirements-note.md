# Requirements Note: TACATDP Prototype Slice 1

## Purpose

Define the first bounded implementation slice for the TACATDP single-project prototype. This slice should prove one end-to-end data-entry path without attempting the full reusable Project platform or generic metadata-driven renderer.

## Scope

Slice 1 covers:

1. Demographics section flow.
2. Region -> district -> ward -> village cascading lookup.
3. One multi-select pattern from agricultural production.
4. One production-cost repeat/line-item pattern.
5. Save draft behavior.
6. Required-visible validation and inline/summary errors.
7. Review summary for the fields and repeat rows in scope.

## Out of scope

- Full multi-project platform implementation.
- Full metadata-driven form renderer.
- Dataverse environment creation/import unless explicitly approved later.
- App publish/import to production.
- Complete 33-screen TACATDP implementation.
- Complete XLSForm expression engine.
- Offline sync and conflict resolution.

## Prototype guardrails

- Use **Project** as the general concept; TACATDP is the only project implemented in this prototype.
- Fixed or generated TACATDP screens are acceptable for the prototype, but they must remain documented as prototype-specific.
- Keep seams compatible with the future renderer: project, instrument, version, group, field, repeat, submission, answer, vocabulary, and reference concepts should remain visible in naming or mapping.
- Keep requiredness app-visible/relevance-aware; do not make skip-eligible backend columns required.
- Use delegated reference filtering for villages through the dedicated village reference artifact.
- Record prototype shortcuts before implementation is considered done.
