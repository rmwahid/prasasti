from datetime import date, datetime
import uuid

from pydantic import BaseModel, Field


class CaseCreate(BaseModel):
    person_id: uuid.UUID
    title: str = Field(..., max_length=500)
    description: str | None = None
    source_url: str | None = Field(None, max_length=1000)
    case_date: date | None = None
    category: str | None = Field(None, max_length=100)


class CaseUpdate(BaseModel):
    title: str | None = Field(None, max_length=500)
    description: str | None = None
    source_url: str | None = Field(None, max_length=1000)
    case_date: date | None = None
    category: str | None = Field(None, max_length=100)


class CaseResponse(BaseModel):
    id: uuid.UUID
    person_id: uuid.UUID
    title: str
    description: str | None
    source_url: str | None
    case_date: date | None
    category: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class CaseWithPerson(CaseResponse):
    person: "PersonResponse"

    model_config = {"from_attributes": True}


class CaseListResponse(BaseModel):
    items: list[CaseResponse]
    total: int
    page: int
    page_size: int


from app.schemas.person import PersonResponse  # noqa: E402
CaseWithPerson.model_rebuild()