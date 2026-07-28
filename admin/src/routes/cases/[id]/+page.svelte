<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { api } from '$lib/api';
  import type { Case, Person } from '../../$types';

  let c = $state<Case | null>(null);
  let persons = $state<Person[]>([]);
  let loading = $state(true);
  const id = $derived($page.params.id);

  onMount(async () => {
    const [caseRes, persRes] = await Promise.all([
      fetch(`/api/v1/cases/${id}`).then(r => r.json()),
      api.getPersons(1, 1000)
    ]) as any;
    c = caseRes;
    persons = persRes.items;
    loading = false;
  });

  async function save() {
    await api.updateCase(id, { title: c!.title, description: c!.description, source_url: c!.source_url, case_date: c!.case_date, category: c!.category });
    alert('Saved');
  }
</script>

<div class="p-6 max-w-xl">
  {#if loading}
    <p>Loading...</p>
  {:else if c}
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Edit Case</h2>
    <label class="block text-sm text-gray-600 mb-1">Person</label>
    <input value={persons.find(p => p.id === c.person_id)?.name || ''} disabled class="w-full border rounded px-3 py-2 text-sm mb-3 bg-gray-50" />

    <label class="block text-sm text-gray-600 mb-1">Title</label>
    <input bind:value={c.title} class="w-full border rounded px-3 py-2 text-sm mb-3" />

    <label class="block text-sm text-gray-600 mb-1">Description</label>
    <textarea bind:value={c.description} rows="4" class="w-full border rounded px-3 py-2 text-sm mb-3"></textarea>

    <label class="block text-sm text-gray-600 mb-1">Source URL</label>
    <input bind:value={c.source_url} class="w-full border rounded px-3 py-2 text-sm mb-3" />

    <label class="block text-sm text-gray-600 mb-1">Case Date</label>
    <input type="date" bind:value={c.case_date} class="w-full border rounded px-3 py-2 text-sm mb-3" />

    <label class="block text-sm text-gray-600 mb-1">Category</label>
    <input bind:value={c.category} class="w-full border rounded px-3 py-2 text-sm mb-4" />

    <div class="flex gap-3">
      <button onclick={save} class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700">Save</button>
      <a href="/persons/{c.person_id}" class="border px-4 py-2 rounded text-sm hover:bg-gray-50">Back</a>
    </div>
  {/if}
</div>
