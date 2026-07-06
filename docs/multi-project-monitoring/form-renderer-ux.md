# Metadata-Driven Form Renderer UX

## MVP decision

The Canvas App should be a runtime engine that renders Dataverse metadata. The July 7 MVP must prove this with one assigned published form, not with generated fixed screens.

Canonical MVP scope: `docs/mvp-july-7.md`.

## MVP renderer surfaces

| Surface | Purpose |
| --- | --- |
| Assigned forms | Show active published forms assigned to the signed-in user. |
| Submission history | Show the user's own submissions for the selected form. |
| Form runner shell | Load sections/questions from metadata, manage progress, validation, save state, submit, and locked read-only state. |
| Field renderer | Render supported MVP field types from question metadata. |
| Attachment capture | Attach one photo/file to a submission/question. |

## MVP supported controls

Support only:

- text;
- integer;
- decimal;
- date;
- select one;
- select many;
- file/photo attachment;
- GPS point if quick enough.

Defer repeat groups, barcode, advanced calculations, complex XPath, and offline-first sync.

## MVP validation behavior

Support only:

- required true/false;
- relevance depending on one prior answer;
- simple numeric/text comparisons.

Show visible inline errors and a validation summary. Requiredness applies only to visible/relevant fields.

## MVP layout rules

- One field per row by default.
- Visible label above each input.
- Helper/error text below each input.
- Clear Save Draft and Submit actions.
- Status is visible: Draft, Submitted, Locked.
- Locked submissions are read-only.
- History is scannable by status and timestamp.

## Long-term renderer direction

After the MVP proves the runtime, expand toward richer ODK Collect-style behavior:

- repeat manager;
- nested repeats;
- advanced relevance/constraint/calculation expressions;
- barcode;
- offline and sync conflict behavior;
- richer media/GPS behavior;
- admin-managed publishing/versioning.

The current 33 TACATDP screens remain reference/prototype artifacts, not the platform default.
