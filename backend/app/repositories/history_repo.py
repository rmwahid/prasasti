import uuid
from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.search_history import SearchHistory


class HistoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, history: SearchHistory) -> SearchHistory:
        self.db.add(history)
        await self.db.flush()
        await self.db.refresh(history)
        return history

    async def get_list(
        self,
        device_id: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[Sequence[SearchHistory], int]:
        query = select(SearchHistory)
        count_query = select(func.count()).select_from(SearchHistory)

        if device_id:
            query = query.where(SearchHistory.device_id == device_id)
            count_query = count_query.where(SearchHistory.device_id == device_id)

        total = (await self.db.execute(count_query)).scalar()

        query = query.order_by(SearchHistory.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        items = result.scalars().all()

        return items, total

    async def count(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(SearchHistory))
        return result.scalar()

    async def get_top_matched_persons(self, limit: int = 10) -> list[dict]:
        """Return persons most frequently matched in search history."""
        sql = text("""
            SELECT
                sh.top_match_person_id AS person_id,
                p.name AS person_name,
                p.photo_url AS person_photo_url,
                COUNT(*) AS match_count
            FROM search_history sh
            JOIN persons p ON p.id = sh.top_match_person_id
            WHERE sh.top_match_person_id IS NOT NULL
            GROUP BY sh.top_match_person_id, p.name, p.photo_url
            ORDER BY match_count DESC
            LIMIT :limit
        """)
        result = await self.db.execute(sql, {"limit": limit})
        return [
            {
                "person_id": row.person_id,
                "person_name": row.person_name,
                "person_photo_url": row.person_photo_url,
                "match_count": row.match_count,
            }
            for row in result.fetchall()
        ]
