from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import logger
from app.api.v1.router import v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: preload face model
    logger.info(f"Loading face engine: {settings.face_engine}")
    from app.api.deps import get_face_engine
    engine = get_face_engine()
    logger.info("Face engine ready")
    yield
    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title="Prasasti API",
    description="Indonesian Face Recognition for Crime Cases",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)
