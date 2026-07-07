from fastapi import APIRouter, Depends

from app.db.session import get_db
from app.modules.code_chunks.schemas import ChunkRequest
from app.modules.code_chunks.service import CodeChunkService

router = APIRouter(
    prefix="/chunks",
    tags=["Code Chunks"],
)


@router.post("/build")
async def build_chunks(
    payload: ChunkRequest,
    db=Depends(get_db),
):

    total = await CodeChunkService.build_chunks(
        db,
        payload.repository_id,
    )

    return {
        "chunks": total,
    }