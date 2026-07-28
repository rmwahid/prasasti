<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { api } from '$lib/api';
  import type { Person, Case } from '../../$types';

  let person = $state<Person | null>(null);
  let cases = $state<Case[]>([]);
  let loading = $state(true);
  const id = $derived($page.params.id);

  async function load() {
    person = await api.getPerson(id) as any;
    const res = await api.getCases(1, 100, id) as any;
    cases = res.items;
    loading = false;
  }

  onMount(load);

  async function save() {
    await api.updatePerson(id, {
      name: person!.name,
      alias: person!.alias,
      bio: person!.bio,
      photo_url: person!.photo_url,
    });
    alert('Saved');
  }

  async function removeCase(caseId: string) {
    if (!confirm('Delete this case?')) return;
    await api.deleteCase(caseId);
    load();
  }
</script>

<div class="p-6">
  {#if loading}
    <p>Loading...</p>
  {:else if person}
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-800">{person.name}</h2>
      <a href="/persons" class="text-sm text-blue-600 hover:underline">Back to list</a>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-1 bg-white rounded-lg p-5 shadow-sm border">
        <h3 class="font-semibold text-gray-700 mb-4">Edit Person</h3>
        <label class="block text-sm text-gray-600 mb-1">Name</label>
        <input bind:value={person.name} class="w-full border rounded px-3 py-2 text-sm mb-3" />

        <label class="block text-sm text-gray-600 mb-1">Alias</label>
        <input bind:value={person.alias} class="w-full border rounded px-3 py-2 text-sm mb-3" />

        <label class="block text-sm text-gray-600 mb-1">Bio</label>
        <textarea bind:value={person.bio} rows="4" class="w-full border rounded px-3 py-2 text-sm mb-3"></textarea>

        <label class="block text-sm text-gray-600 mb-1">Photo URL</label>
        <input bind:value={person.photo_url} class="w-full border rounded px-3 py-2 text-sm mb-4" />

        <button onclick={save} class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700 w-full">Save</button>
      </div>

      <div class="lg:col-span-2">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-700">Cases</h3>
          <a href="/cases/new?person_id={id}" class="bg-gray-900 text-white px-3 py-1.5 rounded text-sm hover:bg-gray-700">+ Add Case</a>
        </div>

        {#if cases.length === 0}
          <p class="text-gray-400">No cases yet.</p>
        {:else}
          <div class="space-y-3">
            {#each cases as c}
              <div class="bg-white rounded-lg p-4 shadow-sm border">
                <div class="flex justify-between items-start">
                  <div>
                    <p class="font-medium text-gray-800">{c.title}</p>
                    {#if c.description}
                      <p class="text-sm text-gray-500 mt-1 line-clamp-2">{c.description}</p>
                    {/if}
                    <div class="flex gap-3 mt-2 text-xs text-gray-400">
                      {#if c.category}<span class="bg-gray-100 px-2 py-0.5 rounded">{c.category}</span>{/if}
                      {#if c.case_date}<span>{new Date(c.case_date).toLocaleDateString('id-ID')}</span>{/if}
                      {#if c.source_url}
                        <a href={c.source_url} target="_blank" class="text-blue-500 hover:underline">Source</a>
                      {/if}
                    </div>
                  </div>
                  <button onclick={() => removeCase(c.id)} class="text-red-500 text-sm hover:underline">Delete</button>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </div>
    </div>
  {/if}
</div>
