<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '$lib/api';
  import type { Case } from '../$types';

  let cases = $state<Case[]>([]);
  let total = $state(0);
  let page = $state(1);
  let loading = $state(true);
  const pageSize = 20;

  async function load() {
    loading = true;
    try {
      const res = await api.getCases(page, pageSize) as any;
      cases = res.items;
      total = res.total;
    } catch (e) { console.error(e); }
    loading = false;
  }

  onMount(load);
  $effect(() => { if (page > 1) load(); });

  async function remove(id: string) {
    if (!confirm('Delete this case?')) return;
    await api.deleteCase(id);
    load();
  }
</script>

<div class="p-6">
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-2xl font-bold text-gray-800">Cases</h2>
    <a href="/cases/new" class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700">+ Add Case</a>
  </div>

  {#if loading}
    <p class="text-gray-400">Loading...</p>
  {:else}
    <div class="bg-white rounded-lg shadow-sm border">
      <table class="w-full text-sm">
        <thead class="text-left text-gray-500 border-b bg-gray-50">
          <tr>
            <th class="px-4 py-3">Title</th>
            <th class="px-4 py-3">Category</th>
            <th class="px-4 py-3">Date</th>
            <th class="px-4 py-3">Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each cases as c}
            <tr class="border-b border-gray-100 hover:bg-gray-50">
              <td class="px-4 py-3 font-medium">{c.title}</td>
              <td class="px-4 py-3 text-gray-500">{c.category || '-'}</td>
              <td class="px-4 py-3 text-gray-400 text-xs">{c.case_date ? new Date(c.case_date).toLocaleDateString('id-ID') : '-'}</td>
              <td class="px-4 py-3">
                <a href="/cases/{c.id}" class="text-blue-600 hover:underline mr-2">Edit</a>
                <button onclick={() => remove(c.id)} class="text-red-600 hover:underline">Delete</button>
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
