from sqlalchemy.ext.asyncio import AsyncSession

import numpy as np

from app.core.logging import logger
from app.core.config import settings
from app.repositories.embedding_repo import EmbeddingRepository
from app.repositories.case_repo import CaseRepository


class FaceMatcher:
    """Search DB for similar face embeddings."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.embedding_repo = EmbeddingRepository(db)
        self.case_repo = CaseRepository(db)

    async def find_similar(
        self,
        query_vector: np.ndarray,
        top_k: int | None = None,
        threshold: float | None = None,
    ) -> list[dict]:
        """Find similar faces in DB.

        Returns list of dicts:
            person_id, person_name, person_alias, person_photo_url, score, cases
        """
        top_k = top_k or settings.face_top_k
        threshold = threshold or settings.face_match_threshold

        query_list = query_vector.tolist()
        matches = await self.embedding_repo.find_similar(
            query_vector=query_list,
            top_k=top_k,
            threshold=threshold,
        )

        # Attach cases for each matched person
        for match in matches:
            cases = await self.case_repo.get_by_person_id(match["person_id"])
            match["cases"] = [
                {
                    "id": str(c.id),
                    "title": c.title,
                    "description": c.description,
                    "source_url": c.source_url,
                    "case_date": c.case_date.isoformat() if c.case_date else None,
                    "category": c.category,
                }
                for c in cases
            ]

        logger.info(f"Face search: {len(matches)} matches found (threshold={threshold})")
        return matches
