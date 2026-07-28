import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.person import Person
from app.repositories.person_repo import PersonRepository
from app.schemas.person import PersonCreate, PersonUpdate, PersonResponse, PersonListResponse


class PersonService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = PersonRepository(db)

    async def create(self, data: PersonCreate) -> Person:
        person = Person(**data.model_dump())
        return await self.repo.create(person)

    async def get_by_id(self, person_id: uuid.UUID) -> Person | None:
        return await self.repo.get_by_id(person_id)

    async def get_list(
        self, page: int = 1, page_size: int = 20, search: str | None = None
    ) -> PersonListResponse:
        items, total = await self.repo.get_list(page, page_size, search)
        return PersonListResponse(
            items=[PersonResponse.model_validate(p) for p in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def update(self, person_id: uuid.UUID, data: PersonUpdate) -> Person:
        person = await self.repo.get_by_id(person_id)
        if not person:
            raise ValueError(f"Person {person_id} not found")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(person, key, value)
        return await self.repo.update(person)

    async def delete(self, person_id: uuid.UUID) -> None:
        person = await self.repo.get_by_id(person_id)
        if not person:
            raise ValueError(f"Person {person_id} not found")
        await self.repo.delete(person)
