<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { api } from '$lib/api';
  import type { Person } from '../../$types';

  let persons = $state<Person[]>([]);
  let person_id = $state('');
  let title = $state('');
  let description = $state('');
  let source_url = $state('');
  let case_date = $state('');
  let category = $state('');
  let saving = $state(false);

  onMount(async () => {
    const pid = $page.url.searchParams.get('person_id');
    if (pid) person_id = pid;
    const res = await api.getPersons(1, 1000) as any;
    persons = res.items;
  });

  async function save() {
    saving = true;
    try {
      const c = await api.createCase({
        person_id,
        title,
        description: description || null,
        source_url: source_url || null,
        case_date: case_date || null,
        category: category || null,
      }) as any;
      goto(`/persons/${person_id}`);
    } catch (e: any) { alert(e.message); }
    saving = false;
  }
</script>

<div class="p-6 max-w-xl">
  <h2 class="text-2xl font-bold text-gray-800 mb-6">Add Case</h2>

  <label class="block text-sm text-gray-600 mb-1">Person *</label>
  <select bind:value={person_id} class="w-full border rounded px-3 py-2 text-sm mb-3">
    <option value="">Select person...</option>
    {#each persons as p}
      <option value={p.id}>{p.name}</option>
    {/each}
  </select>

  <label class="block text-sm text-gray-600 mb-1">Title *</label>
  <input bind:value={title} class="w-full border rounded px-3 py-2 text-sm mb-3" />

  <label class="block text-sm text-gray-600 mb-1">Description</label>
  <textarea bind:value={description} rows="4" class="w-full border rounded px-3 py-2 text-sm mb-3"></textarea>

  <label class="block text-sm text-gray-600 mb-1">Source URL</label>
  <input bind:value={source_url} class="w-full border rounded px-3 py-2 text-sm mb-3" />

  <label class="block text-sm text-gray-600 mb-1">Case Date</label>
  <input type="date" bind:value={case_date} class="w-full border rounded px-3 py-2 text-sm mb-3" />

  <label class="block text-sm text-gray-600 mb-1">Category</label>
  <input bind:value={category} placeholder="Korupsi, Suap, Penggelapan..." class="w-full border rounded px-3 py-2 text-sm mb-4" />

  <div class="flex gap-3">
    <button onclick={save} disabled={!person_id || !title || saving} class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700 disabled:opacity-40">Save</button>
    <a href="/cases" class="border px-4 py-2 rounded text-sm hover:bg-gray-50">Cancel</a>
  </div>
</div>
