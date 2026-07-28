import uuid
import numpy as np

from sqlalchemy import select, func, delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.embedding import Embedding


class EmbeddingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, embedding: Embedding) -> Embedding:
        self.db.add(embedding)
        await self.db.flush()
        await self.db.refresh(embedding)
        return embedding

    async def create_batch(self, embeddings: list[Embedding]) -> list[Embedding]:
        self.db.add_all(embeddings)
        await self.db.flush()
        for e in embeddings:
            await self.db.refresh(e)
        return embeddings

    async def get_by_person_id(self, person_id: uuid.UUID) -> list[Embedding]:
        result = await self.db.execute(
            select(Embedding).where(Embedding.person_id == person_id)
        )
        return list(result.scalars().all())

    async def delete_by_person_id(self, person_id: uuid.UUID) -> int:
        result = await self.db.execute(
            delete(Embedding).where(Embedding.person_id == person_id)
        )
        await self.db.flush()
        return result.rowcount

    async def find_similar(
        self,
        query_vector: list[float],
        top_k: int = 5,
        threshold: float = 0.6,
    ) -> list[dict]:
        """Cosine similarity search using pgvector.

        Returns list of dicts with keys:
          person_id, person_name, person_alias, person_photo_url, score, embedding_id
        """
        vec_str = "[" + ",".join(str(v) for v in query_vector) + "]"

        sql = text("""
            SELECT
                e.id AS embedding_id,
                e.person_id,
                p.name AS person_name,
                p.alias AS person_alias,
                p.photo_url AS person_photo_url,
                1 - (e.vector <=> :vec::vector) AS score
            FROM embeddings e
            JOIN persons p ON p.id = e.person_id
            WHERE 1 - (e.vector <=> :vec::vector) >= :threshold
            ORDER BY e.vector <=> :vec::vector
            LIMIT :top_k
        """)

        result = await self.db.execute(
            sql,
            {"vec": vec_str, "threshold": threshold, "top_k": top_k},
        )
        rows = result.fetchall()
        return [
            {
                "embedding_id": row.embedding_id,
                "person_id": row.person_id,
                "person_name": row.person_name,
                "person_alias": row.person_alias,
                "person_photo_url": row.person_photo_url,
                "score": float(row.score),
            }
            for row in rows
        ]

    async def count(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(Embedding))
        return result.scalar()
