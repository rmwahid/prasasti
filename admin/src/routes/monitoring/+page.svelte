<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '$lib/api';
  import type { StatsResponse } from '../$types';

  let stats = $state<StatsResponse | null>(null);
  let loading = $state(true);

  onMount(async () => {
    stats = await api.getStats() as any;
    loading = false;
  });
</script>

<div class="p-6">
  <h2 class="text-2xl font-bold text-gray-800 mb-6">Monitoring</h2>

  {#if loading}
    <p>Loading...</p>
  {:else if stats}
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white rounded-lg p-5 shadow-sm border">
        <h3 class="font-semibold text-gray-700 mb-4">Summary</h3>
        <div class="space-y-3 text-sm">
          <div class="flex justify-between"><span class="text-gray-500">Total Persons</span><span class="font-medium">{stats.total_persons}</span></div>
          <div class="flex justify-between"><span class="text-gray-500">Total Cases</span><span class="font-medium">{stats.total_cases}</span></div>
          <div class="flex justify-between"><span class="text-gray-500">Total Embeddings</span><span class="font-medium">{stats.total_embeddings}</span></div>
          <div class="flex justify-between"><span class="text-gray-500">Total Searches</span><span class="font-medium">{stats.total_searches}</span></div>
        </div>
      </div>

      <div class="bg-white rounded-lg p-5 shadow-sm border">
        <h3 class="font-semibold text-gray-700 mb-4">Top Matched Persons</h3>
        {#if stats.top_matched_persons.length === 0}
          <p class="text-gray-400 text-sm">No data yet.</p>
        {:else}
          <table class="w-full text-sm">
            <thead class="text-left text-gray-500 border-b">
              <tr><th class="pb-2">Name</th><th class="pb-2 text-right">Matches</th></tr>
            </thead>
            <tbody>
              {#each stats.top_matched_persons as p}
                <tr class="border-b border-gray-50">
                  <td class="py-2 font-medium">{p.person_name}</td>
                  <td class="py-2 text-right">{p.match_count}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}
      </div>
    </div>
  {/if}
</div>
