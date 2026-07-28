import json

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query

from app.api.deps import DbDep, EngineDep
from app.schemas.search import EmbeddingInject
from app.services.face_service import FaceService
from app.core.logging import logger

router = APIRouter(prefix="/search", tags=["search"])


@router.post("")
async def search_face(
    db: DbDep,
    engine: EngineDep,
    file: UploadFile = File(..., description="Photo to search"),
    device_id: str | None = Form(None),
    top_k: int | None = Query(None),
    threshold: float | None = Query(None),
):
    """Upload a photo and find matching persons in the database."""
    image_bytes = await file.read()

    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(413, "Image too large (max 10MB)")

    svc = FaceService(db, engine)
    result = await svc.search(
        image_bytes=image_bytes,
        device_id=device_id,
        top_k=top_k,
        threshold=threshold,
    )

    if "error" in result:
        return {"matches": [], "message": result["error"]}

    return result


@router.post("/embeddings", status_code=201)
async def inject_embedding(db: DbDep, data: EmbeddingInject):
    """Manually inject an embedding vector (from training output)."""
    svc = FaceService(db, engine=None)
    embedding = await svc.inject_embedding(data)
    return {"id": str(embedding.id), "person_id": str(embedding.person_id)}


@router.post("/embeddings/batch", status_code=201)
async def inject_embedding_batch(
    db: DbDep,
    body: dict,
):
    """Inject multiple embedding vectors for a person.

    Body: { "person_id": "...", "model_version": "...", "vectors": [[...], [...]] }
    """
    from uuid import UUID

    svc = FaceService(db, engine=None)
    person_id = UUID(body["person_id"])
    model_version = body.get("model_version", "facenet-vggface2")
    vectors = body["vectors"]

    embeddings = await svc.inject_embedding_batch(person_id, vectors, model_version)
    return {
        "injected": len(embeddings),
        "person_id": str(person_id),
    }


@router.delete("/embeddings/{person_id}", status_code=204)
async def delete_person_embeddings(db: DbDep, person_id):
    from uuid import UUID

    svc = FaceService(db, engine=None)
    count = await svc.delete_embeddings_by_person(UUID(person_id))
    if count == 0:
        raise HTTPException(404, "No embeddings found for this person")
