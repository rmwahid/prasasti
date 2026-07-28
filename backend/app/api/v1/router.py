from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.persons import router as persons_router
from app.api.v1.endpoints.cases import router as cases_router
from app.api.v1.endpoints.search import router as search_router
from app.api.v1.endpoints.history import router as history_router

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(health_router)
v1_router.include_router(persons_router)
v1_router.include_router(cases_router)
v1_router.include_router(search_router)
v1_router.include_router(history_router)
