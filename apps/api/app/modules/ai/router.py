from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.ai.schemas import AIQuestion, AIAnswer
from app.modules.ai.service import AIService

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/ask",
    response_model=AIAnswer,
)
async def ask(
    request: AIQuestion,
    db: AsyncSession = Depends(get_db),
):

    answer = await AIService.ask(
        db=db,
        repository_id=request.repository_id,
        question=request.question,
    )

    return AIAnswer(
        answer=answer
    )