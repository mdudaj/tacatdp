<script setup lang="ts">
import { OdkWebForm, POST_SUBMIT__NEW_INSTANCE } from '@getodk/web-forms';
import { computed, onMounted, onUnmounted, ref } from 'vue';
import crdbLogoUrl from '../../../../assets/images/CRDB_Bank_PLC.svg';
import { draftStore } from '../offline/drafts';
import { PowerPagesApiClient } from '../powerpages-api/client';
import type { FormAssignmentSummary } from '../powerpages-api/types';

type AppView = 'workQueue' | 'runner';

const api = new PowerPagesApiClient();
const loading = ref(false);
const authRequired = ref(false);
const error = ref('');
const assignments = ref<FormAssignmentSummary[]>([]);
const selectedAssignment = ref<FormAssignmentSummary | null>(null);
const draftCount = ref(0);
const activeView = ref<AppView>('workQueue');
const runtimeStatus = ref('');
const submitStatus = ref('');
const submitTone = ref<'neutral' | 'success' | 'warning' | 'error'>('neutral');
const buildMarker = 'monitoring-tool-ux-foundation-20260711-001';
const previousBuildMarker = 'renderer-spacing-submit-label-20260711-001';
const runtimeClickStatus = ref('No ODK runtime button click observed in this page load.');
const odkSubmitEventStatus = ref('No ODK submit event observed in this page load.');
const dataverseWriteStatus = ref('No Dataverse submit write attempted in this page load.');
let odkRuntimeObserver: MutationObserver | null = null;

const hasAssignments = computed(() => assignments.value.length > 0);
const signedInUserEmail = computed(() => assignments.value.find((assignment) => assignment.userEmail)?.userEmail ?? 'Signed in');
const selectedDraftId = computed(() => {
  if (!selectedAssignment.value) {
    return '';
  }
  return `assignment:${selectedAssignment.value.assignmentId}:form-version:${selectedAssignment.value.formVersionId}`;
});
const selectedVersionLabel = computed(() => {
  if (!selectedAssignment.value) {
    return '';
  }
  return `${selectedAssignment.value.formName} v${selectedAssignment.value.version}`;
});

function isInsideOdkRuntime(target: EventTarget | null): boolean {
  return target instanceof Element && Boolean(target.closest('.odk-runtime-host'));
}

function preventPowerPagesFormSubmit(event: Event) {
  if (isInsideOdkRuntime(event.target)) {
    event.preventDefault();
  }
}

function preventRuntimeButtonDefault(event: MouseEvent) {
  const target = event.target;
  if (!(target instanceof Element)) {
    return;
  }

  const button = target.closest('button');
  if (button && button.closest('.odk-runtime-host')) {
    const label = button.textContent?.replace(/\s+/g, ' ').trim() || 'ODK runtime button';
    runtimeClickStatus.value = `${new Date().toLocaleTimeString()} - ${label} click captured by host boundary.`;
    event.preventDefault();
  }
}

function relabelOdkSubmitButton() {
  const submitButtons = document.querySelectorAll<HTMLButtonElement>('.odk-runtime-host .footer button');
  submitButtons.forEach((button) => {
    if (button.textContent?.replace(/\s+/g, ' ').trim() !== 'Send') {
      return;
    }

    const label = button.querySelector<HTMLElement>('.p-button-label') ?? button;
    label.textContent = 'Submit';
    button.setAttribute('aria-label', 'Submit');
  });
}

function resetRuntimeDiagnostics(assignment: FormAssignmentSummary) {
  runtimeStatus.value = 'Initializing ODK Web Forms runtime...';
  submitStatus.value = '';
  submitTone.value = 'neutral';
  runtimeClickStatus.value = 'No ODK runtime button click observed for this selected form.';
  odkSubmitEventStatus.value = 'No ODK submit event observed for this selected form.';
  dataverseWriteStatus.value = 'No Dataverse submit write attempted for this selected form.';
  selectedAssignment.value = assignment;
}

function openRunner(assignment: FormAssignmentSummary) {
  resetRuntimeDiagnostics(assignment);
  activeView.value = 'runner';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function backToWorkQueue() {
  activeView.value = 'workQueue';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function handleFormLoaded() {
  if (!selectedAssignment.value || !selectedDraftId.value) {
    return;
  }

  await draftStore.save({
    id: selectedDraftId.value,
    assignmentKey: selectedAssignment.value.assignmentKey,
    formVersionId: selectedAssignment.value.formVersionId,
    updatedAt: new Date().toISOString(),
    payload: {
      status: 'RuntimeLoaded',
      xmlFormId: selectedAssignment.value.xmlFormId,
      version: selectedAssignment.value.version,
    },
  });
  draftCount.value = await draftStore.count();
  runtimeStatus.value = 'ODK Web Forms runtime loaded. Local runtime marker saved.';
  relabelOdkSubmitButton();
}

async function handleSubmit(payload: unknown, callback?: (result: unknown) => void) {
  if (!selectedAssignment.value) {
    submitStatus.value = 'Select an assigned form before submitting.';
    submitTone.value = 'warning';
    return;
  }

  const candidate = payload as { status?: string; violations?: unknown };
  const violationCount = Array.isArray(candidate.violations) ? candidate.violations.length : 'unknown';
  odkSubmitEventStatus.value = `${new Date().toLocaleTimeString()} - ODK submit event received; payload status ${candidate.status ?? 'unknown'}, violations ${violationCount}.`;
  dataverseWriteStatus.value = `${new Date().toLocaleTimeString()} - Starting Dataverse submit write.`;
  submitStatus.value = 'Submitting to Dataverse...';
  submitTone.value = 'neutral';
  try {
    const result = await api.submitOdkSubmission(selectedAssignment.value, payload);
    dataverseWriteStatus.value = `${new Date().toLocaleTimeString()} - Dataverse submit write completed.`;
    const attachmentSummary = `${result.attachmentCount} attachment record${result.attachmentCount === 1 ? '' : 's'}, ${result.attachmentBinaryUploadCount} binary upload${result.attachmentBinaryUploadCount === 1 ? '' : 's'}`;
    const warningSummary = result.attachmentWarnings.length > 0 ? ` Attachment warning: ${result.attachmentWarnings.join(' ')}` : '';
    submitStatus.value = `Submitted to Dataverse. Instance ${result.instanceId}, version ${result.versionNumber}; ${attachmentSummary}.${warningSummary}`;
    submitTone.value = result.attachmentWarnings.length > 0 ? 'warning' : 'success';
    callback?.({ next: POST_SUBMIT__NEW_INSTANCE });
  } catch (caught) {
    dataverseWriteStatus.value = `${new Date().toLocaleTimeString()} - Dataverse submit write failed.`;
    submitStatus.value = caught instanceof Error ? `Submit failed: ${caught.message}` : 'Submit failed.';
    submitTone.value = 'error';
  }
}

async function loadAssignments() {
  if (!api.hasPowerPagesSession()) {
    authRequired.value = true;
    window.location.assign(api.getSignInUrl());
    return;
  }

  loading.value = true;
  error.value = '';
  authRequired.value = false;
  try {
    assignments.value = await api.listAssignedForms();
    selectedAssignment.value = assignments.value[0] ?? null;
    runtimeStatus.value = selectedAssignment.value ? 'Initializing ODK Web Forms runtime...' : '';
    submitStatus.value = '';
    submitTone.value = 'neutral';
    runtimeClickStatus.value = selectedAssignment.value
      ? 'No ODK runtime button click observed for this selected form.'
      : 'No assigned form selected.';
    odkSubmitEventStatus.value = selectedAssignment.value
      ? 'No ODK submit event observed for this selected form.'
      : 'No assigned form selected.';
    dataverseWriteStatus.value = selectedAssignment.value
      ? 'No Dataverse submit write attempted for this selected form.'
      : 'No assigned form selected.';
    draftCount.value = await draftStore.count();
  } catch (caught) {
    error.value = caught instanceof Error ? caught.message : 'Unable to load assigned forms.';
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  document.addEventListener('submit', preventPowerPagesFormSubmit, true);
  document.addEventListener('click', preventRuntimeButtonDefault, true);
  odkRuntimeObserver = new MutationObserver(relabelOdkSubmitButton);
  odkRuntimeObserver.observe(document.body, { childList: true, subtree: true });
  void loadAssignments();
});

onUnmounted(() => {
  document.removeEventListener('submit', preventPowerPagesFormSubmit, true);
  document.removeEventListener('click', preventRuntimeButtonDefault, true);
  odkRuntimeObserver?.disconnect();
  odkRuntimeObserver = null;
});
</script>

<template>
  <main class="monitoring-shell" aria-labelledby="app-title">
    <header class="app-header">
      <a class="brand-lockup" href="/" aria-label="Monitoring Tool home">
        <img class="brand-logo" :src="crdbLogoUrl" alt="CRDB Bank" />
        <span class="brand-divider" aria-hidden="true"></span>
        <span class="brand-product">Monitoring Tool</span>
      </a>
      <div class="session-summary" aria-label="Signed in user">
        <span class="session-label">Signed in</span>
        <strong>{{ signedInUserEmail }}</strong>
      </div>
    </header>

    <section v-if="authRequired" class="auth-panel" aria-labelledby="auth-title">
      <img class="loading-logo" :src="crdbLogoUrl" alt="CRDB Bank" />
      <h1 id="auth-title">Sign in required</h1>
      <p>Use your Microsoft account to continue to Monitoring Tool.</p>
      <a class="primary-action" :href="api.getSignInUrl()">Sign in with Microsoft</a>
    </section>

    <template v-else-if="activeView === 'workQueue'">
      <section class="hero-panel" aria-labelledby="app-title">
        <div>
          <p class="eyebrow">Field monitoring workspace</p>
          <h1 id="app-title">Assigned work</h1>
          <p class="hero-copy">Start a form, continue local work, or review your recent submission status.</p>
        </div>
        <div class="hero-actions">
          <button class="secondary-action" type="button" :disabled="loading" @click="loadAssignments">
            Refresh
          </button>
        </div>
      </section>

      <section v-if="loading" class="loading-panel" aria-live="polite" aria-label="Loading assignments">
        <img class="loading-logo" :src="crdbLogoUrl" alt="CRDB Bank" />
        <h2>Loading work queue</h2>
        <p>Preparing the secure form session</p>
        <span class="loading-dots" aria-hidden="true"><i></i><i></i><i></i></span>
      </section>

      <section v-else class="status-grid" aria-label="Workspace summary">
        <article class="metric-card">
          <span class="metric-value">{{ assignments.length }}</span>
          <span class="metric-label">Assigned forms</span>
        </article>
        <article class="metric-card">
          <span class="metric-value">{{ draftCount }}</span>
          <span class="metric-label">Local drafts</span>
        </article>
        <article class="metric-card">
          <span class="metric-value">Online</span>
          <span class="metric-label">Power Pages session</span>
        </article>
      </section>

      <section v-if="error" class="status-banner status-banner--error" aria-live="polite">
        {{ error }}
      </section>

      <section v-if="hasAssignments" class="workspace-grid" aria-label="Assigned projects and forms">
        <article class="project-card">
          <p class="eyebrow">Project</p>
          <h2>TACATDP Impact Monitoring</h2>
          <p>Secure Microsoft-hosted monitoring workspace for assigned project forms.</p>
          <dl class="compact-facts">
            <div>
              <dt>Assigned forms</dt>
              <dd>{{ assignments.length }}</dd>
            </div>
            <div>
              <dt>Local drafts</dt>
              <dd>{{ draftCount }}</dd>
            </div>
          </dl>
        </article>

        <div class="form-list" aria-label="Assigned forms">
          <article
            v-for="assignment in assignments"
            :key="assignment.assignmentId"
            class="form-card"
          >
            <div>
              <p class="eyebrow">Form</p>
              <h3>{{ assignment.formName }}</h3>
              <p class="form-meta">Version {{ assignment.version }} · {{ assignment.xmlFormId }}</p>
            </div>
            <div class="form-card__footer">
              <span class="state-chip">Published</span>
              <button class="primary-action" type="button" @click="openRunner(assignment)">
                Start form
              </button>
            </div>
          </article>
        </div>
      </section>

      <section v-else-if="!loading && !error" class="empty-state" aria-label="No assigned forms">
        <h2>No assigned forms</h2>
        <p>No published form assignments were returned for this Power Pages session.</p>
      </section>
    </template>

    <template v-else>
      <nav class="top-action-bar" aria-label="Form actions">
        <button class="back-action" type="button" @click="backToWorkQueue">
          Back to assigned work
        </button>
        <div class="top-action-title">
          <span class="eyebrow">Form runner</span>
          <h1>{{ selectedAssignment?.formName }}</h1>
          <p v-if="selectedAssignment">Version {{ selectedAssignment.version }} · {{ selectedAssignment.xmlFormId }}</p>
        </div>
        <button class="secondary-action" type="button" :disabled="loading" @click="loadAssignments">
          Refresh
        </button>
      </nav>

      <section v-if="runtimeStatus || submitStatus" class="runner-status-stack" aria-live="polite">
        <p v-if="runtimeStatus" class="status-banner status-banner--success">{{ runtimeStatus }}</p>
        <p v-if="submitStatus" class="status-banner" :class="`status-banner--${submitTone}`">{{ submitStatus }}</p>
      </section>

      <section v-if="selectedAssignment" class="runner-shell" :aria-label="selectedVersionLabel">
        <section class="odk-runtime-host" aria-label="ODK Web Forms runtime">
          <OdkWebForm
            :key="selectedAssignment.formVersionId"
            :form-xml="selectedAssignment.xformXml"
            device-id="tacatdp-powerpages-poc"
            missing-resource-behavior="placeholder"
            @loaded="handleFormLoaded"
            @submit="handleSubmit"
            @submit-chunked="handleSubmit"
          />
        </section>

        <details class="debug-panel">
          <summary>Technical diagnostics</summary>
          <div class="debug-grid">
            <p>Build {{ buildMarker }}</p>
            <p>Previous renderer marker {{ previousBuildMarker }}</p>
            <p>{{ selectedAssignment.xformXml.length }} bytes of XForm XML loaded.</p>
            <p>Last runtime click: {{ runtimeClickStatus }}</p>
            <p>Last ODK submit event: {{ odkSubmitEventStatus }}</p>
            <p>Last Dataverse write: {{ dataverseWriteStatus }}</p>
          </div>
        </details>
      </section>
    </template>
  </main>
</template>
