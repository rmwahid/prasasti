const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request<T>(path: string, opts?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}/api/v1${path}`, {
    headers: { 'Content-Type': 'application/json', ...opts?.headers },
    ...opts
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}

export const api = {
  // Persons
  getPersons: (page = 1, pageSize = 20, search?: string) =>
    request(`/persons?page=${page}&page_size=${pageSize}${search ? `&search=${search}` : ''}`),
  getPerson: (id: string) => request(`/persons/${id}`),
  createPerson: (data: object) => request('/persons', { method: 'POST', body: JSON.stringify(data) }),
  updatePerson: (id: string, data: object) => request(`/persons/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  deletePerson: (id: string) => request(`/persons/${id}`, { method: 'DELETE' }),

  // Cases
  getCases: (page = 1, pageSize = 20, personId?: string) =>
    request(`/cases?page=${page}&page_size=${pageSize}${personId ? `&person_id=${personId}` : ''}`),
  createCase: (data: object) => request('/cases', { method: 'POST', body: JSON.stringify(data) }),
  updateCase: (id: string, data: object) => request(`/cases/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  deleteCase: (id: string) => request(`/cases/${id}`, { method: 'DELETE' }),

  // Embeddings
  injectEmbedding: (data: object) => request('/search/embeddings', { method: 'POST', body: JSON.stringify(data) }),
  injectEmbeddingBatch: (data: object) => request('/search/embeddings/batch', { method: 'POST', body: JSON.stringify(data) }),

  // Stats
  getStats: () => request('/history/stats'),
};
