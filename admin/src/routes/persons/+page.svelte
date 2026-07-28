<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '$lib/api';
  import type { Person } from '../$types';

  let persons = $state<Person[]>([]);
  let total = $state(0);
  let page = $state(1);
  let search = $state('');
  let loading = $state(true);
  const pageSize = 20;

  async function load() {
    loading = true;
    try {
      const res = await api.getPersons(page, pageSize, search || undefined) as any;
      persons = res.items;
      total = res.total;
    } catch (e) { console.error(e); }
    loading = false;
  }

  onMount(load);
  $effect(() => { if (page > 1 || search) load(); });

  async function remove(id: string) {
    if (!confirm('Delete this person?')) return;
    await api.deletePerson(id);
    load();
  }
</script>

<div class="p-6">
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-2xl font-bold text-gray-800">Persons</h2>
    <a href="/persons/new" class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700">+ Add Person</a>
  </div>

  <div class="mb-4">
    <input
      type="text"
      bind:value={search}
      placeholder="Search name or alias..."
      class="border rounded px-3 py-2 text-sm w-64"
    />
  </div>

  {#if loading}
    <p class="text-gray-400">Loading...</p>
  {:else}
    <div class="bg-white rounded-lg shadow-sm border">
      <table class="w-full text-sm">
        <thead class="text-left text-gray-500 border-b bg-gray-50">
          <tr>
            <th class="px-4 py-3">Name</th>
            <th class="px-4 py-3">Alias</th>
            <th class="px-4 py-3">Cases</th>
            <th class="px-4 py-3">Created</th>
            <th class="px-4 py-3">Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each persons as p}
            <tr class="border-b border-gray-100 hover:bg-gray-50">
              <td class="px-4 py-3 font-medium">{p.name}</td>
              <td class="px-4 py-3 text-gray-500">{p.alias || '-'}</td>
              <td class="px-4 py-3">
                <a href="/persons/{p.id}" class="text-blue-600 hover:underline">View</a>
              </td>
              <td class="px-4 py-3 text-gray-400 text-xs">{new Date(p.created_at).toLocaleDateString('id-ID')}</td>
              <td class="px-4 py-3">
                <a href="/persons/{p.id}" class="text-blue-600 hover:underline mr-2">Edit</a>
                <button onclick={() => remove(p.id)} class="text-red-600 hover:underline">Delete</button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <div class="flex justify-between items-center mt-4 text-sm text-gray-500">
      <p>{total} total</p>
      <div class="flex gap-2">
        <button disabled={page <= 1} onclick={() => page--} class="px-3 py-1 border rounded disabled:opacity-30">Prev</button>
        <span class="px-3 py-1">{page}</span>
        <button disabled={page * pageSize >= total} onclick={() => page++} class="px-3 py-1 border rounded disabled:opacity-30">Next</button>
      </div>
    </div>
  {/if}
</div>
