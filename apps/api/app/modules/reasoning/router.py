from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.modules.reasoning.schemas import (
    ReasoningRequest,
)

from app.modules.reasoning.service import (
    ReasoningService,
)

router = APIRouter(
    prefix="/reasoning",
    tags=["Reasoning"],
)


@router.post("/build")
async def build_reasoning(

    payload: ReasoningRequest,

    db: AsyncSession = Depends(get_db),

):

    return await ReasoningService.build(

        db=db,

        repository_id=payload.repository_id,

        query=payload.query,

        top_k=payload.top_k,

    )