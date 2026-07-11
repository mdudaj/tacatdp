import type {
  DataverseCollection,
  FormAssignmentRow,
  FormAssignmentSummary,
  FormRow,
  FormVersionRow,
  OdkSubmitResult,
  SubmissionRow,
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

  getSignInUrl(): string {
    const returnUrl = `${window.location.pathname}${window.location.search}${window.location.hash}`;
    return `/SignIn?returnUrl=${encodeURIComponent(returnUrl)}`;
  }

  async listAssignedForms(): Promise<FormAssignmentSummary[]> {
    if (this.shouldUseLocalFixture()) {
      return devAssignedForms;
    }

    const assignments = await this.get<DataverseCollection<FormAssignmentRow>>(
      '/_api/mp_formassignments?$select=mp_formassignmentid,mp_assignmentkey,mp_useremail,_mp_formversion_value&$top=20',
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

  async submitOdkSubmission(assignment: FormAssignmentSummary, payload: unknown): Promise<OdkSubmitResult> {
    if (this.shouldUseLocalFixture()) {
      return {
        instanceId: `local:${crypto.randomUUID()}`,
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
    const instanceId = this.extractInstanceId(xml) ?? `uuid:${crypto.randomUUID()}`;
    const now = new Date().toISOString();
    const existingSubmission = await this.findSubmissionByInstanceId(instanceId);
    const submissionId = existingSubmission?.mp_submissionid ?? await this.createSubmission(assignment, instanceId, now);
    const versionNumber = await this.nextSubmissionVersionNumber(instanceId);
    const submissionVersionId = await this.createSubmissionVersion({
      assignment,
      instanceId,
      now,
      payload,
      submissionId,
      versionNumber,
      xml,
    });
    const attachmentResults = await this.createSubmissionAttachments(submissionVersionId, attachments, now);

    return {
      instanceId,
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
      mp_submissionjson: JSON.stringify(this.summarizePayload(input.payload, input.assignment)),
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

  private async createRecord(url: string, body: unknown): Promise<string> {
    const response = await this.send(url, { method: 'POST', body });
    const entityId = response.headers.get('entityid') ?? response.headers.get('OData-EntityId');
    const id = entityId?.match(/\(([^)]+)\)$/)?.[1] ?? entityId;
    if (!id) {
      throw new Error(`Power Pages Web API create did not return an entity id for ${url}.`);
    }
    return id;
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

  private summarizePayload(payload: unknown, assignment: FormAssignmentSummary): InstancePayloadSummary & {
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
}
