# Definition of Done: Phase 3 Validation and Save Map

## Artifact slice done

This documentation/protocol slice is done when:

1. PRD, requirements note, user stories, acceptance criteria, traceability, readiness, definition of done, and verification summary exist under `docs/phase-3-validation-save-map/`.
2. The artifacts cite repository evidence instead of relying only on chat history.
3. The artifacts record the delegated planning route: GitHub `gpt-5-mini`.
4. The artifacts record the next implementation route: `openai_codex` `gpt-5.4-mini` for routine implementation after readiness.
5. Karakana protocol trace `20260703-071158-1facb9` has all required artifacts attached.
6. The task handoff is refreshed and attached to the trace.

## Next implementation slice done

The later implementation slice is done only when:

1. Each of the 33 screens has visible-only required validation.
2. Invalid visible required fields show inline error text and appear in a validation summary.
3. Hidden/skipped fields do not block Continue, Save Draft, or Submit.
4. Placeholder Save Draft records are shaped for future Microsoft Lists and include `SubmissionKey`.
5. Save failure is visible and cannot be mistaken for success.
6. Multi-select answers are normalized into `TACATDP_MultiSelectAnswers`-shaped placeholder rows.
7. Production cost detail saves one `TACATDP_ProductionCostLines`-shaped placeholder row per line item.
8. ODK metadata fields remain absent from visible UI entry screens.
9. The app remains packable/importable using the documented native-control strategy.
10. App Checker, Monitor, and manual screen scenarios are run in the authorized Power Apps environment when available.

## Not done if

- Required artifacts exist only in chat and not in repository documentation or protocol attachments.
- Any production SharePoint write, permission change, app import/publish, or destructive list change occurs without explicit approval.
- The implementation reintroduces generated custom components that were associated with `ErrOpeningDocument_UnknownError`.
- The app silently swallows save errors or shows success after a failed save.

