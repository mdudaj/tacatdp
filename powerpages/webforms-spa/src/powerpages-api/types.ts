export interface DataverseCollection<T> {
  value: T[];
}

export interface FormAssignmentRow {
  mp_formassignmentid: string;
  mp_assignmentkey: string;
  mp_useremail?: string;
  _mp_formversion_value: string;
}

export interface FormVersionRow {
  mp_formversionid?: string;
  mp_version: string;
  mp_webformsenabled: boolean;
  mp_xformxml: string;
  _mp_form_value: string;
}

export interface FormRow {
  mp_formid?: string;
  mp_name: string;
  mp_xmlformid: string;
}

export interface FormAssignmentSummary {
  assignmentId: string;
  assignmentKey: string;
  userEmail?: string;
  formVersionId: string;
  formId: string;
  formName: string;
  xmlFormId: string;
  version: string;
  xformXml: string;
}

export interface SubmissionRow {
  mp_submissionid: string;
  mp_instanceid: string;
  mp_useremail?: string;
  mp_submittedat?: string;
  mp_updatedat?: string;
  mp_lifecyclestatus?: number;
  mp_reviewstate?: number;
}

export interface SubmissionVersionRow {
  mp_submissionversionid: string;
  mp_versionnumber: number;
  mp_xformsubmissionxml?: string;
  mp_submissionjson?: string;
}

export interface OdkSubmitResult {
  instanceId: string;
  submissionId: string;
  submissionVersionId: string;
  versionNumber: number;
  attachmentCount: number;
  attachmentBinaryUploadCount: number;
  attachmentWarnings: string[];
}

export interface SubmissionSummary {
  submissionId: string;
  instanceId: string;
  userEmail?: string;
  submittedAt?: string;
  updatedAt?: string;
  lifecycleStatus?: number;
  reviewState?: number;
  assignmentKey?: string;
  formVersionId?: string;
  xmlFormId?: string;
  versionNumber?: number;
}
