import uuid

from fastapi import APIRouter, HTTPException, Query

from app.api.deps import DbDep
from app.schemas.case import CaseCreate, CaseUpdate, CaseResponse, CaseListResponse
from app.services.case_service import CaseService

router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("", response_model=CaseListResponse)
async def list_cases(
    db: DbDep,
    person_id: uuid.UUID | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    svc = CaseService(db)
    return await svc.get_list(person_id, page, page_size)


@router.post("", response_model=CaseResponse, status_code=201)
async def create_case(db: DbDep, data: CaseCreate):
    svc = CaseService(db)
    case = await svc.create(data)
    return CaseResponse.model_validate(case)


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(db: DbDep, case_id: uuid.UUID):
    svc = CaseService(db)
    case = await svc.get_by_id(case_id)
    if not case:
        raise HTTPException(404, "Case not found")
    return CaseResponse.model_validate(case)


@router.patch("/{case_id}", response_model=CaseResponse)
async def update_case(db: DbDep, case_id: uuid.UUID, data: CaseUpdate):
    svc = CaseService(db)
    try:
        case = await svc.update(case_id, data)
    except ValueError:
        raise HTTPException(404, "Case not found")
    return CaseResponse.model_validate(case)


@router.delete("/{case_id}", status_code=204)
async def delete_case(db: DbDep, case_id: uuid.UUID):
    svc = CaseService(db)
    try:
        await svc.delete(case_id)
    except ValueError:
        raise HTTPException(404, "Case not found")
