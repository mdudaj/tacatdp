import type {
  DataverseCollection,
  FormAssignmentRow,
  FormAssignmentSummary,
  FormRow,
  FormVersionRow,
  OdkSubmitResult,
  SubmissionRow,
  SubmissionSummary,
  SubmissionVersionRow,
} from './types';
import { devAssignedForms } from '../dev/assignedForms';

type HttpMethod = 'GET' | 'POST' | 'PATCH' | 'DELETE';

interface RequestOptions {
  method?: HttpMethod;
  body?: unknown;
  headers?: Record<string, string>;
}

const INSTANCE_FILE_NAME = 'xml_submission_file';
const SUBMISSION_LIFECYCLE_SUBMITTED = 100000001;
const SUBMISSION_REVIEW_RECEIVED = 100000000;

interface OdkInstancePayload {
  payloadType?: string;
  status?: string;
  violations?: unknown;
  submissionMeta?: unknown;
  data?: Array<FormData>;
}

interface InstancePayloadSummary {
  payloadType?: string;
  status?: string;
  violationCount: number;
  instanceName?: string;
  attachmentNames: string[];
  attachmentDetails: AttachmentPayloadSummary[];
  submissionMeta?: unknown;
}

interface AttachmentPayloadSummary {
  fieldName: string;
  fileName: string;
  mediaType: string;
  size: number;
}

interface AttachmentPayload extends AttachmentPayloadSummary {
  file: File;
}

interface AttachmentPersistResult {
  attachmentId: string;
  binaryUploaded: boolean;
  warning?: string;
}

declare global {
  interface Window {
    __TACATDP_POWERPAGES__?: {
      isAuthenticated?: boolean;
      userEmail?: string;
      userName?: string;
    };
    shell?: {
      getTokenDeferred?: () => {
        done: (callback: (token: string) => void) => { fail: (callback: () => void) => void };
      };
    };
  }
}

export class PowerPagesApiClient {
  hasPowerPagesSession(): boolean {
    return this.shouldUseLocalFixture() || Boolean(window.__TACATDP_POWERPAGES__?.isAuthenticated);
  }

  getSignedInUserLabel(): string {
    if (this.shouldUseLocalFixture()) {
      return 'local.dev@example.test';
    }

    return window.__TACATDP_POWERPAGES__?.userEmail
      || window.__TACATDP_POWERPAGES__?.userName
      || 'Signed in';
  }

  getSignedInUserEmail(): string {
    if (this.shouldUseLocalFixture()) {
      return 'local.dev@example.test';
    }

    return window.__TACATDP_POWERPAGES__?.userEmail?.trim() ?? '';
  }

  getSignInUrl(): string {
    const returnUrl = `${window.location.pathname}${window.location.search}${window.location.hash}`;
    return `/SignIn?returnUrl=${encodeURIComponent(returnUrl)}`;
  }

  async listAssignedForms(): Promise<FormAssignmentSummary[]> {
    if (this.shouldUseLocalFixture()) {
      return devAssignedForms;
    }

    const signedInEmail = this.getSignedInUserEmail();
    if (!signedInEmail) {
      throw new Error('Power Pages session did not provide a signed-in email for assignment filtering.');
    }

    const assignments = await this.get<DataverseCollection<FormAssignmentRow>>(
      `/_api/mp_formassignments?$select=mp_formassignmentid,mp_assignmentkey,mp_useremail,_mp_formversion_value&$filter=mp_useremail eq '${this.escapeODataString(signedInEmail)}'&$top=20`,
    );

    return Promise.all(assignments.value.map((assignment) => this.toSummary(assignment)));
  }

  async getFormVersion(formVersionId: string): Promise<FormVersionRow> {
    return this.get<FormVersionRow>(
      `/_api/mp_formversions(${encodeURIComponent(formVersionId)})?$select=mp_version,mp_webformsenabled,mp_xformxml,_mp_form_value`,
    );
  }

  async getForm(formId: string): Promise<FormRow> {
    return this.get<FormRow>(
      `/_api/mp_forms(${encodeURIComponent(formId)})?$select=mp_name,mp_xmlformid`,
    );
  }

  async listSavedSubmissions(): Promise<SubmissionSummary[]> {
    if (this.shouldUseLocalFixture()) {
      return [];
    }

    const submissions = await this.get<DataverseCollection<SubmissionRow>>(
      `/_api/mp_submissions?$select=mp_submissionid,mp_instanceid,mp_useremail,mp_submittedat,mp_updatedat,mp_lifecyclestatus,mp_reviewstate&$filter=mp_lifecyclestatus eq ${SUBMISSION_LIFECYCLE_SUBMITTED}&$orderby=mp_updatedat desc&$top=5000`,
    );

    return Promise.all(submissions.value.map(async (submission) => {
      const latestVersion = await this.getLatestSubmissionVersionByInstanceId(submission.mp_instanceid);
      const metadata = this.parseSubmissionMetadata(latestVersion?.mp_submissionjson);
      return {
        submissionId: submission.mp_submissionid,
        instanceId: submission.mp_instanceid,
        displayName: metadata.instanceName,
        userEmail: submission.mp_useremail,
        submittedAt: submission.mp_submittedat,
        updatedAt: submission.mp_updatedat,
        lifecycleStatus: submission.mp_lifecyclestatus,
        reviewState: submission.mp_reviewstate,
        assignmentKey: metadata.assignmentKey,
        formVersionId: metadata.formVersionId,
        xmlFormId: metadata.xmlFormId,
        versionNumber: latestVersion?.mp_versionnumber,
      };
    }));
  }

  async getSubmissionFormContext(submission: SubmissionSummary): Promise<FormAssignmentSummary> {
    if (!submission.formVersionId) {
      throw new Error(`Submission ${submission.instanceId} does not include formVersionId metadata for edit mode.`);
    }

    const formVersion = await this.getFormVersion(submission.formVersionId);
    const form = await this.getForm(formVersion._mp_form_value);

    return {
      assignmentId: `submission:${submission.submissionId}`,
      assignmentKey: submission.assignmentKey ?? `submission:${submission.instanceId}`,
      userEmail: submission.userEmail,
      formVersionId: submission.formVersionId,
      formId: formVersion._mp_form_value,
      formName: form.mp_name,
      xmlFormId: form.mp_xmlformid,
      version: formVersion.mp_version,
      xformXml: formVersion.mp_xformxml,
    };
  }

  async getLatestSubmissionXml(instanceId: string): Promise<string> {
    const latestVersion = await this.getLatestSubmissionVersionByInstanceId(instanceId);
    if (!latestVersion?.mp_xformsubmissionxml) {
      throw new Error(`No saved XForm submission XML was found for ${instanceId}.`);
    }

    return latestVersion.mp_xformsubmissionxml;
  }

  async submitOdkSubmission(
    assignment: FormAssignmentSummary,
    payload: unknown,
    options: { existingSubmission?: SubmissionSummary | null } = {},
  ): Promise<OdkSubmitResult> {
    if (this.shouldUseLocalFixture()) {
      return {
        instanceId: `local:${crypto.randomUUID()}`,
        displayName: 'Local development record',
        submissionId: 'local-submission',
        submissionVersionId: 'local-submission-version',
        versionNumber: 1,
        attachmentCount: 0,
        attachmentBinaryUploadCount: 0,
        attachmentWarnings: [],
      };
    }

    const xml = await this.extractSubmittedXml(payload);
    const attachments = this.extractAttachmentPayloads(payload);
    const submittedInstanceId = this.extractInstanceId(xml) ?? `uuid:${crypto.randomUUID()}`;
    const instanceId = options.existingSubmission?.instanceId ?? submittedInstanceId;
    const canonicalXml = this.normalizeInstanceId(xml, instanceId);
    const now = new Date().toISOString();
    const existingSubmission = options.existingSubmission
      ? { mp_submissionid: options.existingSubmission.submissionId, mp_instanceid: options.existingSubmission.instanceId }
      : await this.findSubmissionByInstanceId(instanceId);
    const submissionId = existingSubmission?.mp_submissionid ?? await this.createSubmission(assignment, instanceId, now);
    const versionNumber = await this.nextSubmissionVersionNumber(instanceId);
    const submissionVersionId = await this.createSubmissionVersion({
      assignment,
      instanceId,
      now,
      payload,
      submissionId,
      versionNumber,
      xml: canonicalXml,
    });
    if (existingSubmission) {
      await this.updateSubmission(existingSubmission.mp_submissionid, now);
    }
    const attachmentResults = await this.createSubmissionAttachments(submissionVersionId, attachments, now);

    return {
      instanceId,
      displayName: this.resolveInstanceName(canonicalXml),
      submissionId,
      submissionVersionId,
      versionNumber,
      attachmentCount: attachmentResults.length,
      attachmentBinaryUploadCount: attachmentResults.filter((result) => result.binaryUploaded).length,
      attachmentWarnings: attachmentResults.flatMap((result) => result.warning ? [result.warning] : []),
    };
  }

  private async toSummary(assignment: FormAssignmentRow): Promise<FormAssignmentSummary> {
    const formVersion = await this.getFormVersion(assignment._mp_formversion_value);
    const form = await this.getForm(formVersion._mp_form_value);

    return {
      assignmentId: assignment.mp_formassignmentid,
      assignmentKey: assignment.mp_assignmentkey,
      userEmail: assignment.mp_useremail,
      formVersionId: assignment._mp_formversion_value,
      formId: formVersion._mp_form_value,
      formName: form.mp_name,
      xmlFormId: form.mp_xmlformid,
      version: formVersion.mp_version,
      xformXml: formVersion.mp_xformxml,
    };
  }

  private async get<T>(url: string): Promise<T> {
    return this.request<T>(url, { method: 'GET' });
  }

  private async createSubmission(assignment: FormAssignmentSummary, instanceId: string, now: string): Promise<string> {
    return this.createRecord('/_api/mp_submissions', {
      mp_instanceid: instanceId,
      mp_useremail: assignment.userEmail,
      mp_lifecyclestatus: SUBMISSION_LIFECYCLE_SUBMITTED,
      mp_reviewstate: SUBMISSION_REVIEW_RECEIVED,
      mp_submittedat: now,
      mp_updatedat: now,
    });
  }

  private async createSubmissionVersion(input: {
    assignment: FormAssignmentSummary;
    instanceId: string;
    now: string;
    payload: unknown;
    submissionId: string;
    versionNumber: number;
    xml: string;
  }): Promise<string> {
    const versionKey = `${input.instanceId}:${input.versionNumber}`;
    return this.createRecord('/_api/mp_submissionversions', {
      mp_versionkey: versionKey,
      mp_versionnumber: input.versionNumber,
      mp_instanceid: input.instanceId,
      mp_xformsubmissionxml: input.xml,
      mp_submissionjson: JSON.stringify(this.summarizePayload(input.payload, input.assignment, input.xml)),
      mp_current: true,
      mp_useragent: window.navigator.userAgent.slice(0, 850),
      mp_deviceid: 'tacatdp-powerpages-poc',
      mp_createdat: input.now,
      'mp_Submission@odata.bind': `/mp_submissions(${input.submissionId})`,
    });
  }

  private async createSubmissionAttachments(submissionVersionId: string, attachments: AttachmentPayload[], now: string): Promise<AttachmentPersistResult[]> {
    const results: AttachmentPersistResult[] = [];
    for (const attachment of attachments) {
      const attachmentId = await this.createRecord('/_api/mp_submissionattachments', {
        mp_filename: attachment.fileName,
        mp_mediatype: attachment.mediaType,
        mp_uploadedat: now,
        'mp_SubmissionVersion@odata.bind': `/mp_submissionversions(${submissionVersionId})`,
      });

      const result: AttachmentPersistResult = {
        attachmentId,
        binaryUploaded: false,
      };

      try {
        await this.uploadAttachmentFile(attachmentId, attachment);
        result.binaryUploaded = true;
      } catch (caught) {
        const detail = caught instanceof Error ? caught.message : 'unknown error';
        result.warning = `${attachment.fileName}: metadata saved, binary upload not confirmed (${detail})`;
      }

      results.push(result);
    }

    return results;
  }

  private async findSubmissionByInstanceId(instanceId: string): Promise<SubmissionRow | null> {
    const submissions = await this.get<DataverseCollection<SubmissionRow>>(
      `/_api/mp_submissions?$select=mp_submissionid,mp_instanceid&$filter=mp_instanceid eq '${this.escapeODataString(instanceId)}'&$top=1`,
    );

    return submissions.value[0] ?? null;
  }

  private async nextSubmissionVersionNumber(instanceId: string): Promise<number> {
    const versions = await this.get<DataverseCollection<SubmissionVersionRow>>(
      `/_api/mp_submissionversions?$select=mp_submissionversionid,mp_versionnumber&$filter=mp_instanceid eq '${this.escapeODataString(instanceId)}'&$orderby=mp_versionnumber desc&$top=1`,
    );

    return (versions.value[0]?.mp_versionnumber ?? 0) + 1;
  }

  private async getLatestSubmissionVersionByInstanceId(instanceId: string): Promise<SubmissionVersionRow | null> {
    const versions = await this.get<DataverseCollection<SubmissionVersionRow>>(
      `/_api/mp_submissionversions?$select=mp_submissionversionid,mp_versionnumber,mp_xformsubmissionxml,mp_submissionjson&$filter=mp_instanceid eq '${this.escapeODataString(instanceId)}'&$orderby=mp_versionnumber desc&$top=1`,
    );

    return versions.value[0] ?? null;
  }

  private async createRecord(url: string, body: unknown): Promise<string> {
    const response = await this.send(url, { method: 'POST', body });
    const entityId = response.headers.get('entityid') ?? response.headers.get('OData-EntityId');
    const id = entityId?.match(/\(([^)]+)\)$/)?.[1] ?? entityId;
    if (!id) {
      throw new Error(`Power Pages Web API create did not return an entity id for ${url}.`);
    }
    return id;
  }

  private async updateSubmission(submissionId: string, updatedAt: string): Promise<void> {
    await this.send(`/_api/mp_submissions(${submissionId})`, {
      method: 'PATCH',
      body: {
        mp_updatedat: updatedAt,
        mp_lifecyclestatus: SUBMISSION_LIFECYCLE_SUBMITTED,
        mp_reviewstate: SUBMISSION_REVIEW_RECEIVED,
      },
    });
  }

  private async request<T>(url: string, options: RequestOptions): Promise<T> {
    const response = await this.send(url, options);
    if (response.status === 204) {
      return undefined as T;
    }
    return response.json() as Promise<T>;
  }

  private async send(url: string, options: RequestOptions): Promise<Response> {
    const headers: Record<string, string> = {
      Accept: 'application/json',
      'OData-MaxVersion': '4.0',
      'OData-Version': '4.0',
      ...options.headers,
    };

    const init: RequestInit = {
      method: options.method ?? 'GET',
      credentials: 'same-origin',
      headers,
    };

    if (!this.shouldUseLocalFixture()) {
      headers.__RequestVerificationToken = await this.getRequestVerificationToken();
    }

    if (options.body !== undefined) {
      headers['Content-Type'] = 'application/json';
      init.body = JSON.stringify(options.body);
    }

    const response = await fetch(url, init);
    if (!response.ok) {
      const body = await response.text();
      throw new Error(`${response.status} ${response.statusText}: ${body.slice(0, 500)}`);
    }
    return response;
  }

  private async sendBinary(url: string, file: File): Promise<Response> {
    const headers: Record<string, string> = {
      Accept: 'application/json',
      'OData-MaxVersion': '4.0',
      'OData-Version': '4.0',
      'Content-Type': file.type || 'application/octet-stream',
      'x-ms-file-name': file.name,
    };

    if (!this.shouldUseLocalFixture()) {
      headers.__RequestVerificationToken = await this.getRequestVerificationToken();
    }

    const response = await fetch(url, {
      method: 'PATCH',
      credentials: 'same-origin',
      headers,
      body: file,
    });
    if (!response.ok) {
      const body = await response.text();
      throw new Error(`${response.status} ${response.statusText}: ${body.slice(0, 500)}`);
    }
    return response;
  }

  private async getRequestVerificationToken(): Promise<string> {
    return new Promise((resolve, reject) => {
      const deferred = window.shell?.getTokenDeferred?.();
      if (!deferred) {
        reject(new Error('Power Pages anti-forgery token provider is not available.'));
        return;
      }
      deferred.done(resolve).fail(() => reject(new Error('Unable to obtain Power Pages anti-forgery token.')));
    });
  }

  private shouldUseLocalFixture(): boolean {
    if (!import.meta.env.DEV) {
      return false;
    }

    return window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  }

  private async extractSubmittedXml(payload: unknown): Promise<string> {
    const candidate = payload as OdkInstancePayload;
    if (candidate.status !== 'ready') {
      const violations = Array.isArray(candidate.violations) ? candidate.violations.length : 'unknown';
      throw new Error(`ODK validation is not ready for submission. Violations: ${violations}.`);
    }

    const instanceData = candidate.data?.[0];
    const file = instanceData?.get?.(INSTANCE_FILE_NAME);
    if (file instanceof File) {
      const xml = await file.text();
      if (xml.trim().startsWith('<')) {
        return xml;
      }
    }

    throw new Error('ODK submit payload did not include xml_submission_file instance XML.');
  }

  private extractInstanceId(xml: string): string | null {
    const parsed = new DOMParser().parseFromString(xml, 'text/xml');
    const instanceId = parsed.getElementsByTagName('instanceID')[0]?.textContent?.trim();
    return instanceId || null;
  }

  private async uploadAttachmentFile(attachmentId: string, attachment: AttachmentPayload): Promise<void> {
    await this.sendBinary(`/_api/mp_submissionattachments(${attachmentId})/mp_file`, attachment.file);
  }

  private extractAttachmentPayloads(payload: unknown): AttachmentPayload[] {
    const candidate = payload as OdkInstancePayload;
    const instanceData = candidate.data?.[0];
    const attachments: AttachmentPayload[] = [];
    instanceData?.forEach?.((value, fieldName) => {
      if (fieldName === INSTANCE_FILE_NAME || !(value instanceof File)) {
        return;
      }

      attachments.push({
        fieldName,
        fileName: value.name || fieldName,
        mediaType: value.type || 'application/octet-stream',
        size: value.size,
        file: value,
      });
    });

    return attachments;
  }

  private summarizePayload(payload: unknown, assignment: FormAssignmentSummary, xml: string): InstancePayloadSummary & {
    assignmentKey: string;
    formVersionId: string;
    xmlFormId: string;
  } {
    const candidate = payload as OdkInstancePayload;
    const instanceData = candidate.data?.[0];
    const attachmentNames: string[] = [];
    const attachmentDetails: AttachmentPayloadSummary[] = [];
    instanceData?.forEach?.((_value, key) => {
      if (key !== INSTANCE_FILE_NAME) {
        attachmentNames.push(key);
      }
    });
    for (const attachment of this.extractAttachmentPayloads(payload)) {
      attachmentDetails.push({
        fieldName: attachment.fieldName,
        fileName: attachment.fileName,
        mediaType: attachment.mediaType,
        size: attachment.size,
      });
    }

    return {
      payloadType: candidate.payloadType,
      status: candidate.status,
      violationCount: Array.isArray(candidate.violations) ? candidate.violations.length : 0,
      instanceName: this.resolveInstanceName(xml),
      submissionMeta: candidate.submissionMeta,
      attachmentNames,
      attachmentDetails,
      assignmentKey: assignment.assignmentKey,
      formVersionId: assignment.formVersionId,
      xmlFormId: assignment.xmlFormId,
    };
  }

  private escapeODataString(value: string): string {
    return value.replaceAll("'", "''");
  }

  private parseSubmissionMetadata(value?: string): { assignmentKey?: string; formVersionId?: string; xmlFormId?: string; instanceName?: string } {
    if (!value) {
      return {};
    }

    try {
      const parsed = JSON.parse(value) as { assignmentKey?: unknown; formVersionId?: unknown; xmlFormId?: unknown; instanceName?: unknown };
      return {
        assignmentKey: typeof parsed.assignmentKey === 'string' ? parsed.assignmentKey : undefined,
        formVersionId: typeof parsed.formVersionId === 'string' ? parsed.formVersionId : undefined,
        xmlFormId: typeof parsed.xmlFormId === 'string' ? parsed.xmlFormId : undefined,
        instanceName: typeof parsed.instanceName === 'string' ? parsed.instanceName : undefined,
      };
    } catch {
      return {};
    }
  }

  private normalizeInstanceId(xml: string, instanceId: string): string {
    const parsed = new DOMParser().parseFromString(xml, 'text/xml');
    const instanceIdElement = parsed.getElementsByTagName('instanceID')[0];
    if (!instanceIdElement) {
      return xml;
    }

    instanceIdElement.textContent = instanceId;
    return new XMLSerializer().serializeToString(parsed);
  }

  private resolveInstanceName(xml: string): string | undefined {
    const parsed = new DOMParser().parseFromString(xml, 'text/xml');
    const explicit = this.firstText(parsed, 'instanceName');
    if (explicit) {
      return explicit;
    }

    const customerId = this.firstText(parsed, 'Customer_ID');
    const customerName = this.firstText(parsed, 'Customer_Name');
    if (customerId && customerName) {
      return `${customerId}:${customerName}`;
    }
    if (customerId || customerName) {
      return customerId || customerName;
    }

    return undefined;
  }

  private firstText(document: Document, tagName: string): string | undefined {
    const value = document.getElementsByTagName(tagName)[0]?.textContent?.trim();
    return value || undefined;
  }
}
