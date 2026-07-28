<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/api';

  let name = $state('');
  let alias = $state('');
  let bio = $state('');
  let photo_url = $state('');
  let saving = $state(false);

  async function save() {
    saving = true;
    try {
      const p = await api.createPerson({ name, alias: alias || null, bio: bio || null, photo_url: photo_url || null }) as any;
      goto(`/persons/${p.id}`);
    } catch (e: any) {
      alert(e.message);
    }
    saving = false;
  }
</script>

<div class="p-6 max-w-xl">
  <h2 class="text-2xl font-bold text-gray-800 mb-6">Add Person</h2>

  <label class="block text-sm text-gray-600 mb-1">Name *</label>
  <input bind:value={name} class="w-full border rounded px-3 py-2 text-sm mb-3" />

  <label class="block text-sm text-gray-600 mb-1">Alias</label>
  <input bind:value={alias} class="w-full border rounded px-3 py-2 text-sm mb-3" />

  <label class="block text-sm text-gray-600 mb-1">Bio</label>
  <textarea bind:value={bio} rows="4" class="w-full border rounded px-3 py-2 text-sm mb-3"></textarea>

  <label class="block text-sm text-gray-600 mb-1">Photo URL</label>
  <input bind:value={photo_url} class="w-full border rounded px-3 py-2 text-sm mb-4" />

  <div class="flex gap-3">
    <button onclick={save} disabled={!name || saving} class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700 disabled:opacity-40">Save</button>
    <a href="/persons" class="border px-4 py-2 rounded text-sm hover:bg-gray-50">Cancel</a>
  </div>
</div>
