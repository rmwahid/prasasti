import uuid
from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case


class CaseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, case: Case) -> Case:
        self.db.add(case)
        await self.db.flush()
        await self.db.refresh(case)
        return case

    async def get_by_id(self, case_id: uuid.UUID) -> Case | None:
        result = await self.db.execute(select(Case).where(Case.id == case_id))
        return result.scalar_one_or_none()

    async def get_list(
        self,
        person_id: uuid.UUID | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[Sequence[Case], int]:
        query = select(Case)
        count_query = select(func.count()).select_from(Case)

        if person_id:
            query = query.where(Case.person_id == person_id)
            count_query = count_query.where(Case.person_id == person_id)

        total = (await self.db.execute(count_query)).scalar()

        query = query.order_by(Case.case_date.desc().nullslast())
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        items = result.scalars().all()

        return items, total

    async def update(self, case: Case) -> Case:
        await self.db.flush()
        await self.db.refresh(case)
        return case

    async def delete(self, case: Case) -> None:
        await self.db.delete(case)
        await self.db.flush()

    async def get_by_person_id(self, person_id: uuid.UUID) -> list[Case]:
        result = await self.db.execute(
            select(Case).where(Case.person_id == person_id).order_by(Case.case_date.desc().nullslast())
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(Case))
        return result.scalar()
