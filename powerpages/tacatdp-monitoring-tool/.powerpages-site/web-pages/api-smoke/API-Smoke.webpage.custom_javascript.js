(function () {
  "use strict";

  var endpoints = {
    assignments: "/_api/mp_formassignments?$select=mp_assignmentkey,mp_useremail,mp_lifecyclestatus,_mp_formversion_value&$top=10",
    formVersion: function (id) {
      return "/_api/mp_formversions(" + encodeURIComponent(id) + ")?$select=mp_version,mp_webformsenabled,mp_lifecyclestatus,mp_xformxml,_mp_form_value";
    },
    form: function (id) {
      return "/_api/mp_forms(" + encodeURIComponent(id) + ")?$select=mp_name,mp_xmlformid,mp_lifecyclestatus";
    }
  };

  function byId(id) {
    return document.getElementById(id);
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function renderRecord(fields) {
    return '<div class="tacatdp-smoke__record">' + fields.map(function (field) {
      return '<div><span class="tacatdp-smoke__label">' + escapeHtml(field.label) + '</span>' +
        '<div class="tacatdp-smoke__value">' + escapeHtml(field.value || "-") + '</div></div>';
    }).join("") + '</div>';
  }

  function setStatus(message, state) {
    var el = byId("tacatdpSmokeStatus");
    if (!el) {
      return;
    }
    el.textContent = message;
    if (state) {
      el.setAttribute("data-state", state);
    } else {
      el.removeAttribute("data-state");
    }
  }

  function setHtml(id, html) {
    var target = byId(id);
    if (target) {
      target.innerHTML = html;
    }
  }

  function getJson(url) {
    return fetch(url, {
      method: "GET",
      credentials: "same-origin",
      headers: {
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
      }
    }).then(function (response) {
      if (!response.ok) {
        return response.text().then(function (body) {
          throw new Error(response.status + " " + response.statusText + ": " + body.slice(0, 500));
        });
      }
      return response.json();
    });
  }

  function renderAssignments(assignments) {
    if (!assignments.length) {
      setHtml("tacatdpAssignments", "<p>No assignments returned for this signed-in session.</p>");
      return;
    }
    setHtml("tacatdpAssignments", assignments.map(function (assignment) {
      return renderRecord([
        { label: "Assignment", value: assignment.mp_assignmentkey },
        { label: "User email", value: assignment.mp_useremail },
        { label: "Form version id", value: assignment._mp_formversion_value }
      ]);
    }).join(""));
  }

  function renderFormVersion(formVersion) {
    setHtml("tacatdpFormVersion", renderRecord([
      { label: "Version", value: formVersion.mp_version },
      { label: "Web Forms enabled", value: String(formVersion.mp_webformsenabled) },
      { label: "XForm XML bytes", value: String((formVersion.mp_xformxml || "").length) },
      { label: "Form id", value: formVersion._mp_form_value }
    ]));
  }

  function renderForm(form) {
    setHtml("tacatdpForm", renderRecord([
      { label: "Name", value: form.mp_name },
      { label: "XmlFormId", value: form.mp_xmlformid },
      { label: "Lifecycle", value: String(form.mp_lifecyclestatus || "") }
    ]));
  }

  function runSmokeTest() {
    setStatus("Checking Power Pages /_api access...", "");
    setHtml("tacatdpAssignments", "");
    setHtml("tacatdpFormVersion", "");
    setHtml("tacatdpForm", "");

    getJson(endpoints.assignments)
      .then(function (assignmentResponse) {
        var assignments = assignmentResponse.value || [];
        renderAssignments(assignments);
        if (!assignments.length || !assignments[0]._mp_formversion_value) {
          throw new Error("Assignments query succeeded, but no form version lookup was returned.");
        }
        return getJson(endpoints.formVersion(assignments[0]._mp_formversion_value));
      })
      .then(function (formVersion) {
        renderFormVersion(formVersion);
        if (!formVersion._mp_form_value) {
          throw new Error("Form version query succeeded, but no form lookup was returned.");
        }
        return getJson(endpoints.form(formVersion._mp_form_value));
      })
      .then(function (form) {
        renderForm(form);
        setStatus("Power Pages /_api read smoke test passed.", "ok");
      })
      .catch(function (error) {
        setStatus("Power Pages /_api read smoke test failed: " + error.message, "error");
      });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var button = byId("tacatdpSmokeRun");
    if (button) {
      button.addEventListener("click", runSmokeTest);
    }
    runSmokeTest();
  });
}());
