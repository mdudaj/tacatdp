# Power Pages File Handling Research

Date: 2026-07-11

## Purpose

Define how TACATDP should handle files in the Power Pages hosted Monitoring Tool without leaving the managed Microsoft boundary.

## Evidence

Microsoft Power Pages basic forms support an **Attach File** option that renders a file upload control at the bottom of a Dataverse-backed basic form. Microsoft documents two storage locations for that built-in control: note attachments and Azure Blob Storage. When table permissions are enabled, the parent table and annotation table need matching privileges: annotation needs at least Create and Append, and the parent table needs Append To.

Microsoft also documents Power Pages file-column support through basic forms and the portals Web API. The important limitation for built-in basic forms is that a file can't be uploaded in Insert mode; a record must already exist for file-column upload behavior.

For custom browser code, Microsoft documents `PUT` or `PATCH /_api/<entity-type>(id)/<file-attribute-name>` with `Content-Type: application/octet-stream` for Power Pages file columns. Dataverse's raw Web API documentation separately documents single-request file-column upload for files under 128 MB with `PATCH <record>/<filecolumn>`, `Content-Type: application/octet-stream`, and `x-ms-file-name`.

Microsoft documents the Power Pages portals Web API as a Dataverse CRUD subset governed by Power Pages table permissions and web roles. It also documents that Dataverse actions and functions are unsupported through the portals Web API. Therefore, chunked upload messages are not an acceptable browser-only Power Pages assumption.

## Live TACATDP Result

The hosted Monitoring Tool proved these facts:

- ODK Web Forms can emit a ready submit payload with a file value.
- Power Pages `/_api` can create `mp_submissions`, `mp_submissionversions`, and `mp_submissionattachments` metadata rows.
- Direct browser binary upload to the Dataverse file column failed on the hosted origin with `400`, Dataverse code `0x80048d19`.
- Dataverse verification showed the attachment row existed but `mp_file_name` remained null.

## Decision

For the shareable MVP, treat file support as **metadata proven, binary storage pending**.

The next binary persistence slice must be one of these Microsoft-managed options:

1. **Retest file-column upload exactly against Microsoft Power Pages file-column syntax**: `PUT /_api/mp_submissionattachments(<id>)/mp_file`, `Content-Type: application/octet-stream`, binary body, and the minimum required headers. Compare with `PATCH` and document exact browser result.
2. **Use a server-side Microsoft-managed mediator** such as Power Automate or a Dataverse plugin/custom API to accept metadata plus a safe file transfer pattern and write the file column or note attachment server-side. Do not expose Dataverse OAuth credentials in the SPA.
3. **Use a built-in Power Pages basic form upload surface** only if the UX can tolerate a separate post-record upload step. This is less aligned with ODK Web Forms because the built-in upload appears at the bottom of a Dataverse form, not inside the ODK runtime.
4. **Use Azure Blob Storage through Power Pages built-in attachment configuration** only if the client explicitly approves Azure Blob as part of the Microsoft-managed services boundary.

## Implementation Instructions

Before changing file upload code:

1. Inspect this document, `attachment-persistence-slice.md`, `powerpages/webforms-spa/src/powerpages-api/client.ts`, and the current `mp_submissionattachments` schema.
2. Recheck Microsoft Learn for Power Pages basic forms, Power Pages file columns, Power Pages portals Web API, and Dataverse file-column data.
3. Keep all browser writes on `/_api`; do not add raw Dataverse access tokens, client secrets, or external upload endpoints.
4. Keep attachment metadata creation separate from binary persistence.
5. Display binary upload count and warning state until hosted browser verification proves nonzero binary upload success and Dataverse file content is readable.

## References

- Power Pages basic forms: https://learn.microsoft.com/en-us/power-pages/configure/basic-forms
- Power Pages file columns: https://learn.microsoft.com/en-us/power-pages/configure/file-column
- Power Pages portals Web API overview: https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview
- Dataverse file column data: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/file-column-data
