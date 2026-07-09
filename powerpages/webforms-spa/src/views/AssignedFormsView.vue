<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { PowerPagesApiClient } from '../powerpages-api/client';
import type { FormAssignmentSummary } from '../powerpages-api/types';
import { draftStore } from '../offline/drafts';

const api = new PowerPagesApiClient();
const loading = ref(false);
const error = ref('');
const assignments = ref<FormAssignmentSummary[]>([]);
const selectedAssignment = ref<FormAssignmentSummary | null>(null);
const draftCount = ref(0);

const hasAssignments = computed(() => assignments.value.length > 0);

async function loadAssignments() {
  loading.value = true;
  error.value = '';
  try {
    assignments.value = await api.listAssignedForms();
    selectedAssignment.value = assignments.value[0] ?? null;
    draftCount.value = await draftStore.count();
  } catch (caught) {
    error.value = caught instanceof Error ? caught.message : 'Unable to load assigned forms.';
  } finally {
    loading.value = false;
  }
}

onMounted(loadAssignments);
</script>

<template>
  <main class="app-shell" aria-labelledby="app-title">
    <header class="topbar">
      <div>
        <p class="eyebrow">TACATDP Monitoring Tool</p>
        <h1 id="app-title">Assigned forms</h1>
      </div>
      <button class="icon-button" type="button" :disabled="loading" aria-label="Refresh assigned forms" @click="loadAssignments">
        Refresh
      </button>
    </header>

    <section class="status-row" aria-live="polite">
      <span v-if="loading">Loading assignments...</span>
      <span v-else-if="error" class="error">{{ error }}</span>
      <span v-else>{{ assignments.length }} assigned form{{ assignments.length === 1 ? '' : 's' }}. {{ draftCount }} local draft{{ draftCount === 1 ? '' : 's' }}.</span>
    </section>

    <section v-if="hasAssignments" class="layout" aria-label="Assigned form workspace">
      <nav class="list" aria-label="Assigned forms">
        <button
          v-for="assignment in assignments"
          :key="assignment.assignmentId"
          class="list-item"
          :class="{ active: selectedAssignment?.assignmentId === assignment.assignmentId }"
          type="button"
          @click="selectedAssignment = assignment"
        >
          <span>{{ assignment.formName }}</span>
          <small>Version {{ assignment.version }}</small>
        </button>
      </nav>

      <article v-if="selectedAssignment" class="detail" aria-label="Selected form">
        <p class="eyebrow">Selected</p>
        <h2>{{ selectedAssignment.formName }}</h2>
        <dl>
          <div>
            <dt>Version</dt>
            <dd>{{ selectedAssignment.version }}</dd>
          </div>
          <div>
            <dt>XmlFormId</dt>
            <dd>{{ selectedAssignment.xmlFormId }}</dd>
          </div>
          <div>
            <dt>XForm XML</dt>
            <dd>{{ selectedAssignment.xformXml.length }} bytes loaded</dd>
          </div>
        </dl>
        <button class="primary-action" type="button" disabled>Render form after ODK package review</button>
      </article>
    </section>

    <section v-else-if="!loading && !error" class="empty-state" aria-label="No assigned forms">
      <h2>No assigned forms</h2>
      <p>No published form assignments were returned for this Power Pages session.</p>
    </section>
  </main>
</template>
