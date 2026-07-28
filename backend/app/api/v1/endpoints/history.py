import uuid

from fastapi import APIRouter, Query

from app.api.deps import DbDep
from app.schemas.history import SearchHistoryListResponse, SearchHistoryResponse, StatsResponse, TopMatchedPerson
from app.repositories.person_repo import PersonRepository
from app.repositories.case_repo import CaseRepository
from app.repositories.embedding_repo import EmbeddingRepository
from app.repositories.history_repo import HistoryRepository

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=SearchHistoryListResponse)
async def list_history(
    db: DbDep,
    device_id: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    repo = HistoryRepository(db)
    items, total = await repo.get_list(device_id, page, page_size)
    return SearchHistoryListResponse(
        items=[SearchHistoryResponse.model_validate(h) for h in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: DbDep):
    person_repo = PersonRepository(db)
    case_repo = CaseRepository(db)
    embedding_repo = EmbeddingRepository(db)
    history_repo = HistoryRepository(db)

    total_persons = await person_repo.count()
    total_cases = await case_repo.count()
    total_embeddings = await embedding_repo.count()
    total_searches = await history_repo.count()
    top_matched = await history_repo.get_top_matched_persons(10)

    return StatsResponse(
        total_persons=total_persons,
        total_cases=total_cases,
        total_embeddings=total_embeddings,
        total_searches=total_searches,
        top_matched_persons=[
            TopMatchedPerson(
                person_id=m["person_id"],
                person_name=m["person_name"],
                person_photo_url=m["person_photo_url"],
                match_count=m["match_count"],
            )
            for m in top_matched
        ],
    )
