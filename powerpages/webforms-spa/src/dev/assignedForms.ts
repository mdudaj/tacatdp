import type { FormAssignmentSummary } from '../powerpages-api/types';

const devXFormXml = `<?xml version="1.0" encoding="UTF-8"?>
<h:html xmlns:h="http://www.w3.org/1999/xhtml"
        xmlns="http://www.w3.org/2002/xforms"
        xmlns:jr="http://openrosa.org/javarosa"
        xmlns:odk="http://www.opendatakit.org/xforms">
  <h:head>
    <h:title>TACATDP Impact Evaluation</h:title>
    <model odk:xforms-version="1.0.0">
      <instance>
        <data id="tacatdp_impact_evaluation" version="260709-rich-mvp">
          <start/>
          <end/>
          <today/>
          <enumerator_name/>
          <ward/>
          <facility_name/>
          <respondent_role/>
          <children_reached/>
          <girls_reached/>
          <boys_reached/>
          <observation_notes/>
          <facility_photo/>
        </data>
      </instance>
      <bind nodeset="/data/start" type="dateTime" jr:preload="timestamp" jr:preloadParams="start"/>
      <bind nodeset="/data/end" type="dateTime" jr:preload="timestamp" jr:preloadParams="end"/>
      <bind nodeset="/data/today" type="date" jr:preload="date"/>
      <bind nodeset="/data/enumerator_name" type="string" required="true()"/>
      <bind nodeset="/data/ward" type="string" required="true()"/>
      <bind nodeset="/data/facility_name" type="string" required="true()"/>
      <bind nodeset="/data/respondent_role" type="string" required="true()"/>
      <bind nodeset="/data/children_reached" type="int" required="true()" constraint=". &gt;= 0"/>
      <bind nodeset="/data/girls_reached" type="int" constraint=". &gt;= 0"/>
      <bind nodeset="/data/boys_reached" type="int" constraint=". &gt;= 0"/>
      <bind nodeset="/data/observation_notes" type="string"/>
      <bind nodeset="/data/facility_photo" type="binary"/>
    </model>
  </h:head>
  <h:body>
    <input ref="/data/enumerator_name"><label>Enumerator name</label></input>
    <input ref="/data/ward"><label>Ward</label></input>
    <input ref="/data/facility_name"><label>Facility name</label></input>
    <select1 ref="/data/respondent_role">
      <label>Respondent role</label>
      <item><label>Facility in-charge</label><value>facility_in_charge</value></item>
      <item><label>CHW supervisor</label><value>chw_supervisor</value></item>
      <item><label>Project officer</label><value>project_officer</value></item>
    </select1>
    <input ref="/data/children_reached"><label>Children reached</label></input>
    <input ref="/data/girls_reached"><label>Girls reached</label></input>
    <input ref="/data/boys_reached"><label>Boys reached</label></input>
    <input ref="/data/observation_notes"><label>Observation notes</label></input>
    <upload ref="/data/facility_photo" mediatype="image/*"><label>Facility photo</label></upload>
  </h:body>
</h:html>`;

export const devAssignedForms: FormAssignmentSummary[] = [
  {
    assignmentId: 'dev-assignment-tacatdp-impact',
    assignmentKey: 'DEV-TACATDP-IMPACT',
    userEmail: 'local.dev@example.test',
    formVersionId: 'dev-form-version-rich-mvp',
    formId: 'dev-form-tacatdp-impact',
    formName: 'TACATDP Impact Evaluation',
    xmlFormId: 'tacatdp_impact_evaluation',
    version: '260709-rich-mvp',
    xformXml: devXFormXml,
  },
];
