from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.ml.engine import create_engine, FaceEngineBase


@lru_cache()
def get_face_engine() -> FaceEngineBase:
    """Singleton: load face model once, reuse across requests."""
    return create_engine()


async def get_db_session() -> AsyncSession:
    async for session in get_db():
        yield session


DbDep = Annotated[AsyncSession, Depends(get_db_session)]
EngineDep = Annotated[FaceEngineBase, Depends(get_face_engine)]
