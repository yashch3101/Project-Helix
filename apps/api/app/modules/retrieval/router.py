from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.retrieval.schemas import SearchRequest
from app.modules.retrieval.service import RetrievalService

router = APIRouter(
    prefix="/retrieval",
    tags=["Retrieval"],
)


@router.post("/search")
async def search(
    payload: SearchRequest,
    db: AsyncSession = Depends(get_db),
):

    results = await RetrievalService.search(
        db=db,
        repository_id=payload.repository_id,
        query=payload.query,
        top_k=payload.top_k,
    )

    return [
        {
            "score": round(item["score"], 4),
            "chunk_id": item["chunk_id"],
            "chunk_name": item["chunk_name"],
            "chunk_type": item["chunk_type"],
            "start_line": item["start_line"],
            "end_line": item["end_line"],
            "content": item["content"],
        }
        for item in results
    ]