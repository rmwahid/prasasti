<script lang="ts">
  import type { Snippet } from 'svelte';
  let { children }: { children: Snippet } = $props();

  const nav = [
    { href: '/', label: 'Dashboard' },
    { href: '/persons', label: 'Persons' },
    { href: '/cases', label: 'Cases' },
    { href: '/embeddings', label: 'Embeddings' },
    { href: '/monitoring', label: 'Monitoring' },
  ];

  let open = $state(true);
</script>

<div class="flex h-screen bg-gray-50">
  <aside class="w-64 bg-gray-900 text-white flex flex-col">
    <div class="p-4 border-b border-gray-700">
      <h1 class="text-xl font-bold tracking-tight">PRASASTI</h1>
      <p class="text-xs text-gray-400 mt-1">Admin Panel</p>
    </div>
    <nav class="flex-1 py-4">
      {#each nav as item}
        <a
          href={item.href}
          class="block px-4 py-2.5 text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
        >
          {item.label}
        </a>
      {/each}
    </nav>
    <div class="p-4 border-t border-gray-700 text-xs text-gray-500">
      v0.1.0
    </div>
  </aside>

  <main class="flex-1 overflow-auto">
    {@render children()}
  </main>
</div>
