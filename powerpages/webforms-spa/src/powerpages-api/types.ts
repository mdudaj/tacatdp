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
