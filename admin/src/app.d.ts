export interface Person {
  id: string;
  name: string;
  alias: string | null;
  bio: string | null;
  photo_url: string | null;
  created_at: string;
  updated_at: string;
}

export interface Case {
  id: string;
  person_id: string;
  title: string;
  description: string | null;
  source_url: string | null;
  case_date: string | null;
  category: string | null;
  created_at: string;
}

export interface PersonListResponse {
  items: Person[];
  total: number;
  page: number;
  page_size: number;
}

export interface CaseListResponse {
  items: Case[];
  total: number;
  page: number;
  page_size: number;
}

export interface StatsResponse {
  total_persons: number;
  total_cases: number;
  total_embeddings: number;
  total_searches: number;
  top_matched_persons: { person_id: string; person_name: string; person_photo_url: string | null; match_count: number }[];
}
