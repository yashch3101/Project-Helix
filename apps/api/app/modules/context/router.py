from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.context.schemas import ContextRequest
from app.modules.context.service import ContextService

router = APIRouter(
    prefix="/context",
    tags=["Context"],
)


@router.post("/build")
async def build_context(
    payload: ContextRequest,
    db: AsyncSession = Depends(get_db),
):

    return await ContextService.build(
        db=db,
        repository_id=payload.repository_id,
        query=payload.query,
        top_k=payload.top_k,
    )