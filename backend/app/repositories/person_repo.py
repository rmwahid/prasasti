import uuid
from typing import Sequence

from sqlalchemy import select, func, or_, String
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.person import Person


class PersonRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, person: Person) -> Person:
        self.db.add(person)
        await self.db.flush()
        await self.db.refresh(person)
        return person

    async def get_by_id(self, person_id: uuid.UUID) -> Person | None:
        result = await self.db.execute(select(Person).where(Person.id == person_id))
        return result.scalar_one_or_none()

    async def get_list(
        self, page: int = 1, page_size: int = 20, search: str | None = None
    ) -> tuple[Sequence[Person], int]:
        query = select(Person)
        count_query = select(func.count()).select_from(Person)

        if search:
            pattern = f"%{search}%"
            condition = or_(
                Person.name.ilike(pattern),
                Person.alias.ilike(pattern),
            )
            query = query.where(condition)
            count_query = count_query.where(condition)

        # Count
        total = (await self.db.execute(count_query)).scalar()

        # Paginate
        query = query.order_by(Person.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        items = result.scalars().all()

        return items, total

    async def update(self, person: Person) -> Person:
        await self.db.flush()
        await self.db.refresh(person)
        return person

    async def delete(self, person: Person) -> None:
        await self.db.delete(person)
        await self.db.flush()

    async def count(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(Person))
        return result.scalar()
