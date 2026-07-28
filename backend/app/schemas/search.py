from datetime import datetime
import uuid

from pydantic import BaseModel, Field


class SearchMatch(BaseModel):
    person_id: uuid.UUID
    person_name: str | None
    person_photo_url: str | None
    score: float
    cases: list[dict] | None = None


class SearchResponse(BaseModel):
    matches: list[SearchMatch]
    query_photo_url: str | None
    searched_at: datetime


class EmbeddingInject(BaseModel):
    person_id: uuid.UUID
    vector: list[float] = Field(..., min_length=512, max_length=512)
    source_photo_url: str | None = None
    model_version: str | None = None
