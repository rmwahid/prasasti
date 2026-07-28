from datetime import datetime
import uuid

from pydantic import BaseModel


class SearchHistoryResponse(BaseModel):
    id: uuid.UUID
    device_id: str
    photo_url: str | None
    top_match_person_id: uuid.UUID | None
    top_match_score: float | None
    created_at: datetime

    model_config = {"from_attributes": True}


class SearchHistoryListResponse(BaseModel):
    items: list[SearchHistoryResponse]
    total: int
    page: int
    page_size: int


class TopMatchedPerson(BaseModel):
    person_id: uuid.UUID
    person_name: str
    match_count: int


class StatsResponse(BaseModel):
    total_persons: int
    total_cases: int
    total_embeddings: int
    total_searches: int
    top_matched_persons: list[TopMatchedPerson]
