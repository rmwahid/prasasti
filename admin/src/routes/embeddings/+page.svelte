<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '$lib/api';
  import type { Person } from '../$types';

  let persons = $state<Person[]>([]);
  let personId = $state('');
  let modelVersion = $state('facenet-vggface2');
  let vectorJson = $state('');
  let status = $state('');

  onMount(async () => {
    const res = await api.getPersons(1, 1000) as any;
    persons = res.items;
  });

  async function inject() {
    try {
      const vector = JSON.parse(vectorJson);
      await api.injectEmbedding({ person_id: personId, vector, model_version: modelVersion });
      status = 'Success: 1 embedding injected';
      vectorJson = '';
    } catch (e: any) {
      status = 'Error: ' + e.message;
    }
  }

  async function injectBatch() {
    try {
      const data = JSON.parse(vectorJson);
      await api.injectEmbeddingBatch({ person_id: personId, model_version: modelVersion, vectors: data });
      status = 'Success: ' + data.length + ' embeddings injected';
      vectorJson = '';
    } catch (e: any) {
      status = 'Error: ' + e.message;
    }
  }
</script>

<div class="p-6 max-w-2xl">
  <h2 class="text-2xl font-bold text-gray-800 mb-6">Inject Embeddings</h2>
  <p class="text-sm text-gray-500 mb-6">Paste embedding vectors from training output (RunPod).</p>

  <label class="block text-sm text-gray-600 mb-1">Person *</label>
  <select bind:value={personId} class="w-full border rounded px-3 py-2 text-sm mb-3">
    <option value="">Select person...</option>
    {#each persons as p}
      <option value={p.id}>{p.name}</option>
    {/each}
  </select>

  <label class="block text-sm text-gray-600 mb-1">Model Version</label>
  <input bind:value={modelVersion} class="w-full border rounded px-3 py-2 text-sm mb-3" />

  <label class="block text-sm text-gray-600 mb-1">Vector(s) *</label>
  <p class="text-xs text-gray-400 mb-1">Single: [0.12, -0.34, ...] | Batch: [[0.12, ...], [0.56, ...]]</p>
  <textarea bind:value={vectorJson} rows="8" placeholder='[0.123, -0.456, ...]' class="w-full border rounded px-3 py-2 text-sm mb-3 font-mono text-xs"></textarea>

  <div class="flex gap-3">
    <button onclick={inject} disabled={!personId || !vectorJson} class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700 disabled:opacity-40">Inject Single</button>
    <button onclick={injectBatch} disabled={!personId || !vectorJson} class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700 disabled:opacity-40">Inject Batch</button>
  </div>

  {#if status}
    <p class="mt-4 text-sm p-3 rounded {status.startsWith('Error') ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'}">{status}</p>
  {/if}
</div>
