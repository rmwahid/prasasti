import uuid

from fastapi import APIRouter, HTTPException, Query

from app.api.deps import DbDep
from app.schemas.person import PersonCreate, PersonUpdate, PersonResponse, PersonListResponse
from app.services.person_service import PersonService

router = APIRouter(prefix="/persons", tags=["persons"])


@router.get("", response_model=PersonListResponse)
async def list_persons(
    db: DbDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
):
    svc = PersonService(db)
    return await svc.get_list(page, page_size, search)


@router.post("", response_model=PersonResponse, status_code=201)
async def create_person(db: DbDep, data: PersonCreate):
    svc = PersonService(db)
    person = await svc.create(data)
    return PersonResponse.model_validate(person)


@router.get("/{person_id}", response_model=PersonResponse)
async def get_person(db: DbDep, person_id: uuid.UUID):
    svc = PersonService(db)
    person = await svc.get_by_id(person_id)
    if not person:
        raise HTTPException(404, "Person not found")
    return PersonResponse.model_validate(person)


@router.patch("/{person_id}", response_model=PersonResponse)
async def update_person(db: DbDep, person_id: uuid.UUID, data: PersonUpdate):
    svc = PersonService(db)
    try:
        person = await svc.update(person_id, data)
    except ValueError:
        raise HTTPException(404, "Person not found")
    return PersonResponse.model_validate(person)


@router.delete("/{person_id}", status_code=204)
async def delete_person(db: DbDep, person_id: uuid.UUID):
    svc = PersonService(db)
    try:
        await svc.delete(person_id)
    except ValueError:
        raise HTTPException(404, "Person not found")
