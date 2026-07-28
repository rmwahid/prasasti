import uuid
from io import BytesIO
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import logger
from app.models.embedding import Embedding
from app.models.search_history import SearchHistory
from app.repositories.embedding_repo import EmbeddingRepository
from app.repositories.history_repo import HistoryRepository
from app.schemas.search import EmbeddingInject
from app.ml.extractor import FaceExtractor
from app.ml.matcher import FaceMatcher
from app.ml.engine import FaceEngineBase


class FaceService:
    def __init__(self, db: AsyncSession, engine: FaceEngineBase):
        self.db = db
        self.extractor = FaceExtractor(engine)
        self.embedding_repo = EmbeddingRepository(db)
        self.history_repo = HistoryRepository(db)

    async def search(
        self,
        image_bytes: bytes,
        device_id: str | None = None,
        top_k: int | None = None,
        threshold: float | None = None,
    ) -> dict:
        """Full search pipeline: extract embedding -> find matches -> save history."""
        embedding = self.extractor.extract(image_bytes)
        if embedding is None:
            return {"matches": [], "error": "No face detected"}

        matcher = FaceMatcher(self.db)
        matches = await matcher.find_similar(embedding, top_k, threshold)

        # Save search history
        top_match = matches[0] if matches else None
        history = SearchHistory(
            device_id=device_id,
            top_match_person_id=uuid.UUID(top_match["person_id"]) if top_match else None,
            top_match_score=top_match["score"] if top_match else None,
        )
        await self.history_repo.create(history)

        return {"matches": matches}

    async def inject_embedding(self, data: EmbeddingInject) -> Embedding:
        """Manually inject an embedding (from training output)."""
        embedding = Embedding(
            person_id=data.person_id,
            vector=data.vector,
            model_version=data.model_version,
            source_photo_url=data.source_photo_url,
        )
        return await self.embedding_repo.create(embedding)

    async def inject_embedding_batch(
        self, person_id: uuid.UUID, vectors: list[list[float]], model_version: str
    ) -> list[Embedding]:
        """Inject multiple embeddings for one person."""
        embeddings = [
            Embedding(
                person_id=person_id,
                vector=vec,
                model_version=model_version,
            )
            for vec in vectors
        ]
        return await self.embedding_repo.create_batch(embeddings)

    async def delete_embeddings_by_person(self, person_id: uuid.UUID) -> int:
        return await self.embedding_repo.delete_by_person_id(person_id)
