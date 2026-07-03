# Definition of Done: TACATDP Prototype Slice 1

The slice is done when:

1. TACATDP prototype context initializes with project, instrument, version, and submission key.
2. Demographics fields render with one-field-per-row layout, visible labels, helper text, inline errors, and validation summary.
3. Required-visible and constraint validation blocks invalid Continue/Save.
4. Region, district, ward, and village cascading lookup works with village backed by dedicated reference data shape.
5. One multi-select field saves one child row per selected value.
6. One production-cost repeat/line item can be added, edited, removed, saved, and summarized.
7. Save Draft persists all in-scope data to approved prototype storage and surfaces failures visibly.
8. Review summary displays completion, blockers, selected multi-select values, repeat lines, and totals.
9. Prototype shortcuts are documented and classified.
10. Relevant validation is run and recorded.

The slice is not done if it requires production writes, commits secrets, makes skip-eligible backend columns required, or claims full multi-project renderer support.
