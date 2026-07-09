import type {
  DataverseCollection,
  FormAssignmentRow,
  FormAssignmentSummary,
  FormRow,
  FormVersionRow,
} from './types';
import { devAssignedForms } from '../dev/assignedForms';

type HttpMethod = 'GET' | 'POST' | 'PATCH' | 'DELETE';

interface RequestOptions {
  method?: HttpMethod;
  body?: unknown;
}

declare global {
  interface Window {
    shell?: {
      getTokenDeferred?: () => {
        done: (callback: (token: string) => void) => { fail: (callback: () => void) => void };
      };
    };
  }
}

export class PowerPagesApiClient {
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

  private async request<T>(url: string, options: RequestOptions): Promise<T> {
    const headers: Record<string, string> = {
      Accept: 'application/json',
      'OData-MaxVersion': '4.0',
      'OData-Version': '4.0',
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
    if (response.status === 204) {
      return undefined as T;
    }
    return response.json() as Promise<T>;
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
}
