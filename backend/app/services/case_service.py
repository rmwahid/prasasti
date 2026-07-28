import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case
from app.repositories.case_repo import CaseRepository
from app.schemas.case import CaseCreate, CaseUpdate, CaseResponse, CaseListResponse, CaseWithPerson
from app.schemas.person import PersonResponse


class CaseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CaseRepository(db)

    async def create(self, data: CaseCreate) -> Case:
        case = Case(**data.model_dump())
        return await self.repo.create(case)

    async def get_by_id(self, case_id: uuid.UUID) -> Case | None:
        return await self.repo.get_by_id(case_id)

    async def get_list(
        self,
        person_id: uuid.UUID | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> CaseListResponse:
        items, total = await self.repo.get_list(person_id, page, page_size)
        return CaseListResponse(
            items=[CaseResponse.model_validate(c) for c in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def get_by_person_id(self, person_id: uuid.UUID) -> list[Case]:
        return await self.repo.get_by_person_id(person_id)

    async def update(self, case_id: uuid.UUID, data: CaseUpdate) -> Case:
        case = await self.repo.get_by_id(case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(case, key, value)
        return await self.repo.update(case)

    async def delete(self, case_id: uuid.UUID) -> None:
        case = await self.repo.get_by_id(case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")
        await self.repo.delete(case)