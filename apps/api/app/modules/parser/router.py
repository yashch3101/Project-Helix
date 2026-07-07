from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.parser.service import ParserService

router = APIRouter(
    prefix="/parser",
    tags=["Parser"],
)


@router.post("/{repository_id}")
async def parse_repository(
    repository_id: str,
    db: AsyncSession = Depends(get_db),
):

    return await ParserService.parse_repository(
        db,
        repository_id,
    )