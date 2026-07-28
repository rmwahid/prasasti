<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '$lib/api';
  import type { StatsResponse } from './$types';

  let stats = $state<StatsResponse | null>(null);
  let loading = $state(true);

  onMount(async () => {
    try {
      stats = await api.getStats();
    } catch (e) { console.error(e); }
    loading = false;
  });
</script>

<div class="p-6">
  <h2 class="text-2xl font-bold text-gray-800 mb-6">Dashboard</h2>

  {#if loading}
    <p>Loading...</p>
  {:else if stats}
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white rounded-lg p-5 shadow-sm border">
        <p class="text-sm text-gray-500">Persons</p>
        <p class="text-3xl font-bold text-gray-800 mt-1">{stats.total_persons}</p>
      </div>
      <div class="bg-white rounded-lg p-5 shadow-sm border">
        <p class="text-sm text-gray-500">Cases</p>
        <p class="text-3xl font-bold text-gray-800 mt-1">{stats.total_cases}</p>
      </div>
      <div class="bg-white rounded-lg p-5 shadow-sm border">
        <p class="text-sm text-gray-500">Embeddings</p>
        <p class="text-3xl font-bold text-gray-800 mt-1">{stats.total_embeddings}</p>
      </div>
      <div class="bg-white rounded-lg p-5 shadow-sm border">
        <p class="text-sm text-gray-500">Searches</p>
        <p class="text-3xl font-bold text-gray-800 mt-1">{stats.total_searches}</p>
      </div>
    </div>

    <div class="bg-white rounded-lg p-5 shadow-sm border">
      <h3 class="text-lg font-semibold text-gray-700 mb-4">Top Matched Persons</h3>
      {#if stats.top_matched_persons.length === 0}
        <p class="text-gray-400">No data yet.</p>
      {:else}
        <table class="w-full text-sm">
          <thead class="text-left text-gray-500 border-b">
            <tr><th class="pb-2">Name</th><th class="pb-2">Match Count</th></tr>
          </thead>
          <tbody>
            {#each stats.top_matched_persons as p}
              <tr class="border-b border-gray-100">
                <td class="py-2 font-medium">{p.person_name}</td>
                <td class="py-2">{p.match_count}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      {/if}
    </div>
  {/if}
</div>
