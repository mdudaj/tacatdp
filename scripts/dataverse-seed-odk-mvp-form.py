#!/usr/bin/env python3
"""Seed a richer XForm-backed TACATDP MVP form for the Power Pages ODK runtime.

This seed targets the ODK Central-inspired schema:
- Projects
- Forms
- FormVersions
- FormAssignments

It intentionally does not create decomposed Questions/Choices rows. The runtime source of
truth is FormVersions.XFormXml.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

DEFAULT_ASSIGNMENT_EMAIL = "john.mduda@mshirikacorp.onmicrosoft.com"
MAX_XFORMXML_CHARS = 1048576
XFORM_FILE_MARKER_PREFIX = "dataverse-file:"
XFORM_FILE_MEDIA_TYPE = "application/xml"
PROJECT_CODE = "TACATDP"
PROJECT_NAME = "TACATDP Impact Monitoring"
XML_FORM_ID = "tacatdp_impact_evaluation"
FORM_NAME = "TACATDP Impact Evaluation"
FORM_VERSION = "260709-rich-mvp"
ASSIGNMENT_KEY_TEMPLATE = f"{XML_FORM_ID}:{{email}}"

CHOICE = {
    "active": 100000000,
    "open": 100000001,
    "published": 100000001,
    "assignment_active": 100000000,
}

RICH_TACATDP_XFORM = """<?xml version="1.0" encoding="UTF-8"?>
<h:html xmlns:h="http://www.w3.org/1999/xhtml"
        xmlns="http://www.w3.org/2002/xforms"
        xmlns:ev="http://www.w3.org/2001/xml-events"
        xmlns:jr="http://openrosa.org/javarosa"
        xmlns:odk="http://www.opendatakit.org/xforms"
        xmlns:orx="http://openrosa.org/xforms">
  <h:head>
    <h:title>TACATDP Impact Evaluation - Rich MVP</h:title>
    <model odk:xforms-version="1.0.0">
      <instance>
        <data id="tacatdp_impact_evaluation" version="260709-rich-mvp">
          <Customer_ID/><Customer_Name/><Gender/><age/><Education_Level/>
          <zone/><CRDB_Branch/><region/><district/><ward/><village/><Georeference/>
          <Farmer_Phone/><loan_amount_tzs/><own_farmland/><land_size_acres/>
          <crop_name/><crop_category/><technology/><climate_risk/>
          <Uses_Irrigation/><Irrigation_Type/><Water_Source/><Energy_Source/><Adopted_Energy/>
          <baseline_yield/><yield_after/><farmer_group_member/><farmer_group_type/>
          <male_members/><female_members/><youth_members/><hh_male/><hh_female/>
          <hh_head_gender/><women_decision/><ara_training/><training_type/><target_group/>
          <male_trained/><female_trained/><vc_stages/><farm_photo/>
          <meta><instanceID/></meta>
        </data>
      </instance>
      <bind nodeset="/data/Customer_ID" type="int"/>
      <bind nodeset="/data/Customer_Name" type="string"/>
      <bind nodeset="/data/Gender" type="select1" required="true()"/>
      <bind nodeset="/data/age" type="int" constraint=". &gt;= 18 and . &lt;= 120" jr:constraintMsg="Farmer age must be between 18 and 120."/>
      <bind nodeset="/data/Education_Level" type="select1" required="true()"/>
      <bind nodeset="/data/zone" type="select1" required="true()"/>
      <bind nodeset="/data/CRDB_Branch" type="select1" required="true()"/>
      <bind nodeset="/data/region" type="select1" required="true()"/>
      <bind nodeset="/data/district" type="select1" required="true()"/>
      <bind nodeset="/data/ward" type="select1" required="true()"/>
      <bind nodeset="/data/village" type="select1" required="true()"/>
      <bind nodeset="/data/Georeference" type="geopoint"/>
      <bind nodeset="/data/Farmer_Phone" type="string" required="true()" constraint="regex(., '0\\d{9}') and string-length(.) = 10" jr:constraintMsg="Insert a 10-digit number including the zero in the beginning."/>
      <bind nodeset="/data/loan_amount_tzs" type="int" required="true()" constraint=". &gt;= 200000" jr:constraintMsg="Loan amount must be TZS 200,000 or more."/>
      <bind nodeset="/data/own_farmland" type="select1" required="true()"/>
      <bind nodeset="/data/land_size_acres" type="int" required="true()" constraint=". &gt; 0"/>
      <bind nodeset="/data/crop_name" type="select" required="true()"/>
      <bind nodeset="/data/crop_category" type="select" required="true()"/>
      <bind nodeset="/data/technology" type="select" required="true()"/>
      <bind nodeset="/data/climate_risk" type="select" required="true()"/>
      <bind nodeset="/data/Uses_Irrigation" type="select1" required="true()"/>
      <bind nodeset="/data/Irrigation_Type" type="select" required="true()" relevant="/data/Uses_Irrigation = '1'"/>
      <bind nodeset="/data/Water_Source" type="select" required="true()"/>
      <bind nodeset="/data/Energy_Source" type="select" required="true()"/>
      <bind nodeset="/data/Adopted_Energy" type="select" required="true()"/>
      <bind nodeset="/data/baseline_yield" type="int" required="true()" constraint=". &gt;= 0"/>
      <bind nodeset="/data/yield_after" type="int" required="true()" constraint=". &gt;= /data/baseline_yield" jr:constraintMsg="Yield after TACATDP should be greater than or equal to baseline yield."/>
      <bind nodeset="/data/farmer_group_member" type="select1" required="true()"/>
      <bind nodeset="/data/farmer_group_type" type="select1" required="true()" relevant="/data/farmer_group_member = '1'"/>
      <bind nodeset="/data/male_members" type="int" required="true()" relevant="/data/farmer_group_member = '1'" constraint=". &gt;= 0"/>
      <bind nodeset="/data/female_members" type="int" required="true()" relevant="/data/farmer_group_member = '1'" constraint=". &gt;= 0"/>
      <bind nodeset="/data/youth_members" type="int" required="true()" relevant="/data/farmer_group_member = '1'" constraint=". &gt;= 0"/>
      <bind nodeset="/data/hh_male" type="int" required="true()" constraint=". &gt;= 0"/>
      <bind nodeset="/data/hh_female" type="int" required="true()" constraint=". &gt;= 0"/>
      <bind nodeset="/data/hh_head_gender" type="select1" required="true()"/>
      <bind nodeset="/data/women_decision" type="select1" required="true()"/>
      <bind nodeset="/data/ara_training" type="select1" required="true()"/>
      <bind nodeset="/data/training_type" type="select" required="true()" relevant="/data/ara_training = '1'"/>
      <bind nodeset="/data/target_group" type="select" required="true()" relevant="/data/ara_training = '1'" constraint="count-selected(.) &gt;= 1"/>
      <bind nodeset="/data/male_trained" type="int" required="true()" relevant="/data/ara_training = '1'" constraint=". &gt;= 0"/>
      <bind nodeset="/data/female_trained" type="int" required="true()" relevant="/data/ara_training = '1'" constraint=". &gt;= 0"/>
      <bind nodeset="/data/vc_stages" type="select" required="true()"/>
      <bind nodeset="/data/farm_photo" type="binary" mediatype="image/*"/>
      <bind nodeset="/data/meta/instanceID" type="string" readonly="true()" calculate="concat('uuid:', uuid())"/>
    </model>
  </h:head>
  <h:body>
    <group><label>Farmer identity and location</label>
      <input ref="/data/Customer_ID"><label>Customer ID</label></input>
      <input ref="/data/Customer_Name"><label>Customer Name</label></input>
      <select1 ref="/data/Gender"><label>Gender</label><item><label>Male</label><value>1</value></item><item><label>Female</label><value>2</value></item></select1>
      <input ref="/data/age"><label>Farmer Age</label></input>
      <select1 ref="/data/Education_Level"><label>Education Level</label><item><label>None</label><value>1</value></item><item><label>Primary</label><value>2</value></item><item><label>Secondary</label><value>3</value></item><item><label>College</label><value>4</value></item><item><label>University</label><value>5</value></item></select1>
      <select1 ref="/data/zone"><label>Zone</label><item><label>Central Zone</label><value>1</value></item><item><label>Coastal Zone</label><value>2</value></item><item><label>Lake Zone</label><value>5</value></item><item><label>Northern Zone</label><value>6</value></item><item><label>Southern Zone</label><value>7</value></item></select1>
      <select1 ref="/data/CRDB_Branch"><label>CRDB Branch</label><item><label>Dodoma</label><value>1</value></item><item><label>Morogoro</label><value>7</value></item><item><label>Ifakara</label><value>10</value></item></select1>
      <select1 ref="/data/region"><label>Region</label><item><label>Arusha</label><value>1</value></item><item><label>Dar es Salaam</label><value>2</value></item><item><label>Dodoma</label><value>3</value></item><item><label>Morogoro</label><value>14</value></item></select1>
      <select1 ref="/data/district"><label>District</label><item><label>Arusha</label><value>2</value></item><item><label>Chamwino</label><value>52</value></item><item><label>Kilombero</label><value>98</value></item></select1>
      <select1 ref="/data/ward"><label>Ward</label><item><label>Kimandolu</label><value>1</value></item><item><label>Chamwino</label><value>25</value></item><item><label>Ifakara</label><value>77</value></item></select1>
      <select1 ref="/data/village"><label>Village</label><item><label>Kitiangare</label><value>1</value></item><item><label>Tindigani</label><value>2</value></item><item><label>Kijenge Kaskazini</label><value>3</value></item></select1>
      <input ref="/data/Georeference"><label>GPS point</label><hint>Measure this outside of the house, in front of the main door.</hint></input>
      <input ref="/data/Farmer_Phone"><label>Farmer Phone</label></input>
    </group>
    <group><label>Farm and production profile</label>
      <input ref="/data/loan_amount_tzs"><label>Loan Amount (TZS)</label></input>
      <select1 ref="/data/own_farmland"><label>Farmer or household owns farmland?</label><item><label>Yes</label><value>1</value></item><item><label>No</label><value>2</value></item></select1>
      <input ref="/data/land_size_acres"><label>Land Size (Acres)</label></input>
      <select ref="/data/crop_name"><label>Crop Name</label><item><label>Maize</label><value>1.1</value></item><item><label>Paddy</label><value>1.2</value></item><item><label>Rice</label><value>1.3</value></item><item><label>Sunflower</label><value>7.1</value></item></select>
      <select ref="/data/crop_category"><label>Crop Category</label><item><label>Cereal Grain</label><value>1</value></item><item><label>Fruit Crop</label><value>2</value></item><item><label>Grain Legumes</label><value>3</value></item><item><label>Edible oil crop</label><value>7</value></item></select>
      <select ref="/data/technology"><label>TACATDP ARA Technology Deployed</label><item><label>Climate-smart seeds</label><value>1</value></item><item><label>Organic inputs and soil testing</label><value>2</value></item><item><label>Efficient irrigation</label><value>4</value></item><item><label>Rainwater harvesting and water storage</label><value>5</value></item><item><label>Solar productive use equipment</label><value>13</value></item></select>
      <select ref="/data/climate_risk"><label>Available key climate risks/hazards</label><item><label>Drought</label><value>1</value></item><item><label>Flooding</label><value>2</value></item><item><label>Erratic rainfall</label><value>3</value></item><item><label>Pest infestation</label><value>7</value></item></select>
      <select1 ref="/data/Uses_Irrigation"><label>Uses Irrigation?</label><item><label>Yes</label><value>1</value></item><item><label>No</label><value>2</value></item></select1>
      <select ref="/data/Irrigation_Type"><label>Irrigation Type</label><item><label>Drip Irrigation</label><value>1</value></item><item><label>Sprinkler Irrigation</label><value>2</value></item><item><label>Solar-Powered Pump Irrigation</label><value>7</value></item></select>
      <select ref="/data/Water_Source"><label>Water Source</label><item><label>Borehole water</label><value>1</value></item><item><label>River and stream water</label><value>3</value></item><item><label>Rainwater harvesting</label><value>8</value></item></select>
      <select ref="/data/Energy_Source"><label>Current Energy Source Used</label><item><label>National grid electricity</label><value>1</value></item><item><label>Diesel/petrol systems</label><value>2</value></item><item><label>Solar energy</label><value>3</value></item></select>
      <select ref="/data/Adopted_Energy"><label>Adopted Energy Source After ARA</label><item><label>Solar-powered irrigation pumps</label><value>2</value></item><item><label>Solar cold rooms</label><value>3</value></item><item><label>Biogas systems</label><value>8</value></item></select>
      <input ref="/data/baseline_yield"><label>Baseline Yield (kg/acre)</label></input>
      <input ref="/data/yield_after"><label>Yield After TACATDP ARA Deployment (kg/acre)</label></input>
      <upload ref="/data/farm_photo" mediatype="image/*"><label>Farm photo</label></upload>
    </group>
    <group><label>Group, household, training, and beneficiaries</label>
      <select1 ref="/data/farmer_group_member"><label>Is farmer a member of a Farmer Group?</label><item><label>Yes</label><value>1</value></item><item><label>No</label><value>2</value></item></select1>
      <select1 ref="/data/farmer_group_type"><label>Farmer Group Type</label><item><label>Producer Group</label><value>producer_group</value></item><item><label>Cooperative</label><value>cooperative</value></item><item><label>SACCO</label><value>sacco</value></item></select1>
      <input ref="/data/male_members"><label>Male Group Members</label></input>
      <input ref="/data/female_members"><label>Female Group Members</label></input>
      <input ref="/data/youth_members"><label>Youth Group Members</label></input>
      <input ref="/data/hh_male"><label>Number of male household members</label></input>
      <input ref="/data/hh_female"><label>Number of female household members</label></input>
      <select1 ref="/data/hh_head_gender"><label>Head of Household Gender</label><item><label>Male</label><value>1</value></item><item><label>Female</label><value>2</value></item></select1>
      <select1 ref="/data/women_decision"><label>Are women direct decision-makers in ARA investment use?</label><item><label>Yes</label><value>1</value></item><item><label>No</label><value>2</value></item></select1>
      <select1 ref="/data/ara_training"><label>Did the farmer or group receive ARA training?</label><item><label>Yes</label><value>1</value></item><item><label>No</label><value>2</value></item></select1>
      <select ref="/data/training_type"><label>Type of Training Received</label><item><label>ARA Practices</label><value>1</value></item><item><label>Financial Inclusion</label><value>2</value></item><item><label>Gender and Social Inclusion</label><value>3</value></item><item><label>Climate-Smart Agriculture</label><value>4</value></item></select>
      <select ref="/data/target_group"><label>Target Groups Covered</label><item><label>Women</label><value>1</value></item><item><label>Youth</label><value>2</value></item><item><label>Vulnerable Groups</label><value>3</value></item><item><label>Mixed Group</label><value>5</value></item></select>
      <input ref="/data/male_trained"><label>Number of male farmers trained</label></input>
      <input ref="/data/female_trained"><label>Number of female farmers trained</label></input>
      <select ref="/data/vc_stages"><label>Value Chain Stages involved</label><item><label>Farm preparation</label><value>1</value></item><item><label>Farm operations</label><value>2</value></item><item><label>Input supply</label><value>3</value></item><item><label>Harvesting</label><value>6</value></item><item><label>Post-harvest handling</label><value>7</value></item></select>
    </group>
  </h:body>
</h:html>
"""


def load_deploy_module():
    module_path = Path(__file__).resolve().parent / "dataverse-schema-deploy.py"
    spec = importlib.util.spec_from_file_location("dataverse_schema_deploy", module_path)
    if not spec or not spec.loader:
        raise SystemExit(f"Unable to load {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["dataverse_schema_deploy"] = module
    spec.loader.exec_module(module)
    return module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed a richer ODK/XForm-backed TACATDP MVP form and assignment.")
    parser.add_argument("--env-file", default=".env", help="Environment file containing Power Platform settings.")
    parser.add_argument("--assignment-email", default=None, help="User email to receive the active form assignment.")
    parser.add_argument("--xform-xml", default=None, help="Compiled XForm XML to store in FormVersions.XFormXml.")
    parser.add_argument("--form-version", default=None, help="Published form version code. Defaults to generated UTC YYYYMMDDHHMMSSmmm when --xform-xml is used.")
    parser.add_argument("--form-name", default=FORM_NAME, help="User-facing form/tool name.")
    parser.add_argument("--execute", action="store_true", help="Perform live writes. Without this flag only a dry-run summary is shown.")
    return parser.parse_args()


def timestamp_version() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y%m%d%H%M%S") + f"{now.microsecond // 1000:03d}"


def escape_odata(value: str) -> str:
    return value.replace("'", "''")


def parse_guid_from_entity_id(value: str) -> str:
    return value.rsplit("(", 1)[-1].rstrip(")")


class SeedClient:
    def __init__(self, deploy: Any, settings: Any, token: str) -> None:
        self.deploy = deploy
        self.settings = settings
        self.dv = deploy.Dataverse(settings, token)
        self.prefix = settings.publisher_prefix
        self.entity_sets: dict[str, str] = {}
        self.primary_ids: dict[str, str] = {}
        self.nav_properties: dict[str, str] = {}

    def logical(self, table: str) -> str:
        return self.deploy.table_logical_name(self.prefix, table)

    def column(self, column: str) -> str:
        return self.deploy.column_logical_name(self.prefix, column)

    def entity_set(self, table: str) -> str:
        if table not in self.entity_sets:
            logical = self.logical(table)
            data = self.dv.get_json(f"EntityDefinitions(LogicalName='{logical}')?$select=EntitySetName,PrimaryIdAttribute")
            if not data:
                raise RuntimeError(f"Missing table metadata for {logical}")
            self.entity_sets[table] = data["EntitySetName"]
            self.primary_ids[table] = data["PrimaryIdAttribute"]
        return self.entity_sets[table]

    def primary_id(self, table: str) -> str:
        self.entity_set(table)
        return self.primary_ids[table]

    def nav_property(self, relationship_schema: str) -> str:
        if relationship_schema not in self.nav_properties:
            encoded = quote(relationship_schema, safe="")
            base = self.dv.get_json(f"RelationshipDefinitions(SchemaName='{encoded}')?$select=MetadataId")
            if not base:
                raise RuntimeError(f"Missing relationship metadata for {relationship_schema}")
            metadata_id = base["MetadataId"]
            data = self.dv.get_json(f"RelationshipDefinitions({metadata_id})/Microsoft.Dynamics.CRM.OneToManyRelationshipMetadata?$select=ReferencingEntityNavigationPropertyName")
            if not data:
                raise RuntimeError(f"Missing one-to-many relationship metadata for {relationship_schema}")
            self.nav_properties[relationship_schema] = data["ReferencingEntityNavigationPropertyName"]
        return self.nav_properties[relationship_schema]

    def relationship_name(self, referenced: str, referencing: str, lookup: str) -> str:
        rel = {"referenced_table": referenced, "referencing_table": referencing, "lookup_column": lookup}
        return self.deploy.relationship_schema_name(self.settings, rel)

    def bind(self, referenced_table: str, referencing_table: str, lookup: str, record_id: str) -> tuple[str, str]:
        rel_schema = self.relationship_name(referenced_table, referencing_table, lookup)
        nav = self.nav_property(rel_schema)
        entity_set = "systemusers" if referenced_table == "SystemUser" else self.entity_set(referenced_table)
        return f"{nav}@odata.bind", f"/{entity_set}({record_id})"

    def find_one(self, table: str, filter_expr: str) -> dict[str, Any] | None:
        entity_set = self.entity_set(table)
        primary_id = self.primary_id(table)
        data = self.dv.get_json(f"{entity_set}?$select={primary_id}&$filter={filter_expr}&$top=1")
        values = (data or {}).get("value") or []
        return values[0] if values else None

    def create(self, table: str, payload: dict[str, Any]) -> str:
        response = self.dv.post(self.entity_set(table), payload)
        return parse_guid_from_entity_id(response.headers.get("OData-EntityId", ""))

    def update(self, table: str, record_id: str, payload: dict[str, Any]) -> None:
        response = self.dv.request("PATCH", f"{self.entity_set(table)}({record_id})", payload=payload)
        if response.status_code >= 400:
            raise RuntimeError(f"PATCH {table} failed: HTTP {response.status_code} {self.deploy.safe_error(response)}")

    def upload_file_column(self, table: str, record_id: str, column: str, path: Path, file_name: str, media_type: str) -> None:
        url = f"{self.dv.base}/{self.entity_set(table)}({record_id})/{self.column(column)}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/octet-stream",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
            "x-ms-file-name": file_name,
        }
        with path.open("rb") as handle:
            response = self.dv.session.patch(url, data=handle, headers=headers, timeout=180)
        if response.status_code >= 400:
            raise RuntimeError(f"PATCH {table}.{column} file failed: HTTP {response.status_code} {self.deploy.safe_error(response)}")

    def ensure(self, table: str, filter_expr: str, payload: dict[str, Any], label: str, execute: bool, update_existing: bool = False) -> str | None:
        existing = self.find_one(table, filter_expr)
        primary_id = self.primary_id(table)
        if existing:
            record_id = existing[primary_id]
            if execute and update_existing:
                self.update(table, record_id, payload)
                print(f"updated: {label}")
            else:
                print(f"exists: {label}")
            return record_id
        if not execute:
            print(f"would create: {label}")
            return None
        record_id = self.create(table, payload)
        print(f"created: {label}")
        return record_id

    def find_system_user(self, email: str) -> str | None:
        escaped = escape_odata(email.lower())
        data = self.dv.get_json(f"systemusers?$select=systemuserid,internalemailaddress,domainname&$filter=internalemailaddress eq '{escaped}' or domainname eq '{escaped}'&$top=1")
        values = (data or {}).get("value") or []
        return values[0]["systemuserid"] if values else None


def env_assignment_email(deploy: Any, env_file: str, explicit: str | None) -> str:
    if explicit:
        return explicit
    env = deploy.load_env(Path(env_file).resolve())
    return env.get("TACATDP_SEED_USER_EMAIL") or env.get("POWER_PLATFORM_ASSIGNMENT_USER_EMAIL") or DEFAULT_ASSIGNMENT_EMAIL


def load_xform_xml(path: str | None, version: str, form_name: str) -> tuple[str, str]:
    if not path:
        return RICH_TACATDP_XFORM, "seed-rich-mvp-20260709"
    xml_path = Path(path).resolve()
    if not xml_path.exists():
        raise SystemExit(f"Compiled XForm XML not found: {xml_path}")
    text = xml_path.read_text(encoding="utf-8")
    if XML_FORM_ID not in text:
        raise SystemExit(f"Compiled XForm XML does not contain expected form id {XML_FORM_ID}: {xml_path}")
    if f'version="{version}"' not in text:
        raise SystemExit(f"Compiled XForm XML does not contain expected version {version}: {xml_path}")
    if form_name not in text:
        raise SystemExit(f"Compiled XForm XML does not contain expected form title {form_name}: {xml_path}")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text, f"xlsform-{version}-{digest[:12]}"


def load_xform_xml_path(path: str | None) -> Path | None:
    return Path(path).resolve() if path else None


def main() -> int:
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    args = parse_args()
    deploy = load_deploy_module()
    settings = deploy.build_settings(argparse.Namespace(env_file=args.env_file, schema_dir=None, schema_file=None, execute=False, no_publish=False))
    assignment_email = env_assignment_email(deploy, args.env_file, args.assignment_email).lower()
    form_version = args.form_version or (timestamp_version() if args.xform_xml else FORM_VERSION)
    xform_xml, xform_hash = load_xform_xml(args.xform_xml, form_version, args.form_name)
    xform_xml_path = load_xform_xml_path(args.xform_xml)
    xform_bytes = len(xform_xml.encode("utf-8"))
    xform_file_name = xform_xml_path.name if xform_xml_path else f"{XML_FORM_ID}-{form_version}.xml"
    uses_file_storage = xform_bytes > MAX_XFORMXML_CHARS
    xform_runtime_source = f"{XFORM_FILE_MARKER_PREFIX}{xform_file_name}" if uses_file_storage else xform_xml

    print("# TACATDP ODK Rich MVP Seed")
    print(f"Mode: {'execute' if args.execute else 'dry-run'}")
    print(f"Target: {settings.deploy_target}")
    print(f"Environment: {settings.environment_url}")
    print(f"Assignment email: {assignment_email}")
    print(f"XmlFormId: {XML_FORM_ID}")
    print(f"Form name: {args.form_name}")
    print(f"Version: {form_version}")
    print(f"XForm XML bytes: {xform_bytes}")
    print(f"XForm hash: {xform_hash}")
    print(f"XForm storage: {'FormAttachments.File' if uses_file_storage else 'FormVersions.XFormXml'}")
    if uses_file_storage and not xform_xml_path:
        raise SystemExit("Refusing Dataverse write: file-backed XForm storage requires --xform-xml.")

    if settings.deploy_target.lower() != "dev":
        raise SystemExit(f"Refusing non-dev deployment target: {settings.deploy_target}")
    if not args.execute:
        print("Dry-run only. Re-run with --execute to seed Dataverse rows.")

    token = deploy.get_token(settings)
    client = SeedClient(deploy, settings, token)
    now = datetime.now(timezone.utc).isoformat()

    project_id = client.ensure(
        "Projects",
        f"{client.column('ProjectCode')} eq '{escape_odata(PROJECT_CODE)}'",
        {
            client.column("ProjectCode"): PROJECT_CODE,
            client.column("Name"): PROJECT_NAME,
            client.column("Description"): "TACATDP Power Pages ODK Web Forms MVP project.",
            client.column("LifecycleStatus"): CHOICE["active"],
        },
        f"project {PROJECT_CODE}",
        args.execute,
        update_existing=True,
    ) or "DRY-RUN-PROJECT-ID"

    form_payload = {
        client.column("XmlFormId"): XML_FORM_ID,
        client.column("Name"): args.form_name,
        client.column("Description"): "TACATDP Impact Evaluation form compiled from XLSForm for ODK Web Forms testing.",
        client.column("LifecycleStatus"): CHOICE["open"],
    }
    if args.execute:
        key, value = client.bind("Projects", "Forms", "Project", project_id)
        form_payload[key] = value
    form_id = client.ensure(
        "Forms",
        f"{client.column('XmlFormId')} eq '{escape_odata(XML_FORM_ID)}'",
        form_payload,
        f"form {XML_FORM_ID}",
        args.execute,
        update_existing=True,
    ) or "DRY-RUN-FORM-ID"

    version_payload = {
        client.column("Version"): form_version,
        client.column("Hash"): xform_hash,
        client.column("XFormXml"): xform_runtime_source,
        client.column("WebFormsEnabled"): True,
        client.column("LifecycleStatus"): CHOICE["published"],
        client.column("PublishedAt"): now,
    }
    if args.execute:
        key, value = client.bind("Forms", "FormVersions", "Form", form_id)
        version_payload[key] = value
    version_id = client.ensure(
        "FormVersions",
        f"{client.column('Version')} eq '{escape_odata(form_version)}'",
        version_payload,
        f"form version {form_version}",
        args.execute,
        update_existing=True,
    ) or "DRY-RUN-VERSION-ID"

    if uses_file_storage:
        attachment_payload = {
            client.column("FileName"): xform_file_name,
            client.column("MediaType"): XFORM_FILE_MEDIA_TYPE,
        }
        if not args.execute:
            print(f"would create/update: xform file {xform_file_name}")
            print(f"would upload: xform file {xform_file_name}")
        elif xform_xml_path:
            key, value = client.bind("FormVersions", "FormAttachments", "FormVersion", version_id)
            attachment_payload[key] = value
            attachment_filter = (
                f"{client.column('FileName')} eq '{escape_odata(xform_file_name)}' "
                f"and _{client.column('FormVersion')}_value eq {version_id}"
            )
            attachment_id = client.ensure(
                "FormAttachments",
                attachment_filter,
                attachment_payload,
                f"xform file {xform_file_name}",
                args.execute,
                update_existing=True,
            )
            if not attachment_id:
                raise RuntimeError(f"Unable to resolve XForm attachment row for {xform_file_name}")
            client.upload_file_column("FormAttachments", attachment_id, "File", xform_xml_path, xform_file_name, XFORM_FILE_MEDIA_TYPE)
            print(f"uploaded: xform file {xform_file_name}")

    assignment_key = ASSIGNMENT_KEY_TEMPLATE.format(email=assignment_email)
    assignment_payload = {
        client.column("UserEmail"): assignment_email,
        client.column("AssignmentKey"): assignment_key,
        client.column("LifecycleStatus"): CHOICE["assignment_active"],
    }
    if args.execute:
        key, value = client.bind("FormVersions", "FormAssignments", "FormVersion", version_id)
        assignment_payload[key] = value
        user_id = client.find_system_user(assignment_email)
        if user_id:
            key, value = client.bind("SystemUser", "FormAssignments", "User", user_id)
            assignment_payload[key] = value
        else:
            print(f"warning: system user not found for {assignment_email}; using UserEmail fallback only")
    existing_assignment = client.find_one(
        "FormAssignments",
        f"{client.column('UserEmail')} eq '{escape_odata(assignment_email)}'",
    )
    if existing_assignment and args.execute:
        assignment_id = existing_assignment[client.primary_id("FormAssignments")]
        client.update("FormAssignments", assignment_id, assignment_payload)
        print(f"updated: assignment for {assignment_email} -> form version {form_version}")
    elif existing_assignment:
        print(f"would update: assignment for {assignment_email} -> form version {form_version}")
    else:
        client.ensure(
            "FormAssignments",
            f"{client.column('AssignmentKey')} eq '{escape_odata(assignment_key)}'",
            assignment_payload,
            f"assignment {assignment_key}",
            args.execute,
            update_existing=True,
        )

    print("seed complete" if args.execute else "dry-run complete")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
