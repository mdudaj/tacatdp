<script setup lang="ts">
import { OdkWebForm, POST_SUBMIT__NEW_INSTANCE } from '@getodk/web-forms';
import {
  ArrowLeft,
  ChevronLeft,
  ChevronRight,
  Database,
  FilePenLine,
  FolderOpen,
  LogIn,
  Pencil,
  Plus,
  RefreshCw,
  Search,
} from '@lucide/vue';
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
import { draftStore, type LocalDraft } from '../offline/drafts';
import { PowerPagesApiClient } from '../powerpages-api/client';
import type { FormAssignmentSummary, SubmissionSummary } from '../powerpages-api/types';

type AppView = 'projects' | 'records' | 'runner';
type RecordTab = 'saved' | 'drafts';

interface ProjectWorkspace {
  id: string;
  name: string;
  description: string;
  assignments: FormAssignmentSummary[];
}

const api = new PowerPagesApiClient();
const pageSize = 10;
const loading = ref(false);
const authRequired = ref(false);
const error = ref('');
const assignments = ref<FormAssignmentSummary[]>([]);
const submissions = ref<SubmissionSummary[]>([]);
const localDrafts = ref<LocalDraft[]>([]);
const selectedProjectId = ref('');
const selectedAssignment = ref<FormAssignmentSummary | null>(null);
const selectedEditSubmission = ref<SubmissionSummary | null>(null);
const activeView = ref<AppView>('projects');
const activeRecordTab = ref<RecordTab>('saved');
const recordSearch = ref('');
const savedPage = ref(1);
const draftPage = ref(1);
const online = ref(typeof navigator === 'undefined' ? true : navigator.onLine);
const runtimeStatus = ref('');
const submitStatus = ref('');
const postSubmitMessage = ref('');
const postSubmitTone = ref<'success' | 'warning'>('success');
const submitTone = ref<'neutral' | 'success' | 'warning' | 'error'>('neutral');
const submitting = ref(false);
const buildMarker = 'always-visible-pagination-app-footer-20260712-001';
const previousBuildMarker = 'single-header-assignment-filter-20260711-001';
const crdbLogoUrl = '/CRDB_Bank_PLC.svg';
const currentYear = new Date().getFullYear();
const runtimeClickStatus = ref('No ODK runtime button click observed in this page load.');
const odkSubmitEventStatus = ref('No ODK submit event observed in this page load.');
const dataverseWriteStatus = ref('No Dataverse submit write attempted in this page load.');
let odkRuntimeObserver: MutationObserver | null = null;

const projectWorkspaces = computed<ProjectWorkspace[]>(() => {
  if (assignments.value.length === 0) {
    return [];
  }

  return [{
    id: 'tacatdp-impact-monitoring',
    name: 'TACATDP Impact Monitoring',
    description: 'Secure Microsoft-hosted monitoring workspace for assigned project data.',
    assignments: assignments.value,
  }];
});
const selectedProject = computed(() => projectWorkspaces.value.find((project) => project.id === selectedProjectId.value) ?? null);
const selectedProjectAssignments = computed(() => selectedProject.value?.assignments ?? []);
const primaryAssignment = computed(() => selectedProjectAssignments.value[0] ?? assignments.value[0] ?? null);
const draftCount = computed(() => localDrafts.value.length);
const savedCount = computed(() => submissions.value.length);
const filteredSavedSubmissions = computed(() => submissions.value.filter((submission) => matchesSearch([
  submission.instanceId,
  submission.displayName,
  submission.userEmail,
  submission.assignmentKey,
  submission.formVersionId,
  submission.xmlFormId,
  submission.versionNumber?.toString(),
  formatStatus(submission.lifecycleStatus),
  formatReviewState(submission.reviewState),
  formatDate(submission.updatedAt || submission.submittedAt),
])));
const filteredDrafts = computed(() => localDrafts.value.filter((draft) => matchesSearch([
  draft.id,
  draft.assignmentKey,
  draft.formVersionId,
  formatDate(draft.updatedAt),
])));
const filteredSavedCount = computed(() => filteredSavedSubmissions.value.length);
const filteredDraftCount = computed(() => filteredDrafts.value.length);
const activeRecordCount = computed(() => activeRecordTab.value === 'saved' ? filteredSavedCount.value : filteredDraftCount.value);
const activeRecordPage = computed(() => activeRecordTab.value === 'saved' ? savedPage.value : draftPage.value);
const activeTotalPages = computed(() => Math.max(1, Math.ceil(activeRecordCount.value / pageSize)));
const activePageStart = computed(() => activeRecordCount.value === 0 ? 0 : ((activeRecordPage.value - 1) * pageSize) + 1);
const activePageEnd = computed(() => Math.min(activeRecordPage.value * pageSize, activeRecordCount.value));
const visiblePageNumbers = computed(() => {
  const total = activeTotalPages.value;
  const current = activeRecordPage.value;
  const start = Math.max(1, current - 1);
  const end = Math.min(total, start + 2);
  const adjustedStart = Math.max(1, end - 2);
  return Array.from({ length: end - adjustedStart + 1 }, (_, index) => adjustedStart + index);
});
const pagedSavedSubmissions = computed(() => paginate(filteredSavedSubmissions.value, savedPage.value));
const pagedDrafts = computed(() => paginate(filteredDrafts.value, draftPage.value));
const selectedVersionLabel = computed(() => {
  if (!selectedAssignment.value) {
    return '';
  }
  return `${selectedAssignment.value.formName} v${selectedAssignment.value.version}`;
});
const runnerTitle = computed(() => selectedEditSubmission.value ? 'Edit record' : 'Form');
const runnerSubtitle = computed(() => {
  if (!selectedAssignment.value) {
    return '';
  }

  const base = `Version ${selectedAssignment.value.version} · ${selectedAssignment.value.xmlFormId} · ${online.value ? 'Online' : 'Offline'}`;
  if (!selectedEditSubmission.value) {
    return base;
  }

  return `${base} · Editing ${selectedEditSubmission.value.displayName || selectedEditSubmission.value.instanceId}`;
});
const editInstanceOptions = computed(() => {
  const submission = selectedEditSubmission.value;
  if (!submission) {
    return null;
  }

  return {
    resolveInstance: () => api.getLatestSubmissionXml(submission.instanceId),
    attachmentFileNames: [] as string[],
    resolveAttachment: async (fileName: string) => {
      throw new Error(`Attachment edit loading is not enabled for ${fileName}.`);
    },
  };
});

function paginate<T>(records: T[], page: number): T[] {
  const start = (page - 1) * pageSize;
  return records.slice(start, start + pageSize);
}

function formatDate(value?: string): string {
  if (!value) {
    return 'Not recorded';
  }
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value));
}

function formatStatus(value?: number): string {
  if (value === 100000001) {
    return 'Submitted';
  }
  if (value === 100000000) {
    return 'Draft';
  }
  return value == null ? 'Submitted' : `Status ${value}`;
}

function formatReviewState(value?: number): string {
  if (value === 100000000) {
    return 'Received';
  }
  return value == null ? 'Received' : `Review ${value}`;
}

function matchesSearch(values: Array<string | undefined>): boolean {
  const query = recordSearch.value.trim().toLowerCase();
  if (!query) {
    return true;
  }

  return values.some((value) => value?.toLowerCase().includes(query));
}

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
  runtimeStatus.value = selectedEditSubmission.value
    ? 'Initializing ODK Web Forms edit session...'
    : 'Initializing ODK Web Forms runtime...';
  submitStatus.value = '';
  submitTone.value = 'neutral';
  runtimeClickStatus.value = 'No ODK runtime button click observed for this selected form.';
  odkSubmitEventStatus.value = 'No ODK submit event observed for this selected form.';
  dataverseWriteStatus.value = 'No Dataverse submit write attempted for this selected form.';
  selectedAssignment.value = assignment;
}

function openProject(project: ProjectWorkspace) {
  selectedProjectId.value = project.id;
  postSubmitMessage.value = '';
  activeView.value = 'records';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function backToProjects() {
  postSubmitMessage.value = '';
  activeView.value = 'projects';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function openRunner(assignment = primaryAssignment.value) {
  if (!assignment) {
    error.value = 'No assigned form is available for this project.';
    return;
  }
  selectedEditSubmission.value = null;
  postSubmitMessage.value = '';
  resetRuntimeDiagnostics(assignment);
  activeView.value = 'runner';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function openSavedSubmission(submission: SubmissionSummary) {
  loading.value = true;
  error.value = '';
  postSubmitMessage.value = '';
  try {
    selectedEditSubmission.value = submission;
    const context = await api.getSubmissionFormContext(submission);
    resetRuntimeDiagnostics(context);
    activeView.value = 'runner';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } catch (caught) {
    selectedEditSubmission.value = null;
    error.value = caught instanceof Error ? caught.message : 'Unable to open saved record for editing.';
  } finally {
    loading.value = false;
  }
}

function backToRecords() {
  activeView.value = selectedProject.value ? 'records' : 'projects';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function selectTab(tab: RecordTab) {
  activeRecordTab.value = tab;
  clampActivePage();
}

function changePage(direction: -1 | 1) {
  setActivePage(activeRecordPage.value + direction);
}

function setActivePage(page: number) {
  const nextPage = Math.min(Math.max(1, page), activeTotalPages.value);
  if (activeRecordTab.value === 'saved') {
    savedPage.value = nextPage;
    return;
  }
  draftPage.value = nextPage;
}

function clampActivePage() {
  setActivePage(activeRecordPage.value);
}

function handleOnline() {
  online.value = true;
}

function handleOffline() {
  online.value = false;
}

async function refreshLocalDrafts() {
  localDrafts.value = await draftStore.list();
}

function handleFormLoaded() {
  if (!selectedAssignment.value) {
    return;
  }

  runtimeStatus.value = selectedEditSubmission.value
    ? 'ODK Web Forms edit session loaded. Submit saves a new version for this record.'
    : 'ODK Web Forms runtime loaded. Complete the form and submit online; editable local draft restore is the next slice.';
  relabelOdkSubmitButton();
}

async function handleSubmit(payload: unknown, callback?: (result: unknown) => void) {
  if (!selectedAssignment.value) {
    submitStatus.value = 'Select an assigned form before submitting.';
    submitTone.value = 'warning';
    return;
  }

  submitting.value = true;
  postSubmitMessage.value = '';
  const candidate = payload as { status?: string; violations?: unknown };
  const violationCount = Array.isArray(candidate.violations) ? candidate.violations.length : 'unknown';
  odkSubmitEventStatus.value = `${new Date().toLocaleTimeString()} - ODK submit event received; payload status ${candidate.status ?? 'unknown'}, violations ${violationCount}.`;
  dataverseWriteStatus.value = `${new Date().toLocaleTimeString()} - Starting Dataverse submit write.`;
  submitStatus.value = 'Submitting to Dataverse...';
  submitTone.value = 'neutral';
  try {
    const result = await api.submitOdkSubmission(selectedAssignment.value, payload, {
      existingSubmission: selectedEditSubmission.value,
    });
    dataverseWriteStatus.value = `${new Date().toLocaleTimeString()} - Dataverse submit write completed.`;
    const attachmentSummary = `${result.attachmentCount} attachment record${result.attachmentCount === 1 ? '' : 's'}, ${result.attachmentBinaryUploadCount} binary upload${result.attachmentBinaryUploadCount === 1 ? '' : 's'}`;
    const warningSummary = result.attachmentWarnings.length > 0 ? ` Attachment warning: ${result.attachmentWarnings.join(' ')}` : '';
    submitStatus.value = `Submitted to Dataverse. ${result.displayName || result.instanceId}, version ${result.versionNumber}; ${attachmentSummary}.${warningSummary}`;
    submitTone.value = result.attachmentWarnings.length > 0 ? 'warning' : 'success';
    submissions.value = await api.listSavedSubmissions();
    callback?.(selectedEditSubmission.value ? {} : { next: POST_SUBMIT__NEW_INSTANCE });
    activeRecordTab.value = 'saved';
    savedPage.value = 1;
    selectedEditSubmission.value = null;
    activeView.value = selectedProject.value ? 'records' : 'projects';
    postSubmitTone.value = result.attachmentWarnings.length > 0 ? 'warning' : 'success';
    postSubmitMessage.value = submitStatus.value;
    submitStatus.value = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } catch (caught) {
    dataverseWriteStatus.value = `${new Date().toLocaleTimeString()} - Dataverse submit write failed.`;
    submitStatus.value = caught instanceof Error ? `Submit failed: ${caught.message}` : 'Submit failed.';
    submitTone.value = 'error';
  } finally {
    submitting.value = false;
  }
}

async function loadWorkspace() {
  if (!api.hasPowerPagesSession()) {
    authRequired.value = true;
    error.value = '';
    window.location.assign(api.getSignInUrl());
    return;
  }

  loading.value = true;
  error.value = '';
  authRequired.value = false;
  try {
    const [nextAssignments, nextSubmissions] = await Promise.all([
      api.listAssignedForms(),
      api.listSavedSubmissions(),
      refreshLocalDrafts(),
    ]);
    assignments.value = nextAssignments;
    submissions.value = nextSubmissions;
    selectedAssignment.value = assignments.value[0] ?? null;
    selectedEditSubmission.value = null;
    if (!selectedProjectId.value && projectWorkspaces.value[0]) {
      selectedProjectId.value = projectWorkspaces.value[0].id;
    }
    savedPage.value = 1;
    draftPage.value = 1;
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
  } catch (caught) {
    const message = caught instanceof Error ? caught.message : 'Unable to load workspace.';
    if ((message.includes('401') || message.includes('403')) && !api.hasPowerPagesSession()) {
      authRequired.value = true;
      window.location.assign(api.getSignInUrl());
      return;
    }
    error.value = message;
  } finally {
    loading.value = false;
  }
}

watch(recordSearch, () => {
  savedPage.value = 1;
  draftPage.value = 1;
});

watch([filteredSavedCount, filteredDraftCount, activeRecordTab], () => {
  clampActivePage();
});

onMounted(() => {
  document.addEventListener('submit', preventPowerPagesFormSubmit, true);
  document.addEventListener('click', preventRuntimeButtonDefault, true);
  window.addEventListener('online', handleOnline);
  window.addEventListener('offline', handleOffline);
  odkRuntimeObserver = new MutationObserver(relabelOdkSubmitButton);
  odkRuntimeObserver.observe(document.body, { childList: true, subtree: true });
  void loadWorkspace();
});

onUnmounted(() => {
  document.removeEventListener('submit', preventPowerPagesFormSubmit, true);
  document.removeEventListener('click', preventRuntimeButtonDefault, true);
  window.removeEventListener('online', handleOnline);
  window.removeEventListener('offline', handleOffline);
  odkRuntimeObserver?.disconnect();
  odkRuntimeObserver = null;
});
</script>

<template>
  <main class="monitoring-shell" aria-labelledby="app-title">
    <section v-if="authRequired" class="auth-panel" aria-labelledby="auth-title">
      <h1 id="auth-title">Sign in required</h1>
      <p>Use your Microsoft account to continue to Monitoring Tool.</p>
      <a class="primary-action" :href="api.getSignInUrl()">
        <LogIn class="action-icon" aria-hidden="true" />
        Sign in with Microsoft
      </a>
    </section>

    <template v-else-if="activeView === 'projects'">
      <section class="hero-panel hero-panel--compact" aria-labelledby="app-title">
        <div>
          <p class="eyebrow">Monitoring workspace</p>
          <h1 id="app-title">Projects</h1>
          <p class="hero-copy">Open a project to review all submitted records, search saved work, or add a new submission.</p>
        </div>
        <div class="hero-actions">
          <button class="icon-action icon-action--secondary" type="button" :disabled="loading" aria-label="Refresh projects" @click="loadWorkspace">
            <RefreshCw class="action-icon" aria-hidden="true" />
            Refresh
          </button>
        </div>
      </section>

      <section v-if="loading" class="loading-panel" aria-live="polite" aria-label="Loading projects">
        <img class="loading-logo" :src="crdbLogoUrl" alt="CRDB Bank">
        <h2>Loading projects</h2>
        <p>Preparing the secure workspace</p>
        <span class="loading-dots" aria-hidden="true"><i></i><i></i><i></i></span>
      </section>

      <section v-else class="status-grid" aria-label="Workspace summary">
        <article class="metric-card metric-card--accent">
          <span class="metric-value">{{ projectWorkspaces.length }}</span>
          <span class="metric-label">Projects</span>
        </article>
        <article class="metric-card">
          <span class="metric-value">{{ savedCount }}</span>
          <span class="metric-label">Saved records</span>
        </article>
        <article class="metric-card">
          <span class="metric-value">{{ online ? 'Online' : 'Offline' }}</span>
          <span class="metric-label">Connection</span>
        </article>
      </section>

      <section v-if="error" class="status-banner status-banner--error" aria-live="polite">
        {{ error }}
      </section>

      <section v-if="projectWorkspaces.length > 0" class="project-list" aria-label="Available projects">
        <article
          v-for="project in projectWorkspaces"
          :key="project.id"
          class="project-card project-card--entry"
        >
          <div>
            <p class="eyebrow">Project</p>
            <h2>{{ project.name }}</h2>
            <p>{{ project.description }}</p>
            <dl class="compact-facts">
              <div>
                <dt>Forms</dt>
                <dd>{{ project.assignments.length }}</dd>
              </div>
              <div>
                <dt>Local drafts</dt>
                <dd>{{ draftCount }}</dd>
              </div>
            </dl>
          </div>
          <button class="icon-action" type="button" :aria-label="`Open ${project.name}`" @click="openProject(project)">
            <FolderOpen class="action-icon" aria-hidden="true" />
            Open
          </button>
        </article>
      </section>

      <section v-else-if="!loading && !error" class="empty-state" aria-label="No projects">
        <h2>No projects</h2>
        <p>No project assignments were returned for this Power Pages session.</p>
      </section>
    </template>

    <template v-else-if="activeView === 'records'">
      <nav class="top-action-bar" aria-label="Project actions">
        <button class="icon-action icon-action--secondary" type="button" aria-label="Back to projects" @click="backToProjects">
          <ArrowLeft class="action-icon" aria-hidden="true" />
          Back
        </button>
        <div class="top-action-title">
          <span class="eyebrow">Project</span>
          <h1>{{ selectedProject?.name }}</h1>
          <p>{{ online ? 'Online' : 'Offline' }} · {{ savedCount }} submitted · {{ draftCount }} local draft{{ draftCount === 1 ? '' : 's' }}</p>
        </div>
        <button class="icon-action" type="button" :disabled="!primaryAssignment" aria-label="Add new record" @click="openRunner()">
          <Plus class="action-icon" aria-hidden="true" />
          Add new
        </button>
      </nav>

      <section v-if="error" class="status-banner status-banner--error" aria-live="polite">
        {{ error }}
      </section>

      <section v-if="postSubmitMessage" class="status-banner" :class="`status-banner--${postSubmitTone}`" aria-live="polite">
        {{ postSubmitMessage }}
      </section>

      <section class="record-workspace" aria-label="Project records">
        <div class="record-toolbar">
          <div class="record-tabs" role="tablist" aria-label="Record views">
            <button
              class="record-tab"
              :class="{ 'record-tab--active': activeRecordTab === 'saved' }"
              type="button"
              role="tab"
              :aria-selected="activeRecordTab === 'saved'"
              @click="selectTab('saved')"
            >
              <Database class="action-icon" aria-hidden="true" />
              Saved
              <span class="tab-count">{{ filteredSavedCount }}</span>
            </button>
            <button
              class="record-tab"
              :class="{ 'record-tab--active': activeRecordTab === 'drafts' }"
              type="button"
              role="tab"
              :aria-selected="activeRecordTab === 'drafts'"
              @click="selectTab('drafts')"
            >
              <FilePenLine class="action-icon" aria-hidden="true" />
              Drafts
              <span class="tab-count">{{ filteredDraftCount }}</span>
            </button>
          </div>
          <label class="record-search">
            <Search class="record-search__icon" aria-hidden="true" />
            <span class="sr-only">Search records</span>
            <input
              v-model="recordSearch"
              type="search"
              autocomplete="off"
              placeholder="Search records"
              aria-label="Search saved records and drafts"
            >
          </label>
        </div>

        <section v-if="activeRecordTab === 'saved'" class="record-list" role="tabpanel" aria-label="Saved records">
          <article
            v-for="submission in pagedSavedSubmissions"
            :key="submission.submissionId"
            class="data-card"
          >
            <div>
              <p class="eyebrow">Saved record</p>
              <h2>{{ submission.displayName || submission.instanceId }}</h2>
              <p class="form-meta">
                {{ submission.userEmail || 'Unknown owner' }} · Version {{ submission.versionNumber || 1 }} · Updated {{ formatDate(submission.updatedAt || submission.submittedAt) }}
              </p>
            </div>
            <div class="data-card__actions">
              <span class="state-chip">{{ formatStatus(submission.lifecycleStatus) }}</span>
              <button class="icon-action icon-action--secondary" type="button" :disabled="loading" @click="openSavedSubmission(submission)">
                <Pencil class="action-icon" aria-hidden="true" />
                Edit
              </button>
            </div>
          </article>
          <section v-if="savedCount === 0" class="empty-state empty-state--inline" aria-label="No saved records">
            <h2>No saved records</h2>
            <p>Add a new record, submit it online, then return here to review it.</p>
          </section>
          <section v-else-if="filteredSavedCount === 0" class="empty-state empty-state--inline" aria-label="No matching saved records">
            <h2>No matching saved records</h2>
            <p>Adjust the search text to find submitted records by instance, owner, form, status, or date.</p>
          </section>
        </section>

        <section v-else class="record-list" role="tabpanel" aria-label="Local drafts">
          <article
            v-for="draft in pagedDrafts"
            :key="draft.id"
            class="data-card data-card--draft"
          >
            <div>
              <p class="eyebrow">Local draft</p>
              <h2>{{ draft.assignmentKey }}</h2>
              <p class="form-meta">Updated {{ formatDate(draft.updatedAt) }}</p>
            </div>
            <div class="data-card__actions">
              <span class="state-chip state-chip--draft">Local</span>
              <button class="icon-action icon-action--secondary" type="button" @click="openRunner()">
                <FolderOpen class="action-icon" aria-hidden="true" />
                Open
              </button>
            </div>
          </article>
          <section v-if="draftCount === 0" class="empty-state empty-state--inline" aria-label="No local drafts">
            <h2>No local drafts</h2>
            <p>Editable local draft save and restore is not enabled yet. Use Add new to capture and submit online.</p>
          </section>
          <section v-else-if="filteredDraftCount === 0" class="empty-state empty-state--inline" aria-label="No matching local drafts">
            <h2>No matching local drafts</h2>
            <p>Adjust the search text to find local drafts.</p>
          </section>
        </section>

        <nav class="pagination-bar" aria-label="Record pagination">
          <p class="pagination-summary">
            Showing {{ activePageStart }}-{{ activePageEnd }} of {{ activeRecordCount }}
          </p>
          <div class="pagination-controls">
            <button
              class="pagination-button pagination-button--icon"
              type="button"
              :disabled="activeRecordPage <= 1"
              aria-label="Previous page"
              @click="changePage(-1)"
            >
              <ChevronLeft class="action-icon" aria-hidden="true" />
            </button>
            <button
              v-for="pageNumber in visiblePageNumbers"
              :key="pageNumber"
              class="pagination-button"
              :class="{ 'pagination-button--active': pageNumber === activeRecordPage }"
              type="button"
              :aria-current="pageNumber === activeRecordPage ? 'page' : undefined"
              :aria-label="`Page ${pageNumber}`"
              @click="setActivePage(pageNumber)"
            >
              {{ pageNumber }}
            </button>
            <button
              class="pagination-button pagination-button--icon"
              type="button"
              :disabled="activeRecordPage >= activeTotalPages"
              aria-label="Next page"
              @click="changePage(1)"
            >
              <ChevronRight class="action-icon" aria-hidden="true" />
            </button>
          </div>
          <p class="pagination-page-count">
            Page {{ activeRecordPage }} of {{ activeTotalPages }}
          </p>
        </nav>
      </section>
    </template>

    <template v-else>
      <section v-if="submitting" class="submit-overlay" aria-live="assertive" aria-label="Submitting record">
        <div class="submit-progress-panel" role="status">
          <img class="loading-logo" :src="crdbLogoUrl" alt="CRDB Bank">
          <h2>Submitting record</h2>
          <p>Saving to Dataverse</p>
          <span class="loading-dots" aria-hidden="true"><i></i><i></i><i></i></span>
        </div>
      </section>

      <nav class="top-action-bar" aria-label="Form actions">
        <button class="icon-action icon-action--secondary" type="button" aria-label="Back to project records" @click="backToRecords">
          <ArrowLeft class="action-icon" aria-hidden="true" />
          Back
        </button>
        <div class="top-action-title">
          <span class="eyebrow">{{ runnerTitle }}</span>
          <h1>{{ selectedAssignment?.formName }}</h1>
          <p v-if="selectedAssignment">{{ runnerSubtitle }}</p>
        </div>
        <button class="icon-action icon-action--secondary" type="button" :disabled="loading" aria-label="Refresh workspace" @click="loadWorkspace">
          <RefreshCw class="action-icon" aria-hidden="true" />
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
            :key="`${selectedAssignment.formVersionId}:${selectedEditSubmission?.submissionId || 'new'}`"
            :form-xml="selectedAssignment.xformXml"
            :edit-instance="editInstanceOptions"
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

    <footer class="app-footer" aria-label="Application footer">
      CRDB @{{ currentYear }}
    </footer>
  </main>
</template>
