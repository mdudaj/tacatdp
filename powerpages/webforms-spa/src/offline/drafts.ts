export interface LocalDraft {
  id: string;
  assignmentKey: string;
  formVersionId: string;
  updatedAt: string;
  payload: unknown;
}

class DraftStore {
  private readonly databaseName = 'tacatdp-webforms';
  private readonly storeName = 'drafts';

  async count(): Promise<number> {
    return (await this.list()).length;
  }

  async save(draft: LocalDraft): Promise<void> {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, 'readwrite');
      tx.objectStore(this.storeName).put(draft);
      tx.oncomplete = () => {
        db.close();
        resolve();
      };
      tx.onerror = () => reject(tx.error ?? new Error('Unable to save draft.'));
    });
  }

  async get(id: string): Promise<LocalDraft | undefined> {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, 'readonly');
      const request = tx.objectStore(this.storeName).get(id);
      request.onsuccess = () => {
        const draft = request.result as LocalDraft | undefined;
        resolve(draft && this.isRestorableDraft(draft) ? draft : undefined);
      };
      request.onerror = () => reject(request.error ?? new Error('Unable to load draft.'));
      tx.oncomplete = () => db.close();
    });
  }

  async list(): Promise<LocalDraft[]> {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, 'readonly');
      const request = tx.objectStore(this.storeName).getAll();
      request.onsuccess = () => {
        const drafts = (request.result as LocalDraft[])
          .filter((draft) => this.isRestorableDraft(draft))
          .sort((left, right) => right.updatedAt.localeCompare(left.updatedAt));
        resolve(drafts);
      };
      request.onerror = () => reject(request.error ?? new Error('Unable to list drafts.'));
      tx.oncomplete = () => db.close();
    });
  }

  private async open(): Promise<IDBDatabase> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.databaseName, 1);
      request.onupgradeneeded = () => {
        const db = request.result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: 'id' });
        }
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error ?? new Error('Unable to open draft database.'));
    });
  }

  private isRestorableDraft(draft: LocalDraft): boolean {
    if (!draft || typeof draft.payload !== 'object' || draft.payload === null) {
      return false;
    }

    const payload = draft.payload as { status?: unknown; instanceXml?: unknown; submissionXml?: unknown };
    if (payload.status === 'RuntimeLoaded') {
      return false;
    }

    return typeof payload.instanceXml === 'string' || typeof payload.submissionXml === 'string';
  }
}

export const draftStore = new DraftStore();
