from datetime import datetime
import uuid

from pydantic import BaseModel, Field


class PersonCreate(BaseModel):
    name: str = Field(..., max_length=255)
    alias: str | None = Field(None, max_length=255)
    bio: str | None = None
    photo_url: str | None = Field(None, max_length=500)


class PersonUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    alias: str | None = Field(None, max_length=255)
    bio: str | None = None
    photo_url: str | None = Field(None, max_length=500)


class PersonResponse(BaseModel):
    id: uuid.UUID
    name: str
    alias: str | None
    bio: str | None
    photo_url: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PersonListResponse(BaseModel):
    items: list[PersonResponse]
    total: int
    page: int
    page_size: int
